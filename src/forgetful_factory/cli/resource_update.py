import argparse
from pathlib import Path

from forgetful_factory.deadlines import DeadlinePolicy
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
    from forgetful_factory.adapters.agentshell.owner_client import read_state
    from forgetful_factory.adapters.filesystem.foreman_profile import ForemanProfile
    from forgetful_factory.adapters.filesystem.role_resources import apply_update, plan_update
    from forgetful_factory.adapters.filesystem.watch_lease import WorkspaceWatchLease

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
        profile = ForemanProfile(workspace, deadlines.owned_process_term_grace)
        profile.validate_bundled_resources(include_memory_extension=True)
        print('Role resources match the installed Factory bundle.')
        if not profile.role_runtime_ready():
            if args.no_install_role_runtime:
                raise FactoryError('The AgentShell runtime does not match its bundled lock, so '
                                   'Foreman cannot start. Rerun update without '
                                   '--no-install-role-runtime to install the locked runtime.')
            profile.install('agentshell-runtime')
            if not profile.role_runtime_ready():
                raise FactoryError('The AgentShell runtime is still not ready after installation.')
    print('Start Foreman or watch to load the updated resources.')
    return 0
