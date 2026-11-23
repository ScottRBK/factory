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
# route through it. cli.prompts imports nothing, so a row that targets it breaks one rule only.
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
    'cli.prompts',
    'configuration',
    'ticketing.model',
    'ticketing.ports',
    'ticketing.adapters.github',
    'forge.model',
    'forge.ports',
    'forge.adapters.github',
    'planning.model',
    'planning.ports',
    'planning.adapters.forgetful.connection',
    'planning.adapters.forgetful.plan_store',
    'agents.model',
    'agents.ports',
    'agents.adapters.agentshell.controller',
    'workspace.ports',
    'workspace.adapters.git.worktrees',
    'boundary_probe.bridge',
)

# Allowed imports (importer, imported). Together they are the known-good fixture: ports, shared
# adapter code and both composition entry points. With every rule on, it must pass.
ALLOWED = (
    ('__main__', 'cli.prompts'),
    ('deadlines', 'shared.errors'),
    ('domain.models', 'shared.errors'),
    ('domain.models', 'ticketing.model'),
    ('application.ports.tracking', 'domain.models'),
    ('application.workflow', 'shared.errors'),
    ('application.workflow', 'application.ports.tracking'),
    ('application.workflow', 'ticketing.ports'),
    ('application.workflow', 'forge.ports'),
    ('adapters.provider', 'application.ports.tracking'),
    ('adapters.provider', 'adapters.shared'),
    ('adapters.provider', 'shared.errors'),
    ('adapters.provider', 'ticketing.model'),
    ('ticketing.ports', 'ticketing.model'),
    ('ticketing.adapters.github', 'ticketing.ports'),
    ('ticketing.adapters.github', 'shared.errors'),
    ('forge.ports', 'forge.model'),
    ('forge.adapters.github', 'forge.ports'),
    ('forge.adapters.github', 'shared.errors'),
    ('cli.bootstrap', 'forge.adapters.github'),
    ('planning.ports', 'planning.model'),
    ('planning.adapters.forgetful.plan_store', 'planning.ports'),
    ('planning.adapters.forgetful.plan_store', 'planning.adapters.forgetful.connection'),
    ('application.workflow', 'planning.ports'),
    ('cli.bootstrap', 'planning.adapters.forgetful.plan_store'),
    ('workspace.adapters.git.worktrees', 'workspace.ports'),
    ('workspace.adapters.git.worktrees', 'shared.errors'),
    ('application.workflow', 'workspace.ports'),
    ('cli.bootstrap', 'workspace.adapters.git.worktrees'),
    ('agents.ports', 'agents.model'),
    ('agents.adapters.agentshell.controller', 'agent_shell'),
    ('application.workflow', 'agents.ports'),
    ('cli.bootstrap', 'agents.adapters.agentshell.controller'),
    ('cli.bootstrap', 'adapters.provider'),
    ('cli.bootstrap', 'application.workflow'),
    ('cli.bootstrap', 'shared.errors'),
    ('cli.bootstrap', 'ticketing.adapters.github'),
    ('configuration', 'adapters.provider'),
    ('configuration', 'shared.errors'),
)

