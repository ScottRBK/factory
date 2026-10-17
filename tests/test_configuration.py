import tempfile
import unittest
from pathlib import Path

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


class ForgetfulConfigurationTests(unittest.TestCase):
    def load(self, section):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / '.factory').mkdir()
            (workspace / '.factory/factory.toml').write_text(VALID + '\n' + section)
            return load_configuration(workspace)

    def test_shared_local_connection_defaults_to_cli_and_has_stable_database(self):
        # Arrange
        section = '''[forgetful]
instance = "local"
executable = "forgetful"
database = "/factory/data/shared.db"
'''
        # Act
        config = self.load(section)
        # Assert
        self.assertEqual(config.forgetful.method, 'cli')
        self.assertEqual(config.forgetful.instance, 'local')
        self.assertEqual(config.forgetful.database, '/factory/data/shared.db')

    def test_remote_cli_connection_roundtrips_without_credentials(self):
        # Arrange
        section = '''[forgetful]
method = "cli"
instance = "server"
server = "https://memory.example/mcp"
executable = "/tools/forgetful"
'''
        # Act
        config = self.load(section)
        # Assert
        self.assertEqual(config.forgetful.method, 'cli')
        self.assertEqual(config.forgetful.server, 'https://memory.example/mcp')
        self.assertEqual(config.forgetful.executable, '/tools/forgetful')

    def test_invalid_or_secret_connection_settings_are_rejected_without_echoing_values(self):
        # Arrange
        sections = [
            'method = "other"\ninstance = "local"\ndatabase = "/data/a.db"',
            'instance = "other"',
            'instance = "local"\ndatabase = "relative.db"',
            'instance = "local"\ndatabase = ":memory:"',
            'instance = "local"\ndatabase = "/data/a.db"\nserver = "https://host/mcp"',
            'instance = "server"\nserver = "file:///tmp/server"',
            'instance = "server"\nserver = "https://user:TOP_SECRET@host/mcp"',
            'instance = "server"\nserver = "https://host/mcp?token=TOP_SECRET"',
            'instance = "server"\nserver = "https://host/mcp"\ntoken = "TOP_SECRET"',
        ]
        for section in sections:
            with self.subTest(section=section):
                # Act / Assert
                with self.assertRaises(FactoryError) as raised:
                    self.load('[forgetful]\n' + section)
                self.assertNotIn('TOP_SECRET', str(raised.exception))

    def test_http_is_allowed_only_for_loopback_without_echoing_server_details(self):
        # Arrange
        for host in ('memory.example', '192.168.1.10', '0.0.0.0', '[2001:db8::1]'):
            with self.subTest(host=host):
                section = ('[forgetful]\ninstance = "server"\n'
                           f'server = "http://{host}/TOP_SECRET"\n')
                # Act / Assert
                with self.assertRaises(FactoryError) as raised:
                    self.load(section)
                self.assertNotIn('TOP_SECRET', str(raised.exception))
                self.assertIn('HTTPS', str(raised.exception))
        for host in ('localhost', 'LOCALHOST', '127.0.0.1', '127.0.0.2', '[::1]'):
            with self.subTest(host=host):
                # Act / Assert
                self.assertEqual(self.load('[forgetful]\ninstance = "server"\n'
                                           f'server = "http://{host}:8020/mcp"').forgetful.server,
                                 f'http://{host}:8020/mcp')

    def test_cli_requires_linux_and_mcp_is_rejected_on_all_platforms(self):
        # Arrange
        from unittest.mock import patch
        section = '[forgetful]\ninstance = "server"\nserver = "https://memory.example/mcp"\n'
        for platform in ('darwin', 'win32'):
            with self.subTest(platform=platform), patch('sys.platform', platform):
                # Act / Assert: fail at configuration boundary before any auth command.
                with self.assertRaisesRegex(FactoryError, 'Linux/WSL'):
                    self.load(section + 'method = "cli"\n')
                with self.assertRaisesRegex(FactoryError, 'MCP.*unsupported'):
                    self.load(section + 'method = "mcp"\n')

    def test_mcp_configuration_requires_explicit_cli_choice_without_conversion(self):
        # Arrange
        section = '[forgetful]\nmethod = "mcp"\ninstance = "local"\ndatabase = "/data/a.db"'
        # Act / Assert
        with self.assertRaisesRegex(FactoryError, 'method = "cli"'):
            self.load(section)
