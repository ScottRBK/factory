# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 96 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 5056. Type relationships removed: 87.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/deadline_support.py`: 2 source occurrences (test-path).
- `tests/fixtures/previous-pi-forgetful-factory.ts`: 18 source occurrences (test-path).
- `tests/lifecycle_support.py`: 21 source occurrences (test-path).
- `tests/poll_support.py`: 9 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_agent_definitions.py`: 21 source occurrences (test-path).
- `tests/test_architecture.py`: 20 source occurrences (test-path).
- `tests/test_assisted_lifecycle.py`: 16 source occurrences (test-path).
- `tests/test_assisted_review_fixes.py`: 20 source occurrences (test-path).
- `tests/test_assisted_setup.py`: 14 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_cleanup_boundaries.py`: 19 source occurrences (test-path).
- `tests/test_cleanup_performance.py`: 24 source occurrences (test-path).
- `tests/test_cleanup_receipts.py`: 11 source occurrences (test-path).
- `tests/test_cleanup_recovery.py`: 12 source occurrences (test-path).
- `tests/test_cleanup_review.py`: 25 source occurrences (test-path).
- `tests/test_cleanup_scheduling.py`: 5 source occurrences (test-path).
- `tests/test_completed_cleanup.py`: 28 source occurrences (test-path).
- `tests/test_completed_cleanup_recovery.py`: 27 source occurrences (test-path).
- `tests/test_configuration.py`: 14 source occurrences (test-path).
- `tests/test_definition_of_done.py`: 12 source occurrences (test-path).
- `tests/test_definition_of_done_lifecycle.py`: 3 source occurrences (test-path).
- `tests/test_definition_of_done_watch.py`: 2 source occurrences (test-path).
- `tests/test_factory_maintenance.py`: 9 source occurrences (test-path).
- `tests/test_foreman_issue_intake.py`: 4 source occurrences (test-path).
- `tests/test_foreman_memory_setup.py`: 21 source occurrences (test-path).
- `tests/test_foreman_setup_repair.py`: 31 source occurrences (test-path).
- `tests/test_github_issue_changes.py`: 4 source occurrences (test-path).
- `tests/test_init.py`: 47 source occurrences (test-path).
- `tests/test_init_launch.py`: 13 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 20 source occurrences (test-path).
- `tests/test_local_skills.py`: 21 source occurrences (test-path).
- `tests/test_managed_watcher_alerts.py`: 10 source occurrences (test-path).
- `tests/test_native_assisted_reload.py`: 3 source occurrences (test-path).
- `tests/test_native_roles.py`: 15 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_normalized_lifecycle.py`: 14 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_owner_startup.py`: 22 source occurrences (test-path).
- `tests/test_pi_runtime_install.py`: 3 source occurrences (test-path).
- `tests/test_planning_adapter.py`: 18 source occurrences (test-path).
- `tests/test_planning_setup.py`: 12 source occurrences (test-path).
- `tests/test_planning_watch.py`: 31 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_resource_update.py`: 18 source occurrences (test-path).
- `tests/test_review_regressions.py`: 54 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 24 source occurrences (test-path).
- `tests/test_watch.py`: 62 source occurrences (test-path).
- `tests/test_watch_issue_changes.py`: 3 source occurrences (test-path).
- `tests/test_watch_lock.py`: 6 source occurrences (test-path).
- `tests/test_watch_status.py`: 22 source occurrences (test-path).
- `tests/test_watch_status_review.py`: 35 source occurrences (test-path).
- `tests/test_watch_stop.py`: 10 source occurrences (test-path).
- `tests/test_watcher_alerts.py`: 62 source occurrences (test-path).
- `tests/test_watcher_cancellation.py`: 5 source occurrences (test-path).
- `tests/test_watcher_followup.py`: 35 source occurrences (test-path).
- `tests/test_watcher_guidance.py`: 2 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 19 source occurrences (test-path).
- `tests/test_worker_profiles.py`: 3 source occurrences (test-path).
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
        +deadlines: unknown
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
        +start_owner(Signature8)
        +enter_terminal(target: dict) None
    }
    class c0007["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature9)
        +python: unknown
        +environment: unknown
        +resources: unknown
        +prompt: unknown
        +cwd: unknown
        +model: unknown
        +effort: unknown
        +deadlines: unknown
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
    class c0008["src/forgetful_factory/adapters/filesystem/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        -_local_selection(value: object, field: str, message: str) str
        -_validate_agent(value: object) dict
        -_validate_roster(path: Path, value: object, agent_type: str) None
        -_validate_resources(value: object) None
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0009["FileCleanupReceipts"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +path: unknown
        +load() set[CleanupSet]
        -_load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0010["src/forgetful_factory/adapters/filesystem/cleanup_receipts.py"] {
        <<module>>
        -_unique_object(pairs: unknown) unknown
        -_resource(value: object) CleanupSet
    }
    class c0011["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(config: FactoryConfiguration, choices: unknown) None
        -_write_foreman_memory(choices: unknown) None
        -_write_agent(Signature10)
        +validate_guidance(config: FactoryConfiguration) None
    }
    class c0012["src/forgetful_factory/adapters/filesystem/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0013["ForemanProfile"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +term_grace: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type5
        -_model_catalogs: Type8
        -_managed_memory_selected: Type9
        +prepare_setup_guidance() None
        +missing_executables(connection: ForgetfulConnection) list[str]
        +role_runtime_ready() bool
        +validate_setup(Signature11)
        +validate_bundled_resources(include_memory_extension: bool) None
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
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type10) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(config: FactoryConfiguration) dict
        +managed_memory_notice() Type3
        +record_completion(config: FactoryConfiguration) bool
        +begin_setup() None
        +validate_completion(_config: FactoryConfiguration) None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0014["src/forgetful_factory/adapters/filesystem/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0015["GitRepositories"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0016["src/forgetful_factory/adapters/filesystem/git_repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0017["GitWorktrees"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +cleanup_defaults: Type11
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        -_read_git(arguments: list[str]) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type12
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type13
        -_validate_registered_worktree(Signature12)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
        -_disposal_state(Signature13)
        -_validate_disposal_origin(root: Path, remote: str, path: str) None
        -_validate_disposal_path(root: Path, target: Path, repository: str, path: str) None
        -_validate_disposal_refs(root: Path, branch: str, target_branch: str, path: str) None
        -_network_git(arguments: list[str]) str
        -_network_read(arguments: list[str]) str
        -_remote_default(root: Path) list[str]
        +cleanup_defaults#91;key#93;: unknown
        -_dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
        -_verify_local_ref_absent(root: Path, ref: str, path: str) None
    }
    class c0018["src/forgetful_factory/adapters/filesystem/git_worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0019["ResourceUpdate"] {
        <<class>>
        +directory: Path
        +files: Type15
        +add: Type16
        +replace: Type16
        +edited: Type16
    }
    class c0020["src/forgetful_factory/adapters/filesystem/role_resources.py"] {
        <<module>>
        -_digest(data: bytes) str
        +bundled_files() Type15
        +plan_update(directory: Path) ResourceUpdate
        -_back_up(update: ResourceUpdate, backups: Path) Path
        +apply_update(update: ResourceUpdate, backups: Path) Type10
    }
    class c0021["src/forgetful_factory/adapters/filesystem/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type17) None
        -_walk_skill_directory(directory: Path, ancestors: Type18, files: Type17) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0022["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type19
        +save(configuration: FactoryConfiguration) None
    }
    class c0023["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0024["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0025["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0026["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0027["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +role: unknown
        +term_grace: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type20
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0028["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature14)
        -_catalog_tools(catalog: object) dict
    }
    class c0029["ForgetfulPlanning"] {
        <<class>>
        -__init__(Signature15)
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
    class c0030["src/forgetful_factory/adapters/forgetful/planning.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0031["GitHubWorkTracking"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +check_cli() None
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type21
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type16) Type22
        -_issue(source: WorkSource, item: dict) Issue
        -_comments(source: WorkSource, number: int) Type23
        -_milestone(item: object) object
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0032["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +runtime: unknown
        +term_grace: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type6) Type20
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type6) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0033["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type24) str
        +runtime_ready(runtime: Path, inputs: Type24, probe: str, term_grace: float) bool
    }
    class c0034["ObservedTerminal"] {
        <<class>>
        -__init__(terminal: ForemanTerminal, observation: PlainWatchObservation) unknown
        +terminal: unknown
        +observation: unknown
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0035["PlainWatchObservation"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +lock: unknown
        +finished: unknown
        +listener: unknown
        +thread: unknown
        +state: unknown
        +update(fields: unknown) None
        +snapshot() dict
        -_publish_history(current: dict) None
        -__enter__() unknown
        -_serve() None
        -_close_resources() None
        -__exit__(_: unknown) unknown
    }
    class c0036["src/forgetful_factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type25
        -_read_discovery(workspace: Path) dict
        +unknown_status(source: str, observation: str) dict
        +plain_watch_status(workspace: Path) Type5
        +observe_plain_watch(workspace: Path, report_unavailable: Type27) Type26
    }
    class c0037["CleanupCompleted"] {
        <<class>>
        -__init__(Signature16)
        +records: unknown
        +worktrees: unknown
        +owners: Type28
        +receipts: unknown
        +confirmed: set[CleanupSet]
        +cursor: Type29
        +poll(alerts: WatcherAlerts, report: unknown) None
        -_claim_indexes(Signature17)
        -_read_plans(inventory: list[dict], alerts: WatcherAlerts) Type32
        -_candidates(plans: list[dict], tasks: Type31, alerts: WatcherAlerts) Type33
        -_candidate(plan: dict, tasks: list[dict]) CompletedWork
        -_read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) None
        -_in_scope(plan: dict) bool
        -_repository_identities(alerts: WatcherAlerts) Type6
        -_keys(mapping: dict, identities: Type20) set[tuple]
        -_claims(tasks: list[dict], plan_id: int, claims: dict, identities: Type20) None
        -_task_mappings(task: dict) list[dict]
        -_validate_claim_mapping(mapping: object) None
        -_overlaps(mapping: dict, claims: dict) bool
        -_dispose(Signature18)
        -_order(work: CompletedWork, mapping: dict) tuple
        -_check_namespaces(mappings: list[dict], identities: Type20) None
        -_mapping_identity(Signature19)
        -_is_confirmed(plan_id: int, reference: str, mapping: dict, workspace: Type3) bool
        -_still_completed(work: CompletedWork) bool
    }
    class c0038["CompletedWork"] {
        <<class>>
        +plan_id: int
        +reference: str
        +task_id: int
        +mappings: list[dict]
    }
    class c0039["src/forgetful_factory/application/cleanup_completed.py"] {
        <<module>>
        -_claim_path(value: str) str
    }
    class c0040["CleanupMarkerError"] {
        <<class>>
    }
    class c0041["src/forgetful_factory/application/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict) Type34
    }
    class c0042["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type16
        +foreman_agent_file: str
        +repository: Type35
        +forgetful: Type36
        +execution_enabled: bool
    }
    class c0043["ForgetfulConnection"] {
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
    class c0044["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type36
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type16
    }
    class c0045["FactoryRecords"] {
        <<class>>
        -__init__(Signature20)
        +planning: unknown
        +workspace: unknown
        +config: unknown
        +repositories: unknown
        +sources: unknown
        +check_repository(repository: RepositoryReference) None
        +check_source(repository: RepositoryReference) None
        +snapshot(context: dict, external_ref: str) Issue
        +active(plan: dict) bool
        +context(plan: dict) dict
        +ownership(plan_id: int, external_ref: str) list[dict]
        +ownership_records(plan_id: int, external_ref: str, tasks: list[dict]) list[dict]
        +mapping_repository(mapping: dict, seen: set[str]) RepositoryReference
    }
    class c0046["InitialAgentChoices"] {
        <<class>>
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +foreman_memory_enabled: bool
        +foreman_memory_model: Type3
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
        +implementation_skills: Type16
        +review_skills: Type16
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0047["src/forgetful_factory/application/initial_agent_choices.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type16
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0048["InitialiseFactory"] {
        <<class>>
        -__init__(Signature21)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type37, confirm: Type38) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type39, labels: Type40) Type19
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type41
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type42
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type43, save: bool) list[str]
    }
    class c0049["CleanupReceipts"] {
        <<class>>
        +load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0050["CleanupSet"] {
        <<class>>
        +workspace: str
        +backend: str
        +plan_id: int
        +external_ref: str
        +repository: str
        +local_dir: str
        +branch: str
        +path: str
        +overlaps(other: Type44) bool
    }
    class c0051["ConfigurationStore"] {
        <<class>>
        +load() Type19
        +save(configuration: FactoryConfiguration) None
    }
    class c0052["ForemanProfile"] {
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
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type10) list[str]
        +managed_memory_notice() Type3
        +record_completion(config: FactoryConfiguration) bool
        +begin_setup() None
    }
    class c0053["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0054["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0055["Planning"] {
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
    class c0056["PlanningReadError"] {
        <<class>>
    }
    class c0057["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0058["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0059["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type3) unknown
        +code: unknown
        +paths: unknown
    }
    class c0060["WorktreeReadError"] {
        <<class>>
    }
    class c0061["Worktrees"] {
        <<class>>
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
    }
    class c0062["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature22)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +records: unknown
        +check() None
        +check_repository(repository: RepositoryReference) None
        +prepare(issue: Issue) Type5
        -_repository(source: WorkSource) RepositoryReference
        -_initial_mappings(issue: Issue) list[dict]
        +preflight(issue: Issue) list[dict]
        -_prepare_plan(issue: Issue, plan: dict, initial_mappings: list[dict]) Type5
        -_setup_ownership(Signature23)
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature24)
        +lookup(issue: Issue) Type2
        -_create_plan(issue: Issue) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type47, task_ids: Type48) Type46
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature25)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_is_unfinished_factory_plan(summary: dict, sources: set[str]) bool
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_validated_mapping(Signature26)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0063["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type2
        +issue: Type47
        +task_ids: Type48
        +recovered: bool
        +setup_paths: Type16
        +setup_cause: Type3
    }
    class c0064["WatchFactory"] {
        <<class>>
        -__init__(Signature27)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +cleanup: unknown
        +run(Signature28)
        -_watch(Signature29)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type27) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature30)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type27) Type51
        -_recover_work(Signature31)
        -_handle_recovery_repository_problem(Signature32)
        -_handle_recovery_read_problem(Signature33)
        -_remember_task_ids(work: BlockedWork, task_ids: Type48) None
        -_complete_recovery(Signature34)
        -_poll_sources(Signature35)
        -_process_source(Signature36)
        -_baseline_source(Signature37)
        -_repository_for_source(Signature38)
        -_include_pending_lookups(Signature39)
        -_process_issues(Signature40)
        -_skip_issue(issue: Issue, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature41)
        -_handle_intake_repository_problem(Signature42)
        -_handle_intake_read_problem(Signature43)
        -_handle_intake_scaffold_problem(Signature44)
        -_complete_intake(Signature45)
        -_sole_task_id(task_ids: Type48) Type2
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature46)
        -_read_issues(source: WorkSource, labels: Type16, alerts: WatcherAlerts) Type55
    }
    class c0065["_WatchState"] {
        <<class>>
        +seen: Type20
        +baseline: Type20
        +baselined: set[WorkSource]
        +blocked: Type56
        +pending_lookup: Type53
        +known: Type56
        +recovered: set[str]
        +pending_repositories: Type41
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0066["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0067["IntakeProblem"] {
        <<class>>
    }
    class c0068["RepositoryProblem"] {
        <<class>>
    }
    class c0069["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature47)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0070["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0071["UncertainScaffold"] {
        <<class>>
    }
    class c0072["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type20
        +last_diagnostic: Type20
        +clear(subject: str) None
        +send(Signature48)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0073["src/forgetful_factory/application/watcher_problems.py"] {
        <<module>>
        -_cleanup_recovery(code: str) str
    }
    class c0074["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +build_watcher(Signature49)
        +prepare_foreman_launch(Signature50)
    }
    class c0075["src/forgetful_factory/cli/definition_of_done.py"] {
        <<module>>
        +agree_definition_of_done(workspace: Path, config: FactoryConfiguration) bool
        -_deployment_agreement(answer: str) str
    }
    class c0076["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0077["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature51)
        -_check_existing_connection(Signature52)
        -_connection(Signature53)
        -_prepare_foreman(Signature54)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type58, show_choices: bool, prompt: Type3) str
        -_select_model(Signature55)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_change_managed_watch(args: argparse.Namespace, workspace: Path) int
        -_managed_watch_status(workspace: Path) Type5
        -_watch_status(workspace: Path) int
        -_watch(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_foreman(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_watch_locked(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature56)
        -_owner_choices(Signature57)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature58)
        -_foreman_memory_choices(Signature59)
        -_managed_rest_mapping_available(connection: ForgetfulConnection) bool
        -_worker_choices(Signature60)
        -_complete_setup(Signature61)
        -_initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type5) None
        -_finish_existing_setup(Signature62)
        -_discover_worker_models(Signature63)
        -_validate_initial_model(Signature64)
        -_start_initial_setup(Signature65)
        -_initialise_locked(Signature66)
        -_launch_setup_foreman(Signature67)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0078["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0079["src/forgetful_factory/cli/resource_update.py"] {
        <<module>>
        -_report(update: unknown, force: bool) None
        +update_resources(Signature68)
    }
    class c0080["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type61) FactoryConfiguration
    }
    class c0081["AgentShellLifecycleDeadlines"] {
        <<class>>
        +controller_ready: float
        +controller_send: float
        +controller_close: float
        +parent_ready: float
        +owner_watcher_start: float
        +owner_watcher_stop: float
        +owner_ready: float
        +owner_controller_close: float
        +owner_pre_adoption_cleanup: float
        -__post_init__() None
    }
    class c0082["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0083["src/forgetful_factory/deadlines.py"] {
        <<module>>
        -_validate_duration(name: str, value: object) None
    }
    class c0084["Issue"] {
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
    class c0085["Label"] {
        <<class>>
        +name: str
    }
    class c0086["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0087["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0088["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type21
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type16) Type22
    }
    class c0089["src/forgetful_factory/shared/command.py"] {
        <<module>>
        +run_command(arguments: list[str], timeout: float, env: Type6, stdin: Type2) str
    }
    class c0090["FactoryError"] {
        <<class>>
    }
    class c0091["src/forgetful_factory/shared/resource_files.py"] {
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
    class c0092["src/forgetful_factory/shared/resources.py"] {
        <<module>>
        +resource_root() Path
    }
    class c0093["src/forgetful_factory/shared/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen, term_grace: float) None
        +run_owned(Signature69)
    }
    class c0094["WatchStop"] {
        <<class>>
        +requested: bool
        +interrupt(_signum: unknown, _frame: unknown) None
    }
    class c0095["src/forgetful_factory/shared/watch_stop.py"] {
        <<module>>
        +watch_stop_scope() unknown
        +check_watch_stop() None
    }
    c0000 ..> c0000 : 2 relationships (see list)
    c0000 ..> c0007 : close() calls close()
    c0000 ..> c0090 : 2 relationships (see list)
    c0000 ..> c0095 : 2 relationships (see list)
    c0002 ..> c0000 : 6 relationships (see list)
    c0002 ..> c0001 : serve() constructs SessionState
    c0002 ..> c0002 : 17 relationships (see list)
    c0002 ..> c0029 : 4 relationships (see list)
    c0003 ..> c0013 : main() calls list_models()
    c0004 ..> c0000 : 11 relationships (see list)
    c0004 ..> c0004 : 27 relationships (see list)
    c0004 ..> c0005 : 2 relationships (see list)
    c0004 ..> c0023 : _apply_controller_problem() calls quote()
    c0004 ..> c0029 : 2 relationships (see list)
    c0004 ..> c0081 : 2 relationships (see list)
    c0004 ..> c0090 : 10 relationships (see list)
    c0004 ..> c0091 : save() calls replace_generated_json()
    c0005 ..> c0000 : 3 relationships (see list)
    c0005 ..> c0004 : 3 relationships (see list)
    c0005 ..> c0005 : 5 relationships (see list)
    c0005 ..> c0006 : _prepare_owner_startup() calls read_state()
    c0005 ..> c0014 : _prepare_owner_startup() calls runtime_directory()
    c0005 ..> c0023 : _acquire_owner_lock() calls quote()
    c0005 ..> c0029 : main() calls create_task()
    c0005 ..> c0090 : 3 relationships (see list)
    c0006 ..> c0000 : 2 relationships (see list)
    c0006 ..> c0004 : 2 relationships (see list)
    c0006 ..> c0006 : 3 relationships (see list)
    c0006 ..> c0014 : 3 relationships (see list)
    c0006 ..> c0023 : request() calls quote()
    c0006 ..> c0081 : 2 relationships (see list)
    c0006 ..> c0090 : 5 relationships (see list)
    c0006 ..> c0091 : read_state() calls read_generated_json()
    c0007 ..> c0000 : close() calls close()
    c0007 ..> c0007 : 5 relationships (see list)
    c0007 ..> c0081 : 2 relationships (see list)
    c0007 ..> c0090 : 4 relationships (see list)
    c0007 ..> c0095 : 3 relationships (see list)
    c0008 ..> c0008 : 8 relationships (see list)
    c0008 ..> c0044 : 4 relationships (see list)
    c0008 ..> c0090 : 2 relationships (see list)
    c0009 ..> c0000 : _load() calls close()
    c0009 ..> c0009 : 2 relationships (see list)
    c0009 ..> c0010 : _load() calls _resource()
    c0009 ..> c0050 : 3 relationships (see list)
    c0009 ..> c0090 : 2 relationships (see list)
    c0009 ..> c0091 : 2 relationships (see list)
    c0009 ..> c0095 : confirm() calls check_watch_stop()
    c0010 ..> c0050 : 2 relationships (see list)
    c0011 ..> c0011 : 3 relationships (see list)
    c0011 ..> c0012 : prepare() calls selected_resources()
    c0011 ..> c0013 : prepare() calls prepare()
    c0011 ..> c0025 : __init__() constructs WorkerProfiles
    c0011 ..> c0042 : 2 relationships (see list)
    c0011 ..> c0090 : 4 relationships (see list)
    c0011 ..> c0091 : 5 relationships (see list)
    c0013 ..> c0008 : selected_launch() calls foreman_launch()
    c0013 ..> c0009 : choose_pi_home() calls confirm()
    c0013 ..> c0011 : 4 relationships (see list)
    c0013 ..> c0013 : 23 relationships (see list)
    c0013 ..> c0020 : _install_resources() calls bundled_files()
    c0013 ..> c0021 : selected_launch() calls selected_skill_files()
    c0013 ..> c0023 : require_pi_home() calls quote()
    c0013 ..> c0026 : uses_browser_login() calls uses_browser_login()
    c0013 ..> c0027 : 8 relationships (see list)
    c0013 ..> c0028 : list_models() calls role_environment()
    c0013 ..> c0032 : 6 relationships (see list)
    c0013 ..> c0033 : 4 relationships (see list)
    c0013 ..> c0042 : 4 relationships (see list)
    c0013 ..> c0043 : 9 relationships (see list)
    c0013 ..> c0090 : 14 relationships (see list)
    c0013 ..> c0091 : 11 relationships (see list)
    c0013 ..> c0093 : list_models() calls run_owned()
    c0014 ..> c0090 : runtime_directory() constructs FactoryError
    c0014 ..> c0091 : runtime_directory() calls check_real_path()
    c0015 ..> c0016 : origin() calls _resolve_repository()
    c0015 ..> c0089 : origin() calls run_command()
    c0015 ..> c0090 : origin() constructs FactoryError
    c0016 ..> c0090 : _resolve_repository() constructs FactoryError
    c0017 ..> c0017 : 35 relationships (see list)
    c0017 ..> c0018 : _repository_entries() calls _worktree_entries()
    c0017 ..> c0023 : _network_git() calls quote()
    c0017 ..> c0059 : 14 relationships (see list)
    c0017 ..> c0060 : 6 relationships (see list)
    c0017 ..> c0072 : begin_cleanup_cycle() calls clear()
    c0017 ..> c0089 : 4 relationships (see list)
    c0017 --> c0090 : field cleanup_defaults
    c0017 ..> c0090 : ensure() constructs FactoryError
    c0017 ..> c0095 : ensure() calls check_watch_stop()
    c0020 ..> c0019 : 4 relationships (see list)
    c0020 ..> c0020 : 4 relationships (see list)
    c0020 ..> c0090 : 2 relationships (see list)
    c0020 ..> c0091 : plan_update() calls check_real_path()
    c0021 ..> c0000 : _add_skill_file() calls close()
    c0021 ..> c0021 : 3 relationships (see list)
    c0021 ..> c0090 : 3 relationships (see list)
    c0022 ..> c0000 : 2 relationships (see list)
    c0022 ..> c0009 : load() calls load()
    c0022 ..> c0023 : save() calls quote()
    c0022 ..> c0042 : 2 relationships (see list)
    c0022 ..> c0044 : load() calls from_mapping()
    c0022 ..> c0090 : 2 relationships (see list)
    c0024 ..> c0000 : _hold_directory() calls close()
    c0024 ..> c0024 : hold() calls _hold_directory()
    c0024 ..> c0090 : _hold_directory() constructs FactoryError
    c0025 ..> c0035 : prepare() calls update()
    c0025 ..> c0046 : type in prepare
    c0025 ..> c0091 : 3 relationships (see list)
    c0026 ..> c0006 : uses_browser_login() calls request()
    c0026 ..> c0043 : type in uses_browser_login
    c0027 ..> c0027 : 7 relationships (see list)
    c0027 ..> c0028 : 2 relationships (see list)
    c0027 ..> c0043 : 7 relationships (see list)
    c0027 ..> c0090 : 5 relationships (see list)
    c0027 ..> c0093 : 2 relationships (see list)
    c0027 ..> c0095 : command() calls check_watch_stop()
    c0028 ..> c0033 : role_environment() calls executable_path()
    c0028 ..> c0035 : role_environment() calls update()
    c0028 ..> c0043 : type in role_environment
    c0029 ..> c0013 : check() calls check()
    c0029 ..> c0027 : 2 relationships (see list)
    c0029 ..> c0029 : 12 relationships (see list)
    c0029 ..> c0030 : 3 relationships (see list)
    c0029 ..> c0043 : type in __init__
    c0029 ..> c0056 : 4 relationships (see list)
    c0031 ..> c0031 : 9 relationships (see list)
    c0031 ..> c0084 : 3 relationships (see list)
    c0031 ..> c0085 : 3 relationships (see list)
    c0031 ..> c0087 : 10 relationships (see list)
    c0031 ..> c0089 : 2 relationships (see list)
    c0031 ..> c0090 : 9 relationships (see list)
    c0032 ..> c0032 : 15 relationships (see list)
    c0032 ..> c0033 : 3 relationships (see list)
    c0032 ..> c0090 : 6 relationships (see list)
    c0032 ..> c0091 : install() calls write_new()
    c0032 ..> c0093 : 4 relationships (see list)
    c0033 ..> c0033 : runtime_ready() calls sync_fingerprint()
    c0033 ..> c0093 : runtime_ready() calls run_owned()
    c0034 ..> c0000 : 5 relationships (see list)
    c0034 ..> c0035 : 3 relationships (see list)
    c0034 ..> c0036 : __init__() calls unknown_status()
    c0034 ..> c0053 : type in __init__
    c0035 ..> c0034 : 2 relationships (see list)
    c0035 ..> c0035 : 9 relationships (see list)
    c0035 ..> c0036 : 6 relationships (see list)
    c0035 ..> c0090 : __enter__() constructs FactoryError
    c0035 ..> c0091 : 3 relationships (see list)
    c0036 ..> c0035 : 4 relationships (see list)
    c0036 ..> c0036 : 8 relationships (see list)
    c0036 ..> c0091 : _read_discovery() calls check_real_path()
    c0037 ..> c0000 : 5 relationships (see list)
    c0037 ..> c0009 : 2 relationships (see list)
    c0037 ..> c0017 : 4 relationships (see list)
    c0037 ..> c0029 : 5 relationships (see list)
    c0037 ..> c0035 : 4 relationships (see list)
    c0037 ..> c0037 : 27 relationships (see list)
    c0037 ..> c0038 : 6 relationships (see list)
    c0037 ..> c0039 : 6 relationships (see list)
    c0037 ..> c0045 : 9 relationships (see list)
    c0037 ..> c0049 : type in __init__
    c0037 --> c0050 : field confirmed
    c0037 ..> c0050 : 3 relationships (see list)
    c0037 ..> c0061 : type in __init__
    c0037 ..> c0069 : 7 relationships (see list)
    c0037 ..> c0072 : 10 relationships (see list)
    c0037 ..> c0090 : type in _read_problem
    c0041 ..> c0040 : validate_cleanup_marker() constructs CleanupMarkerError
    c0042 --> c0043 : field forgetful
    c0042 --> c0086 : field repository
    c0043 ..> c0044 : 2 relationships (see list)
    c0043 ..> c0090 : _validate_server() constructs FactoryError
    c0044 ..> c0042 : 3 relationships (see list)
    c0044 ..> c0043 : 3 relationships (see list)
    c0044 ..> c0044 : 5 relationships (see list)
    c0044 ..> c0086 : from_mapping() constructs RepositoryReference
    c0044 ..> c0087 : from_mapping() constructs WorkSource
    c0044 ..> c0090 : 4 relationships (see list)
    c0045 ..> c0015 : check_repository() calls origin()
    c0045 ..> c0029 : ownership() calls tasks()
    c0045 ..> c0031 : check_source() calls source_from_remote()
    c0045 ..> c0042 : type in __init__
    c0045 ..> c0045 : 2 relationships (see list)
    c0045 ..> c0054 : type in __init__
    c0045 ..> c0055 : type in __init__
    c0045 ..> c0058 : type in __init__
    c0045 ..> c0068 : 2 relationships (see list)
    c0045 ..> c0069 : 5 relationships (see list)
    c0045 ..> c0084 : 2 relationships (see list)
    c0045 ..> c0086 : 3 relationships (see list)
    c0045 ..> c0087 : 2 relationships (see list)
    c0047 ..> c0044 : 4 relationships (see list)
    c0047 ..> c0046 : 3 relationships (see list)
    c0047 ..> c0047 : 4 relationships (see list)
    c0047 ..> c0090 : 5 relationships (see list)
    c0048 ..> c0004 : initialise() calls save()
    c0048 ..> c0009 : 2 relationships (see list)
    c0048 ..> c0011 : prepare_foreman() calls prepare()
    c0048 ..> c0013 : 5 relationships (see list)
    c0048 ..> c0015 : 3 relationships (see list)
    c0048 ..> c0031 : 5 relationships (see list)
    c0048 ..> c0042 : 6 relationships (see list)
    c0048 ..> c0043 : 2 relationships (see list)
    c0048 ..> c0044 : 2 relationships (see list)
    c0048 ..> c0048 : 3 relationships (see list)
    c0048 ..> c0051 : type in __init__
    c0048 ..> c0052 : type in __init__
    c0048 ..> c0054 : type in __init__
    c0048 ..> c0058 : type in __init__
    c0048 ..> c0085 : 2 relationships (see list)
    c0048 ..> c0086 : 2 relationships (see list)
    c0048 ..> c0087 : 2 relationships (see list)
    c0048 ..> c0088 : type in __init__
    c0048 ..> c0090 : 5 relationships (see list)
    c0049 ..> c0050 : 2 relationships (see list)
    c0051 ..> c0042 : 2 relationships (see list)
    c0052 ..> c0042 : 3 relationships (see list)
    c0052 ..> c0043 : 8 relationships (see list)
    c0052 ..> c0046 : type in prepare_roles
    c0056 --|> c0090 : inherits
    c0058 ..> c0087 : type in source_from_remote
    c0059 ..> c0000 : __init__() calls __init__()
    c0059 --|> c0090 : inherits
    c0060 --|> c0090 : inherits
    c0062 ..> c0013 : check() calls check()
    c0062 ..> c0017 : 4 relationships (see list)
    c0062 ..> c0029 : 9 relationships (see list)
    c0062 ..> c0035 : recover() calls snapshot()
    c0062 ..> c0041 : _ensure_mapping() calls validate_cleanup_marker()
    c0062 ..> c0042 : type in __init__
    c0062 ..> c0045 : 11 relationships (see list)
    c0062 ..> c0054 : type in __init__
    c0062 ..> c0055 : type in __init__
    c0062 ..> c0058 : type in __init__
    c0062 ..> c0061 : type in __init__
    c0062 ..> c0062 : 22 relationships (see list)
    c0062 ..> c0067 : preflight() constructs IntakeProblem
    c0062 ..> c0069 : 8 relationships (see list)
    c0062 ..> c0070 : 5 relationships (see list)
    c0062 ..> c0071 : 5 relationships (see list)
    c0062 ..> c0084 : 8 relationships (see list)
    c0062 ..> c0086 : 3 relationships (see list)
    c0062 ..> c0087 : type in _repository
    c0062 ..> c0090 : _is_unfinished_factory_plan() constructs FactoryError
    c0063 --> c0084 : field issue
    c0064 ..> c0000 : 15 relationships (see list)
    c0064 ..> c0011 : _process_issue() calls prepare()
    c0064 ..> c0013 : _check_planning_access() calls check()
    c0064 ..> c0031 : _read_issues() calls list_issues()
    c0064 ..> c0037 : 2 relationships (see list)
    c0064 ..> c0042 : 4 relationships (see list)
    c0064 ..> c0045 : _check_pending_repositories() calls check_repository()
    c0064 ..> c0053 : type in __init__
    c0064 ..> c0062 : 5 relationships (see list)
    c0064 ..> c0063 : 13 relationships (see list)
    c0064 ..> c0064 : 35 relationships (see list)
    c0064 ..> c0065 : 19 relationships (see list)
    c0064 ..> c0066 : 2 relationships (see list)
    c0064 ..> c0068 : 2 relationships (see list)
    c0064 ..> c0069 : 3 relationships (see list)
    c0064 ..> c0070 : 2 relationships (see list)
    c0064 ..> c0072 : 28 relationships (see list)
    c0064 ..> c0084 : 13 relationships (see list)
    c0064 ..> c0086 : 5 relationships (see list)
    c0064 ..> c0087 : 7 relationships (see list)
    c0064 ..> c0088 : type in __init__
    c0064 ..> c0090 : _read_issues() constructs FactoryError
    c0064 ..> c0095 : 3 relationships (see list)
    c0065 --> c0063 : 2 relationships (see list)
    c0065 --> c0084 : field pending_lookup
    c0065 --> c0086 : field pending_repositories
    c0065 --> c0087 : field baselined
    c0067 --|> c0069 : inherits
    c0068 --|> c0069 : inherits
    c0069 --|> c0090 : inherits
    c0070 --|> c0069 : inherits
    c0071 --|> c0069 : inherits
    c0072 ..> c0000 : 2 relationships (see list)
    c0072 ..> c0073 : send() calls _cleanup_recovery()
    c0072 ..> c0090 : type in send
    c0074 ..> c0007 : build_watcher() constructs AgentShellTerminal
    c0074 ..> c0009 : build_watcher() constructs FileCleanupReceipts
    c0074 ..> c0013 : 6 relationships (see list)
    c0074 ..> c0015 : 2 relationships (see list)
    c0074 ..> c0017 : build_watcher() constructs GitWorktrees
    c0074 ..> c0022 : build_initialiser() constructs TomlConfigurationStore
    c0074 ..> c0028 : prepare_foreman_launch() calls role_environment()
    c0074 ..> c0029 : build_watcher() constructs ForgetfulPlanning
    c0074 ..> c0031 : 4 relationships (see list)
    c0074 ..> c0034 : build_watcher() constructs ObservedTerminal
    c0074 ..> c0037 : build_watcher() constructs CleanupCompleted
    c0074 ..> c0042 : 2 relationships (see list)
    c0074 ..> c0048 : 2 relationships (see list)
    c0074 ..> c0062 : build_watcher() constructs ScaffoldIssue
    c0074 ..> c0064 : 2 relationships (see list)
    c0074 ..> c0074 : build_watcher() calls prepare_foreman_launch()
    c0074 ..> c0082 : 4 relationships (see list)
    c0074 ..> c0090 : 2 relationships (see list)
    c0075 ..> c0042 : type in agree_definition_of_done
    c0075 ..> c0075 : agree_definition_of_done() calls _deployment_agreement()
    c0075 ..> c0090 : 2 relationships (see list)
    c0075 ..> c0091 : 2 relationships (see list)
    c0076 --> c0042 : field config
    c0076 --> c0043 : field connection
    c0077 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0077 ..> c0004 : _watch_locked() calls run()
    c0077 ..> c0006 : 14 relationships (see list)
    c0077 ..> c0009 : _initialise_locked() calls load()
    c0077 ..> c0013 : 17 relationships (see list)
    c0077 ..> c0015 : select_repositories() calls discover()
    c0077 ..> c0017 : _configure_new_factory() calls inspect()
    c0077 ..> c0023 : 6 relationships (see list)
    c0077 ..> c0024 : 6 relationships (see list)
    c0077 ..> c0035 : _prompt_workers() calls update()
    c0077 ..> c0036 : 4 relationships (see list)
    c0077 ..> c0042 : 4 relationships (see list)
    c0077 ..> c0043 : 8 relationships (see list)
    c0077 ..> c0046 : 7 relationships (see list)
    c0077 ..> c0047 : _start_initial_setup() calls validate_initial_agents()
    c0077 ..> c0048 : 15 relationships (see list)
    c0077 ..> c0074 : 4 relationships (see list)
    c0077 ..> c0075 : 2 relationships (see list)
    c0077 ..> c0076 : 3 relationships (see list)
    c0077 ..> c0077 : 55 relationships (see list)
    c0077 ..> c0078 : _select_numbered() calls parse_numbered_selection()
    c0077 ..> c0079 : main() calls update_resources()
    c0077 ..> c0080 : 3 relationships (see list)
    c0077 ..> c0082 : 9 relationships (see list)
    c0077 ..> c0090 : 20 relationships (see list)
    c0077 ..> c0091 : _discover_worker_models() calls check_real_path()
    c0077 ..> c0095 : _watch_locked() calls watch_stop_scope()
    c0078 ..> c0090 : parse_numbered_selection() constructs FactoryError
    c0079 ..> c0006 : update_resources() calls read_state()
    c0079 ..> c0013 : 4 relationships (see list)
    c0079 ..> c0020 : 2 relationships (see list)
    c0079 ..> c0024 : 2 relationships (see list)
    c0079 ..> c0079 : update_resources() calls _report()
    c0079 ..> c0082 : type in update_resources
    c0079 ..> c0090 : 2 relationships (see list)
    c0080 ..> c0009 : load_configuration() calls load()
    c0080 ..> c0022 : load_configuration() constructs TomlConfigurationStore
    c0080 ..> c0042 : type in load_configuration
    c0080 ..> c0090 : load_configuration() constructs FactoryError
    c0082 --> c0081 : field agentshell
    c0082 ..> c0083 : __post_init__() calls _validate_duration()
    c0084 --> c0087 : field source
    c0086 --> c0087 : field work_source
    c0088 ..> c0084 : type in list_issues
    c0088 ..> c0085 : 2 relationships (see list)
    c0088 ..> c0087 : 4 relationships (see list)
    c0089 ..> c0004 : run_command() calls run()
    c0089 ..> c0090 : run_command() constructs FactoryError
    c0089 ..> c0095 : run_command() calls check_watch_stop()
    c0091 ..> c0000 : 2 relationships (see list)
    c0091 ..> c0009 : read_generated_json() calls load()
    c0091 ..> c0090 : 6 relationships (see list)
    c0091 ..> c0091 : 9 relationships (see list)
    c0093 ..> c0000 : 2 relationships (see list)
    c0093 ..> c0090 : run_owned() constructs FactoryError
    c0093 ..> c0093 : 2 relationships (see list)
    c0093 ..> c0095 : run_owned() calls check_watch_stop()
    c0095 ..> c0094 : watch_stop_scope() constructs WatchStop
```

