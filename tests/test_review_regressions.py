"""Review regressions at the public CLI, with disposable external-command fixtures."""
import json
import shutil
import time

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture
from test_watch import WatchFixture
from worker_support import worker_settings

MODELS = ('provider  model  context  max-out  thinking  images\n'
          'fixture  first  128000  8192  yes  yes\n'
          'fixture  second  128000  8192  yes  yes')


class PartialSetupTests(InitFixture):
    def failed_labels(self, name='app'):
        repo = self.repo(name)
        self.env['PROFILE_MODELS'] = MODELS
        self.state.write_text(json.dumps({'fail_create': 'factory'}))
        result = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                              '--foreman-model', 'fixture/first', '--foreman-effort', 'high')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        self.assertTrue((repo / '.factory/agents/foreman/agent.json').is_file())
        state = json.loads(self.state.read_text())
        del state['fail_create']
        self.state.write_text(json.dumps(state))
        return repo

    def assert_refused(self, repo, result, before):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('agent.json', result.stderr)
        self.assertIn('preserved', result.stderr)
        self.assertIn('differs or is invalid', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertNotIn('Factory setup complete', result.stdout)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_boolean_integer_and_effort_drift_are_conflicts(self):
        # Arrange: JSON false/0 and true/1 differ even though Python equality accepts them.
        for key, value in (('inherit_personal_resources', 0), ('include_instruction_files', 1)):
            with self.subTest(key=key):
                repo = self.failed_labels(key)
                path = repo / '.factory/agents/research/agent.json'
                document = json.loads(path.read_text())
                document['agent']['resources'][key] = value
                path.write_text(json.dumps(document))
                before = {p: p.read_bytes() for p in repo.rglob('agent.json')}

                # Act
                retry = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                                     '--foreman-model', 'fixture/first', '--foreman-effort', 'high')

                # Assert: refusal must preserve the edited definitions and incomplete first setup.
                self.assert_refused(repo, retry, before)

    def test_changed_foreman_choices_refused_after_first_label_failure(self):
        repo = self.failed_labels()
        before = {p: p.read_bytes() for p in repo.rglob('agent.json')}

        retry = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                             '--foreman-model', 'fixture/second', '--foreman-effort', 'low')

        self.assert_refused(repo, retry, before)


    def test_matching_retry_accepts_equal_document_without_reformatting(self):
        repo = self.failed_labels()
        definition = repo / '.factory/agents/foreman/agent.json'
        definition.write_text(json.dumps(json.loads(definition.read_text()), indent=4) + '\n')
        before = {p: p.read_bytes() for p in repo.rglob('agent.json')}

        retry = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                             '--foreman-model', 'fixture/first', '--foreman-effort', 'high')

        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual({p: p.read_bytes() for p in before}, before)
        self.assertEqual(json.loads((repo / '.factory/setup-complete.json').read_text()),
                         {'complete': True})

    def test_invalid_preserved_definition_refuses_first_setup_retry(self):
        repo = self.failed_labels()
        definition = repo / '.factory/agents/research/agent.json'
        definition.write_bytes(b'{invalid\xff')
        before = {p: p.read_bytes() for p in repo.rglob('agent.json')}

        retry = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                             '--foreman-model', 'fixture/first', '--foreman-effort', 'high')

        self.assert_refused(repo, retry, before)

    def test_changed_worker_choices_refused_after_review_skill_failure(self):
        self.worker_retry(model='gpt-5.5', effort='high')

    def test_changed_worker_harness_refused_after_review_skill_failure(self):
        self.worker_retry(harness='claude_code', model='opus', effort='high')

    def worker_retry(self, **choices):
        repo = self.repo()
        self.env['WORKER_CODEX_MODELS'] = '["gpt-5.4", "gpt-5.5"]'
        settings = list(worker_settings(self))
        settings[settings.index('--review-skill') + 1] = str(self.workspace / 'missing.md')
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        self.assertNotEqual(failed.returncode, 0)
        self.assertTrue((repo / '.factory/agents/implementation/agent.json').is_file())
        before = {p: p.read_bytes() for p in repo.rglob('agent.json')}

        retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             *worker_settings(self, **choices))

        self.assert_refused(repo, retry, before)


