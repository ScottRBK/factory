"""First-time starter team provisioning through the public init command, without inference."""
import json
import tomllib

from test_init import InitFixture
from test_watch import WatchFixture


class AgentDefinitionInitTests(InitFixture):
    def test_full_manual_team_owns_settings_in_reference_only_agent_documents(self):
        # Arrange: each native model choice is distinct and advertised by fake Pi.
        repo = self.repo()
        roles = ('foreman', 'feature-owner', 'research', 'implementation', 'review')
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n' +
            '\n'.join(f'fixture  {role}  128000  8192  yes  yes' for role in roles))
        args = ['--repo', '.', '--label', 'factory']
        for role in roles:
            args.extend((f'--{role}-model', f'fixture/{role}', f'--{role}-effort', 'high'))
            if role in ('research', 'implementation', 'review'):
                args.extend((f'--{role}-harness', 'pi'))

        # Act
        result = self.run_cli(repo, *args, worker_defaults=False)

        # Assert: TOML owns factory settings; agent documents own all agent selections.
        self.assertEqual(result.returncode, 0, result.stderr)
        factory = repo / '.factory'
        saved = tomllib.loads((factory / 'factory.toml').read_text())
        self.assertEqual(set(saved), {'watcher_label', 'foreman_agent_file',
                                     'execution_enabled', 'repository', 'forgetful'})
        self.assertTrue(saved['execution_enabled'])
        self.assertEqual(saved['foreman_agent_file'], 'agents/foreman/agent.json')
        children = {'foreman': ['feature-owner'],
                    'feature-owner': ['research', 'implementation', 'review']}
        for role in roles:
            with self.subTest(role=role):
                path = factory / 'agents' / role / 'agent.json'
                document = json.loads(path.read_text())
                self.assertEqual(set(document), {'agent', 'roster'})
                agent = document['agent']
                self.assertEqual(agent['name'], role)
                self.assertTrue(agent['description'])
                self.assertEqual(agent['agent_type'], 'pi')
                self.assertEqual(agent['model'], f'fixture/{role}')
                self.assertEqual(agent['effort'], 'high')
                self.assertIn('skills', agent['resources'])
                self.assertIn('./skills', agent['resources']['skills'])
                if role in ('implementation', 'review'):
                    self.assertNotIn('cwd', agent)
                else:
                    self.assertEqual(agent['cwd'], '.')
                descendants = children.get(role, [])
                self.assertEqual(document['roster'], {
                    'enabled': bool(descendants),
                    'roles': [{'agent_file': f'../{child}/agent.json'} for child in descendants],
                })
                for reference in document['roster']['roles']:
                    self.assertTrue((path.parent / reference['agent_file']).is_file())
        self.assertEqual(list((factory / 'agents').glob('*/resources.json')), [])
        self.assertEqual(list((factory / 'agents').glob('*/roster.json')), [])
        self.assertEqual(list((factory / 'runtime').glob('**/roster.json')), [])

    def test_repeated_init_preserves_edits_without_backend_calls_or_launch_offer(self):
        # Arrange: a complete factory with deliberately changed agent and instruction files.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                             '--foreman-model', 'provider/model', '--foreman-effort', 'high')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        factory = repo / '.factory'
        definition = factory / 'agents/foreman/agent.json'
        selected = json.loads(definition.read_text())
        selected['agent']['name'] = 'dispatcher'
        selected['agent']['model'] = 'new-provider/unlisted-model'
        definition.write_text(json.dumps(selected, indent=4) + '\n')
        instructions = factory / 'agents/foreman/AGENTS.md'
        instructions.write_text('Preserve my custom team instructions.\n')
        added = factory / 'agents/research/skills/new/SKILL.md'
        added.parent.mkdir()
        added.write_text('New local skill, discovered by native Pi.\n')
        before = {p.relative_to(factory): p.read_bytes()
                  for p in factory.rglob('*') if p.is_file()}
        log = self.workspace / 'repeat.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.env['PROFILE_FAIL'] = 'pi'
        self.state.write_text('{}')

        # Act: even surplus initial choices cannot reconfigure or consume launch consent.
        result = self.run_cli(repo, '--foreman-model', 'ignored/choice', input='y\n')

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('already initialized', result.stdout)
        self.assertNotIn('Launch factory', result.stdout)
        self.assertNotIn('Select ', result.stdout)
        self.assertFalse(log.exists())
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual({p.relative_to(factory): p.read_bytes()
                          for p in factory.rglob('*') if p.is_file()}, before)

    def test_native_workers_keep_selected_skills_and_arbitrary_name_briefing(self):
        from test_init import INIT_SETTINGS
        from worker_support import worker_settings

        # Arrange / Act
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))

        # Assert: native defaults stay native; authoritative skills stay in the definition.
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        for role, harness in (('implementation', 'codex'), ('review', 'claude_code')):
            document = json.loads((agents / role / 'agent.json').read_text())
            selected = document['agent']
            self.assertEqual(selected['agent_type'], harness)
            self.assertEqual(set(selected['resources']), {'skills'})
            self.assertIn(str(self.workspace / 'standards/SKILL.md'),
                          selected['resources']['skills'])
            self.assertNotIn('cwd', selected)
            self.assertEqual(document['roster'], {'enabled': False, 'roles': []})
        implementation = json.loads((agents / 'implementation/agent.json').read_text())['agent']
        self.assertIn(str(self.workspace / 'tdd/SKILL.md'), implementation['resources']['skills'])
        guidance = ' '.join((agents / 'feature-owner/skills/feature-owner/SKILL.md')
                            .read_text().split())
        for required in ('agent.json', 'configured names and descriptions', 'directory selections',
                         'absolute SKILL.md', 'full role briefing', 'read them before work',
                         'TDD', 'additional skills'):
            self.assertIn(required, guidance)
        for obsolete in ('resources.json', 'roster_entry="implementation"',
                         'roster_entry="review"'):
            self.assertNotIn(obsolete, guidance)


