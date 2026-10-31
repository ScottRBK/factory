import argparse
import math
import os
import shlex
import signal
import sys
from dataclasses import dataclass, replace
from functools import partial
from pathlib import Path
from typing import cast
from urllib.parse import urlsplit

from forgetful_factory.application.configuration import (
    FactoryConfiguration,
    ForgetfulConnection,
)
from forgetful_factory.application.initial_agent_choices import (
    WORKER_EFFORTS,
    InitialAgentChoices,
    validate_initial_agents,
)
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.cli.bootstrap import build_initialiser, build_watcher
from forgetful_factory.cli.numbered_selection import parse_numbered_selection
from forgetful_factory.deadlines import DeadlinePolicy
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
    init.set_defaults(manual_setup=False)
    mode = init.add_mutually_exclusive_group()
    mode.add_argument('--finalize', action='store_true',
                      help='Validate saved setup through the normal init checks')
    mode.add_argument('--assisted', action='store_true',
                      help='Finish setup with a dedicated Foreman')
    mode.add_argument('--attach', action='store_true', help='Enter the existing setup Foreman')
    init.add_argument('--delegated-work-stopped', action='store_true',
                      help='Confirm delegated work is stopped before changing live-owner setup')
    init.add_argument('--agentshell-python', default=sys.executable,
                      help='Installed AgentShell interpreter for the setup Foreman')
    init.add_argument('--workspace', type=Path, default=Path.cwd(),
                      help='Existing workspace for discovery and .factory/factory.toml')
    init.add_argument('--repo', action='append', type=Path,
                      help='Local repository root; repeat for multiple repos')
    init.add_argument('--label', action='append', help='Watched label or *; repeat for multiple')
    init.add_argument('--foreman-model', help='Foreman model text setting (provider/model)')
    init.add_argument('--foreman-effort', help='Foreman effort text setting')
    init.add_argument('--foreman-memory', action=argparse.BooleanOptionalAction, default=None,
                      help='Enable Foreman recall/capture for a Forgetful server')
    init.add_argument('--foreman-memory-model',
                      help='Exact native model selector for Foreman recall and capture')
    init.add_argument('--feature-owner-model', help='Native Pi model; defaults to Foreman model')
    init.add_argument('--feature-owner-effort', help='Native Pi effort; defaults to Foreman effort')
    init.add_argument('--research-model', help='Independent native research model selector')
    init.add_argument('--research-harness', help='Native research app')
    init.add_argument('--research-effort', help='Native research reasoning effort')
    init.add_argument('--grill-me-skill', type=Path, help='Existing unchanged grill-me SKILL.md')
    for role in ('implementation', 'review'):
        init.add_argument(f'--{role}-model', help=f'Native {role} model selector')
        init.add_argument(f'--{role}-harness', help='Native app: pi, codex or claude_code')
        init.add_argument(f'--{role}-effort', help=f'Native {role} reasoning effort')
        init.add_argument(f'--{role}-skill', action='append', type=Path,
                          help='Existing local skill file; repeat for additional skills')
    init.add_argument('--planning-only', action='store_true',
                      help='Explicitly defer implementation/review worker setup')
    init.add_argument('--tdd-skill', type=Path, help='Existing local TDD skill file')
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
    action = watch.add_mutually_exclusive_group()
    action.add_argument('--status', action='store_true',
                        help='Show Foreman and watcher lifecycle observations')
    action.add_argument('--start', action='store_true', help='Start watcher on the setup Foreman')
    action.add_argument('--stop', action='store_true',
                        help='Stop watcher, preserving setup Foreman')
    watch.add_argument('--owner-fd', type=int, help=argparse.SUPPRESS)
    watch.add_argument('--interval', type=float, default=30)
    watch.add_argument('--agentshell-python', default=sys.executable,
                       help='Override AgentShell Python; defaults to the factory environment')
    choice = watch.add_mutually_exclusive_group()
    choice.add_argument('--existing', action='store_true', help='Forward existing open matches')
    choice.add_argument('--new-only', action='store_true', help='Baseline existing open matches')
    foreman = commands.add_parser('foreman', help='Start or enter Foreman without a watcher')
    foreman.add_argument('--workspace', type=Path, default=Path.cwd())
    foreman.add_argument('--attach', action='store_true', help='Enter the existing Foreman')
    foreman.add_argument('--agentshell-python', default=sys.executable,
                         help='Installed AgentShell interpreter for Foreman')
    return parser.parse_args()


