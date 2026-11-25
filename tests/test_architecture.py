"""Exercise the real Import Linter CLI against disposable packages and repository rules."""

import ast
import importlib.util
import os
import re
import runpy
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
    'shared.command',
    'cli.bootstrap',
    'cli.prompts',
    'configuration',
    'factory.model',
    'factory.ports',
    'factory.services.workflow',
    'factory.adapters.filesystem',
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
    'agents.services.dispatch',
    'agents.adapters.agentshell.controller',
    'workspace.ports',
    'workspace.adapters.git.worktrees',
    'runtime.ports',
    'runtime.adapters.tmux',
    'channels.ports',
    'channels.adapters.terminal',
    'boundary_probe.bridge',
)

# Allowed imports (importer, imported). Together they are the known-good fixture: ports, shared
# adapter code and both composition entry points. With every rule on, it must pass.
# Only factory.adapters.filesystem starts processes: a core probe that targets any other adapter
# then breaks the composition rule alone, not core-no-processes too.
ALLOWED = (
    ('__main__', 'cli.prompts'),
    ('shared.command', 'shared.errors'),
    ('shared.command', 'subprocess'),
    ('factory.model', 'shared.errors'),
    ('factory.model', 'ticketing.model'),
    ('factory.model', 'planning.model'),
    ('factory.ports', 'factory.model'),
    ('factory.services.workflow', 'shared.errors'),
    ('factory.services.workflow', 'factory.ports'),
    ('factory.services.workflow', 'factory.model'),
    ('factory.services.workflow', 'ticketing.ports'),
    ('factory.services.workflow', 'forge.ports'),
    ('factory.services.workflow', 'planning.ports'),
    ('factory.services.workflow', 'workspace.ports'),
    ('factory.services.workflow', 'agents.ports'),
    ('factory.services.workflow', 'channels.ports'),
    ('factory.adapters.filesystem', 'factory.ports'),
    ('factory.adapters.filesystem', 'agents.ports'),
    ('factory.adapters.filesystem', 'shared.command'),
    ('factory.adapters.filesystem', 'socket'),
    ('ticketing.ports', 'ticketing.model'),
    ('ticketing.adapters.github', 'ticketing.ports'),
    ('ticketing.adapters.github', 'shared.errors'),
    ('forge.ports', 'forge.model'),
    ('forge.adapters.github', 'forge.ports'),
    ('forge.adapters.github', 'shared.errors'),
    ('planning.ports', 'planning.model'),
    ('planning.adapters.forgetful.plan_store', 'planning.ports'),
    ('planning.adapters.forgetful.plan_store', 'planning.adapters.forgetful.connection'),
    ('workspace.adapters.git.worktrees', 'workspace.ports'),
    ('workspace.adapters.git.worktrees', 'shared.errors'),
    ('agents.ports', 'agents.model'),
    ('agents.adapters.agentshell.controller', 'agent_shell'),
    ('agents.adapters.agentshell.controller', 'runtime.ports'),
    ('agents.adapters.agentshell.controller', 'channels.ports'),
    ('runtime.adapters.tmux', 'runtime.ports'),
    ('runtime.adapters.tmux', 'shared.errors'),
    ('channels.ports', 'runtime.ports'),
    ('channels.adapters.terminal', 'channels.ports'),
    ('channels.adapters.terminal', 'runtime.ports'),
    ('cli.bootstrap', 'configuration'),
    ('cli.bootstrap', 'factory.adapters.filesystem'),
    ('cli.bootstrap', 'factory.services.workflow'),
    ('cli.bootstrap', 'ticketing.adapters.github'),
    ('cli.bootstrap', 'forge.adapters.github'),
    ('cli.bootstrap', 'planning.adapters.forgetful.plan_store'),
    ('cli.bootstrap', 'workspace.adapters.git.worktrees'),
    ('cli.bootstrap', 'agents.adapters.agentshell.controller'),
    ('cli.bootstrap', 'runtime.adapters.tmux'),
    ('cli.bootstrap', 'channels.adapters.terminal'),
    ('cli.bootstrap', 'shared.errors'),
    ('configuration', 'factory.adapters.filesystem'),
    ('configuration', 'factory.model'),
    ('configuration', 'shared.errors'),
)

