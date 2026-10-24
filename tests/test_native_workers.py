"""Real Pi tools, extension worker and AgentShell with native-process doubles; no inference."""
import json
import os
import subprocess
import unittest
from pathlib import Path

from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings

NATIVE = r'''#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
args = sys.argv[1:]
name = Path(sys.argv[0]).name
sid = os.environ['NATIVE_REVIEW_ID' if name == 'claude' else 'NATIVE_IMPLEMENTATION_ID']
with open(os.environ['NATIVE_LOG'], 'a') as stream:
    stream.write(json.dumps({'name': name, 'args': args, 'cwd': os.getcwd(),
        'roster': os.environ.get('PI_AGENTSHELL_ROSTER_FILE'),
        'depth': os.environ.get('PI_AGENT_SHELL_DEPTH')}) + '\n')
if name == 'codex':
    print(json.dumps({'type': 'thread.started', 'thread_id': sid}))
    print(json.dumps({'type': 'item.completed', 'item': {
        'type': 'agent_message', 'text': 'Task 31: controlled process completed.'}}))
    print(json.dumps({'type': 'turn.completed', 'usage': {'output_tokens': 1}}))
elif name == 'claude':
    print(json.dumps({'type': 'assistant', 'message': {'content': [
        {'type': 'text', 'text': 'Task 32: controlled review completed.'}]}}))
    print(json.dumps({'type': 'result', 'is_error': False, 'session_id': sid}))
else:
    print(json.dumps({'type': 'session', 'id': sid}))
    print(json.dumps({'type': 'message_update', 'assistantMessageEvent': {
        'type': 'text_end', 'content': 'Task 31: controlled Pi process completed.'}}))
    print(json.dumps({'type': 'agent_end', 'messages': [
        {'role': 'assistant', 'stopReason': 'stop'}]}))
'''

