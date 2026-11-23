"""Promises every SessionHost adapter keeps.

A new host adapter is done when a subclass of SessionHostContract passes for it.
"""
import io
import json
from contextlib import redirect_stdout
from unittest.mock import patch


class SessionHostContract:
    """Mix into unittest.TestCase. The subclass supplies the host and one launched target."""

    target: dict

    def host(self):
        raise NotImplementedError

    def test_spec_is_plain_data_with_a_kind(self):
        spec = self.host().spec()
        self.assertEqual(json.loads(json.dumps(spec)), spec)
        self.assertIsInstance(spec.get('kind'), str)

    def test_attach_text_names_the_session(self):
        self.assertIn('factory-foreman-0123456789ab',
                      self.host().how_to_attach('factory-foreman-0123456789ab'))

    def test_enter_without_a_terminal_only_prints_how_to_enter(self):
        with redirect_stdout(io.StringIO()) as output, patch('sys.stdin', io.StringIO()):
            self.host().enter(self.target)
        self.assertTrue(output.getvalue().strip())