## Source index

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/adapters/agentshell/borrowed_terminal.py`:10
- c0001: `SessionState` — `src/forgetful_factory/adapters/agentshell/controller.py`:140
- c0002: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0003: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0004: `ForemanOwner` — `src/forgetful_factory/adapters/agentshell/owner.py`:104
- c0005: `src/forgetful_factory/adapters/agentshell/owner.py` —
  `src/forgetful_factory/adapters/agentshell/owner.py`:1
- c0006: `src/forgetful_factory/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/adapters/agentshell/owner_client.py`:1
- c0007: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:15
- c0008: `src/forgetful_factory/adapters/filesystem/agent_definitions.py` —
  `src/forgetful_factory/adapters/filesystem/agent_definitions.py`:1
- c0009: `FileCleanupReceipts` — `src/forgetful_factory/adapters/filesystem/cleanup_receipts.py`:40
- c0010: `src/forgetful_factory/adapters/filesystem/cleanup_receipts.py` —
  `src/forgetful_factory/adapters/filesystem/cleanup_receipts.py`:1
- c0011: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:30
- c0012: `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:1
- c0013: `ForemanProfile` — `src/forgetful_factory/adapters/filesystem/foreman_profile.py`:52
- c0014: `src/forgetful_factory/adapters/filesystem/foreman_runtime.py` —
  `src/forgetful_factory/adapters/filesystem/foreman_runtime.py`:1
