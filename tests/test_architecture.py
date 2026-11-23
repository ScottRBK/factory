"""Exercise the real Import Linter CLI against disposable packages and repository rules."""

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'forgetful_factory'
SOURCE = ROOT / 'src' / PACKAGE
LINTER = Path(sys.executable).with_name('lint-imports')
RULES = {rule['id']: rule for rule in
         tomllib.loads((ROOT / 'pyproject.toml').read_text())['tool']['importlinter']['contracts']}

# Modules of the disposable package. boundary_probe sits outside every area; indirect rows
# route through it.
MODULES = (
    '__main__',
    'shared.errors',
    'deadlines',
    'domain.models',
    'application.ports.tracking',
    'application.workflow',
    'adapters.shared',
    'adapters.provider',
    'cli.bootstrap',
    'configuration',
    'ticketing.model',
    'boundary_probe.bridge',
)

# Allowed imports (importer, imported). Together they are the known-good fixture: ports, shared
# adapter code and both composition entry points. With every rule on, it must pass.
ALLOWED = (
    ('__main__', 'cli.bootstrap'),
    ('deadlines', 'shared.errors'),
    ('domain.models', 'shared.errors'),
    ('application.ports.tracking', 'domain.models'),
    ('application.workflow', 'shared.errors'),
    ('application.workflow', 'application.ports.tracking'),
    ('adapters.provider', 'application.ports.tracking'),
    ('adapters.provider', 'adapters.shared'),
    ('cli.bootstrap', 'adapters.provider'),
    ('adapters.provider', 'shared.errors'),
    ('cli.bootstrap', 'application.workflow'),
    ('cli.bootstrap', 'shared.errors'),
    ('configuration', 'adapters.provider'),
    ('configuration', 'shared.errors'),
)

# Rejected imports (rule id, importing area, imported module). Each row runs direct and
# indirect. The rule must be the one that rejects it.
REJECTED = (
    ('domain-independent', 'domain', 'application.workflow'),
    ('domain-independent', 'domain', 'adapters.provider'),
    ('domain-independent', 'domain', 'cli.bootstrap'),
    ('domain-independent', 'domain', 'configuration'),
    ('application-contracts', 'application', 'adapters.provider'),
    ('application-contracts', 'application', 'cli.bootstrap'),
    ('application-contracts', 'application', 'configuration'),
    ('adapters-no-cli', 'adapters', 'cli.bootstrap'),
    ('shared-independent', 'shared', '__main__'),
    ('shared-independent', 'shared', 'deadlines'),
    ('shared-independent', 'shared', 'domain.models'),
    ('shared-independent', 'shared', 'application.workflow'),
    ('shared-independent', 'shared', 'adapters.provider'),
    ('shared-independent', 'shared', 'cli.bootstrap'),
    ('shared-independent', 'shared', 'configuration'),
    ('shared-independent', 'shared', 'ticketing.model'),
)


