# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 72 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 3407. Type relationships removed: 52.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/lifecycle_support.py`: 21 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_agent_definitions.py`: 21 source occurrences (test-path).
- `tests/test_architecture.py`: 12 source occurrences (test-path).
- `tests/test_assisted_lifecycle.py`: 16 source occurrences (test-path).
- `tests/test_assisted_review_fixes.py`: 20 source occurrences (test-path).
- `tests/test_assisted_setup.py`: 15 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_cleanup_recovery.py`: 14 source occurrences (test-path).
- `tests/test_configuration.py`: 14 source occurrences (test-path).
- `tests/test_factory_maintenance.py`: 8 source occurrences (test-path).
- `tests/test_foreman_setup_repair.py`: 31 source occurrences (test-path).
- `tests/test_init.py`: 43 source occurrences (test-path).
- `tests/test_init_launch.py`: 13 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 20 source occurrences (test-path).
- `tests/test_local_skills.py`: 21 source occurrences (test-path).
- `tests/test_managed_watcher_alerts.py`: 10 source occurrences (test-path).
- `tests/test_native_assisted_reload.py`: 2 source occurrences (test-path).
- `tests/test_native_roles.py`: 4 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_normalized_lifecycle.py`: 8 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_planning_setup.py`: 13 source occurrences (test-path).
- `tests/test_planning_watch.py`: 29 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_review_regressions.py`: 56 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 23 source occurrences (test-path).
- `tests/test_watch.py`: 52 source occurrences (test-path).
- `tests/test_watch_lock.py`: 6 source occurrences (test-path).
- `tests/test_watcher_alerts.py`: 62 source occurrences (test-path).
- `tests/test_watcher_cancellation.py`: 5 source occurrences (test-path).
- `tests/test_watcher_followup.py`: 35 source occurrences (test-path).
- `tests/test_watcher_guidance.py`: 4 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 18 source occurrences (test-path).
- `tests/test_worker_profiles.py`: 8 source occurrences (test-path).
- `tests/test_worker_setup.py`: 15 source occurrences (test-path).
- `tests/test_worker_watch_permissions.py`: 6 source occurrences (test-path).
- `tests/worker_support.py`: 2 source occurrences (test-path).

## Diagram 1