def _configure_new_factory(application: InitialiseFactory, workspace: Path,
                           args: argparse.Namespace, paths: list[Path] | None,
                           connection: ForgetfulConnection, home: str
                           ) -> tuple[FactoryConfiguration, InitialAgentChoices]:
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
    effort = args.foreman_effort if args.foreman_effort is not None else _select_numbered(
        'Foreman effort', WORKER_EFFORTS['pi'])
    config = application.configure(paths, labels,
        str(workspace / '.factory/agents/foreman/agent.json'))
    return config, InitialAgentChoices(
        model,
        effort,
        foreman_memory_enabled=args.foreman_memory is True,
        foreman_memory_model=args.foreman_memory_model,
    )


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


def _prepare_foreman(application, connection, args, *, prepared=False):
    if prepared:
        return
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


def _select_numbered(label: str, choices: list[str] | tuple[str, ...],
                     *, show_choices: bool = True, prompt: str | None = None) -> str:
    if show_choices:
        print(f'{label} choices:')
        for index, choice in enumerate(choices, 1):
            print(f'  {index}. {_safe_diagnostic(choice)}')
    answer = input(prompt if prompt is not None else f'Select {label} number: ')
    index = parse_numbered_selection(label, answer, len(choices))
    return choices[index - 1]


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
    return _select_numbered('Foreman model', models, show_choices=False)


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


def _change_managed_watch(args: argparse.Namespace, workspace: Path) -> int:
    import json

    from forgetful_factory.adapters.agentshell.owner_client import request

    if args.start:
        if not args.existing and not args.new_only:
            raise FactoryError('Managed watch needs --existing or --new-only.')
        if not math.isfinite(args.interval) or args.interval <= 0:
            raise FactoryError('--interval must be positive and finite.')
        result = request(workspace, 'start', existing=args.existing, interval=args.interval)
    else:
        result = request(workspace, 'stop')
    print(json.dumps(result))
    return 0


def _managed_watch_status(workspace: Path) -> dict | None:
    from forgetful_factory.adapters.agentshell.owner_client import read_state, request
    from forgetful_factory.adapters.watch_status import unknown_status

    try:
        state = read_state(workspace)
    except FactoryError as error:
        return {**unknown_status('managed_owner'), 'warning': str(error)}
    if state is None:
        return None
    try:
        state = {**request(workspace, 'status'), 'source': 'managed_owner',
                 'observation': 'live', 'process': 'present', 'process_role': 'foreman_owner',
                 'evidence': 'owner_report', 'health': 'not_checked'}
        state['phase'] = 'watching' if state['watcher'] == 'running' else state['watcher']
    except FactoryError as error:
        state = {**state, **unknown_status('managed_owner', 'saved'),
                 'target': state.get('target'), 'recorded_foreman': state.get('foreman'),
                 'recorded_watcher': state.get('watcher'), 'evidence': 'saved_record'}
        if state['recorded_foreman'] != 'stopped':
            state['warning'] = str(error)
            state['recovery'] = (
                'Saved state is not a live observation. Inspect the recorded socket/pane '
                'and .factory/runtime/foreman/owner.log. Do not signal saved PIDs. '
                'Only after independently confirming the original Foreman and owner '
                'have exited, archive owner.json and control.sock from '
                '.factory/runtime/foreman, then retry foreman '
                f'--workspace {shlex.quote(str(workspace))}. If uncertain, preserve them.')
    return state


def _watch_status(workspace: Path) -> int:
    import json

    from forgetful_factory.adapters.filesystem.foreman_profile import ForemanProfile
    from forgetful_factory.adapters.watch_status import plain_watch_status, unknown_status
    from forgetful_factory.configuration import load_configuration

    plain = plain_watch_status(workspace)
    if plain and plain['observation'] == 'live':
        state = plain
    else:
        managed = _managed_watch_status(workspace)
        if managed and managed['observation'] == 'live':
            state = managed
        elif plain and managed:
            state = {**managed, 'source': 'combined', 'foreman': 'unknown', 'watcher': 'unknown',
                     'phase': 'unknown', 'process': 'unknown', 'health': 'not_checked',
                     'observation': ('saved' if 'saved' in (plain['observation'],
                                                          managed['observation'])
                                     else 'unavailable'),
                     'evidence': 'multiple_records', 'plain_watch': plain}
        else:
            state = plain or managed or unknown_status()
    try:
        ForemanProfile(workspace).validate_completion(load_configuration(workspace))
        state['setup'] = 'complete'
    except (FactoryError, OSError):
        state['setup'] = 'incomplete'
    print(json.dumps(state))
    return 0


