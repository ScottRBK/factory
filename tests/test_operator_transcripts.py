"""Golden operator text for setup agreement, Foreman start and watch status.

Recorded from the code before slice 5b of docs/plans/domain-contexts.md moved this logic out of the
CLI. The move must reproduce every transcript exactly. To record a deliberate change, run with
UPDATE_TRANSCRIPTS=1 and review the fixture diff before committing.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_init import INIT_SETTINGS, InitFixture

FIXTURE = Path(__file__).parent / 'fixtures' / 'transcripts.json'
UPDATE = os.environ.get('UPDATE_TRANSCRIPTS') == '1'
RUN_ID = '0123456789abcdef0123456789abcdef'

# The agreement part of init output: from the cleanup warning to the agreement's last line.
AGREEMENT_START = 'Automatic cleanup deletes'
AGREEMENT_ENDS = ('Saved Definition of Done: ', 'Preserved Definition of Done: ',
                  'before finalizing setup or handing off work.')

# A local owner that answers one status request; the reply comes from argv as JSON.
OWNER = r'''
import json, os, socket, sys
path, reply = sys.argv[1], json.loads(sys.argv[2])
os.umask(0o077)
with socket.socket(socket.AF_UNIX) as listener:
    listener.bind(path)
    listener.listen()
    print('ready', flush=True)
    with listener.accept()[0] as connection:
        connection.recv(4096)
        connection.sendall((json.dumps(reply) + '\n').encode())
'''


def agreement(stdout: str) -> str:
    rest = stdout[stdout.index(AGREEMENT_START):]
    ends = [rest.index('\n', rest.index(marker)) + 1 for marker in AGREEMENT_ENDS
            if marker in rest]
    return rest[:min(ends)] if ends else rest


class TranscriptFixture:
    """Compare each recorded transcript with the stored fixture, or record it."""

    recorded: dict = {}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.recorded = {}

    @classmethod
    def tearDownClass(cls):
        if UPDATE and cls.recorded:
            saved = json.loads(FIXTURE.read_text()) if FIXTURE.is_file() else {}
            FIXTURE.write_text(json.dumps({**saved, **cls.recorded}, indent=2, sort_keys=True)
                               + '\n')
        super().tearDownClass()

    def assert_transcript(self, name: str, transcript: dict):
        if UPDATE:
            self.recorded[name] = transcript
            return
        self.assertEqual(transcript, json.loads(FIXTURE.read_text())[name])


class AgreementTranscriptTests(TranscriptFixture, InitFixture):
    def record(self, name: str, result):
        transcript = {
            'returncode': result.returncode,
            'agreement': agreement(result.stdout).replace(str(self.workspace), '<workspace>'),
            'stderr': result.stderr.replace(str(self.workspace), '<workspace>'),
        }
        if name == 'discuss':
            # Setup goes on to start a Foreman conversation; that outcome depends on the host.
            transcript = {'agreement': transcript['agreement']}
        self.assert_transcript(f'agreement/{name}', transcript)

    def test_first_setup_agreement_transcripts(self):
        for name, answers in (('merge', '1\ny\n'), ('deployment', '2\nstaging\nDelivery\ny\n'),
                              ('deployed_e2e', '3\nstaging\nDelivery\ny\n'),
                              ('discuss', '4\n'), ('invalid', '9\n'), ('declined', '1\nn\n'),
                              ('unnamed_deployment', '2\n\nDelivery\n')):
            with self.subTest(name=name):
                repo = self.repo(name)
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input=answers,
                                      agreement_input='')
                self.record(name, result)

    def test_existing_agreement_transcript(self):
        repo = self.repo()
        path = repo / '.factory/definition_of_done.md'
        path.parent.mkdir()
        path.write_text('# Programme delivery\n')
        self.record('preserved', self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                              agreement_input=''))

    def test_finalize_agreement_transcript(self):
        repo = self.repo()
        incomplete = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, agreement_input='')
        self.assertNotEqual(incomplete.returncode, 0)
        self.record('finalize', self.run_cli(repo, '--finalize', input='1\ny\n',
                                             agreement_input=''))

    def test_watch_status_after_complete_setup(self):
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'watch', '--status',
             '--workspace', str(repo)], env=self.env, capture_output=True, text=True, timeout=10)
        self.assert_transcript('status/complete_setup', {
            'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})


class LifecycleTranscriptTests(TranscriptFixture, unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name).resolve()
        self.runtime = self.workspace / '.factory/runtime/foreman'

    def cli(self, *args):
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', *args, '--workspace',
             str(self.workspace)], capture_output=True, text=True, timeout=20,
            stdin=subprocess.DEVNULL)
        # Raw text: the order of keys in printed JSON is visible output too.
        return {'returncode': result.returncode,
                'stdout': result.stdout.replace(str(self.workspace), '<workspace>'),
                'stderr': result.stderr.replace(str(self.workspace), '<workspace>')}

    def save_owner(self, foreman: str):
        self.runtime.mkdir(parents=True, mode=0o700)
        path = self.runtime / 'owner.json'
        path.write_text(json.dumps({'workspace': str(self.workspace), 'run_id': RUN_ID,
                                    'foreman': foreman, 'watcher': 'stopped', 'target': None,
                                    'owner_pid': 4242}))
        path.chmod(0o600)

    def save_plain_watch(self):
        directory = self.workspace / '.factory/runtime/watch'
        directory.mkdir(parents=True, mode=0o700)
        path = directory / 'status.json'
        path.write_text(json.dumps({'workspace': str(self.workspace), 'run_id': RUN_ID,
                                    'watcher_pid': 4242, 'process_started': 'boot:1',
                                    'foreman': 'ready', 'watcher': 'running',
                                    'phase': 'watching', 'evidence': 'session_ready'}))
        path.chmod(0o600)

    def answer_status(self, reply: dict):
        owner = subprocess.Popen([sys.executable, '-c', OWNER, str(self.runtime / 'control.sock'),
                                  json.dumps({'run_id': RUN_ID, **reply})],
                                 stdout=subprocess.PIPE, text=True)
        self.addCleanup(owner.stdout.close)
        self.addCleanup(owner.wait, 10)
        self.addCleanup(owner.kill)
        self.assertEqual(owner.stdout.readline(), 'ready\n')

    def test_watch_status_without_records(self):
        self.assert_transcript('status/none', self.cli('watch', '--status'))

    def test_watch_status_with_saved_owner_only(self):
        for foreman in ('ready', 'stopped'):
            with self.subTest(foreman=foreman):
                self.setUp()
                self.save_owner(foreman)
                self.assert_transcript(f'status/saved_owner_{foreman}',
                                       self.cli('watch', '--status'))

    def test_watch_status_with_saved_plain_watch_and_owner(self):
        self.save_plain_watch()
        self.save_owner('ready')
        self.assert_transcript('status/combined', self.cli('watch', '--status'))

    def test_watch_status_with_unreadable_owner_records(self):
        self.runtime.mkdir(parents=True, mode=0o700)
        (self.runtime / 'owner.json').write_text('{invalid')
        self.assert_transcript('status/invalid_owner', self.cli('watch', '--status'))

    def test_watch_status_with_live_owner(self):
        self.save_owner('ready')
        self.answer_status({'foreman': 'ready', 'watcher': 'stopped', 'target': {
            'socket_path': '/fixture', 'pane_id': '%1', 'server_pid': 1, 'server_started': 1,
            'pane_pid': 1}})
        self.assert_transcript('status/live_owner', self.cli('watch', '--status'))

    def test_foreman_refuses_an_existing_owner(self):
        self.save_owner('ready')
        self.assert_transcript('foreman/existing', self.cli('foreman'))

    def test_foreman_attach_without_an_owner(self):
        self.assert_transcript('foreman/attach_none', self.cli('foreman', '--attach'))

    def test_foreman_attach_to_an_owner_that_is_not_ready(self):
        for name, reply in (('warning', {'warning': 'Foreman exited.'}), ('plain', {})):
            with self.subTest(name=name):
                self.setUp()
                self.save_owner('stopped')
                self.answer_status({'foreman': 'stopped', 'watcher': 'stopped', 'target': None,
                                    **reply})
                self.assert_transcript(f'foreman/attach_not_ready_{name}',
                                       self.cli('foreman', '--attach'))
