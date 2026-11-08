"""Set up a human agreement, not a machine-interpreted completion policy."""
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import check_skill_file, write_new
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.domain.models import FactoryError


def agree_definition_of_done(workspace: Path, config: FactoryConfiguration) -> bool:
    """Return True when setup needs a Foreman conversation instead of finalization."""
    path = workspace / '.factory/definition_of_done.md'
    print('Automatic cleanup deletes completed-plan worktrees, including changed, untracked and\n'
          'ignored files, and recorded local/remote feature branches, including extra commits.\n'
          'Completion authorizes disposal without another prompt or recoverable trash. Save\n'
          'required evidence outside worktrees first; never reuse completed-plan resources.')
    if path.exists() or path.is_symlink():
        check_skill_file(path)
        print(f'Preserved Definition of Done: {path}. Foreman must read it before feature work.')
        return False
    print('Definition of Done: a shared agreement, separate from feature acceptance criteria.\n'
          'Starting points (not a list of all possible agreements):\n'
          '  1. After merge\n'
          '  2. After merge and deployment\n'
          '  3. After merge, deployment and deployed E2E\n'
          '  4. Discuss with Foreman')
    answer = input('Select Definition of Done number (no default): ').strip()
    if answer == '4':
        print('No agreement saved. Discuss requirements and prerequisites with Foreman, then\n'
              'confirm and save this Markdown file before finalizing setup or handing off work.')
        return True
    if answer not in ('1', '2', '3'):
        raise FactoryError('Select a Definition of Done starting point; there is no default.')
    repositories = '\n'.join(f'- {repo.work_source.reference}' for repo in config.repository)
    text = ('# Definition of Done\n\n'
            'This agreement covers these repositories in this Factory workspace:\n'
            f'{repositories}\n\n'
            'Feature-specific plan acceptance criteria must also be met.\n'
            'Independent review, required repository/PR checks and confirmed merge are required.\n'
            'Foreman checks the PR, actual merge commit, review and exact-final-revision check\n'
            'results before completing the plan after the feature-owner handoff.\n')
    if answer == '1':
        text += 'Deployment and deployed E2E are not completion requirements.\n'
    else:
        text += _deployment_agreement(answer)
    print(f'\nProposed agreement at {path}:\n{text}')
    if input('Save this Definition of Done agreement? [y/N]: ').strip().lower() != 'y':
        raise FactoryError('Definition of Done not saved. Discuss requirements with Foreman; '
                           'setup is incomplete. Use init --finalize for saved setup.')
    write_new(path, text)
    if path.read_text(encoding='utf-8') != text:
        raise FactoryError('A different Definition of Done was saved during confirmation. '
                           'The file is preserved; discuss it with Foreman before finalizing.')
    print(f'Saved Definition of Done: {path}')
    return False


def _deployment_agreement(answer: str) -> str:
    """Ask for deployment prerequisites and draft their agreement section."""
    environment = input('Deployment environment name: ').strip()
    workflow = input('Post-merge deployment workflow name (per repository if needed): ').strip()
    if not environment or not workflow:
        raise FactoryError('Name the deployment environment and workflow, or discuss with '
                           'Foreman. No agreement was saved.')
    text = (f'Deployment to {environment} through {workflow} is required. Foreman verifies\n'
            'successful stages and revision evidence for the actual merged revision in each\n'
            'affected repository. Record workflow run/attempt and artifact links in tasks.\n'
            'Missing, failed, skipped, pending or inconclusive required evidence blocks\n'
            'completion. Keep the plan open and raise or reuse a linked follow-up issue.\n')
    if answer == '2':
        text += 'Deployed E2E is not a completion requirement.\n'
    else:
        text += ('Deployed E2E must pass after deployment succeeds, against this isolated\n'
                 'environment, not just a checkout server. Record run/attempt and artifact\n'
                 'links identifying the actual deployed repository combination tested.\n')
    print('This requires a usable post-merge deployment workflow and deployed-revision\n'
          'evidence in the named environment. Setup has not checked them. If missing or\n'
          'unclear, do not confirm: discuss prerequisites with Foreman first.')
    if answer == '3':
        print('Deployed E2E also needs an isolated test environment and a workflow stage\n'
              'after deployment with evidence of the deployed combination it tested.')
    return text