def _watch(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) -> int:
    if args.start or args.stop:
        return _change_managed_watch(args, workspace)
    if args.status:
        return _watch_status(workspace)

    from forgetful_factory.adapters.filesystem.watch_lease import WorkspaceWatchLease

    with WorkspaceWatchLease(workspace).hold():
        return _watch_locked(args, workspace, deadlines)


def _foreman(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) -> int:
    import uuid

    from forgetful_factory.adapters.agentshell.owner_client import (
        enter_terminal,
        read_state,
        request,
        start_owner,
    )
    from forgetful_factory.adapters.filesystem.watch_lease import WorkspaceWatchLease
    from forgetful_factory.cli.bootstrap import prepare_foreman_launch
    from forgetful_factory.configuration import load_configuration

    if args.attach:
        state = request(workspace, 'status')
    else:
        with WorkspaceWatchLease(workspace).hold():
            state = read_state(workspace)
            if state and state.get('foreman') != 'stopped':
                raise FactoryError('Foreman already exists or is uncertain; use foreman --attach '
                                   'or watch --status. The existing owner was preserved.')
            config = load_configuration(workspace)
            profile, environment, launch = prepare_foreman_launch(
                config, workspace, term_grace=deadlines.owned_process_term_grace)
            notice = profile.managed_memory_notice()
            if notice is not None:
                print(notice, flush=True)
            state = start_owner(workspace, args.agentshell_python, environment, {
                **launch, 'session_name': f'factory-foreman-{uuid.uuid4().hex[:12]}',
                'prompt': None}, deadlines.agentshell)
    if state['foreman'] != 'ready':
        raise FactoryError(state.get('warning', 'Foreman is not ready.') +
                           ' Foreman was preserved; inspect watch --status.')
    enter_terminal(state['target'])
    return 0


def _watch_locked(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) -> int:
    from contextlib import nullcontext

    from forgetful_factory.adapters.agentshell.borrowed_terminal import BorrowedForemanTerminal
    from forgetful_factory.adapters.agentshell.owner_client import read_state
    from forgetful_factory.adapters.watch_status import observe_plain_watch
    from forgetful_factory.configuration import load_configuration

    if not math.isfinite(args.interval) or args.interval <= 0:
        raise FactoryError('--interval must be positive and finite.')
    config = load_configuration(workspace)
    terminal = None
    if args.owner_fd is not None:
        terminal = BorrowedForemanTerminal(args.owner_fd)
    else:
        state = read_state(workspace)
        if state and state.get('foreman') != 'stopped':
            raise FactoryError('Setup Foreman exists or is uncertain; use watch --start '
                               f'--workspace {shlex.quote(str(workspace))} after completing setup. '
                               'No second Foreman was launched.')
    if terminal is None:
        observer = observe_plain_watch(workspace, lambda error: print(
            'Warning: watch observation unavailable: ' + _safe_diagnostic(error) +
            '; watching continues without verified observation.', file=sys.stderr, flush=True))
    else:
        observer = nullcontext()
    with observer as observation:
        application = build_watcher(
            args.agentshell_python, config, workspace, terminal, deadlines, observation)

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


def _owner_choices(args: argparse.Namespace, choices: InitialAgentChoices) -> InitialAgentChoices:
    # replace returns the same concrete dataclass type; retain that contract for static analyzers.
    return cast(InitialAgentChoices, replace(
        choices,
        feature_owner_agent_model=args.feature_owner_model or choices.foreman_agent_model,
        feature_owner_agent_effort=args.feature_owner_effort or choices.foreman_agent_effort,
        grill_me_skill=str((args.grill_me_skill or
                           Path.home() / '.agents/skills/grill-me/SKILL.md')
                          .expanduser().resolve())))


def _worker_arguments(args: argparse.Namespace) -> dict:
    supplied = {}
    for role in ('implementation', 'review'):
        for field in ('model', 'harness', 'effort'):
            value = getattr(args, f'{role}_{field}')
            if value is not None:
                supplied[f'{role}_agent_{field}'] = value
        paths = getattr(args, f'{role}_skill')
        if paths is not None:
            supplied[f'{role}_skills'] = tuple(str(path.expanduser().resolve()) for path in paths)
    if args.tdd_skill is not None:
        supplied['tdd_skill'] = str(args.tdd_skill.expanduser().resolve())
    return supplied


