"""Promises every Forge adapter keeps, and a non-GitHub fake that keeps them.

A new forge adapter is done when a subclass of ForgeContract passes for it.
"""
import re

from forgetful_factory.forge.model import RepositoryRef
from forgetful_factory.shared.errors import FactoryError


class ForgeContract:
    """Mix into unittest.TestCase. The subclass supplies the adapter and forge data."""

    remotes: tuple[str, ...]            # remotes of one repository, in every accepted form
    reference: str                      # that repository's reference, lowercase
    invalid_remotes: tuple[str, ...]

    def adapter(self):
        raise NotImplementedError

    def change_request(self, reference: str, number: str) -> str:
        """The canonical change-request URL for a repository on this forge."""
        raise NotImplementedError

    def test_every_remote_form_names_the_same_repository(self):
        forge = self.adapter()
        for remote in self.remotes:
            with self.subTest(remote=remote):
                repository = forge.repository(remote)
                self.assertIsInstance(repository, RepositoryRef)
                self.assertEqual(repository.reference, self.reference)
                self.assertEqual(repository, forge.repository(self.remotes[0]))

    def test_unsupported_remotes_are_refused(self):
        forge = self.adapter()
        for remote in self.invalid_remotes:
            with self.subTest(remote=remote):
                with self.assertRaises(FactoryError):
                    forge.repository(remote)

    def test_change_requests_belong_to_their_repository(self):
        forge = self.adapter()
        repository = forge.repository(self.remotes[0])
        other = self.reference.split('/')[0] + '/other'
        accepted = (self.change_request(self.reference, '7'),
                    self.change_request(self.reference.upper(), '12'))
        refused = ('', self.change_request(other, '7'), self.change_request(self.reference, '0'),
                   self.change_request(self.reference, '07'),
                   self.change_request(self.reference, '7') + '/files',
                   'https://elsewhere.example/' + self.reference + '/pull/7')
        for url in accepted:
            with self.subTest(url=url):
                self.assertTrue(forge.is_change_request(repository, url))
        for url in refused:
            with self.subTest(url=url):
                self.assertFalse(forge.is_change_request(repository, url))


class FakeForge:
    """A non-GitHub forge: git@forge.example remotes and /changes/N review URLs."""

    def repository(self, remote: str) -> RepositoryRef:
        match = re.fullmatch(r'(?:git@forge\.example:|https://forge\.example/)'
                             r'([a-z0-9-]+/[a-z0-9-]+?)(?:\.git)?', remote, re.IGNORECASE)
        if match is None:
            raise FactoryError(f'Unsupported origin {remote!r}; use a forge.example URL.')
        return RepositoryRef('fake-forge', match.group(1).casefold())

    def is_change_request(self, repository: RepositoryRef, url: str) -> bool:
        pattern = rf'https://forge\.example/{re.escape(repository.reference)}/changes/[1-9][0-9]*'
        return re.fullmatch(pattern, url, re.IGNORECASE) is not None
