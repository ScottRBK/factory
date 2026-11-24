"""Init keeps the ticket source it derives from an unusual origin, as before the ticketing port."""
import tomllib

from test_init import INIT_SETTINGS, InitFixture


class InitSourceTests(InitFixture):
    def test_origin_with_a_doubled_git_suffix_sets_up_as_before(self):
        # Arrange: the remote parser removes one ".git", so the source keeps the other.
        repo = self.repo(remote='git@github.com:team/app.git.git')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert: init checked the origin against the source it derived, and saved setup.
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = tomllib.loads((repo / '.factory/factory.toml').read_text())
        self.assertEqual(saved['repository'][0]['source'], 'team/app.git')