- c0015: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:15
- c0016: `src/forgetful_factory/adapters/filesystem/git_repositories.py` —
  `src/forgetful_factory/adapters/filesystem/git_repositories.py`:1
- c0017: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:33
- c0018: `src/forgetful_factory/adapters/filesystem/git_worktrees.py` —
  `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:1
- c0019: `ResourceUpdate` — `src/forgetful_factory/adapters/filesystem/role_resources.py`:39
- c0020: `src/forgetful_factory/adapters/filesystem/role_resources.py` —
  `src/forgetful_factory/adapters/filesystem/role_resources.py`:1
- c0021: `src/forgetful_factory/adapters/filesystem/selected_skills.py` —
  `src/forgetful_factory/adapters/filesystem/selected_skills.py`:1
- c0022: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:20
- c0023: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0024: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0025: `WorkerProfiles` — `src/forgetful_factory/adapters/filesystem/worker_profiles.py`:16
- c0026: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0027: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:55
- c0028: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0029: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:13
- c0030: `src/forgetful_factory/adapters/forgetful/planning.py` —
  `src/forgetful_factory/adapters/forgetful/planning.py`:1
- c0031: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:10
- c0032: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:54
- c0033: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0034: `ObservedTerminal` — `src/forgetful_factory/adapters/watch_status.py`:252
- c0035: `PlainWatchObservation` — `src/forgetful_factory/adapters/watch_status.py`:129
- c0036: `src/forgetful_factory/adapters/watch_status.py` —
  `src/forgetful_factory/adapters/watch_status.py`:1
- c0037: `CleanupCompleted` — `src/forgetful_factory/application/cleanup_completed.py`:37
- c0038: `CompletedWork` — `src/forgetful_factory/application/cleanup_completed.py`:22
- c0039: `src/forgetful_factory/application/cleanup_completed.py` —
  `src/forgetful_factory/application/cleanup_completed.py`:1
- c0040: `CleanupMarkerError` — `src/forgetful_factory/application/cleanup_marker.py`:8
- c0041: `src/forgetful_factory/application/cleanup_marker.py` —
  `src/forgetful_factory/application/cleanup_marker.py`:1
- c0042: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:83
- c0043: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:12
- c0044: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0045: `FactoryRecords` — `src/forgetful_factory/application/factory_records.py`:14
- c0046: `InitialAgentChoices` — `src/forgetful_factory/application/initial_agent_choices.py`:9
- c0047: `src/forgetful_factory/application/initial_agent_choices.py` —
  `src/forgetful_factory/application/initial_agent_choices.py`:1
- c0048: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:19
- c0049: `CleanupReceipts` — `src/forgetful_factory/application/ports/cleanup_receipts.py`:24
- c0050: `CleanupSet` — `src/forgetful_factory/application/ports/cleanup_receipts.py`:7
- c0051: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0052: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:8
- c0053: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0054: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0055: `Planning` — `src/forgetful_factory/application/ports/planning.py`:10
- c0056: `PlanningReadError` — `src/forgetful_factory/application/ports/planning.py`:6
- c0057: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0058: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0059: `WorktreeProblem` — `src/forgetful_factory/application/ports/worktrees.py`:10
- c0060: `WorktreeReadError` — `src/forgetful_factory/application/ports/worktrees.py`:6
- c0061: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:19
- c0062: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:29
- c0063: `BlockedWork` — `src/forgetful_factory/application/watch_factory.py`:30
- c0064: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:62
- c0065: `_WatchState` — `src/forgetful_factory/application/watch_factory.py`:41
- c0066: `_WorkAction` — `src/forgetful_factory/application/watch_factory.py`:55
- c0067: `IntakeProblem` — `src/forgetful_factory/application/watcher_problems.py`:143
- c0068: `RepositoryProblem` — `src/forgetful_factory/application/watcher_problems.py`:139
- c0069: `ScaffoldProblem` — `src/forgetful_factory/application/watcher_problems.py`:119
- c0070: `ScaffoldReadProblem` — `src/forgetful_factory/application/watcher_problems.py`:135
- c0071: `UncertainScaffold` — `src/forgetful_factory/application/watcher_problems.py`:147
- c0072: `WatcherAlerts` — `src/forgetful_factory/application/watcher_problems.py`:151
- c0073: `src/forgetful_factory/application/watcher_problems.py` —
  `src/forgetful_factory/application/watcher_problems.py`:1
- c0074: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0075: `src/forgetful_factory/cli/definition_of_done.py` —
  `src/forgetful_factory/cli/definition_of_done.py`:1
- c0076: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:749
- c0077: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0078: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0079: `src/forgetful_factory/cli/resource_update.py` —
  `src/forgetful_factory/cli/resource_update.py`:1
- c0080: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0081: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/deadlines.py`:12
- c0082: `DeadlinePolicy` — `src/forgetful_factory/deadlines.py`:29
- c0083: `src/forgetful_factory/deadlines.py` — `src/forgetful_factory/deadlines.py`:1
- c0084: `Issue` — `src/forgetful_factory/domain/models.py`:23
- c0085: `Label` — `src/forgetful_factory/domain/models.py`:18
- c0086: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:11
- c0087: `WorkSource` — `src/forgetful_factory/domain/models.py`:5
- c0088: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6
- c0089: `src/forgetful_factory/shared/command.py` — `src/forgetful_factory/shared/command.py`:1
- c0090: `FactoryError` — `src/forgetful_factory/shared/errors.py`:1
- c0091: `src/forgetful_factory/shared/resource_files.py` —
  `src/forgetful_factory/shared/resource_files.py`:1
- c0092: `src/forgetful_factory/shared/resources.py` — `src/forgetful_factory/shared/resources.py`:1
- c0093: `src/forgetful_factory/shared/sensitive_command.py` —
  `src/forgetful_factory/shared/sensitive_command.py`:1
