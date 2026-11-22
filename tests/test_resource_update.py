"""Bundled role-resource updates through the public CLI and the real installed bundle."""
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

import test_watch
from lifecycle_support import LifecycleFixture
from profile_support import events
from test_init import INIT_SETTINGS, ROOT, InitFixture

BUNDLE = ROOT / 'src/forgetful_factory/resources/role-resources.zip'
CHANGED = 'pi-forgetful/src/bootstrap/factory.ts'
# The exact bytes that the previous release (manifest at 688c926) shipped for CHANGED.
PREVIOUS = Path(__file__).parent / 'fixtures/previous-pi-forgetful-factory.ts'
MISSING = 'pi-forgetful/src/queue.ts'
EDITED = 'agentshell/config.ts'


def bundled(member: str) -> bytes:
    with zipfile.ZipFile(BUNDLE) as archive:
        return archive.read(member)


def snapshot(directory: Path) -> dict[str, bytes]:
    return {str(path.relative_to(directory)): path.read_bytes()
            for path in sorted(directory.rglob('*')) if path.is_file()}


def run_update(fixture, repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, '-m', 'forgetful_factory', 'update',
                           '--workspace', str(repo), *args], cwd=repo, env=fixture.env,
                          capture_output=True, text=True, timeout=20)


class ResourceUpdateTests(InitFixture):
    def mixed_factory(self) -> Path:
        """A factory with one previous-release, one missing and one user-edited bundled file."""
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        resources = repo / '.factory/resources'
        (resources / CHANGED).write_bytes(PREVIOUS.read_bytes())
        (resources / MISSING).unlink()
        edited = resources / EDITED
        edited.write_bytes(edited.read_bytes() + b'\n// user edit to preserve\n')
        return repo

    def test_edited_file_blocks_the_whole_update_and_is_named(self):
        # Arrange
        repo = self.mixed_factory()
        before = snapshot(repo / '.factory')

        # Act
        result = run_update(self, repo, '--delegated-work-stopped')

        # Assert: no partial update; the missing and previous-release files are also untouched.
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(EDITED, result.stderr)
        self.assertIn('--force', result.stderr)
        self.assertEqual(snapshot(repo / '.factory'), before)

    def test_force_backs_up_edited_file_then_updates_every_file(self):
        # Arrange
        repo = self.mixed_factory()
        resources = repo / '.factory/resources'
        edit = (resources / EDITED).read_bytes()
        agents = snapshot(repo / '.factory/agents')

        # Act
        result = run_update(self, repo, '--delegated-work-stopped', '--force')

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        for member in (CHANGED, MISSING, EDITED):
            self.assertEqual((resources / member).read_bytes(), bundled(member))
        backup, = (repo / '.factory/resource-backups').glob(f'*/{EDITED}')
        self.assertEqual(backup.read_bytes(), edit)
        self.assertIn(str(backup.parents[1]), result.stdout)
        self.assertEqual(snapshot(repo / '.factory/agents'), agents)


    def test_dry_run_lists_each_planned_change_and_writes_nothing(self):
        # Arrange
        repo = self.mixed_factory()
        before = snapshot(repo / '.factory')

        # Act: no stop confirmation is needed to preview.
        preview = run_update(self, repo, '--dry-run')
        forced = run_update(self, repo, '--dry-run', '--force')

        # Assert: the plain preview reports that the edited file would block the update.
        self.assertEqual(preview.returncode, 1, preview.stderr)
        self.assertIn(EDITED, preview.stderr)
        self.assertEqual(forced.returncode, 0, forced.stderr)
        for result in (preview, forced):
            self.assertIn(f'replace  {CHANGED}', result.stdout)
            self.assertIn(f'add      {MISSING}', result.stdout)
            self.assertIn(f'edited   {EDITED}', result.stdout)
            self.assertIn('Dry run: nothing was changed.', result.stdout)
        self.assertEqual(snapshot(repo / '.factory'), before)

    def test_update_requires_confirmation_that_delegated_work_stopped(self):
        # Arrange
        repo = self.mixed_factory()
        before = snapshot(repo / '.factory')

        # Act
        result = run_update(self, repo, '--force')

        # Assert
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('--delegated-work-stopped', result.stderr)
        self.assertEqual(snapshot(repo / '.factory'), before)

    def test_runtime_that_no_longer_matches_its_lock_needs_install_consent(self):
        # Arrange: the installed runtime records an earlier lock, as after a lock change.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        resources = repo / '.factory/resources'
        (resources / CHANGED).write_bytes(PREVIOUS.read_bytes())
        (resources / 'agentshell/python/.venv/.factory-sync').write_text('earlier lock')
        log = self.workspace / 'install.jsonl'
        self.env['PROFILE_INSTALL_LOG'] = str(log)

        # Act
        declined = run_update(self, repo, '--delegated-work-stopped')
        consented = run_update(self, repo, '--delegated-work-stopped', '--install-role-runtime')

        # Assert: files update without consent; only the consented run syncs the locked runtime.
        self.assertEqual(declined.returncode, 1, declined.stderr)
        self.assertIn('--install-role-runtime', declined.stderr)
        self.assertEqual((resources / CHANGED).read_bytes(), bundled(CHANGED))
        self.assertEqual(consented.returncode, 0, consented.stderr)
        syncs = [event for event in events(log) if event['args'][:1] == ['sync']]
        self.assertEqual(len(syncs), 1)
        self.assertIn('--locked', syncs[0]['args'])


class ResourceUpdateWatchTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_watch.WatchCliTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_update_is_refused_while_watch_runs(self):
        # Arrange
        fixture = self.fixture
        watcher = fixture.start('--existing')
        fixture.wait_until(watcher, lambda: any(e['kind'] == 'ready' for e in fixture.events()))
        resources = fixture.workspace / '.factory/resources'
        (resources / CHANGED).write_bytes(PREVIOUS.read_bytes())
        before = snapshot(resources)

        # Act
        result = run_update(fixture, fixture.workspace, '--delegated-work-stopped')

        # Assert
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('already running', result.stderr)
        self.assertEqual(snapshot(resources), before)
        self.assertIsNone(watcher.poll())
        fixture.stop(watcher)


class ResourceUpdateLifecycleTests(LifecycleFixture):
    def test_previous_release_factory_updates_and_foreman_starts(self):
        # Arrange: a completed factory whose memory extension has previous-release bytes.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        stale = repo / '.factory/resources' / CHANGED
        stale.write_bytes(PREVIOUS.read_bytes())
        refused = self.foreman(repo)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn('Stale or edited role resource', refused.stderr)
        self.assertIn('update --dry-run', refused.stderr)
        agents = repo / '.factory/agents'
        before = snapshot(agents)

        # Act
        updated = run_update(self, repo, '--delegated-work-stopped')
        started = self.foreman(repo)

        # Assert
        self.assertEqual(updated.returncode, 0, updated.stderr)
        self.assertIn(f'replace  {CHANGED}', updated.stdout)
        self.assertEqual(stale.read_bytes(), bundled(CHANGED))
        self.assertEqual(snapshot(agents), before)
        self.assertEqual(started.returncode, 0, started.stderr)
        self.send_and_wait_for_exit(repo, self.status(repo)['target'])

    def test_update_is_refused_while_foreman_runs(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        started = self.foreman(repo)
        self.assertEqual(started.returncode, 0, started.stderr)
        (repo / '.factory/resources' / CHANGED).write_bytes(PREVIOUS.read_bytes())
        before = snapshot(repo / '.factory/resources')

        # Act
        result = run_update(self, repo, '--delegated-work-stopped')

        # Assert
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('Foreman is running', result.stderr)
        self.assertEqual(snapshot(repo / '.factory/resources'), before)
        self.send_and_wait_for_exit(repo, self.status(repo)['target'])
