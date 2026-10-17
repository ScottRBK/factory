import argparse
import math
import os
import shlex
import signal
import sys
from dataclasses import replace
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration, ForgetfulConnection
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.cli.bootstrap import build_initialiser, build_watcher
from forgetful_factory.domain.models import FactoryError


def select_repositories(application: InitialiseFactory, workspace: Path) -> list[Path]:
    candidates = application.discover(workspace)
    if not candidates:
        raise FactoryError('No local repository roots found. Use --repo /path/to/repository.')
    for index, path in enumerate(candidates, 1):
        print(f'{index}. {path}')
    answer = input('Select repositories (comma-separated numbers; Enter selects all): ').strip()
    if not answer:
        return candidates
    try:
        indexes = [int(value.strip()) for value in answer.split(',')]
    except ValueError as error:
        raise FactoryError('Select repository numbers separated by commas.') from error
    if any(index < 1 or index > len(candidates) for index in indexes):
        raise FactoryError('Repository selection is out of range.')
    return list(dict.fromkeys(candidates[index - 1] for index in indexes))


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='forgetful-factory')
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init', help='Configure this workspace factory')
    init.add_argument('--workspace', type=Path, default=Path.cwd(),
                      help='Existing workspace for discovery and .factory/factory.toml')
    init.add_argument('--repo', action='append', type=Path,
                      help='Local repository root; repeat for multiple repos')
    init.add_argument('--label', action='append', help='Watched label or *; repeat for multiple')
    init.add_argument('--foreman-model', help='Foreman model text setting (provider/model)')
    init.add_argument('--foreman-effort', help='Foreman effort text setting')
    init.add_argument('--feature-owner-model', help='Native Pi model; defaults to Foreman model')
    init.add_argument('--feature-owner-effort', help='Native Pi effort; defaults to Foreman effort')
    init.add_argument('--grill-me-skill', type=Path, help='Existing unchanged grill-me SKILL.md')
    init.add_argument('--install-role-runtime', action='store_true',
                      help='Consent to the locked AgentShell extension runtime installation')
    init.add_argument('--pi-agent-dir', help='Normal native Pi agent directory to share')
    init.add_argument('--share-pi-profile', action='store_true',
                      help='Consent to the whole shared native Pi profile, including model listing')
    init.add_argument('--login', action='store_true',
                      help='Run native Forgetful server sign-in before the access check')
    init.add_argument('--check-connection', action='store_true',
                      help='Compatibility option; init always checks Forgetful access')
    init.add_argument('--forgetful-method', choices=('mcp', 'cli'))
    init.add_argument('--forgetful-instance', choices=('local', 'server'))
    init.add_argument('--forgetful-executable')
    init.add_argument('--forgetful-database', type=Path)
    init.add_argument('--forgetful-server')
    init.add_argument('--forgetful-project', type=int, help='Existing Forgetful project ID')
    watch = commands.add_parser('watch', help='Watch issues and notify one new owned Pi session')
    watch.add_argument('--workspace', type=Path, default=Path.cwd())
    watch.add_argument('--interval', type=float, default=30)
    watch.add_argument('--agentshell-python', default=sys.executable,
                       help='Override AgentShell Python; defaults to the factory environment')
    choice = watch.add_mutually_exclusive_group()
    choice.add_argument('--existing', action='store_true', help='Forward existing open matches')
    choice.add_argument('--new-only', action='store_true', help='Baseline existing open matches')
    return parser.parse_args()


def _configure_new_factory(application: InitialiseFactory, workspace: Path,
                           args: argparse.Namespace, paths: list[Path] | None,
                           connection: ForgetfulConnection, home: str
                           ) -> FactoryConfiguration:
    if paths is None:
        paths = select_repositories(application, workspace)
        for reference in application.inspect(paths).values():
            print(f'{reference.local_dir} -> {reference.remote}')
        if input('Confirm these GitHub origins? [y/N]: ').strip().lower() != 'y':
            raise FactoryError('Initialization cancelled; no labels or config changed.')
    labels = args.label if args.label is not None else input(
        'Watched labels (comma-separated, or *): ').split(',')
    model = args.foreman_model
    if model is None:
        _prepare_foreman(application, connection, args)
        model = _select_model(application, connection, home, None, args.feature_owner_model)
    effort = args.foreman_effort if args.foreman_effort is not None else input(
        'Foreman effort: ')
    return application.configure(paths, labels, model, effort)