```mermaid
classDiagram
    direction TB
    class c0000["BorrowedForemanTerminal"] {
        <<class>>
        -__init__(descriptor: int) unknown
        +connection: unknown
        +reader: unknown
        +startup_hint() str
        -_request(value: dict) None
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0001["SessionState"] {
        <<class>>
        +session: Type1
        +worker: Type2
        +worker_error: Type3
        +cleanup_known: bool
    }
    class c0002["src/forgetful_factory/adapters/agentshell/controller.py"] {
        <<module>>
        +ready(session: unknown) None
        +interact(Signature1)
        +retain_identity(session: unknown, reply: unknown) None
        +pin_worker(target: unknown) int
        +worker_exited(descriptor: unknown) None
        +resume_exit_observation(session: unknown) int
        +runtime() unknown
        +validate_launch_config(config: unknown) None
        +build_shell(config: unknown) unknown
        +open_session(Signature2)
        +capture_worker(state: unknown, reply: unknown) None
        +replace_failed_exit_task(Signature3)
        +cancel_tasks(tasks: unknown) None
        +supervise_session(Signature4)
        +close_session(state: unknown, config: unknown, reply: unknown) None
        +serve(reader: unknown, config: unknown, reply: unknown, opened: unknown) None
        +control(reply: unknown) None
        +main(reply: unknown) int
        +reply(value: unknown) unknown
    }
    class c0003["src/forgetful_factory/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0004["ForemanOwner"] {
        <<class>>
        -__init__(workspace: Path, python: str, directory: Path) unknown
        +workspace: unknown
        +python: unknown
        +directory: unknown
        +state: unknown
        +controller: unknown
        +ready: unknown
        +stopped: unknown
        +watcher: unknown
        +watcher_done: unknown
        +watcher_ready: unknown
        +channel: unknown
        +delivery: unknown
        +sent: unknown
        +delivery_error: unknown
        +spawned: unknown
        +save() unknown
        -_validate_readiness(value: unknown) None
        -_reject_controller_event(error: unknown) None
        +state#91;#39;foreman#39;#93;: unknown
        +state#91;#39;warning#39;#93;: unknown
        -_apply_controller_problem(value: unknown) None
        -_apply_controller_event(value: unknown) None
        +state#91;#39;target#39;#93;: unknown
        -_finish_observation() None
        +observe() unknown
        -_relay_request(value: unknown) None
        +state#91;#39;watcher#39;#93;: unknown
        +relay(reader: unknown, writer: unknown) unknown
        +reap_watcher(child: unknown, relay: unknown) unknown
        +start_watcher(value: unknown) unknown
        +stop_watcher() unknown
        +control(reader: unknown, writer: unknown) unknown
        -_start_controller(reader: unknown) unknown
        -_await_readiness(disconnected: unknown) None
        -_complete_handover(writer: unknown, disconnected: unknown) None
        -_close_controller(observer: unknown) None
        -_remove_control_socket(Signature5)
        -_cleanup(Signature6)
        +run(handover: unknown, endpoint: unknown) unknown
    }
    class c0005["src/forgetful_factory/adapters/agentshell/owner.py"] {
        <<module>>
        -_validate_target(target: unknown) None
        -_controller_event(line: bytes) dict
        -_watcher_request(line: bytes) dict
        -_acquire_owner_lock(directory: Path, workspace: Path) int
        -_prepare_owner_startup(workspace: Path) Type4
        +main(Signature7)
        -_report_startup_error(handover: unknown, error: unknown) None
        +entrypoint() None
    }
    class c0006["src/forgetful_factory/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type5
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(workspace: Path, python: str, environment: dict, launch: dict) dict
        +enter_terminal(target: dict) None
    }
    class c0007["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature8)
        +python: unknown
        +environment: unknown
        +resources: unknown
        +prompt: unknown
        +cwd: unknown
        +model: unknown
        +effort: unknown
        +process: Type7
        +buffer: unknown
        +session_name: unknown
        +startup_hint() str
        -_write(value: dict, timeout: float) None
        -_read(timeout: float, expected: str) dict
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0008["src/forgetful_factory/adapters/command.py"] {
        <<module>>
        +run_command(arguments: list[str]) str
    }
    class c0009["src/forgetful_factory/adapters/filesystem/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        -_local_selection(value: object, field: str, message: str) str
        -_validate_agent(value: object) dict
        -_validate_roster(path: Path, value: object, agent_type: str) None
        -_validate_resources(value: object) None
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0010["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(config: FactoryConfiguration, choices: unknown) None
        -_write_agent(Signature9)
        +validate_guidance(config: FactoryConfiguration) None
    }
    class c0011["src/forgetful_factory/adapters/filesystem/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0012["ForemanProfile"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type5
        -_model_catalogs: Type8
        +prepare_setup_guidance() None
        +missing_executables(connection: ForgetfulConnection) list[str]
        +validate_setup(connection: ForgetfulConnection, include_home_system_prompt: bool) None
        +validate_bundled_resources() None
        +installation(command: str) Type3
        +install(command: str) None
        -_install_resources() None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection, execution_enabled: bool) str
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        -_protect_runtime() None
        +prepare(connection: ForgetfulConnection) None
        +save_pi_choice() None
        +prepare_roles(config: unknown, choices: unknown) None
        +validate_worker_models(config: FactoryConfiguration, choices: unknown) None
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type9) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(config: FactoryConfiguration) dict
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
        +validate_completion(_config: FactoryConfiguration) None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0013["src/forgetful_factory/adapters/filesystem/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0014["GitRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0015["src/forgetful_factory/adapters/filesystem/git_repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0016["GitWorktrees"] {
        <<class>>
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type10
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type11
        -_validate_registered_worktree(Signature10)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
    }
    class c0017["src/forgetful_factory/adapters/filesystem/git_worktrees.py"] {
        <<module>>
        -_read_git(arguments: list[str]) str
        -_worktree_entries(output: str) list[dict]
    }
    class c0018["src/forgetful_factory/adapters/filesystem/resource_files.py"] {
        <<module>>
        +check_real_path(path: Path) None
        +check_skill_file(path: Path) None
        +write_new(path: Path, content: str) None
        +write_json(path: Path, value: dict) None
        +write_definition(path: Path, value: dict) None
        -_generated_parent(path: Path) unknown
        +remove_generated(path: Path) None
        +replace_generated_json(path: Path, value: dict) None
        +read_generated_json(path: Path) dict
    }
    class c0019["src/forgetful_factory/adapters/filesystem/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type12) None
        -_walk_skill_directory(directory: Path, ancestors: Type13, files: Type12) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0020["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type14
        +save(configuration: FactoryConfiguration) None
    }
    class c0021["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0022["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0023["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0024["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0025["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +role: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type15
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0026["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature11)
        -_catalog_tools(catalog: object) dict
    }
    class c0027["ForgetfulPlanning"] {
        <<class>>
        -__init__(Signature12)
        +cli: unknown
        +connection: unknown
        +execution_enabled: unknown
        +check() None
        -_call(tool: str, fields: unknown) dict
        -_read(tool: str, fields: unknown) dict
        +plans(external_ref: Type3) list[dict]
        -_rows(result: dict, key: str) list[dict]
        +get_plan(plan_id: int) dict
        +create_plan(fields: unknown) dict
        +update_plan(plan_id: int, fields: unknown) dict
        +tasks(plan_id: int) list[dict]
        -_task(task_id: int, plan_id: int) dict
        +create_task(fields: unknown) dict
        +update_task(task_id: int, fields: unknown) dict
    }
    class c0028["src/forgetful_factory/adapters/forgetful/planning.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0029["GitHubWorkTracking"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type16
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type18) Type17
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0030["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +runtime: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type6) Type15
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type6) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0031["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type19) str
        +runtime_ready(runtime: Path, inputs: Type19, probe: str) bool
    }
    class c0032["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen) None
        +run_owned(args: list[str], cwd: Path, env: Type15, login: bool, timeout: Type20) str
    }
    class c0033["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type18
        +foreman_agent_file: str
        +repository: Type21
        +forgetful: Type22
        +execution_enabled: bool
    }
    class c0034["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type3
        +server: Type3
        +project_id: Type2
        +validate() None
        -_validate_server() None
    }
    class c0035["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type22
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type18
    }
    class c0036["InitialAgentChoices"] {
        <<class>>
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +feature_owner_agent_model: Type3
        +feature_owner_agent_effort: Type3
        +feature_owner_agent_harness: str
        +grill_me_skill: Type3
        +implementation_agent_model: Type3
        +implementation_agent_harness: Type3
        +implementation_agent_effort: Type3
        +review_agent_model: Type3
        +review_agent_harness: Type3
        +review_agent_effort: Type3
        +tdd_skill: Type3
        +implementation_skills: Type18
        +review_skills: Type18
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0037["src/forgetful_factory/application/initial_agent_choices.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type18
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0038["InitialiseFactory"] {
        <<class>>
        -__init__(Signature13)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type23, confirm: Type24) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type25, labels: Type26) Type14
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type27
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type28
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type29, save: bool) list[str]
    }
    class c0039["ConfigurationStore"] {
        <<class>>
        +load() Type14
        +save(configuration: FactoryConfiguration) None
    }
    class c0040["ForemanProfile"] {
        <<class>>
        +prepare_roles(config: FactoryConfiguration, choices: InitialAgentChoices) None
        +selected_launch(config: FactoryConfiguration) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +prepare(connection: ForgetfulConnection) None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection, execution_enabled: bool) str
        +missing_executables(connection: ForgetfulConnection) list[str]
        +installation(command: str) Type3
        +install(command: str) None
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +save_pi_choice() None
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type9) list[str]
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
    }
    class c0041["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0042["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0043["Planning"] {
        <<class>>
        +check() None
        +plans(external_ref: Type3) list[dict]
        +get_plan(plan_id: int) dict
        +create_plan(fields: unknown) dict
        +update_plan(plan_id: int, fields: unknown) dict
        +tasks(plan_id: int) list[dict]
        +create_task(fields: unknown) dict
        +update_task(task_id: int, fields: unknown) dict
    }
    class c0044["PlanningReadError"] {
        <<class>>
    }
    class c0045["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0046["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0047["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type3) unknown
        +code: unknown
        +paths: unknown
    }
    class c0048["WorktreeReadError"] {
        <<class>>
    }
    class c0049["Worktrees"] {
        <<class>>
        +inspect(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
    }
    class c0050["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature14)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +repositories: unknown
        +sources: unknown
        +check() None
        +check_repository(repository: RepositoryReference) None
        -_check_source(repository: RepositoryReference) None
        +prepare(issue: Issue) Type5
        -_repository(source: WorkSource) RepositoryReference
        -_initial_mappings(issue: Issue) list[dict]
        +preflight(issue: Issue) None
        -_prepare_plan(issue: Issue, plan: dict) Type5
        -_setup_ownership(plan_id: int, issue: Issue, context: dict) Type30
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature15)
        +lookup(issue: Issue) Type2
        -_create_plan(issue: Issue) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type32, task_ids: Type33) Type31
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature16)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_snapshot(context: dict, external_ref: str) Issue
        -_is_unfinished_factory_plan(summary: dict, sources: set[str]) bool
        -_active(plan: dict) bool
        -_context(plan: dict) dict
        -_ownership(plan_id: int, external_ref: str) list[dict]
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_mapping_repository(mapping: dict, seen: set[str]) RepositoryReference
        -_ensure_validated_mapping(Signature17)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0051["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        -_cleanup_state(mapping: dict) Type3
    }
    class c0052["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type2
        +issue: Type32
        +task_ids: Type33
        +recovered: bool
        +setup_paths: Type18
        +setup_cause: Type3
    }
    class c0053["WatchFactory"] {
        <<class>>
        -__init__(Signature18)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +run(Signature19)
        -_watch(Signature20)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type36) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature21)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type36) Type37
        -_recover_work(Signature22)
        -_handle_recovery_repository_problem(Signature23)
        -_handle_recovery_read_problem(Signature24)
        -_remember_task_ids(work: BlockedWork, task_ids: Type33) None
        -_complete_recovery(Signature25)
        -_poll_sources(Signature26)
        -_process_source(Signature27)
        -_baseline_source(Signature28)
        -_repository_for_source(Signature29)
        -_include_pending_lookups(Signature30)
        -_process_issues(Signature31)
        -_skip_issue(issue: Issue, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature32)
        -_handle_intake_repository_problem(Signature33)
        -_handle_intake_read_problem(Signature34)
        -_handle_intake_scaffold_problem(Signature35)
        -_complete_intake(Signature36)
        -_sole_task_id(task_ids: Type33) Type2
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature37)
        -_read_issues(source: WorkSource, labels: Type18, alerts: WatcherAlerts) Type41
    }
    class c0054["_WatchState"] {
        <<class>>
        +seen: Type15
        +baseline: Type15
        +baselined: set[WorkSource]
        +blocked: Type42
        +pending_lookup: Type39
        +known: Type42
        +recovered: set[str]
        +pending_repositories: Type27
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0055["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0056["IntakeProblem"] {
        <<class>>
    }
    class c0057["RepositoryProblem"] {
        <<class>>
    }
    class c0058["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature38)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0059["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0060["UncertainScaffold"] {
        <<class>>
    }
    class c0061["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type15
        +last_diagnostic: Type15
        +clear(subject: str) None
        +send(Signature39)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0062["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path) InitialiseFactory
        +build_watcher(Signature40)
        +prepare_foreman_launch(Signature41)
    }
    class c0063["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0064["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature42)
        -_check_existing_connection(Signature43)
        -_connection(Signature44)
        -_prepare_foreman(Signature45)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type44, show_choices: bool, prompt: Type3) str
        -_select_model(Signature46)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_change_managed_watch(args: argparse.Namespace, workspace: Path) int
        -_watch_status(workspace: Path) int
        -_watch(args: argparse.Namespace, workspace: Path) int
        -_foreman(args: argparse.Namespace, workspace: Path) int
        -_watch_locked(args: argparse.Namespace, workspace: Path) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature47)
        -_owner_choices(Signature48)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature49)
        -_worker_choices(Signature50)
        -_complete_setup(Signature51)
        -_initialise(args: argparse.Namespace, workspace: Path) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type5) None
        -_finish_existing_setup(Signature52)
        -_discover_worker_models(Signature53)
        -_validate_initial_model(Signature54)
        -_start_initial_setup(Signature55)
        -_initialise_locked(args: argparse.Namespace, workspace: Path) Type46
        -_launch_setup_foreman(Signature56)
        +main() int
    }
    class c0065["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type47) FactoryConfiguration
    }
    class c0066["FactoryError"] {
        <<class>>
    }
    class c0067["Issue"] {
        <<class>>
        +source: WorkSource
        +number: int
        +title: str
        +url: str
        +body: str
        +revision: str
        +epic: bool
        +id: str
    }
    class c0068["Label"] {
        <<class>>
        +name: str
    }
    class c0069["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0070["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0071["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type16
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type18) Type17
    }
    c0000 ..> c0000 : 2 relationships (see list)
    c0000 ..> c0007 : close() calls close()
    c0000 ..> c0066 : 2 relationships (see list)
    c0002 ..> c0000 : 6 relationships (see list)
    c0002 ..> c0001 : serve() constructs SessionState
    c0002 ..> c0002 : 17 relationships (see list)
    c0002 ..> c0027 : 4 relationships (see list)
    c0003 ..> c0012 : main() calls list_models()
    c0004 ..> c0000 : 11 relationships (see list)
    c0004 ..> c0004 : 27 relationships (see list)
    c0004 ..> c0005 : 2 relationships (see list)
    c0004 ..> c0018 : save() calls replace_generated_json()
    c0004 ..> c0021 : _apply_controller_problem() calls quote()
    c0004 ..> c0027 : 2 relationships (see list)
    c0004 ..> c0066 : 10 relationships (see list)
    c0005 ..> c0000 : 3 relationships (see list)
    c0005 ..> c0004 : 3 relationships (see list)
    c0005 ..> c0005 : 5 relationships (see list)
    c0005 ..> c0006 : _prepare_owner_startup() calls read_state()
    c0005 ..> c0013 : _prepare_owner_startup() calls runtime_directory()
    c0005 ..> c0021 : _acquire_owner_lock() calls quote()
    c0005 ..> c0027 : main() calls create_task()
    c0005 ..> c0066 : 3 relationships (see list)
    c0006 ..> c0000 : 2 relationships (see list)
    c0006 ..> c0004 : 2 relationships (see list)
    c0006 ..> c0006 : 3 relationships (see list)
    c0006 ..> c0013 : 3 relationships (see list)
    c0006 ..> c0018 : read_state() calls read_generated_json()
    c0006 ..> c0021 : request() calls quote()
    c0006 ..> c0066 : 5 relationships (see list)
    c0007 ..> c0000 : close() calls close()
    c0007 ..> c0007 : 5 relationships (see list)
    c0007 ..> c0066 : 4 relationships (see list)
    c0008 ..> c0004 : run_command() calls run()
    c0008 ..> c0066 : run_command() constructs FactoryError
    c0009 ..> c0009 : 8 relationships (see list)
    c0009 ..> c0035 : 4 relationships (see list)
    c0009 ..> c0066 : 2 relationships (see list)
    c0010 ..> c0010 : 2 relationships (see list)
    c0010 ..> c0011 : prepare() calls selected_resources()
    c0010 ..> c0012 : prepare() calls prepare()
    c0010 ..> c0018 : 3 relationships (see list)
    c0010 ..> c0023 : __init__() constructs WorkerProfiles
    c0010 ..> c0033 : 2 relationships (see list)
    c0010 ..> c0066 : 3 relationships (see list)
    c0012 ..> c0009 : selected_launch() calls foreman_launch()
    c0012 ..> c0010 : 4 relationships (see list)
    c0012 ..> c0012 : 22 relationships (see list)
    c0012 ..> c0018 : 11 relationships (see list)
    c0012 ..> c0019 : selected_launch() calls selected_skill_files()
    c0012 ..> c0021 : require_pi_home() calls quote()
    c0012 ..> c0024 : uses_browser_login() calls uses_browser_login()
    c0012 ..> c0025 : 8 relationships (see list)
    c0012 ..> c0026 : list_models() calls role_environment()
    c0012 ..> c0030 : 6 relationships (see list)
    c0012 ..> c0031 : 3 relationships (see list)
    c0012 ..> c0032 : list_models() calls run_owned()
    c0012 ..> c0033 : 4 relationships (see list)
    c0012 ..> c0034 : 9 relationships (see list)
    c0012 ..> c0066 : 14 relationships (see list)
    c0013 ..> c0018 : runtime_directory() calls check_real_path()
    c0013 ..> c0066 : runtime_directory() constructs FactoryError
    c0014 ..> c0008 : origin() calls run_command()
    c0014 ..> c0015 : origin() calls _resolve_repository()
    c0014 ..> c0066 : origin() constructs FactoryError
    c0015 ..> c0066 : _resolve_repository() constructs FactoryError
    c0016 ..> c0008 : ensure() calls run_command()
    c0016 ..> c0016 : 9 relationships (see list)
    c0016 ..> c0017 : 5 relationships (see list)
    c0016 ..> c0047 : 6 relationships (see list)
    c0016 ..> c0048 : 3 relationships (see list)
    c0016 ..> c0066 : ensure() constructs FactoryError
    c0017 ..> c0008 : _read_git() calls run_command()
    c0017 ..> c0048 : _read_git() constructs WorktreeReadError
    c0018 ..> c0000 : 2 relationships (see list)
    c0018 ..> c0018 : 9 relationships (see list)
    c0018 ..> c0020 : read_generated_json() calls load()
    c0018 ..> c0066 : 6 relationships (see list)
    c0019 ..> c0000 : _add_skill_file() calls close()
    c0019 ..> c0019 : 3 relationships (see list)
    c0019 ..> c0066 : 3 relationships (see list)
    c0020 ..> c0000 : 2 relationships (see list)
    c0020 ..> c0021 : save() calls quote()
    c0020 ..> c0033 : 2 relationships (see list)
    c0020 ..> c0035 : load() calls from_mapping()
    c0020 ..> c0039 : load() calls load()
    c0020 ..> c0066 : 2 relationships (see list)
    c0022 ..> c0000 : _hold_directory() calls close()
    c0022 ..> c0022 : hold() calls _hold_directory()
    c0022 ..> c0066 : _hold_directory() constructs FactoryError
    c0023 ..> c0018 : 3 relationships (see list)
    c0023 ..> c0036 : type in prepare
    c0024 ..> c0006 : uses_browser_login() calls request()
    c0024 ..> c0034 : type in uses_browser_login
    c0025 ..> c0025 : 7 relationships (see list)
    c0025 ..> c0026 : 2 relationships (see list)
    c0025 ..> c0032 : 2 relationships (see list)
    c0025 ..> c0034 : 7 relationships (see list)
    c0025 ..> c0066 : 5 relationships (see list)
    c0026 ..> c0031 : role_environment() calls executable_path()
    c0026 ..> c0034 : type in role_environment
    c0027 ..> c0012 : check() calls check()
    c0027 ..> c0025 : 2 relationships (see list)
    c0027 ..> c0027 : 12 relationships (see list)
    c0027 ..> c0028 : 3 relationships (see list)
    c0027 ..> c0034 : type in __init__
    c0027 ..> c0044 : 4 relationships (see list)
    c0029 ..> c0008 : _api() calls run_command()
    c0029 ..> c0029 : 5 relationships (see list)
    c0029 ..> c0066 : 7 relationships (see list)
    c0029 ..> c0067 : 2 relationships (see list)
    c0029 ..> c0068 : 3 relationships (see list)
    c0029 ..> c0070 : 8 relationships (see list)
    c0030 ..> c0018 : install() calls write_new()
    c0030 ..> c0030 : 15 relationships (see list)
    c0030 ..> c0031 : 3 relationships (see list)
    c0030 ..> c0032 : 4 relationships (see list)
    c0030 ..> c0066 : 6 relationships (see list)
    c0031 ..> c0031 : runtime_ready() calls sync_fingerprint()
    c0031 ..> c0032 : runtime_ready() calls run_owned()
    c0032 ..> c0000 : 2 relationships (see list)
    c0032 ..> c0032 : 2 relationships (see list)
    c0032 ..> c0066 : run_owned() constructs FactoryError
    c0033 --> c0034 : field forgetful
    c0033 --> c0069 : field repository
    c0034 ..> c0035 : 2 relationships (see list)
    c0034 ..> c0066 : _validate_server() constructs FactoryError
    c0035 ..> c0033 : 3 relationships (see list)
    c0035 ..> c0034 : 3 relationships (see list)
    c0035 ..> c0035 : 5 relationships (see list)
    c0035 ..> c0066 : 4 relationships (see list)
    c0035 ..> c0069 : from_mapping() constructs RepositoryReference
    c0035 ..> c0070 : from_mapping() constructs WorkSource
    c0037 ..> c0035 : 3 relationships (see list)
    c0037 ..> c0036 : 2 relationships (see list)
    c0037 ..> c0037 : 3 relationships (see list)
    c0037 ..> c0066 : 4 relationships (see list)
    c0038 ..> c0004 : initialise() calls save()
    c0038 ..> c0010 : prepare_foreman() calls prepare()
    c0038 ..> c0012 : 5 relationships (see list)
    c0038 ..> c0014 : 3 relationships (see list)
    c0038 ..> c0020 : load_existing() calls load()
    c0038 ..> c0029 : 5 relationships (see list)
    c0038 ..> c0033 : 6 relationships (see list)
    c0038 ..> c0034 : 2 relationships (see list)
    c0038 ..> c0035 : 2 relationships (see list)
    c0038 ..> c0038 : 3 relationships (see list)
    c0038 ..> c0039 : type in __init__
    c0038 ..> c0040 : type in __init__
    c0038 ..> c0042 : type in __init__
    c0038 ..> c0046 : type in __init__
    c0038 ..> c0066 : 5 relationships (see list)
    c0038 ..> c0068 : 2 relationships (see list)
    c0038 ..> c0069 : 2 relationships (see list)
    c0038 ..> c0070 : 2 relationships (see list)
    c0038 ..> c0071 : type in __init__
    c0039 ..> c0033 : 2 relationships (see list)
    c0040 ..> c0033 : 3 relationships (see list)
    c0040 ..> c0034 : 8 relationships (see list)
    c0040 ..> c0036 : type in prepare_roles
    c0044 --|> c0066 : inherits
    c0046 ..> c0070 : type in source_from_remote
    c0047 ..> c0000 : __init__() calls __init__()
    c0047 --|> c0066 : inherits
    c0048 --|> c0066 : inherits
    c0050 ..> c0012 : check() calls check()
    c0050 ..> c0014 : check_repository() calls origin()
    c0050 ..> c0016 : 3 relationships (see list)
    c0050 ..> c0027 : 10 relationships (see list)
    c0050 ..> c0029 : _check_source() calls source_from_remote()
    c0050 ..> c0033 : type in __init__
    c0050 ..> c0042 : type in __init__
    c0050 ..> c0043 : type in __init__
    c0050 ..> c0046 : type in __init__
    c0050 ..> c0049 : type in __init__
    c0050 ..> c0050 : 34 relationships (see list)
    c0050 ..> c0051 : _ensure_mapping() calls _cleanup_state()
    c0050 ..> c0056 : preflight() constructs IntakeProblem
    c0050 ..> c0057 : 2 relationships (see list)
    c0050 ..> c0058 : 13 relationships (see list)
    c0050 ..> c0059 : 5 relationships (see list)
    c0050 ..> c0060 : 5 relationships (see list)
    c0050 ..> c0066 : _is_unfinished_factory_plan() constructs FactoryError
    c0050 ..> c0067 : 10 relationships (see list)
    c0050 ..> c0069 : 5 relationships (see list)
    c0050 ..> c0070 : 3 relationships (see list)
    c0051 ..> c0058 : _cleanup_state() constructs ScaffoldProblem
    c0052 --> c0067 : field issue
    c0053 ..> c0000 : 15 relationships (see list)
    c0053 ..> c0010 : _process_issue() calls prepare()
    c0053 ..> c0012 : _check_planning_access() calls check()
    c0053 ..> c0029 : _read_issues() calls list_issues()
    c0053 ..> c0033 : 4 relationships (see list)
    c0053 ..> c0041 : type in __init__
    c0053 ..> c0050 : 6 relationships (see list)
    c0053 ..> c0052 : 13 relationships (see list)
    c0053 ..> c0053 : 35 relationships (see list)
    c0053 ..> c0054 : 19 relationships (see list)
    c0053 ..> c0055 : 2 relationships (see list)
    c0053 ..> c0057 : 2 relationships (see list)
    c0053 ..> c0058 : 3 relationships (see list)
    c0053 ..> c0059 : 2 relationships (see list)
    c0053 ..> c0061 : 28 relationships (see list)
    c0053 ..> c0066 : _read_issues() constructs FactoryError
    c0053 ..> c0067 : 13 relationships (see list)
    c0053 ..> c0069 : 5 relationships (see list)
    c0053 ..> c0070 : 7 relationships (see list)
    c0053 ..> c0071 : type in __init__
    c0054 --> c0052 : 2 relationships (see list)
    c0054 --> c0067 : field pending_lookup
    c0054 --> c0069 : field pending_repositories
    c0054 --> c0070 : field baselined
    c0056 --|> c0058 : inherits
    c0057 --|> c0058 : inherits
    c0058 --|> c0066 : inherits
    c0059 --|> c0058 : inherits
    c0060 --|> c0058 : inherits
    c0061 ..> c0000 : 2 relationships (see list)
    c0061 ..> c0066 : type in send
    c0062 ..> c0007 : build_watcher() constructs AgentShellTerminal
    c0062 ..> c0012 : 5 relationships (see list)
    c0062 ..> c0014 : 2 relationships (see list)
    c0062 ..> c0016 : build_watcher() constructs GitWorktrees
    c0062 ..> c0020 : build_initialiser() constructs TomlConfigurationStore
    c0062 ..> c0026 : prepare_foreman_launch() calls role_environment()
    c0062 ..> c0027 : build_watcher() constructs ForgetfulPlanning
    c0062 ..> c0029 : 3 relationships (see list)
    c0062 ..> c0033 : 2 relationships (see list)
    c0062 ..> c0038 : 2 relationships (see list)
    c0062 ..> c0050 : build_watcher() constructs ScaffoldIssue
    c0062 ..> c0053 : 2 relationships (see list)
    c0062 ..> c0062 : build_watcher() calls prepare_foreman_launch()
    c0062 ..> c0066 : 2 relationships (see list)
    c0063 --> c0033 : field config
    c0063 --> c0034 : field connection
    c0064 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0064 ..> c0004 : _watch_locked() calls run()
    c0064 ..> c0006 : 13 relationships (see list)
    c0064 ..> c0012 : 15 relationships (see list)
    c0064 ..> c0014 : select_repositories() calls discover()
    c0064 ..> c0016 : _configure_new_factory() calls inspect()
    c0064 ..> c0018 : _discover_worker_models() calls check_real_path()
    c0064 ..> c0020 : _initialise_locked() calls load()
    c0064 ..> c0021 : 6 relationships (see list)
    c0064 ..> c0022 : 6 relationships (see list)
    c0064 ..> c0033 : 4 relationships (see list)
    c0064 ..> c0034 : 6 relationships (see list)
    c0064 ..> c0036 : 6 relationships (see list)
    c0064 ..> c0037 : _start_initial_setup() calls validate_initial_agents()
    c0064 ..> c0038 : 15 relationships (see list)
    c0064 ..> c0062 : 4 relationships (see list)
    c0064 ..> c0063 : 3 relationships (see list)
    c0064 ..> c0064 : 49 relationships (see list)
    c0064 ..> c0065 : 3 relationships (see list)
    c0064 ..> c0066 : 19 relationships (see list)
    c0065 ..> c0020 : 2 relationships (see list)
    c0065 ..> c0033 : type in load_configuration
    c0065 ..> c0066 : load_configuration() constructs FactoryError
    c0067 --> c0070 : field source
    c0069 --> c0070 : field work_source
    c0071 ..> c0067 : type in list_issues
    c0071 ..> c0068 : 2 relationships (see list)
    c0071 ..> c0070 : 4 relationships (see list)
```

