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
const selection = JSON.parse(fs.readFileSync(path.join(cwd, "resources.json"), "utf8"));
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
const roster = tools.find(t => t.name === "subagent_roster");
const result = roster ? await roster.execute("probe", {}, undefined, undefined, {}) : null;
console.log(JSON.stringify({
    agents: loader.getAgentsFiles().agentsFiles.map(f => f.path),
    skills: loader.getSkills().skills,
    tools: tools.map(t => t.name),
    roles: result ? JSON.parse(result.content[0].text) : [],
    systemPrompt: loader.getSystemPrompt() ?? null
}));
'''


@unittest.skipUnless(os.environ.get('NATIVE_PI_SDK'), 'Set NATIVE_PI_SDK for native loading')
class NativeRoleTests(InitFixture):
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
                       'PI_AGENTSHELL_ROSTER_FILE': str(directory / 'roster.json'),
                       'NATIVE_PI_SDK': str(Path(os.environ['NATIVE_PI_SDK']).resolve())}
                # Act
                result = subprocess.run(['node', '--input-type=module', '-e', PROBE],
                                        cwd=directory, env=env, capture_output=True, text=True,
                                        timeout=30, check=True)
                observation = json.loads(result.stdout)
                # Assert
                self.assertIn(str(directory / 'AGENTS.md'), observation['agents'])
                self.assertIn(str(repo / 'AGENTS.md'), observation['agents'])
                self.assertIn(str(home / 'AGENTS.md'), observation['agents'])
                self.assertNotIn('PERSONAL_SYSTEM_MUST_NOT_LOAD', observation['systemPrompt'] or '')
                self.assertEqual([r['name'] for r in observation['roles']], children)
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
        worker = repo / '.factory/agents/foreman/resources/agentshell/python/worker.py'
        # Act
        result = subprocess.run([sys.executable, '-I', str(worker)],
                                input='{"operation":"list_agent_types"}\n',
                                capture_output=True, text=True, timeout=10, check=True,
                                env={'PATH': os.environ['PATH'], 'HOME': str(self.workspace)})
        # Assert
        output = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(output[0]['kind'], 'agent_types')
        self.assertIn('pi', output[0]['agent_types'])
