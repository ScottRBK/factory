import argparse
import math
import os
import signal
import sys
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration
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
                           args: argparse.Namespace, paths: list[Path] | None
                           ) -> FactoryConfiguration:
    if paths is None:
        paths = select_repositories(application, workspace)
        for reference in application.inspect(paths).values():
            print(f'{reference.local_dir} -> {reference.remote}')
        if input('Confirm these GitHub origins? [y/N]: ').strip().lower() != 'y':
            raise FactoryError('Initialization cancelled; no labels or config changed.')
    labels = args.label if args.label is not None else input(
        'Watched labels (comma-separated, or *): ').split(',')
    model = args.foreman_model if args.foreman_model is not None else input(
        'Foreman model (provider/model): ')
    effort = args.foreman_effort if args.foreman_effort is not None else input(
        'Foreman effort: ')
    return application.configure(paths, labels, model, effort)


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


def main() -> int:
    args = _parse_arguments()
    try:
        workspace = args.workspace.expanduser().resolve()
        if not workspace.is_dir():
            raise FactoryError(f'Workspace must be an existing directory: {workspace}')
        if args.command == 'watch':
            return _watch(args, workspace)
        application = build_initialiser(workspace)
        paths = ([Path(os.path.abspath(path.expanduser())) for path in args.repo]
                 if args.repo is not None else None)
        config = application.load_existing(paths, args.label, args.foreman_model,
                                           args.foreman_effort)
        existing = config is not None
        if config is None:
            config = _configure_new_factory(application, workspace, args, paths)
        for message in application.initialise(config, save=not existing):
            print(message)
        print(f'Factory configuration: {workspace}/.factory/factory.toml')
        return 0
    except EOFError:
        message = ('For noninteractive watch provide --existing or --new-only.'
                   if args.command == 'watch' else
                   'For noninteractive init provide --repo, --label, '
                   '--foreman-model, and --foreman-effort.')
        print(f'Error: Input ended. {message}', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f'Error: {args.command.capitalize()} interrupted.', file=sys.stderr)
        return 130
    except (FactoryError, OSError) as error:
        print(f'Error: {_safe_diagnostic(str(error))}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
