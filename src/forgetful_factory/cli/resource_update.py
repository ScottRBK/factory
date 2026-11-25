import argparse
from pathlib import Path

from forgetful_factory.cli.deadlines import DeadlinePolicy
from forgetful_factory.shared.errors import FactoryError


def _report(update, force: bool) -> None:
    """Print each planned change; refuse edited files unless forced."""
    for action, members in (('add', update.add), ('replace', update.replace),
                            ('edited', update.edited)):
        for member in members:
            print(f'{action:<8} {member}')
    print(f'{len(update.files)} bundled files: {len(update.add)} to add, '
          f'{len(update.replace)} to replace, {len(update.edited)} edited.')
    if update.edited and not force:
        raise FactoryError('Edited bundled files: ' + ', '.join(update.edited) +
                           '. Reconcile them with the bundle, or rerun with --force to '
                           'back them up and replace them. Nothing was changed.')


def update_resources(args: argparse.Namespace, workspace: Path,
                     deadlines: DeadlinePolicy) -> int:
    from forgetful_factory.agents.adapters.agentshell.owner_client import read_state
    from forgetful_factory.agents.adapters.agentshell.runtime_install import (
        AgentShellRuntimeInstall,
    )
    from forgetful_factory.agents.adapters.pi.role_resources import apply_update, plan_update
    from forgetful_factory.cli.bootstrap import build_team
    from forgetful_factory.factory.adapters.watch_lease import WorkspaceWatchLease

    directory = workspace / '.factory/resources'
    if not directory.is_dir():
        raise FactoryError(f'No factory role resources in {workspace}; run init first.')
    if args.dry_run:
        # A read-only preview takes no lease, so it also works while the factory runs.
        update = plan_update(directory)
        print('Dry run: nothing was changed.')
        _report(update, args.force)
        return 0
    with WorkspaceWatchLease(workspace).hold():
        state = read_state(workspace)
        if state and state.get('foreman') != 'stopped':
            raise FactoryError('Foreman is running or uncertain; close it (see watch --status), '
                               'then rerun update. Nothing was changed.')
        update = plan_update(directory)
        _report(update, args.force)
        backup = apply_update(update, workspace / '.factory/resource-backups')
        if backup is not None:
            print(f'Edited files were backed up under {backup}')
        term_grace = deadlines.owned_process_term_grace
        build_team(workspace, term_grace).validate_bundled_resources(
            include_memory_extension=True)
        print('Role resources match the installed Factory bundle.')
        runtime = AgentShellRuntimeInstall(workspace, term_grace)
        if not runtime.ready():
            if args.no_install_role_runtime:
                raise FactoryError('The AgentShell runtime does not match its bundled lock, so '
                                   'Foreman cannot start. Rerun update without '
                                   '--no-install-role-runtime to install the locked runtime.')
            runtime.install('agentshell-runtime')
            if not runtime.ready():
                raise FactoryError('The AgentShell runtime is still not ready after installation.')
    print('Start Foreman or watch to load the updated resources.')
    return 0
