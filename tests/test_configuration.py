from pathlib import Path
import tempfile
import unittest

from forgetful_factory.configuration import load_configuration
from forgetful_factory.domain.models import FactoryError


VALID = '''watcher_label = ["factory"]
foreman_agent_model = "provider/model"
foreman_agent_effort = "high"
[[repository]]
local_dir = "/existing/repo"
remote = "git@github.com:team/app.git"
provider = "github"
source = "team/app"
'''


class ConfigurationTests(unittest.TestCase):
    def test_loader_reads_repeated_repository_tables_in_order(self):
        # Arrange
        contents = VALID + '''
[[repository]]
local_dir = "/existing/web"
remote = "https://github.com/team/web.git"
provider = "github"
source = "team/web"
'''
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            config = workspace / '.factory' / 'factory.toml'
            config.parent.mkdir()
            config.write_text(contents)
            # Act
            loaded = load_configuration(workspace)
            # Assert
            self.assertEqual([item.local_dir for item in loaded.repository],
                             ['/existing/repo', '/existing/web'])
            self.assertEqual([item.remote for item in loaded.repository],
                             ['git@github.com:team/app.git', 'https://github.com/team/web.git'])
            self.assertEqual([item.work_source.reference for item in loaded.repository],
                             ['team/app', 'team/web'])

    def test_loader_rejects_nul_characters_before_settings_reach_external_tools(self):
        # Arrange
        cases = [
            ('watcher_label = ["factory"]', r'watcher_label = ["bad\u0000label"]'),
            ('foreman_agent_model = "provider/model"',
             r'foreman_agent_model = "provider/\u0000model"'),
            ('foreman_agent_effort = "high"', r'foreman_agent_effort = "high\u0000"'),
            ('local_dir = "/existing/repo"', r'local_dir = "/existing/\u0000repo"'),
            ('remote = "git@github.com:team/app.git"',
             r'remote = "git@github.com:team/\u0000app.git"'),
            ('provider = "github"', r'provider = "git\u0000hub"'),
            ('source = "team/app"', r'source = "team/\u0000app"'),
        ]
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            config = workspace / '.factory' / 'factory.toml'
            config.parent.mkdir()
            for before, after in cases:
                with self.subTest(setting=before):
                    config.write_text(VALID.replace(before, after))
                    # Act / Assert
                    with self.assertRaisesRegex(FactoryError, 'NUL'):
                        load_configuration(workspace)

    def test_loader_rejects_invalid_types_missing_fields_and_malformed_toml(self):
        # Arrange
        cases = [
            ('watcher_label = ["factory"]', 'watcher_label = "factory"'),
            ('watcher_label = ["factory"]', 'watcher_label = []'),
            ('watcher_label = ["factory"]', 'watcher_label = [false]'),
            ('foreman_agent_model = "provider/model"', 'foreman_agent_model = 2'),
            ('foreman_agent_effort = "high"', 'foreman_agent_effort = ["high"]'),
            ('foreman_agent_effort = "high"', 'foreman_agent_effort = "  "'),
            ('foreman_agent_effort = "high"', ''),
            ('local_dir = "/existing/repo"', 'local_dir = 3'),
            ('remote = "git@github.com:team/app.git"', 'remote = true'),
            ('provider = "github"', 'provider = ""'),
            ('source = "team/app"', 'source = ["team/app"]'),
            (VALID, 'repository = []'),
            (VALID, 'repository = "team/app"'),
            (VALID, 'repository = [42]'),
            ('[[repository]]', '[repository]'),
            ('[[repository]]', '[other]'),
            (VALID, VALID + '\n[[repository]]\nlocal_dir = "/existing/web"\n'),
            (VALID, '['),
        ]
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            config = workspace / '.factory' / 'factory.toml'
            config.parent.mkdir()
            for before, after in cases:
                with self.subTest(after=after):
                    config.write_text(VALID.replace(before, after))
                    # Act / Assert
                    with self.assertRaises(FactoryError):
                        load_configuration(workspace)