def _research_choices(args, config):
    supplied = {f'research_agent_{field}': getattr(args, f'research_{field}')
                for field in ('model', 'harness', 'effort')
                if getattr(args, f'research_{field}') is not None}
    if not supplied:
        return config
    return replace(config, **{
        'research_agent_model': config.feature_owner_agent_model,
        'research_agent_harness': 'pi',
        'research_agent_effort': config.feature_owner_agent_effort,
        **supplied,
    })


def _prompt_worker(role: str, discover_models) -> dict:
    harness = _select_numbered(f'{role.capitalize()} app', tuple(WORKER_EFFORTS))
    models = discover_models(harness)
    if not models:
        raise FactoryError(f'No common {harness} model catalog choices '
                           'in selected repositories.')
    model = _select_numbered(f'{role.capitalize()} model', models)
    effort = _select_numbered(f'{role.capitalize()} effort', WORKER_EFFORTS[harness])
    return {f'{role}_agent_harness': harness, f'{role}_agent_model': model,
            f'{role}_agent_effort': effort}


def _prompt_workers(discover_models) -> dict:
    print('Worker setup uses your existing native accounts. Listing may read native settings, '
          'credentials and network catalogs; no inference or model access check is made.')
    supplied = {}
    for role in ('implementation', 'review'):
        supplied.update(_prompt_worker(role, discover_models))
    return supplied


def _select_setup_route(args: argparse.Namespace) -> bool:
    print('How would you like to set up your factory?\n'
          '  1. Manual — Choose agents, models and settings through step-by-step prompts.\n'
          '  2. Foreman-assisted — Chat with Foreman, your coordinating AI agent, '
          'to finish setup together.')
    route = _select_numbered('Setup', ('Manual', 'Foreman-assisted'),
                             show_choices=False, prompt='Select 1 or 2: ')
    if route == 'Foreman-assisted':
        args.assisted = True
        return True
    args.manual_setup = True
    return False


def _prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
                                discover_models) -> InitialAgentChoices:
    if config.research_agent_harness not in (None, 'pi'):
        raise FactoryError('Factory research setup currently supports Pi only; '
                           'choose --research-harness pi before selecting its model.')
    for role, title in (('feature_owner', 'Feature-owner'), ('research', 'Research')):
        model = getattr(args, f'{role}_model')
        effort = getattr(args, f'{role}_effort')
        if model is None:
            model = _select_numbered(f'{title} model', discover_models('pi', role))
        if effort is None:
            effort = _select_numbered(f'{title} effort', WORKER_EFFORTS['pi'])
        harness = args.research_harness or 'pi' if role == 'research' else 'pi'
        config = replace(config, **{f'{role}_agent_model': model,
                                   f'{role}_agent_effort': effort,
                                   f'{role}_agent_harness': harness})
    return config


def _foreman_memory_choices(
        args: argparse.Namespace, config: InitialAgentChoices, discover_models,
        connection: ForgetfulConnection) -> InitialAgentChoices:
    enabled = args.foreman_memory is True
    model = args.foreman_memory_model
    if args.manual_setup and args.foreman_memory is None:
        try:
            enabled = _select_numbered(
                'Foreman automatic memory',
                ('Off', 'Automatic recall and capture'),
            ) == 'Automatic recall and capture'
        except EOFError:
            enabled = False
    if enabled and connection.instance != 'server':
        raise FactoryError('Foreman automatic memory requires a Forgetful server. '
                           'Local CLI planning remains available; rerun init with '
                           '--no-foreman-memory or configure an existing server.')
    if enabled and not _managed_rest_mapping_available(connection):
        raise FactoryError('Foreman automatic memory cannot derive the server REST endpoint. '
                           'Use a server root URL or an exact terminal /mcp path, or rerun with '
                           '--no-foreman-memory. Native CLI planning can still use this server '
                           'URL; Factory did not guess a REST target.')
    if enabled and model is None and args.manual_setup:
        models = discover_models()
        if not models:
            raise FactoryError('No native Pi model catalog choices are available for Foreman '
                               'automatic recall and capture.')
        model = _select_numbered('Foreman memory model', models)
    return cast(InitialAgentChoices, replace(
        config,
        foreman_memory_enabled=enabled,
        foreman_memory_model=model,
    ))


