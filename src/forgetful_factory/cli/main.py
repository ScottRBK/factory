import argparse
import os
from pathlib import Path
import sys

from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.cli.bootstrap import build_initialiser
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


def main() -> int:
    args = _parse_arguments()
    try:
        workspace = args.workspace.expanduser().resolve()
        if not workspace.is_dir():
            raise FactoryError(f'Workspace must be an existing directory: {workspace}')
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
        print('Error: Input ended. For noninteractive init provide --repo, --label, '
              '--foreman-model, and --foreman-effort.', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('Error: Initialization interrupted.', file=sys.stderr)
        return 130
    except (FactoryError, OSError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
