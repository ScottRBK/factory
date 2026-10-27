from forgetful_factory.deadlines import DeadlinePolicy


def programmatic_factory(policy: DeadlinePolicy) -> list[str]:
    lifecycle = policy.agentshell
    code = (
        'from forgetful_factory.cli.main import main;'
        'from forgetful_factory.deadlines import DeadlinePolicy,AgentShellLifecycleDeadlines;'
        'policy=DeadlinePolicy('
        f'external_command={policy.external_command!r},'
        f'owned_process_term_grace={policy.owned_process_term_grace!r},'
        'agentshell=AgentShellLifecycleDeadlines('
        + ','.join(
            f'{name}={getattr(lifecycle, name)!r}'
            for name in (
                'controller_ready',
                'controller_send',
                'controller_close',
                'parent_ready',
                'owner_watcher_start',
                'owner_watcher_stop',
                'owner_ready',
                'owner_controller_close',
                'owner_pre_adoption_cleanup',
            )
        )
        + '));raise SystemExit(main(policy))'
    )
    return ['-c', code]