def _managed_rest_mapping_available(connection: ForgetfulConnection) -> bool:
    if connection.instance != 'server' or connection.server is None:
        return False
    path = urlsplit(connection.server).path
    return path in ('', '/') or path.endswith('/mcp')


def _worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
                    discover_models=None) -> InitialAgentChoices:
    supplied = _worker_arguments(args)
    if args.planning_only and (supplied or config.execution_enabled):
        raise FactoryError('--planning-only conflicts with explicit worker configuration.')
    interactive = not supplied and not args.planning_only and not args.assisted
    if interactive:
        if _select_setup_route(args):
            return config
        config = _prompt_coordinator_choices(args, config, discover_models)
        supplied = _prompt_workers(discover_models)
    updated = replace(config, **supplied)
    return updated


def _complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
                    workspace: Path, *, login: bool, initial: bool = False) -> None:
    print('Foreman model selected; access unverified (no model request made).')
    print(f'Factory configuration: {workspace}/.factory/factory.toml')
    print('Checking Forgetful connection and planning access...', flush=True)
    if application.profile.uses_browser_login(config.forgetful):
        print('If your browser opens, complete Forgetful sign-in there.', flush=True)
    print(application.check_foreman(config, login=login))
    memory_selected = application.profile.record_completion(config)
    if initial:
        print('Add your skills as <skill-name>/SKILL.md inside these agent folders:')
        roles = ['foreman', 'feature-owner', 'research']
        if config.execution_enabled:
            roles.extend(('implementation', 'review'))
        for role in roles:
            print(f'  {role}: {workspace}/.factory/agents/{role}/skills')
    else:
        print(f'Selected Foreman definition: {config.foreman_agent_file}')
        print('Follow agent_file references and use each agent\'s selected skills directories.')
    print('Agent settings live in agent.json. Add skills to a selected directory; '
          'reload or restart affected agents. Repeated init preserves your files.')
    notice = application.profile.managed_memory_notice()
    if notice is not None:
        print(notice)
    elif config.forgetful.instance == 'server' and not _managed_rest_mapping_available(
            config.forgetful):
        print('The managed Foreman extension reports unavailable for this server URL; '
              'no REST target was guessed. Native Factory CLI planning remains available.')
    elif config.forgetful.instance == 'server':
        definition = Path(config.foreman_agent_file)
        print('The Foreman server extension plans against the selected Forgetful project even '
              'when automatic memory is off.')
        print(f'Optional extension authentication: {definition.with_name("forgetful-auth.json")} '
              'may contain token_env naming a distinct environment variable. '
              'Factory does not create this file or copy a token; native CLI login is separate.')
    elif memory_selected:
        print('The Foreman memory extension reports unavailable for local Forgetful. '
              'Local Factory CLI planning remains available; no server is started.')


def _initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) -> int:
    from forgetful_factory.adapters.agentshell.owner_client import enter_terminal, request
    from forgetful_factory.adapters.filesystem.watch_lease import WorkspaceWatchLease

    if args.attach:
        state = request(workspace, 'status')
        if state['foreman'] != 'ready':
            raise FactoryError('Foreman is not ready; inspect watch --status '
                               f'--workspace {shlex.quote(str(workspace))}.')
        enter_terminal(state['target'])
        return 0
    with WorkspaceWatchLease(workspace).hold():
        result = _initialise_locked(args, workspace, deadlines)
    if result == 'existing':
        return 0
    if isinstance(result, dict):
        if result['foreman'] != 'ready':
            raise FactoryError(result.get('warning', 'Foreman is not ready.') +
                               ' Foreman was preserved. Inspect watch --status '
                               f'--workspace {shlex.quote(str(workspace))}.')
        enter_terminal(result['target'])
        return 0
    return _offer_factory_launch(args, workspace)