def _check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
                               executable: str | None) -> None:
    supplied = {'method': args.forgetful_method, 'instance': args.forgetful_instance,
                'executable': executable, 'server': args.forgetful_server,
                'project_id': args.forgetful_project,
                'database': (str(args.forgetful_database.expanduser().resolve())
                             if args.forgetful_database is not None else None)}
    if any(value is not None and value != getattr(existing, key)
           for key, value in supplied.items()):
        raise FactoryError('Forgetful arguments conflict with existing config; edit '
                           '.factory/factory.toml explicitly, then rerun init.')


def _connection(args: argparse.Namespace, workspace: Path,
                existing: ForgetfulConnection | None) -> ForgetfulConnection:
    executable = args.forgetful_executable
    if executable is not None and ('/' in executable or executable.startswith('~')):
        executable = str(Path(executable).expanduser().resolve())
    if existing is not None:
        _check_existing_connection(args, existing, executable)
        return existing
    method = args.forgetful_method or 'cli'
    instance = args.forgetful_instance or (
        input('Forgetful instance [local/server; default local]: ').strip() or 'local')
    server = args.forgetful_server
    if instance == 'server' and server is None:
        server = input('Existing Forgetful server URL: ').strip()
    database = args.forgetful_database
    if instance == 'local' and database is None:
        database = workspace / '.factory/data/forgetful.db'
    connection = ForgetfulConnection(method, instance, executable or 'forgetful',
                                     str(database.expanduser().resolve()) if database else None,
                                     server, args.forgetful_project)
    connection.validate()
    return connection


def _prepare_foreman(application, connection, args):
    application.prepare_foreman(connection, _install_missing,
                                lambda command, prompt: (
                                    command == 'agentshell-runtime'
                                    and args.install_role_runtime
                                    or input(prompt).strip().lower() == 'y'))


def _print_models(models: list[str]) -> None:
    provider = None
    for index, model in enumerate(models, 1):
        group = model.partition('/')[0]
        if group != provider:
            print(_safe_diagnostic(group) + ':')
            provider = group
        print(f'  {index}. {_safe_diagnostic(model)}')


def _select_model(application, connection, home: str, requested: str | None,
                  owner: str | None = None) -> str:
    print(f'Native Pi login: in another terminal run PI_CODING_AGENT_DIR={shlex.quote(home)} pi, '
          'then use /login. Listing and selection do not verify model access.')
    while True:
        models = application.profile.list_models(connection)
        if models:
            break
        print('No selectable models. Configure native Pi login/models in the chosen home.')
        if input('After login, [r] recheck or [n] stop: ').strip().lower() != 'r':
            raise FactoryError('Pi model setup is incomplete; rerun init after native Pi /login.')
    _print_models(models)
    if owner is not None and owner not in models:
        raise FactoryError('Feature-owner model is not selectable; choose an exact native Pi '
                           'provider/model and rerun init.')
    if requested is not None:
        if requested not in models:
            raise FactoryError('Configured Foreman model is not selectable in the chosen Pi home. '
                               'Choose an exact provider/model listed above; access unverified. '
                               'Correct --foreman-model (or edit existing factory.toml) '
                               'and rerun init.')
        return requested
    try:
        index = int(input('Select Foreman model number: '))
    except ValueError as error:
        raise FactoryError('Select a model number from the native Pi list.') from error
    if index < 1 or index > len(models):
        raise FactoryError('Model selection is out of range.')
    return models[index - 1]


