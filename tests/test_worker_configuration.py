"""Worker setup through public configuration and init/watch boundaries."""
import json

from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.cli.numbered_selection import parse_numbered_selection
from forgetful_factory.configuration import load_configuration
from forgetful_factory.domain.models import FactoryError


class WorkerConfigurationTests(InitFixture):
    def agent(self, repo, role):
        return json.loads((repo / f'.factory/agents/{role}/agent.json').read_text())['agent']

    def test_worker_settings_belong_only_to_selected_definitions(self):
        # Arrange / Act
        from worker_support import worker_settings
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config = load_configuration(repo)
        self.assertEqual(set(vars(config)), {'watcher_label', 'foreman_agent_file', 'repository',
                                            'forgetful', 'execution_enabled'})
        implementation = self.agent(repo, 'implementation')
        self.assertEqual(implementation['model'], 'gpt-5.4')
        self.assertEqual(implementation['agent_type'], 'codex')
        self.assertEqual(implementation['effort'], 'xhigh')
        self.assertIn(str(self.workspace / 'tdd/SKILL.md'),
                      implementation['resources']['skills'])

    def test_partial_or_malformed_worker_settings_fail_in_public_loader(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/factory.toml'
        original = path.read_text()
        for fields in ('implementation_agent_model = "gpt-5.4"\n',
                       'tdd_skill = "/existing/skill.md"\n',
                       'tdd_skill = ""\n',
                       'review_skills = ["/existing/skill.md"]\n',
                       'implementation_skills = "not-a-list"\n',
                       'review_skills = 7\n'):
            with self.subTest(fields=fields):
                path.write_text(fields + original)
                # Act / Assert
                with self.assertRaisesRegex(FactoryError, 'Unknown Factory settings'):
                    load_configuration(repo)

    def test_init_saves_explicit_workers_and_repeated_init_preserves_them(self):
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

        self.assertEqual(self.agent(repo, 'implementation')['agent_type'], 'codex')
        self.assertEqual(self.agent(repo, 'review')['model'], 'opus')
        self.assertIn(str(tdd), self.agent(repo, 'implementation')['resources']['skills'])
        self.assertIn(str(self.grill_skill),
                      self.agent(repo, 'implementation')['resources']['skills'])
        path = repo / '.factory/factory.toml'
        before = path.read_bytes()
        receipt = repo / '.factory/setup-complete.json'
        completion = receipt.read_bytes()
        conflict = self.run_cli(repo, '--review-model', 'sonnet')
        self.assertEqual(conflict.returncode, 0, conflict.stderr)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(receipt.read_bytes(), completion)

    def test_worker_flags_need_no_skills_but_explicit_tdd_values_are_still_validated(self):
        # Arrange: only the six worker app/model/effort flags are supplied.
        from worker_support import worker_settings
        repo = self.repo()
        settings = worker_settings(self)[:12]
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config = load_configuration(repo)
        self.assertTrue(config.execution_enabled)
        self.assertEqual(self.agent(repo, 'implementation')['resources']['skills'], ['./skills'])
        path = repo / '.factory/factory.toml'
        original = path.read_text()
        for value in ('', ' ', 42, False, [], '\x00'):
            with self.subTest(value=value):
                path.write_text(f'tdd_skill = {json.dumps(value)}\n' + original)
                with self.assertRaisesRegex(FactoryError, 'Unknown Factory settings|Invalid TOML'):
                    load_configuration(repo)
        path.write_text(original)
        # Act / Assert: re-init preserves an already valid worker setup with no custom skills.
        before = path.read_bytes()
        retry = self.run_cli(repo, worker_defaults=False)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(path.read_bytes(), before)

    def test_new_onboarding_requires_a_worker_choice_without_silent_defaults(self):
        # Arrange
        repo = self.repo()
        # Act: EOF is not consent to choose worker accounts or planning-only operation.
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, worker_defaults=False)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('How would you like to set up your factory?', result.stdout)
        self.assertIn('Select 1 or 2:', result.stdout)
        self.assertIn('--planning-only', result.stderr)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        # Act: choose planning only explicitly.
        selected = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                '--planning-only', worker_defaults=False)
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertFalse(load_configuration(repo).execution_enabled)
        for role in ('foreman', 'feature-owner', 'research'):
            self.assertIn(str(repo / '.factory/agents' / role / 'skills'), selected.stdout)
        for role in ('implementation', 'review'):
            self.assertNotIn(str(repo / '.factory/agents' / role / 'skills'), selected.stdout)
        self.assertIn('Agent settings live in agent.json', selected.stdout)

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

                self.assertEqual(self.agent(repo, 'implementation')['effort'], effort)
                self.assertEqual(self.agent(repo, 'review')['effort'], 'max')
                self.assertIn('model-specific effort support', result.stdout)
                self.assertIn('does not verify model access', result.stdout)

    def test_interactive_worker_setup_uses_only_explicit_choices(self):
        # Arrange
        from worker_support import worker_settings
        repo = self.repo()
        worker_settings(self)
        answers = '1\n1\n5\n1\n5\n2\n1\n6\n3\n1\n3\n'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              worker_defaults=False, input=answers)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)

        self.assertEqual(self.agent(repo, 'implementation')['agent_type'], 'codex')
        self.assertEqual(self.agent(repo, 'review')['agent_type'], 'claude_code')
        self.assertEqual(self.agent(repo, 'implementation')['model'], 'gpt-5.4')
        self.assertEqual(self.agent(repo, 'review')['model'], 'opus')
        self.assertEqual(self.agent(repo, 'implementation')['effort'], 'xhigh')
        self.assertEqual(self.agent(repo, 'review')['effort'], 'high')
        for title, role in (('Feature-owner', 'feature-owner'), ('Research', 'research')):
            self.assertIn(f'{title} model choices:\n  1. provider/model', result.stdout)
            self.assertIn(f'Select {title} model number:', result.stdout)
            self.assertIn(f'Select {title} effort number:', result.stdout)
            self.assertEqual(self.agent(repo, role)['model'], 'provider/model')
            self.assertEqual(self.agent(repo, role)['effort'], 'high')
        self.assertIn('Implementation app choices:\n  1. pi\n  2. codex\n  3. claude_code',
                      result.stdout)
        self.assertIn('Select Implementation app number:', result.stdout)
        self.assertIn('Implementation model choices:\n  1. gpt-5.4', result.stdout)
        self.assertIn('Select Implementation model number:', result.stdout)
        self.assertIn('Implementation effort choices:\n  1. none\n  2. minimal\n  3. low\n'
                      '  4. medium\n  5. high\n  6. xhigh\n  7. max\n  8. ultra\n'
                      '  9. persistent', result.stdout)
        self.assertIn('Select Implementation effort number:', result.stdout)
        self.assertIn('Review app choices:\n  1. pi\n  2. codex\n  3. claude_code',
                      result.stdout)
        self.assertIn('Select Review app number:', result.stdout)
        self.assertIn('Review model choices:\n  1. opus', result.stdout)
        self.assertIn('Select Review model number:', result.stdout)
        self.assertIn('Review effort choices:\n  1. low\n  2. medium\n  3. high\n'
                      '  4. xhigh\n  5. max', result.stdout)
        self.assertIn('Select Review effort number:', result.stdout)
        self.assertEqual(self.agent(repo, 'review')['resources']['skills'], ['./skills'])

    def test_numbered_selection_preserves_all_worker_answer_results(self):
        # Arrange: preserve every answer from the former seven-prompt CLI matrix.
        prompts = (
            ('Setup', 2, '3', 'Manual'),
            ('Implementation app', 3, '4', 'codex'),
            ('Implementation model', 1, '2', 'gpt-5.4'),
            ('Implementation effort', 9, '10', 'xhigh'),
            ('Review app', 3, '4', 'claude_code'),
            ('Review model', 1, '2', 'opus'),
            ('Review effort', 5, '6', 'high'),
        )
        for label, choice_count, upper, old_name in prompts:
            invalid = (('', 'number'), ('not-a-number', 'number'), ('0', 'range'),
                       ('-1', 'range'), (upper, 'range'), (old_name, 'number'))
            for answer, failure in invalid:
                with self.subTest(prompt=label, answer=answer):
                    expected = (f'{label}: select a number from 1 to {choice_count}.'
                                if failure == 'number' else
                                f'{label} selection is out of range; '
                                f'select a number from 1 to {choice_count}.')
                    # Act / Assert
                    with self.assertRaises(FactoryError) as raised:
                        parse_numbered_selection(label, answer, choice_count)
                    self.assertEqual(str(raised.exception), expected)
            # Act / Assert: preserve both accepted endpoints for each prompt.
            self.assertEqual(parse_numbered_selection(label, '1', choice_count), 1)
            self.assertEqual(
                parse_numbered_selection(label, str(choice_count), choice_count),
                choice_count,
            )

    def test_invalid_worker_numbers_stop_before_config_or_label_changes(self):
        # Keep one invalid answer at every distinct CLI prompt, without repeating the matrix.
        from worker_support import worker_settings
        worker_settings(self)
        cases = (
            ('Setup', '', 'Manual'),
            ('Implementation app', '1\n1\n5\n1\n5\n', 'codex'),
            ('Implementation model', '1\n1\n5\n1\n5\n2\n', 'gpt-5.4'),
            ('Implementation effort', '1\n1\n5\n1\n5\n2\n1\n', '10'),
            ('Review app', '1\n1\n5\n1\n5\n2\n1\n6\n', 'claude_code'),
            ('Review model', '1\n1\n5\n1\n5\n2\n1\n6\n3\n', 'opus'),
            ('Review effort', '1\n1\n5\n1\n5\n2\n1\n6\n3\n1\n', '6'),
        )
        for index, (label, prefix, answer) in enumerate(cases):
            with self.subTest(prompt=label):
                # Arrange
                repo = self.repo(f'choice-{index}')
                self.state.write_text('{}')
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      worker_defaults=False, input=prefix + answer + '\n')
                # Assert
                self.assertEqual(result.returncode, 1)
                self.assertIn(label, result.stderr)
                self.assertIn('select a number from 1 to', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/setup-complete.json').exists())
                self.assertEqual(json.loads(self.state.read_text()), {})

    def test_numbered_pi_workers_preserve_exact_models_and_native_effort_order(self):
        # Arrange
        from worker_support import worker_settings
        repo = self.repo()
        worker_settings(self)
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'z-provider  special/model  128000  8192  yes  yes\n'
            'provider  model  128000  8192  yes  yes')
        answers = '1\n1\n5\n1\n5\n1\n2\n1\n1\n1\n7\n'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              worker_defaults=False, input=answers)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Implementation model choices:\n  1. provider/model\n'
                      '  2. z-provider/special/model', result.stdout)
        self.assertIn('Implementation effort choices:\n  1. off\n  2. minimal\n  3. low\n'
                      '  4. medium\n  5. high\n  6. xhigh\n  7. max', result.stdout)

        self.assertEqual(self.agent(repo, 'implementation')['agent_type'], 'pi')
        self.assertEqual(self.agent(repo, 'review')['agent_type'], 'pi')
        self.assertEqual(self.agent(repo, 'implementation')['model'], 'z-provider/special/model')
        self.assertEqual(self.agent(repo, 'review')['model'], 'provider/model')
        self.assertEqual(self.agent(repo, 'implementation')['effort'], 'off')
        self.assertEqual(self.agent(repo, 'review')['effort'], 'max')

    def test_interactive_catalog_is_advertised_and_reused_for_each_actual_repository(self):
        # Arrange: catalogs differ in order and in choices available to only one repository.
        from worker_support import worker_settings
        repo = self.repo()
        other = self.repo('other')
        worker_settings(self)
        log = self.workspace / 'catalogs.jsonl'
        catalogs = {str(repo): ['z/special/model', 'catalog-choice', 'only-first-repo'],
                    str(other): ['only-other-repo', 'catalog-choice', 'z/special/model']}
        (self.bin / 'codex').write_text(
            '#!/usr/bin/env python3\n'
            'import json, os, sys\n'
            'from pathlib import Path\n'
            'assert sys.argv[1:] == ["debug", "models"]\n'
            f'catalogs = {catalogs!r}\n'
            f'with Path({str(log)!r}).open("a") as stream:\n'
            '    stream.write(json.dumps({"harness": "codex", "cwd": os.getcwd()}) + "\\n")\n'
            'print(json.dumps({"models": [{"slug": value, "visibility": "list"}\n'
            '                             for value in catalogs[os.getcwd()]]}))\n')
        answers = '1\n1\n5\n1\n5\n2\n2\n6\n2\n1\n3\n'
        # Act
        result = self.run_cli(repo, '--repo', '.', '--repo', str(other), *INIT_SETTINGS,
                              worker_defaults=False, input=answers)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        output = result.stdout
        self.assertIn('Implementation app choices:\n  1. pi\n  2. codex\n  3. claude_code', output)
        self.assertLess(output.index('catalog-choice'), output.index('Select Implementation model'))
        self.assertIn('Implementation effort choices:\n  1. none\n  2. minimal\n  3. low\n'
                      '  4. medium\n  5. high\n  6. xhigh\n  7. max', output)
        self.assertIn('network', output)
        self.assertIn('Implementation model choices:\n  1. catalog-choice\n'
                      '  2. z/special/model', output)
        self.assertNotIn('only-first-repo', output)
        self.assertNotIn('only-other-repo', output)

        self.assertEqual(self.agent(repo, 'implementation')['model'], 'z/special/model')
        self.assertEqual(self.agent(repo, 'review')['model'], 'catalog-choice')
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
                                      worker_defaults=False, input='1\n1\n5\n1\n5\n2\nnot-listed\n')
                self.assertNotEqual(result.returncode, 0)
                expected = 'catalog' if case != 'invalid' else 'model: select a number'
                self.assertIn(expected, result.stderr)
                self.assertNotIn('TOP_SECRET', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/setup-complete.json').exists())

    def test_worker_setup_finishes_without_skill_questions_and_shows_each_role_folder(self):
        # Arrange: model catalogs exist, but no user skill files have been supplied.
        from worker_support import worker_settings
        repo = self.repo()
        worker_settings(self)
        (self.workspace / 'tdd/SKILL.md').unlink()
        (self.workspace / 'standards/SKILL.md').unlink()
        # Act: the last answer selects review effort; setup must not read further input.
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, worker_defaults=False,
                              input='1\n1\n5\n1\n5\n2\n1\n6\n3\n1\n3\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertTrue(config.execution_enabled)
        self.assertEqual(self.agent(repo, 'implementation')['resources']['skills'], ['./skills'])
        self.assertEqual(self.agent(repo, 'implementation')['resources']['skills'], ['./skills'])
        self.assertEqual(self.agent(repo, 'review')['resources']['skills'], ['./skills'])
        self.assertNotIn('Local TDD skill file:', result.stdout)
        self.assertNotIn('architecture/standards skill (', result.stdout)
        self.assertNotIn('tdd_skill', (repo / '.factory/factory.toml').read_text())
        agents = repo / '.factory/agents'
        for role in ('foreman', 'feature-owner', 'research', 'implementation', 'review'):
            with self.subTest(role=role):
                folder = agents / role / 'skills'
                self.assertTrue(folder.is_dir())
                self.assertIn(str(folder), result.stdout)
        for role in ('implementation', 'review'):
            selected = self.agent(repo, role)['resources']['skills']
            self.assertEqual(selected, ['./skills'])
        self.assertIn('<skill-name>/SKILL.md', result.stdout)
        self.assertIn('Agent settings live in agent.json', result.stdout)
        self.assertIn('reload or restart affected agents', result.stdout)
        self.assertTrue((repo / '.factory/setup-complete.json').is_file())
