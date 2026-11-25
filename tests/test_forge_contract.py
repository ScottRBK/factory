"""Run the Forge contract against the non-GitHub fake and the GitHub adapter."""
import unittest

from contracts.forge import FakeForge, ForgeContract

from forgetful_factory.forge.adapters.github import GitHubForge


class FakeForgeContractTests(ForgeContract, unittest.TestCase):
    remotes = ('git@forge.example:team/app.git', 'https://forge.example/Team/App')
    reference = 'team/app'
    invalid_remotes = ('git@github.com:team/app.git', 'https://forge.example/team', '')

    def adapter(self):
        return FakeForge()

    def change_request(self, reference, number):
        return f'https://forge.example/{reference}/changes/{number}'


class GitHubForgeContractTests(ForgeContract, unittest.TestCase):
    remotes = ('git@github.com:team/app.git', 'https://github.com/Team/App.git',
               'https://github.com/team/app')
    reference = 'team/app'
    invalid_remotes = ('git@gitlab.com:team/app.git', 'https://github.com/team',
                       'https://github.com/team/..', 'ssh://github.com/team/app', '')

    def adapter(self):
        return GitHubForge()

    def change_request(self, reference, number):
        return f'https://github.com/{reference}/pull/{number}'