class WatchOutcomeFixture(WatchFixture):
    def launch_outcome(self):
        process = self.start('--new-only')
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if any(e['kind'] == 'ready' for e in self.events()):
                _, _, errors = self.stop(process)
                return 'launched', errors
            if process.poll() is not None:
                _, errors = process.communicate()
                return 'rejected', errors
            time.sleep(0.02)
        self.stop(process)
        return 'timeout', ''



class RequiredGuidanceTests(WatchOutcomeFixture):
    def test_required_guidance_excluded_by_folder_rules_refuses_launch(self):
        skills = self.workspace / '.factory/agents/foreman/skills'
        original = skills / 'foreman'
        for relocated in ('.archive/foreman', 'node_modules/old/foreman',
                          'factory-maintenance/examples/foreman'):
            with self.subTest(relocated=relocated):
                target = skills / relocated
                target.parent.mkdir(parents=True, exist_ok=True)
                original.rename(target)
                self.terminal_log.unlink(missing_ok=True)
                try:
                    outcome, errors = self.launch_outcome()

                    self.assertEqual(outcome, 'rejected', errors)
                    self.assertIn('Required Foreman guidance', errors)
                    self.assertEqual(self.events(), [])
                finally:
                    target.rename(original)

    def test_symlinked_required_guidance_folder_can_launch(self):
        skills = self.workspace / '.factory/agents/foreman/skills'
        shared = self.workspace / 'shared-guidance/foreman'
        shared.parent.mkdir()
        shutil.move(str(skills / 'foreman'), str(shared))
        (skills / 'foreman').symlink_to(shared, target_is_directory=True)

        outcome, errors = self.launch_outcome()

        self.assertEqual(outcome, 'launched', errors)
        launch = next(e for e in self.events() if e['kind'] == 'launch')
        self.assertEqual(launch['resources']['skills'], [str(skills)])

    def test_ancestor_cycle_refuses_launch_without_following_it_forever(self):
        skills = self.workspace / '.factory/agents/foreman/skills'
        (skills / 'loop').symlink_to(skills, target_is_directory=True)

        outcome, errors = self.launch_outcome()

        self.assertEqual(outcome, 'rejected', errors)
        self.assertIn('cycle', errors)
        self.assertEqual(self.events(), [])

    def test_distinct_required_guidance_candidates_refuse_ambiguous_launch(self):
        skills = self.workspace / '.factory/agents/foreman/skills'
        shutil.copytree(skills / 'foreman', skills / 'extra/foreman')

        outcome, errors = self.launch_outcome()

        self.assertEqual(outcome, 'rejected', errors)
        self.assertIn('Ambiguous required Foreman guidance', errors)
        self.assertEqual(self.events(), [])