## Source index

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/adapters/agentshell/borrowed_terminal.py`:9
- c0001: `SessionState` — `src/forgetful_factory/adapters/agentshell/controller.py`:136
- c0002: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0003: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0004: `ForemanOwner` — `src/forgetful_factory/adapters/agentshell/owner.py`:102
- c0005: `src/forgetful_factory/adapters/agentshell/owner.py` —
  `src/forgetful_factory/adapters/agentshell/owner.py`:1
- c0006: `src/forgetful_factory/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/adapters/agentshell/owner_client.py`:1
- c0007: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:12
- c0008: `src/forgetful_factory/adapters/command.py` — `src/forgetful_factory/adapters/command.py`:1
- c0009: `src/forgetful_factory/adapters/filesystem/agent_definitions.py` —
  `src/forgetful_factory/adapters/filesystem/agent_definitions.py`:1
- c0010: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:27
- c0011: `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:1
- c0012: `ForemanProfile` — `src/forgetful_factory/adapters/filesystem/foreman_profile.py`:49
- c0013: `src/forgetful_factory/adapters/filesystem/foreman_runtime.py` —
  `src/forgetful_factory/adapters/filesystem/foreman_runtime.py`:1
- c0014: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:15
- c0015: `src/forgetful_factory/adapters/filesystem/git_repositories.py` —
  `src/forgetful_factory/adapters/filesystem/git_repositories.py`:1