def source(module: str) -> Path:
    """Return the file of a fixture module, relative to the package."""
    return Path(*module.split('.')).with_suffix('.py')


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(LINTER.is_file(),
                        "Missing lint-imports; run uv sync --locked, then "
                        "uv run --locked python -m unittest discover -s tests -v.")

    def fixture(self, workspace):
        package = workspace / 'src' / PACKAGE
        for module in MODULES:
            path = package / source(module)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(''.join(f'import {PACKAGE}.{imported}\n'
                                    for importer, imported in ALLOWED if importer == module))
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

    def assert_passes(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected(self, rule_id):
        rows = [(area, target) for rule, area, target in REJECTED if rule == rule_id]
        self.assertTrue(rows, f'Rule {rule_id} has no rows in REJECTED.')
        rule = RULES[rule_id]
        others = [other for other in RULES if other != rule_id]
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            package = workspace / 'src' / PACKAGE
            bridge = package / source('boundary_probe.bridge')
            # Arrange: the actual rules accept the clean fixture.
            self.assert_passes(self.check(workspace))
            for (area, target), indirect in [(row, way) for row in rows for way in (False, True)]:
                with self.subTest(area=area, target=target, indirect=indirect):
                    probe = package / area / 'probe.py'
                    target_module = f'{PACKAGE}.{target}'
                    if indirect:
                        bridge.write_text(f'import {target_module}\n')
                        probe.write_text(f'import {PACKAGE}.boundary_probe.bridge\n')
                    else:
                        probe.write_text(f'import {target_module}\n')
                    # Step 1: with the target rule off, the violation passes.
                    self.assert_passes(self.check(workspace, contracts=others))
                    # Step 2: with the target rule on, it fails with that rule and full path.
                    result = self.check(workspace)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    output = ' '.join(result.stdout.split())
                    forbidden = [module for module in rule['forbidden_modules']
                                 if f'{target_module}.'.startswith(f'{module}.')]
                    self.assertEqual(len(forbidden), 1, f'{rule_id} must forbid {target_module}.')
                    forbidden = forbidden[0]
                    self.assertIn(f'{rule["name"]} BROKEN', output)
                    self.assertIn(f'{PACKAGE}.{area} is not allowed to import {forbidden}:',
                                  output)
                    self.assertIn(f'{PACKAGE}.{area}.probe', output)
                    self.assertIn(target_module, output)
                    if indirect:
                        self.assertIn(f'{PACKAGE}.boundary_probe.bridge', output)
                    # Step 3: with the violation removed, the fixture passes again.
                    probe.unlink()
                    bridge.write_text('')
                    self.assert_passes(self.check(workspace))

    def test_allowed_imports_pass_every_rule(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            # Act
            result = self.check(workspace)
            # Assert
            self.assert_passes(result)

    def test_every_rejected_row_names_a_configured_rule(self):
        self.assertLessEqual({rule for rule, _, _ in REJECTED}, set(RULES))


def real_modules() -> set[str]:
    modules = set()
    for path in SOURCE.rglob('*.py'):
        parts = path.relative_to(SOURCE.parent).with_suffix('').parts
        modules.add('.'.join(parts[:-1] if parts[-1] == '__init__' else parts))
    return modules


def matches(name: str, module: str) -> bool:
    """Match an Import Linter name: '*' is one segment, '**' is one or more."""
    pattern = re.escape(name).replace(r'\*\*', r'[^.]+(\.[^.]+)*').replace(r'\*', r'[^.]+')
    return re.fullmatch(pattern, module) is not None


class CoverageTests(unittest.TestCase):
    """The checker sees every module, and the rules name every area they must."""

    def test_every_source_folder_is_a_package(self):
        # A folder without __init__.py hides its modules from the checker.
        folders = {path.parent for path in SOURCE.rglob('*.py')}
        missing = sorted(str(folder.relative_to(SOURCE)) for folder in folders
                         if not (folder / '__init__.py').is_file())
        self.assertEqual(missing, [])

    def test_rule_names_match_real_modules(self):
        # Import Linter silently skips a wildcard that matches nothing, which turns a rule off.
        modules = real_modules()
        for rule in RULES.values():
            self.assertEqual(rule['type'], 'forbidden',
                             f'Extend this check to cover {rule["type"]} rules.')
            for name in [*rule['source_modules'], *rule['forbidden_modules']]:
                if name.startswith(f'{PACKAGE}.'):
                    with self.subTest(rule=rule['id'], name=name):
                        self.assertTrue(any(matches(name, module) for module in modules))

    def test_shared_forbids_every_other_top_level_module(self):
        # Arrange: top-level modules and packages of the real source tree.
        top_level = {path.stem for path in SOURCE.glob('*.py')} | {
            path.parent.name for path in SOURCE.glob('*/__init__.py')}
        # Act
        forbidden = {module.removeprefix(f'{PACKAGE}.')
                     for module in RULES['shared-independent']['forbidden_modules']}
        # Assert
        self.assertEqual(forbidden, top_level - {'__init__', 'shared'})

    def test_package_folders_find_files_in_one_place(self):
        # Arrange: a file found relative to source breaks silently when a module moves.
        allowed = {Path('shared/resources.py'), Path('adapters/agentshell/launch.py')}
        # Act
        users = {path.relative_to(SOURCE) for path in SOURCE.rglob('*.py')
                 if '__file__' in path.read_text()}
        # Assert
        self.assertEqual(users, allowed)

    def test_resource_root_holds_the_bundle(self):
        from forgetful_factory.shared.resources import resource_root

        self.assertTrue((resource_root() / 'role-resources.json').is_file())
        self.assertTrue((resource_root() / 'install-locks.zip').is_file())
        self.assertTrue((resource_root() / 'foreman' / 'AGENTS.md').is_file())

    def test_launch_targets_exist(self):
        # Arrange: these are started by file path or module name, which imports cannot see.
        from forgetful_factory.adapters.agentshell import launch

        # Assert
        self.assertTrue(launch.CONTROLLER.is_file())
        self.assertTrue(launch.MODEL_CATALOG.is_file())
        owner = importlib.util.find_spec(launch.OWNER_MODULE)
        self.assertIsNotNone(owner)
        self.assertTrue(Path(owner.origin).is_relative_to(SOURCE))


def _rejection_test(rule_id):
    def test(self):
        self.assert_rejected(rule_id)
    test.__doc__ = f'Rule {rule_id} rejects every row in REJECTED, direct and indirect.'
    return test


# One test per configured rule, so a new rule fails until it has REJECTED rows.
for _rule_id in RULES:
    setattr(ArchitectureTests, f'test_{_rule_id.replace("-", "_")}_rejects_violations',
            _rejection_test(_rule_id))
