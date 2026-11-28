import tempfile
import unittest
from pathlib import Path

from forgetful_factory.configuration import load_configuration
from forgetful_factory.shared.errors import FactoryError

VALID = '''watcher_label = ["factory"]
foreman_agent_file = "agents/foreman/agent.json"
execution_enabled = false
[[repository]]
local_dir = "/existing/repo"
remote = "git@github.com:team/app.git"
provider = "github"
source = "team/app"
'''


class ConfigurationTests(unittest.TestCase):
    def test_factory_settings_reference_one_foreman_definition(self):
        # Arrange
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            factory = workspace / '.factory'
            factory.mkdir()
            (factory / 'factory.toml').write_text('''watcher_label = ["factory"]
foreman_agent_file = "agents/foreman/agent.json"
[[repository]]
local_dir = "/existing/repo"
remote = "git@github.com:team/app.git"
provider = "github"
source = "team/app"
''')
            # Act
            loaded = load_configuration(workspace)
            # Assert
            self.assertEqual(loaded.foreman_agent_file,
                             str(factory / 'agents/foreman/agent.json'))
            self.assertEqual(loaded.watcher_label, ('factory',))
            self.assertEqual(loaded.repository[0].work_source.reference, 'team/app')

    def test_duplicate_agent_choices_are_rejected_without_rewriting(self):
        # Arrange
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            path = workspace / '.factory/factory.toml'
            path.parent.mkdir()
            for field in ('foreman_agent_model', 'feature_owner_agent_model',
                          'implementation_agent_harness', 'review_agent_effort'):
                with self.subTest(field=field):
                    contents = f'{field} = "old-setting"\n' + VALID
                    path.write_text(contents)
                    # Act / Assert
                    with self.assertRaisesRegex(FactoryError, 'agent.json'):
                        load_configuration(workspace)
                    self.assertEqual(path.read_text(), contents)

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
            ('foreman_agent_file = "agents/foreman/agent.json"',
             r'foreman_agent_file = "agents/\u0000foreman/agent.json"'),
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
            ('foreman_agent_file = "agents/foreman/agent.json"', 'foreman_agent_file = 2'),
            ('foreman_agent_file = "agents/foreman/agent.json"', 'foreman_agent_file = "  "'),
            ('foreman_agent_file = "agents/foreman/agent.json"', ''),
            ('execution_enabled = false', 'execution_enabled = [false]'),
            ('execution_enabled = false', 'execution_enabled = "false"'),
            ('execution_enabled = false', 'execution_enabled = 1'),
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


CHANNEL = '123456789012345678'
USER = '234567890123456789'


class ChatSettingsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        (self.workspace / '.factory').mkdir()

    def load(self, top='', section=''):
        # Top-level keys must come before the first table in TOML.
        (self.workspace / '.factory/factory.toml').write_text(top + VALID + '\n' + section)
        return load_configuration(self.workspace)

    def test_existing_settings_load_without_chat(self):
        # Act
        config = self.load()
        # Assert
        self.assertIsNone(config.env_file)
        self.assertIsNone(config.discord)

    def test_discord_settings_load_with_the_default_token_variable(self):
        # Arrange
        section = f'[discord]\nchannel_id = "{CHANNEL}"\nallowed_users = ["{USER}"]\n'
        # Act
        config = self.load(section=section)
        # Assert
        self.assertEqual(config.discord.channel_id, CHANNEL)
        self.assertEqual(config.discord.allowed_users, (USER,))
        self.assertEqual(config.discord.token_variable, 'DISCORD_BOT_TOKEN')

    def test_named_token_variable_and_env_file_paths(self):
        # Arrange
        section = (f'[discord]\nchannel_id = "{CHANNEL}"\nallowed_users = ["{USER}"]\n'
                   'token_variable = "DARK_BUSINESS_DISCORD_TOKEN"\n')
        cases = {'~/.config/factory.env': str(Path.home() / '.config/factory.env'),
                 'secrets/factory.env': str(self.workspace / 'secrets/factory.env'),
                 '/etc/factory.env': '/etc/factory.env'}
        for written, expected in cases.items():
            with self.subTest(env_file=written):
                # Act
                config = self.load(f'env_file = "{written}"\n', section)
                # Assert
                self.assertEqual(config.env_file, expected)
                self.assertEqual(config.discord.token_variable, 'DARK_BUSINESS_DISCORD_TOKEN')

    def test_invalid_chat_settings_are_refused(self):
        # Arrange
        users = f'allowed_users = ["{USER}"]\n'
        channel = f'channel_id = "{CHANNEL}"\n'
        cases = {
            'not a table': ('discord = "yes"\n', ''),
            'channel as a number': ('', f'[discord]\nchannel_id = {CHANNEL}\n{users}'),
            'short channel': ('', f'[discord]\nchannel_id = "1234"\n{users}'),
            'channel with letters': ('', f'[discord]\nchannel_id = "12345678901234567a"\n{users}'),
            # Only ASCII digits and names: Python's \d and \w also take other scripts.
            'channel with other digits': ('', f'[discord]\nchannel_id = "{"١" * 18}"\n{users}'),
            'variable with other letters': ('', f'[discord]\n{channel}{users}'
                                                'token_variable = "TOKÉN"\n'),
            'missing channel': ('', f'[discord]\n{users}'),
            'empty users': ('', f'[discord]\n{channel}allowed_users = []\n'),
            'missing users': ('', f'[discord]\n{channel}'),
            'bad user': ('', f'[discord]\n{channel}allowed_users = ["someone"]\n'),
            'users not a list': ('', f'[discord]\n{channel}allowed_users = "{USER}"\n'),
            'bad variable': ('', f'[discord]\n{channel}{users}token_variable = "BAD-NAME"\n'),
            'unknown key': ('', f'[discord]\n{channel}{users}token = "secret-value"\n'),
            'blank env_file': ('env_file = " "\n', ''),
            'env_file not text': ('env_file = 3\n', ''),
        }
        for name, (top, section) in cases.items():
            with self.subTest(name):
                # Act / Assert
                with self.assertRaises(FactoryError) as caught:
                    self.load(top, section)
                self.assertNotIn('secret-value', str(caught.exception))

    def test_saved_chat_settings_load_again_unchanged(self):
        # Arrange
        from forgetful_factory.factory.adapters.toml_configuration import TomlConfigurationStore
        section = (f'[discord]\nchannel_id = "{CHANNEL}"\nallowed_users = ["{USER}"]\n'
                   'token_variable = "FACTORY_TOKEN"\n')
        config = self.load('env_file = "/secrets/factory.env"\n', section)
        (self.workspace / '.factory/factory.toml').unlink()
        # Act
        TomlConfigurationStore(self.workspace).save(config)
        # Assert
        self.assertEqual(load_configuration(self.workspace), config)
