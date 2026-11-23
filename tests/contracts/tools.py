"""Promises every ToolInstaller keeps.

A new installer is done when a subclass of ToolInstallerContract passes for it.
"""
from forgetful_factory.shared.errors import FactoryError


class ToolInstallerContract:
    """Mix into unittest.TestCase. The subclass supplies the installer and arranges its host."""

    missing_on_bare_host: tuple[str, ...]   # absent and unready names when nothing is installed

    def installer(self):
        raise NotImplementedError

    def arrange_installed(self) -> None:
        """Make the tool present and usable, as a finished installation leaves it."""
        raise NotImplementedError

    def test_a_bare_host_misses_the_tool(self):
        tool = self.installer()
        self.assertEqual([*tool.absent(), *tool.unready()], list(self.missing_on_bare_host))

    def test_an_installed_tool_is_not_missing(self):
        self.arrange_installed()
        tool = self.installer()
        self.assertEqual((tool.absent(), tool.unready()), ([], []))

    def test_other_tools_are_neither_described_nor_installed(self):
        tool = self.installer()
        self.assertIsNone(tool.describe('no-such-tool'))
        with self.assertRaises(FactoryError):
            tool.install('no-such-tool')
