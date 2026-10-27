"""Real Pi session reload; no prompts, inference, child agents or native accounts."""
import json
import os
import select
import subprocess
import unittest
from pathlib import Path

from test_init import INIT_SETTINGS, InitFixture

PROBE = r'''
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import {pathToFileURL} from 'node:url';
globalThis.fetch = async () => { throw new Error('Network forbidden'); };
const sdk = await import(pathToFileURL(process.env.NATIVE_PI_SDK).href);
const cwd = process.cwd();
const settingsManager = sdk.SettingsManager.inMemory({packages: [], cacheWarming: 'off'});
const selection = JSON.parse(fs.readFileSync(path.join(cwd, 'agent.json'), 'utf8')).agent.resources;
const loader = new sdk.DefaultResourceLoader({
  cwd, agentDir: process.env.PI_CODING_AGENT_DIR, settingsManager,
  additionalExtensionPaths: selection.extensions.map(p => path.resolve(cwd, p)),
  additionalSkillPaths: selection.skills.map(p => path.resolve(cwd, p)),
  noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true,
  disabledBuiltinExtensions: ['mcp'], noContextFiles: false, systemPrompt: ''
});
await loader.reload();
const {session} = await sdk.createAgentSession({
  cwd, agentDir: process.env.PI_CODING_AGENT_DIR, settingsManager, resourceLoader: loader,
  sessionManager: sdk.SessionManager.inMemory(cwd),
  model: {provider: 'fixture', id: 'no-inference', api: 'openai-completions', name: 'Fixture',
          baseUrl: 'http://invalid', reasoning: false, input: ['text'],
          contextWindow: 32000, maxTokens: 1024,
          cost: {input: 0, output: 0, cacheRead: 0, cacheWrite: 0}}
});
async function report() {
  const loaded = loader.getExtensions();
  if (loaded.errors.length) throw new Error(JSON.stringify(loaded.errors));
  const tools = loaded.extensions.flatMap(e => [...e.tools.values()].map(t => t.definition));
  const tool = tools.find(t => t.name === 'subagent_roster');
  const value = tool ? await tool.execute('probe', {}, undefined, undefined, {}) : null;
  console.log(JSON.stringify({session: session.sessionId, pid: process.pid,
    roles: value ? JSON.parse(value.content[0].text) : [],
    skills: loader.getSkills().skills.map(s => s.filePath)}));
}
await report();
for await (const line of readline.createInterface({input: process.stdin})) {
  if (line === 'reload') { await session.reload(); await report(); }
  if (line === 'exit') break;
}
session.dispose();
'''


@unittest.skipUnless(os.environ.get('NATIVE_PI_SDK'), 'Set NATIVE_PI_SDK for native Pi reload')
class NativeSetupReloadTests(InitFixture):
    def test_first_finalization_and_direct_file_edits_reload_in_same_native_session(self):
        # Arrange: save incomplete setup, then observe its resources through a real Pi SDK session.
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.env.pop('PROFILE_FAIL')
        self.assertNotEqual(setup.returncode, 0)
        self.assertTrue((repo / '.factory/factory.toml').is_file())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        directory = repo / '.factory/agents/foreman'
        env = {**self.env, 'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve()),
               'PI_AGENTSHELL_ROSTER_FILE': str(repo / '.factory/agents/foreman/agent.json')}
        node = os.environ.get('NATIVE_PI_NODE', 'node')
        process = subprocess.Popen([node, '--input-type=module', '-e', PROBE], cwd=directory,
                                   env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        def observation():
            self.assertTrue(select.select([process.stdout], [], [], 30)[0], 'Pi loader timeout')
            line = process.stdout.readline()
            if not line:
                self.fail(process.stderr.read())
            return json.loads(line)

        try:
            initial = observation()
            self.assertEqual([r['name'] for r in initial['roles']], ['feature-owner'])

            # Act: normal public finalization, followed by explicit native session reload.
            finalize = self.run_cli(repo, '--finalize')
            self.assertEqual(finalize.returncode, 0, finalize.stderr)
            self.assertEqual(
                json.loads((repo / '.factory/setup-complete.json').read_text()),
                {'complete': True},
            )
            process.stdin.write('reload\n')
            process.stdin.flush()
            completed = observation()

            # Assert
            self.assertEqual(completed['session'], initial['session'])
            self.assertEqual(completed['pid'], initial['pid'])
            self.assertEqual(completed['skills'], initial['skills'])
            self.assertEqual([r['name'] for r in completed['roles']], ['feature-owner'])
            skill = directory / 'skills/team/SKILL.md'
            skill.parent.mkdir()
            skill.write_text('---\nname: team\ndescription: Team context.\n---\nRead context.\n')
            child = repo / '.factory/agents/feature-owner/agent.json'
            document = json.loads(child.read_text())
            document['agent']['name'] = 'invoice-lead'
            document['agent']['effort'] = 'low'
            child.write_text(json.dumps(document))
            saved = child.read_bytes()
            process.stdin.write('reload\n')
            process.stdin.flush()
            refreshed = observation()
            self.assertEqual(refreshed['session'], initial['session'])
            self.assertIn(str(skill), refreshed['skills'])
            self.assertEqual(refreshed['roles'][0]['name'], 'invoice-lead')
            self.assertEqual(refreshed['roles'][0]['effort'], 'low')
            self.assertEqual(child.read_bytes(), saved)
            process.stdin.write('exit\n')
            process.stdin.flush()
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, stdout + stderr)
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=10)