PROBE = r'''
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
globalThis.fetch = async () => { throw new Error('Network forbidden in native worker probe'); };
const {DefaultResourceLoader, SettingsManager, SessionManager, createAgentSession} =
    await import(pathToFileURL(process.env.NATIVE_PI_SDK).href);
const cwd = process.env.PROBE_OWNER;
const agentDir = process.env.PI_CODING_AGENT_DIR;
const settingsManager = SettingsManager.inMemory({packages: []});
const selected = JSON.parse(fs.readFileSync(path.join(cwd, 'agent.json'), 'utf8')).agent.resources;
const loader = new DefaultResourceLoader({cwd, agentDir, settingsManager,
    additionalExtensionPaths: selected.extensions.map(p => path.resolve(cwd, p)),
    additionalSkillPaths: selected.skills.map(p => path.resolve(cwd, p)),
    noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true,
    disabledBuiltinExtensions: ['mcp'], noContextFiles: false, systemPrompt: ''});
await loader.reload();
if (loader.getExtensions().errors.length) throw new Error('Extension loading failed');
const sessionManager = SessionManager.inMemory(cwd);
const {session} = await createAgentSession({cwd, agentDir, settingsManager,
    sessionManager, resourceLoader: loader});
await session.bindExtensions({mode: 'json'});
const ctx = {cwd, mode: 'json', hasUI: false, sessionManager,
             ui: {setWidget() {}, notify() {}}, isIdle: () => true};
const tool = session.extensionRunner.getToolDefinition('subagent');
const roles = JSON.parse((await session.extensionRunner.getToolDefinition('subagent_roster')
    .execute('roster', {}, undefined, undefined, ctx)).content[0].text);
const results = [];
const prompts = {};
function skillFiles(selected) {
    if (fs.statSync(selected).isFile()) return [selected];
    return fs.readdirSync(selected, {withFileTypes: true}).flatMap(entry => {
        const file = path.join(selected, entry.name);
        return entry.isDirectory() ? skillFiles(file) : entry.name === 'SKILL.md' ? [file] : [];
    });
}
for (const role of ['implementation', 'review']) {
    const root = path.resolve(cwd, '..', role);
    const resources = JSON.parse(
        fs.readFileSync(path.join(root, 'agent.json'), 'utf8')).agent.resources;
    const skills = resources.skills.flatMap(p => skillFiles(path.resolve(root, p)));
    prompts[role] = fs.readFileSync(path.join(root, `skills/${role}/SKILL.md`), 'utf8') +
        '\nRead these selected skills before work: ' + skills.join(', ') +
        '\nTask IDs: 31, 32. Implement or review invoice retry acceptance tests.';
    results.push(await tool.execute(role, {roster_entry: role, task_name: `Invoice ${role}`,
        cwd: process.env.PROBE_WORKTREE, prompt: prompts[role], interactive: false,
        stay_open: false, auto_approve: role === 'review',
        disallowed_tools: role === 'review' ? ['write'] : undefined},
        undefined, undefined, ctx));
}
// A known stopped Claude result can resume. Tool controls must be supplied on each call.
const resumed = await tool.execute('resume', {resume_session_id: results[1].details.sessionId,
    task_name: 'Review fixes', prompt: prompts.review, interactive: false, stay_open: false},
    undefined, undefined, ctx);
let rejected;
try {
    await tool.execute('conflict', {resume_session_id: results[0].details.sessionId,
        task_name: 'Wrong worktree', prompt: 'Must never launch', cwd,
        interactive: false, stay_open: false}, undefined, undefined, ctx);
} catch (error) { rejected = error.message; }
const denied = {};
for (const [name, args] of Object.entries({
    unknown: {roster_entry: 'implementation', resume_session_id: 'unknown-native-id'},
    model: {roster_entry: 'implementation', model: 'unselected-model'}
})) {
    try {
        await tool.execute(name, {...args, task_name: 'Invalid selection',
            prompt: 'Must not launch',
            cwd: process.env.PROBE_WORKTREE, interactive: false, stay_open: false},
            undefined, undefined, ctx);
    } catch (error) { denied[name] = error.message; }
}
let instructions = [];
if (roles.find(r => r.name === 'implementation').agent_type === 'pi') {
    const worker = roles.find(r => r.name === 'implementation');
    const workerLoader = new DefaultResourceLoader({cwd: process.env.PROBE_WORKTREE, agentDir,
        settingsManager, additionalSkillPaths: worker.resources.skills,
        noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true,
        disabledBuiltinExtensions: ['mcp'], noContextFiles: false, systemPrompt: ''});
    await workerLoader.reload();
    instructions = workerLoader.getAgentsFiles().agentsFiles.map(f => f.path);
}
await session.extensionRunner.emit({type: 'session_shutdown'});
session.dispose();
console.log(JSON.stringify({roles, results, resumed, rejected, denied, instructions,
    history: sessionManager.getBranch().filter(e => e.type === 'custom')}));
'''