class RenewedConsentTests(InitFixture):
    def completed_setup(self):
        repo = self.repo()
        self.log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(self.log)
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.log.unlink()
        return repo

    def test_finalize_saves_new_consent_without_recreating_templates_or_querying_models(self):
        repo = self.completed_setup()
        consent = repo / '.factory/pi-profile.json'
        consent.unlink()
        guidance = repo / '.factory/agents/foreman/APPEND_SYSTEM.md'
        guidance.unlink()
        before = {p: p.read_bytes() for p in (repo / '.factory/agents').rglob('*') if p.is_file()}
        new_home = self.workspace / 'approved native home'
        (new_home / 'extensions').mkdir(parents=True)
        (new_home / 'extensions/agentshell.json').write_text('{"max_sub_agent_depth": 1}')
        ordinary = self.run_cli(repo, '--pi-agent-dir', str(new_home))
        self.assertEqual(ordinary.returncode, 0, ordinary.stderr)
        self.assertFalse(consent.exists())
        self.assertEqual(events(self.log), [])

        final = self.run_cli(repo, '--finalize', '--pi-agent-dir', str(new_home))

        self.assertEqual(final.returncode, 0, final.stderr)
        self.assertEqual(json.loads(consent.read_text()),
                         {'agent_directory': str(new_home), 'shared_profile_consent': True})
        self.assertFalse(guidance.exists())
        self.assertEqual({p: p.read_bytes() for p in before}, before)
        self.assertFalse(any(e['name'] == 'pi' for e in events(self.log)))
        self.assertEqual(json.loads((repo / '.factory/setup-complete.json').read_text()),
                         {'complete': True})

    def test_declined_finalization_consent_preserves_files_without_external_calls(self):
        repo = self.completed_setup()
        consent = repo / '.factory/pi-profile.json'
        consent.unlink()
        before = {p: p.read_bytes() for p in (repo / '.factory').rglob('*') if p.is_file()}
        github = self.state.read_bytes()

        final = self.run_cli(repo, '--finalize', pi_defaults=False, input='n\n')

        self.assertNotEqual(final.returncode, 0)
        self.assertIn('Shared Pi profile consent declined', final.stderr)
        self.assertFalse(consent.exists())
        self.assertEqual({p: p.read_bytes() for p in before}, before)
        self.assertEqual(self.state.read_bytes(), github)
        self.assertEqual(events(self.log), [])

    def test_malformed_consent_cannot_be_replaced_by_finalize_approval(self):
        repo = self.completed_setup()
        consent = repo / '.factory/pi-profile.json'
        consent.write_bytes(b'{invalid')
        before = consent.read_bytes()

        final = self.run_cli(repo, '--finalize')

        self.assertNotEqual(final.returncode, 0)
        self.assertIn('consent', final.stderr)
        self.assertEqual(consent.read_bytes(), before)
        self.assertEqual(events(self.log), [])



class RuntimeDiagnosticsTests(WatchFixture):
    def test_unknown_status_points_to_standalone_recovery_preserving_recorded_state(self):
        state = self.workspace / '.factory/runtime/foreman/owner.json'
        state.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        state.write_text(json.dumps({'workspace': str(self.workspace), 'run_id': 'unknown-fixture',
                                     'foreman': 'unknown', 'watcher': 'stopped', 'target': None}))
        before = state.read_bytes()

        process = self.start('--status')
        output, errors = process.communicate(timeout=5)

        self.assertEqual(process.returncode, 0, errors)
        observed = json.loads(output)
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertIn('then retry foreman --workspace', observed['recovery'])
        self.assertIn('independently confirming', observed['recovery'])
        self.assertIn('If uncertain, preserve them', observed['recovery'])
        self.assertNotIn('init --assisted', observed['recovery'])
        self.assertEqual(state.read_bytes(), before)
        self.assertEqual(self.events(), [])

    def test_profile_failures_give_working_recovery_routes_without_launch(self):
        factory = self.workspace / '.factory'
        skill = factory / 'agents/foreman/skills/foreman/SKILL.md'
        consent = factory / 'pi-profile.json'
        extension = factory / 'resources/agentshell/extensions/agentshell.ts'
        missing_home = json.loads(consent.read_text())
        missing_home['agent_directory'] = str(self.workspace / 'missing-home')
        cases = ((extension, b'edited audited resource', 'audited bundle', 'restart'),
                 (consent, None, 'consent', 'init --finalize'),
                 (consent, json.dumps(missing_home).encode(), 'home does not exist', 'foreman'),
                 (skill, b'\xff', 'valid UTF-8', 'restart'),
                 (skill, b'Do not start implementation or dispatch feature owners.',
                  'discussion-only', 'restart'),
                 (skill, b'cd "$PI_CODING_AGENT_DIR"', 'obsolete', 'restart'))
        for path, content, reason, route in cases:
            with self.subTest(reason=reason):
                original = path.read_bytes()
                if content is None:
                    path.unlink()
                else:
                    path.write_bytes(content)
                try:
                    process = self.start('--new-only')
                    _, errors = process.communicate(timeout=5)

                    self.assertNotEqual(process.returncode, 0)
                    self.assertIn(reason, errors)
                    self.assertIn(route, errors)
                    self.assertNotIn('rerun init', errors)
                    self.assertEqual(self.events(), [])
                    self.assertEqual(path.read_bytes() if path.exists() else None, content)
                finally:
                    path.write_bytes(original)

    def test_readiness_does_not_claim_disabled_instructions_were_loaded(self):
        path = self.workspace / '.factory/agents/foreman/agent.json'
        document = json.loads(path.read_text())
        document['agent']['resources']['include_instruction_files'] = False
        path.write_text(json.dumps(document))

        process = self.start('--new-only')
        self.wait_until(process, lambda: json.loads(self.state_path.read_text()).get('counts'))
        code, output, errors = self.stop(process)

        self.assertEqual(code, 130, errors)
        self.assertIn('Foreman session ready', output)
        self.assertIn('Resource loading unverified', output)
        self.assertNotIn('instructions loaded', output)
        launch = next(e for e in self.events() if e['kind'] == 'launch')
        self.assertIs(launch['resources']['include_instruction_files'], False)

    def test_failed_backend_readiness_names_finalize_or_restart_and_keeps_diagnostics_private(self):
        self.env['PROFILE_FAIL'] = 'forgetful'

        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)

        self.assertNotEqual(process.returncode, 0)
        self.assertIn('planning check failed', errors)
        self.assertIn('init --finalize', errors)
        self.assertIn('restart', errors)
        self.assertNotIn('rerun init.', errors)
        self.assertNotIn('TOP_SECRET', errors)
        self.assertEqual(self.events(), [])