- c0094: `WatchStop` — `src/forgetful_factory/shared/watch_stop.py`:8
- c0095: `src/forgetful_factory/shared/watch_stop.py` —
  `src/forgetful_factory/shared/watch_stop.py`:1

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0007: `close() calls close()`
- c0000 ..> c0090: `_request() constructs FactoryError`
- c0000 ..> c0090: `wait() constructs FactoryError`
- c0000 ..> c0095: `_request() calls check_watch_stop()`
- c0000 ..> c0095: `wait() calls check_watch_stop()`
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
- c0002 ..> c0029: `control() calls create_task()`
- c0002 ..> c0029: `main() calls create_task()`
- c0002 ..> c0029: `replace_failed_exit_task() calls create_task()`
- c0002 ..> c0029: `supervise_session() calls create_task()`
- c0003 ..> c0013: `main() calls list_models()`
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
- c0004 ..> c0023: `_apply_controller_problem() calls quote()`
- c0004 ..> c0029: `_start_controller() calls create_task()`
- c0004 ..> c0029: `start_watcher() calls create_task()`
- c0004 ..> c0081: `__init__() constructs AgentShellLifecycleDeadlines`
- c0004 ..> c0081: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0004 ..> c0090: `_apply_controller_problem() constructs FactoryError`
- c0004 ..> c0090: `_await_readiness() constructs FactoryError`
- c0004 ..> c0090: `_complete_handover() constructs FactoryError`
- c0004 ..> c0090: `_finish_observation() constructs FactoryError`
- c0004 ..> c0090: `_reject_controller_event() constructs FactoryError`
- c0004 ..> c0090: `_relay_request() constructs FactoryError`
- c0004 ..> c0090: `control() constructs FactoryError`
- c0004 ..> c0090: `observe() constructs FactoryError`
- c0004 ..> c0090: `reap_watcher() constructs FactoryError`
- c0004 ..> c0090: `start_watcher() constructs FactoryError`
- c0004 ..> c0091: `save() calls replace_generated_json()`
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
- c0005 ..> c0014: `_prepare_owner_startup() calls runtime_directory()`
- c0005 ..> c0023: `_acquire_owner_lock() calls quote()`
- c0005 ..> c0029: `main() calls create_task()`
- c0005 ..> c0090: `_acquire_owner_lock() constructs FactoryError`
- c0005 ..> c0090: `_prepare_owner_startup() constructs FactoryError`
- c0005 ..> c0090: `_watcher_request() constructs FactoryError`
- c0006 ..> c0000: `start_owner() calls close()`
- c0006 ..> c0000: `start_owner() calls wait()`
- c0006 ..> c0004: `enter_terminal() calls run()`
- c0006 ..> c0004: `start_owner() calls run()`
- c0006 ..> c0006: `request() calls _reply()`
- c0006 ..> c0006: `request() calls read_state()`
- c0006 ..> c0006: `start_owner() calls _reply()`
- c0006 ..> c0014: `read_state() calls runtime_directory()`
- c0006 ..> c0014: `request() calls runtime_directory()`
- c0006 ..> c0014: `start_owner() calls runtime_directory()`
- c0006 ..> c0023: `request() calls quote()`
- c0006 ..> c0081: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0006 ..> c0081: `type in start_owner`
- c0006 ..> c0090: `_reply() constructs FactoryError`
- c0006 ..> c0090: `enter_terminal() constructs FactoryError`
- c0006 ..> c0090: `read_state() constructs FactoryError`
- c0006 ..> c0090: `request() constructs FactoryError`
- c0006 ..> c0090: `start_owner() constructs FactoryError`
- c0006 ..> c0091: `read_state() calls read_generated_json()`
- c0007 ..> c0000: `close() calls close()`
- c0007 ..> c0007: `send() calls _read()`
- c0007 ..> c0007: `send() calls _write()`
- c0007 ..> c0007: `start() calls _read()`
- c0007 ..> c0007: `start() calls _write()`
- c0007 ..> c0007: `wait() calls _read()`
- c0007 ..> c0081: `__init__() constructs AgentShellLifecycleDeadlines`
- c0007 ..> c0081: `type in __init__`
- c0007 ..> c0090: `_read() constructs FactoryError`
- c0007 ..> c0090: `_write() constructs FactoryError`
- c0007 ..> c0090: `close() constructs FactoryError`
- c0007 ..> c0090: `start() constructs FactoryError`
- c0007 ..> c0095: `_read() calls check_watch_stop()`
- c0007 ..> c0095: `_write() calls check_watch_stop()`
- c0007 ..> c0095: `wait() calls check_watch_stop()`
- c0008 ..> c0008: `_validate_agent() calls _local_selection()`
- c0008 ..> c0008: `_validate_roster() calls _local_selection()`
- c0008 ..> c0008: `_validate_roster() calls relative_path()`
- c0008 ..> c0008: `foreman_launch() calls read_definition()`
- c0008 ..> c0008: `foreman_launch() calls relative_path()`
- c0008 ..> c0008: `read_definition() calls _validate_agent()`
- c0008 ..> c0008: `read_definition() calls _validate_resources()`
- c0008 ..> c0008: `read_definition() calls _validate_roster()`
- c0008 ..> c0044: `_local_selection() calls nonblank()`
- c0008 ..> c0044: `_validate_agent() calls nonblank()`
- c0008 ..> c0044: `foreman_launch() calls nonblank()`
- c0008 ..> c0044: `relative_path() calls nonblank()`
- c0008 ..> c0090: `foreman_launch() constructs FactoryError`
- c0008 ..> c0090: `read_definition() constructs FactoryError`
- c0009 ..> c0000: `_load() calls close()`
- c0009 ..> c0009: `confirm() calls load()`
- c0009 ..> c0009: `load() calls _load()`
- c0009 ..> c0010: `_load() calls _resource()`
- c0009 ..> c0050: `type in _load`
- c0009 ..> c0050: `type in confirm`
- c0009 ..> c0050: `type in load`
- c0009 ..> c0090: `confirm() constructs FactoryError`
- c0009 ..> c0090: `load() constructs FactoryError`
- c0009 ..> c0091: `_load() calls check_real_path()`
- c0009 ..> c0091: `confirm() calls replace_generated_json()`
- c0009 ..> c0095: `confirm() calls check_watch_stop()`
- c0010 ..> c0050: `_resource() constructs CleanupSet`
- c0010 ..> c0050: `type in _resource`
- c0011 ..> c0011: `prepare() calls _write_agent()`
- c0011 ..> c0011: `prepare() calls _write_foreman_memory()`
- c0011 ..> c0011: `prepare() calls validate_guidance()`
- c0011 ..> c0012: `prepare() calls selected_resources()`
- c0011 ..> c0013: `prepare() calls prepare()`
- c0011 ..> c0025: `__init__() constructs WorkerProfiles`
- c0011 ..> c0042: `type in prepare`
- c0011 ..> c0042: `type in validate_guidance`
- c0011 ..> c0090: `_write_foreman_memory() constructs FactoryError`
- c0011 ..> c0090: `prepare() constructs FactoryError`
- c0011 ..> c0090: `validate_depth() constructs FactoryError`
- c0011 ..> c0090: `validate_guidance() constructs FactoryError`
- c0011 ..> c0091: `_write_agent() calls write_definition()`
- c0011 ..> c0091: `_write_foreman_memory() calls read_generated_json()`
- c0011 ..> c0091: `_write_foreman_memory() calls write_json()`
- c0011 ..> c0091: `prepare() calls check_skill_file()`
- c0011 ..> c0091: `prepare() calls write_new()`
- c0013 ..> c0008: `selected_launch() calls foreman_launch()`
- c0013 ..> c0009: `choose_pi_home() calls confirm()`
- c0013 ..> c0011: `prepare_roles() calls validate_depth()`
- c0013 ..> c0011: `prepare_roles() constructs CoordinatorProfiles`
- c0013 ..> c0011: `validate_setup() calls validate_depth()`
- c0013 ..> c0011: `validate_setup() constructs CoordinatorProfiles`
- c0013 ..> c0013: `choose_pi_home() calls pi_home()`
- c0013 ..> c0013: `choose_pi_home() calls require_pi_home()`
- c0013 ..> c0013: `list_models() calls pi_home()`
- c0013 ..> c0013: `list_models() calls require_pi_home()`
- c0013 ..> c0013: `missing_executables() calls pi_home()`
- c0013 ..> c0013: `missing_executables() calls role_runtime_ready()`
- c0013 ..> c0013: `prepare() calls _install_resources()`
- c0013 ..> c0013: `prepare() calls _protect_runtime()`
- c0013 ..> c0013: `prepare() calls save_pi_choice()`
- c0013 ..> c0013: `prepare() calls validate_guidance()`
- c0013 ..> c0013: `prepare_roles() calls list_models()`
- c0013 ..> c0013: `prepare_roles() calls pi_home()`
- c0013 ..> c0013: `prepare_roles() calls prepare()`
- c0013 ..> c0013: `prepare_roles() calls validate_worker_models()`
- c0013 ..> c0013: `record_completion() calls selected_launch()`
- c0013 ..> c0013: `selected_launch() calls validate_setup()`
- c0013 ..> c0013: `validate_guidance() calls _read_guidance()`
- c0013 ..> c0013: `validate_setup() calls missing_executables()`
- c0013 ..> c0013: `validate_setup() calls pi_home()`
- c0013 ..> c0013: `validate_setup() calls require_pi_home()`
- c0013 ..> c0013: `validate_setup() calls validate_bundled_resources()`
- c0013 ..> c0013: `validate_setup() calls validate_guidance()`
- c0013 ..> c0013: `validate_worker_models() calls list_models()`
- c0013 ..> c0020: `_install_resources() calls bundled_files()`
- c0013 ..> c0021: `selected_launch() calls selected_skill_files()`
- c0013 ..> c0023: `require_pi_home() calls quote()`
- c0013 ..> c0026: `uses_browser_login() calls uses_browser_login()`
- c0013 ..> c0027: `check() calls check()`
- c0013 ..> c0027: `check() constructs AgentForgetfulConnection`
- c0013 ..> c0027: `create_project() calls create_project()`
- c0013 ..> c0027: `create_project() constructs AgentForgetfulConnection`
- c0013 ..> c0027: `login() calls login()`
- c0013 ..> c0027: `login() constructs AgentForgetfulConnection`
- c0013 ..> c0027: `projects() calls projects()`
- c0013 ..> c0027: `projects() constructs AgentForgetfulConnection`
- c0013 ..> c0028: `list_models() calls role_environment()`
- c0013 ..> c0032: `install() calls install()`
- c0013 ..> c0032: `install() constructs HostDependencies`
- c0013 ..> c0032: `installation() calls description()`
- c0013 ..> c0032: `installation() constructs HostDependencies`
- c0013 ..> c0032: `missing_executables() calls pi_ready()`
- c0013 ..> c0032: `missing_executables() constructs HostDependencies`
- c0013 ..> c0033: `missing_executables() calls executable_path()`
- c0013 ..> c0033: `missing_executables() calls runtime_ready()`
- c0013 ..> c0033: `require_pi_home() calls executable_path()`
- c0013 ..> c0033: `role_runtime_ready() calls runtime_ready()`
- c0013 ..> c0042: `type in record_completion`
- c0013 ..> c0042: `type in selected_launch`
- c0013 ..> c0042: `type in validate_completion`
- c0013 ..> c0042: `type in validate_worker_models`
- c0013 ..> c0043: `type in check`
- c0013 ..> c0043: `type in create_project`
- c0013 ..> c0043: `type in list_models`
- c0013 ..> c0043: `type in login`
- c0013 ..> c0043: `type in missing_executables`
- c0013 ..> c0043: `type in prepare`
- c0013 ..> c0043: `type in projects`
- c0013 ..> c0043: `type in uses_browser_login`
- c0013 ..> c0043: `type in validate_setup`
- c0013 ..> c0090: `_install_resources() constructs FactoryError`
- c0013 ..> c0090: `_read_guidance() constructs FactoryError`
- c0013 ..> c0090: `choose_pi_home() constructs FactoryError`
- c0013 ..> c0090: `list_models() constructs FactoryError`
- c0013 ..> c0090: `pi_home() constructs FactoryError`
- c0013 ..> c0090: `prepare_roles() constructs FactoryError`
- c0013 ..> c0090: `prepare_setup_guidance() constructs FactoryError`
- c0013 ..> c0090: `require_pi_home() constructs FactoryError`
- c0013 ..> c0090: `selected_launch() constructs FactoryError`
- c0013 ..> c0090: `validate_bundled_resources() constructs FactoryError`
- c0013 ..> c0090: `validate_completion() constructs FactoryError`
- c0013 ..> c0090: `validate_guidance() constructs FactoryError`
- c0013 ..> c0090: `validate_setup() constructs FactoryError`
- c0013 ..> c0090: `validate_worker_models() constructs FactoryError`
- c0013 ..> c0091: `_install_resources() calls write_new()`
- c0013 ..> c0091: `_protect_runtime() calls write_new()`
- c0013 ..> c0091: `begin_setup() calls remove_generated()`
- c0013 ..> c0091: `pi_home() calls read_generated_json()`
- c0013 ..> c0091: `prepare() calls write_new()`
- c0013 ..> c0091: `prepare_roles() calls check_real_path()`
- c0013 ..> c0091: `prepare_setup_guidance() calls write_new()`
- c0013 ..> c0091: `record_completion() calls replace_generated_json()`
- c0013 ..> c0091: `save_pi_choice() calls write_json()`
- c0013 ..> c0091: `validate_bundled_resources() calls check_real_path()`
- c0013 ..> c0091: `validate_completion() calls read_generated_json()`
- c0013 ..> c0093: `list_models() calls run_owned()`
- c0014 ..> c0090: `runtime_directory() constructs FactoryError`
- c0014 ..> c0091: `runtime_directory() calls check_real_path()`
- c0015 ..> c0016: `origin() calls _resolve_repository()`
- c0015 ..> c0089: `origin() calls run_command()`
- c0015 ..> c0090: `origin() constructs FactoryError`
- c0016 ..> c0090: `_resolve_repository() constructs FactoryError`
- c0017 ..> c0017: `_disposal_state() calls _repository_entries()`
- c0017 ..> c0017: `_disposal_state() calls _validate_disposal_origin()`
- c0017 ..> c0017: `_disposal_state() calls _validate_disposal_path()`
- c0017 ..> c0017: `_disposal_state() calls _validate_disposal_refs()`
- c0017 ..> c0017: `_disposal_state() calls _validate_registered_worktree()`
- c0017 ..> c0017: `_dispose() calls _disposal_state()`
- c0017 ..> c0017: `_dispose() calls _network_git()`
- c0017 ..> c0017: `_dispose() calls _network_read()`
- c0017 ..> c0017: `_dispose() calls _read_git()`
- c0017 ..> c0017: `_dispose() calls _repository_entries()`
- c0017 ..> c0017: `_dispose() calls _verify_local_ref_absent()`
- c0017 ..> c0017: `_inspect() calls _read_git()`
- c0017 ..> c0017: `_inspect() calls _repository_entries()`
- c0017 ..> c0017: `_inspect() calls _validate_registered_worktree()`
- c0017 ..> c0017: `_network_git() calls _read_git()`
- c0017 ..> c0017: `_network_read() calls _network_git()`
- c0017 ..> c0017: `_remote_default() calls _network_read()`
- c0017 ..> c0017: `_repository_entries() calls _read_git()`
- c0017 ..> c0017: `_validate_common_directory() calls _read_git()`
- c0017 ..> c0017: `_validate_disposal_origin() calls _read_git()`
- c0017 ..> c0017: `_validate_disposal_path() calls _read_git()`
- c0017 ..> c0017: `_validate_disposal_refs() calls _read_git()`
- c0017 ..> c0017: `_validate_disposal_refs() calls _remote_default()`
- c0017 ..> c0017: `_validate_registered_worktree() calls _validate_common_directory()`
- c0017 ..> c0017: `_validate_registered_worktree() calls _validate_registration()`
- c0017 ..> c0017: `_validate_registered_worktree() calls _validate_target_identity()`
- c0017 ..> c0017: `_validate_target_identity() calls _read_git()`
- c0017 ..> c0017: `_verify_local_ref_absent() calls _read_git()`
- c0017 ..> c0017: `_verify_removed() calls _repository_entries()`
- c0017 ..> c0017: `dispose() calls _dispose()`
- c0017 ..> c0017: `ensure() calls _inspect()`
- c0017 ..> c0017: `inspect() calls _inspect()`
- c0017 ..> c0017: `repository_identity() calls _read_git()`
- c0017 ..> c0017: `target_branch() calls _read_git()`
- c0017 ..> c0017: `verify_removed() calls _verify_removed()`
- c0017 ..> c0018: `_repository_entries() calls _worktree_entries()`
- c0017 ..> c0023: `_network_git() calls quote()`
- c0017 ..> c0059: `_disposal_state() constructs WorktreeProblem`
- c0017 ..> c0059: `_dispose() constructs WorktreeProblem`
- c0017 ..> c0059: `_inspect() constructs WorktreeProblem`
- c0017 ..> c0059: `_network_read() constructs WorktreeProblem`
- c0017 ..> c0059: `_repository_entries() constructs WorktreeProblem`
- c0017 ..> c0059: `_validate_common_directory() constructs WorktreeProblem`
- c0017 ..> c0059: `_validate_disposal_origin() constructs WorktreeProblem`
- c0017 ..> c0059: `_validate_disposal_path() constructs WorktreeProblem`
- c0017 ..> c0059: `_validate_disposal_refs() constructs WorktreeProblem`
- c0017 ..> c0059: `_validate_registration() constructs WorktreeProblem`
- c0017 ..> c0059: `_validate_target_identity() constructs WorktreeProblem`
- c0017 ..> c0059: `_verify_local_ref_absent() constructs WorktreeProblem`
- c0017 ..> c0059: `_verify_removed() constructs WorktreeProblem`
- c0017 ..> c0059: `dispose() constructs WorktreeProblem`
- c0017 ..> c0060: `_read_git() constructs WorktreeReadError`
- c0017 ..> c0060: `ensure() constructs WorktreeReadError`
- c0017 ..> c0060: `inspect() constructs WorktreeReadError`
- c0017 ..> c0060: `repository_identity() constructs WorktreeReadError`
- c0017 ..> c0060: `target_branch() constructs WorktreeReadError`
- c0017 ..> c0060: `verify_removed() constructs WorktreeReadError`
- c0017 ..> c0072: `begin_cleanup_cycle() calls clear()`
- c0017 ..> c0089: `_dispose() calls run_command()`
- c0017 ..> c0089: `_network_git() calls run_command()`
- c0017 ..> c0089: `_read_git() calls run_command()`
- c0017 ..> c0089: `ensure() calls run_command()`
- c0017 --> c0090: `field cleanup_defaults`
- c0017 ..> c0090: `ensure() constructs FactoryError`
- c0017 ..> c0095: `ensure() calls check_watch_stop()`
- c0020 ..> c0019: `plan_update() constructs ResourceUpdate`
- c0020 ..> c0019: `type in _back_up`
- c0020 ..> c0019: `type in apply_update`
- c0020 ..> c0019: `type in plan_update`
- c0020 ..> c0020: `apply_update() calls _back_up()`
- c0020 ..> c0020: `bundled_files() calls _digest()`
- c0020 ..> c0020: `plan_update() calls _digest()`
- c0020 ..> c0020: `plan_update() calls bundled_files()`
- c0020 ..> c0090: `bundled_files() constructs FactoryError`
- c0020 ..> c0090: `plan_update() constructs FactoryError`
- c0020 ..> c0091: `plan_update() calls check_real_path()`
- c0021 ..> c0000: `_add_skill_file() calls close()`
- c0021 ..> c0021: `_walk_skill_directory() calls _add_skill_file()`
- c0021 ..> c0021: `selected_skill_files() calls _add_skill_file()`
- c0021 ..> c0021: `selected_skill_files() calls _walk_skill_directory()`
- c0021 ..> c0090: `_add_skill_file() constructs FactoryError`
- c0021 ..> c0090: `_walk_skill_directory() constructs FactoryError`
- c0021 ..> c0090: `selected_skill_files() constructs FactoryError`
- c0022 ..> c0000: `load() calls close()`
- c0022 ..> c0000: `save() calls close()`
- c0022 ..> c0009: `load() calls load()`
- c0022 ..> c0023: `save() calls quote()`
- c0022 ..> c0042: `type in load`
- c0022 ..> c0042: `type in save`
- c0022 ..> c0044: `load() calls from_mapping()`
- c0022 ..> c0090: `load() constructs FactoryError`
- c0022 ..> c0090: `save() constructs FactoryError`
- c0024 ..> c0000: `_hold_directory() calls close()`
- c0024 ..> c0024: `hold() calls _hold_directory()`
- c0024 ..> c0090: `_hold_directory() constructs FactoryError`
- c0025 ..> c0035: `prepare() calls update()`
- c0025 ..> c0046: `type in prepare`
- c0025 ..> c0091: `prepare() calls check_skill_file()`
- c0025 ..> c0091: `prepare() calls write_definition()`
- c0025 ..> c0091: `prepare() calls write_new()`
- c0026 ..> c0006: `uses_browser_login() calls request()`
- c0026 ..> c0043: `type in uses_browser_login`
- c0027 ..> c0027: `call() calls command()`
- c0027 ..> c0027: `check() calls call()`
- c0027 ..> c0027: `check() calls command()`
- c0027 ..> c0027: `command() calls _environment()`
- c0027 ..> c0027: `create_project() calls call()`
- c0027 ..> c0027: `login() calls _environment()`
- c0027 ..> c0027: `projects() calls command()`
- c0027 ..> c0028: `_environment() calls role_environment()`
- c0027 ..> c0028: `check() calls _catalog_tools()`
- c0027 ..> c0043: `type in _environment`
- c0027 ..> c0043: `type in call`
- c0027 ..> c0043: `type in check`
- c0027 ..> c0043: `type in command`
- c0027 ..> c0043: `type in create_project`
- c0027 ..> c0043: `type in login`
- c0027 ..> c0043: `type in projects`
- c0027 ..> c0090: `check() constructs FactoryError`
- c0027 ..> c0090: `command() constructs FactoryError`
- c0027 ..> c0090: `create_project() constructs FactoryError`
- c0027 ..> c0090: `login() constructs FactoryError`
- c0027 ..> c0090: `projects() constructs FactoryError`
- c0027 ..> c0093: `command() calls run_owned()`
- c0027 ..> c0093: `login() calls run_owned()`
- c0027 ..> c0095: `command() calls check_watch_stop()`
- c0028 ..> c0033: `role_environment() calls executable_path()`
- c0028 ..> c0035: `role_environment() calls update()`
- c0028 ..> c0043: `type in role_environment`
- c0029 ..> c0013: `check() calls check()`
- c0029 ..> c0027: `__init__() constructs AgentForgetfulConnection`
- c0029 ..> c0027: `_call() calls call()`
- c0029 ..> c0029: `_read() calls _call()`
- c0029 ..> c0029: `_task() calls _read()`
- c0029 ..> c0029: `create_plan() calls _call()`
- c0029 ..> c0029: `create_task() calls _call()`
- c0029 ..> c0029: `get_plan() calls _read()`
- c0029 ..> c0029: `plans() calls _read()`
- c0029 ..> c0029: `plans() calls _rows()`
- c0029 ..> c0029: `tasks() calls _read()`
- c0029 ..> c0029: `tasks() calls _rows()`
- c0029 ..> c0029: `tasks() calls _task()`
- c0029 ..> c0029: `update_plan() calls _call()`
- c0029 ..> c0029: `update_task() calls _call()`
- c0029 ..> c0030: `_rows() calls _positive_id()`
- c0029 ..> c0030: `_task() calls _positive_id()`
- c0029 ..> c0030: `get_plan() calls _positive_id()`
- c0029 ..> c0043: `type in __init__`
- c0029 ..> c0056: `_read() constructs PlanningReadError`
- c0029 ..> c0056: `_rows() constructs PlanningReadError`
- c0029 ..> c0056: `_task() constructs PlanningReadError`
- c0029 ..> c0056: `get_plan() constructs PlanningReadError`
- c0031 ..> c0031: `_comments() calls _api()`
- c0031 ..> c0031: `_issue() calls _comments()`
- c0031 ..> c0031: `_issue() calls _milestone()`
- c0031 ..> c0031: `check_access() calls _api()`
- c0031 ..> c0031: `create_label() calls _api()`
- c0031 ..> c0031: `list_issues() calls _api()`
- c0031 ..> c0031: `list_issues() calls _issue()`
- c0031 ..> c0031: `list_issues() calls _validate_issue()`
- c0031 ..> c0031: `list_labels() calls _api()`
- c0031 ..> c0084: `_issue() constructs Issue`
- c0031 ..> c0084: `type in _issue`
- c0031 ..> c0084: `type in list_issues`
- c0031 ..> c0085: `list_labels() constructs Label`
- c0031 ..> c0085: `type in create_label`
- c0031 ..> c0085: `type in list_labels`
- c0031 ..> c0087: `source_from_remote() constructs WorkSource`
- c0031 ..> c0087: `type in _api`
- c0031 ..> c0087: `type in _comments`
- c0031 ..> c0087: `type in _issue`
- c0031 ..> c0087: `type in _validate_issue`
- c0031 ..> c0087: `type in check_access`
- c0031 ..> c0087: `type in create_label`
- c0031 ..> c0087: `type in list_issues`
- c0031 ..> c0087: `type in list_labels`
- c0031 ..> c0087: `type in source_from_remote`
- c0031 ..> c0089: `_api() calls run_command()`
- c0031 ..> c0089: `check_cli() calls run_command()`
- c0031 ..> c0090: `_api() constructs FactoryError`
- c0031 ..> c0090: `_comments() constructs FactoryError`
- c0031 ..> c0090: `_validate_issue() constructs FactoryError`
- c0031 ..> c0090: `check_access() constructs FactoryError`
- c0031 ..> c0090: `check_cli() constructs FactoryError`
- c0031 ..> c0090: `create_label() constructs FactoryError`
- c0031 ..> c0090: `list_issues() constructs FactoryError`
- c0031 ..> c0090: `list_labels() constructs FactoryError`
- c0031 ..> c0090: `source_from_remote() constructs FactoryError`
- c0032 ..> c0032: `_check_uv() calls _environment()`
- c0032 ..> c0032: `_forgetful_python() calls _check_uv()`
- c0032 ..> c0032: `_forgetful_python() calls _environment()`
- c0032 ..> c0032: `_install_role_runtime() calls _check_uv()`
- c0032 ..> c0032: `_install_role_runtime() calls _run()`
- c0032 ..> c0032: `_install_tmux() calls _run()`
- c0032 ..> c0032: `_run() calls _environment()`
- c0032 ..> c0032: `description() calls _forgetful_python()`
- c0032 ..> c0032: `description() calls _ubuntu_tmux()`
- c0032 ..> c0032: `install() calls _forgetful_python()`
- c0032 ..> c0032: `install() calls _install_role_runtime()`
- c0032 ..> c0032: `install() calls _install_tmux()`
- c0032 ..> c0032: `install() calls _run()`
- c0032 ..> c0032: `install() calls _ubuntu_tmux()`
- c0032 ..> c0032: `pi_ready() calls _environment()`
- c0032 ..> c0033: `_install_role_runtime() calls sync_fingerprint()`
- c0032 ..> c0033: `install() calls sync_fingerprint()`
- c0032 ..> c0033: `pi_ready() calls sync_fingerprint()`
- c0032 ..> c0090: `_check_uv() constructs FactoryError`
- c0032 ..> c0090: `_forgetful_python() constructs FactoryError`
- c0032 ..> c0090: `_install_role_runtime() constructs FactoryError`
- c0032 ..> c0090: `_install_tmux() constructs FactoryError`
- c0032 ..> c0090: `_run() constructs FactoryError`
- c0032 ..> c0090: `install() constructs FactoryError`
- c0032 ..> c0091: `install() calls write_new()`
- c0032 ..> c0093: `_check_uv() calls run_owned()`
- c0032 ..> c0093: `_forgetful_python() calls run_owned()`
- c0032 ..> c0093: `_run() calls run_owned()`
- c0032 ..> c0093: `pi_ready() calls run_owned()`
- c0033 ..> c0033: `runtime_ready() calls sync_fingerprint()`
- c0033 ..> c0093: `runtime_ready() calls run_owned()`
- c0034 ..> c0000: `close() calls close()`
- c0034 ..> c0000: `send() calls send()`
- c0034 ..> c0000: `start() calls start()`
- c0034 ..> c0000: `startup_hint() calls startup_hint()`
- c0034 ..> c0000: `wait() calls wait()`
- c0034 ..> c0035: `close() calls update()`
- c0034 ..> c0035: `start() calls update()`
- c0034 ..> c0035: `type in __init__`
- c0034 ..> c0036: `__init__() calls unknown_status()`
- c0034 ..> c0053: `type in __init__`
- c0035 ..> c0034: `__enter__() calls start()`
- c0035 ..> c0034: `_close_resources() calls close()`
- c0035 ..> c0035: `__enter__() calls _close_resources()`
- c0035 ..> c0035: `__enter__() calls snapshot()`
- c0035 ..> c0035: `__enter__() calls update()`
- c0035 ..> c0035: `__exit__() calls _close_resources()`
- c0035 ..> c0035: `__exit__() calls _publish_history()`
- c0035 ..> c0035: `__exit__() calls snapshot()`
- c0035 ..> c0035: `__exit__() calls update()`
- c0035 ..> c0035: `_serve() calls snapshot()`
- c0035 ..> c0035: `update() calls _publish_history()`
- c0035 ..> c0036: `__enter__() calls _discovery_path()`
- c0035 ..> c0036: `__enter__() calls _endpoint()`
- c0035 ..> c0036: `_publish_history() calls _discovery_path()`
- c0035 ..> c0036: `_publish_history() calls _read_discovery()`
- c0035 ..> c0036: `_serve() calls _frame()`
- c0035 ..> c0036: `_serve() calls _peer()`
- c0035 ..> c0090: `__enter__() constructs FactoryError`
- c0035 ..> c0091: `__enter__() calls check_real_path()`
- c0035 ..> c0091: `__enter__() calls replace_generated_json()`
- c0035 ..> c0091: `_publish_history() calls replace_generated_json()`
- c0036 ..> c0035: `observe_plain_watch() calls __enter__()`
- c0036 ..> c0035: `observe_plain_watch() calls __exit__()`
- c0036 ..> c0035: `observe_plain_watch() constructs PlainWatchObservation`
- c0036 ..> c0035: `type in observe_plain_watch`
- c0036 ..> c0036: `_frame() calls _observation_json()`
- c0036 ..> c0036: `_read_discovery() calls _discovery_path()`
- c0036 ..> c0036: `_read_discovery() calls _observation_json()`
- c0036 ..> c0036: `plain_watch_status() calls _endpoint()`
- c0036 ..> c0036: `plain_watch_status() calls _frame()`
- c0036 ..> c0036: `plain_watch_status() calls _peer()`
- c0036 ..> c0036: `plain_watch_status() calls _read_discovery()`
- c0036 ..> c0036: `plain_watch_status() calls unknown_status()`
- c0036 ..> c0091: `_read_discovery() calls check_real_path()`
- c0037 ..> c0000: `_candidates() calls send()`
- c0037 ..> c0000: `_dispose() calls send()`
- c0037 ..> c0000: `_read_problem() calls send()`
- c0037 ..> c0000: `_repository_identities() calls send()`
- c0037 ..> c0000: `poll() calls send()`
- c0037 ..> c0009: `_dispose() calls confirm()`
- c0037 ..> c0009: `poll() calls load()`
- c0037 ..> c0017: `_claims() calls repository_identity()`
- c0037 ..> c0017: `_dispose() calls dispose()`
- c0037 ..> c0017: `_repository_identities() calls repository_identity()`
- c0037 ..> c0017: `poll() calls begin_cleanup_cycle()`
- c0037 ..> c0029: `_candidates() calls tasks()`
- c0037 ..> c0029: `_claim_indexes() calls tasks()`
- c0037 ..> c0029: `_read_plans() calls get_plan()`
- c0037 ..> c0029: `_still_completed() calls get_plan()`
- c0037 ..> c0029: `poll() calls plans()`
- c0037 ..> c0035: `_candidate() calls snapshot()`
- c0037 ..> c0035: `_candidate() calls update()`
- c0037 ..> c0035: `_check_namespaces() calls update()`
- c0037 ..> c0035: `_still_completed() calls snapshot()`
- c0037 ..> c0037: `_candidate() calls _keys()`
- c0037 ..> c0037: `_candidates() calls _candidate()`
- c0037 ..> c0037: `_candidates() calls _in_scope()`
- c0037 ..> c0037: `_check_namespaces() calls _keys()`
- c0037 ..> c0037: `_claim_indexes() calls _claims()`
- c0037 ..> c0037: `_claim_indexes() calls _read_problem()`
- c0037 ..> c0037: `_claims() calls _is_confirmed()`
- c0037 ..> c0037: `_claims() calls _keys()`
- c0037 ..> c0037: `_claims() calls _task_mappings()`
- c0037 ..> c0037: `_dispose() calls _check_namespaces()`
- c0037 ..> c0037: `_dispose() calls _keys()`
- c0037 ..> c0037: `_dispose() calls _mapping_identity()`
- c0037 ..> c0037: `_dispose() calls _overlaps()`
- c0037 ..> c0037: `_dispose() calls _read_problem()`
- c0037 ..> c0037: `_dispose() calls _still_completed()`
- c0037 ..> c0037: `_is_confirmed() calls _mapping_identity()`
- c0037 ..> c0037: `_read_plans() calls _read_problem()`
- c0037 ..> c0037: `_still_completed() calls _in_scope()`
- c0037 ..> c0037: `_task_mappings() calls _validate_claim_mapping()`
- c0037 ..> c0037: `poll() calls _candidates()`
- c0037 ..> c0037: `poll() calls _claim_indexes()`
- c0037 ..> c0037: `poll() calls _dispose()`
- c0037 ..> c0037: `poll() calls _in_scope()`
- c0037 ..> c0037: `poll() calls _is_confirmed()`
- c0037 ..> c0037: `poll() calls _order()`
- c0037 ..> c0037: `poll() calls _read_plans()`
- c0037 ..> c0037: `poll() calls _repository_identities()`
- c0037 ..> c0038: `_candidate() constructs CompletedWork`
- c0037 ..> c0038: `type in _candidate`
- c0037 ..> c0038: `type in _candidates`
- c0037 ..> c0038: `type in _dispose`
- c0037 ..> c0038: `type in _order`
- c0037 ..> c0038: `type in _still_completed`
- c0037 ..> c0039: `_candidate() calls _claim_path()`
- c0037 ..> c0039: `_claims() calls _claim_path()`
- c0037 ..> c0039: `_dispose() calls _claim_path()`
- c0037 ..> c0039: `_keys() calls _claim_path()`
- c0037 ..> c0039: `_overlaps() calls _claim_path()`
- c0037 ..> c0039: `_repository_identities() calls _claim_path()`
- c0037 ..> c0045: `_candidate() calls check_source()`
- c0037 ..> c0045: `_candidate() calls context()`
- c0037 ..> c0045: `_candidate() calls mapping_repository()`
- c0037 ..> c0045: `_candidate() calls ownership_records()`
- c0037 ..> c0045: `_dispose() calls check_repository()`
- c0037 ..> c0045: `_dispose() calls mapping_repository()`
- c0037 ..> c0045: `_still_completed() calls context()`
- c0037 ..> c0045: `_still_completed() calls ownership()`
- c0037 ..> c0045: `type in __init__`
- c0037 ..> c0049: `type in __init__`
- c0037 --> c0050: `field confirmed`
- c0037 ..> c0050: `_is_confirmed() calls overlaps()`
- c0037 ..> c0050: `_mapping_identity() constructs CleanupSet`
- c0037 ..> c0050: `type in _mapping_identity`
- c0037 ..> c0061: `type in __init__`
- c0037 ..> c0069: `_candidate() constructs ScaffoldProblem`
- c0037 ..> c0069: `_check_namespaces() constructs ScaffoldProblem`
- c0037 ..> c0069: `_dispose() constructs ScaffoldProblem`
- c0037 ..> c0069: `_is_confirmed() constructs ScaffoldProblem`
- c0037 ..> c0069: `_still_completed() constructs ScaffoldProblem`
- c0037 ..> c0069: `_task_mappings() constructs ScaffoldProblem`
- c0037 ..> c0069: `_validate_claim_mapping() constructs ScaffoldProblem`
- c0037 ..> c0072: `_dispose() calls clear()`
- c0037 ..> c0072: `_repository_identities() calls clear()`
- c0037 ..> c0072: `poll() calls clear()`
- c0037 ..> c0072: `type in _candidates`
- c0037 ..> c0072: `type in _claim_indexes`
- c0037 ..> c0072: `type in _dispose`
- c0037 ..> c0072: `type in _read_plans`
- c0037 ..> c0072: `type in _read_problem`
- c0037 ..> c0072: `type in _repository_identities`
- c0037 ..> c0072: `type in poll`
- c0037 ..> c0090: `type in _read_problem`
- c0041 ..> c0040: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0042 --> c0043: `field forgetful`
- c0042 --> c0086: `field repository`
- c0043 ..> c0044: `_validate_server() calls loopback_host()`
- c0043 ..> c0044: `_validate_server() calls nonblank()`
- c0043 ..> c0090: `_validate_server() constructs FactoryError`
- c0044 ..> c0042: `from_mapping() constructs FactoryConfiguration`
- c0044 ..> c0042: `type in from_mapping`
- c0044 ..> c0042: `type in validate`
- c0044 ..> c0043: `connection_from_mapping() constructs ForgetfulConnection`
- c0044 ..> c0043: `type in connection_from_mapping`
- c0044 ..> c0043: `validate() calls _validate_server()`
- c0044 ..> c0044: `connection_from_mapping() calls validate()`
- c0044 ..> c0044: `from_mapping() calls connection_from_mapping()`
- c0044 ..> c0044: `from_mapping() calls validate()`
- c0044 ..> c0044: `unique_labels() calls nonblank()`
- c0044 ..> c0044: `validate() calls nonblank()`
- c0044 ..> c0086: `from_mapping() constructs RepositoryReference`
- c0044 ..> c0087: `from_mapping() constructs WorkSource`
- c0044 ..> c0090: `connection_from_mapping() constructs FactoryError`
- c0044 ..> c0090: `from_mapping() constructs FactoryError`
- c0044 ..> c0090: `nonblank() constructs FactoryError`
- c0044 ..> c0090: `validate() constructs FactoryError`
- c0045 ..> c0015: `check_repository() calls origin()`
- c0045 ..> c0029: `ownership() calls tasks()`
- c0045 ..> c0031: `check_source() calls source_from_remote()`
- c0045 ..> c0042: `type in __init__`
- c0045 ..> c0045: `check_repository() calls check_source()`
- c0045 ..> c0045: `ownership() calls ownership_records()`
- c0045 ..> c0054: `type in __init__`
- c0045 ..> c0055: `type in __init__`
- c0045 ..> c0058: `type in __init__`
- c0045 ..> c0068: `check_repository() constructs RepositoryProblem`
- c0045 ..> c0068: `check_source() constructs RepositoryProblem`
- c0045 ..> c0069: `active() constructs ScaffoldProblem`
- c0045 ..> c0069: `context() constructs ScaffoldProblem`
- c0045 ..> c0069: `mapping_repository() constructs ScaffoldProblem`
- c0045 ..> c0069: `ownership_records() constructs ScaffoldProblem`
- c0045 ..> c0069: `snapshot() constructs ScaffoldProblem`
- c0045 ..> c0084: `snapshot() constructs Issue`
- c0045 ..> c0084: `type in snapshot`
- c0045 ..> c0086: `type in check_repository`
- c0045 ..> c0086: `type in check_source`
- c0045 ..> c0086: `type in mapping_repository`
- c0045 ..> c0087: `check_source() constructs WorkSource`
- c0045 ..> c0087: `snapshot() constructs WorkSource`
- c0047 ..> c0044: `_validate_foreman_memory() calls nonblank()`
- c0047 ..> c0044: `skill_paths() calls nonblank()`
- c0047 ..> c0044: `validate_initial_agents() calls nonblank()`
- c0047 ..> c0044: `validate_workers() calls nonblank()`
- c0047 ..> c0046: `type in _validate_foreman_memory`
- c0047 ..> c0046: `type in validate_initial_agents`
- c0047 ..> c0046: `type in validate_workers`
- c0047 ..> c0047: `validate_initial_agents() calls _validate_foreman_memory()`
- c0047 ..> c0047: `validate_initial_agents() calls validate_role_app()`
- c0047 ..> c0047: `validate_initial_agents() calls validate_workers()`
- c0047 ..> c0047: `validate_workers() calls validate_role_app()`
- c0047 ..> c0090: `_validate_foreman_memory() constructs FactoryError`
- c0047 ..> c0090: `skill_paths() constructs FactoryError`
- c0047 ..> c0090: `validate_initial_agents() constructs FactoryError`
- c0047 ..> c0090: `validate_role_app() constructs FactoryError`
- c0047 ..> c0090: `validate_workers() constructs FactoryError`
- c0048 ..> c0004: `initialise() calls save()`
- c0048 ..> c0009: `load_existing() calls load()`
- c0048 ..> c0009: `prepare_foreman() calls confirm()`
- c0048 ..> c0011: `prepare_foreman() calls prepare()`
- c0048 ..> c0013: `check_foreman() calls check()`
- c0048 ..> c0013: `check_foreman() calls login()`
- c0048 ..> c0013: `prepare_foreman() calls install()`
- c0048 ..> c0013: `prepare_foreman() calls installation()`
- c0048 ..> c0013: `prepare_foreman() calls missing_executables()`
- c0048 ..> c0015: `_preflight() calls origin()`
- c0048 ..> c0015: `discover() calls discover()`
- c0048 ..> c0015: `inspect() calls origin()`
- c0048 ..> c0031: `_ensure_label() calls create_label()`
- c0048 ..> c0031: `_preflight() calls check_access()`
- c0048 ..> c0031: `_preflight() calls list_labels()`
- c0048 ..> c0031: `_preflight() calls source_from_remote()`
- c0048 ..> c0031: `inspect() calls source_from_remote()`
- c0048 ..> c0042: `configure() constructs FactoryConfiguration`
- c0048 ..> c0042: `type in _preflight`
- c0048 ..> c0042: `type in check_foreman`
- c0048 ..> c0042: `type in configure`
- c0048 ..> c0042: `type in initialise`
- c0048 ..> c0042: `type in load_existing`
- c0048 ..> c0043: `_preflight() calls validate()`
- c0048 ..> c0043: `type in prepare_foreman`
- c0048 ..> c0044: `configure() calls unique_labels()`
- c0048 ..> c0044: `load_existing() calls unique_labels()`
- c0048 ..> c0048: `configure() calls inspect()`
- c0048 ..> c0048: `initialise() calls _ensure_label()`
- c0048 ..> c0048: `initialise() calls _preflight()`
- c0048 ..> c0051: `type in __init__`
- c0048 ..> c0052: `type in __init__`
- c0048 ..> c0054: `type in __init__`
- c0048 ..> c0058: `type in __init__`
- c0048 ..> c0085: `_ensure_label() constructs Label`
- c0048 ..> c0085: `type in _preflight`
- c0048 ..> c0086: `inspect() constructs RepositoryReference`
- c0048 ..> c0086: `type in inspect`
- c0048 ..> c0087: `type in _ensure_label`
- c0048 ..> c0087: `type in _preflight`
- c0048 ..> c0088: `type in __init__`
- c0048 ..> c0090: `_preflight() constructs FactoryError`
- c0048 ..> c0090: `initialise() constructs FactoryError`
- c0048 ..> c0090: `inspect() constructs FactoryError`
- c0048 ..> c0090: `load_existing() constructs FactoryError`
- c0048 ..> c0090: `prepare_foreman() constructs FactoryError`
- c0049 ..> c0050: `type in confirm`
- c0049 ..> c0050: `type in load`
- c0051 ..> c0042: `type in load`
- c0051 ..> c0042: `type in save`
- c0052 ..> c0042: `type in prepare_roles`
- c0052 ..> c0042: `type in record_completion`
- c0052 ..> c0042: `type in selected_launch`
- c0052 ..> c0043: `type in check`
- c0052 ..> c0043: `type in create_project`
- c0052 ..> c0043: `type in list_models`
- c0052 ..> c0043: `type in login`
- c0052 ..> c0043: `type in missing_executables`
- c0052 ..> c0043: `type in prepare`
- c0052 ..> c0043: `type in projects`
- c0052 ..> c0043: `type in uses_browser_login`
- c0052 ..> c0046: `type in prepare_roles`
- c0056 --|> c0090: `inherits`
- c0058 ..> c0087: `type in source_from_remote`
- c0059 ..> c0000: `__init__() calls __init__()`
- c0059 --|> c0090: `inherits`
- c0060 --|> c0090: `inherits`
- c0062 ..> c0013: `check() calls check()`
- c0062 ..> c0017: `_ensure_mapping() calls ensure()`
- c0062 ..> c0017: `_ensure_mapping() calls verify_removed()`
- c0062 ..> c0017: `_initial_mappings() calls target_branch()`
- c0062 ..> c0017: `preflight() calls inspect()`
- c0062 ..> c0029: `_create_ownership() calls create_task()`
- c0062 ..> c0029: `_create_ownership() calls update_plan()`
- c0062 ..> c0029: `_create_plan() calls create_plan()`
- c0062 ..> c0029: `_create_plan() calls get_plan()`
- c0062 ..> c0029: `_create_plan() calls plans()`
- c0062 ..> c0029: `_recovery_plan() calls get_plan()`
- c0062 ..> c0029: `_recovery_plan() calls plans()`
- c0062 ..> c0029: `lookup() calls plans()`
- c0062 ..> c0029: `unfinished() calls plans()`
- c0062 ..> c0035: `recover() calls snapshot()`
- c0062 ..> c0041: `_ensure_mapping() calls validate_cleanup_marker()`
- c0062 ..> c0042: `type in __init__`
- c0062 ..> c0045: `__init__() constructs FactoryRecords`
- c0062 ..> c0045: `_create_ownership() calls ownership()`
- c0062 ..> c0045: `_ensure_mapping() calls check_source()`
- c0062 ..> c0045: `_ensure_worktrees() calls mapping_repository()`
- c0062 ..> c0045: `_prepare_plan() calls active()`
- c0062 ..> c0045: `_prepare_plan() calls context()`
- c0062 ..> c0045: `_setup_ownership() calls ownership()`
- c0062 ..> c0045: `check_repository() calls check_repository()`
- c0062 ..> c0045: `recover() calls active()`
- c0062 ..> c0045: `recover() calls context()`
- c0062 ..> c0045: `recover() calls ownership()`
- c0062 ..> c0054: `type in __init__`
- c0062 ..> c0055: `type in __init__`
- c0062 ..> c0058: `type in __init__`
- c0062 ..> c0061: `type in __init__`
- c0062 ..> c0062: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0062 ..> c0062: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0062 ..> c0062: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0062 ..> c0062: `_initial_mappings() calls _repository()`
- c0062 ..> c0062: `_prepare_plan() calls _create_ownership()`
- c0062 ..> c0062: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0062 ..> c0062: `_prepare_plan() calls _setup_ownership()`
- c0062 ..> c0062: `preflight() calls _initial_mappings()`
- c0062 ..> c0062: `preflight() calls _repository()`
- c0062 ..> c0062: `preflight() calls check_repository()`
- c0062 ..> c0062: `prepare() calls _create_plan()`
- c0062 ..> c0062: `prepare() calls _prepare_plan()`
- c0062 ..> c0062: `prepare() calls lookup()`
- c0062 ..> c0062: `prepare() calls preflight()`
- c0062 ..> c0062: `prepare() calls recover()`
- c0062 ..> c0062: `recover() calls _ensure_worktrees()`
- c0062 ..> c0062: `recover() calls _recovery_plan()`
- c0062 ..> c0062: `recover() calls _repository()`
- c0062 ..> c0062: `recover() calls _sole_recovery_owner()`
- c0062 ..> c0062: `recover() calls _validate_recovery_candidates()`
- c0062 ..> c0062: `recover() calls check_repository()`
- c0062 ..> c0062: `unfinished() calls _is_unfinished_factory_plan()`
- c0062 ..> c0067: `preflight() constructs IntakeProblem`
- c0062 ..> c0069: `_create_plan() constructs ScaffoldProblem`
- c0062 ..> c0069: `_ensure_mapping() constructs ScaffoldProblem`
- c0062 ..> c0069: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0062 ..> c0069: `_recovery_plan() constructs ScaffoldProblem`
- c0062 ..> c0069: `_setup_ownership() constructs ScaffoldProblem`
- c0062 ..> c0069: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0062 ..> c0069: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0062 ..> c0069: `lookup() constructs ScaffoldProblem`
- c0062 ..> c0070: `_create_plan() constructs ScaffoldReadProblem`
- c0062 ..> c0070: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0062 ..> c0070: `lookup() constructs ScaffoldReadProblem`
- c0062 ..> c0070: `prepare() constructs ScaffoldReadProblem`
- c0062 ..> c0070: `recover() constructs ScaffoldReadProblem`
- c0062 ..> c0071: `_create_ownership() constructs UncertainScaffold`
- c0062 ..> c0071: `_create_plan() constructs UncertainScaffold`
- c0062 ..> c0071: `_setup_ownership() constructs UncertainScaffold`
- c0062 ..> c0071: `_sole_recovery_owner() constructs UncertainScaffold`
- c0062 ..> c0071: `prepare() constructs UncertainScaffold`
- c0062 ..> c0084: `type in _create_plan`
- c0062 ..> c0084: `type in _initial_mappings`
- c0062 ..> c0084: `type in _prepare_plan`
- c0062 ..> c0084: `type in _setup_ownership`
- c0062 ..> c0084: `type in lookup`
- c0062 ..> c0084: `type in preflight`
- c0062 ..> c0084: `type in prepare`
- c0062 ..> c0084: `type in recover`
- c0062 ..> c0086: `type in _ensure_validated_mapping`
- c0062 ..> c0086: `type in _repository`
- c0062 ..> c0086: `type in check_repository`
- c0062 ..> c0087: `type in _repository`
- c0062 ..> c0090: `_is_unfinished_factory_plan() constructs FactoryError`
- c0063 --> c0084: `field issue`
- c0064 ..> c0000: `_alert_plan() calls send()`
- c0064 ..> c0000: `_check_pending_repositories() calls send()`
- c0064 ..> c0000: `_check_planning_access() calls send()`
- c0064 ..> c0000: `_handle_intake_read_problem() calls send()`
- c0064 ..> c0000: `_handle_intake_repository_problem() calls send()`
- c0064 ..> c0000: `_handle_recovery_read_problem() calls send()`
- c0064 ..> c0000: `_load_inventory() calls send()`
- c0064 ..> c0000: `_process_issue() calls send()`
- c0064 ..> c0000: `_read_issues() calls send()`
- c0064 ..> c0000: `_recover_work() calls send()`
- c0064 ..> c0000: `_submit() calls send()`
- c0064 ..> c0000: `_watch() calls close()`
- c0064 ..> c0000: `_watch() calls start()`
- c0064 ..> c0000: `_watch() calls wait()`
- c0064 ..> c0000: `run() calls startup_hint()`
- c0064 ..> c0011: `_process_issue() calls prepare()`
- c0064 ..> c0013: `_check_planning_access() calls check()`
- c0064 ..> c0031: `_read_issues() calls list_issues()`
- c0064 ..> c0037: `_watch() calls poll()`
- c0064 ..> c0037: `type in __init__`
- c0064 ..> c0042: `type in _poll_sources`
- c0064 ..> c0042: `type in _repository_for_source`
- c0064 ..> c0042: `type in _watch`
- c0064 ..> c0042: `type in run`
- c0064 ..> c0045: `_check_pending_repositories() calls check_repository()`
- c0064 ..> c0053: `type in __init__`
- c0064 ..> c0062: `_load_inventory() calls unfinished()`
- c0064 ..> c0062: `_process_issue() calls lookup()`
- c0064 ..> c0062: `_process_issue() calls recover()`
- c0064 ..> c0062: `_recover_work() calls recover()`
- c0064 ..> c0062: `type in __init__`
- c0064 ..> c0063: `_complete_intake() constructs BlockedWork`
- c0064 ..> c0063: `_handle_intake_read_problem() constructs BlockedWork`
- c0064 ..> c0063: `_handle_intake_repository_problem() constructs BlockedWork`
- c0064 ..> c0063: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0064 ..> c0063: `_process_issue() constructs BlockedWork`
- c0064 ..> c0063: `_remember_inventory_candidate() constructs BlockedWork`
- c0064 ..> c0063: `type in _alert_plan`
- c0064 ..> c0063: `type in _complete_intake`
- c0064 ..> c0063: `type in _complete_recovery`
- c0064 ..> c0063: `type in _handle_recovery_read_problem`
- c0064 ..> c0063: `type in _handle_recovery_repository_problem`
- c0064 ..> c0063: `type in _recover_work`
- c0064 ..> c0063: `type in _remember_task_ids`
- c0064 ..> c0064: `_complete_intake() calls _submit()`
- c0064 ..> c0064: `_complete_recovery() calls _submit()`
- c0064 ..> c0064: `_handle_intake_read_problem() calls _sole_task_id()`
- c0064 ..> c0064: `_handle_intake_repository_problem() calls _alert_plan()`
- c0064 ..> c0064: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0064 ..> c0064: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0064 ..> c0064: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0064 ..> c0064: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0064 ..> c0064: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0064 ..> c0064: `_load_inventory() calls _remember_inventory_candidate()`
- c0064 ..> c0064: `_poll_sources() calls _baseline_source()`
- c0064 ..> c0064: `_poll_sources() calls _process_source()`
- c0064 ..> c0064: `_poll_sources() calls _read_issues()`
- c0064 ..> c0064: `_poll_sources() calls _repository_for_source()`
- c0064 ..> c0064: `_process_issue() calls _complete_intake()`
- c0064 ..> c0064: `_process_issue() calls _handle_intake_read_problem()`
- c0064 ..> c0064: `_process_issue() calls _handle_intake_repository_problem()`
- c0064 ..> c0064: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0064 ..> c0064: `_process_issues() calls _process_issue()`
- c0064 ..> c0064: `_process_issues() calls _skip_issue()`
- c0064 ..> c0064: `_process_source() calls _include_pending_lookups()`
- c0064 ..> c0064: `_process_source() calls _process_issues()`
- c0064 ..> c0064: `_recover_blocked() calls _recover_work()`
- c0064 ..> c0064: `_recover_work() calls _alert_plan()`
- c0064 ..> c0064: `_recover_work() calls _complete_recovery()`
- c0064 ..> c0064: `_recover_work() calls _handle_recovery_read_problem()`
- c0064 ..> c0064: `_recover_work() calls _handle_recovery_repository_problem()`
- c0064 ..> c0064: `_recover_work() calls _remember_task_ids()`
- c0064 ..> c0064: `_remember_inventory_candidate() calls _alert_plan()`
- c0064 ..> c0064: `_watch() calls _check_pending_repositories()`
- c0064 ..> c0064: `_watch() calls _check_planning_access()`
- c0064 ..> c0064: `_watch() calls _load_inventory()`
- c0064 ..> c0064: `_watch() calls _poll_sources()`
- c0064 ..> c0064: `_watch() calls _recover_blocked()`
- c0064 ..> c0064: `run() calls _watch()`
- c0064 ..> c0065: `_watch() constructs _WatchState`
- c0064 ..> c0065: `type in _baseline_source`
- c0064 ..> c0065: `type in _check_pending_repositories`
- c0064 ..> c0065: `type in _check_planning_access`
- c0064 ..> c0065: `type in _complete_intake`
- c0064 ..> c0065: `type in _complete_recovery`
- c0064 ..> c0065: `type in _handle_intake_read_problem`
- c0064 ..> c0065: `type in _handle_intake_repository_problem`
- c0064 ..> c0065: `type in _handle_intake_scaffold_problem`
- c0064 ..> c0065: `type in _handle_recovery_repository_problem`
- c0064 ..> c0065: `type in _load_inventory`
- c0064 ..> c0065: `type in _poll_sources`
- c0064 ..> c0065: `type in _process_issue`
- c0064 ..> c0065: `type in _process_issues`
- c0064 ..> c0065: `type in _process_source`
- c0064 ..> c0065: `type in _recover_blocked`
- c0064 ..> c0065: `type in _recover_work`
- c0064 ..> c0065: `type in _remember_inventory_candidate`
- c0064 ..> c0065: `type in _skip_issue`
- c0064 ..> c0066: `type in _process_issue`
- c0064 ..> c0066: `type in _recover_work`
- c0064 ..> c0068: `type in _handle_intake_repository_problem`
- c0064 ..> c0068: `type in _handle_recovery_repository_problem`
- c0064 ..> c0069: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0064 ..> c0069: `type in _alert_plan`
- c0064 ..> c0069: `type in _handle_intake_scaffold_problem`
- c0064 ..> c0070: `type in _handle_intake_read_problem`
- c0064 ..> c0070: `type in _handle_recovery_read_problem`
- c0064 ..> c0072: `_check_pending_repositories() calls clear()`
- c0064 ..> c0072: `_check_planning_access() calls clear()`
- c0064 ..> c0072: `_complete_intake() calls clear()`
- c0064 ..> c0072: `_complete_recovery() calls clear()`
- c0064 ..> c0072: `_load_inventory() calls clear()`
- c0064 ..> c0072: `_process_issue() calls clear()`
- c0064 ..> c0072: `_read_issues() calls clear()`
- c0064 ..> c0072: `_watch() calls clear()`
- c0064 ..> c0072: `_watch() constructs WatcherAlerts`
- c0064 ..> c0072: `type in _alert_plan`
- c0064 ..> c0072: `type in _check_pending_repositories`
- c0064 ..> c0072: `type in _check_planning_access`
- c0064 ..> c0072: `type in _complete_intake`
- c0064 ..> c0072: `type in _complete_recovery`
- c0064 ..> c0072: `type in _handle_intake_read_problem`
- c0064 ..> c0072: `type in _handle_intake_repository_problem`
- c0064 ..> c0072: `type in _handle_intake_scaffold_problem`
- c0064 ..> c0072: `type in _handle_recovery_read_problem`
- c0064 ..> c0072: `type in _handle_recovery_repository_problem`
- c0064 ..> c0072: `type in _load_inventory`
- c0064 ..> c0072: `type in _poll_sources`
- c0064 ..> c0072: `type in _process_issue`
- c0064 ..> c0072: `type in _process_issues`
- c0064 ..> c0072: `type in _process_source`
- c0064 ..> c0072: `type in _read_issues`
- c0064 ..> c0072: `type in _recover_blocked`
- c0064 ..> c0072: `type in _recover_work`
- c0064 ..> c0072: `type in _remember_inventory_candidate`
- c0064 ..> c0084: `type in _baseline_source`
- c0064 ..> c0084: `type in _complete_intake`
- c0064 ..> c0084: `type in _complete_recovery`
- c0064 ..> c0084: `type in _handle_intake_read_problem`
- c0064 ..> c0084: `type in _handle_intake_repository_problem`
- c0064 ..> c0084: `type in _handle_intake_scaffold_problem`
- c0064 ..> c0084: `type in _include_pending_lookups`
- c0064 ..> c0084: `type in _process_issue`
- c0064 ..> c0084: `type in _process_issues`
- c0064 ..> c0084: `type in _process_source`
- c0064 ..> c0084: `type in _read_issues`
- c0064 ..> c0084: `type in _skip_issue`
- c0064 ..> c0084: `type in _submit`
- c0064 ..> c0086: `type in _handle_intake_repository_problem`
- c0064 ..> c0086: `type in _process_issue`
- c0064 ..> c0086: `type in _process_issues`
- c0064 ..> c0086: `type in _process_source`
- c0064 ..> c0086: `type in _repository_for_source`
- c0064 ..> c0087: `_watch() constructs WorkSource`
- c0064 ..> c0087: `type in _baseline_source`
- c0064 ..> c0087: `type in _include_pending_lookups`
- c0064 ..> c0087: `type in _poll_sources`
- c0064 ..> c0087: `type in _process_source`
- c0064 ..> c0087: `type in _read_issues`
- c0064 ..> c0087: `type in _repository_for_source`
- c0064 ..> c0088: `type in __init__`
- c0064 ..> c0090: `_read_issues() constructs FactoryError`
- c0064 ..> c0095: `_submit() calls check_watch_stop()`
- c0064 ..> c0095: `_watch() calls check_watch_stop()`
- c0064 ..> c0095: `run() calls check_watch_stop()`
- c0065 --> c0063: `field blocked`
- c0065 --> c0063: `field known`
- c0065 --> c0084: `field pending_lookup`
- c0065 --> c0086: `field pending_repositories`
- c0065 --> c0087: `field baselined`
- c0067 --|> c0069: `inherits`
- c0068 --|> c0069: `inherits`
- c0069 --|> c0090: `inherits`
- c0070 --|> c0069: `inherits`
- c0071 --|> c0069: `inherits`
- c0072 ..> c0000: `__init__() calls __init__()`
- c0072 ..> c0000: `send() calls send()`
- c0072 ..> c0073: `send() calls _cleanup_recovery()`
- c0072 ..> c0090: `type in send`
- c0074 ..> c0007: `build_watcher() constructs AgentShellTerminal`
- c0074 ..> c0009: `build_watcher() constructs FileCleanupReceipts`
- c0074 ..> c0013: `build_initialiser() constructs ForemanProfile`
- c0074 ..> c0013: `build_watcher() calls managed_memory_notice()`
- c0074 ..> c0013: `prepare_foreman_launch() calls pi_home()`
- c0074 ..> c0013: `prepare_foreman_launch() calls selected_launch()`
- c0074 ..> c0013: `prepare_foreman_launch() calls validate_completion()`
- c0074 ..> c0013: `prepare_foreman_launch() constructs ForemanProfile`
- c0074 ..> c0015: `build_initialiser() constructs GitRepositories`
- c0074 ..> c0015: `build_watcher() constructs GitRepositories`
- c0074 ..> c0017: `build_watcher() constructs GitWorktrees`
- c0074 ..> c0022: `build_initialiser() constructs TomlConfigurationStore`
- c0074 ..> c0028: `prepare_foreman_launch() calls role_environment()`
- c0074 ..> c0029: `build_watcher() constructs ForgetfulPlanning`
- c0074 ..> c0031: `build_initialiser() constructs GitHubWorkTracking`
- c0074 ..> c0031: `build_watcher() calls check_cli()`
- c0074 ..> c0031: `build_watcher() calls source_from_remote()`
- c0074 ..> c0031: `build_watcher() constructs GitHubWorkTracking`
- c0074 ..> c0034: `build_watcher() constructs ObservedTerminal`
- c0074 ..> c0037: `build_watcher() constructs CleanupCompleted`
- c0074 ..> c0042: `type in build_watcher`
- c0074 ..> c0042: `type in prepare_foreman_launch`
- c0074 ..> c0048: `build_initialiser() constructs InitialiseFactory`
- c0074 ..> c0048: `type in build_initialiser`
- c0074 ..> c0062: `build_watcher() constructs ScaffoldIssue`
- c0074 ..> c0064: `build_watcher() constructs WatchFactory`
- c0074 ..> c0064: `type in build_watcher`
- c0074 ..> c0074: `build_watcher() calls prepare_foreman_launch()`
- c0074 ..> c0082: `build_initialiser() constructs DeadlinePolicy`
- c0074 ..> c0082: `build_watcher() constructs DeadlinePolicy`
- c0074 ..> c0082: `type in build_initialiser`
- c0074 ..> c0082: `type in build_watcher`
- c0074 ..> c0090: `build_watcher() constructs FactoryError`
- c0074 ..> c0090: `prepare_foreman_launch() constructs FactoryError`
- c0075 ..> c0042: `type in agree_definition_of_done`
- c0075 ..> c0075: `agree_definition_of_done() calls _deployment_agreement()`
- c0075 ..> c0090: `_deployment_agreement() constructs FactoryError`
- c0075 ..> c0090: `agree_definition_of_done() constructs FactoryError`
- c0075 ..> c0091: `agree_definition_of_done() calls check_skill_file()`
- c0075 ..> c0091: `agree_definition_of_done() calls write_new()`
- c0076 --> c0042: `field config`
- c0076 --> c0043: `field connection`
- c0077 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0077 ..> c0004: `_watch_locked() calls run()`
- c0077 ..> c0006: `_change_managed_watch() calls request()`
- c0077 ..> c0006: `_finish_existing_setup() calls read_state()`
- c0077 ..> c0006: `_foreman() calls enter_terminal()`
- c0077 ..> c0006: `_foreman() calls read_state()`
- c0077 ..> c0006: `_foreman() calls request()`
- c0077 ..> c0006: `_foreman() calls start_owner()`
- c0077 ..> c0006: `_initialise() calls enter_terminal()`
- c0077 ..> c0006: `_initialise() calls request()`
- c0077 ..> c0006: `_initialise_locked() calls read_state()`
- c0077 ..> c0006: `_launch_setup_foreman() calls start_owner()`
- c0077 ..> c0006: `_managed_watch_status() calls read_state()`
- c0077 ..> c0006: `_managed_watch_status() calls request()`
- c0077 ..> c0006: `_offer_factory_launch() calls read_state()`
- c0077 ..> c0006: `_watch_locked() calls read_state()`
- c0077 ..> c0009: `_initialise_locked() calls load()`
- c0077 ..> c0013: `_complete_setup() calls managed_memory_notice()`
- c0077 ..> c0013: `_complete_setup() calls record_completion()`
- c0077 ..> c0013: `_complete_setup() calls uses_browser_login()`
- c0077 ..> c0013: `_discover_worker_models() calls list_models()`
- c0077 ..> c0013: `_finish_existing_setup() calls choose_pi_home()`
- c0077 ..> c0013: `_finish_existing_setup() calls save_pi_choice()`
- c0077 ..> c0013: `_finish_existing_setup() calls selected_launch()`
- c0077 ..> c0013: `_foreman() calls managed_memory_notice()`
- c0077 ..> c0013: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0077 ..> c0013: `_select_model() calls list_models()`
- c0077 ..> c0013: `_select_project() calls create_project()`
- c0077 ..> c0013: `_select_project() calls projects()`
- c0077 ..> c0013: `_start_initial_setup() calls begin_setup()`
- c0077 ..> c0013: `_start_initial_setup() calls choose_pi_home()`
- c0077 ..> c0013: `_validate_initial_model() calls prepare_roles()`
- c0077 ..> c0013: `_watch_status() calls validate_completion()`
- c0077 ..> c0013: `_watch_status() constructs ForemanProfile`
- c0077 ..> c0015: `select_repositories() calls discover()`
- c0077 ..> c0017: `_configure_new_factory() calls inspect()`
- c0077 ..> c0023: `_initialise() calls quote()`
- c0077 ..> c0023: `_launch_setup_foreman() calls quote()`
- c0077 ..> c0023: `_managed_watch_status() calls quote()`
- c0077 ..> c0023: `_select_model() calls quote()`
- c0077 ..> c0023: `_validate_setup_owner() calls quote()`
- c0077 ..> c0023: `_watch_locked() calls quote()`
- c0077 ..> c0024: `_foreman() calls hold()`
- c0077 ..> c0024: `_foreman() constructs WorkspaceWatchLease`
- c0077 ..> c0024: `_initialise() calls hold()`
- c0077 ..> c0024: `_initialise() constructs WorkspaceWatchLease`
- c0077 ..> c0024: `_watch() calls hold()`
- c0077 ..> c0024: `_watch() constructs WorkspaceWatchLease`
- c0077 ..> c0035: `_prompt_workers() calls update()`
- c0077 ..> c0036: `_managed_watch_status() calls unknown_status()`
- c0077 ..> c0036: `_watch_locked() calls observe_plain_watch()`
- c0077 ..> c0036: `_watch_status() calls plain_watch_status()`
- c0077 ..> c0036: `_watch_status() calls unknown_status()`
- c0077 ..> c0042: `type in _complete_setup`
- c0077 ..> c0042: `type in _configure_new_factory`
- c0077 ..> c0042: `type in _finish_existing_setup`
- c0077 ..> c0042: `type in _validate_initial_model`
- c0077 ..> c0043: `_connection() calls validate()`
- c0077 ..> c0043: `_connection() constructs ForgetfulConnection`
- c0077 ..> c0043: `type in _check_existing_connection`
- c0077 ..> c0043: `type in _configure_new_factory`
- c0077 ..> c0043: `type in _connection`
- c0077 ..> c0043: `type in _foreman_memory_choices`
- c0077 ..> c0043: `type in _managed_rest_mapping_available`
- c0077 ..> c0043: `type in _select_project`
- c0077 ..> c0046: `_configure_new_factory() constructs InitialAgentChoices`
- c0077 ..> c0046: `type in _configure_new_factory`
- c0077 ..> c0046: `type in _foreman_memory_choices`
- c0077 ..> c0046: `type in _owner_choices`
- c0077 ..> c0046: `type in _prompt_coordinator_choices`
- c0077 ..> c0046: `type in _validate_initial_model`
- c0077 ..> c0046: `type in _worker_choices`
- c0077 ..> c0047: `_start_initial_setup() calls validate_initial_agents()`
- c0077 ..> c0048: `_complete_setup() calls check_foreman()`
- c0077 ..> c0048: `_configure_new_factory() calls configure()`
- c0077 ..> c0048: `_finish_existing_setup() calls initialise()`
- c0077 ..> c0048: `_initialise_locked() calls load_existing()`
- c0077 ..> c0048: `_launch_setup_foreman() calls check_foreman()`
- c0077 ..> c0048: `_prepare_foreman() calls prepare_foreman()`
- c0077 ..> c0048: `_start_initial_setup() calls initialise()`
- c0077 ..> c0048: `type in _complete_setup`
- c0077 ..> c0048: `type in _configure_new_factory`
- c0077 ..> c0048: `type in _discover_worker_models`
- c0077 ..> c0048: `type in _finish_existing_setup`
- c0077 ..> c0048: `type in _select_project`
- c0077 ..> c0048: `type in _start_initial_setup`
- c0077 ..> c0048: `type in _validate_initial_model`
- c0077 ..> c0048: `type in select_repositories`
- c0077 ..> c0074: `_foreman() calls prepare_foreman_launch()`
- c0077 ..> c0074: `_initialise_locked() calls build_initialiser()`
- c0077 ..> c0074: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0077 ..> c0074: `_watch_locked() calls build_watcher()`
- c0077 ..> c0075: `_finish_existing_setup() calls agree_definition_of_done()`
- c0077 ..> c0075: `_start_initial_setup() calls agree_definition_of_done()`
- c0077 ..> c0076: `_start_initial_setup() constructs _InitialSetupState`
- c0077 ..> c0076: `type in _discover_worker_models`
- c0077 ..> c0076: `type in _validate_initial_model`
- c0077 ..> c0077: `_complete_setup() calls _managed_rest_mapping_available()`
- c0077 ..> c0077: `_configure_new_factory() calls _prepare_foreman()`
- c0077 ..> c0077: `_configure_new_factory() calls _select_model()`
- c0077 ..> c0077: `_configure_new_factory() calls _select_numbered()`
- c0077 ..> c0077: `_configure_new_factory() calls select_repositories()`
- c0077 ..> c0077: `_connection() calls _check_existing_connection()`
- c0077 ..> c0077: `_discover_worker_models() calls _prepare_foreman()`
- c0077 ..> c0077: `_finish_existing_setup() calls _complete_setup()`
- c0077 ..> c0077: `_finish_existing_setup() calls _confirm_pi_home()`
- c0077 ..> c0077: `_finish_existing_setup() calls _connection()`
- c0077 ..> c0077: `_finish_existing_setup() calls _launch_setup_foreman()`
- c0077 ..> c0077: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0077 ..> c0077: `_foreman_memory_choices() calls _select_numbered()`
- c0077 ..> c0077: `_initialise() calls _initialise_locked()`
- c0077 ..> c0077: `_initialise() calls _offer_factory_launch()`
- c0077 ..> c0077: `_initialise_locked() calls _finish_existing_setup()`
- c0077 ..> c0077: `_initialise_locked() calls _start_initial_setup()`
- c0077 ..> c0077: `_initialise_locked() calls _validate_setup_owner()`
- c0077 ..> c0077: `_print_models() calls _safe_diagnostic()`
- c0077 ..> c0077: `_prompt_coordinator_choices() calls _select_numbered()`
- c0077 ..> c0077: `_prompt_worker() calls _select_numbered()`
- c0077 ..> c0077: `_prompt_workers() calls _prompt_worker()`
- c0077 ..> c0077: `_select_model() calls _print_models()`
- c0077 ..> c0077: `_select_model() calls _select_numbered()`
- c0077 ..> c0077: `_select_numbered() calls _safe_diagnostic()`
- c0077 ..> c0077: `_select_project() calls _listed_project_id()`
- c0077 ..> c0077: `_select_project() calls _safe_diagnostic()`
- c0077 ..> c0077: `_select_setup_route() calls _select_numbered()`
- c0077 ..> c0077: `_start_initial_setup() calls _complete_setup()`
- c0077 ..> c0077: `_start_initial_setup() calls _configure_new_factory()`
- c0077 ..> c0077: `_start_initial_setup() calls _confirm_pi_home()`
- c0077 ..> c0077: `_start_initial_setup() calls _connection()`
- c0077 ..> c0077: `_start_initial_setup() calls _foreman_memory_choices()`
- c0077 ..> c0077: `_start_initial_setup() calls _launch_setup_foreman()`
- c0077 ..> c0077: `_start_initial_setup() calls _owner_choices()`
- c0077 ..> c0077: `_start_initial_setup() calls _research_choices()`
- c0077 ..> c0077: `_start_initial_setup() calls _worker_choices()`
- c0077 ..> c0077: `_validate_initial_model() calls _prepare_foreman()`
- c0077 ..> c0077: `_validate_initial_model() calls _select_model()`
- c0077 ..> c0077: `_validate_initial_model() calls _select_project()`
- c0077 ..> c0077: `_watch() calls _change_managed_watch()`
- c0077 ..> c0077: `_watch() calls _watch_locked()`
- c0077 ..> c0077: `_watch() calls _watch_status()`
- c0077 ..> c0077: `_watch_locked() calls _choose_existing()`
- c0077 ..> c0077: `_watch_locked() calls _safe_diagnostic()`
- c0077 ..> c0077: `_watch_status() calls _managed_watch_status()`
- c0077 ..> c0077: `_worker_choices() calls _prompt_coordinator_choices()`
- c0077 ..> c0077: `_worker_choices() calls _prompt_workers()`
- c0077 ..> c0077: `_worker_choices() calls _select_setup_route()`
- c0077 ..> c0077: `_worker_choices() calls _worker_arguments()`
- c0077 ..> c0077: `main() calls _foreman()`
- c0077 ..> c0077: `main() calls _initialise()`
- c0077 ..> c0077: `main() calls _parse_arguments()`
- c0077 ..> c0077: `main() calls _safe_diagnostic()`
- c0077 ..> c0077: `main() calls _watch()`
- c0077 ..> c0078: `_select_numbered() calls parse_numbered_selection()`
- c0077 ..> c0079: `main() calls update_resources()`
- c0077 ..> c0080: `_foreman() calls load_configuration()`
- c0077 ..> c0080: `_watch_locked() calls load_configuration()`
- c0077 ..> c0080: `_watch_status() calls load_configuration()`
- c0077 ..> c0082: `main() constructs DeadlinePolicy`
- c0077 ..> c0082: `type in _finish_existing_setup`
- c0077 ..> c0082: `type in _foreman`
- c0077 ..> c0082: `type in _initialise`
- c0077 ..> c0082: `type in _initialise_locked`
- c0077 ..> c0082: `type in _start_initial_setup`
- c0077 ..> c0082: `type in _watch`
- c0077 ..> c0082: `type in _watch_locked`
- c0077 ..> c0082: `type in main`
- c0077 ..> c0090: `_change_managed_watch() constructs FactoryError`
- c0077 ..> c0090: `_check_existing_connection() constructs FactoryError`
- c0077 ..> c0090: `_choose_existing() constructs FactoryError`
- c0077 ..> c0090: `_configure_new_factory() constructs FactoryError`
- c0077 ..> c0090: `_finish_existing_setup() constructs FactoryError`
- c0077 ..> c0090: `_foreman() constructs FactoryError`
- c0077 ..> c0090: `_foreman_memory_choices() constructs FactoryError`
- c0077 ..> c0090: `_initialise() constructs FactoryError`
- c0077 ..> c0090: `_initialise_locked() constructs FactoryError`
- c0077 ..> c0090: `_install_missing() constructs FactoryError`
- c0077 ..> c0090: `_listed_project_id() constructs FactoryError`
- c0077 ..> c0090: `_prompt_coordinator_choices() constructs FactoryError`
- c0077 ..> c0090: `_prompt_worker() constructs FactoryError`
- c0077 ..> c0090: `_select_model() constructs FactoryError`
- c0077 ..> c0090: `_select_project() constructs FactoryError`
- c0077 ..> c0090: `_validate_setup_owner() constructs FactoryError`
- c0077 ..> c0090: `_watch_locked() constructs FactoryError`
- c0077 ..> c0090: `_worker_choices() constructs FactoryError`
- c0077 ..> c0090: `main() constructs FactoryError`
- c0077 ..> c0090: `select_repositories() constructs FactoryError`
- c0077 ..> c0091: `_discover_worker_models() calls check_real_path()`
- c0077 ..> c0095: `_watch_locked() calls watch_stop_scope()`
- c0078 ..> c0090: `parse_numbered_selection() constructs FactoryError`
- c0079 ..> c0006: `update_resources() calls read_state()`
- c0079 ..> c0013: `update_resources() calls install()`
- c0079 ..> c0013: `update_resources() calls role_runtime_ready()`
- c0079 ..> c0013: `update_resources() calls validate_bundled_resources()`
- c0079 ..> c0013: `update_resources() constructs ForemanProfile`
- c0079 ..> c0020: `update_resources() calls apply_update()`
- c0079 ..> c0020: `update_resources() calls plan_update()`
- c0079 ..> c0024: `update_resources() calls hold()`
- c0079 ..> c0024: `update_resources() constructs WorkspaceWatchLease`
- c0079 ..> c0079: `update_resources() calls _report()`
- c0079 ..> c0082: `type in update_resources`
- c0079 ..> c0090: `_report() constructs FactoryError`
- c0079 ..> c0090: `update_resources() constructs FactoryError`
- c0080 ..> c0009: `load_configuration() calls load()`
- c0080 ..> c0022: `load_configuration() constructs TomlConfigurationStore`
- c0080 ..> c0042: `type in load_configuration`
- c0080 ..> c0090: `load_configuration() constructs FactoryError`
- c0082 --> c0081: `field agentshell`
- c0082 ..> c0083: `__post_init__() calls _validate_duration()`
- c0084 --> c0087: `field source`
- c0086 --> c0087: `field work_source`
- c0088 ..> c0084: `type in list_issues`
- c0088 ..> c0085: `type in create_label`
- c0088 ..> c0085: `type in list_labels`
- c0088 ..> c0087: `type in check_access`
- c0088 ..> c0087: `type in create_label`
- c0088 ..> c0087: `type in list_issues`
- c0088 ..> c0087: `type in list_labels`
- c0089 ..> c0004: `run_command() calls run()`
- c0089 ..> c0090: `run_command() constructs FactoryError`
- c0089 ..> c0095: `run_command() calls check_watch_stop()`
- c0091 ..> c0000: `_generated_parent() calls close()`
- c0091 ..> c0000: `check_skill_file() calls close()`
- c0091 ..> c0009: `read_generated_json() calls load()`
- c0091 ..> c0090: `_generated_parent() constructs FactoryError`
- c0091 ..> c0090: `check_real_path() constructs FactoryError`
- c0091 ..> c0090: `check_skill_file() constructs FactoryError`
- c0091 ..> c0090: `read_generated_json() constructs FactoryError`
- c0091 ..> c0090: `write_definition() constructs FactoryError`
- c0091 ..> c0090: `write_new() constructs FactoryError`
- c0091 ..> c0091: `_generated_parent() calls check_real_path()`
- c0091 ..> c0091: `check_skill_file() calls check_real_path()`
- c0091 ..> c0091: `read_generated_json() calls _generated_parent()`
- c0091 ..> c0091: `remove_generated() calls _generated_parent()`
- c0091 ..> c0091: `replace_generated_json() calls _generated_parent()`
- c0091 ..> c0091: `write_definition() calls read_generated_json()`
- c0091 ..> c0091: `write_definition() calls write_json()`
- c0091 ..> c0091: `write_json() calls write_new()`
- c0091 ..> c0091: `write_new() calls check_real_path()`
- c0093 ..> c0000: `_close_capture_streams() calls close()`
- c0093 ..> c0000: `_terminate_owned_process() calls wait()`
- c0093 ..> c0090: `run_owned() constructs FactoryError`
- c0093 ..> c0093: `_terminate_owned_process() calls _close_capture_streams()`
- c0093 ..> c0093: `run_owned() calls _terminate_owned_process()`
- c0093 ..> c0095: `run_owned() calls check_watch_stop()`
- c0095 ..> c0094: `watch_stop_scope() constructs WatchStop`