# Rejected imports (rule id, importing area, imported module[, other rules]). The area is a
# package (the probe is a new module in it) or a module (the probe line is added to it). Each row
# runs direct and indirect. Only its own rule may reject it, unless the row names the other rules
# that must also reject it; step 1 then turns those off too (the skill's isolation).
REJECTED = (
    ('domain-independent', 'domain', 'application.workflow'),
    ('domain-independent', 'domain', 'adapters.provider'),
    ('domain-independent', 'domain', 'cli.prompts'),
    ('domain-independent', 'domain', 'configuration'),
    ('application-contracts', 'application', 'adapters.provider'),
    ('application-contracts', 'application', 'cli.prompts'),
    ('application-contracts', 'application', 'configuration'),
    ('adapters-no-cli', 'adapters', 'cli.prompts'),
    ('shared-independent', 'shared', '__main__'),
    ('shared-independent', 'shared', 'deadlines'),
    ('shared-independent', 'shared', 'domain.models'),
    ('shared-independent', 'shared', 'application.workflow'),
    ('shared-independent', 'shared', 'adapters.provider'),
    ('shared-independent', 'shared', 'cli.prompts'),
    ('shared-independent', 'shared', 'configuration'),
    ('shared-independent', 'shared', 'ticketing.model'),
    ('shared-independent', 'shared', 'forge.model'),
    ('shared-independent', 'shared', 'planning.model'),
    ('shared-independent', 'shared', 'workspace.ports'),
    ('shared-independent', 'shared', 'agents.model'),
    ('inside-each-area', 'ticketing.model', 'ticketing.ports'),
    ('inside-each-area', 'forge.model', 'forge.ports'),
    ('inside-each-area', 'planning.model', 'planning.ports'),
    ('inside-each-area', 'agents.model', 'agents.ports'),
    ('adapters-from-composition', 'application', 'ticketing.adapters.github'),
    ('adapters-from-composition', 'application', 'forge.adapters.github'),
    ('adapters-from-composition', 'application', 'workspace.adapters.git.worktrees'),
    ('adapters-from-composition', 'application', 'agents.adapters.agentshell.controller'),
    ('adapters-from-composition', 'domain', 'ticketing.adapters.github'),
    # Every forge module is reachable from forge.adapters, so independence also rejects this.
    ('adapters-from-composition', 'forge.ports', 'ticketing.adapters.github',
     ('adapters-independent',)),
    ('adapters-independent', 'adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'forge.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'planning.adapters', 'forge.adapters.github'),
    ('adapters-independent', 'workspace.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'agents.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'adapters.shared', 'planning.adapters.forgetful.plan_store'),
    # Legacy adapters and configuration are left out: application and domain import the
    # ticketing port and model, so from any ticketing module those imports break a second rule.
    ('contexts-not-legacy', 'ticketing.adapters', 'cli.prompts'),
    ('contexts-not-legacy', 'ticketing.adapters', 'application.workflow'),
    ('contexts-not-legacy', 'ticketing.ports', 'domain.models'),
    ('contexts-not-legacy', 'ticketing.model', 'deadlines'),
    ('contexts-not-legacy', 'forge.adapters', 'cli.prompts'),
    ('contexts-not-legacy', 'planning.adapters', 'cli.prompts'),
    ('contexts-not-legacy', 'workspace.adapters', 'application.workflow'),
    ('contexts-not-legacy', 'agents.adapters', 'application.workflow'),
    ('contexts-not-legacy', 'agents.model', 'deadlines'),
    # The slice 4a imports from agents adapters into legacy adapters: both rules reject them.
    ('contexts-not-legacy', 'agents.adapters', 'adapters.shared', ('adapters-independent',)),
    # allow_indirect_imports: only direct imports are rejected; the indirect run must pass.
    ('agentshell-in-agents', 'ticketing.adapters', 'agent_shell'),
    ('agentshell-in-agents', 'agents.model', 'agent_shell'),
    ('agentshell-in-agents', 'cli', 'agent_shell'),
)

# Rows and imports name modules relative to the package, except these external packages.
EXTERNAL = {'agent_shell'}


def absolute(module: str) -> str:
    return module if module in EXTERNAL else f'{PACKAGE}.{module}'


def rule_units(rule: dict) -> tuple[list[str], list[str]]:
    """Names the checker reports a violation between: (importer side, imported side)."""
    if rule['type'] == 'forbidden':
        return rule['source_modules'], rule['forbidden_modules']
    if rule['type'] == 'independence':
        return rule['modules'], rule['modules']
    names = [f'{container}.{name.strip()}' for container in rule['containers']
             for layer in rule['layers'] for name in re.split('[:|]', layer.strip('()'))]
    return names, names