def _offer_factory_launch(args: argparse.Namespace, workspace: Path) -> int:
    from forgetful_factory.adapters.agentshell.owner_client import read_state

    state = read_state(workspace)
    if args.finalize or (state and state.get('foreman') != 'stopped'):
        return 0
    command = [sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace', str(workspace)]
    if args.agentshell_python != sys.executable:
        python = args.agentshell_python
        if '/' in python or python.startswith('~'):
            python = os.path.abspath(os.path.expanduser(python))
        command.extend(['--agentshell-python', python])
    print('\nTo start your factory later, run:\n'
          f'  {shlex.join(command)}\n\n'
          'This watches GitHub issues and sends work to Foreman.')
    if not sys.stdin.isatty():
        return 0
    try:
        answer = input('Launch factory now? [y/N]: ').strip().lower()
    except EOFError:
        print()
        return 0
    except KeyboardInterrupt:
        print('\nLaunch cancelled. Factory setup is complete; use the command above later.')
        return 130
    if answer in ('y', 'yes'):
        # Replace init only after its lease is released. Watch retains its own input and cleanup.
        os.execv(sys.executable, command)
    return 0


@dataclass
class _InitialSetupState:
    connection: ForgetfulConnection
    config: FactoryConfiguration
    prepared: bool


def _validate_setup_owner(args: argparse.Namespace, workspace: Path, state: dict | None) -> None:
    if not state or state.get('foreman') == 'stopped':
        return
    if args.assisted:
        raise FactoryError('Foreman already exists or is uncertain; use init --attach '
                           f'--workspace {shlex.quote(str(workspace))} or inspect '
                           f'watch --status --workspace {shlex.quote(str(workspace))}. '
                           'Nothing was replaced.')
    if not args.delegated_work_stopped:
        raise FactoryError('Confirm delegated work is stopped with --delegated-work-stopped '
                           'before revalidating the live setup Foreman.')


def _finish_existing_setup(application: InitialiseFactory, config: FactoryConfiguration,
                           args: argparse.Namespace, workspace: Path) -> int:
    _connection(args, workspace, config.forgetful)
    application.profile.choose_pi_home(args.pi_agent_dir,
                                       lambda home: _confirm_pi_home(home, args))
    application.profile.save_pi_choice()
    application.profile.selected_launch(config)
    for message in application.initialise(config, before_writes=lambda: None, save=False):
        print(message)
    _complete_setup(application, config, workspace, login=args.login)
    print('First setup validated. Use /reload while idle in the same conversation. '
          'Finalization does not clear delivery uncertainty.')
    return 0


def _discover_worker_models(harness, role=None, *, application: InitialiseFactory,
                            args: argparse.Namespace, workspace: Path,
                            state: _InitialSetupState):
    if not state.prepared:
        _prepare_foreman(application, state.connection, args)
        state.prepared = True
    if role is not None:
        from forgetful_factory.adapters.filesystem.resource_files import check_real_path

        directory = workspace / '.factory/agents' / role.replace('_', '-')
        check_real_path(directory)
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        return application.profile.list_models(state.connection, harness=harness, cwd=directory)
    catalogs = [set(application.profile.list_models(
        state.connection, harness=harness, cwd=Path(repository.local_dir)))
        for repository in state.config.repository]
    return sorted(set.intersection(*catalogs))


def _validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
                            choices: InitialAgentChoices, home: str, workspace: Path,
                            state: _InitialSetupState) -> FactoryConfiguration:
    if args.foreman_model is not None:
        _prepare_foreman(application, state.connection, args, prepared=state.prepared)
        _select_model(application, state.connection, home, choices.foreman_agent_model,
                      choices.feature_owner_agent_model)
    if state.connection.project_id is None:
        project_id = _select_project(application, state.connection, workspace)
        state.connection = replace(state.connection, project_id=project_id)
        state.config = replace(state.config, forgetful=state.connection)
    if state.config.execution_enabled:
        print('Checking worker model catalogs using the selected native apps/accounts. '
              'Listing may read native settings, credentials and network catalogs; '
              'it does not verify model access or model-specific effort support.')
    application.profile.prepare_roles(state.config, choices)
    return state.config


