"""Run the Ticketing contract against the non-GitHub fake and the GitHub adapter."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from contracts.ticketing import FakeTicketing, TicketingContract

from forgetful_factory.ticketing.adapters.github import GitHubTicketing
from forgetful_factory.ticketing.model import TicketSource

# A stateful gh: serves the GitHub API paths the adapter reads, from a JSON state file.
GH = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
state_path = Path(os.environ['GH_STATE'])
state = json.loads(state_path.read_text())
arguments = sys.argv[1:]
if arguments == ['api', '--help']:
    print('FLAGS\n      --paginate   Make additional requests\n      --slurp      Combine pages')
    sys.exit(0)
endpoint = arguments[1]
repository = 'repos/' + state['repository']
if endpoint == repository:
    print(json.dumps({'full_name': state['repository']}))
elif endpoint == repository + '/labels?per_page=100':
    print(json.dumps([[{'name': name} for name in state['labels']]]))
elif endpoint == repository + '/labels' and '--method' in arguments:
    name = next(value.removeprefix('name=') for value in arguments if value.startswith('name='))
    state['labels'].append(name)
    state_path.write_text(json.dumps(state))
    print(json.dumps({'name': name}))
elif endpoint == repository + '/issues?state=open&per_page=100':
    print(json.dumps([[issue for issue in state['issues'] if issue['state'] == 'open']]))
elif endpoint.startswith(repository + '/issues/') and endpoint.endswith('/comments?per_page=100'):
    print(json.dumps([[]]))
else:
    sys.exit('unexpected gh call: ' + ' '.join(arguments))
'''


class FakeTicketingContractTests(TicketingContract, unittest.TestCase):
    source = TicketSource('tracker', 'Platform')
    invalid_references = ('', 'team/app', 'two words')
    keys = ('ENG-1', 'ENG-22', 'OPS-333')
    non_keys = ('42', 'eng-1', 'ENG-0', 'ENG-01', 'ENG 1')

    def setUp(self):
        self.fake = FakeTicketing()

    def adapter(self):
        return self.fake

    def publish(self, tickets):
        self.fake.tickets[self.source.reference.casefold()] = tickets


class GitHubTicketingContractTests(TicketingContract, unittest.TestCase):
    source = TicketSource('github', 'team/app')
    invalid_references = ('team', 'team/app.git', 'team/..', 'team/app/x')
    keys = ('1', '22', '333')
    non_keys = ('0', '01', '-1', 'ENG-1')

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / 'gh').write_text(GH)
        (root / 'gh').chmod(0o755)
        self.state = root / 'state.json'
        self.state.write_text(json.dumps({'repository': 'team/app', 'labels': [], 'issues': []}))
        environment = patch.dict(os.environ, {'PATH': f'{root}{os.pathsep}{os.environ["PATH"]}',
                                              'GH_STATE': str(self.state)})
        environment.start()
        self.addCleanup(environment.stop)

    def adapter(self):
        return GitHubTicketing()

    def publish(self, tickets):
        state = json.loads(self.state.read_text())
        state['issues'] = [
            {'number': int(ticket['key']), 'title': ticket['title'], 'body': ticket['body'],
             'html_url': f'https://github.com/team/app/issues/{ticket["key"]}',
             'state': ticket['state'], 'labels': [{'name': name} for name in ticket['labels']]}
            for ticket in tickets]
        self.state.write_text(json.dumps(state))