class GeneratedGuidanceTests(InitFixture):
    def test_foreman_setup_guidance_explains_complete_roster_and_python_completion_gate(self):
        repo = self.repo()

        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)

        self.assertEqual(setup.returncode, 0, setup.stderr)
        root = repo / '.factory/agents/foreman'
        guidance = (root / 'AGENTS.md').read_text()
        self.assertIn('complete starter roster is already present', guidance)
        self.assertIn('Python refuses watching until first setup completes', guidance)
        self.assertIn('instructions do not sandbox tools or prevent dispatch', guidance)
        self.assertIn('init --finalize', guidance)
        self.assertIn('do not dispatch', guidance)
        self.assertNotIn('empty roster', guidance)
        self.assertEqual(json.loads((root / 'agent.json').read_text())['roster'],
                         {'enabled': True,
                          'roles': [{'agent_file': '../feature-owner/agent.json'}]})

    def test_owner_guidance_uses_explicit_permission_and_its_own_selected_definition(self):
        repo = self.repo()

        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))

        self.assertEqual(setup.returncode, 0, setup.stderr)
        owner = repo / '.factory/agents/feature-owner'
        instructions = (owner / 'AGENTS.md').read_text()
        workflow = (owner / 'skills/feature-owner/SKILL.md').read_text()
        self.assertIn('execution_enabled', instructions)
        self.assertIn('$FACTORY_WORKSPACE/.factory/factory.toml', instructions)
        self.assertIn('$FACTORY_WORKSPACE/.factory/factory.toml', workflow)
        self.assertIn('$PI_AGENTSHELL_ROSTER_FILE', workflow)
        self.assertNotIn('research-only roster means planning-only', instructions)
        for phrase in ('full role', 'TDD for implementation', 'additional skills',
                       'absolute SKILL.md', 'before work', 'configured responsibilities',
                       'independent review', 'acceptance criteria', 'auto_approve false'):
            self.assertIn(phrase, workflow)

    def test_maintenance_guidance_accepts_local_relative_or_absolute_child_references(self):
        repo = self.repo()

        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)

        self.assertEqual(setup.returncode, 0, setup.stderr)
        skill = repo / '.factory/agents/foreman/skills/factory-maintenance/SKILL.md'
        guidance = ' '.join(skill.read_text().split())
        self.assertIn('local relative or absolute `agent_file`', guidance)
        self.assertIn('Children own their settings', guidance)
        self.assertIn('Do not claim that selecting a path proves native loading', guidance)