## Type key

- Type1: `object | None`
- Type2: `int | None`
- Type3: `str | None`
- Type4: `tuple[Path, Path, int]`
- Type5: `dict | None`
- Type6: `dict[str, str] | None`
- Type7: `subprocess.Popen | None`
- Type8: `dict[tuple[str, Path], list[str]]`
- Type9: `bool | None`
- Type10: `Path | None`
- Type11: `dict[str, list[str] | FactoryError]`
- Type12: `tuple[Path, list[dict]]`
- Type13: `tuple[Path, Path] | None`
- Type14: `tuple[Path, Path, dict | None]`
- Type15: `dict[str, bytes]`
- Type16: `tuple[str, ...]`
- Type17: `dict[Path, None]`
- Type18: `frozenset[tuple[int, int]]`
- Type19: `FactoryConfiguration | None`
- Type20: `dict[str, str]`
- Type21: `tuple[Label, ...]`
- Type22: `tuple[Issue, ...]`
- Type23: `list[tuple[int, str, str]]`
- Type24: `tuple[Path, ...]`
- Type25: `tuple[int, int]`
- Type26: `Iterator[PlainWatchObservation | None]`
- Type27: `Callable[[str], None]`
- Type28: `dict[int, int]`
- Type29: `tuple | None`
- Type30: `tuple[dict, dict] | None`
- Type31: `dict[int, list[dict]]`
- Type32: `list[dict] | None`
- Type33: `list[CompletedWork] | None`
- Type34: `CleanupState | None`
- Type35: `tuple[RepositoryReference, ...]`
- Type36: `ForgetfulConnection | None`
- Type37: `Callable[[list[str]], None]`
- Type38: `Callable[[str, str], bool]`
- Type39: `list[Path] | None`
- Type40: `list[str] | None`
- Type41: `dict[str, RepositoryReference]`
- Type42: `dict[WorkSource, tuple[Label, ...]]`
- Type43: `Callable[[], FactoryConfiguration | None]`
- Type44: `'CleanupSet'`
- Type45: `tuple[list[dict], list[dict]]`
- Type46: `tuple[Issue, dict] | None`
- Type47: `Issue | None`
- Type48: `tuple[int, ...] | None`
- Type49: `tuple[int, ...]`
- Type50: `Callable[[], bool]`
- Type51: `tuple[set[str], bool]`
- Type52: `tuple[WorkSource, ...]`
- Type53: `dict[str, Issue]`
- Type54: `BlockedWork | None`
- Type55: `tuple[Issue, ...] | None`
- Type56: `dict[str, BlockedWork]`
- Type57: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type58: `list[str] | tuple[str, ...]`
- Type59: `int | dict`
- Type60: `int | dict | str`
- Type61: `str | Path`
- Type62: `float | None`

