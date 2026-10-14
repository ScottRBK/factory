"""Exercise the real Import Linter CLI against disposable packages and repository rules."""

import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'forgetful_factory'
LINTER = Path(sys.executable).with_name('lint-imports')

# This known-good fixture includes ports, shared adapter code, and both composition entry points.
FILES = {
    'domain/models.py': '',
    'application/ports/tracking.py': 'import forgetful_factory.domain.models\n',
    'application/workflow.py': 'import forgetful_factory.application.ports.tracking\n',
    'adapters/shared.py': '',
    'adapters/provider.py': (
        'import forgetful_factory.application.ports.tracking\n'
        'import forgetful_factory.adapters.shared\n'
    ),
    'cli/bootstrap.py': (
        'import forgetful_factory.adapters.provider\n'
        'import forgetful_factory.application.workflow\n'
    ),
    'configuration.py': 'import forgetful_factory.adapters.provider\n',
    'boundary_probe/bridge.py': '',
}


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(LINTER.is_file(),
                        "Missing lint-imports; run uv sync --locked, then "
                        "uv run --locked python -m unittest discover -s tests -v.")

    def fixture(self, workspace):
        for relative, content in FILES.items():
            path = workspace / 'src' / PACKAGE / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            parent = path.parent
            while parent != workspace / 'src':
                (parent / '__init__.py').touch()
                parent = parent.parent
        (workspace / 'pyproject.toml').write_text((ROOT / 'pyproject.toml').read_text())

    def check(self, workspace, contracts=()):
        command = [str(LINTER), '--config', 'pyproject.toml', '--no-cache', '--no-logo']
        for contract in contracts:
            command.extend(['--contract', contract])
        return subprocess.run(
            command, cwd=workspace,
            env=dict(os.environ, PYTHONPATH=str(workspace / 'src'), COLUMNS='200'),
            text=True, capture_output=True, timeout=20,
        )

    def assert_forbidden(self, contract_id, name, area, target, indirect=False):
        # Arrange: the actual contracts accept a clean package with legitimate composition.
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            baseline = self.check(workspace)
            self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
            probe = workspace / 'src' / PACKAGE / area / 'probe.py'
            target_module = f'{PACKAGE}.{target}'
            if indirect:
                bridge = workspace / 'src' / PACKAGE / 'boundary_probe' / 'bridge.py'
                bridge.write_text(f'import {target_module}\n')
                probe.write_text(f'import {PACKAGE}.boundary_probe.bridge\n')
            else:
                probe.write_text(f'import {target_module}\n')
            configuration = tomllib.loads((workspace / 'pyproject.toml').read_text())
            rules = configuration['tool']['importlinter']
            others = [rule['id'] for rule in rules['contracts'] if rule['id'] != contract_id]
            unenforced = self.check(workspace, contracts=others)
            self.assertEqual(unenforced.returncode, 0, unenforced.stdout + unenforced.stderr)
            # Act: enable the target rule and run the same real checker.
            result = self.check(workspace)
            # Assert: rejection comes from the intended contract and complete dependency path.
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            output = ' '.join(result.stdout.split())
            forbidden = f'{PACKAGE}.{target.split(".")[0]}'
            self.assertIn(f'{name} BROKEN', output)
            self.assertIn(f'{PACKAGE}.{area} is not allowed to import {forbidden}:', output)
            self.assertIn(f'{PACKAGE}.{area}.probe', output)
            self.assertIn(target_module, output)
            if indirect:
                self.assertIn(f'{PACKAGE}.boundary_probe.bridge', output)
            probe.unlink()
            if indirect:
                bridge.write_text('')
            clean = self.check(workspace)
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

    def test_domain_rejects_direct_outer_dependencies(self):
        for target in ('application.workflow', 'adapters.provider', 'cli.bootstrap',
                       'configuration'):
            with self.subTest(target=target):
                self.assert_forbidden('domain-independent', 'Domain stays independent',
                                      'domain', target)

    def test_application_rejects_direct_concrete_dependencies(self):
        for target in ('adapters.provider', 'cli.bootstrap', 'configuration'):
            with self.subTest(target=target):
                self.assert_forbidden(
                    'application-contracts', 'Application uses contracts, not adapters',
                    'application', target,
                )

    def test_adapters_reject_direct_cli_dependencies(self):
        self.assert_forbidden('adapters-no-cli', 'Adapters cannot depend on the CLI',
                              'adapters', 'cli.bootstrap')

    def test_domain_rejects_indirect_outer_dependencies(self):
        for target in ('application.workflow', 'adapters.provider', 'cli.bootstrap',
                       'configuration'):
            with self.subTest(target=target):
                self.assert_forbidden('domain-independent', 'Domain stays independent',
                                      'domain', target, indirect=True)

    def test_application_rejects_indirect_concrete_dependencies(self):
        for target in ('adapters.provider', 'cli.bootstrap', 'configuration'):
            with self.subTest(target=target):
                self.assert_forbidden(
                    'application-contracts', 'Application uses contracts, not adapters',
                    'application', target, indirect=True,
                )

    def test_adapters_reject_indirect_cli_dependencies(self):
        self.assert_forbidden('adapters-no-cli', 'Adapters cannot depend on the CLI',
                              'adapters', 'cli.bootstrap', indirect=True)

    def test_ports_shared_utilities_and_composition_are_allowed(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            # Act
            result = self.check(workspace)
            # Assert
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