# Rejected imports (rule id, importing area, imported module[, other rules]). The area is a
# package (the probe is a new module in it) or a module (the probe line is added to it). Each row
# runs direct and indirect. Only its own rule may reject it, unless the row names the other rules
# that must also reject it; step 1 then turns those off too (the skill's isolation).
REJECTED = (
    # Top level, downwards only: __main__, then cli and configuration, factory, the contexts
    # and shared.
    ('top-level', 'shared', '__main__'),
    ('top-level', 'shared', 'cli.prompts'),
    ('top-level', 'shared', 'factory.model'),
    ('top-level', 'shared', 'ticketing.model'),
    ('top-level', 'shared', 'agents.ports'),
    # The configuration facade imports a factory adapter, so the composition rule also applies.
    ('top-level', 'shared', 'configuration', ('adapters-from-composition',)),
    ('top-level', 'cli', '__main__'),
    ('top-level', 'factory.services', 'cli.prompts'),
    ('top-level', 'factory.model', 'cli.prompts'),
    ('top-level', 'factory.adapters', 'cli.prompts'),
    ('top-level', 'ticketing.model', 'factory.model'),
    ('top-level', 'ticketing.adapters', 'cli.prompts'),
    ('top-level', 'forge.adapters', 'factory.ports'),
    ('top-level', 'planning.adapters', 'cli.prompts'),
    ('top-level', 'workspace.adapters', 'factory.model'),
    ('top-level', 'agents.model', 'factory.model'),
    ('top-level', 'agents.adapters', 'cli.prompts'),
    ('top-level', 'runtime.adapters', 'factory.ports'),
    ('top-level', 'channels.adapters', 'cli.prompts'),
    ('inside-each-area', 'factory.model', 'factory.ports'),
    ('inside-each-area', 'factory.ports', 'factory.services.workflow'),
    ('inside-each-area', 'ticketing.model', 'ticketing.ports'),
    ('inside-each-area', 'forge.model', 'forge.ports'),
    ('inside-each-area', 'planning.model', 'planning.ports'),
    ('inside-each-area', 'agents.model', 'agents.ports'),
    # A port importing its own adapter breaks the layers and the composition rule; through the
    # agents adapter's use of the port it also links two adapter packages.
    ('inside-each-area', 'runtime.ports', 'runtime.adapters.tmux',
     ('adapters-from-composition', 'adapters-independent')),
    ('adapters-from-composition', 'factory.services', 'ticketing.adapters.github'),
    ('adapters-from-composition', 'factory.services', 'forge.adapters.github'),
    ('adapters-from-composition', 'factory.services', 'workspace.adapters.git.worktrees'),
    ('adapters-from-composition', 'factory.services', 'agents.adapters.agentshell.controller'),
    ('adapters-from-composition', 'factory.services', 'runtime.adapters.tmux'),
    ('adapters-from-composition', 'factory.services', 'channels.adapters.terminal'),
    # The factory adapter imports the factory port and model, so independence also rejects these.
    ('adapters-from-composition', 'factory.model', 'planning.adapters.forgetful.plan_store',
     ('adapters-independent',)),
    ('adapters-from-composition', 'factory.ports', 'ticketing.adapters.github',
     ('adapters-independent',)),
    ('adapters-from-composition', 'shared', 'ticketing.adapters.github',
     ('top-level',)),
    # Every forge module is reachable from forge.adapters, so independence also rejects this.
    ('adapters-from-composition', 'forge.ports', 'ticketing.adapters.github',
     ('adapters-independent',)),
    # The entry point runs the CLI; it does not build adapters itself. Indirect runs pass.
    ('entry-through-cli', '__main__', 'ticketing.adapters.github'),
    ('entry-through-cli', '__main__', 'agents.adapters.agentshell.controller'),
    ('adapters-independent', 'factory.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'factory.adapters', 'planning.adapters.forgetful.plan_store'),
    ('adapters-independent', 'forge.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'planning.adapters', 'forge.adapters.github'),
    ('adapters-independent', 'workspace.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'agents.adapters', 'ticketing.adapters.github'),
    ('adapters-independent', 'agents.adapters', 'runtime.adapters.tmux'),
    ('adapters-independent', 'runtime.adapters', 'agents.adapters.agentshell.controller'),
    # A channel reaches the host through its port; composition supplies the adapter.
    ('adapters-independent', 'channels.adapters', 'runtime.adapters.tmux'),
    ('core-no-processes', 'factory.services', 'subprocess'),
    ('core-no-processes', 'factory.services', 'socket'),
    ('core-no-processes', 'factory.ports', 'subprocess'),
    ('core-no-processes', 'factory.model', 'socket'),
    ('core-no-processes', 'ticketing.model', 'subprocess'),
    ('core-no-processes', 'agents.ports', 'subprocess'),
    ('core-no-processes', 'runtime.ports', 'socket'),
    # allow_indirect_imports: only direct imports are rejected; the indirect run must pass.
    ('agentshell-in-agents', 'factory.services', 'agent_shell'),
    ('agentshell-in-agents', 'ticketing.adapters', 'agent_shell'),
    ('agentshell-in-agents', 'agents.model', 'agent_shell'),
    ('agentshell-in-agents', 'agents.services', 'agent_shell'),
    ('agentshell-in-agents', 'runtime.adapters', 'agent_shell'),
    ('agentshell-in-agents', 'channels.adapters', 'agent_shell'),
    ('agentshell-in-agents', 'cli', 'agent_shell'),
)

# Rows and imports name modules relative to the package, except these external packages.
EXTERNAL = {'agent_shell', 'socket', 'subprocess'}


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
        # The probe package sits outside every layer on purpose; only exhaustiveness ignores it.
        rules = (ROOT / 'pyproject.toml').read_text()
        marker = 'id = "top-level"\n'
        self.assertEqual(rules.count(marker), 1)
        rules = rules.replace(marker, marker + 'exhaustive_ignores = ["boundary_probe"]\n')
        (workspace / 'pyproject.toml').write_text(rules)

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

    def assert_unclassified_rejected(self, rule_id, module):
        # Arrange: every module in the rule's containers must be one of its layers.
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            self.fixture(workspace)
            (workspace / 'src' / PACKAGE / source(module)).write_text('')
            others = [rule for rule in RULES if rule != rule_id]
            self.assert_passes(self.check(workspace, contracts=others))
            # Act
            result = self.check(workspace)
            # Assert
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            output = ' '.join(result.stdout.split())
            self.assertIn(f'{RULES[rule_id]["name"]} BROKEN', output)
            self.assertIn('not listed as layers', output)
            self.assertIn(f'{PACKAGE}.{module}', output)

    def test_unclassified_module_in_a_context_is_rejected(self):
        self.assert_unclassified_rejected('inside-each-area', 'ticketing.helpers')

    def test_unclassified_module_in_the_factory_is_rejected(self):
        self.assert_unclassified_rejected('inside-each-area', 'factory.helpers')

    def test_unclassified_top_level_module_is_rejected(self):
        self.assert_unclassified_rejected('top-level', 'helpers')

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

    def test_package_initializers_import_nothing(self):
        # A rule that names a package's children cannot see imports in its __init__.py.
        found = {str(path.relative_to(SOURCE)) for path in SOURCE.rglob('__init__.py')
                 if any(isinstance(node, (ast.Import, ast.ImportFrom))
                        for node in ast.walk(ast.parse(path.read_text())))}
        self.assertEqual(found, set())

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

    def test_top_level_rule_classifies_every_package(self):
        # The checker enforces this too (exhaustive); a direct check names the gap clearly.
        top_level = {path.stem for path in SOURCE.glob('*.py')} | {
            path.parent.name for path in SOURCE.glob('*/__init__.py')}
        rule = RULES['top-level']
        layers = {name.strip() for layer in rule['layers'] for name in re.split('[:|]', layer)}
        self.assertEqual(rule['containers'], [PACKAGE])
        self.assertTrue(rule['exhaustive'])
        self.assertEqual(layers, top_level - {'__init__'})

    def test_core_rule_covers_every_context(self):
        # A wildcard covers a new context's services, ports and model without an edit.
        rule = RULES['core-no-processes']
        self.assertEqual(rule['source_modules'], [f'{PACKAGE}.*.services', f'{PACKAGE}.*.ports',
                                                  f'{PACKAGE}.*.model'])
        self.assertNotIn('allow_indirect_imports', rule)

    def test_package_folders_find_files_in_one_place(self):
        # Arrange: a file found relative to source breaks silently when a module moves.
        # The controller runs in AgentShell's interpreter, where Factory cannot be imported, so it
        # finds its host file beside itself; test_launch_targets_exist checks that file.
        allowed = {Path('shared/resources.py'), Path('agents/adapters/agentshell/launch.py'),
                   Path('agents/adapters/agentshell/controller.py')}
        # Act
        users = {path.relative_to(SOURCE) for path in SOURCE.rglob('*.py')
                 if '__file__' in path.read_text()}
        # Assert
        self.assertEqual(users, allowed)

    def test_ports_and_models_name_no_provider(self):
        # Import rules cannot see a hard-coded provider name, URL or pattern in core code.
        files = [*SOURCE.glob('*/ports.py'), *SOURCE.glob('*/model.py'),
                 *SOURCE.glob('*/model/*.py'), *SOURCE.glob('factory/**/*.py')]
        self.assertTrue(any(path.parts[-3] == 'factory' for path in files))
        names = re.compile(r'github|gitlab|codeberg|linear|tmux|herdr|agent_?shell', re.IGNORECASE)
        found = {str(path.relative_to(SOURCE)): sorted(name.casefold() for name in
                                                       names.findall(path.read_text()))
                 for path in set(files)}
        # Known leaks, kept because the refactor must not change behaviour (changes need Scott):
        # init's failure text after label writes says "check GitHub"; the agents model holds
        # AgentShellLifecycleDeadlines (placed there by the plan) and two role-validation
        # messages that name AgentShell.
        known = {'factory/services/initialise_factory.py': ['github'],
                 'agents/model.py': ['agentshell'] * 5}
        self.assertEqual({path: hits for path, hits in found.items() if hits}, known)

    def test_source_distribution_carries_every_test_file(self):
        # The sdist ships the tests; a file outside these patterns breaks collection there.
        build = tomllib.loads((ROOT / 'pyproject.toml').read_text())['tool']['uv']
        patterns = build['build-backend']['source-include']

        def included(path: str) -> bool:
            return any(re.fullmatch(re.escape(pattern).replace(r'\*', '[^/]*'), path)
                       for pattern in patterns)

        files = [path.relative_to(ROOT).as_posix() for path in (ROOT / 'tests').rglob('*')
                 if path.is_file() and '__pycache__' not in path.parts]
        self.assertTrue(files)
        self.assertEqual([path for path in files if not included(path)], [])

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
        self.assertTrue(launch.TMUX_HOST.is_file())
        self.assertEqual(launch.TMUX_HOST.parent, launch.CONTROLLER.parent)
        owner = importlib.util.find_spec(launch.OWNER_MODULE)
        self.assertIsNotNone(owner)
        self.assertTrue(Path(owner.origin).is_relative_to(SOURCE))
        # The controller picks its host file by name; the constant must name the same file.
        from forgetful_factory.agents.adapters.agentshell import controller
        self.assertEqual(controller.HOST_FILES['tmux'], launch.TMUX_HOST.name)

    def test_help_works_without_the_lock_module(self):
        # Arrange: fcntl is needed only when a command takes the workspace lease.
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, 'sitecustomize.py').write_text(
                "import sys\nsys.modules['fcntl'] = None\n")
            env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(SOURCE.parent), temporary)))
            # Act
            result = subprocess.run([sys.executable, '-m', PACKAGE, '--help'], env=env,
                                    capture_output=True, text=True, timeout=30)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('usage:', result.stdout)

    def test_launch_paths_keep_the_installed_spelling(self):
        # Arrange: the package reached through a symlinked folder, as some installs are.
        from forgetful_factory.agents.adapters.agentshell import launch

        with tempfile.TemporaryDirectory() as temporary:
            link = Path(temporary) / 'agentshell'
            link.symlink_to(Path(launch.__file__).parent, target_is_directory=True)
            # Act
            names = runpy.run_path(str(link / 'launch.py'))
        # Assert: the owner and the model catalog were started by the path as given.
        self.assertEqual(names['CONTROLLER'], link / 'controller.py')
        self.assertEqual(names['MODEL_CATALOG'], link / 'model_catalog.py')


def _rejection_test(rule_id):
    def test(self):
        self.assert_rejected(rule_id)
    test.__doc__ = f'Rule {rule_id} rejects every row in REJECTED, direct and indirect.'
    return test


# One test per configured rule, so a new rule fails until it has REJECTED rows.
for _rule_id in RULES:
    setattr(ArchitectureTests, f'test_{_rule_id.replace("-", "_")}_rejects_violations',
            _rejection_test(_rule_id))
