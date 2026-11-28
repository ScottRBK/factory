"""The secrets file reader: one KEY=value file, read by name, never copied into os.environ."""
import os
import tempfile
import unittest
from pathlib import Path

from forgetful_factory.shared.env_file import find_secret, read_env_file


class EnvFileTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / '.env'

    def test_reader_takes_plain_quoted_and_exported_values(self):
        # Arrange
        self.path.write_text('\n'.join((
            '# Factory secrets',
            '',
            'PLAIN=abc.def',
            '  SPACED = value with spaces  ',
            'DOUBLE="quoted # not a comment"',
            "SINGLE='single'",
            'export EXPORTED=yes',
            'UNMATCHED="left',
            'EMPTY=',
            'EQUALS=a=b',
            'not a setting',
            '1BAD=no',
            'NAMÉ=no',
        )))
        # Act
        values = read_env_file(self.path)
        # Assert
        self.assertEqual(values, {
            'PLAIN': 'abc.def', 'SPACED': 'value with spaces',
            'DOUBLE': 'quoted # not a comment', 'SINGLE': 'single', 'EXPORTED': 'yes',
            'UNMATCHED': '"left', 'EMPTY': '', 'EQUALS': 'a=b',
        })

    def test_reader_does_not_expand_variables(self):
        # Arrange
        self.path.write_text('TOKEN=$HOME/${USER}\n')
        # Act / Assert
        self.assertEqual(read_env_file(self.path), {'TOKEN': '$HOME/${USER}'})

    def test_environment_wins_over_the_file(self):
        # Arrange
        self.path.write_text('BOT_TOKEN=from-file\n')
        # Act
        value, warning = find_secret('BOT_TOKEN', self.path, explicit=True,
                                     environment={'BOT_TOKEN': 'from-environment'})
        # Assert
        self.assertEqual((value, warning), ('from-environment', None))

    def test_file_value_is_found_and_os_environ_is_unchanged(self):
        # Arrange
        self.path.write_text('FACTORY_TEST_SECRET=from-file\n')
        before = dict(os.environ)
        # Act
        value, warning = find_secret('FACTORY_TEST_SECRET', self.path, explicit=False,
                                     environment={})
        # Assert
        self.assertEqual((value, warning), ('from-file', None))
        self.assertEqual(dict(os.environ), before)

    def test_missing_value_names_the_variable_and_both_places(self):
        # Arrange
        self.path.write_text('OTHER=value\nBOT_TOKEN=\n')
        # Act
        value, warning = find_secret('BOT_TOKEN', self.path, explicit=False, environment={})
        # Assert
        self.assertIsNone(value)
        self.assertIn('BOT_TOKEN', warning)
        self.assertIn('environment', warning)
        self.assertIn(str(self.path), warning)

    def test_a_set_file_that_is_missing_is_named(self):
        # Act
        value, warning = find_secret('BOT_TOKEN', self.path, explicit=True, environment={})
        # Assert
        self.assertIsNone(value)
        self.assertIn(f'env_file {self.path} does not exist', warning)
        self.assertIn('BOT_TOKEN', warning)

    def test_a_missing_default_file_is_only_one_of_the_places_checked(self):
        # Act
        value, warning = find_secret('BOT_TOKEN', self.path, explicit=False, environment={})
        # Assert
        self.assertIsNone(value)
        self.assertNotIn('does not exist', warning)
        self.assertIn(str(self.path), warning)

    def test_an_unreadable_file_gives_a_warning_not_an_error(self):
        # Arrange: a folder in place of the file cannot be read.
        self.path.mkdir()
        # Act
        value, warning = find_secret('BOT_TOKEN', self.path, explicit=True, environment={})
        # Assert
        self.assertIsNone(value)
        self.assertIn(f'Cannot read env_file {self.path}', warning)


if __name__ == '__main__':
    unittest.main()