def _confirm_pi_home(home: str, args: argparse.Namespace) -> bool:
    print(f'Use your existing Pi login from:\n  {home}')
    print('Your Pi settings and history remain shared; changes can affect your usual Pi sessions.\n'
          'The Foreman skips your personal SYSTEM.md. '
          'AGENTS.md and APPEND_SYSTEM.md can still apply.\n'
          'The Foreman uses Factory-selected skills/extensions. MCP connections are disabled.\n'
          'Listing models can run your installed Pi extensions and credential commands.\n'
          'Handling work sends model requests and may incur charges.')
    return args.share_pi_profile or input('Use this Pi profile? [y/N]: ').strip().lower() == 'y'


def _install_missing(commands: list[str]) -> None:
    print('Missing executables: ' + ', '.join(commands))
    print('No automatic installer for these executables is bundled. '
          'Existing installations will not be upgraded.')
    answer = input('Install missing executables manually with a reviewed source now? [y/N]: ')
    if answer.strip().lower() != 'y':
        raise FactoryError('Installation declined; required executable missing. '
                           'Setup is incomplete; install it and rerun init.')
    input('Complete the reviewed installation in another terminal, then press Enter to recheck: ')


def _safe_diagnostic(message: str) -> str:
    return ''.join(char if char.isprintable() or char == '\n' else f'\\u{ord(char):04x}'
                   for char in message)


def _choose_existing(args: argparse.Namespace) -> bool:
    if args.existing or args.new_only:
        return args.existing
    answer = input('Forward existing matches [e] or new matches only [n]? [e/n]: ')
    answer = answer.strip().lower()
    if answer not in ('e', 'n'):
        raise FactoryError('Choose e for existing matches or n for new matches only.')
    return answer == 'e'


def _watch(args: argparse.Namespace, workspace: Path) -> int:
    from forgetful_factory.configuration import load_configuration

    if not math.isfinite(args.interval) or args.interval <= 0:
        raise FactoryError('--interval must be positive and finite.')
    config = load_configuration(workspace)
    application = build_watcher(args.agentshell_python, config, workspace)

    def interrupted(signum, frame):
        raise KeyboardInterrupt

    previous = signal.signal(signal.SIGTERM, interrupted)
    try:
        application.run(config, workspace, args.interval, lambda: _choose_existing(args),
                        lambda message: print(message, flush=True),
                        lambda message: print(_safe_diagnostic(message),
                                              file=sys.stderr, flush=True))
    finally:
        signal.signal(signal.SIGTERM, previous)
    return 0


def _listed_project_id(answer: str, projects: list[dict]) -> int:
    try:
        project_id = int(answer)
    except ValueError as error:
        raise FactoryError('Select a listed project ID or c to create one.') from error
    if project_id not in {project['id'] for project in projects}:
        raise FactoryError('Select a listed project ID or c to create one.')
    return project_id


def _select_project(application: InitialiseFactory, connection: ForgetfulConnection,
                    workspace: Path) -> int:
    projects = application.profile.projects(connection)
    if projects:
        for project in projects:
            print(f"{project['id']}. {_safe_diagnostic(project['name'])}")
        print('c. Create new project')
        answer = input('Select Forgetful project ID or c to create: ').strip()
        if answer.casefold() != 'c':
            return _listed_project_id(answer, projects)
    else:
        print('No Forgetful projects found. Create one to continue setup.')
    name = input(f'Project name [{_safe_diagnostic(workspace.name)}]: ').strip() or workspace.name
    if not name or len(name) > 500:
        raise FactoryError('Project name must contain 1 to 500 characters.')
    confirm = input(f'Create Forgetful project "{_safe_diagnostic(name)}"? [y/N]: ')
    if confirm.strip().lower() != 'y':
        raise FactoryError('Project creation cancelled; no project was created. '
                           'Setup is incomplete.')
    project_id = application.profile.create_project(connection, name)
    print(f'Created Forgetful project {project_id}: {_safe_diagnostic(name)}')
    return project_id


