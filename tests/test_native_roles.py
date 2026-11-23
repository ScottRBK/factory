"""Opt-in native resource loading with an already installed Pi SDK, never inference.

NATIVE_PI_SDK=/absolute/pi-coding-agent/dist/index.js enables these tests.
The SDK and bundled extension load inside fresh temporary homes. No native child agents launch;
these checks do not establish liveness, resume success, task claims or autonomous planning.
"""
import json
import os
import stat
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
for (const command of JSON.parse(process.env.PROBE_COMMANDS)) await session.prompt(command);
await session.extensionRunner.emit({type: "session_shutdown", reason: "quit"});
session.dispose();
await new Promise(resolve => { server.close(resolve); server.closeAllConnections(); });
console.log(JSON.stringify({
  loadErrors: loaded.errors, errors, notices, requests,
  tools: loaded.extensions.flatMap(e => [...e.tools.keys()]),
  commands: loaded.extensions.flatMap(e => [...e.commands.keys()])
}));
'''

OFF = {'enabled': False, 'capture_mode': 'off'}
ON = {'enabled': True, 'capture_mode': 'auto', 'model': 'provider/model'}
PROJECT_REQUEST = ['GET /factory/api/v1/projects/12']
PROJECT = 'project Factory fixture project (#12)'
MANAGED_NO_MODEL = ('Forgetful memory model is not configured; recall and capture are paused. '
                    'Set model in the selected Foreman forgetful.json.')
MANAGED_BLOCKED = ('This Foreman memory configuration is managed by Factory; settings were not '
                   'changed. Edit the selected Foreman forgetful.json or forgetful-auth.json.')


def managed_probe(workspace: Path, repo: Path, definition: Path, *commands: str) -> dict:
    """Load the managed Foreman memory extension in native Pi against a fixture server."""
    env = {
        'PATH': os.environ['PATH'],
        'HOME': str(workspace),
        'PI_OFFLINE': '1',
        'PI_CODING_AGENT_DIR': str(workspace / 'native pi'),
        'PROBE_ROLE': str(definition.parent),
        'PROBE_COMMANDS': json.dumps(commands or ['/forgetful status']),
        'PI_AGENTSHELL_ROSTER_FILE': str(definition),
        'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve()),
        'FACTORY_WORKSPACE': str(repo),
        'FACTORY_FOREMAN_AGENT_FILE': str(definition),
        'FACTORY_FORGETFUL_INSTANCE': 'server',
        'FACTORY_FORGETFUL_PROJECT_ID': '12',
        'FORGETFUL_SERVER': 'https://memory.example/factory/mcp',
    }
    result = subprocess.run(
        [os.environ.get('NATIVE_PI_NODE', 'node'), '--input-type=module', '-e', MANAGED_PROBE],
        cwd=definition.parent, env=env, capture_output=True, text=True, timeout=30, check=True)
    return json.loads(result.stdout)


def status_and_warnings(observation: dict) -> tuple[str, set[str]]:
    """Split probe notices into the one status line and the distinct warnings."""
    status, = (notice for notice in observation['notices']
               if 'Forgetful on; capture' in notice or 'Forgetful off; capture' in notice)
    return status, set(observation['notices']) - {status}


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

        # Act
        observation = managed_probe(self.workspace, repo, definition)

        # Assert
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


@unittest.skipUnless(os.environ.get('NATIVE_PI_SDK'), 'Set NATIVE_PI_SDK for native loading')
class NativeManagedMemorySettingsTests(InitFixture):
    """forgetful.json holds the extension's own settings; Factory keeps server, auth and state."""

    def server_factory(self) -> tuple[Path, Path]:
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--no-foreman-memory',
                             '--forgetful-instance', 'server',
                             '--forgetful-server', 'https://memory.example/factory/mcp')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        return repo, repo / '.factory/agents/foreman/agent.json'

    def test_memory_off_starter_file_loads_without_warnings(self):
        # Arrange
        repo, definition = self.server_factory()

        # Act
        observation = managed_probe(self.workspace, repo, definition)

        # Assert
        status, warnings = status_and_warnings(observation)
        self.assertEqual(warnings, set())
        self.assertTrue(status.startswith(
            'Managed Foreman memory is off; planning uses fixed project #12; '
            'private task window up to 100000 tokens. Forgetful off; capture off;'), status)
        self.assertIn('verbosity warning; logging off;', status)
        self.assertIn(PROJECT, status)
        self.assertEqual(observation['requests'], PROJECT_REQUEST)

    def test_settings_follow_extension_rules_and_defaults(self):
        # Arrange
        repo, definition = self.server_factory()
        cases = {
            'larger task window': ({**OFF, 'context_limit_tokens': 262144},
                                   ['private task window up to 262144 tokens.'], set()),
            'invalid task window': ({**OFF, 'context_limit_tokens': 0},
                                    ['private task window up to 100000 tokens.'],
                                    {'Invalid context_limit_tokens; choose a positive safe '
                                     'integer. Using 100000.'}),
            'recall only': ({**ON, 'capture_mode': 'off'},
                            ['Forgetful on; capture off;', 'model provider/model'], set()),
            'observe': ({**ON, 'capture_mode': 'observe'},
                        ['Forgetful on; capture observe;'], set()),
            'invalid capture mode': ({**ON, 'capture_mode': 'bogus'},
                                     ['Forgetful on; capture off;'],
                                     {'Invalid capture mode; using off until corrected.'}),
            'on without a model': ({'enabled': True, 'capture_mode': 'auto'},
                                   ['Forgetful on; capture auto;', 'model not configured'],
                                   {MANAGED_NO_MODEL}),
            'empty': ({}, ['Forgetful on; capture auto;', 'model not configured'],
                      {MANAGED_NO_MODEL}),
            'ready': (ON, ['Managed Foreman memory uses fixed project #12; private task window '
                           'up to 100000 tokens. Forgetful on; capture auto;',
                           'verbosity warning; logging off;', 'model provider/model'], set()),
        }
        for name, (settings, fragments, expected_warnings) in cases.items():
            with self.subTest(name):
                definition.with_name('forgetful.json').write_text(json.dumps(settings))

                # Act
                observation = managed_probe(self.workspace, repo, definition)

                # Assert: plans keep working; no Factory rule turns memory unavailable.
                status, warnings = status_and_warnings(observation)
                self.assertEqual(observation['errors'], [])
                self.assertEqual(warnings, expected_warnings)
                for fragment in fragments:
                    self.assertIn(fragment, status)
                self.assertIn(PROJECT, status)
                self.assertEqual(observation['requests'], PROJECT_REQUEST)

    def test_factory_owned_unknown_or_non_object_settings_make_memory_unavailable(self):
        # Arrange
        repo, definition = self.server_factory()
        owned = {'base_url': 'http://elsewhere.example', 'token': 'secret',
                 'token_env': 'OTHER_TOKEN', 'log_directory': '/tmp/forgetful-logs',
                 'planning_panel': True}
        cases = {key: ({**OFF, key: value}, f'forgetful.json must not set {key}; Factory sets it.')
                 for key, value in owned.items()}
        cases['unknown'] = ({**OFF, 'contextLimitTokens': 262144},
                            'forgetful.json has unknown setting contextLimitTokens.')
        # Factory fixes the project scope; the extension's project-file key is refused too.
        cases['scope'] = ({**OFF, 'scope': 'global'}, 'forgetful.json has unknown setting scope.')
        cases['array'] = ([OFF], 'forgetful.json must be a JSON object.')
        for name, (settings, reason) in cases.items():
            with self.subTest(name):
                definition.with_name('forgetful.json').write_text(json.dumps(settings))

                # Act
                observation = managed_probe(self.workspace, repo, definition)

                # Assert: no request reaches the server.
                status, warnings = status_and_warnings(observation)
                message = f'Managed Foreman memory is unavailable: {reason}'
                self.assertEqual(warnings, {message})
                self.assertTrue(status.startswith(f'{message} Forgetful off;'), status)
                self.assertEqual(observation['requests'], [])

    def test_debug_logging_writes_only_below_factory_state(self):
        # Arrange
        repo, definition = self.server_factory()
        definition.with_name('forgetful.json').write_text(
            json.dumps({**OFF, 'verbosity': 'info', 'logging': 'debug'}))

        # Act
        observation = managed_probe(self.workspace, repo, definition)

        # Assert
        status, warnings = status_and_warnings(observation)
        self.assertEqual(warnings, set())
        self.assertIn('verbosity info; logging on;', status)
        logs = list(self.workspace.rglob('forgetful-*.jsonl'))
        self.assertTrue(logs)
        for log in logs:
            self.assertEqual(log.parent, repo / '.factory/data/pi-forgetful/logs')
            self.assertEqual(stat.S_IMODE(log.stat().st_mode), 0o600)

    def test_blocked_command_points_to_the_foreman_settings_files(self):
        # Arrange
        repo, definition = self.server_factory()

        # Act
        observation = managed_probe(self.workspace, repo, definition, '/forgetful setup')

        # Assert
        self.assertIn(MANAGED_BLOCKED, observation['notices'])