class AgentDefinitionLaunchTests(WatchFixture):
    def test_invalid_roster_envelopes_and_nonlocal_references_fail_before_native_launch(self):
        # Arrange: defaulted fields do not relax types, leaf rules or local-file restrictions.
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        original = definition.read_text()
        cases = [({'extra': True}, 'reference-only'), ({'enabled': 1}, 'reference-only'),
                 ({'roles': None}, 'reference-only'),
                 ({'roles': [{'agent_file': '../feature-owner/agent.json', 'model': 'x'}]},
                  'only agent_file')]
        for value in ('https://example.test/agent.json', '~/.pi/agent.json', 'npm:team',
                      'git:team', 'file:/tmp/agent.json', 'bad\x00path', '../missing.json'):
            cases.append(({'roles': [{'agent_file': value}]}, 'agent'))
        for roster, message in cases:
            with self.subTest(roster=roster):
                document = json.loads(original)
                document['roster'] = roster
                definition.write_text(json.dumps(document))
                before = definition.read_bytes()
                # Act
                process = self.start('--new-only')
                _, errors = process.communicate(timeout=5)
                # Assert
                self.assertNotEqual(process.returncode, 0)
                self.assertIn(message, errors)
                self.assertNotIn('Traceback', errors)
                self.assertEqual(self.events(), [])
                self.assertEqual(definition.read_bytes(), before)
        document = json.loads(original)
        document['agent']['agent_type'] = 'codex'
        definition.write_text(json.dumps(document))
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)
        self.assertIn('Non-Pi agents require a disabled empty roster', errors)
        self.assertEqual(self.events(), [])

    def test_selected_guidance_is_validated_outside_definition_and_launch_directories(self):
        # Arrange: explicit skill selections identify guidance, irrespective of root cwd.
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        selected = self.workspace / 'shared-guidance'
        (definition.parent / 'skills').rename(selected)
        document = json.loads(definition.read_text())
        document['agent']['resources']['skills'] = [str(selected / 'foreman/SKILL.md'),
                                                   str(selected / 'factory-maintenance')]
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)
        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.events()[0]['resources']['skills'],
                         document['agent']['resources']['skills'])
        self.assertEqual(definition.read_bytes(), before)
        self.terminal_log.unlink()
        skill = selected / 'foreman/SKILL.md'
        skill.write_text('Do not dispatch agents, create plans or tasks, in this old slice.')
        # Act: stale guidance must be detected at the selected path, not at an old default.
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)
        # Assert
        self.assertNotEqual(process.returncode, 0)
        self.assertIn(str(skill), errors)
        self.assertIn('manual reconciliation', errors)
        self.assertEqual(self.events(), [])
        self.assertEqual(definition.read_bytes(), before)

    def test_omitted_root_cwd_inherits_cli_directory_with_independent_selected_guidance(self):
        # Arrange: selected skills stay file-relative even when launch cwd is inherited.
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        del document['agent']['cwd']
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()
        caller = self.workspace / 'caller'
        caller.mkdir()

        # Act
        process = self.start('--new-only', cwd=caller)
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)

        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.events()[0]['cwd'], str(caller))
        self.assertEqual(self.events()[0]['resources']['skills'],
                         [str(definition.parent / 'skills')])
        self.assertEqual(definition.read_bytes(), before)

    def test_watch_uses_edited_root_settings_without_init_and_owns_cleanup(self):
        # Arrange: keep child definitions independent and put Foreman at an arbitrary path.
        factory = self.workspace / '.factory'
        original = factory / 'agents/foreman'
        moved = factory / 'coordinators/dispatch'
        moved.parent.mkdir()
        original.rename(moved)
        definition = moved / 'agent.json'
        document = json.loads(definition.read_text())
        document['agent'].update(name='dispatch-lead', description='Lead this configured team',
                                 model='another/selector', effort='low')
        document['roster']['roles'] = [{'agent_file': '../../agents/feature-owner/agent.json'}]
        extra = moved / 'extra-skills'
        extra.mkdir()
        document['agent']['resources']['skills'].append('./extra-skills')
        definition.write_text(json.dumps(document))
        config = factory / 'factory.toml'
        config.write_text(config.read_text().replace('agents/foreman/agent.json',
                                                     'coordinators/dispatch/agent.json'))
        before = definition.read_bytes()

        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)

        # Assert: test the controller's external native launch, not private JSON parsing.
        self.assertEqual(code, 130, errors)
        launch, = [e for e in self.events() if e['kind'] == 'launch']
        self.assertEqual((launch['model'], launch['effort'], launch['cwd']),
                         ('another/selector', 'low', str(moved)))
        self.assertEqual(launch['roster'], str(definition))
        self.assertEqual(launch['agent_dir'], str(self.workspace / 'native pi'))
        self.assertEqual(launch['resources']['skills'], [str(moved / 'skills'), str(extra)])
        self.assertTrue(any(e['kind'] == 'close' for e in self.events()))
        self.assertEqual(definition.read_bytes(), before)

    def test_watch_forwards_root_resource_options_from_the_definition(self):
        # Arrange: these native options are deliberately different from the starter defaults.
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        policy = {'mcp_servers': None, 'inherit_personal_resources': True,
                  'inherit_project_resources': True, 'include_instruction_files': True,
                  'include_home_system_prompt': True}
        document['agent']['resources'].update(policy)
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()
        preferences = self.workspace / 'native pi/extensions/agentshell.json'
        preferences_before = preferences.read_bytes()

        # Act: launch through the public CLI without rerunning setup.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)

        # Assert: native options are forwarded, with normal owned-session cleanup.
        self.assertEqual(code, 130, errors)
        launch, = [e for e in self.events() if e['kind'] == 'launch']
        self.assertEqual({key: launch['resources'][key] for key in policy}, policy)
        self.assertEqual(launch['agent_dir'], str(self.workspace / 'native pi'))
        self.assertTrue(any(e['kind'] == 'close' for e in self.events()))
        self.assertEqual(definition.read_bytes(), before)
        self.assertEqual(preferences.read_bytes(), preferences_before)

    def test_watch_rejects_missing_required_root_guidance_without_rewriting_selection(self):
        # Arrange: a valid native resource selection can still omit required Factory guidance.
        self.env['WATCH_EXIT_DELAY'] = '0.2'
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        document['agent']['resources']['skills'] = []
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()

        # Act
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)

        # Assert
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('Foreman guidance', errors)
        self.assertEqual(self.events(), [])
        self.assertEqual(definition.read_bytes(), before)

    def test_watch_rejects_non_boolean_resource_policy_before_native_launch(self):
        # Arrange
        self.env['WATCH_EXIT_DELAY'] = '0.2'
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        document['agent']['resources']['inherit_personal_resources'] = 0
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()

        # Act
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)

        # Assert
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('boolean', errors)
        self.assertEqual(self.events(), [])
        self.assertEqual(definition.read_bytes(), before)

    def test_watch_rejects_invalid_mcp_selection_without_starting_native_pi(self):
        # Arrange: agent.json accepts only inherited MCP (null) or none ([]).
        self.env['WATCH_EXIT_DELAY'] = '0.2'
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        for invalid in ('inherit', False, {}, [{'name': 'unsupported'}]):
            with self.subTest(invalid=invalid):
                document['agent']['resources']['mcp_servers'] = invalid
                definition.write_text(json.dumps(document))
                before = definition.read_bytes()

                # Act
                process = self.start('--new-only')
                _, errors = process.communicate(timeout=5)

                # Assert
                self.assertNotEqual(process.returncode, 0)
                self.assertIn('mcp_servers', errors)
                self.assertEqual(self.events(), [])
                self.assertEqual(definition.read_bytes(), before)

    def test_watch_keeps_initial_completion_consent_depth_and_audited_resource_gates(self):
        # Arrange: each failure is externally visible before any native launch.
        factory = self.workspace / '.factory'
        cases = (
            (factory / 'setup-complete.json', None, 'incomplete'),
            (factory / 'pi-profile.json', '{"shared_profile_consent": false}', 'consent'),
            (factory / 'resources/agentshell/config.ts', '// changed audited code', 'audited'),
            (self.workspace / 'native pi/extensions/agentshell.json',
             '{"max_sub_agent_depth": 0}', 'depth'),
        )
        for path, content, diagnostic in cases:
            with self.subTest(path=path):
                before = path.read_bytes()
                if content is None:
                    path.unlink()
                else:
                    path.write_text(content)
                try:
                    # Act
                    process = self.start('--new-only')
                    _, errors = process.communicate(timeout=5)

                    # Assert
                    self.assertNotEqual(process.returncode, 0)
                    self.assertIn(diagnostic, errors)
                    self.assertEqual(self.events(), [])
                    if content is not None:
                        self.assertEqual(path.read_text(), content)
                finally:
                    path.write_bytes(before)

    def test_absolute_child_reference_edit_launches_without_reconciliation(self):
        # Arrange
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        child = self.workspace / '.factory/agents/feature-owner/agent.json'
        document['roster']['roles'] = [{'agent_file': str(child)}]
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()

        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)

        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.events()[0]['roster'], str(definition))
        self.assertEqual(definition.read_bytes(), before)

    def test_root_roster_accepts_omitted_envelope_keys_without_rewriting(self):
        # Arrange: the extension defaults enabled to false and roles to an empty list.
        definition = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        for roster in ({}, {'enabled': True}, {'roles': []}):
            with self.subTest(roster=roster):
                document['roster'] = roster
                definition.write_text(json.dumps(document))
                before = definition.read_bytes()
                self.terminal_log.unlink(missing_ok=True)

                # Act
                process = self.start('--new-only')
                self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
                code, _, errors = self.stop(process)

                # Assert
                self.assertEqual(code, 130, errors)
                self.assertEqual(self.events()[0]['roster'], str(definition))
                self.assertEqual(definition.read_bytes(), before)

    def test_relocated_definition_keeps_selected_guidance_and_explicit_launch_directory(self):
        # Arrange: only the definition moves, not its selected instructions or working directory.
        factory = self.workspace / '.factory'
        original = factory / 'agents/foreman/agent.json'
        definition = factory / 'definitions/dispatcher.json'
        definition.parent.mkdir()
        document = json.loads(original.read_text())
        document['agent']['cwd'] = '../agents/foreman'
        document['agent']['resources']['skills'] = ['../agents/foreman/skills']
        document['agent']['resources']['extensions'] = [
            '../resources/agentshell/extensions/agentshell.ts', '../resources/hide-tools/index.ts']
        document['roster']['roles'] = [{'agent_file': '../agents/feature-owner/agent.json'}]
        original.unlink()
        definition.write_text(json.dumps(document))
        config = factory / 'factory.toml'
        config.write_text(config.read_text().replace('agents/foreman/agent.json',
                                                     'definitions/dispatcher.json'))
        before = definition.read_bytes()

        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)

        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.events()[0]['cwd'], str(original.parent))
        self.assertEqual(self.events()[0]['resources']['skills'], [str(original.parent / 'skills')])
        self.assertEqual(definition.read_bytes(), before)
        self.assertFalse(original.exists())
