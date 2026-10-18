"""Worker setup through public configuration and init/watch boundaries."""
import json

from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.configuration import load_configuration
from forgetful_factory.domain.models import FactoryError


class WorkerConfigurationTests(InitFixture):
    def test_explicit_worker_configuration_roundtrips_without_changing_legacy_mode(self):
        # Arrange: an existing planning-only factory can be edited explicitly.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/factory.toml'
        original = path.read_text()
        tdd = self.workspace / 'tdd.md'
        tdd.write_text('Use sequential red-green-refactor.\n')
        fields = {
            'implementation_agent_model': 'gpt-5.4',
            'implementation_agent_harness': 'codex',
            'implementation_agent_effort': 'xhigh',
            'review_agent_model': 'opus',
            'review_agent_harness': 'claude_code',
            'review_agent_effort': 'high',
            'tdd_skill': str(tdd),
            'implementation_skills': [str(self.grill_skill)],
            'review_skills': [],
        }
        # Act
        legacy = load_configuration(repo)
        path.write_text(''.join(f'{k} = {json.dumps(v)}\n' for k, v in fields.items()) + original)
        configured = load_configuration(repo)
        # Assert
        self.assertIsNone(legacy.implementation_agent_model)
        for key, value in fields.items():
            self.assertEqual(getattr(configured, key), tuple(value) if isinstance(value, list)
                             else value)
        self.assertEqual(path.read_text().split('watcher_label')[1],
                         original.split('watcher_label')[1])

    def test_partial_or_malformed_worker_settings_fail_in_public_loader(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/factory.toml'
        original = path.read_text()
        for fields in ('implementation_agent_model = "gpt-5.4"\n',
                       'review_skills = ["/existing/skill.md"]\n',
                       'implementation_skills = "not-a-list"\n',
                       'review_skills = 7\n'):
            with self.subTest(fields=fields):
                path.write_text(fields + original)
                # Act / Assert
                with self.assertRaisesRegex(FactoryError, 'worker|skills'):
                    load_configuration(repo)

    def test_init_saves_explicit_workers_and_existing_config_rejects_conflicting_flags(self):
        # Arrange
        repo = self.repo()
        tdd = self.workspace / 'tdd.md'
        tdd.write_text('Sequential TDD.\n')
        from worker_support import worker_settings
        worker_settings(self)
        settings = ('--implementation-model', 'gpt-5.4', '--implementation-harness', 'codex',
                    '--implementation-effort', 'xhigh', '--review-model', 'opus',
                    '--review-harness', 'claude_code', '--review-effort', 'high',
                    '--tdd-skill', str(tdd), '--implementation-skill', str(self.grill_skill))
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertEqual(config.implementation_agent_harness, 'codex')
        self.assertEqual(config.review_agent_model, 'opus')
        self.assertEqual(config.tdd_skill, str(tdd))
        self.assertEqual(config.implementation_skills, (str(self.grill_skill),))
        path = repo / '.factory/factory.toml'
        before = path.read_bytes()
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        completion = receipt.read_bytes()
        conflict = self.run_cli(repo, '--review-model', 'sonnet')
        self.assertNotEqual(conflict.returncode, 0)
        self.assertIn('conflict', conflict.stderr)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(receipt.read_bytes(), completion)

    def test_new_onboarding_requires_a_worker_choice_without_silent_defaults(self):
        # Arrange
        repo = self.repo()
        # Act: EOF is not consent to choose worker accounts or planning-only operation.
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, worker_defaults=False)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('worker', result.stdout.lower())
        self.assertIn('--planning-only', result.stderr)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        # Act: choose planning only explicitly.
        selected = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                input='p\n', worker_defaults=False)
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertFalse(load_configuration(repo).execution_enabled)

    def test_harness_model_and_effort_validation_rejects_invalid_native_choices(self):
        # Arrange
        from worker_support import worker_settings
        repo = self.repo()
        settings = worker_settings(self)
        for flag, value in (('--implementation-harness', 'invented'),
                            ('--implementation-effort', 'high"\ninjected=true'),
                            ('--implementation-effort', 'off'),
                            ('--review-effort', 'ultra'),
                            ('--implementation-model', 'openai-codex/gpt-5.4'),
                            ('--review-model', 'not-listed')):
            with self.subTest(flag=flag, value=value):
                selected = list(settings)
                selected[selected.index(flag) + 1] = value
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *selected)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertRegex(result.stderr, 'harness|effort|not selectable')
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])

    def test_current_native_effort_vocabularies_are_distinct_and_preserved(self):
        # Arrange
        from worker_support import worker_settings
        for effort in ('none', 'ultra', 'persistent'):
            with self.subTest(effort=effort):
                repo = self.repo(effort)
                settings = list(worker_settings(self, effort=effort))
                settings[settings.index('--review-effort') + 1] = 'max'
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
                # Assert
                self.assertEqual(result.returncode, 0, result.stderr)
                config = load_configuration(repo)
                self.assertEqual(config.implementation_agent_effort, effort)
                self.assertEqual(config.review_agent_effort, 'max')
                self.assertIn('model-specific effort support', result.stdout)
                self.assertIn('does not verify model access', result.stdout)

    def test_interactive_worker_setup_uses_only_explicit_choices(self):
        # Arrange
        from worker_support import worker_settings
        repo = self.repo()
        worker_settings(self)
        answers = ('w\ncodex\ngpt-5.4\nxhigh\nclaude_code\nopus\nhigh\n'
                   + str(self.workspace / 'tdd/SKILL.md') + '\n'
                   + str(self.workspace / 'standards/SKILL.md') + '\n\n')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              worker_defaults=False, input=answers)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertEqual(config.implementation_agent_harness, 'codex')
        self.assertEqual(config.review_agent_harness, 'claude_code')
        self.assertEqual(config.implementation_agent_model, 'gpt-5.4')
        self.assertEqual(config.review_agent_model, 'opus')
        self.assertEqual(config.review_skills, ())

    def test_interactive_catalog_is_advertised_and_reused_for_each_actual_repository(self):
        from worker_support import worker_settings
        repo = self.repo()
        other = self.repo('other')
        worker_settings(self)
        log = self.workspace / 'catalogs.jsonl'
        self.env['WORKER_CATALOG_LOG'] = str(log)
        self.env['WORKER_CODEX_MODELS'] = '["catalog-choice"]'
        answers = ('w\ncodex\ncatalog-choice\nxhigh\ncodex\ncatalog-choice\nlow\n'
                   + str(self.workspace / 'tdd/SKILL.md') + '\n\n\n')
        result = self.run_cli(repo, '--repo', '.', '--repo', str(other), *INIT_SETTINGS,
                              worker_defaults=False, input=answers)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = result.stdout
        self.assertIn('Harnesses: pi, codex, claude_code', output)
        self.assertLess(output.index('catalog-choice'), output.index('Implementation model:'))
        self.assertIn('Efforts for codex: none, minimal, low, medium, high, xhigh, max', output)
        self.assertIn('network', output)
        config = load_configuration(repo)
        self.assertEqual(config.implementation_agent_model, 'catalog-choice')
        self.assertEqual(config.review_agent_model, 'catalog-choice')
        self.assertEqual([json.loads(line) for line in log.read_text().splitlines()],
                         [{'harness': 'codex', 'cwd': str(repo)},
                          {'harness': 'codex', 'cwd': str(other)}])

    def test_interactive_catalog_failure_empty_or_unlisted_choice_keeps_setup_incomplete(self):
        from worker_support import worker_settings
        worker_settings(self)
        for case in ('failed', 'empty', 'invalid'):
            with self.subTest(case=case):
                repo = self.repo(case)
                self.env['WORKER_CODEX_MODELS'] = '[]' if case == 'empty' else '["gpt-5.4"]'
                if case == 'failed':
                    self.env['WORKER_CATALOG_FAIL'] = '1'
                else:
                    self.env.pop('WORKER_CATALOG_FAIL', None)
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      worker_defaults=False, input='w\ncodex\nnot-listed\n')
                self.assertNotEqual(result.returncode, 0)
                self.assertRegex(result.stderr, 'catalog|not selectable')
                self.assertNotIn('TOP_SECRET', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())

    def test_blank_interactive_tdd_path_is_rejected_without_resolving_to_repository(self):
        from worker_support import worker_settings
        repo = self.repo()
        worker_settings(self)
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, worker_defaults=False,
                              input='w\ncodex\ngpt-5.4\nxhigh\nclaude_code\nopus\nhigh\n\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('TDD skill file cannot be blank', result.stderr)
        self.assertNotIn('Local implementation architecture', result.stdout)
        self.assertFalse((repo / '.factory/agents/implementation/resources.json').exists())