## Signature key

- Signature1: `+interact(session: unknown, reader: unknown, reply: unknown, name: unknown,
  deadlines: unknown, persistent: unknown, startup_warning: unknown) None`
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
- Signature8: `+start_owner(workspace: Path, python: str, environment: dict, launch: dict,
  deadlines: AgentShellLifecycleDeadlines) dict`
- Signature9: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None, model: str | None, effort: str | None, deadlines:
  AgentShellLifecycleDeadlines) unknown`
- Signature10: `-_write_agent(name: unknown, model: unknown, effort: unknown, description: unknown,
  children: unknown, resources: unknown) unknown`
- Signature11: `+validate_setup(connection: ForgetfulConnection, include_home_system_prompt: bool,
  include_memory_extension: bool) None`
- Signature12: `-_validate_registered_worktree(root: Path, target: Path, branch: str, path: str,
  match: dict) None`
- Signature13: `-_disposal_state(repository: str, branch: str, path: str, remote: str,
  target_branch: str) tuple[Path, Path, dict | None]`
- Signature14: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature15: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool,
  term_grace: float) unknown`
- Signature16: `-__init__(records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts)
  unknown`
- Signature17: `-_claim_indexes(inventory: list[dict], plans: list[dict], tasks: dict[int,
  list[dict]], identities: dict[str, str], alerts: WatcherAlerts) tuple[dict, dict] | None`