- c0016: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:32
- c0017: `src/forgetful_factory/adapters/filesystem/git_worktrees.py` —
  `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:1
- c0018: `src/forgetful_factory/adapters/filesystem/resource_files.py` —
  `src/forgetful_factory/adapters/filesystem/resource_files.py`:1
- c0019: `src/forgetful_factory/adapters/filesystem/selected_skills.py` —
  `src/forgetful_factory/adapters/filesystem/selected_skills.py`:1
- c0020: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:20
- c0021: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0022: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0023: `WorkerProfiles` — `src/forgetful_factory/adapters/filesystem/worker_profiles.py`:15
- c0024: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0025: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:52
- c0026: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0027: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:13
- c0028: `src/forgetful_factory/adapters/forgetful/planning.py` —
  `src/forgetful_factory/adapters/forgetful/planning.py`:1
- c0029: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0030: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:52
- c0031: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0032: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0033: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:82
- c0034: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0035: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0036: `InitialAgentChoices` — `src/forgetful_factory/application/initial_agent_choices.py`:9
- c0037: `src/forgetful_factory/application/initial_agent_choices.py` —
  `src/forgetful_factory/application/initial_agent_choices.py`:1
- c0038: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0039: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0040: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:8
- c0041: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0042: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0043: `Planning` — `src/forgetful_factory/application/ports/planning.py`:10
- c0044: `PlanningReadError` — `src/forgetful_factory/application/ports/planning.py`:6
- c0045: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0046: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0047: `WorktreeProblem` — `src/forgetful_factory/application/ports/worktrees.py`:10
- c0048: `WorktreeReadError` — `src/forgetful_factory/application/ports/worktrees.py`:6
- c0049: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:19
- c0050: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:47
- c0051: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0052: `BlockedWork` — `src/forgetful_factory/application/watch_factory.py`:28
- c0053: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:60
- c0054: `_WatchState` — `src/forgetful_factory/application/watch_factory.py`:39
- c0055: `_WorkAction` — `src/forgetful_factory/application/watch_factory.py`:53
- c0056: `IntakeProblem` — `src/forgetful_factory/application/watcher_problems.py`:104
- c0057: `RepositoryProblem` — `src/forgetful_factory/application/watcher_problems.py`:100
- c0058: `ScaffoldProblem` — `src/forgetful_factory/application/watcher_problems.py`:80
- c0059: `ScaffoldReadProblem` — `src/forgetful_factory/application/watcher_problems.py`:96
- c0060: `UncertainScaffold` — `src/forgetful_factory/application/watcher_problems.py`:108
- c0061: `WatcherAlerts` — `src/forgetful_factory/application/watcher_problems.py`:112
- c0062: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0063: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:629
- c0064: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0065: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0066: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0067: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0068: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0069: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0070: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0071: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0007: `close() calls close()`
- c0000 ..> c0066: `_request() constructs FactoryError`
- c0000 ..> c0066: `wait() constructs FactoryError`
- c0002 ..> c0000: `close_session() calls close()`
- c0002 ..> c0000: `control() calls close()`
- c0002 ..> c0000: `control() calls wait()`
- c0002 ..> c0000: `pin_worker() calls close()`
- c0002 ..> c0000: `resume_exit_observation() calls wait()`
- c0002 ..> c0000: `supervise_session() calls wait()`
- c0002 ..> c0001: `serve() constructs SessionState`
- c0002 ..> c0002: `build_shell() calls runtime()`
- c0002 ..> c0002: `capture_worker() calls pin_worker()`
- c0002 ..> c0002: `control() calls serve()`
- c0002 ..> c0002: `interact() calls ready()`
- c0002 ..> c0002: `main() calls control()`
- c0002 ..> c0002: `open_session() calls capture_worker()`
- c0002 ..> c0002: `replace_failed_exit_task() calls resume_exit_observation()`
- c0002 ..> c0002: `serve() calls build_shell()`
- c0002 ..> c0002: `serve() calls close_session()`
- c0002 ..> c0002: `serve() calls open_session()`
- c0002 ..> c0002: `serve() calls supervise_session()`
- c0002 ..> c0002: `serve() calls validate_launch_config()`
- c0002 ..> c0002: `supervise_session() calls cancel_tasks()`
- c0002 ..> c0002: `supervise_session() calls interact()`
- c0002 ..> c0002: `supervise_session() calls replace_failed_exit_task()`
- c0002 ..> c0002: `supervise_session() calls retain_identity()`
- c0002 ..> c0002: `supervise_session() calls worker_exited()`
- c0002 ..> c0027: `control() calls create_task()`
- c0002 ..> c0027: `main() calls create_task()`
- c0002 ..> c0027: `replace_failed_exit_task() calls create_task()`
- c0002 ..> c0027: `supervise_session() calls create_task()`
- c0003 ..> c0012: `main() calls list_models()`
- c0004 ..> c0000: `_await_readiness() calls wait()`
- c0004 ..> c0000: `_cleanup() calls close()`
- c0004 ..> c0000: `_close_controller() calls close()`
- c0004 ..> c0000: `_close_controller() calls wait()`
- c0004 ..> c0000: `_complete_handover() calls close()`
- c0004 ..> c0000: `control() calls close()`
- c0004 ..> c0000: `reap_watcher() calls wait()`
- c0004 ..> c0000: `relay() calls close()`
- c0004 ..> c0000: `run() calls close()`
- c0004 ..> c0000: `run() calls wait()`
- c0004 ..> c0000: `start_watcher() calls close()`
- c0004 ..> c0004: `_apply_controller_event() calls _apply_controller_problem()`
- c0004 ..> c0004: `_apply_controller_event() calls save()`
- c0004 ..> c0004: `_apply_controller_problem() calls save()`
- c0004 ..> c0004: `_apply_controller_problem() calls stop_watcher()`
- c0004 ..> c0004: `_cleanup() calls _close_controller()`
- c0004 ..> c0004: `_cleanup() calls _remove_control_socket()`
- c0004 ..> c0004: `_cleanup() calls stop_watcher()`
- c0004 ..> c0004: `_close_controller() calls save()`
- c0004 ..> c0004: `_finish_observation() calls save()`
- c0004 ..> c0004: `_reject_controller_event() calls save()`
- c0004 ..> c0004: `_reject_controller_event() calls stop_watcher()`
- c0004 ..> c0004: `_start_controller() calls observe()`
- c0004 ..> c0004: `control() calls start_watcher()`
- c0004 ..> c0004: `control() calls stop_watcher()`
- c0004 ..> c0004: `observe() calls _apply_controller_event()`
- c0004 ..> c0004: `observe() calls _finish_observation()`
- c0004 ..> c0004: `observe() calls _reject_controller_event()`
- c0004 ..> c0004: `observe() calls _validate_readiness()`
- c0004 ..> c0004: `relay() calls _relay_request()`
- c0004 ..> c0004: `run() calls _await_readiness()`
- c0004 ..> c0004: `run() calls _cleanup()`
- c0004 ..> c0004: `run() calls _complete_handover()`
- c0004 ..> c0004: `run() calls _start_controller()`
- c0004 ..> c0004: `run() calls save()`
- c0004 ..> c0004: `start_watcher() calls reap_watcher()`
- c0004 ..> c0004: `start_watcher() calls relay()`
- c0004 ..> c0004: `start_watcher() calls stop_watcher()`
- c0004 ..> c0005: `observe() calls _controller_event()`
- c0004 ..> c0005: `relay() calls _watcher_request()`
- c0004 ..> c0018: `save() calls replace_generated_json()`
- c0004 ..> c0021: `_apply_controller_problem() calls quote()`
- c0004 ..> c0027: `_start_controller() calls create_task()`
- c0004 ..> c0027: `start_watcher() calls create_task()`
- c0004 ..> c0066: `_apply_controller_problem() constructs FactoryError`
- c0004 ..> c0066: `_await_readiness() constructs FactoryError`
- c0004 ..> c0066: `_complete_handover() constructs FactoryError`
- c0004 ..> c0066: `_finish_observation() constructs FactoryError`
- c0004 ..> c0066: `_reject_controller_event() constructs FactoryError`
- c0004 ..> c0066: `_relay_request() constructs FactoryError`
- c0004 ..> c0066: `control() constructs FactoryError`
- c0004 ..> c0066: `observe() constructs FactoryError`
- c0004 ..> c0066: `reap_watcher() constructs FactoryError`
- c0004 ..> c0066: `start_watcher() constructs FactoryError`
- c0005 ..> c0000: `_acquire_owner_lock() calls close()`
- c0005 ..> c0000: `_prepare_owner_startup() calls close()`
- c0005 ..> c0000: `entrypoint() calls close()`
- c0005 ..> c0004: `entrypoint() calls run()`
- c0005 ..> c0004: `main() calls run()`
- c0005 ..> c0004: `main() constructs ForemanOwner`
- c0005 ..> c0005: `_controller_event() calls _validate_target()`
- c0005 ..> c0005: `_prepare_owner_startup() calls _acquire_owner_lock()`
- c0005 ..> c0005: `entrypoint() calls _prepare_owner_startup()`
- c0005 ..> c0005: `entrypoint() calls _report_startup_error()`
- c0005 ..> c0005: `entrypoint() calls main()`
- c0005 ..> c0006: `_prepare_owner_startup() calls read_state()`
- c0005 ..> c0013: `_prepare_owner_startup() calls runtime_directory()`
- c0005 ..> c0021: `_acquire_owner_lock() calls quote()`
- c0005 ..> c0027: `main() calls create_task()`
- c0005 ..> c0066: `_acquire_owner_lock() constructs FactoryError`
- c0005 ..> c0066: `_prepare_owner_startup() constructs FactoryError`
- c0005 ..> c0066: `_watcher_request() constructs FactoryError`
- c0006 ..> c0000: `start_owner() calls close()`
- c0006 ..> c0000: `start_owner() calls wait()`
- c0006 ..> c0004: `enter_terminal() calls run()`
- c0006 ..> c0004: `start_owner() calls run()`
- c0006 ..> c0006: `request() calls _reply()`
- c0006 ..> c0006: `request() calls read_state()`
- c0006 ..> c0006: `start_owner() calls _reply()`
- c0006 ..> c0013: `read_state() calls runtime_directory()`
- c0006 ..> c0013: `request() calls runtime_directory()`
- c0006 ..> c0013: `start_owner() calls runtime_directory()`
- c0006 ..> c0018: `read_state() calls read_generated_json()`
- c0006 ..> c0021: `request() calls quote()`
- c0006 ..> c0066: `_reply() constructs FactoryError`
- c0006 ..> c0066: `enter_terminal() constructs FactoryError`
- c0006 ..> c0066: `read_state() constructs FactoryError`
- c0006 ..> c0066: `request() constructs FactoryError`
- c0006 ..> c0066: `start_owner() constructs FactoryError`
- c0007 ..> c0000: `close() calls close()`
- c0007 ..> c0007: `send() calls _read()`
- c0007 ..> c0007: `send() calls _write()`
- c0007 ..> c0007: `start() calls _read()`
- c0007 ..> c0007: `start() calls _write()`
- c0007 ..> c0007: `wait() calls _read()`
- c0007 ..> c0066: `_read() constructs FactoryError`
- c0007 ..> c0066: `_write() constructs FactoryError`
- c0007 ..> c0066: `close() constructs FactoryError`
- c0007 ..> c0066: `start() constructs FactoryError`
- c0008 ..> c0004: `run_command() calls run()`
- c0008 ..> c0066: `run_command() constructs FactoryError`
- c0009 ..> c0009: `_validate_agent() calls _local_selection()`
- c0009 ..> c0009: `_validate_roster() calls _local_selection()`
- c0009 ..> c0009: `_validate_roster() calls relative_path()`
- c0009 ..> c0009: `foreman_launch() calls read_definition()`
- c0009 ..> c0009: `foreman_launch() calls relative_path()`
- c0009 ..> c0009: `read_definition() calls _validate_agent()`
- c0009 ..> c0009: `read_definition() calls _validate_resources()`
- c0009 ..> c0009: `read_definition() calls _validate_roster()`
- c0009 ..> c0035: `_local_selection() calls nonblank()`
- c0009 ..> c0035: `_validate_agent() calls nonblank()`
- c0009 ..> c0035: `foreman_launch() calls nonblank()`
- c0009 ..> c0035: `relative_path() calls nonblank()`
- c0009 ..> c0066: `foreman_launch() constructs FactoryError`
- c0009 ..> c0066: `read_definition() constructs FactoryError`
- c0010 ..> c0010: `prepare() calls _write_agent()`
- c0010 ..> c0010: `prepare() calls validate_guidance()`
- c0010 ..> c0011: `prepare() calls selected_resources()`
- c0010 ..> c0012: `prepare() calls prepare()`
- c0010 ..> c0018: `_write_agent() calls write_definition()`
- c0010 ..> c0018: `prepare() calls check_skill_file()`
- c0010 ..> c0018: `prepare() calls write_new()`
- c0010 ..> c0023: `__init__() constructs WorkerProfiles`
- c0010 ..> c0033: `type in prepare`
- c0010 ..> c0033: `type in validate_guidance`
- c0010 ..> c0066: `prepare() constructs FactoryError`
- c0010 ..> c0066: `validate_depth() constructs FactoryError`
- c0010 ..> c0066: `validate_guidance() constructs FactoryError`
- c0012 ..> c0009: `selected_launch() calls foreman_launch()`
- c0012 ..> c0010: `prepare_roles() calls validate_depth()`
- c0012 ..> c0010: `prepare_roles() constructs CoordinatorProfiles`
- c0012 ..> c0010: `validate_setup() calls validate_depth()`
- c0012 ..> c0010: `validate_setup() constructs CoordinatorProfiles`
- c0012 ..> c0012: `choose_pi_home() calls pi_home()`
- c0012 ..> c0012: `choose_pi_home() calls require_pi_home()`
- c0012 ..> c0012: `list_models() calls pi_home()`
- c0012 ..> c0012: `list_models() calls require_pi_home()`
- c0012 ..> c0012: `missing_executables() calls pi_home()`
- c0012 ..> c0012: `prepare() calls _install_resources()`
- c0012 ..> c0012: `prepare() calls _protect_runtime()`
- c0012 ..> c0012: `prepare() calls save_pi_choice()`
- c0012 ..> c0012: `prepare() calls validate_guidance()`
- c0012 ..> c0012: `prepare_roles() calls list_models()`
- c0012 ..> c0012: `prepare_roles() calls pi_home()`
- c0012 ..> c0012: `prepare_roles() calls prepare()`
- c0012 ..> c0012: `prepare_roles() calls validate_worker_models()`
- c0012 ..> c0012: `record_completion() calls selected_launch()`
- c0012 ..> c0012: `selected_launch() calls validate_setup()`
- c0012 ..> c0012: `validate_guidance() calls _read_guidance()`
- c0012 ..> c0012: `validate_setup() calls missing_executables()`
- c0012 ..> c0012: `validate_setup() calls pi_home()`
- c0012 ..> c0012: `validate_setup() calls require_pi_home()`
- c0012 ..> c0012: `validate_setup() calls validate_bundled_resources()`
- c0012 ..> c0012: `validate_setup() calls validate_guidance()`
- c0012 ..> c0012: `validate_worker_models() calls list_models()`
- c0012 ..> c0018: `_install_resources() calls write_new()`
- c0012 ..> c0018: `_protect_runtime() calls write_new()`
- c0012 ..> c0018: `begin_setup() calls remove_generated()`
- c0012 ..> c0018: `pi_home() calls read_generated_json()`
- c0012 ..> c0018: `prepare() calls write_new()`
- c0012 ..> c0018: `prepare_roles() calls check_real_path()`
- c0012 ..> c0018: `prepare_setup_guidance() calls write_new()`
- c0012 ..> c0018: `record_completion() calls replace_generated_json()`
- c0012 ..> c0018: `save_pi_choice() calls write_json()`
- c0012 ..> c0018: `validate_bundled_resources() calls check_real_path()`
- c0012 ..> c0018: `validate_completion() calls read_generated_json()`
- c0012 ..> c0019: `selected_launch() calls selected_skill_files()`
- c0012 ..> c0021: `require_pi_home() calls quote()`
- c0012 ..> c0024: `uses_browser_login() calls uses_browser_login()`
- c0012 ..> c0025: `check() calls check()`
- c0012 ..> c0025: `check() constructs AgentForgetfulConnection`
- c0012 ..> c0025: `create_project() calls create_project()`
- c0012 ..> c0025: `create_project() constructs AgentForgetfulConnection`
- c0012 ..> c0025: `login() calls login()`
- c0012 ..> c0025: `login() constructs AgentForgetfulConnection`
- c0012 ..> c0025: `projects() calls projects()`
- c0012 ..> c0025: `projects() constructs AgentForgetfulConnection`
- c0012 ..> c0026: `list_models() calls role_environment()`
- c0012 ..> c0030: `install() calls install()`
- c0012 ..> c0030: `install() constructs HostDependencies`
- c0012 ..> c0030: `installation() calls description()`
- c0012 ..> c0030: `installation() constructs HostDependencies`
- c0012 ..> c0030: `missing_executables() calls pi_ready()`
- c0012 ..> c0030: `missing_executables() constructs HostDependencies`
- c0012 ..> c0031: `missing_executables() calls executable_path()`
- c0012 ..> c0031: `missing_executables() calls runtime_ready()`
- c0012 ..> c0031: `require_pi_home() calls executable_path()`
- c0012 ..> c0032: `list_models() calls run_owned()`
- c0012 ..> c0033: `type in record_completion`
- c0012 ..> c0033: `type in selected_launch`
- c0012 ..> c0033: `type in validate_completion`
- c0012 ..> c0033: `type in validate_worker_models`
- c0012 ..> c0034: `type in check`
- c0012 ..> c0034: `type in create_project`
- c0012 ..> c0034: `type in list_models`
- c0012 ..> c0034: `type in login`
- c0012 ..> c0034: `type in missing_executables`
- c0012 ..> c0034: `type in prepare`
- c0012 ..> c0034: `type in projects`
- c0012 ..> c0034: `type in uses_browser_login`
- c0012 ..> c0034: `type in validate_setup`
- c0012 ..> c0066: `_install_resources() constructs FactoryError`
- c0012 ..> c0066: `_read_guidance() constructs FactoryError`
- c0012 ..> c0066: `choose_pi_home() constructs FactoryError`
- c0012 ..> c0066: `list_models() constructs FactoryError`
- c0012 ..> c0066: `pi_home() constructs FactoryError`
- c0012 ..> c0066: `prepare_roles() constructs FactoryError`
- c0012 ..> c0066: `prepare_setup_guidance() constructs FactoryError`
- c0012 ..> c0066: `require_pi_home() constructs FactoryError`
- c0012 ..> c0066: `selected_launch() constructs FactoryError`
- c0012 ..> c0066: `validate_bundled_resources() constructs FactoryError`
- c0012 ..> c0066: `validate_completion() constructs FactoryError`
- c0012 ..> c0066: `validate_guidance() constructs FactoryError`
- c0012 ..> c0066: `validate_setup() constructs FactoryError`
- c0012 ..> c0066: `validate_worker_models() constructs FactoryError`
- c0013 ..> c0018: `runtime_directory() calls check_real_path()`
- c0013 ..> c0066: `runtime_directory() constructs FactoryError`
- c0014 ..> c0008: `origin() calls run_command()`
- c0014 ..> c0015: `origin() calls _resolve_repository()`
- c0014 ..> c0066: `origin() constructs FactoryError`
- c0015 ..> c0066: `_resolve_repository() constructs FactoryError`
- c0016 ..> c0008: `ensure() calls run_command()`
- c0016 ..> c0016: `_inspect() calls _repository_entries()`
- c0016 ..> c0016: `_inspect() calls _validate_registered_worktree()`
- c0016 ..> c0016: `_validate_registered_worktree() calls _validate_common_directory()`
- c0016 ..> c0016: `_validate_registered_worktree() calls _validate_registration()`
- c0016 ..> c0016: `_validate_registered_worktree() calls _validate_target_identity()`
- c0016 ..> c0016: `_verify_removed() calls _repository_entries()`
- c0016 ..> c0016: `ensure() calls _inspect()`
- c0016 ..> c0016: `inspect() calls _inspect()`
- c0016 ..> c0016: `verify_removed() calls _verify_removed()`
- c0016 ..> c0017: `_inspect() calls _read_git()`
- c0016 ..> c0017: `_repository_entries() calls _read_git()`
- c0016 ..> c0017: `_repository_entries() calls _worktree_entries()`
- c0016 ..> c0017: `_validate_common_directory() calls _read_git()`
- c0016 ..> c0017: `_validate_target_identity() calls _read_git()`
- c0016 ..> c0047: `_inspect() constructs WorktreeProblem`
- c0016 ..> c0047: `_repository_entries() constructs WorktreeProblem`
- c0016 ..> c0047: `_validate_common_directory() constructs WorktreeProblem`
- c0016 ..> c0047: `_validate_registration() constructs WorktreeProblem`
- c0016 ..> c0047: `_validate_target_identity() constructs WorktreeProblem`
- c0016 ..> c0047: `_verify_removed() constructs WorktreeProblem`
- c0016 ..> c0048: `ensure() constructs WorktreeReadError`
- c0016 ..> c0048: `inspect() constructs WorktreeReadError`
- c0016 ..> c0048: `verify_removed() constructs WorktreeReadError`
- c0016 ..> c0066: `ensure() constructs FactoryError`
- c0017 ..> c0008: `_read_git() calls run_command()`
- c0017 ..> c0048: `_read_git() constructs WorktreeReadError`
- c0018 ..> c0000: `_generated_parent() calls close()`
- c0018 ..> c0000: `check_skill_file() calls close()`
- c0018 ..> c0018: `_generated_parent() calls check_real_path()`
- c0018 ..> c0018: `check_skill_file() calls check_real_path()`
- c0018 ..> c0018: `read_generated_json() calls _generated_parent()`
- c0018 ..> c0018: `remove_generated() calls _generated_parent()`
- c0018 ..> c0018: `replace_generated_json() calls _generated_parent()`
- c0018 ..> c0018: `write_definition() calls read_generated_json()`
- c0018 ..> c0018: `write_definition() calls write_json()`
- c0018 ..> c0018: `write_json() calls write_new()`
- c0018 ..> c0018: `write_new() calls check_real_path()`
- c0018 ..> c0020: `read_generated_json() calls load()`
- c0018 ..> c0066: `_generated_parent() constructs FactoryError`
- c0018 ..> c0066: `check_real_path() constructs FactoryError`
- c0018 ..> c0066: `check_skill_file() constructs FactoryError`
- c0018 ..> c0066: `read_generated_json() constructs FactoryError`
- c0018 ..> c0066: `write_definition() constructs FactoryError`
- c0018 ..> c0066: `write_new() constructs FactoryError`
- c0019 ..> c0000: `_add_skill_file() calls close()`
- c0019 ..> c0019: `_walk_skill_directory() calls _add_skill_file()`
- c0019 ..> c0019: `selected_skill_files() calls _add_skill_file()`
- c0019 ..> c0019: `selected_skill_files() calls _walk_skill_directory()`
- c0019 ..> c0066: `_add_skill_file() constructs FactoryError`
- c0019 ..> c0066: `_walk_skill_directory() constructs FactoryError`
- c0019 ..> c0066: `selected_skill_files() constructs FactoryError`
- c0020 ..> c0000: `load() calls close()`
- c0020 ..> c0000: `save() calls close()`
- c0020 ..> c0021: `save() calls quote()`
- c0020 ..> c0033: `type in load`
- c0020 ..> c0033: `type in save`
- c0020 ..> c0035: `load() calls from_mapping()`
- c0020 ..> c0039: `load() calls load()`
- c0020 ..> c0066: `load() constructs FactoryError`
- c0020 ..> c0066: `save() constructs FactoryError`
- c0022 ..> c0000: `_hold_directory() calls close()`
- c0022 ..> c0022: `hold() calls _hold_directory()`
- c0022 ..> c0066: `_hold_directory() constructs FactoryError`
- c0023 ..> c0018: `prepare() calls check_skill_file()`
- c0023 ..> c0018: `prepare() calls write_definition()`
- c0023 ..> c0018: `prepare() calls write_new()`
- c0023 ..> c0036: `type in prepare`
- c0024 ..> c0006: `uses_browser_login() calls request()`
- c0024 ..> c0034: `type in uses_browser_login`
- c0025 ..> c0025: `call() calls command()`
- c0025 ..> c0025: `check() calls call()`
- c0025 ..> c0025: `check() calls command()`
- c0025 ..> c0025: `command() calls _environment()`
- c0025 ..> c0025: `create_project() calls call()`
- c0025 ..> c0025: `login() calls _environment()`
- c0025 ..> c0025: `projects() calls command()`
- c0025 ..> c0026: `_environment() calls role_environment()`
- c0025 ..> c0026: `check() calls _catalog_tools()`
- c0025 ..> c0032: `command() calls run_owned()`
- c0025 ..> c0032: `login() calls run_owned()`
- c0025 ..> c0034: `type in _environment`
- c0025 ..> c0034: `type in call`
- c0025 ..> c0034: `type in check`
- c0025 ..> c0034: `type in command`
- c0025 ..> c0034: `type in create_project`
- c0025 ..> c0034: `type in login`
- c0025 ..> c0034: `type in projects`
- c0025 ..> c0066: `check() constructs FactoryError`
- c0025 ..> c0066: `command() constructs FactoryError`
- c0025 ..> c0066: `create_project() constructs FactoryError`
- c0025 ..> c0066: `login() constructs FactoryError`
- c0025 ..> c0066: `projects() constructs FactoryError`
- c0026 ..> c0031: `role_environment() calls executable_path()`
- c0026 ..> c0034: `type in role_environment`
- c0027 ..> c0012: `check() calls check()`
- c0027 ..> c0025: `__init__() constructs AgentForgetfulConnection`
- c0027 ..> c0025: `_call() calls call()`
- c0027 ..> c0027: `_read() calls _call()`
- c0027 ..> c0027: `_task() calls _read()`
- c0027 ..> c0027: `create_plan() calls _call()`
- c0027 ..> c0027: `create_task() calls _call()`
- c0027 ..> c0027: `get_plan() calls _read()`
- c0027 ..> c0027: `plans() calls _read()`
- c0027 ..> c0027: `plans() calls _rows()`
- c0027 ..> c0027: `tasks() calls _read()`
- c0027 ..> c0027: `tasks() calls _rows()`
- c0027 ..> c0027: `tasks() calls _task()`
- c0027 ..> c0027: `update_plan() calls _call()`
- c0027 ..> c0027: `update_task() calls _call()`
- c0027 ..> c0028: `_rows() calls _positive_id()`
- c0027 ..> c0028: `_task() calls _positive_id()`
- c0027 ..> c0028: `get_plan() calls _positive_id()`
- c0027 ..> c0034: `type in __init__`
- c0027 ..> c0044: `_read() constructs PlanningReadError`
- c0027 ..> c0044: `_rows() constructs PlanningReadError`
- c0027 ..> c0044: `_task() constructs PlanningReadError`
- c0027 ..> c0044: `get_plan() constructs PlanningReadError`
- c0029 ..> c0008: `_api() calls run_command()`
- c0029 ..> c0029: `check_access() calls _api()`
- c0029 ..> c0029: `create_label() calls _api()`
- c0029 ..> c0029: `list_issues() calls _api()`
- c0029 ..> c0029: `list_issues() calls _validate_issue()`
- c0029 ..> c0029: `list_labels() calls _api()`
- c0029 ..> c0066: `_api() constructs FactoryError`
- c0029 ..> c0066: `_validate_issue() constructs FactoryError`
- c0029 ..> c0066: `check_access() constructs FactoryError`
- c0029 ..> c0066: `create_label() constructs FactoryError`
- c0029 ..> c0066: `list_issues() constructs FactoryError`
- c0029 ..> c0066: `list_labels() constructs FactoryError`
- c0029 ..> c0066: `source_from_remote() constructs FactoryError`
- c0029 ..> c0067: `list_issues() constructs Issue`
- c0029 ..> c0067: `type in list_issues`
- c0029 ..> c0068: `list_labels() constructs Label`
- c0029 ..> c0068: `type in create_label`
- c0029 ..> c0068: `type in list_labels`
- c0029 ..> c0070: `source_from_remote() constructs WorkSource`
- c0029 ..> c0070: `type in _api`
- c0029 ..> c0070: `type in _validate_issue`
- c0029 ..> c0070: `type in check_access`
- c0029 ..> c0070: `type in create_label`
- c0029 ..> c0070: `type in list_issues`
- c0029 ..> c0070: `type in list_labels`
- c0029 ..> c0070: `type in source_from_remote`
- c0030 ..> c0018: `install() calls write_new()`
- c0030 ..> c0030: `_check_uv() calls _environment()`
- c0030 ..> c0030: `_forgetful_python() calls _check_uv()`
- c0030 ..> c0030: `_forgetful_python() calls _environment()`
- c0030 ..> c0030: `_install_role_runtime() calls _check_uv()`
- c0030 ..> c0030: `_install_role_runtime() calls _run()`
- c0030 ..> c0030: `_install_tmux() calls _run()`
- c0030 ..> c0030: `_run() calls _environment()`
- c0030 ..> c0030: `description() calls _forgetful_python()`
- c0030 ..> c0030: `description() calls _ubuntu_tmux()`
- c0030 ..> c0030: `install() calls _forgetful_python()`
- c0030 ..> c0030: `install() calls _install_role_runtime()`
- c0030 ..> c0030: `install() calls _install_tmux()`
- c0030 ..> c0030: `install() calls _run()`
- c0030 ..> c0030: `install() calls _ubuntu_tmux()`
- c0030 ..> c0030: `pi_ready() calls _environment()`
- c0030 ..> c0031: `_install_role_runtime() calls sync_fingerprint()`
- c0030 ..> c0031: `install() calls sync_fingerprint()`
- c0030 ..> c0031: `pi_ready() calls sync_fingerprint()`
- c0030 ..> c0032: `_check_uv() calls run_owned()`
- c0030 ..> c0032: `_forgetful_python() calls run_owned()`
- c0030 ..> c0032: `_run() calls run_owned()`
- c0030 ..> c0032: `pi_ready() calls run_owned()`
- c0030 ..> c0066: `_check_uv() constructs FactoryError`
- c0030 ..> c0066: `_forgetful_python() constructs FactoryError`
- c0030 ..> c0066: `_install_role_runtime() constructs FactoryError`
- c0030 ..> c0066: `_install_tmux() constructs FactoryError`
- c0030 ..> c0066: `_run() constructs FactoryError`
- c0030 ..> c0066: `install() constructs FactoryError`
- c0031 ..> c0031: `runtime_ready() calls sync_fingerprint()`
- c0031 ..> c0032: `runtime_ready() calls run_owned()`
- c0032 ..> c0000: `_close_capture_streams() calls close()`
- c0032 ..> c0000: `_terminate_owned_process() calls wait()`
- c0032 ..> c0032: `_terminate_owned_process() calls _close_capture_streams()`
- c0032 ..> c0032: `run_owned() calls _terminate_owned_process()`
- c0032 ..> c0066: `run_owned() constructs FactoryError`
- c0033 --> c0034: `field forgetful`
- c0033 --> c0069: `field repository`
- c0034 ..> c0035: `_validate_server() calls loopback_host()`
- c0034 ..> c0035: `_validate_server() calls nonblank()`
- c0034 ..> c0066: `_validate_server() constructs FactoryError`
- c0035 ..> c0033: `from_mapping() constructs FactoryConfiguration`
- c0035 ..> c0033: `type in from_mapping`
- c0035 ..> c0033: `type in validate`
- c0035 ..> c0034: `connection_from_mapping() constructs ForgetfulConnection`
- c0035 ..> c0034: `type in connection_from_mapping`
- c0035 ..> c0034: `validate() calls _validate_server()`
- c0035 ..> c0035: `connection_from_mapping() calls validate()`
- c0035 ..> c0035: `from_mapping() calls connection_from_mapping()`
- c0035 ..> c0035: `from_mapping() calls validate()`
- c0035 ..> c0035: `unique_labels() calls nonblank()`
- c0035 ..> c0035: `validate() calls nonblank()`
- c0035 ..> c0066: `connection_from_mapping() constructs FactoryError`
- c0035 ..> c0066: `from_mapping() constructs FactoryError`
- c0035 ..> c0066: `nonblank() constructs FactoryError`
- c0035 ..> c0066: `validate() constructs FactoryError`
- c0035 ..> c0069: `from_mapping() constructs RepositoryReference`
- c0035 ..> c0070: `from_mapping() constructs WorkSource`
- c0037 ..> c0035: `skill_paths() calls nonblank()`
- c0037 ..> c0035: `validate_initial_agents() calls nonblank()`
- c0037 ..> c0035: `validate_workers() calls nonblank()`
- c0037 ..> c0036: `type in validate_initial_agents`
- c0037 ..> c0036: `type in validate_workers`
- c0037 ..> c0037: `validate_initial_agents() calls validate_role_app()`
- c0037 ..> c0037: `validate_initial_agents() calls validate_workers()`
- c0037 ..> c0037: `validate_workers() calls validate_role_app()`
- c0037 ..> c0066: `skill_paths() constructs FactoryError`
- c0037 ..> c0066: `validate_initial_agents() constructs FactoryError`
- c0037 ..> c0066: `validate_role_app() constructs FactoryError`
- c0037 ..> c0066: `validate_workers() constructs FactoryError`
- c0038 ..> c0004: `initialise() calls save()`
- c0038 ..> c0010: `prepare_foreman() calls prepare()`
- c0038 ..> c0012: `check_foreman() calls check()`
- c0038 ..> c0012: `check_foreman() calls login()`
- c0038 ..> c0012: `prepare_foreman() calls install()`
- c0038 ..> c0012: `prepare_foreman() calls installation()`
- c0038 ..> c0012: `prepare_foreman() calls missing_executables()`
- c0038 ..> c0014: `_preflight() calls origin()`
- c0038 ..> c0014: `discover() calls discover()`
- c0038 ..> c0014: `inspect() calls origin()`
- c0038 ..> c0020: `load_existing() calls load()`
- c0038 ..> c0029: `_ensure_label() calls create_label()`
- c0038 ..> c0029: `_preflight() calls check_access()`
- c0038 ..> c0029: `_preflight() calls list_labels()`
- c0038 ..> c0029: `_preflight() calls source_from_remote()`
- c0038 ..> c0029: `inspect() calls source_from_remote()`
- c0038 ..> c0033: `configure() constructs FactoryConfiguration`
- c0038 ..> c0033: `type in _preflight`
- c0038 ..> c0033: `type in check_foreman`
- c0038 ..> c0033: `type in configure`
- c0038 ..> c0033: `type in initialise`
- c0038 ..> c0033: `type in load_existing`
- c0038 ..> c0034: `_preflight() calls validate()`
- c0038 ..> c0034: `type in prepare_foreman`
- c0038 ..> c0035: `configure() calls unique_labels()`
- c0038 ..> c0035: `load_existing() calls unique_labels()`
- c0038 ..> c0038: `configure() calls inspect()`
- c0038 ..> c0038: `initialise() calls _ensure_label()`
- c0038 ..> c0038: `initialise() calls _preflight()`
- c0038 ..> c0039: `type in __init__`
- c0038 ..> c0040: `type in __init__`
- c0038 ..> c0042: `type in __init__`
- c0038 ..> c0046: `type in __init__`
- c0038 ..> c0066: `_preflight() constructs FactoryError`
- c0038 ..> c0066: `initialise() constructs FactoryError`
- c0038 ..> c0066: `inspect() constructs FactoryError`
- c0038 ..> c0066: `load_existing() constructs FactoryError`
- c0038 ..> c0066: `prepare_foreman() constructs FactoryError`
- c0038 ..> c0068: `_ensure_label() constructs Label`
- c0038 ..> c0068: `type in _preflight`
- c0038 ..> c0069: `inspect() constructs RepositoryReference`
- c0038 ..> c0069: `type in inspect`
- c0038 ..> c0070: `type in _ensure_label`
- c0038 ..> c0070: `type in _preflight`
- c0038 ..> c0071: `type in __init__`
- c0039 ..> c0033: `type in load`
- c0039 ..> c0033: `type in save`
- c0040 ..> c0033: `type in prepare_roles`
- c0040 ..> c0033: `type in record_completion`
- c0040 ..> c0033: `type in selected_launch`
- c0040 ..> c0034: `type in check`
- c0040 ..> c0034: `type in create_project`
- c0040 ..> c0034: `type in list_models`
- c0040 ..> c0034: `type in login`
- c0040 ..> c0034: `type in missing_executables`
- c0040 ..> c0034: `type in prepare`
- c0040 ..> c0034: `type in projects`
- c0040 ..> c0034: `type in uses_browser_login`
- c0040 ..> c0036: `type in prepare_roles`
- c0044 --|> c0066: `inherits`
- c0046 ..> c0070: `type in source_from_remote`
- c0047 ..> c0000: `__init__() calls __init__()`
- c0047 --|> c0066: `inherits`
- c0048 --|> c0066: `inherits`
- c0050 ..> c0012: `check() calls check()`
- c0050 ..> c0014: `check_repository() calls origin()`
- c0050 ..> c0016: `_ensure_mapping() calls ensure()`
- c0050 ..> c0016: `_ensure_mapping() calls verify_removed()`
- c0050 ..> c0016: `preflight() calls inspect()`
- c0050 ..> c0027: `_create_ownership() calls create_task()`
- c0050 ..> c0027: `_create_ownership() calls update_plan()`
- c0050 ..> c0027: `_create_plan() calls create_plan()`
- c0050 ..> c0027: `_create_plan() calls get_plan()`
- c0050 ..> c0027: `_create_plan() calls plans()`
- c0050 ..> c0027: `_ownership() calls tasks()`
- c0050 ..> c0027: `_recovery_plan() calls get_plan()`
- c0050 ..> c0027: `_recovery_plan() calls plans()`
- c0050 ..> c0027: `lookup() calls plans()`
- c0050 ..> c0027: `unfinished() calls plans()`
- c0050 ..> c0029: `_check_source() calls source_from_remote()`
- c0050 ..> c0033: `type in __init__`
- c0050 ..> c0042: `type in __init__`
- c0050 ..> c0043: `type in __init__`
- c0050 ..> c0046: `type in __init__`
- c0050 ..> c0049: `type in __init__`
- c0050 ..> c0050: `_create_ownership() calls _ownership()`
- c0050 ..> c0050: `_ensure_mapping() calls _check_source()`
- c0050 ..> c0050: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0050 ..> c0050: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0050 ..> c0050: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0050 ..> c0050: `_ensure_worktrees() calls _mapping_repository()`
- c0050 ..> c0050: `_initial_mappings() calls _repository()`
- c0050 ..> c0050: `_prepare_plan() calls _active()`
- c0050 ..> c0050: `_prepare_plan() calls _context()`
- c0050 ..> c0050: `_prepare_plan() calls _create_ownership()`
- c0050 ..> c0050: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0050 ..> c0050: `_prepare_plan() calls _setup_ownership()`
- c0050 ..> c0050: `_setup_ownership() calls _initial_mappings()`
- c0050 ..> c0050: `_setup_ownership() calls _ownership()`
- c0050 ..> c0050: `check_repository() calls _check_source()`
- c0050 ..> c0050: `preflight() calls _initial_mappings()`
- c0050 ..> c0050: `preflight() calls _repository()`
- c0050 ..> c0050: `preflight() calls check_repository()`
- c0050 ..> c0050: `prepare() calls _create_plan()`
- c0050 ..> c0050: `prepare() calls _prepare_plan()`
- c0050 ..> c0050: `prepare() calls lookup()`
- c0050 ..> c0050: `prepare() calls preflight()`
- c0050 ..> c0050: `prepare() calls recover()`
- c0050 ..> c0050: `recover() calls _active()`
- c0050 ..> c0050: `recover() calls _context()`
- c0050 ..> c0050: `recover() calls _ensure_worktrees()`
- c0050 ..> c0050: `recover() calls _ownership()`
- c0050 ..> c0050: `recover() calls _recovery_plan()`
- c0050 ..> c0050: `recover() calls _repository()`
- c0050 ..> c0050: `recover() calls _snapshot()`
- c0050 ..> c0050: `recover() calls _sole_recovery_owner()`
- c0050 ..> c0050: `recover() calls _validate_recovery_candidates()`
- c0050 ..> c0050: `recover() calls check_repository()`
- c0050 ..> c0050: `unfinished() calls _is_unfinished_factory_plan()`
- c0050 ..> c0051: `_ensure_mapping() calls _cleanup_state()`
- c0050 ..> c0056: `preflight() constructs IntakeProblem`
- c0050 ..> c0057: `_check_source() constructs RepositoryProblem`
- c0050 ..> c0057: `check_repository() constructs RepositoryProblem`
- c0050 ..> c0058: `_active() constructs ScaffoldProblem`
- c0050 ..> c0058: `_context() constructs ScaffoldProblem`
- c0050 ..> c0058: `_create_plan() constructs ScaffoldProblem`
- c0050 ..> c0058: `_ensure_mapping() constructs ScaffoldProblem`
- c0050 ..> c0058: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0050 ..> c0058: `_mapping_repository() constructs ScaffoldProblem`
- c0050 ..> c0058: `_ownership() constructs ScaffoldProblem`
- c0050 ..> c0058: `_recovery_plan() constructs ScaffoldProblem`
- c0050 ..> c0058: `_setup_ownership() constructs ScaffoldProblem`
- c0050 ..> c0058: `_snapshot() constructs ScaffoldProblem`
- c0050 ..> c0058: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0050 ..> c0058: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0050 ..> c0058: `lookup() constructs ScaffoldProblem`
- c0050 ..> c0059: `_create_plan() constructs ScaffoldReadProblem`
- c0050 ..> c0059: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0050 ..> c0059: `lookup() constructs ScaffoldReadProblem`
- c0050 ..> c0059: `prepare() constructs ScaffoldReadProblem`
- c0050 ..> c0059: `recover() constructs ScaffoldReadProblem`
- c0050 ..> c0060: `_create_ownership() constructs UncertainScaffold`
- c0050 ..> c0060: `_create_plan() constructs UncertainScaffold`
- c0050 ..> c0060: `_setup_ownership() constructs UncertainScaffold`
- c0050 ..> c0060: `_sole_recovery_owner() constructs UncertainScaffold`
- c0050 ..> c0060: `prepare() constructs UncertainScaffold`
- c0050 ..> c0066: `_is_unfinished_factory_plan() constructs FactoryError`
- c0050 ..> c0067: `_snapshot() constructs Issue`
- c0050 ..> c0067: `type in _create_plan`
- c0050 ..> c0067: `type in _initial_mappings`
- c0050 ..> c0067: `type in _prepare_plan`
- c0050 ..> c0067: `type in _setup_ownership`
- c0050 ..> c0067: `type in _snapshot`
- c0050 ..> c0067: `type in lookup`
- c0050 ..> c0067: `type in preflight`
- c0050 ..> c0067: `type in prepare`
- c0050 ..> c0067: `type in recover`
- c0050 ..> c0069: `type in _check_source`
- c0050 ..> c0069: `type in _ensure_validated_mapping`
- c0050 ..> c0069: `type in _mapping_repository`
- c0050 ..> c0069: `type in _repository`
- c0050 ..> c0069: `type in check_repository`
- c0050 ..> c0070: `_check_source() constructs WorkSource`
- c0050 ..> c0070: `_snapshot() constructs WorkSource`
- c0050 ..> c0070: `type in _repository`
- c0051 ..> c0058: `_cleanup_state() constructs ScaffoldProblem`
- c0052 --> c0067: `field issue`
- c0053 ..> c0000: `_alert_plan() calls send()`
- c0053 ..> c0000: `_check_pending_repositories() calls send()`
- c0053 ..> c0000: `_check_planning_access() calls send()`
- c0053 ..> c0000: `_handle_intake_read_problem() calls send()`
- c0053 ..> c0000: `_handle_intake_repository_problem() calls send()`
- c0053 ..> c0000: `_handle_recovery_read_problem() calls send()`
- c0053 ..> c0000: `_load_inventory() calls send()`
- c0053 ..> c0000: `_process_issue() calls send()`
- c0053 ..> c0000: `_read_issues() calls send()`
- c0053 ..> c0000: `_recover_work() calls send()`
- c0053 ..> c0000: `_submit() calls send()`
- c0053 ..> c0000: `_watch() calls close()`
- c0053 ..> c0000: `_watch() calls start()`
- c0053 ..> c0000: `_watch() calls wait()`
- c0053 ..> c0000: `run() calls startup_hint()`
- c0053 ..> c0010: `_process_issue() calls prepare()`
- c0053 ..> c0012: `_check_planning_access() calls check()`
- c0053 ..> c0029: `_read_issues() calls list_issues()`
- c0053 ..> c0033: `type in _poll_sources`
- c0053 ..> c0033: `type in _repository_for_source`
- c0053 ..> c0033: `type in _watch`
- c0053 ..> c0033: `type in run`
- c0053 ..> c0041: `type in __init__`
- c0053 ..> c0050: `_check_pending_repositories() calls check_repository()`
- c0053 ..> c0050: `_load_inventory() calls unfinished()`
- c0053 ..> c0050: `_process_issue() calls lookup()`
- c0053 ..> c0050: `_process_issue() calls recover()`
- c0053 ..> c0050: `_recover_work() calls recover()`
- c0053 ..> c0050: `type in __init__`
- c0053 ..> c0052: `_complete_intake() constructs BlockedWork`
- c0053 ..> c0052: `_handle_intake_read_problem() constructs BlockedWork`
- c0053 ..> c0052: `_handle_intake_repository_problem() constructs BlockedWork`
- c0053 ..> c0052: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0053 ..> c0052: `_process_issue() constructs BlockedWork`
- c0053 ..> c0052: `_remember_inventory_candidate() constructs BlockedWork`
- c0053 ..> c0052: `type in _alert_plan`
- c0053 ..> c0052: `type in _complete_intake`
- c0053 ..> c0052: `type in _complete_recovery`
- c0053 ..> c0052: `type in _handle_recovery_read_problem`
- c0053 ..> c0052: `type in _handle_recovery_repository_problem`
- c0053 ..> c0052: `type in _recover_work`
- c0053 ..> c0052: `type in _remember_task_ids`
- c0053 ..> c0053: `_complete_intake() calls _submit()`
- c0053 ..> c0053: `_complete_recovery() calls _submit()`
- c0053 ..> c0053: `_handle_intake_read_problem() calls _sole_task_id()`
- c0053 ..> c0053: `_handle_intake_repository_problem() calls _alert_plan()`
- c0053 ..> c0053: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0053 ..> c0053: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0053 ..> c0053: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0053 ..> c0053: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0053 ..> c0053: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0053 ..> c0053: `_load_inventory() calls _remember_inventory_candidate()`
- c0053 ..> c0053: `_poll_sources() calls _baseline_source()`
- c0053 ..> c0053: `_poll_sources() calls _process_source()`
- c0053 ..> c0053: `_poll_sources() calls _read_issues()`
- c0053 ..> c0053: `_poll_sources() calls _repository_for_source()`
- c0053 ..> c0053: `_process_issue() calls _complete_intake()`
- c0053 ..> c0053: `_process_issue() calls _handle_intake_read_problem()`
- c0053 ..> c0053: `_process_issue() calls _handle_intake_repository_problem()`
- c0053 ..> c0053: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0053 ..> c0053: `_process_issues() calls _process_issue()`
- c0053 ..> c0053: `_process_issues() calls _skip_issue()`
- c0053 ..> c0053: `_process_source() calls _include_pending_lookups()`
- c0053 ..> c0053: `_process_source() calls _process_issues()`
- c0053 ..> c0053: `_recover_blocked() calls _recover_work()`
- c0053 ..> c0053: `_recover_work() calls _alert_plan()`
- c0053 ..> c0053: `_recover_work() calls _complete_recovery()`
- c0053 ..> c0053: `_recover_work() calls _handle_recovery_read_problem()`
- c0053 ..> c0053: `_recover_work() calls _handle_recovery_repository_problem()`
- c0053 ..> c0053: `_recover_work() calls _remember_task_ids()`
- c0053 ..> c0053: `_remember_inventory_candidate() calls _alert_plan()`
- c0053 ..> c0053: `_watch() calls _check_pending_repositories()`
- c0053 ..> c0053: `_watch() calls _check_planning_access()`
- c0053 ..> c0053: `_watch() calls _load_inventory()`
- c0053 ..> c0053: `_watch() calls _poll_sources()`
- c0053 ..> c0053: `_watch() calls _recover_blocked()`
- c0053 ..> c0053: `run() calls _watch()`
- c0053 ..> c0054: `_watch() constructs _WatchState`
- c0053 ..> c0054: `type in _baseline_source`
- c0053 ..> c0054: `type in _check_pending_repositories`
- c0053 ..> c0054: `type in _check_planning_access`
- c0053 ..> c0054: `type in _complete_intake`
- c0053 ..> c0054: `type in _complete_recovery`
- c0053 ..> c0054: `type in _handle_intake_read_problem`
- c0053 ..> c0054: `type in _handle_intake_repository_problem`
- c0053 ..> c0054: `type in _handle_intake_scaffold_problem`
- c0053 ..> c0054: `type in _handle_recovery_repository_problem`
- c0053 ..> c0054: `type in _load_inventory`
- c0053 ..> c0054: `type in _poll_sources`
- c0053 ..> c0054: `type in _process_issue`
- c0053 ..> c0054: `type in _process_issues`
- c0053 ..> c0054: `type in _process_source`
- c0053 ..> c0054: `type in _recover_blocked`
- c0053 ..> c0054: `type in _recover_work`
- c0053 ..> c0054: `type in _remember_inventory_candidate`
- c0053 ..> c0054: `type in _skip_issue`
- c0053 ..> c0055: `type in _process_issue`
- c0053 ..> c0055: `type in _recover_work`
- c0053 ..> c0057: `type in _handle_intake_repository_problem`
- c0053 ..> c0057: `type in _handle_recovery_repository_problem`
- c0053 ..> c0058: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0053 ..> c0058: `type in _alert_plan`
- c0053 ..> c0058: `type in _handle_intake_scaffold_problem`
- c0053 ..> c0059: `type in _handle_intake_read_problem`
- c0053 ..> c0059: `type in _handle_recovery_read_problem`
- c0053 ..> c0061: `_check_pending_repositories() calls clear()`
- c0053 ..> c0061: `_check_planning_access() calls clear()`
- c0053 ..> c0061: `_complete_intake() calls clear()`
- c0053 ..> c0061: `_complete_recovery() calls clear()`
- c0053 ..> c0061: `_load_inventory() calls clear()`
- c0053 ..> c0061: `_process_issue() calls clear()`
- c0053 ..> c0061: `_read_issues() calls clear()`
- c0053 ..> c0061: `_watch() calls clear()`
- c0053 ..> c0061: `_watch() constructs WatcherAlerts`
- c0053 ..> c0061: `type in _alert_plan`
- c0053 ..> c0061: `type in _check_pending_repositories`
- c0053 ..> c0061: `type in _check_planning_access`
- c0053 ..> c0061: `type in _complete_intake`
- c0053 ..> c0061: `type in _complete_recovery`
- c0053 ..> c0061: `type in _handle_intake_read_problem`
- c0053 ..> c0061: `type in _handle_intake_repository_problem`
- c0053 ..> c0061: `type in _handle_intake_scaffold_problem`
- c0053 ..> c0061: `type in _handle_recovery_read_problem`
- c0053 ..> c0061: `type in _handle_recovery_repository_problem`
- c0053 ..> c0061: `type in _load_inventory`
- c0053 ..> c0061: `type in _poll_sources`
- c0053 ..> c0061: `type in _process_issue`
- c0053 ..> c0061: `type in _process_issues`
- c0053 ..> c0061: `type in _process_source`
- c0053 ..> c0061: `type in _read_issues`
- c0053 ..> c0061: `type in _recover_blocked`
- c0053 ..> c0061: `type in _recover_work`
- c0053 ..> c0061: `type in _remember_inventory_candidate`
- c0053 ..> c0066: `_read_issues() constructs FactoryError`
- c0053 ..> c0067: `type in _baseline_source`
- c0053 ..> c0067: `type in _complete_intake`
- c0053 ..> c0067: `type in _complete_recovery`
- c0053 ..> c0067: `type in _handle_intake_read_problem`
- c0053 ..> c0067: `type in _handle_intake_repository_problem`
- c0053 ..> c0067: `type in _handle_intake_scaffold_problem`
- c0053 ..> c0067: `type in _include_pending_lookups`
- c0053 ..> c0067: `type in _process_issue`
- c0053 ..> c0067: `type in _process_issues`
- c0053 ..> c0067: `type in _process_source`
- c0053 ..> c0067: `type in _read_issues`
- c0053 ..> c0067: `type in _skip_issue`
- c0053 ..> c0067: `type in _submit`
- c0053 ..> c0069: `type in _handle_intake_repository_problem`
- c0053 ..> c0069: `type in _process_issue`
- c0053 ..> c0069: `type in _process_issues`
- c0053 ..> c0069: `type in _process_source`
- c0053 ..> c0069: `type in _repository_for_source`
- c0053 ..> c0070: `_watch() constructs WorkSource`
- c0053 ..> c0070: `type in _baseline_source`
- c0053 ..> c0070: `type in _include_pending_lookups`
- c0053 ..> c0070: `type in _poll_sources`
- c0053 ..> c0070: `type in _process_source`
- c0053 ..> c0070: `type in _read_issues`
- c0053 ..> c0070: `type in _repository_for_source`
- c0053 ..> c0071: `type in __init__`
- c0054 --> c0052: `field blocked`
- c0054 --> c0052: `field known`
- c0054 --> c0067: `field pending_lookup`
- c0054 --> c0069: `field pending_repositories`
- c0054 --> c0070: `field baselined`
- c0056 --|> c0058: `inherits`
- c0057 --|> c0058: `inherits`
- c0058 --|> c0066: `inherits`
- c0059 --|> c0058: `inherits`
- c0060 --|> c0058: `inherits`
- c0061 ..> c0000: `__init__() calls __init__()`
- c0061 ..> c0000: `send() calls send()`
- c0061 ..> c0066: `type in send`
- c0062 ..> c0007: `build_watcher() constructs AgentShellTerminal`
- c0062 ..> c0012: `build_initialiser() constructs ForemanProfile`
- c0062 ..> c0012: `prepare_foreman_launch() calls pi_home()`
- c0062 ..> c0012: `prepare_foreman_launch() calls selected_launch()`
- c0062 ..> c0012: `prepare_foreman_launch() calls validate_completion()`
- c0062 ..> c0012: `prepare_foreman_launch() constructs ForemanProfile`
- c0062 ..> c0014: `build_initialiser() constructs GitRepositories`
- c0062 ..> c0014: `build_watcher() constructs GitRepositories`
- c0062 ..> c0016: `build_watcher() constructs GitWorktrees`
- c0062 ..> c0020: `build_initialiser() constructs TomlConfigurationStore`
- c0062 ..> c0026: `prepare_foreman_launch() calls role_environment()`
- c0062 ..> c0027: `build_watcher() constructs ForgetfulPlanning`
- c0062 ..> c0029: `build_initialiser() constructs GitHubWorkTracking`
- c0062 ..> c0029: `build_watcher() calls source_from_remote()`
- c0062 ..> c0029: `build_watcher() constructs GitHubWorkTracking`
- c0062 ..> c0033: `type in build_watcher`
- c0062 ..> c0033: `type in prepare_foreman_launch`
- c0062 ..> c0038: `build_initialiser() constructs InitialiseFactory`
- c0062 ..> c0038: `type in build_initialiser`
- c0062 ..> c0050: `build_watcher() constructs ScaffoldIssue`
- c0062 ..> c0053: `build_watcher() constructs WatchFactory`
- c0062 ..> c0053: `type in build_watcher`
- c0062 ..> c0062: `build_watcher() calls prepare_foreman_launch()`
- c0062 ..> c0066: `build_watcher() constructs FactoryError`
- c0062 ..> c0066: `prepare_foreman_launch() constructs FactoryError`
- c0063 --> c0033: `field config`
- c0063 --> c0034: `field connection`
- c0064 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0064 ..> c0004: `_watch_locked() calls run()`
- c0064 ..> c0006: `_change_managed_watch() calls request()`
- c0064 ..> c0006: `_foreman() calls enter_terminal()`
- c0064 ..> c0006: `_foreman() calls read_state()`
- c0064 ..> c0006: `_foreman() calls request()`
- c0064 ..> c0006: `_foreman() calls start_owner()`
- c0064 ..> c0006: `_initialise() calls enter_terminal()`
- c0064 ..> c0006: `_initialise() calls request()`
- c0064 ..> c0006: `_initialise_locked() calls read_state()`
- c0064 ..> c0006: `_launch_setup_foreman() calls start_owner()`
- c0064 ..> c0006: `_offer_factory_launch() calls read_state()`
- c0064 ..> c0006: `_watch_locked() calls read_state()`
- c0064 ..> c0006: `_watch_status() calls read_state()`
- c0064 ..> c0006: `_watch_status() calls request()`
- c0064 ..> c0012: `_complete_setup() calls record_completion()`
- c0064 ..> c0012: `_complete_setup() calls uses_browser_login()`
- c0064 ..> c0012: `_discover_worker_models() calls list_models()`
- c0064 ..> c0012: `_finish_existing_setup() calls choose_pi_home()`
- c0064 ..> c0012: `_finish_existing_setup() calls save_pi_choice()`
- c0064 ..> c0012: `_finish_existing_setup() calls selected_launch()`
- c0064 ..> c0012: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0064 ..> c0012: `_select_model() calls list_models()`
- c0064 ..> c0012: `_select_project() calls create_project()`
- c0064 ..> c0012: `_select_project() calls projects()`
- c0064 ..> c0012: `_start_initial_setup() calls begin_setup()`
- c0064 ..> c0012: `_start_initial_setup() calls choose_pi_home()`
- c0064 ..> c0012: `_validate_initial_model() calls prepare_roles()`
- c0064 ..> c0012: `_watch_status() calls validate_completion()`
- c0064 ..> c0012: `_watch_status() constructs ForemanProfile`
- c0064 ..> c0014: `select_repositories() calls discover()`
- c0064 ..> c0016: `_configure_new_factory() calls inspect()`
- c0064 ..> c0018: `_discover_worker_models() calls check_real_path()`
- c0064 ..> c0020: `_initialise_locked() calls load()`
- c0064 ..> c0021: `_initialise() calls quote()`
- c0064 ..> c0021: `_launch_setup_foreman() calls quote()`
- c0064 ..> c0021: `_select_model() calls quote()`
- c0064 ..> c0021: `_validate_setup_owner() calls quote()`
- c0064 ..> c0021: `_watch_locked() calls quote()`
- c0064 ..> c0021: `_watch_status() calls quote()`
- c0064 ..> c0022: `_foreman() calls hold()`
- c0064 ..> c0022: `_foreman() constructs WorkspaceWatchLease`
- c0064 ..> c0022: `_initialise() calls hold()`
- c0064 ..> c0022: `_initialise() constructs WorkspaceWatchLease`
- c0064 ..> c0022: `_watch() calls hold()`
- c0064 ..> c0022: `_watch() constructs WorkspaceWatchLease`
- c0064 ..> c0033: `type in _complete_setup`
- c0064 ..> c0033: `type in _configure_new_factory`
- c0064 ..> c0033: `type in _finish_existing_setup`
- c0064 ..> c0033: `type in _validate_initial_model`
- c0064 ..> c0034: `_connection() calls validate()`
- c0064 ..> c0034: `_connection() constructs ForgetfulConnection`
- c0064 ..> c0034: `type in _check_existing_connection`
- c0064 ..> c0034: `type in _configure_new_factory`
- c0064 ..> c0034: `type in _connection`
- c0064 ..> c0034: `type in _select_project`
- c0064 ..> c0036: `_configure_new_factory() constructs InitialAgentChoices`
- c0064 ..> c0036: `type in _configure_new_factory`
- c0064 ..> c0036: `type in _owner_choices`
- c0064 ..> c0036: `type in _prompt_coordinator_choices`
- c0064 ..> c0036: `type in _validate_initial_model`
- c0064 ..> c0036: `type in _worker_choices`
- c0064 ..> c0037: `_start_initial_setup() calls validate_initial_agents()`
- c0064 ..> c0038: `_complete_setup() calls check_foreman()`
- c0064 ..> c0038: `_configure_new_factory() calls configure()`
- c0064 ..> c0038: `_finish_existing_setup() calls initialise()`
- c0064 ..> c0038: `_initialise_locked() calls load_existing()`
- c0064 ..> c0038: `_launch_setup_foreman() calls check_foreman()`
- c0064 ..> c0038: `_prepare_foreman() calls prepare_foreman()`
- c0064 ..> c0038: `_start_initial_setup() calls initialise()`
- c0064 ..> c0038: `type in _complete_setup`
- c0064 ..> c0038: `type in _configure_new_factory`
- c0064 ..> c0038: `type in _discover_worker_models`
- c0064 ..> c0038: `type in _finish_existing_setup`
- c0064 ..> c0038: `type in _select_project`
- c0064 ..> c0038: `type in _start_initial_setup`
- c0064 ..> c0038: `type in _validate_initial_model`
- c0064 ..> c0038: `type in select_repositories`
- c0064 ..> c0062: `_foreman() calls prepare_foreman_launch()`
- c0064 ..> c0062: `_initialise_locked() calls build_initialiser()`
- c0064 ..> c0062: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0064 ..> c0062: `_watch_locked() calls build_watcher()`
- c0064 ..> c0063: `_start_initial_setup() constructs _InitialSetupState`
- c0064 ..> c0063: `type in _discover_worker_models`
- c0064 ..> c0063: `type in _validate_initial_model`
- c0064 ..> c0064: `_configure_new_factory() calls _prepare_foreman()`
- c0064 ..> c0064: `_configure_new_factory() calls _select_model()`
- c0064 ..> c0064: `_configure_new_factory() calls _select_numbered()`
- c0064 ..> c0064: `_configure_new_factory() calls select_repositories()`
- c0064 ..> c0064: `_connection() calls _check_existing_connection()`
- c0064 ..> c0064: `_discover_worker_models() calls _prepare_foreman()`
- c0064 ..> c0064: `_finish_existing_setup() calls _complete_setup()`
- c0064 ..> c0064: `_finish_existing_setup() calls _confirm_pi_home()`
- c0064 ..> c0064: `_finish_existing_setup() calls _connection()`
- c0064 ..> c0064: `_initialise() calls _initialise_locked()`
- c0064 ..> c0064: `_initialise() calls _offer_factory_launch()`
- c0064 ..> c0064: `_initialise_locked() calls _finish_existing_setup()`
- c0064 ..> c0064: `_initialise_locked() calls _start_initial_setup()`
- c0064 ..> c0064: `_initialise_locked() calls _validate_setup_owner()`
- c0064 ..> c0064: `_print_models() calls _safe_diagnostic()`
- c0064 ..> c0064: `_prompt_coordinator_choices() calls _select_numbered()`
- c0064 ..> c0064: `_prompt_worker() calls _select_numbered()`
- c0064 ..> c0064: `_prompt_workers() calls _prompt_worker()`
- c0064 ..> c0064: `_select_model() calls _print_models()`
- c0064 ..> c0064: `_select_model() calls _select_numbered()`
- c0064 ..> c0064: `_select_numbered() calls _safe_diagnostic()`
- c0064 ..> c0064: `_select_project() calls _listed_project_id()`
- c0064 ..> c0064: `_select_project() calls _safe_diagnostic()`
- c0064 ..> c0064: `_select_setup_route() calls _select_numbered()`
- c0064 ..> c0064: `_start_initial_setup() calls _complete_setup()`
- c0064 ..> c0064: `_start_initial_setup() calls _configure_new_factory()`
- c0064 ..> c0064: `_start_initial_setup() calls _confirm_pi_home()`
- c0064 ..> c0064: `_start_initial_setup() calls _connection()`
- c0064 ..> c0064: `_start_initial_setup() calls _launch_setup_foreman()`
- c0064 ..> c0064: `_start_initial_setup() calls _owner_choices()`
- c0064 ..> c0064: `_start_initial_setup() calls _research_choices()`
- c0064 ..> c0064: `_start_initial_setup() calls _worker_choices()`
- c0064 ..> c0064: `_validate_initial_model() calls _prepare_foreman()`
- c0064 ..> c0064: `_validate_initial_model() calls _select_model()`
- c0064 ..> c0064: `_validate_initial_model() calls _select_project()`
- c0064 ..> c0064: `_watch() calls _change_managed_watch()`
- c0064 ..> c0064: `_watch() calls _watch_locked()`
- c0064 ..> c0064: `_watch() calls _watch_status()`
- c0064 ..> c0064: `_watch_locked() calls _choose_existing()`
- c0064 ..> c0064: `_watch_locked() calls _safe_diagnostic()`
- c0064 ..> c0064: `_worker_choices() calls _prompt_coordinator_choices()`
- c0064 ..> c0064: `_worker_choices() calls _prompt_workers()`
- c0064 ..> c0064: `_worker_choices() calls _select_setup_route()`
- c0064 ..> c0064: `_worker_choices() calls _worker_arguments()`
- c0064 ..> c0064: `main() calls _foreman()`
- c0064 ..> c0064: `main() calls _initialise()`
- c0064 ..> c0064: `main() calls _parse_arguments()`
- c0064 ..> c0064: `main() calls _safe_diagnostic()`
- c0064 ..> c0064: `main() calls _watch()`
- c0064 ..> c0065: `_foreman() calls load_configuration()`
- c0064 ..> c0065: `_watch_locked() calls load_configuration()`
- c0064 ..> c0065: `_watch_status() calls load_configuration()`
- c0064 ..> c0066: `_change_managed_watch() constructs FactoryError`
- c0064 ..> c0066: `_check_existing_connection() constructs FactoryError`
- c0064 ..> c0066: `_choose_existing() constructs FactoryError`
- c0064 ..> c0066: `_configure_new_factory() constructs FactoryError`
- c0064 ..> c0066: `_foreman() constructs FactoryError`
- c0064 ..> c0066: `_initialise() constructs FactoryError`
- c0064 ..> c0066: `_initialise_locked() constructs FactoryError`
- c0064 ..> c0066: `_install_missing() constructs FactoryError`
- c0064 ..> c0066: `_listed_project_id() constructs FactoryError`
- c0064 ..> c0066: `_prompt_coordinator_choices() constructs FactoryError`
- c0064 ..> c0066: `_prompt_worker() constructs FactoryError`
- c0064 ..> c0066: `_select_model() constructs FactoryError`
- c0064 ..> c0066: `_select_numbered() constructs FactoryError`
- c0064 ..> c0066: `_select_project() constructs FactoryError`
- c0064 ..> c0066: `_validate_setup_owner() constructs FactoryError`
- c0064 ..> c0066: `_watch_locked() constructs FactoryError`
- c0064 ..> c0066: `_worker_choices() constructs FactoryError`
- c0064 ..> c0066: `main() constructs FactoryError`
- c0064 ..> c0066: `select_repositories() constructs FactoryError`
- c0065 ..> c0020: `load_configuration() calls load()`
- c0065 ..> c0020: `load_configuration() constructs TomlConfigurationStore`
- c0065 ..> c0033: `type in load_configuration`
- c0065 ..> c0066: `load_configuration() constructs FactoryError`
- c0067 --> c0070: `field source`
- c0069 --> c0070: `field work_source`
- c0071 ..> c0067: `type in list_issues`
- c0071 ..> c0068: `type in create_label`
- c0071 ..> c0068: `type in list_labels`
- c0071 ..> c0070: `type in check_access`
- c0071 ..> c0070: `type in create_label`
- c0071 ..> c0070: `type in list_issues`
- c0071 ..> c0070: `type in list_labels`

## Type key

- Type1: `object | None`
- Type2: `int | None`
- Type3: `str | None`
- Type4: `tuple[Path, Path, int]`
- Type5: `dict | None`
- Type6: `dict[str, str] | None`
- Type7: `subprocess.Popen | None`
- Type8: `dict[tuple[str, Path], list[str]]`
- Type9: `Path | None`
- Type10: `tuple[Path, list[dict]]`
- Type11: `tuple[Path, Path] | None`
- Type12: `dict[Path, None]`
- Type13: `frozenset[tuple[int, int]]`
- Type14: `FactoryConfiguration | None`
- Type15: `dict[str, str]`
- Type16: `tuple[Label, ...]`
- Type17: `tuple[Issue, ...]`
- Type18: `tuple[str, ...]`
- Type19: `tuple[Path, ...]`
- Type20: `float | None`
- Type21: `tuple[RepositoryReference, ...]`
- Type22: `ForgetfulConnection | None`
- Type23: `Callable[[list[str]], None]`
- Type24: `Callable[[str, str], bool]`
- Type25: `list[Path] | None`
- Type26: `list[str] | None`
- Type27: `dict[str, RepositoryReference]`
- Type28: `dict[WorkSource, tuple[Label, ...]]`
- Type29: `Callable[[], FactoryConfiguration | None]`
- Type30: `tuple[list[dict], list[dict]]`
- Type31: `tuple[Issue, dict] | None`
- Type32: `Issue | None`
- Type33: `tuple[int, ...] | None`
- Type34: `tuple[int, ...]`
- Type35: `Callable[[], bool]`
- Type36: `Callable[[str], None]`
- Type37: `tuple[set[str], bool]`
- Type38: `tuple[WorkSource, ...]`
- Type39: `dict[str, Issue]`
- Type40: `BlockedWork | None`
- Type41: `tuple[Issue, ...] | None`
- Type42: `dict[str, BlockedWork]`
- Type43: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type44: `list[str] | tuple[str, ...]`
- Type45: `int | dict`
- Type46: `int | dict | str`
- Type47: `str | Path`

## Signature key

- Signature1: `+interact(session: unknown, reader: unknown, reply: unknown, name: unknown,
  persistent: unknown, startup_warning: unknown) None`
- Signature2: `+open_session(state: unknown, shell: unknown, resources_type: unknown, config:
  unknown, reply: unknown, opened: unknown) None`
- Signature3: `+replace_failed_exit_task(state: unknown, exit_task: unknown, session: unknown,
  config: unknown, reply: unknown, failed: unknown) unknown`
- Signature4: `+supervise_session(state: unknown, reader: unknown, config: unknown, reply: unknown)
  None`
- Signature5: `-_remove_control_socket(server: unknown, endpoint: unknown, socket_identity: unknown)
  None`
- Signature6: `-_cleanup(server: unknown, endpoint: unknown, socket_identity: unknown, observer:
  unknown, disconnected: unknown) None`
- Signature7: `+main(workspace: unknown, python: unknown, directory: unknown, endpoint: unknown,
  handover: unknown) unknown`
- Signature8: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None, model: str | None, effort: str | None) unknown`
- Signature9: `-_write_agent(name: unknown, model: unknown, effort: unknown, description: unknown,
  children: unknown, resources: unknown) unknown`