class LocalSelectorTests(WatchOutcomeFixture):
    def test_existing_scheme_paths_cannot_be_used_as_selected_resources(self):
        root = self.workspace / '.factory/agents/foreman'
        definition = root / 'agent.json'
        original = definition.read_bytes()
        for selector in ('file:skills', 'Custom:skills', '~skills', '!skills', 'npm:skills'):
            with self.subTest(selector=selector):
                folder = root / selector
                folder.mkdir()
                (folder / 'SKILL.md').write_text('---\nname: example\ndescription: Fixture.\n---\n')
                document = json.loads(original)
                document['agent']['resources']['skills'].append(selector)
                definition.write_text(json.dumps(document))
                before = definition.read_bytes()
                self.terminal_log.unlink(missing_ok=True)

                outcome, errors = self.launch_outcome()

                self.assertEqual(outcome, 'rejected', errors)
                self.assertIn('local paths', errors)
                self.assertNotIn('Missing selected', errors)
                self.assertEqual(definition.read_bytes(), before)
                self.assertEqual(self.events(), [])

    def test_existing_scheme_or_tilde_cwd_cannot_be_used_as_launch_directory(self):
        root = self.workspace / '.factory/agents/foreman'
        definition = root / 'agent.json'
        original = definition.read_bytes()
        for selector in ('file:launch', 'Custom:launch', '~launch'):
            with self.subTest(selector=selector):
                (root / selector).mkdir()
                document = json.loads(original)
                document['agent']['cwd'] = selector
                definition.write_text(json.dumps(document))
                before = definition.read_bytes()
                self.terminal_log.unlink(missing_ok=True)

                outcome, errors = self.launch_outcome()

                self.assertEqual(outcome, 'rejected', errors)
                self.assertIn('cwd must select a local path', errors)
                self.assertEqual(definition.read_bytes(), before)
                self.assertEqual(self.events(), [])


class RelocatedCompletionTests(InitFixture):
    def test_finalization_points_to_selected_definition_after_team_relocation(self):
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        factory = repo / '.factory'
        team = repo / 'custom-team'
        team.mkdir()
        names = {'foreman': 'captain', 'feature-owner': 'planner', 'research': 'analyst'}
        for role, name in names.items():
            old = factory / 'agents' / role
            definition = json.loads((old / 'agent.json').read_text())
            definition['agent']['name'] = name
            resources = definition['agent']['resources']
            resources['extensions'] = [str((old / value).resolve())
                                       for value in resources['extensions']]
            for child in definition['roster']['roles']:
                child_role = child['agent_file'].split('/')[1]
                child['agent_file'] = f'../{names[child_role]}/agent.json'
            (old / 'agent.json').write_text(json.dumps(definition))
            old.rename(team / name)
        config = factory / 'factory.toml'
        config.write_text(config.read_text().replace('agents/foreman/agent.json',
                                                     '../custom-team/captain/agent.json'))
        before = {p: p.read_bytes() for p in team.rglob('*') if p.is_file()}
        config_before = config.read_bytes()

        final = self.run_cli(repo, '--finalize')

        self.assertEqual(final.returncode, 0, final.stderr)
        self.assertIn(str(team / 'captain/agent.json'), final.stdout)
        self.assertIn('selected skills directories', final.stdout)
        self.assertNotIn(str(factory / 'agents'), final.stdout)
        self.assertEqual({p: p.read_bytes() for p in before}, before)
        self.assertEqual(config.read_bytes(), config_before)
        self.assertEqual(list((factory / 'agents').iterdir()), [])