def unit(module: str, names: list[str]) -> str | None:
    """The shortest part of the module name that a rule name matches."""
    parts = module.split('.')
    for end in range(1, len(parts) + 1):
        prefix = '.'.join(parts[:end])
        if any(matches(name, prefix) for name in names):
            return prefix
    return None


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
            path.write_text(''.join(f'import {absolute(imported)}\n'
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
        rows = [(row[1], row[2], row[3] if len(row) > 3 else ())
                for row in REJECTED if row[0] == rule_id]
        self.assertTrue(rows, f'Rule {rule_id} has no rows in REJECTED.')
        rule = RULES[rule_id]
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            package = workspace / 'src' / PACKAGE
            bridge = package / source('boundary_probe.bridge')
            # Arrange: the actual rules accept the clean fixture.
            self.assert_passes(self.check(workspace))
            for (area, target, also), indirect in [(row, way) for row in rows
                                                   for way in (False, True)]:
                with self.subTest(area=area, target=target, indirect=indirect):
                    others = [other for other in RULES if other != rule_id and other not in also]
                    module = package / source(area)
                    if module.is_file():
                        probe, importer = module, f'{PACKAGE}.{area}'
                    else:
                        probe = package / source(area).with_suffix('') / 'probe.py'
                        importer = f'{PACKAGE}.{area}.probe'
                    clean = probe.read_text() if probe.is_file() else None
                    target_module = absolute(target)
                    line = f'import {target_module}\n'
                    if indirect:
                        bridge.write_text(line)
                        line = f'import {PACKAGE}.boundary_probe.bridge\n'
                    probe.write_text((clean or '') + line)
                    # Step 1: with the target rule off, the violation passes.
                    self.assert_passes(self.check(workspace, contracts=others))
                    if indirect and rule.get('allow_indirect_imports'):
                        # The rule rejects direct imports only; this indirect path must pass.
                        self.assert_passes(self.check(workspace))
                        if clean is None:
                            probe.unlink()
                        else:
                            probe.write_text(clean)
                        bridge.write_text('')
                        continue
                    # Step 2: with the target rule on, it fails with that rule and full path.
                    result = self.check(workspace)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    output = ' '.join(result.stdout.split())
                    sources, targets = rule_units(rule)
                    importer_unit, target_unit = unit(importer, sources), unit(target_module,
                                                                               targets)
                    self.assertTrue(importer_unit and target_unit,
                                    f'{rule_id} does not cover {importer} -> {target_module}.')
                    self.assertIn(f'{rule["name"]} BROKEN', output)
                    self.assertIn(f'{importer_unit} is not allowed to import {target_unit}:',
                                  output)
                    self.assertIn(importer, output)
                    self.assertIn(target_module, output)
                    if indirect:
                        self.assertIn(f'{PACKAGE}.boundary_probe.bridge', output)
                    # Step 3: with the violation removed, the fixture passes again.
                    if clean is None:
                        probe.unlink()
                    else:
                        probe.write_text(clean)
                    bridge.write_text('')
                    self.assert_passes(self.check(workspace))

    def test_unclassified_module_in_a_context_is_rejected(self):
        # Arrange: every module in a context must be one of its layers.
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            (workspace / 'src' / PACKAGE / 'ticketing' / 'helpers.py').write_text('')
            others = [rule for rule in RULES if rule != 'inside-each-area']
            self.assert_passes(self.check(workspace, contracts=others))
            # Act
            result = self.check(workspace)
            # Assert
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            output = ' '.join(result.stdout.split())
            self.assertIn(f'{RULES["inside-each-area"]["name"]} BROKEN', output)
            self.assertIn('not listed as layers', output)
            self.assertIn(f'{PACKAGE}.ticketing.helpers', output)

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
        named = {row[0] for row in REJECTED} | {
            rule for row in REJECTED for rule in (row[3] if len(row) > 3 else ())}
        self.assertLessEqual(named, set(RULES))


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
            if rule['type'] == 'forbidden':
                names = [*rule['source_modules'], *rule['forbidden_modules']]
            elif rule['type'] == 'independence':
                names = rule['modules']
            elif rule['type'] == 'layers':
                # The checker itself fails on a missing required layer; optional ones may be absent.
                names = rule['containers']
            else:
                self.fail(f'Extend this check to cover {rule["type"]} rules.')
            for name in names:
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
        allowed = {Path('shared/resources.py'), Path('agents/adapters/agentshell/launch.py')}
        # Act
        users = {path.relative_to(SOURCE) for path in SOURCE.rglob('*.py')
                 if '__file__' in path.read_text()}
        # Assert
        self.assertEqual(users, allowed)

    def test_ports_and_models_name_no_provider(self):
        # Import rules cannot see a hard-coded provider name, URL or pattern in core code.
        files = [*SOURCE.glob('*/ports.py'), *SOURCE.glob('*/model.py'),
                 *SOURCE.glob('factory/**/*.py')]
        self.assertTrue(files)
        names = re.compile(r'github|gitlab|codeberg|linear|tmux|herdr|agent_shell', re.IGNORECASE)
        found = {str(path.relative_to(SOURCE)): sorted({name.casefold() for name in
                                                        names.findall(path.read_text())})
                 for path in files}
        self.assertEqual({path: hits for path, hits in found.items() if hits}, {})

    def test_tests_find_source_files_through_constants(self):
        # A source path written in a test breaks silently when the module moves (slice 4a).
        written = re.compile(rf'src/{PACKAGE}/[\w/]+\.py')
        found = {path.name: written.findall(path.read_text())
                 for path in ROOT.joinpath('tests').rglob('*.py')
                 if path.name != Path(__file__).name}
        self.assertEqual({name: paths for name, paths in found.items() if paths}, {})

    def test_resource_root_holds_the_bundle(self):
        from forgetful_factory.shared.resources import resource_root

        self.assertTrue((resource_root() / 'role-resources.json').is_file())
        self.assertTrue((resource_root() / 'install-locks.zip').is_file())
        self.assertTrue((resource_root() / 'foreman' / 'AGENTS.md').is_file())

    def test_launch_targets_exist(self):
        # Arrange: these are started by file path or module name, which imports cannot see.
        from forgetful_factory.agents.adapters.agentshell import launch

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
