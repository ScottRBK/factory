"""Opt-in native resource loading with an already installed Pi SDK, never inference.

NATIVE_PI_SDK=/absolute/pi-coding-agent/dist/index.js enables these tests.
The SDK and bundled extension load inside fresh temporary homes. No native child agents launch;
these checks do not establish liveness, resume success, task claims or autonomous planning.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from test_init import INIT_SETTINGS, InitFixture

PROBE = r'''
import fs from "node:fs";
import path from "node:path";
import {pathToFileURL} from "node:url";
// Fail any accidental HTTP attempt without sending a request.
globalThis.fetch = async () => { throw new Error("Network forbidden in resource probe"); };
const {DefaultResourceLoader, SettingsManager} = await import(
    pathToFileURL(process.env.NATIVE_PI_SDK).href);
const cwd = process.env.PROBE_ROLE;
const selection = JSON.parse(fs.readFileSync(path.join(cwd, "agent.json"), "utf8")).agent.resources;
const resolve = p => path.resolve(cwd, p);
const loader = new DefaultResourceLoader({
    cwd, agentDir: process.env.PI_CODING_AGENT_DIR,
    settingsManager: SettingsManager.inMemory({packages: []}),
    additionalExtensionPaths: selection.extensions.map(resolve),
    additionalSkillPaths: selection.skills.map(resolve),
    noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true,
    disabledBuiltinExtensions: ["mcp"], noContextFiles: false, systemPrompt: ""
});
await loader.reload();
const loaded = loader.getExtensions();
if (loaded.errors.length) throw new Error(JSON.stringify(loaded.errors));
const tools = loaded.extensions.flatMap(e => [...e.tools.values()].map(t => t.definition));
const commands = loaded.extensions.flatMap(e => [...e.commands.keys()]);
const roster = tools.find(t => t.name === "subagent_roster");
const result = roster ? await roster.execute("probe", {}, undefined, undefined, {}) : null;
console.log(JSON.stringify({
    agents: loader.getAgentsFiles().agentsFiles.map(f => f.path),
    skills: loader.getSkills().skills,
    tools: tools.map(t => t.name),
    commands,
    roles: result ? JSON.parse(result.content[0].text) : [],
    systemPrompt: loader.getSystemPrompt() ?? null
}));
'''

MANAGED_PROBE = r'''
import fs from "node:fs";
import path from "node:path";
import {once} from "node:events";
import {createServer} from "node:http";
import {pathToFileURL} from "node:url";
const {createAgentSession, DefaultResourceLoader, SessionManager, SettingsManager} = await import(
    pathToFileURL(process.env.NATIVE_PI_SDK).href);
const cwd = process.env.PROBE_ROLE;
const selection = JSON.parse(fs.readFileSync(path.join(cwd, "agent.json"), "utf8")).agent.resources;
const requests = [];
const server = createServer((request, response) => {
  requests.push(`${request.method} ${request.url}`);
  response.setHeader("content-type", "application/json");
  response.end(JSON.stringify({id: 12, name: "Factory fixture project"}));
});
server.listen(0, "127.0.0.1");
await once(server, "listening");
process.env.FORGETFUL_SERVER =
    `http://127.0.0.1:${server.address().port}/factory/mcp`;
const settings = SettingsManager.create(cwd, process.env.PI_CODING_AGENT_DIR);
settings.setProjectTrusted(true);
const loader = new DefaultResourceLoader({
  cwd, agentDir: process.env.PI_CODING_AGENT_DIR, settingsManager: settings,
  additionalExtensionPaths: selection.extensions.map(p => path.resolve(cwd, p)),
  additionalSkillPaths: selection.skills.map(p => path.resolve(cwd, p)),
  noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true,
  disabledBuiltinExtensions: ["codemode", "tool_search", "mcp"], noContextFiles: false,
  systemPrompt: ""
});
await loader.reload();
const loaded = loader.getExtensions();
const {session} = await createAgentSession({
  cwd, agentDir: process.env.PI_CODING_AGENT_DIR, settingsManager: settings,
  sessionManager: SessionManager.inMemory(cwd), resourceLoader: loader, noTools: true
});
const notices = [];
const errors = [];
await session.bindExtensions({mode: "json", onError: error => errors.push(error.error),
  uiContext: {notify: message => notices.push(message), setWidget: () => undefined}});
await session.prompt("/forgetful status");
await session.extensionRunner.emit({type: "session_shutdown", reason: "quit"});
session.dispose();
await new Promise(resolve => { server.close(resolve); server.closeAllConnections(); });
console.log(JSON.stringify({
  loadErrors: loaded.errors, errors, notices, requests,
  tools: loaded.extensions.flatMap(e => [...e.tools.keys()]),
  commands: loaded.extensions.flatMap(e => [...e.commands.keys()])
}));
'''


@unittest.skipUnless(os.environ.get('NATIVE_PI_SDK'), 'Set NATIVE_PI_SDK for native loading')
class NativeRoleTests(InitFixture):
    def test_native_pi_loads_relocated_managed_foreman_with_controlled_rest(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--no-foreman-memory',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/factory/mcp',
        )
        self.assertEqual(setup.returncode, 0, setup.stderr)
        factory = repo / '.factory'
        original = factory / 'agents/foreman'
        role = factory / 'coordinators/dispatch'
        role.parent.mkdir()
        original.rename(role)
        definition = role / 'agent.json'
        document = json.loads(definition.read_text())
        document['agent']['name'] = 'dispatch-lead'
        document['agent']['resources']['extensions'] = [
            '../../resources/agentshell/extensions/agentshell.ts',
            '../../resources/hide-tools/index.ts',
            '../../resources/pi-forgetful/factory.ts',
        ]
        document['roster']['roles'] = [{'agent_file': '../../agents/feature-owner/agent.json'}]
        definition.write_text(json.dumps(document))
        config = factory / 'factory.toml'
        config.write_text(config.read_text().replace(
            'agents/foreman/agent.json', 'coordinators/dispatch/agent.json'))
        env = {
            'PATH': os.environ['PATH'],
            'HOME': str(self.workspace),
            'PI_OFFLINE': '1',
            'PI_CODING_AGENT_DIR': str(self.workspace / 'native pi'),
            'PROBE_ROLE': str(role),
            'PI_AGENTSHELL_ROSTER_FILE': str(definition),
            'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve()),
            'FACTORY_WORKSPACE': str(repo),
            'FACTORY_FOREMAN_AGENT_FILE': str(definition),
            'FACTORY_FORGETFUL_INSTANCE': 'server',
            'FACTORY_FORGETFUL_PROJECT_ID': '12',
            'FORGETFUL_SERVER': 'https://memory.example/factory/mcp',
        }

        # Act
        result = subprocess.run(
            [os.environ.get('NATIVE_PI_NODE', 'node'), '--input-type=module', '-e', MANAGED_PROBE],
            cwd=role, env=env, capture_output=True, text=True, timeout=30, check=True)

        # Assert
        observation = json.loads(result.stdout)
        self.assertEqual(observation['loadErrors'], [])
        self.assertEqual(observation['errors'], [])
        self.assertIn('forgetful', observation['commands'])
        self.assertIn('forgetful_recall_wait', observation['tools'])
        self.assertEqual(observation['requests'], ['GET /factory/api/v1/projects/12'])
        self.assertIn('Factory fixture project (#12)', '\n'.join(observation['notices']))
        self.assertFalse((role / 'forgetful-auth.json').exists())

    def test_native_pi_discovers_added_local_skill_without_init_or_inference(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/research'
        skill = role / 'skills/team-context/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('---\nname: team-context\ndescription: >-\n'
                         '  Gather our team context.\n---\nPreserve this guidance.\n')
        env = {'PATH': os.environ['PATH'], 'HOME': str(self.workspace), 'PI_OFFLINE': '1',
               'PI_CODING_AGENT_DIR': str(self.workspace / 'native pi'),
               'PROBE_ROLE': str(role), 'PI_AGENTSHELL_ROSTER_FILE': str(role / 'agent.json'),
               'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve())}

        # Act
        result = subprocess.run(
            [os.environ.get('NATIVE_PI_NODE', 'node'), '--input-type=module', '-e', PROBE],
            cwd=role, env=env, capture_output=True, text=True, timeout=30, check=True)

        # Assert
        skills = json.loads(result.stdout)['skills']
        selected = next(item for item in skills if item['name'] == 'team-context')
        self.assertEqual(selected['filePath'], str(skill))
        self.assertEqual(selected['description'], 'Gather our team context.')
        self.assertFalse(selected['disableModelInvocation'])

    def test_native_pi_loads_coordinator_instructions_and_explicit_child_rosters(self):
        # Arrange
        # Public init provisions the files using controlled external setup programs.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        home = self.workspace / 'native pi'
        (home / 'AGENTS.md').write_text('Native home context remains applicable.\n')
        (repo / 'AGENTS.md').write_text('Repository ancestor context remains applicable.\n')
        (home / 'SYSTEM.md').write_text('PERSONAL_SYSTEM_MUST_NOT_LOAD\n')
        agents = repo / '.factory/agents'
        for role, children in (('foreman', ['feature-owner']), ('feature-owner', ['research']),
                               ('research', [])):
            with self.subTest(role=role):
                directory = agents / role
                # Minimal environment deliberately creates an isolated root resource-loader test.
                # It does not claim to exercise or bypass native child ancestry enforcement.
                env = {'PATH': os.environ['PATH'], 'HOME': str(self.workspace), 'PI_OFFLINE': '1',
                       'PI_CODING_AGENT_DIR': str(home), 'PROBE_ROLE': str(directory),
                       'PI_AGENTSHELL_ROSTER_FILE': str(directory / 'agent.json'),
                       'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve())}
                # Act
                result = subprocess.run(
                    [os.environ.get('NATIVE_PI_NODE', 'node'), '--input-type=module', '-e', PROBE],
                    cwd=directory, env=env, capture_output=True, text=True, timeout=30, check=True)
                observation = json.loads(result.stdout)
                # Assert
                self.assertIn(str(directory / 'AGENTS.md'), observation['agents'])
                self.assertIn(str(repo / 'AGENTS.md'), observation['agents'])
                self.assertIn(str(home / 'AGENTS.md'), observation['agents'])
                self.assertNotIn('PERSONAL_SYSTEM_MUST_NOT_LOAD', observation['systemPrompt'] or '')
                self.assertEqual([r['name'] for r in observation['roles']], children)
                if role == 'foreman':
                    maintenance = next(s for s in observation['skills']
                                       if s['name'] == 'factory-maintenance')
                    self.assertFalse(maintenance['disableModelInvocation'])
                    self.assertIn('configuring agent apps', maintenance['description'])
                    self.assertEqual(maintenance['filePath'],
                                     str(directory / 'skills/factory-maintenance/SKILL.md'))
                if role == 'feature-owner':
                    grill = next(s for s in observation['skills'] if s['name'] == 'grill-me')
                    self.assertIs(grill['disableModelInvocation'], True)
                if role == 'research':
                    self.assertNotIn('subagent', observation['tools'])

    def test_bundled_worker_uses_existing_agentshell_without_inference(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        worker = repo / '.factory/resources/agentshell/python/worker.py'
        # Act
        result = subprocess.run([sys.executable, '-I', str(worker)],
                                input='{"operation":"list_agent_types"}\n',
                                capture_output=True, text=True, timeout=10, check=True,
                                env={'PATH': os.environ['PATH'], 'HOME': str(self.workspace)})
        # Assert
        output = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(output[0]['kind'], 'agent_types')
        self.assertIn('pi', output[0]['agent_types'])