def _start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
                         workspace: Path, paths: list[Path] | None,
                         deadlines: DeadlinePolicy) -> int | dict:
    connection = _connection(args, workspace, None)
    home = application.profile.choose_pi_home(args.pi_agent_dir,
                                             lambda value: _confirm_pi_home(value, args))
    application.profile.begin_setup()
    config, choices = _configure_new_factory(
        application, workspace, args, paths, connection, home)
    state = _InitialSetupState(connection, config, args.foreman_model is None)
    choices = _research_choices(args, _owner_choices(args, choices))
    discover_models = partial(_discover_worker_models, application=application, args=args,
                              workspace=workspace, state=state)
    choices = _worker_choices(args, choices, discover_models)

    def memory_models():
        if not state.prepared:
            _prepare_foreman(application, state.connection, args)
            state.prepared = True
        return application.profile.list_models(state.connection)

    choices = _foreman_memory_choices(args, choices, memory_models, state.connection)
    validate_initial_agents(choices)
    state.config = replace(state.config, execution_enabled=choices.execution_enabled,
                           forgetful=state.connection)
    validate_model = partial(_validate_initial_model, application, args, choices, home,
                             workspace, state)
    for message in application.initialise(state.config, before_writes=validate_model):
        print(message)
    if choices.foreman_memory_enabled:
        print('Foreman automatic memory enabled for the configured Forgetful server.')
    if args.assisted:
        return _launch_setup_foreman(
            application, state.config, workspace, args, deadlines)
    _complete_setup(application, state.config, workspace, login=args.login, initial=True)
    print('\nFactory setup complete.')
    return 0


def _initialise_locked(args: argparse.Namespace, workspace: Path,
                       deadlines: DeadlinePolicy) -> int | dict | str:
    from forgetful_factory.adapters.agentshell.owner_client import read_state

    application = build_initialiser(workspace, deadlines)
    if application.storage.load() is not None and not args.finalize:
        print('Factory already initialized. Edit factory.toml and agent.json directly; '
              'reload or restart affected agents. Use init --finalize for incomplete first setup.')
        return 'existing'
    _validate_setup_owner(args, workspace, read_state(workspace))
    paths = ([Path(os.path.abspath(path.expanduser())) for path in args.repo]
             if args.repo is not None else None)
    config = application.load_existing(paths, args.label)
    if args.finalize and config is None:
        raise FactoryError('Finalization requires saved configuration. '
                           'Run init in a terminal first.')
    if config is not None:
        return _finish_existing_setup(application, config, args, workspace)
    return _start_initial_setup(application, args, workspace, paths, deadlines)


def _launch_setup_foreman(application, config, workspace, args, deadlines):
    import uuid

    from forgetful_factory.adapters.agentshell.owner_client import start_owner
    from forgetful_factory.cli.bootstrap import prepare_foreman_launch

    application.profile.prepare_setup_guidance()
    print(application.check_foreman(config, login=args.login))
    _, environment, launch = prepare_foreman_launch(
        config, workspace, complete=False,
        term_grace=deadlines.owned_process_term_grace)
    result = start_owner(workspace, args.agentshell_python, environment, {
        **launch, 'session_name': f'factory-foreman-{uuid.uuid4().hex[:12]}', 'prompt': None},
        deadlines.agentshell)
    print('Setup is incomplete. Review the starter team with Foreman, then run '
          'init --finalize --delegated-work-stopped '
          f'--workspace {shlex.quote(str(workspace))}. Use /reload after finalization.')
    return result


def main(deadlines: DeadlinePolicy = DeadlinePolicy()) -> int:
    args = _parse_arguments()
    try:
        workspace = args.workspace.expanduser().resolve()
        if not workspace.is_dir():
            raise FactoryError(f'Workspace must be an existing directory: {workspace}')
        if args.command == 'watch':
            return _watch(args, workspace, deadlines)
        if args.command == 'foreman':
            return _foreman(args, workspace, deadlines)
        return _initialise(args, workspace, deadlines)
    except EOFError:
        message = ('For noninteractive watch provide --existing or --new-only.'
                   if args.command == 'watch' else
                   'For noninteractive init provide --repo, --label, '
                   '--foreman-model, --foreman-effort, --forgetful-instance, '
                   'and --share-pi-profile. '
                   'Choose --planning-only or provide complete worker settings. '
                   'Run init in a terminal for required setup prompts or installation consent. '
                   'Forgetful access is always checked; '
                   'server checks may open browser sign-in. '
                   'Existing saved setup is kept; rerun init to retry.')
        print(f'Error: Input ended. {message}', file=sys.stderr)
        return 1
    except KeyboardInterrupt as error:
        message = f'Error: {args.command.capitalize()} interrupted.'
        if str(error):
            message += ' ' + _safe_diagnostic(str(error))
        elif args.command == 'init':
            message += (' Setup is incomplete; rerun init if no configuration was saved, '
                        'otherwise use init --finalize.')
        print(message, file=sys.stderr)
        return 130
    except (FactoryError, OSError) as error:
        print(f'Error: {_safe_diagnostic(str(error))}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