@unittest.skipUnless(os.environ.get('NATIVE_PI_SDK'), 'Set NATIVE_PI_SDK for native worker tools')
class NativeWorkerTests(InitFixture):
    def test_native_named_workers_launch_in_worktree_and_retain_real_session_contracts(self):
        for harness, model, effort in (('codex', 'gpt-5.4', 'xhigh'),
                                        ('pi', 'provider/model', 'high')):
            with self.subTest(harness=harness):
                # Arrange: public init followed by isolated public native tool invocation.
                repo = self.repo(harness)
                settings = worker_settings(self, harness=harness, model=model, effort=effort)
                setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
                self.assertEqual(setup.returncode, 0, setup.stderr)
                self.git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test',
                         'commit', '--allow-empty', '-m', 'Fixture baseline')
                worktree = self.workspace / f'{harness}-worktree'
                self.git(repo, 'worktree', 'add', '-b', 'invoice-retry', str(worktree))
                instruction = worktree / 'AGENTS.md'
                instruction.write_text('Repository instructions: preserve invoice compatibility.\n')
                original = instruction.read_bytes()
                for command in ('pi', 'codex', 'claude'):
                    executable = self.bin / command
                    executable.write_text(NATIVE)
                    executable.chmod(0o755)
                owner = repo / '.factory/agents/feature-owner'
                log = self.workspace / f'{harness}-native.jsonl'
                # Fresh native sessions need distinct IDs across both cases sharing SDK state.
                implementation_id = f'{harness}-implementation-session'
                review_id = f'{harness}-review-session'
                env = {'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
                       'HOME': str(self.workspace), 'XDG_STATE_HOME': str(self.workspace / 'state'),
                       'PI_CODING_AGENT_DIR': self.env['PI_CODING_AGENT_DIR'], 'PI_OFFLINE': '1',
                       'PI_AGENTSHELL_ROSTER_FILE': str(owner / 'agent.json'),
                       'PI_AGENT_SHELL_CHILD': '1', 'PI_AGENT_SHELL_DEPTH': '1',
                       'PI_AGENT_SHELL_MAX_DEPTH': '1',
                       'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve()),
                       'NATIVE_LOG': str(log), 'NATIVE_IMPLEMENTATION_ID': implementation_id,
                       'NATIVE_REVIEW_ID': review_id, 'PROBE_OWNER': str(owner),
                       'PROBE_WORKTREE': str(worktree)}
                # Act
                result = subprocess.run(
                    [os.environ.get('NATIVE_PI_NODE', 'node'), '--input-type=module', '-e', PROBE],
                    cwd=owner, env=env, capture_output=True, text=True, timeout=30)
                # Assert
                self.assertEqual(result.returncode, 0, result.stderr)
                observed = json.loads(result.stdout)
                self.assertEqual([r['name'] for r in observed['roles']],
                                 ['research', 'implementation', 'review'])
                self.assertEqual(observed['results'][0]['details']['sessionId'], implementation_id)
                self.assertEqual(observed['results'][1]['details']['sessionId'], review_id)
                self.assertEqual(observed['resumed']['details']['sessionId'], review_id)
                self.assertIn('cwd', observed['rejected'])
                self.assertIn('No recorded launch', observed['denied']['unknown'])
                self.assertIn('conflicts', observed['denied']['model'])
                if harness == 'pi':
                    self.assertIn(str(instruction), observed['instructions'])
                calls = [json.loads(line) for line in log.read_text().splitlines()]
                self.assertEqual(len(calls), 3)
                self.assertTrue(all(c['cwd'] == str(worktree) for c in calls))
                self.assertTrue(all(c['depth'] == '2' for c in calls))
                self.assertEqual(instruction.read_bytes(), original)
                for index, call in enumerate(calls):
                    args = call['args']
                    if index == 1:
                        self.assertIn('--dangerously-skip-permissions', args)
                        self.assertIn('--disallowed-tools', args)
                    else:
                        self.assertNotIn('--dangerously-skip-permissions', args)
                        self.assertNotIn('--disallowed-tools', args)
                    self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', args)
                    if index == 2:
                        self.assertEqual(args[args.index('--resume') + 1], review_id)
                    else:
                        self.assertNotIn('--resume', args)
                    expected_model = 'opus' if call['name'] == 'claude' else model
                    self.assertEqual(args[args.index('--model') + 1], expected_model)
                    if call['name'] == 'codex':
                        self.assertIn('model_reasoning_effort="xhigh"', args)
                    elif call['name'] == 'claude':
                        self.assertEqual(args[args.index('--effort') + 1], 'high')
                    else:
                        self.assertEqual(args[args.index('--thinking') + 1], 'high')
                    if call['name'] != 'pi':
                        self.assertIsNone(call['roster'])
                        self.assertNotIn('--skill', args)
                        self.assertNotIn('--no-context-files', args)
                    else:
                        self.assertEqual(call['roster'],
                                         str(repo / '.factory/agents/implementation/agent.json'))
                        self.assertIn('--skill', args)
                    prompt = args[args.index('-p') + 1] if call['name'] == 'claude' else args[-1]
                    self.assertIn('Do not use Forgetful', prompt)
                    self.assertIn('Task IDs: 31, 32', prompt)
                    self.assertIn(str(self.workspace / 'standards/SKILL.md'), prompt)
                    expected_role = 'review' if call['name'] == 'claude' else 'implementation'
                    self.assertIn(str(repo / '.factory/agents' / expected_role /
                                      f'skills/{expected_role}/SKILL.md'), prompt)
                    if expected_role == 'implementation':
                        self.assertIn(str(self.workspace / 'tdd/SKILL.md'), prompt)
                self.assertTrue(observed['history'])
                # Restore controlled listing for the next iteration; no real Pi process is run.
                from profile_support import COMMAND
                (self.bin / 'pi').write_text(COMMAND)