def _owner_configuration(args: argparse.Namespace, config: FactoryConfiguration,
                         existing: bool) -> FactoryConfiguration:
    if existing:
        for supplied, saved in ((args.feature_owner_model, config.feature_owner_agent_model),
                                (args.feature_owner_effort, config.feature_owner_agent_effort),
                                (str(args.grill_me_skill.expanduser().resolve())
                                 if args.grill_me_skill else None, config.grill_me_skill)):
            if supplied is not None and supplied != saved:
                raise FactoryError('Owner arguments conflict with config; edit factory.toml.')
    else:
        config = replace(config,
            feature_owner_agent_model=args.feature_owner_model or config.foreman_agent_model,
            feature_owner_agent_effort=args.feature_owner_effort or config.foreman_agent_effort,
            grill_me_skill=str((args.grill_me_skill or
                               Path.home() / '.agents/skills/grill-me/SKILL.md')
                              .expanduser().resolve()))
    return config


def _initialise(args: argparse.Namespace, workspace: Path) -> int:
    application = build_initialiser(workspace)
    paths = ([Path(os.path.abspath(path.expanduser())) for path in args.repo]
             if args.repo is not None else None)
    config = application.load_existing(paths, args.label, args.foreman_model,
                                       args.foreman_effort)
    existing = config is not None
    connection = _connection(args, workspace, config.forgetful if config else None)
    home = application.profile.choose_pi_home(args.pi_agent_dir,
                                             lambda home: _confirm_pi_home(home, args))
    application.profile.begin_setup()
    if config is None:
        config = _configure_new_factory(application, workspace, args, paths, connection, home)
    config = _owner_configuration(args, config, existing)
    config = replace(config, forgetful=connection)
    def validate_model():
        nonlocal connection, config
        if existing or args.foreman_model is not None:
            _prepare_foreman(application, connection, args)
            _select_model(application, connection, home, config.foreman_agent_model,
                          config.feature_owner_agent_model)

        if connection.project_id is None:
            project_id = _select_project(application, connection, workspace)
            connection = replace(connection, project_id=project_id)
            config = replace(config, forgetful=connection)
        application.profile.prepare_roles(config)
        return config
    for message in application.initialise(config, before_writes=validate_model,
                                           save=not existing):
        print(message)
    print('Foreman model selected; access unverified (no model request made).')
    print(f'Factory configuration: {workspace}/.factory/factory.toml')
    print('Checking Forgetful connection and planning access...', flush=True)
    if application.profile.uses_browser_login(connection):
        print('If your browser opens, complete Forgetful sign-in there.', flush=True)
    print(application.check_foreman(config, login=args.login))
    application.profile.record_completion(config)
    return 0


def main() -> int:
    args = _parse_arguments()
    try:
        workspace = args.workspace.expanduser().resolve()
        if not workspace.is_dir():
            raise FactoryError(f'Workspace must be an existing directory: {workspace}')
        if args.command == 'watch':
            return _watch(args, workspace)
        return _initialise(args, workspace)
    except EOFError:
        message = ('For noninteractive watch provide --existing or --new-only.'
                   if args.command == 'watch' else
                   'For noninteractive init provide --repo, --label, '
                   '--foreman-model, --foreman-effort, --forgetful-instance, '
                   'and --share-pi-profile. '
                   'Setup may need installation consent. Forgetful access is always checked; '
                   'server checks may open browser sign-in. '
                   'Existing saved setup is kept; rerun init to retry.')
        print(f'Error: Input ended. {message}', file=sys.stderr)
        return 1
    except KeyboardInterrupt as error:
        message = f'Error: {args.command.capitalize()} interrupted.'
        if str(error):
            message += ' ' + _safe_diagnostic(str(error))
        elif args.command == 'init':
            message += ' Setup is incomplete; rerun init to retry.'
        print(message, file=sys.stderr)
        return 130
    except (FactoryError, OSError) as error:
        print(f'Error: {_safe_diagnostic(str(error))}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