- Signature18: `-_dispose(work: CompletedWork, mapping: dict, claims: dict, references: dict,
  identities: dict[str, str], alerts: WatcherAlerts, report: unknown) bool`
- Signature19: `-_mapping_identity(plan_id: int, reference: str, mapping: dict, workspace: str |
  None) CleanupSet`
- Signature20: `-__init__(planning: Planning, workspace: Path, config: FactoryConfiguration,
  repositories: LocalRepositories, sources: WorkSourceResolver) unknown`
- Signature21: `-__init__(tracking: WorkTrackingService, storage: ConfigurationStore, repositories:
  LocalRepositories, sources: WorkSourceResolver, profile: ForemanProfile) unknown`
- Signature22: `-__init__(planning: Planning, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, sources: WorkSourceResolver) unknown`
- Signature23: `-_setup_ownership(plan_id: int, issue: Issue, context: dict, initial_mappings:
  list[dict]) tuple[list[dict], list[dict]]`
- Signature24: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature25: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature26: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature27: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, scaffold:
  ScaffoldIssue, cleanup: CleanupCompleted) unknown`
- Signature28: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature29: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature30: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature31: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature32: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature33: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature34: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Issue, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature35: `-_poll_sources(sources: tuple[WorkSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature36: `-_process_source(source: WorkSource, issues: tuple[Issue, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature37: `-_baseline_source(source: WorkSource, issues: tuple[Issue, ...], state: _WatchState,
  report: Callable[[str], None]) None`
- Signature38: `-_repository_for_source(config: FactoryConfiguration, source: WorkSource)
  RepositoryReference`
- Signature39: `-_include_pending_lookups(source: WorkSource, current: dict[str, Issue],
  pending_lookup: dict[str, Issue]) None`
- Signature40: `-_process_issues(issues: tuple[Issue, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature41: `-_process_issue(issue: Issue, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature42: `-_handle_intake_repository_problem(issue: Issue, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature43: `-_handle_intake_read_problem(issue: Issue, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature44: `-_handle_intake_scaffold_problem(issue: Issue, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature45: `-_complete_intake(issue: Issue, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature46: `-_submit(issue: Issue, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature47: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature48: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature49: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown, deadlines: DeadlinePolicy, observation: unknown) WatchFactory`
- Signature50: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown, term_grace: float) unknown`
- Signature51: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature52: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature53: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature54: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature55: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature56: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature57: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature58: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature59: `-_foreman_memory_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown, connection: ForgetfulConnection) InitialAgentChoices`
- Signature60: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature61: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature62: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int |
  dict`
- Signature63: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature64: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature65: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None, deadlines: DeadlinePolicy) int | dict`
- Signature66: `-_initialise_locked(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int | dict | str`
- Signature67: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown, deadlines: unknown) unknown`
- Signature68: `+update_resources(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int`
- Signature69: `+run_owned(args: list[str], cwd: Path, env: dict[str, str], login: bool, timeout:
  float | None, term_grace: float) str`

## Extraction warnings

- `Unresolved or out-of-scope base: CleanupMarkerError -> ValueError`
- `Unresolved or out-of-scope base: CleanupReceipts -> Protocol`
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