class SavedSetupDiagnosticTests(InitFixture):
    def test_finalize_configuration_errors_name_explicit_validation_and_restart_routes(self):
        cases = (('project', 'lacks forgetful.project_id'),
                 ('arguments', 'Arguments conflict with existing config'),
                 ('provider', 'Unsupported work-tracking provider'),
                 ('origin', 'Origin/source changed'))
        for completed in (False, True):
            for case, reason in cases:
                with self.subTest(case=case, completed=completed):
                    # Arrange: public init saves config before the first access check can fail.
                    repo = self.repo(f'{case}-{completed}')
                    if not completed:
                        self.env['PROFILE_FAIL'] = 'forgetful'
                    setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
                    self.env.pop('PROFILE_FAIL', None)
                    self.assertEqual(setup.returncode == 0, completed, setup.stderr)
                    config = repo / '.factory/factory.toml'
                    self.assertTrue(config.is_file())
                    receipt = repo / '.factory/setup-complete.json'
                    self.assertEqual(receipt.exists(), completed)
                    if case == 'project':
                        config.write_text(config.read_text().replace('project_id = 12\n', ''))
                    elif case == 'provider':
                        config.write_text(config.read_text().replace('provider = "github"',
                                                                     'provider = "linear"'))
                    elif case == 'origin':
                        self.git(repo, 'remote', 'set-url', 'origin',
                                 'git@github.com:team/other.git')
                    flags = ('--label', 'different') if case == 'arguments' else ()
                    before = {p: p.read_bytes() for p in (repo / '.factory').rglob('*')
                              if p.is_file()}
                    github = self.state.read_bytes()
                    self.log = self.workspace / f'{case}-{completed}.jsonl'
                    self.env['PROFILE_LOG'] = str(self.log)

                    # Act
                    result = self.run_cli(repo, '--finalize', *flags)

                    # Assert: the exact diagnostic branch, with no config/receipt/backend writes.
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(reason, result.stderr)
                    self.assertNotIn('Traceback', result.stderr)
                    self.assertNotIn('First setup validated', result.stdout)
                    self.assertEqual({p: p.read_bytes() for p in before}, before)
                    self.assertEqual(receipt.exists(), completed)
                    self.assertEqual(self.state.read_bytes(), github)
                    self.assertEqual(events(self.log), [])
                    self.assertIn('init --finalize', result.stderr)
                    self.assertIn('restart watch or foreman', result.stderr)
                    self.assertNotIn('rerun init', result.stderr)

    def test_initial_mcp_failure_explains_new_setup_choice_without_claiming_saved_configuration(
            self):
        repo = self.repo()
        self.log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(self.log)

        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--forgetful-method', 'mcp')

        self.assertNotEqual(result.returncode, 0)
        self.assertIn('MCP configuration is unsupported', result.stderr)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        self.assertEqual(events(self.log), [])
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertIn('For new setup', result.stderr)
        self.assertIn('--forgetful-method cli', result.stderr)


class SavedConfigurationDiagnosticTests(WatchFixture):
    def test_saved_mcp_configuration_is_preserved_with_finalize_or_restart_guidance(self):
        # Arrange: the existing completed configuration selects an unsupported method.
        config = self.workspace / '.factory/factory.toml'
        config.write_text(config.read_text().replace('[forgetful]', '[forgetful]\nmethod = "mcp"'))
        before = config.read_bytes()
        receipt = self.workspace / '.factory/setup-complete.json'
        completion = receipt.read_bytes()
        github = self.state_path.read_bytes()

        # Act
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)

        # Assert: config loading rejects this method before any runtime or backend operation.
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('MCP configuration is unsupported', errors)
        self.assertIn('method = "cli"', errors)
        self.assertEqual(config.read_bytes(), before)
        self.assertEqual(receipt.read_bytes(), completion)
        self.assertEqual(self.state_path.read_bytes(), github)
        self.assertEqual(self.events(), [])
        self.assertIn('init --finalize', errors)
        self.assertIn('restart watch or foreman', errors)
        self.assertNotIn('rerun init', errors)