- Signature10: `-_validate_registered_worktree(root: Path, target: Path, branch: str, path: str,
  match: dict) None`
- Signature11: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature12: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool)
  unknown`
- Signature13: `-__init__(tracking: WorkTrackingService, storage: ConfigurationStore, repositories:
  LocalRepositories, sources: WorkSourceResolver, profile: ForemanProfile) unknown`
- Signature14: `-__init__(planning: Planning, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, sources: WorkSourceResolver) unknown`
- Signature15: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature16: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature17: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature18: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, scaffold:
  ScaffoldIssue) unknown`
- Signature19: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature20: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature21: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature22: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature23: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature24: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature25: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Issue, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature26: `-_poll_sources(sources: tuple[WorkSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature27: `-_process_source(source: WorkSource, issues: tuple[Issue, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature28: `-_baseline_source(source: WorkSource, issues: tuple[Issue, ...], state: _WatchState,
  report: Callable[[str], None]) None`
- Signature29: `-_repository_for_source(config: FactoryConfiguration, source: WorkSource)
  RepositoryReference`
- Signature30: `-_include_pending_lookups(source: WorkSource, current: dict[str, Issue],
  pending_lookup: dict[str, Issue]) None`
- Signature31: `-_process_issues(issues: tuple[Issue, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature32: `-_process_issue(issue: Issue, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature33: `-_handle_intake_repository_problem(issue: Issue, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature34: `-_handle_intake_read_problem(issue: Issue, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature35: `-_handle_intake_scaffold_problem(issue: Issue, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature36: `-_complete_intake(issue: Issue, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature37: `-_submit(issue: Issue, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature38: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature39: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature40: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown) WatchFactory`
- Signature41: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown) unknown`
- Signature42: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature43: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature44: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature45: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature46: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature47: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature48: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature49: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature50: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature51: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature52: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path) int`
- Signature53: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature54: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature55: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None) int | dict`
- Signature56: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown) unknown`

## Extraction warnings

- `Unresolved or out-of-scope base: ConfigurationStore -> Protocol`
- `Unresolved or out-of-scope base: FactoryError -> Exception`
- `Unresolved or out-of-scope base: ForemanProfile -> Protocol`
- `Unresolved or out-of-scope base: ForemanTerminal -> Protocol`
- `Unresolved or out-of-scope base: LocalRepositories -> Protocol`
- `Unresolved or out-of-scope base: Planning -> Protocol`
- `Unresolved or out-of-scope base: WatchLease -> Protocol`
- `Unresolved or out-of-scope base: WorkSourceResolver -> Protocol`
- `Unresolved or out-of-scope base: WorkTrackingService -> Protocol`
- `Unresolved or out-of-scope base: Worktrees -> Protocol`
- `Unresolved or out-of-scope base: _WorkAction -> Enum`