class MalformedPlanningReplyTests(WatchFixture):
    def reject_reply(self, tool):
        # Only the external fake's reply is damaged, after it saves the operation's actual result.
        program = self.bin / 'forgetful'
        content = program.read_text()
        marker = '        print(json.dumps(result))\n'
        self.assertEqual(content.count(marker), 1)
        program.write_text(content.replace(marker,
            "        if tool == os.environ.get('RESIDUAL_BAD_REPLY'):\n"
            "            print('TOP_SECRET malformed native reply')\n"
            "            sys.exit(0)\n" + marker))
        self.env['RESIDUAL_BAD_REPLY'] = tool

    def test_malformed_plan_read_requires_reconciliation_without_raw_diagnostics(self):
        # Arrange: ordinary readiness succeeds; the later list_plans reply is invalid JSON.
        self.reject_reply('list_plans')
        receipt = self.workspace / '.factory/setup-complete.json'
        completion = receipt.read_bytes()

        # Act
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)

        # Assert: reach the generic reply handler after launch, then close without delivery.
        self.assertNotEqual(process.returncode, 0)
        self.assertRegex(errors, r'Forgetful (check failed|reply was invalid)')
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual([call[0] for call in state['calls']], ['list_plans'])
        self.assertEqual(state['plans'], [])
        self.assertEqual(receipt.read_bytes(), completion)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])
        self.assertNotIn('TOP_SECRET', errors)
        self.assertNotIn('Traceback', errors)
        self.assertIn('Inspect and reconcile', errors)
        self.assertIn('init --finalize', errors)
        self.assertIn('restart watch or foreman', errors)
        self.assertNotIn('rerun init', errors)

    def test_malformed_write_reply_keeps_intent_and_cannot_authorize_replay(self):
        # Arrange: update_plan commits the ownership intent but its reply cannot be interpreted.
        self.reject_reply('update_plan')
        self.script({'team/app': [[[self.issue()]]]})
        receipt = self.workspace / '.factory/setup-complete.json'
        completion = receipt.read_bytes()

        # Act
        process = self.start('--existing')
        _, errors = process.communicate(timeout=5)

        # Assert: the diagnostic cannot suggest that repeating an uncertain write is safe.
        self.assertNotEqual(process.returncode, 0)
        self.assertRegex(errors, r'Forgetful (check failed|reply was invalid)')
        state_path = self.workspace / '.factory/fixture-plans.json'
        state = json.loads(state_path.read_text())
        self.assertEqual(len(state['plans']), 1)
        self.assertEqual(state['tasks'], [])
        self.assertTrue(json.loads(state['plans'][0]['context'])['ownership_create_started'])
        self.assertEqual([call[0] for call in state['calls']].count('update_plan'), 1)
        self.assertNotIn('TOP_SECRET', errors)
        self.assertNotIn('Traceback', errors)
        self.assertIn('Inspect and reconcile', errors)
        self.assertIn('do not replay uncertain writes', errors)
        self.assertIn('After reconciliation', errors)

        # Act: merely fixing the reply and restarting cannot clear the existing uncertainty gate.
        del self.env['RESIDUAL_BAD_REPLY']
        restarted = self.start('--existing')
        _, retry_errors = restarted.communicate(timeout=5)

        # Assert: no second write or notification; the public outer recovery rules remain intact.
        self.assertNotEqual(restarted.returncode, 0)
        self.assertIn('Ownership creation uncertain', retry_errors)
        after = json.loads(state_path.read_text())
        writes = [call[0] for call in after['calls'] if call[0].startswith(('create_', 'update_'))]
        self.assertEqual(writes, ['create_plan', 'update_plan'])
        self.assertEqual(after['plans'], state['plans'])
        self.assertEqual(after['tasks'], [])
        self.assertEqual(receipt.read_bytes(), completion)
        self.assertFalse(any(e['kind'] == 'send' for e in self.events()))
        self.assertEqual(sum(e['kind'] == 'close' for e in self.events()), 2)
