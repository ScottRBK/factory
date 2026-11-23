# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 101 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 5274. Type relationships removed: 94.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/contracts/forge.py`: 12 source occurrences (test-path).
- `tests/contracts/planning.py`: 8 source occurrences (test-path).
- `tests/contracts/ticketing.py`: 29 source occurrences (test-path).
- `tests/deadline_support.py`: 2 source occurrences (test-path).
- `tests/fixtures/previous-pi-forgetful-factory.ts`: 18 source occurrences (test-path).
- `tests/lifecycle_support.py`: 21 source occurrences (test-path).
- `tests/poll_support.py`: 9 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_agent_definitions.py`: 21 source occurrences (test-path).
- `tests/test_architecture.py`: 25 source occurrences (test-path).
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
- `tests/test_forge_contract.py`: 12 source occurrences (test-path).
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
- `tests/test_planning_contract.py`: 6 source occurrences (test-path).
- `tests/test_planning_setup.py`: 12 source occurrences (test-path).
- `tests/test_planning_watch.py`: 31 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_resource_update.py`: 18 source occurrences (test-path).
- `tests/test_review_regressions.py`: 54 source occurrences (test-path).
- `tests/test_saved_data.py`: 14 source occurrences (test-path).
- `tests/test_second_provider.py`: 8 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 24 source occurrences (test-path).
- `tests/test_ticketing.py`: 18 source occurrences (test-path).
- `tests/test_ticketing_contract.py`: 18 source occurrences (test-path).
- `tests/test_watch.py`: 63 source occurrences (test-path).
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
    class c0000["FileCleanupReceipts"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +path: unknown
        +load() set[CleanupSet]
        -_load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0001["src/forgetful_factory/adapters/filesystem/cleanup_receipts.py"] {
        <<module>>
        -_unique_object(pairs: unknown) unknown
        -_resource(value: object) CleanupSet
    }
    class c0002["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type1
        +save(configuration: FactoryConfiguration) None
    }
    class c0003["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0004["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0005["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +runtime: unknown
        +term_grace: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type2
        -_environment(extra: Type4) Type3
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type4) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0006["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +sync_fingerprint(inputs: Type5) str
        +runtime_ready(runtime: Path, inputs: Type5, probe: str, term_grace: float) bool
    }
    class c0007["ObservedTerminal"] {
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
    class c0008["PlainWatchObservation"] {
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
    class c0009["src/forgetful_factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type6
        -_read_discovery(workspace: Path) dict
        +unknown_status(source: str, observation: str) dict
        +plain_watch_status(workspace: Path) Type7
        +observe_plain_watch(workspace: Path, report_unavailable: Type9) Type8
    }
    class c0010["BorrowedForemanTerminal"] {
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
    class c0011["SessionState"] {
        <<class>>
        +session: Type10
        +worker: Type11
        +worker_error: Type2
        +cleanup_known: bool
    }
    class c0012["src/forgetful_factory/agents/adapters/agentshell/controller.py"] {
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
    class c0013["src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0014["src/forgetful_factory/agents/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0015["ForemanOwner"] {
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
    class c0016["src/forgetful_factory/agents/adapters/agentshell/owner.py"] {
        <<module>>
        -_validate_target(target: unknown) None
        -_controller_event(line: bytes) dict
        -_watcher_request(line: bytes) dict
        -_acquire_owner_lock(directory: Path, workspace: Path) int
        -_prepare_owner_startup(workspace: Path) Type12
        +main(Signature7)
        -_report_startup_error(handover: unknown, error: unknown) None
        +entrypoint() None
    }
    class c0017["src/forgetful_factory/agents/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type7
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(Signature8)
        +enter_terminal(target: dict) None
    }
    class c0018["AgentShellTerminal"] {
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
        +process: Type13
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
    class c0019["src/forgetful_factory/agents/adapters/pi/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        -_local_selection(value: object, field: str, message: str) str
        -_validate_agent(value: object) dict
        -_validate_roster(path: Path, value: object, agent_type: str) None
        -_validate_resources(value: object) None
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0020["CoordinatorProfiles"] {
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
    class c0021["src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0022["ForemanProfile"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +term_grace: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type7
        -_model_catalogs: Type14
        -_managed_memory_selected: Type15
        +prepare_setup_guidance() None
        +missing_executables(connection: ForgetfulConnection) list[str]
        +role_runtime_ready() bool
        +validate_setup(Signature11)
        +validate_bundled_resources(include_memory_extension: bool) None
        +installation(command: str) Type2
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
        +choose_pi_home(requested: Type2, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type16) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(config: FactoryConfiguration) dict
        +managed_memory_notice() Type2
        +record_completion(config: FactoryConfiguration) bool
        +begin_setup() None
        +validate_completion(_config: FactoryConfiguration) None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0023["ResourceUpdate"] {
        <<class>>
        +directory: Path
        +files: Type17
        +add: Type18
        +replace: Type18
        +edited: Type18
    }
    class c0024["src/forgetful_factory/agents/adapters/pi/role_resources.py"] {
        <<module>>
        -_digest(data: bytes) str
        +bundled_files() Type17
        +plan_update(directory: Path) ResourceUpdate
        -_back_up(update: ResourceUpdate, backups: Path) Path
        +apply_update(update: ResourceUpdate, backups: Path) Type16
    }
    class c0025["src/forgetful_factory/agents/adapters/pi/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type19) None
        -_walk_skill_directory(directory: Path, ancestors: Type20, files: Type19) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0026["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0027["AgentShellLifecycleDeadlines"] {
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
    class c0028["InitialAgentChoices"] {
        <<class>>
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +foreman_memory_enabled: bool
        +foreman_memory_model: Type2
        +feature_owner_agent_model: Type2
        +feature_owner_agent_effort: Type2
        +feature_owner_agent_harness: str
        +grill_me_skill: Type2
        +implementation_agent_model: Type2
        +implementation_agent_harness: Type2
        +implementation_agent_effort: Type2
        +review_agent_model: Type2
        +review_agent_harness: Type2
        +review_agent_effort: Type2
        +tdd_skill: Type2
        +implementation_skills: Type18
        +review_skills: Type18
        +research_agent_model: Type2
        +research_agent_harness: Type2
        +research_agent_effort: Type2
        +execution_enabled: bool
    }
    class c0029["src/forgetful_factory/agents/model.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type18
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0030["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0031["CleanupCompleted"] {
        <<class>>
        -__init__(Signature12)
        +records: unknown
        +ticketing: unknown
        +worktrees: unknown
        +owners: Type21
        +receipts: unknown
        +confirmed: set[CleanupSet]
        +cursor: Type22
        +poll(alerts: WatcherAlerts, report: unknown) None
        -_claim_indexes(Signature13)
        -_read_plans(inventory: list[dict], alerts: WatcherAlerts) Type25
        -_candidates(plans: list[dict], tasks: Type24, alerts: WatcherAlerts) Type26
        -_candidate(plan: dict, tasks: list[dict]) CompletedWork
        -_read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) None
        -_in_scope(plan: dict) bool
        -_repository_identities(alerts: WatcherAlerts) Type4
        -_keys(mapping: dict, identities: Type3) set[tuple]
        -_claims(tasks: list[dict], plan_id: int, claims: dict, identities: Type3) None
        -_task_mappings(task: dict) list[dict]
        -_validate_claim_mapping(mapping: object) None
        -_overlaps(mapping: dict, claims: dict) bool
        -_dispose(Signature14)
        -_order(work: CompletedWork, mapping: dict) tuple
        -_check_namespaces(mappings: list[dict], identities: Type3) None
        -_mapping_identity(Signature15)
        -_is_confirmed(plan_id: int, reference: str, mapping: dict, workspace: Type2) bool
        -_still_completed(work: CompletedWork) bool
    }
    class c0032["CompletedWork"] {
        <<class>>
        +plan_id: int
        +reference: str
        +task_id: int
        +mappings: list[dict]
    }
    class c0033["src/forgetful_factory/application/cleanup_completed.py"] {
        <<module>>
        -_claim_path(value: str) str
    }
    class c0034["CleanupMarkerError"] {
        <<class>>
    }
    class c0035["src/forgetful_factory/application/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict, forge: Forge, repository: RepositoryRef) Type27
    }
    class c0036["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type18
        +foreman_agent_file: str
        +repository: Type28
        +forgetful: Type29
        +execution_enabled: bool
    }
    class c0037["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type18
    }
    class c0038["FactoryRecords"] {
        <<class>>
        -__init__(Signature16)
        +planning: unknown
        +workspace: unknown
        +config: unknown
        +repositories: unknown
        +forge: unknown
        +check_repository(repository: RepositoryReference) None
        +check_source(repository: RepositoryReference) RepositoryRef
        +snapshot(context: dict, external_ref: str) Ticket
        +active(plan: dict) bool
        +context(plan: dict) dict
        +ownership(plan_id: int, external_ref: str) list[dict]
        +ownership_records(plan_id: int, external_ref: str, tasks: list[dict]) list[dict]
        +mapping_repository(mapping: dict, seen: set[str]) RepositoryReference
    }
    class c0039["InitialiseFactory"] {
        <<class>>
        -__init__(Signature17)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +forge: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type30, confirm: Type31) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type32, labels: Type33) Type1
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type34
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type35
        -_ensure_label(source: TicketSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type36, save: bool) list[str]
    }
    class c0040["CleanupReceipts"] {
        <<class>>
        +load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0041["CleanupSet"] {
        <<class>>
        +workspace: str
        +backend: str
        +plan_id: int
        +external_ref: str
        +repository: str
        +local_dir: str
        +branch: str
        +path: str
        +overlaps(other: Type37) bool
    }
    class c0042["ConfigurationStore"] {
        <<class>>
        +load() Type1
        +save(configuration: FactoryConfiguration) None
    }
    class c0043["ForemanProfile"] {
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
        +installation(command: str) Type2
        +install(command: str) None
        +choose_pi_home(requested: Type2, confirm: unknown) str
        +save_pi_choice() None
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type16) list[str]
        +managed_memory_notice() Type2
        +record_completion(config: FactoryConfiguration) bool
        +begin_setup() None
    }
    class c0044["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0045["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature18)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +records: unknown
        +check() None
        +check_repository(repository: RepositoryReference) None
        +prepare(issue: Ticket) Type7
        -_repository(source: TicketSource) RepositoryReference
        -_initial_mappings(issue: Ticket) list[dict]
        +preflight(issue: Ticket) list[dict]
        -_prepare_plan(issue: Ticket, plan: dict, initial_mappings: list[dict]) Type7
        -_setup_ownership(Signature19)
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature20)
        +lookup(issue: Ticket) Type11
        -_create_plan(issue: Ticket) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type40, task_ids: Type41) Type39
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature21)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_is_unfinished_factory_plan(summary: dict, prefixes: set[str]) bool
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_validated_mapping(Signature22)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0046["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        +worktree_name(ticket: Ticket) str
    }
    class c0047["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type11
        +issue: Type40
        +task_ids: Type41
        +recovered: bool
        +setup_paths: Type18
        +setup_cause: Type2
    }
    class c0048["WatchFactory"] {
        <<class>>
        -__init__(Signature23)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +cleanup: unknown
        +run(Signature24)
        -_watch(Signature25)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type9) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature26)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type9) Type44
        -_recover_work(Signature27)
        -_handle_recovery_repository_problem(Signature28)
        -_handle_recovery_read_problem(Signature29)
        -_remember_task_ids(work: BlockedWork, task_ids: Type41) None
        -_complete_recovery(Signature30)
        -_poll_sources(Signature31)
        -_process_source(Signature32)
        -_baseline_source(Signature33)
        -_repository_for_source(Signature34)
        -_include_pending_lookups(Signature35)
        -_process_issues(Signature36)
        -_skip_issue(issue: Ticket, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature37)
        -_handle_intake_repository_problem(Signature38)
        -_handle_intake_read_problem(Signature39)
        -_handle_intake_scaffold_problem(Signature40)
        -_complete_intake(Signature41)
        -_sole_task_id(task_ids: Type41) Type11
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature42)
        -_read_issues(source: TicketSource, labels: Type18, alerts: WatcherAlerts) Type49
    }
    class c0049["_WatchState"] {
        <<class>>
        +seen: Type3
        +baseline: Type3
        +baselined: set[TicketSource]
        +blocked: Type50
        +pending_lookup: Type47
        +known: Type50
        +recovered: set[str]
        +pending_repositories: Type34
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0050["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0051["IntakeProblem"] {
        <<class>>
    }
    class c0052["RepositoryProblem"] {
        <<class>>
    }
    class c0053["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature43)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0054["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0055["UncertainScaffold"] {
        <<class>>
    }
    class c0056["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type3
        +last_diagnostic: Type3
        +clear(subject: str) None
        +send(Signature44)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0057["src/forgetful_factory/application/watcher_problems.py"] {
        <<module>>
        -_cleanup_recovery(code: str) str
    }
    class c0058["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +select_ticketing(config: FactoryConfiguration, command_timeout: float) Ticketing
        +build_watcher(Signature45)
        +prepare_foreman_launch(Signature46)
    }
    class c0059["src/forgetful_factory/cli/definition_of_done.py"] {
        <<module>>
        +agree_definition_of_done(workspace: Path, config: FactoryConfiguration) bool
        -_deployment_agreement(answer: str) str
    }
    class c0060["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0061["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature47)
        -_check_existing_connection(Signature48)
        -_connection(Signature49)
        -_prepare_foreman(Signature50)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type52, show_choices: bool, prompt: Type2) str
        -_select_model(Signature51)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_change_managed_watch(args: argparse.Namespace, workspace: Path) int
        -_managed_watch_status(workspace: Path) Type7
        -_watch_status(workspace: Path) int
        -_watch(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_foreman(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_watch_locked(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature52)
        -_owner_choices(Signature53)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature54)
        -_foreman_memory_choices(Signature55)
        -_managed_rest_mapping_available(connection: ForgetfulConnection) bool
        -_worker_choices(Signature56)
        -_complete_setup(Signature57)
        -_initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type7) None
        -_finish_existing_setup(Signature58)
        -_discover_worker_models(Signature59)
        -_validate_initial_model(Signature60)
        -_start_initial_setup(Signature61)
        -_initialise_locked(Signature62)
        -_launch_setup_foreman(Signature63)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0062["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0063["src/forgetful_factory/cli/resource_update.py"] {
        <<module>>
        -_report(update: unknown, force: bool) None
        +update_resources(Signature64)
    }
    class c0064["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type55) FactoryConfiguration
    }
    class c0065["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0066["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: TicketSource
    }
    class c0067["GitHubForge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0068["RepositoryRef"] {
        <<class>>
        +forge: str
        +reference: str
    }
    class c0069["Forge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0070["src/forgetful_factory/planning/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0071["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +role: unknown
        +term_grace: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type3
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0072["src/forgetful_factory/planning/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature65)
        -_catalog_tools(catalog: object) dict
    }
    class c0073["ForgetfulPlanStore"] {
        <<class>>
        -__init__(Signature66)
        +cli: unknown
        +connection: unknown
        +execution_enabled: unknown
        +check() None
        -_call(tool: str, fields: unknown) dict
        -_read(tool: str, fields: unknown) dict
        +plans(external_ref: Type2) list[dict]
        -_rows(result: dict, key: str) list[dict]
        +get_plan(plan_id: int) dict
        +create_plan(fields: unknown) dict
        +owns(plan: dict) bool
        +backend_identity() str
        +update_plan(plan_id: int, fields: unknown) dict
        +tasks(plan_id: int) list[dict]
        -_task(task_id: int, plan_id: int) dict
        +create_task(fields: unknown) dict
        +update_task(task_id: int, fields: unknown) dict
    }
    class c0074["src/forgetful_factory/planning/adapters/forgetful/plan_store.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0075["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type2
        +server: Type2
        +project_id: Type11
        +validate() None
        -_validate_server() None
    }
    class c0076["src/forgetful_factory/planning/model.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type29
    }
    class c0077["PlanStore"] {
        <<class>>
        +check() None
        +plans(external_ref: Type2) list[dict]
        +get_plan(plan_id: int) dict
        +create_plan(fields: unknown) dict
        +update_plan(plan_id: int, fields: unknown) dict
        +tasks(plan_id: int) list[dict]
        +create_task(fields: unknown) dict
        +update_task(task_id: int, fields: unknown) dict
        +owns(plan: dict) bool
        +backend_identity() str
    }
    class c0078["PlanningReadError"] {
        <<class>>
    }
    class c0079["src/forgetful_factory/shared/command.py"] {
        <<module>>
        +run_command(arguments: list[str], timeout: float, env: Type4, stdin: Type11) str
    }
    class c0080["FactoryError"] {
        <<class>>
    }
    class c0081["src/forgetful_factory/shared/executables.py"] {
        <<module>>
        +executable_path(workspace: Path) str
    }
    class c0082["src/forgetful_factory/shared/resource_files.py"] {
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
    class c0083["src/forgetful_factory/shared/resources.py"] {
        <<module>>
        +resource_root() Path
    }
    class c0084["src/forgetful_factory/shared/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen, term_grace: float) None
        +run_owned(Signature67)
    }
    class c0085["src/forgetful_factory/shared/validation.py"] {
        <<module>>
        +nonblank(value: object, field: str) str
        +positive_duration(name: str, value: object) None
    }
    class c0086["WatchStop"] {
        <<class>>
        +requested: bool
        +interrupt(_signum: unknown, _frame: unknown) None
    }
    class c0087["src/forgetful_factory/shared/watch_stop.py"] {
        <<module>>
        +watch_stop_scope() unknown
        +check_watch_stop() None
    }
    class c0088["GitHubTicketing"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        -_api(source: TicketSource, suffix: str, #42;arguments: str) object
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type57
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type18) Type46
        -_ticket(source: TicketSource, item: dict) Ticket
        -_comments(source: TicketSource, number: int) Type58
        -_milestone(item: object) object
        -_validate_issue(source: TicketSource, item: dict) None
    }
    class c0089["Label"] {
        <<class>>
        +name: str
    }
    class c0090["Ticket"] {
        <<class>>
        +source: TicketSource
        +key: str
        +title: str
        +url: str
        +body: str
        +revision: str
        +epic: bool
        +id: str
    }
    class c0091["TicketSource"] {
        <<class>>
        +provider: str
        +reference: str
        +id_prefix: str
    }
    class c0092["Ticketing"] {
        <<class>>
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type57
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type18) Type46
    }
    class c0093["GitRepositories"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0094["src/forgetful_factory/workspace/adapters/git/repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0095["GitWorktrees"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +cleanup_defaults: Type59
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        -_read_git(arguments: list[str]) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type60
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type61
        -_validate_registered_worktree(Signature68)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
        -_disposal_state(Signature69)
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
    class c0096["src/forgetful_factory/workspace/adapters/git/worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0097["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0098["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type2) unknown
        +code: unknown
        +paths: unknown
    }
    class c0099["WorktreeReadError"] {
        <<class>>
    }
    class c0100["Worktrees"] {
        <<class>>
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
    }
    c0000 ..> c0000 : 2 relationships (see list)
    c0000 ..> c0001 : _load() calls _resource()
    c0000 ..> c0007 : _load() calls close()
    c0000 ..> c0041 : 3 relationships (see list)
    c0000 ..> c0080 : 2 relationships (see list)
    c0000 ..> c0082 : 2 relationships (see list)
    c0000 ..> c0087 : confirm() calls check_watch_stop()
    c0001 ..> c0041 : 2 relationships (see list)
    c0002 ..> c0000 : load() calls load()
    c0002 ..> c0003 : save() calls quote()
    c0002 ..> c0007 : 2 relationships (see list)
    c0002 ..> c0036 : 2 relationships (see list)
    c0002 ..> c0037 : load() calls from_mapping()
    c0002 ..> c0080 : 2 relationships (see list)
    c0004 ..> c0004 : hold() calls _hold_directory()
    c0004 ..> c0007 : _hold_directory() calls close()
    c0004 ..> c0080 : _hold_directory() constructs FactoryError
    c0005 ..> c0005 : 15 relationships (see list)
    c0005 ..> c0006 : 3 relationships (see list)
    c0005 ..> c0080 : 6 relationships (see list)
    c0005 ..> c0082 : install() calls write_new()
    c0005 ..> c0084 : 4 relationships (see list)
    c0006 ..> c0006 : runtime_ready() calls sync_fingerprint()
    c0006 ..> c0084 : runtime_ready() calls run_owned()
    c0007 ..> c0008 : 3 relationships (see list)
    c0007 ..> c0009 : __init__() calls unknown_status()
    c0007 ..> c0010 : 5 relationships (see list)
    c0007 ..> c0030 : type in __init__
    c0008 ..> c0007 : 2 relationships (see list)
    c0008 ..> c0008 : 9 relationships (see list)
    c0008 ..> c0009 : 6 relationships (see list)
    c0008 ..> c0080 : __enter__() constructs FactoryError
    c0008 ..> c0082 : 3 relationships (see list)
    c0009 ..> c0008 : 4 relationships (see list)
    c0009 ..> c0009 : 8 relationships (see list)
    c0009 ..> c0082 : _read_discovery() calls check_real_path()
    c0010 ..> c0007 : close() calls close()
    c0010 ..> c0010 : 2 relationships (see list)
    c0010 ..> c0080 : 2 relationships (see list)
    c0010 ..> c0087 : 2 relationships (see list)
    c0012 ..> c0007 : 6 relationships (see list)
    c0012 ..> c0011 : serve() constructs SessionState
    c0012 ..> c0012 : 17 relationships (see list)
    c0012 ..> c0073 : 4 relationships (see list)
    c0013 ..> c0080 : runtime_directory() constructs FactoryError
    c0013 ..> c0082 : runtime_directory() calls check_real_path()
    c0014 ..> c0022 : main() calls list_models()
    c0015 ..> c0003 : _apply_controller_problem() calls quote()
    c0015 ..> c0007 : 11 relationships (see list)
    c0015 ..> c0015 : 27 relationships (see list)
    c0015 ..> c0016 : 2 relationships (see list)
    c0015 ..> c0027 : 2 relationships (see list)
    c0015 ..> c0073 : 2 relationships (see list)
    c0015 ..> c0080 : 10 relationships (see list)
    c0015 ..> c0082 : save() calls replace_generated_json()
    c0016 ..> c0003 : _acquire_owner_lock() calls quote()
    c0016 ..> c0007 : 3 relationships (see list)
    c0016 ..> c0013 : _prepare_owner_startup() calls runtime_directory()
    c0016 ..> c0015 : 3 relationships (see list)
    c0016 ..> c0016 : 5 relationships (see list)
    c0016 ..> c0017 : _prepare_owner_startup() calls read_state()
    c0016 ..> c0073 : main() calls create_task()
    c0016 ..> c0080 : 3 relationships (see list)
    c0017 ..> c0003 : request() calls quote()
    c0017 ..> c0007 : 2 relationships (see list)
    c0017 ..> c0013 : 3 relationships (see list)
    c0017 ..> c0015 : 2 relationships (see list)
    c0017 ..> c0017 : 3 relationships (see list)
    c0017 ..> c0027 : 2 relationships (see list)
    c0017 ..> c0080 : 5 relationships (see list)
    c0017 ..> c0082 : read_state() calls read_generated_json()
    c0018 ..> c0007 : close() calls close()
    c0018 ..> c0018 : 5 relationships (see list)
    c0018 ..> c0027 : 2 relationships (see list)
    c0018 ..> c0080 : 4 relationships (see list)
    c0018 ..> c0087 : 3 relationships (see list)
    c0019 ..> c0019 : 8 relationships (see list)
    c0019 ..> c0080 : 2 relationships (see list)
    c0019 ..> c0085 : 4 relationships (see list)
    c0020 ..> c0020 : 3 relationships (see list)
    c0020 ..> c0021 : prepare() calls selected_resources()
    c0020 ..> c0022 : prepare() calls prepare()
    c0020 ..> c0026 : __init__() constructs WorkerProfiles
    c0020 ..> c0036 : 2 relationships (see list)
    c0020 ..> c0080 : 4 relationships (see list)
    c0020 ..> c0082 : 5 relationships (see list)
    c0022 ..> c0000 : choose_pi_home() calls confirm()
    c0022 ..> c0003 : require_pi_home() calls quote()
    c0022 ..> c0005 : 6 relationships (see list)
    c0022 ..> c0006 : 2 relationships (see list)
    c0022 ..> c0019 : selected_launch() calls foreman_launch()
    c0022 ..> c0020 : 4 relationships (see list)
    c0022 ..> c0022 : 23 relationships (see list)
    c0022 ..> c0024 : _install_resources() calls bundled_files()
    c0022 ..> c0025 : selected_launch() calls selected_skill_files()
    c0022 ..> c0036 : 4 relationships (see list)
    c0022 ..> c0043 : 5 relationships (see list)
    c0022 ..> c0071 : 4 relationships (see list)
    c0022 ..> c0072 : list_models() calls role_environment()
    c0022 ..> c0075 : 9 relationships (see list)
    c0022 ..> c0080 : 14 relationships (see list)
    c0022 ..> c0081 : 2 relationships (see list)
    c0022 ..> c0082 : 11 relationships (see list)
    c0022 ..> c0084 : list_models() calls run_owned()
    c0024 ..> c0023 : 4 relationships (see list)
    c0024 ..> c0024 : 4 relationships (see list)
    c0024 ..> c0080 : 2 relationships (see list)
    c0024 ..> c0082 : plan_update() calls check_real_path()
    c0025 ..> c0007 : _add_skill_file() calls close()
    c0025 ..> c0025 : 3 relationships (see list)
    c0025 ..> c0080 : 3 relationships (see list)
    c0026 ..> c0008 : prepare() calls update()
    c0026 ..> c0028 : type in prepare
    c0026 ..> c0082 : 3 relationships (see list)
    c0027 ..> c0085 : __post_init__() calls positive_duration()
    c0029 ..> c0028 : 3 relationships (see list)
    c0029 ..> c0029 : 4 relationships (see list)
    c0029 ..> c0080 : 5 relationships (see list)
    c0029 ..> c0085 : 4 relationships (see list)
    c0031 ..> c0000 : 2 relationships (see list)
    c0031 ..> c0007 : 5 relationships (see list)
    c0031 ..> c0008 : 4 relationships (see list)
    c0031 ..> c0031 : 27 relationships (see list)
    c0031 ..> c0032 : 6 relationships (see list)
    c0031 ..> c0033 : 6 relationships (see list)
    c0031 ..> c0038 : 9 relationships (see list)
    c0031 ..> c0040 : type in __init__
    c0031 --> c0041 : field confirmed
    c0031 ..> c0041 : 3 relationships (see list)
    c0031 ..> c0053 : 7 relationships (see list)
    c0031 ..> c0056 : 10 relationships (see list)
    c0031 ..> c0073 : 7 relationships (see list)
    c0031 ..> c0080 : type in _read_problem
    c0031 ..> c0088 : _in_scope() calls is_key()
    c0031 ..> c0092 : type in __init__
    c0031 ..> c0095 : 4 relationships (see list)
    c0031 ..> c0100 : type in __init__
    c0035 ..> c0034 : validate_cleanup_marker() constructs CleanupMarkerError
    c0035 ..> c0067 : validate_cleanup_marker() calls is_change_request()
    c0035 ..> c0068 : type in validate_cleanup_marker
    c0035 ..> c0069 : type in validate_cleanup_marker
    c0036 --> c0066 : field repository
    c0036 --> c0075 : field forgetful
    c0037 ..> c0036 : 3 relationships (see list)
    c0037 ..> c0037 : from_mapping() calls validate()
    c0037 ..> c0066 : from_mapping() constructs RepositoryReference
    c0037 ..> c0075 : validate() calls validate()
    c0037 ..> c0076 : from_mapping() calls connection_from_mapping()
    c0037 ..> c0080 : 2 relationships (see list)
    c0037 ..> c0085 : 2 relationships (see list)
    c0037 ..> c0091 : from_mapping() constructs TicketSource
    c0038 ..> c0036 : type in __init__
    c0038 ..> c0038 : 2 relationships (see list)
    c0038 ..> c0052 : 2 relationships (see list)
    c0038 ..> c0053 : 5 relationships (see list)
    c0038 ..> c0066 : 3 relationships (see list)
    c0038 ..> c0067 : check_source() calls repository()
    c0038 ..> c0068 : type in check_source
    c0038 ..> c0069 : type in __init__
    c0038 ..> c0073 : ownership() calls tasks()
    c0038 ..> c0077 : type in __init__
    c0038 ..> c0090 : 2 relationships (see list)
    c0038 ..> c0091 : snapshot() constructs TicketSource
    c0038 ..> c0093 : check_repository() calls origin()
    c0038 ..> c0097 : type in __init__
    c0039 ..> c0000 : 2 relationships (see list)
    c0039 ..> c0002 : initialise() calls save()
    c0039 ..> c0005 : prepare_foreman() calls install()
    c0039 ..> c0020 : prepare_foreman() calls prepare()
    c0039 ..> c0022 : 4 relationships (see list)
    c0039 ..> c0036 : 6 relationships (see list)
    c0039 ..> c0037 : 3 relationships (see list)
    c0039 ..> c0039 : 3 relationships (see list)
    c0039 ..> c0042 : type in __init__
    c0039 ..> c0043 : type in __init__
    c0039 ..> c0066 : 2 relationships (see list)
    c0039 ..> c0067 : 2 relationships (see list)
    c0039 ..> c0069 : type in __init__
    c0039 ..> c0075 : type in prepare_foreman
    c0039 ..> c0080 : 5 relationships (see list)
    c0039 ..> c0088 : 4 relationships (see list)
    c0039 ..> c0089 : 2 relationships (see list)
    c0039 ..> c0091 : 3 relationships (see list)
    c0039 ..> c0092 : type in __init__
    c0039 ..> c0093 : 3 relationships (see list)
    c0039 ..> c0097 : type in __init__
    c0040 ..> c0041 : 2 relationships (see list)
    c0042 ..> c0036 : 2 relationships (see list)
    c0043 ..> c0028 : type in prepare_roles
    c0043 ..> c0036 : 3 relationships (see list)
    c0043 ..> c0075 : 8 relationships (see list)
    c0045 ..> c0008 : recover() calls snapshot()
    c0045 ..> c0022 : check() calls check()
    c0045 ..> c0035 : _ensure_mapping() calls validate_cleanup_marker()
    c0045 ..> c0036 : type in __init__
    c0045 ..> c0038 : 11 relationships (see list)
    c0045 ..> c0039 : preflight() calls inspect()
    c0045 ..> c0045 : 22 relationships (see list)
    c0045 ..> c0046 : _initial_mappings() calls worktree_name()
    c0045 ..> c0051 : preflight() constructs IntakeProblem
    c0045 ..> c0053 : 8 relationships (see list)
    c0045 ..> c0054 : 5 relationships (see list)
    c0045 ..> c0055 : 5 relationships (see list)
    c0045 ..> c0066 : 3 relationships (see list)
    c0045 ..> c0069 : type in __init__
    c0045 ..> c0073 : 12 relationships (see list)
    c0045 ..> c0077 : type in __init__
    c0045 ..> c0080 : _is_unfinished_factory_plan() constructs FactoryError
    c0045 ..> c0090 : 8 relationships (see list)
    c0045 ..> c0091 : type in _repository
    c0045 ..> c0095 : 3 relationships (see list)
    c0045 ..> c0097 : type in __init__
    c0045 ..> c0100 : type in __init__
    c0046 ..> c0090 : type in worktree_name
    c0047 --> c0090 : field issue
    c0048 ..> c0007 : 15 relationships (see list)
    c0048 ..> c0020 : _process_issue() calls prepare()
    c0048 ..> c0022 : _check_planning_access() calls check()
    c0048 ..> c0030 : type in __init__
    c0048 ..> c0031 : 2 relationships (see list)
    c0048 ..> c0036 : 4 relationships (see list)
    c0048 ..> c0038 : _check_pending_repositories() calls check_repository()
    c0048 ..> c0045 : 5 relationships (see list)
    c0048 ..> c0047 : 13 relationships (see list)
    c0048 ..> c0048 : 35 relationships (see list)
    c0048 ..> c0049 : 19 relationships (see list)
    c0048 ..> c0050 : 2 relationships (see list)
    c0048 ..> c0052 : 2 relationships (see list)
    c0048 ..> c0053 : 3 relationships (see list)
    c0048 ..> c0054 : 2 relationships (see list)
    c0048 ..> c0056 : 28 relationships (see list)
    c0048 ..> c0066 : 5 relationships (see list)
    c0048 ..> c0080 : _read_issues() constructs FactoryError
    c0048 ..> c0087 : 3 relationships (see list)
    c0048 ..> c0088 : _read_issues() calls list_open()
    c0048 ..> c0090 : 13 relationships (see list)
    c0048 ..> c0091 : 7 relationships (see list)
    c0048 ..> c0092 : type in __init__
    c0049 --> c0047 : 2 relationships (see list)
    c0049 --> c0066 : field pending_repositories
    c0049 --> c0090 : field pending_lookup
    c0049 --> c0091 : field baselined
    c0051 --|> c0053 : inherits
    c0052 --|> c0053 : inherits
    c0053 --|> c0080 : inherits
    c0054 --|> c0053 : inherits
    c0055 --|> c0053 : inherits
    c0056 ..> c0000 : __init__() calls __init__()
    c0056 ..> c0007 : send() calls send()
    c0056 ..> c0057 : send() calls _cleanup_recovery()
    c0056 ..> c0080 : type in send
    c0058 ..> c0000 : build_watcher() constructs FileCleanupReceipts
    c0058 ..> c0002 : build_initialiser() constructs TomlConfigurationStore
    c0058 ..> c0007 : build_watcher() constructs ObservedTerminal
    c0058 ..> c0018 : build_watcher() constructs AgentShellTerminal
    c0058 ..> c0022 : 6 relationships (see list)
    c0058 ..> c0031 : build_watcher() constructs CleanupCompleted
    c0058 ..> c0036 : 3 relationships (see list)
    c0058 ..> c0039 : 2 relationships (see list)
    c0058 ..> c0045 : build_watcher() constructs ScaffoldIssue
    c0058 ..> c0048 : 2 relationships (see list)
    c0058 ..> c0058 : 2 relationships (see list)
    c0058 ..> c0065 : 4 relationships (see list)
    c0058 ..> c0067 : 2 relationships (see list)
    c0058 ..> c0072 : prepare_foreman_launch() calls role_environment()
    c0058 ..> c0073 : build_watcher() constructs ForgetfulPlanStore
    c0058 ..> c0080 : 3 relationships (see list)
    c0058 ..> c0088 : 3 relationships (see list)
    c0058 ..> c0092 : type in select_ticketing
    c0058 ..> c0093 : 2 relationships (see list)
    c0058 ..> c0095 : build_watcher() constructs GitWorktrees
    c0059 ..> c0036 : type in agree_definition_of_done
    c0059 ..> c0059 : agree_definition_of_done() calls _deployment_agreement()
    c0059 ..> c0080 : 2 relationships (see list)
    c0059 ..> c0082 : 2 relationships (see list)
    c0060 --> c0036 : field config
    c0060 --> c0075 : field connection
    c0061 ..> c0000 : _initialise_locked() calls load()
    c0061 ..> c0003 : 6 relationships (see list)
    c0061 ..> c0004 : 6 relationships (see list)
    c0061 ..> c0008 : _prompt_workers() calls update()
    c0061 ..> c0009 : 4 relationships (see list)
    c0061 ..> c0010 : _watch_locked() constructs BorrowedForemanTerminal
    c0061 ..> c0015 : _watch_locked() calls run()
    c0061 ..> c0017 : 14 relationships (see list)
    c0061 ..> c0022 : 17 relationships (see list)
    c0061 ..> c0028 : 7 relationships (see list)
    c0061 ..> c0029 : _start_initial_setup() calls validate_initial_agents()
    c0061 ..> c0036 : 4 relationships (see list)
    c0061 ..> c0037 : _connection() calls validate()
    c0061 ..> c0039 : 17 relationships (see list)
    c0061 ..> c0058 : 4 relationships (see list)
    c0061 ..> c0059 : 2 relationships (see list)
    c0061 ..> c0060 : 3 relationships (see list)
    c0061 ..> c0061 : 55 relationships (see list)
    c0061 ..> c0062 : _select_numbered() calls parse_numbered_selection()
    c0061 ..> c0063 : main() calls update_resources()
    c0061 ..> c0064 : 3 relationships (see list)
    c0061 ..> c0065 : 9 relationships (see list)
    c0061 ..> c0075 : 7 relationships (see list)
    c0061 ..> c0080 : 20 relationships (see list)
    c0061 ..> c0082 : _discover_worker_models() calls check_real_path()
    c0061 ..> c0087 : _watch_locked() calls watch_stop_scope()
    c0062 ..> c0080 : parse_numbered_selection() constructs FactoryError
    c0063 ..> c0004 : 2 relationships (see list)
    c0063 ..> c0005 : update_resources() calls install()
    c0063 ..> c0017 : update_resources() calls read_state()
    c0063 ..> c0022 : 3 relationships (see list)
    c0063 ..> c0024 : 2 relationships (see list)
    c0063 ..> c0063 : update_resources() calls _report()
    c0063 ..> c0065 : type in update_resources
    c0063 ..> c0080 : 2 relationships (see list)
    c0064 ..> c0000 : load_configuration() calls load()
    c0064 ..> c0002 : load_configuration() constructs TomlConfigurationStore
    c0064 ..> c0036 : type in load_configuration
    c0064 ..> c0080 : load_configuration() constructs FactoryError
    c0065 --> c0027 : field agentshell
    c0065 ..> c0085 : __post_init__() calls positive_duration()
    c0066 --> c0091 : field work_source
    c0067 ..> c0068 : 3 relationships (see list)
    c0067 ..> c0080 : repository() constructs FactoryError
    c0069 ..> c0068 : 2 relationships (see list)
    c0070 ..> c0017 : uses_browser_login() calls request()
    c0070 ..> c0075 : type in uses_browser_login
    c0071 ..> c0071 : 7 relationships (see list)
    c0071 ..> c0072 : 2 relationships (see list)
    c0071 ..> c0075 : 7 relationships (see list)
    c0071 ..> c0080 : 5 relationships (see list)
    c0071 ..> c0084 : 2 relationships (see list)
    c0071 ..> c0087 : command() calls check_watch_stop()
    c0072 ..> c0008 : role_environment() calls update()
    c0072 ..> c0075 : type in role_environment
    c0072 ..> c0081 : role_environment() calls executable_path()
    c0073 ..> c0022 : check() calls check()
    c0073 ..> c0071 : 2 relationships (see list)
    c0073 ..> c0073 : 12 relationships (see list)
    c0073 ..> c0074 : 3 relationships (see list)
    c0073 ..> c0075 : type in __init__
    c0073 ..> c0078 : 4 relationships (see list)
    c0075 ..> c0075 : validate() calls _validate_server()
    c0075 ..> c0076 : _validate_server() calls loopback_host()
    c0075 ..> c0080 : 2 relationships (see list)
    c0075 ..> c0085 : 2 relationships (see list)
    c0076 ..> c0075 : 3 relationships (see list)
    c0076 ..> c0080 : connection_from_mapping() constructs FactoryError
    c0078 --|> c0080 : inherits
    c0079 ..> c0015 : run_command() calls run()
    c0079 ..> c0080 : run_command() constructs FactoryError
    c0079 ..> c0087 : run_command() calls check_watch_stop()
    c0082 ..> c0000 : read_generated_json() calls load()
    c0082 ..> c0007 : 2 relationships (see list)
    c0082 ..> c0080 : 6 relationships (see list)
    c0082 ..> c0082 : 9 relationships (see list)
    c0084 ..> c0007 : 2 relationships (see list)
    c0084 ..> c0080 : run_owned() constructs FactoryError
    c0084 ..> c0084 : 2 relationships (see list)
    c0084 ..> c0087 : run_owned() calls check_watch_stop()
    c0085 ..> c0080 : nonblank() constructs FactoryError
    c0087 ..> c0086 : watch_stop_scope() constructs WatchStop
    c0088 ..> c0079 : 2 relationships (see list)
    c0088 ..> c0080 : 9 relationships (see list)
    c0088 ..> c0088 : 9 relationships (see list)
    c0088 ..> c0089 : 3 relationships (see list)
    c0088 ..> c0090 : 3 relationships (see list)
    c0088 ..> c0091 : 9 relationships (see list)
    c0090 --> c0091 : field source
    c0092 ..> c0089 : 2 relationships (see list)
    c0092 ..> c0090 : type in list_open
    c0092 ..> c0091 : 5 relationships (see list)
    c0093 ..> c0079 : origin() calls run_command()
    c0093 ..> c0080 : origin() constructs FactoryError
    c0093 ..> c0094 : origin() calls _resolve_repository()
    c0094 ..> c0080 : _resolve_repository() constructs FactoryError
    c0095 ..> c0003 : _network_git() calls quote()
    c0095 ..> c0056 : begin_cleanup_cycle() calls clear()
    c0095 ..> c0079 : 4 relationships (see list)
    c0095 --> c0080 : field cleanup_defaults
    c0095 ..> c0080 : ensure() constructs FactoryError
    c0095 ..> c0087 : ensure() calls check_watch_stop()
    c0095 ..> c0095 : 35 relationships (see list)
    c0095 ..> c0096 : _repository_entries() calls _worktree_entries()
    c0095 ..> c0098 : 14 relationships (see list)
    c0095 ..> c0099 : 6 relationships (see list)
    c0098 ..> c0000 : __init__() calls __init__()
    c0098 --|> c0080 : inherits
    c0099 --|> c0080 : inherits
```

## Source index

- c0000: `FileCleanupReceipts` — `src/forgetful_factory/adapters/filesystem/cleanup_receipts.py`:40
- c0001: `src/forgetful_factory/adapters/filesystem/cleanup_receipts.py` —
  `src/forgetful_factory/adapters/filesystem/cleanup_receipts.py`:1
- c0002: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:17
- c0003: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0004: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0005: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:48
- c0006: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0007: `ObservedTerminal` — `src/forgetful_factory/adapters/watch_status.py`:252
- c0008: `PlainWatchObservation` — `src/forgetful_factory/adapters/watch_status.py`:129
- c0009: `src/forgetful_factory/adapters/watch_status.py` —
  `src/forgetful_factory/adapters/watch_status.py`:1
- c0010: `BorrowedForemanTerminal` —
  `src/forgetful_factory/agents/adapters/agentshell/borrowed_terminal.py`:10
- c0011: `SessionState` — `src/forgetful_factory/agents/adapters/agentshell/controller.py`:140
- c0012: `src/forgetful_factory/agents/adapters/agentshell/controller.py` —
  `src/forgetful_factory/agents/adapters/agentshell/controller.py`:1
- c0013: `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py` —
  `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py`:1
- c0014: `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py`:1
- c0015: `ForemanOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner.py`:104
- c0016: `src/forgetful_factory/agents/adapters/agentshell/owner.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner.py`:1
- c0017: `src/forgetful_factory/agents/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:1
- c0018: `AgentShellTerminal` — `src/forgetful_factory/agents/adapters/agentshell/terminal.py`:15
- c0019: `src/forgetful_factory/agents/adapters/pi/agent_definitions.py` —
  `src/forgetful_factory/agents/adapters/pi/agent_definitions.py`:1
- c0020: `CoordinatorProfiles` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:30
- c0021: `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:1
- c0022: `ForemanProfile` — `src/forgetful_factory/agents/adapters/pi/foreman_profile.py`:53
- c0023: `ResourceUpdate` — `src/forgetful_factory/agents/adapters/pi/role_resources.py`:39
- c0024: `src/forgetful_factory/agents/adapters/pi/role_resources.py` —
  `src/forgetful_factory/agents/adapters/pi/role_resources.py`:1
- c0025: `src/forgetful_factory/agents/adapters/pi/selected_skills.py` —
  `src/forgetful_factory/agents/adapters/pi/selected_skills.py`:1
- c0026: `WorkerProfiles` — `src/forgetful_factory/agents/adapters/pi/worker_profiles.py`:16
- c0027: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/agents/model.py`:131
- c0028: `InitialAgentChoices` — `src/forgetful_factory/agents/model.py`:9
- c0029: `src/forgetful_factory/agents/model.py` — `src/forgetful_factory/agents/model.py`:1
- c0030: `ForemanTerminal` — `src/forgetful_factory/agents/ports.py`:4
- c0031: `CleanupCompleted` — `src/forgetful_factory/application/cleanup_completed.py`:37
- c0032: `CompletedWork` — `src/forgetful_factory/application/cleanup_completed.py`:22
- c0033: `src/forgetful_factory/application/cleanup_completed.py` —
  `src/forgetful_factory/application/cleanup_completed.py`:1
- c0034: `CleanupMarkerError` — `src/forgetful_factory/application/cleanup_marker.py`:11
- c0035: `src/forgetful_factory/application/cleanup_marker.py` —
  `src/forgetful_factory/application/cleanup_marker.py`:1
- c0036: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:11
- c0037: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0038: `FactoryRecords` — `src/forgetful_factory/application/factory_records.py`:16
- c0039: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:20
- c0040: `CleanupReceipts` — `src/forgetful_factory/application/ports/cleanup_receipts.py`:24
- c0041: `CleanupSet` — `src/forgetful_factory/application/ports/cleanup_receipts.py`:7
- c0042: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0043: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:9
- c0044: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0045: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:37
- c0046: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0047: `BlockedWork` — `src/forgetful_factory/application/watch_factory.py`:27
- c0048: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:59
- c0049: `_WatchState` — `src/forgetful_factory/application/watch_factory.py`:38
- c0050: `_WorkAction` — `src/forgetful_factory/application/watch_factory.py`:52
- c0051: `IntakeProblem` — `src/forgetful_factory/application/watcher_problems.py`:143
- c0052: `RepositoryProblem` — `src/forgetful_factory/application/watcher_problems.py`:139
- c0053: `ScaffoldProblem` — `src/forgetful_factory/application/watcher_problems.py`:119
- c0054: `ScaffoldReadProblem` — `src/forgetful_factory/application/watcher_problems.py`:135
- c0055: `UncertainScaffold` — `src/forgetful_factory/application/watcher_problems.py`:147
- c0056: `WatcherAlerts` — `src/forgetful_factory/application/watcher_problems.py`:151
- c0057: `src/forgetful_factory/application/watcher_problems.py` —
  `src/forgetful_factory/application/watcher_problems.py`:1
- c0058: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0059: `src/forgetful_factory/cli/definition_of_done.py` —
  `src/forgetful_factory/cli/definition_of_done.py`:1
- c0060: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:749
- c0061: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0062: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0063: `src/forgetful_factory/cli/resource_update.py` —
  `src/forgetful_factory/cli/resource_update.py`:1
- c0064: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0065: `DeadlinePolicy` — `src/forgetful_factory/deadlines.py`:9
- c0066: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:7
- c0067: `GitHubForge` — `src/forgetful_factory/forge/adapters/github.py`:8
- c0068: `RepositoryRef` — `src/forgetful_factory/forge/model.py`:6
- c0069: `Forge` — `src/forgetful_factory/forge/ports.py`:6
- c0070: `src/forgetful_factory/planning/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/planning/adapters/forgetful/authentication.py`:1
- c0071: `AgentForgetfulConnection` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:55
- c0072: `src/forgetful_factory/planning/adapters/forgetful/connection.py` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:1
- c0073: `ForgetfulPlanStore` — `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:13
- c0074: `src/forgetful_factory/planning/adapters/forgetful/plan_store.py` —
  `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:1
- c0075: `ForgetfulConnection` — `src/forgetful_factory/planning/model.py`:13
- c0076: `src/forgetful_factory/planning/model.py` — `src/forgetful_factory/planning/model.py`:1
- c0077: `PlanStore` — `src/forgetful_factory/planning/ports.py`:10
- c0078: `PlanningReadError` — `src/forgetful_factory/planning/ports.py`:6
- c0079: `src/forgetful_factory/shared/command.py` — `src/forgetful_factory/shared/command.py`:1
- c0080: `FactoryError` — `src/forgetful_factory/shared/errors.py`:1
- c0081: `src/forgetful_factory/shared/executables.py` —
  `src/forgetful_factory/shared/executables.py`:1
- c0082: `src/forgetful_factory/shared/resource_files.py` —
  `src/forgetful_factory/shared/resource_files.py`:1
- c0083: `src/forgetful_factory/shared/resources.py` — `src/forgetful_factory/shared/resources.py`:1
- c0084: `src/forgetful_factory/shared/sensitive_command.py` —
  `src/forgetful_factory/shared/sensitive_command.py`:1
- c0085: `src/forgetful_factory/shared/validation.py` —
  `src/forgetful_factory/shared/validation.py`:1
- c0086: `WatchStop` — `src/forgetful_factory/shared/watch_stop.py`:8
- c0087: `src/forgetful_factory/shared/watch_stop.py` —
  `src/forgetful_factory/shared/watch_stop.py`:1
- c0088: `GitHubTicketing` — `src/forgetful_factory/ticketing/adapters/github.py`:14
- c0089: `Label` — `src/forgetful_factory/ticketing/model.py`:17
- c0090: `Ticket` — `src/forgetful_factory/ticketing/model.py`:22
- c0091: `TicketSource` — `src/forgetful_factory/ticketing/model.py`:6
- c0092: `Ticketing` — `src/forgetful_factory/ticketing/ports.py`:6
- c0093: `GitRepositories` — `src/forgetful_factory/workspace/adapters/git/repositories.py`:15
- c0094: `src/forgetful_factory/workspace/adapters/git/repositories.py` —
  `src/forgetful_factory/workspace/adapters/git/repositories.py`:1
- c0095: `GitWorktrees` — `src/forgetful_factory/workspace/adapters/git/worktrees.py`:33
- c0096: `src/forgetful_factory/workspace/adapters/git/worktrees.py` —
  `src/forgetful_factory/workspace/adapters/git/worktrees.py`:1
- c0097: `LocalRepositories` — `src/forgetful_factory/workspace/ports.py`:8
- c0098: `WorktreeProblem` — `src/forgetful_factory/workspace/ports.py`:18
- c0099: `WorktreeReadError` — `src/forgetful_factory/workspace/ports.py`:14
- c0100: `Worktrees` — `src/forgetful_factory/workspace/ports.py`:27

## Relationships

- c0000 ..> c0000: `confirm() calls load()`
- c0000 ..> c0000: `load() calls _load()`
- c0000 ..> c0001: `_load() calls _resource()`
- c0000 ..> c0007: `_load() calls close()`
- c0000 ..> c0041: `type in _load`
- c0000 ..> c0041: `type in confirm`
- c0000 ..> c0041: `type in load`
- c0000 ..> c0080: `confirm() constructs FactoryError`
- c0000 ..> c0080: `load() constructs FactoryError`
- c0000 ..> c0082: `_load() calls check_real_path()`
- c0000 ..> c0082: `confirm() calls replace_generated_json()`
- c0000 ..> c0087: `confirm() calls check_watch_stop()`
- c0001 ..> c0041: `_resource() constructs CleanupSet`
- c0001 ..> c0041: `type in _resource`
- c0002 ..> c0000: `load() calls load()`
- c0002 ..> c0003: `save() calls quote()`
- c0002 ..> c0007: `load() calls close()`
- c0002 ..> c0007: `save() calls close()`
- c0002 ..> c0036: `type in load`
- c0002 ..> c0036: `type in save`
- c0002 ..> c0037: `load() calls from_mapping()`
- c0002 ..> c0080: `load() constructs FactoryError`
- c0002 ..> c0080: `save() constructs FactoryError`
- c0004 ..> c0004: `hold() calls _hold_directory()`
- c0004 ..> c0007: `_hold_directory() calls close()`
- c0004 ..> c0080: `_hold_directory() constructs FactoryError`
- c0005 ..> c0005: `_check_uv() calls _environment()`
- c0005 ..> c0005: `_forgetful_python() calls _check_uv()`
- c0005 ..> c0005: `_forgetful_python() calls _environment()`
- c0005 ..> c0005: `_install_role_runtime() calls _check_uv()`
- c0005 ..> c0005: `_install_role_runtime() calls _run()`
- c0005 ..> c0005: `_install_tmux() calls _run()`
- c0005 ..> c0005: `_run() calls _environment()`
- c0005 ..> c0005: `description() calls _forgetful_python()`
- c0005 ..> c0005: `description() calls _ubuntu_tmux()`
- c0005 ..> c0005: `install() calls _forgetful_python()`
- c0005 ..> c0005: `install() calls _install_role_runtime()`
- c0005 ..> c0005: `install() calls _install_tmux()`
- c0005 ..> c0005: `install() calls _run()`
- c0005 ..> c0005: `install() calls _ubuntu_tmux()`
- c0005 ..> c0005: `pi_ready() calls _environment()`
- c0005 ..> c0006: `_install_role_runtime() calls sync_fingerprint()`
- c0005 ..> c0006: `install() calls sync_fingerprint()`
- c0005 ..> c0006: `pi_ready() calls sync_fingerprint()`
- c0005 ..> c0080: `_check_uv() constructs FactoryError`
- c0005 ..> c0080: `_forgetful_python() constructs FactoryError`
- c0005 ..> c0080: `_install_role_runtime() constructs FactoryError`
- c0005 ..> c0080: `_install_tmux() constructs FactoryError`
- c0005 ..> c0080: `_run() constructs FactoryError`
- c0005 ..> c0080: `install() constructs FactoryError`
- c0005 ..> c0082: `install() calls write_new()`
- c0005 ..> c0084: `_check_uv() calls run_owned()`
- c0005 ..> c0084: `_forgetful_python() calls run_owned()`
- c0005 ..> c0084: `_run() calls run_owned()`
- c0005 ..> c0084: `pi_ready() calls run_owned()`
- c0006 ..> c0006: `runtime_ready() calls sync_fingerprint()`
- c0006 ..> c0084: `runtime_ready() calls run_owned()`
- c0007 ..> c0008: `close() calls update()`
- c0007 ..> c0008: `start() calls update()`
- c0007 ..> c0008: `type in __init__`
- c0007 ..> c0009: `__init__() calls unknown_status()`
- c0007 ..> c0010: `close() calls close()`
- c0007 ..> c0010: `send() calls send()`
- c0007 ..> c0010: `start() calls start()`
- c0007 ..> c0010: `startup_hint() calls startup_hint()`
- c0007 ..> c0010: `wait() calls wait()`
- c0007 ..> c0030: `type in __init__`
- c0008 ..> c0007: `__enter__() calls start()`
- c0008 ..> c0007: `_close_resources() calls close()`
- c0008 ..> c0008: `__enter__() calls _close_resources()`
- c0008 ..> c0008: `__enter__() calls snapshot()`
- c0008 ..> c0008: `__enter__() calls update()`
- c0008 ..> c0008: `__exit__() calls _close_resources()`
- c0008 ..> c0008: `__exit__() calls _publish_history()`
- c0008 ..> c0008: `__exit__() calls snapshot()`
- c0008 ..> c0008: `__exit__() calls update()`
- c0008 ..> c0008: `_serve() calls snapshot()`
- c0008 ..> c0008: `update() calls _publish_history()`
- c0008 ..> c0009: `__enter__() calls _discovery_path()`
- c0008 ..> c0009: `__enter__() calls _endpoint()`
- c0008 ..> c0009: `_publish_history() calls _discovery_path()`
- c0008 ..> c0009: `_publish_history() calls _read_discovery()`
- c0008 ..> c0009: `_serve() calls _frame()`
- c0008 ..> c0009: `_serve() calls _peer()`
- c0008 ..> c0080: `__enter__() constructs FactoryError`
- c0008 ..> c0082: `__enter__() calls check_real_path()`
- c0008 ..> c0082: `__enter__() calls replace_generated_json()`
- c0008 ..> c0082: `_publish_history() calls replace_generated_json()`
- c0009 ..> c0008: `observe_plain_watch() calls __enter__()`
- c0009 ..> c0008: `observe_plain_watch() calls __exit__()`
- c0009 ..> c0008: `observe_plain_watch() constructs PlainWatchObservation`
- c0009 ..> c0008: `type in observe_plain_watch`
- c0009 ..> c0009: `_frame() calls _observation_json()`
- c0009 ..> c0009: `_read_discovery() calls _discovery_path()`
- c0009 ..> c0009: `_read_discovery() calls _observation_json()`
- c0009 ..> c0009: `plain_watch_status() calls _endpoint()`
- c0009 ..> c0009: `plain_watch_status() calls _frame()`
- c0009 ..> c0009: `plain_watch_status() calls _peer()`
- c0009 ..> c0009: `plain_watch_status() calls _read_discovery()`
- c0009 ..> c0009: `plain_watch_status() calls unknown_status()`
- c0009 ..> c0082: `_read_discovery() calls check_real_path()`
- c0010 ..> c0007: `close() calls close()`
- c0010 ..> c0010: `send() calls _request()`
- c0010 ..> c0010: `start() calls _request()`
- c0010 ..> c0080: `_request() constructs FactoryError`
- c0010 ..> c0080: `wait() constructs FactoryError`
- c0010 ..> c0087: `_request() calls check_watch_stop()`
- c0010 ..> c0087: `wait() calls check_watch_stop()`
- c0012 ..> c0007: `close_session() calls close()`
- c0012 ..> c0007: `control() calls close()`
- c0012 ..> c0007: `control() calls wait()`
- c0012 ..> c0007: `pin_worker() calls close()`
- c0012 ..> c0007: `resume_exit_observation() calls wait()`
- c0012 ..> c0007: `supervise_session() calls wait()`
- c0012 ..> c0011: `serve() constructs SessionState`
- c0012 ..> c0012: `build_shell() calls runtime()`
- c0012 ..> c0012: `capture_worker() calls pin_worker()`
- c0012 ..> c0012: `control() calls serve()`
- c0012 ..> c0012: `interact() calls ready()`
- c0012 ..> c0012: `main() calls control()`
- c0012 ..> c0012: `open_session() calls capture_worker()`
- c0012 ..> c0012: `replace_failed_exit_task() calls resume_exit_observation()`
- c0012 ..> c0012: `serve() calls build_shell()`
- c0012 ..> c0012: `serve() calls close_session()`
- c0012 ..> c0012: `serve() calls open_session()`
- c0012 ..> c0012: `serve() calls supervise_session()`
- c0012 ..> c0012: `serve() calls validate_launch_config()`
- c0012 ..> c0012: `supervise_session() calls cancel_tasks()`
- c0012 ..> c0012: `supervise_session() calls interact()`
- c0012 ..> c0012: `supervise_session() calls replace_failed_exit_task()`
- c0012 ..> c0012: `supervise_session() calls retain_identity()`
- c0012 ..> c0012: `supervise_session() calls worker_exited()`
- c0012 ..> c0073: `control() calls create_task()`
- c0012 ..> c0073: `main() calls create_task()`
- c0012 ..> c0073: `replace_failed_exit_task() calls create_task()`
- c0012 ..> c0073: `supervise_session() calls create_task()`
- c0013 ..> c0080: `runtime_directory() constructs FactoryError`
- c0013 ..> c0082: `runtime_directory() calls check_real_path()`
- c0014 ..> c0022: `main() calls list_models()`
- c0015 ..> c0003: `_apply_controller_problem() calls quote()`
- c0015 ..> c0007: `_await_readiness() calls wait()`
- c0015 ..> c0007: `_cleanup() calls close()`
- c0015 ..> c0007: `_close_controller() calls close()`
- c0015 ..> c0007: `_close_controller() calls wait()`
- c0015 ..> c0007: `_complete_handover() calls close()`
- c0015 ..> c0007: `control() calls close()`
- c0015 ..> c0007: `reap_watcher() calls wait()`
- c0015 ..> c0007: `relay() calls close()`
- c0015 ..> c0007: `run() calls close()`
- c0015 ..> c0007: `run() calls wait()`
- c0015 ..> c0007: `start_watcher() calls close()`
- c0015 ..> c0015: `_apply_controller_event() calls _apply_controller_problem()`
- c0015 ..> c0015: `_apply_controller_event() calls save()`
- c0015 ..> c0015: `_apply_controller_problem() calls save()`
- c0015 ..> c0015: `_apply_controller_problem() calls stop_watcher()`
- c0015 ..> c0015: `_cleanup() calls _close_controller()`
- c0015 ..> c0015: `_cleanup() calls _remove_control_socket()`
- c0015 ..> c0015: `_cleanup() calls stop_watcher()`
- c0015 ..> c0015: `_close_controller() calls save()`
- c0015 ..> c0015: `_finish_observation() calls save()`
- c0015 ..> c0015: `_reject_controller_event() calls save()`
- c0015 ..> c0015: `_reject_controller_event() calls stop_watcher()`
- c0015 ..> c0015: `_start_controller() calls observe()`
- c0015 ..> c0015: `control() calls start_watcher()`
- c0015 ..> c0015: `control() calls stop_watcher()`
- c0015 ..> c0015: `observe() calls _apply_controller_event()`
- c0015 ..> c0015: `observe() calls _finish_observation()`
- c0015 ..> c0015: `observe() calls _reject_controller_event()`
- c0015 ..> c0015: `observe() calls _validate_readiness()`
- c0015 ..> c0015: `relay() calls _relay_request()`
- c0015 ..> c0015: `run() calls _await_readiness()`
- c0015 ..> c0015: `run() calls _cleanup()`
- c0015 ..> c0015: `run() calls _complete_handover()`
- c0015 ..> c0015: `run() calls _start_controller()`
- c0015 ..> c0015: `run() calls save()`
- c0015 ..> c0015: `start_watcher() calls reap_watcher()`
- c0015 ..> c0015: `start_watcher() calls relay()`
- c0015 ..> c0015: `start_watcher() calls stop_watcher()`
- c0015 ..> c0016: `observe() calls _controller_event()`
- c0015 ..> c0016: `relay() calls _watcher_request()`
- c0015 ..> c0027: `__init__() constructs AgentShellLifecycleDeadlines`
- c0015 ..> c0027: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0015 ..> c0073: `_start_controller() calls create_task()`
- c0015 ..> c0073: `start_watcher() calls create_task()`
- c0015 ..> c0080: `_apply_controller_problem() constructs FactoryError`
- c0015 ..> c0080: `_await_readiness() constructs FactoryError`
- c0015 ..> c0080: `_complete_handover() constructs FactoryError`
- c0015 ..> c0080: `_finish_observation() constructs FactoryError`
- c0015 ..> c0080: `_reject_controller_event() constructs FactoryError`
- c0015 ..> c0080: `_relay_request() constructs FactoryError`
- c0015 ..> c0080: `control() constructs FactoryError`
- c0015 ..> c0080: `observe() constructs FactoryError`
- c0015 ..> c0080: `reap_watcher() constructs FactoryError`
- c0015 ..> c0080: `start_watcher() constructs FactoryError`
- c0015 ..> c0082: `save() calls replace_generated_json()`
- c0016 ..> c0003: `_acquire_owner_lock() calls quote()`
- c0016 ..> c0007: `_acquire_owner_lock() calls close()`
- c0016 ..> c0007: `_prepare_owner_startup() calls close()`
- c0016 ..> c0007: `entrypoint() calls close()`
- c0016 ..> c0013: `_prepare_owner_startup() calls runtime_directory()`
- c0016 ..> c0015: `entrypoint() calls run()`
- c0016 ..> c0015: `main() calls run()`
- c0016 ..> c0015: `main() constructs ForemanOwner`
- c0016 ..> c0016: `_controller_event() calls _validate_target()`
- c0016 ..> c0016: `_prepare_owner_startup() calls _acquire_owner_lock()`
- c0016 ..> c0016: `entrypoint() calls _prepare_owner_startup()`
- c0016 ..> c0016: `entrypoint() calls _report_startup_error()`
- c0016 ..> c0016: `entrypoint() calls main()`
- c0016 ..> c0017: `_prepare_owner_startup() calls read_state()`
- c0016 ..> c0073: `main() calls create_task()`
- c0016 ..> c0080: `_acquire_owner_lock() constructs FactoryError`
- c0016 ..> c0080: `_prepare_owner_startup() constructs FactoryError`
- c0016 ..> c0080: `_watcher_request() constructs FactoryError`
- c0017 ..> c0003: `request() calls quote()`
- c0017 ..> c0007: `start_owner() calls close()`
- c0017 ..> c0007: `start_owner() calls wait()`
- c0017 ..> c0013: `read_state() calls runtime_directory()`
- c0017 ..> c0013: `request() calls runtime_directory()`
- c0017 ..> c0013: `start_owner() calls runtime_directory()`
- c0017 ..> c0015: `enter_terminal() calls run()`
- c0017 ..> c0015: `start_owner() calls run()`
- c0017 ..> c0017: `request() calls _reply()`
- c0017 ..> c0017: `request() calls read_state()`
- c0017 ..> c0017: `start_owner() calls _reply()`
- c0017 ..> c0027: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0017 ..> c0027: `type in start_owner`
- c0017 ..> c0080: `_reply() constructs FactoryError`
- c0017 ..> c0080: `enter_terminal() constructs FactoryError`
- c0017 ..> c0080: `read_state() constructs FactoryError`
- c0017 ..> c0080: `request() constructs FactoryError`
- c0017 ..> c0080: `start_owner() constructs FactoryError`
- c0017 ..> c0082: `read_state() calls read_generated_json()`
- c0018 ..> c0007: `close() calls close()`
- c0018 ..> c0018: `send() calls _read()`
- c0018 ..> c0018: `send() calls _write()`
- c0018 ..> c0018: `start() calls _read()`
- c0018 ..> c0018: `start() calls _write()`
- c0018 ..> c0018: `wait() calls _read()`
- c0018 ..> c0027: `__init__() constructs AgentShellLifecycleDeadlines`
- c0018 ..> c0027: `type in __init__`
- c0018 ..> c0080: `_read() constructs FactoryError`
- c0018 ..> c0080: `_write() constructs FactoryError`
- c0018 ..> c0080: `close() constructs FactoryError`
- c0018 ..> c0080: `start() constructs FactoryError`
- c0018 ..> c0087: `_read() calls check_watch_stop()`
- c0018 ..> c0087: `_write() calls check_watch_stop()`
- c0018 ..> c0087: `wait() calls check_watch_stop()`
- c0019 ..> c0019: `_validate_agent() calls _local_selection()`
- c0019 ..> c0019: `_validate_roster() calls _local_selection()`
- c0019 ..> c0019: `_validate_roster() calls relative_path()`
- c0019 ..> c0019: `foreman_launch() calls read_definition()`
- c0019 ..> c0019: `foreman_launch() calls relative_path()`
- c0019 ..> c0019: `read_definition() calls _validate_agent()`
- c0019 ..> c0019: `read_definition() calls _validate_resources()`
- c0019 ..> c0019: `read_definition() calls _validate_roster()`
- c0019 ..> c0080: `foreman_launch() constructs FactoryError`
- c0019 ..> c0080: `read_definition() constructs FactoryError`
- c0019 ..> c0085: `_local_selection() calls nonblank()`
- c0019 ..> c0085: `_validate_agent() calls nonblank()`
- c0019 ..> c0085: `foreman_launch() calls nonblank()`
- c0019 ..> c0085: `relative_path() calls nonblank()`
- c0020 ..> c0020: `prepare() calls _write_agent()`
- c0020 ..> c0020: `prepare() calls _write_foreman_memory()`
- c0020 ..> c0020: `prepare() calls validate_guidance()`
- c0020 ..> c0021: `prepare() calls selected_resources()`
- c0020 ..> c0022: `prepare() calls prepare()`
- c0020 ..> c0026: `__init__() constructs WorkerProfiles`
- c0020 ..> c0036: `type in prepare`
- c0020 ..> c0036: `type in validate_guidance`
- c0020 ..> c0080: `_write_foreman_memory() constructs FactoryError`
- c0020 ..> c0080: `prepare() constructs FactoryError`
- c0020 ..> c0080: `validate_depth() constructs FactoryError`
- c0020 ..> c0080: `validate_guidance() constructs FactoryError`
- c0020 ..> c0082: `_write_agent() calls write_definition()`
- c0020 ..> c0082: `_write_foreman_memory() calls read_generated_json()`
- c0020 ..> c0082: `_write_foreman_memory() calls write_json()`
- c0020 ..> c0082: `prepare() calls check_skill_file()`
- c0020 ..> c0082: `prepare() calls write_new()`
- c0022 ..> c0000: `choose_pi_home() calls confirm()`
- c0022 ..> c0003: `require_pi_home() calls quote()`
- c0022 ..> c0005: `install() calls install()`
- c0022 ..> c0005: `install() constructs HostDependencies`
- c0022 ..> c0005: `installation() calls description()`
- c0022 ..> c0005: `installation() constructs HostDependencies`
- c0022 ..> c0005: `missing_executables() calls pi_ready()`
- c0022 ..> c0005: `missing_executables() constructs HostDependencies`
- c0022 ..> c0006: `missing_executables() calls runtime_ready()`
- c0022 ..> c0006: `role_runtime_ready() calls runtime_ready()`
- c0022 ..> c0019: `selected_launch() calls foreman_launch()`
- c0022 ..> c0020: `prepare_roles() calls validate_depth()`
- c0022 ..> c0020: `prepare_roles() constructs CoordinatorProfiles`
- c0022 ..> c0020: `validate_setup() calls validate_depth()`
- c0022 ..> c0020: `validate_setup() constructs CoordinatorProfiles`
- c0022 ..> c0022: `choose_pi_home() calls pi_home()`
- c0022 ..> c0022: `choose_pi_home() calls require_pi_home()`
- c0022 ..> c0022: `list_models() calls pi_home()`
- c0022 ..> c0022: `list_models() calls require_pi_home()`
- c0022 ..> c0022: `missing_executables() calls pi_home()`
- c0022 ..> c0022: `missing_executables() calls role_runtime_ready()`
- c0022 ..> c0022: `prepare() calls _install_resources()`
- c0022 ..> c0022: `prepare() calls _protect_runtime()`
- c0022 ..> c0022: `prepare() calls save_pi_choice()`
- c0022 ..> c0022: `prepare() calls validate_guidance()`
- c0022 ..> c0022: `prepare_roles() calls list_models()`
- c0022 ..> c0022: `prepare_roles() calls pi_home()`
- c0022 ..> c0022: `prepare_roles() calls prepare()`
- c0022 ..> c0022: `prepare_roles() calls validate_worker_models()`
- c0022 ..> c0022: `record_completion() calls selected_launch()`
- c0022 ..> c0022: `selected_launch() calls validate_setup()`
- c0022 ..> c0022: `validate_guidance() calls _read_guidance()`
- c0022 ..> c0022: `validate_setup() calls missing_executables()`
- c0022 ..> c0022: `validate_setup() calls pi_home()`
- c0022 ..> c0022: `validate_setup() calls require_pi_home()`
- c0022 ..> c0022: `validate_setup() calls validate_bundled_resources()`
- c0022 ..> c0022: `validate_setup() calls validate_guidance()`
- c0022 ..> c0022: `validate_worker_models() calls list_models()`
- c0022 ..> c0024: `_install_resources() calls bundled_files()`
- c0022 ..> c0025: `selected_launch() calls selected_skill_files()`
- c0022 ..> c0036: `type in record_completion`
- c0022 ..> c0036: `type in selected_launch`
- c0022 ..> c0036: `type in validate_completion`
- c0022 ..> c0036: `type in validate_worker_models`
- c0022 ..> c0043: `check() calls check()`
- c0022 ..> c0043: `create_project() calls create_project()`
- c0022 ..> c0043: `login() calls login()`
- c0022 ..> c0043: `projects() calls projects()`
- c0022 ..> c0043: `uses_browser_login() calls uses_browser_login()`
- c0022 ..> c0071: `check() constructs AgentForgetfulConnection`
- c0022 ..> c0071: `create_project() constructs AgentForgetfulConnection`
- c0022 ..> c0071: `login() constructs AgentForgetfulConnection`
- c0022 ..> c0071: `projects() constructs AgentForgetfulConnection`
- c0022 ..> c0072: `list_models() calls role_environment()`
- c0022 ..> c0075: `type in check`
- c0022 ..> c0075: `type in create_project`
- c0022 ..> c0075: `type in list_models`
- c0022 ..> c0075: `type in login`
- c0022 ..> c0075: `type in missing_executables`
- c0022 ..> c0075: `type in prepare`
- c0022 ..> c0075: `type in projects`
- c0022 ..> c0075: `type in uses_browser_login`
- c0022 ..> c0075: `type in validate_setup`
- c0022 ..> c0080: `_install_resources() constructs FactoryError`
- c0022 ..> c0080: `_read_guidance() constructs FactoryError`
- c0022 ..> c0080: `choose_pi_home() constructs FactoryError`
- c0022 ..> c0080: `list_models() constructs FactoryError`
- c0022 ..> c0080: `pi_home() constructs FactoryError`
- c0022 ..> c0080: `prepare_roles() constructs FactoryError`
- c0022 ..> c0080: `prepare_setup_guidance() constructs FactoryError`
- c0022 ..> c0080: `require_pi_home() constructs FactoryError`
- c0022 ..> c0080: `selected_launch() constructs FactoryError`
- c0022 ..> c0080: `validate_bundled_resources() constructs FactoryError`
- c0022 ..> c0080: `validate_completion() constructs FactoryError`
- c0022 ..> c0080: `validate_guidance() constructs FactoryError`
- c0022 ..> c0080: `validate_setup() constructs FactoryError`
- c0022 ..> c0080: `validate_worker_models() constructs FactoryError`
- c0022 ..> c0081: `missing_executables() calls executable_path()`
- c0022 ..> c0081: `require_pi_home() calls executable_path()`
- c0022 ..> c0082: `_install_resources() calls write_new()`
- c0022 ..> c0082: `_protect_runtime() calls write_new()`
- c0022 ..> c0082: `begin_setup() calls remove_generated()`
- c0022 ..> c0082: `pi_home() calls read_generated_json()`
- c0022 ..> c0082: `prepare() calls write_new()`
- c0022 ..> c0082: `prepare_roles() calls check_real_path()`
- c0022 ..> c0082: `prepare_setup_guidance() calls write_new()`
- c0022 ..> c0082: `record_completion() calls replace_generated_json()`
- c0022 ..> c0082: `save_pi_choice() calls write_json()`
- c0022 ..> c0082: `validate_bundled_resources() calls check_real_path()`
- c0022 ..> c0082: `validate_completion() calls read_generated_json()`
- c0022 ..> c0084: `list_models() calls run_owned()`
- c0024 ..> c0023: `plan_update() constructs ResourceUpdate`
- c0024 ..> c0023: `type in _back_up`
- c0024 ..> c0023: `type in apply_update`
- c0024 ..> c0023: `type in plan_update`
- c0024 ..> c0024: `apply_update() calls _back_up()`
- c0024 ..> c0024: `bundled_files() calls _digest()`
- c0024 ..> c0024: `plan_update() calls _digest()`
- c0024 ..> c0024: `plan_update() calls bundled_files()`
- c0024 ..> c0080: `bundled_files() constructs FactoryError`
- c0024 ..> c0080: `plan_update() constructs FactoryError`
- c0024 ..> c0082: `plan_update() calls check_real_path()`
- c0025 ..> c0007: `_add_skill_file() calls close()`
- c0025 ..> c0025: `_walk_skill_directory() calls _add_skill_file()`
- c0025 ..> c0025: `selected_skill_files() calls _add_skill_file()`
- c0025 ..> c0025: `selected_skill_files() calls _walk_skill_directory()`
- c0025 ..> c0080: `_add_skill_file() constructs FactoryError`
- c0025 ..> c0080: `_walk_skill_directory() constructs FactoryError`
- c0025 ..> c0080: `selected_skill_files() constructs FactoryError`
- c0026 ..> c0008: `prepare() calls update()`
- c0026 ..> c0028: `type in prepare`
- c0026 ..> c0082: `prepare() calls check_skill_file()`
- c0026 ..> c0082: `prepare() calls write_definition()`
- c0026 ..> c0082: `prepare() calls write_new()`
- c0027 ..> c0085: `__post_init__() calls positive_duration()`
- c0029 ..> c0028: `type in _validate_foreman_memory`
- c0029 ..> c0028: `type in validate_initial_agents`
- c0029 ..> c0028: `type in validate_workers`
- c0029 ..> c0029: `validate_initial_agents() calls _validate_foreman_memory()`
- c0029 ..> c0029: `validate_initial_agents() calls validate_role_app()`
- c0029 ..> c0029: `validate_initial_agents() calls validate_workers()`
- c0029 ..> c0029: `validate_workers() calls validate_role_app()`
- c0029 ..> c0080: `_validate_foreman_memory() constructs FactoryError`
- c0029 ..> c0080: `skill_paths() constructs FactoryError`
- c0029 ..> c0080: `validate_initial_agents() constructs FactoryError`
- c0029 ..> c0080: `validate_role_app() constructs FactoryError`
- c0029 ..> c0080: `validate_workers() constructs FactoryError`
- c0029 ..> c0085: `_validate_foreman_memory() calls nonblank()`
- c0029 ..> c0085: `skill_paths() calls nonblank()`
- c0029 ..> c0085: `validate_initial_agents() calls nonblank()`
- c0029 ..> c0085: `validate_workers() calls nonblank()`
- c0031 ..> c0000: `_dispose() calls confirm()`
- c0031 ..> c0000: `poll() calls load()`
- c0031 ..> c0007: `_candidates() calls send()`
- c0031 ..> c0007: `_dispose() calls send()`
- c0031 ..> c0007: `_read_problem() calls send()`
- c0031 ..> c0007: `_repository_identities() calls send()`
- c0031 ..> c0007: `poll() calls send()`
- c0031 ..> c0008: `_candidate() calls snapshot()`
- c0031 ..> c0008: `_candidate() calls update()`
- c0031 ..> c0008: `_check_namespaces() calls update()`
- c0031 ..> c0008: `_still_completed() calls snapshot()`
- c0031 ..> c0031: `_candidate() calls _keys()`
- c0031 ..> c0031: `_candidates() calls _candidate()`
- c0031 ..> c0031: `_candidates() calls _in_scope()`
- c0031 ..> c0031: `_check_namespaces() calls _keys()`
- c0031 ..> c0031: `_claim_indexes() calls _claims()`
- c0031 ..> c0031: `_claim_indexes() calls _read_problem()`
- c0031 ..> c0031: `_claims() calls _is_confirmed()`
- c0031 ..> c0031: `_claims() calls _keys()`
- c0031 ..> c0031: `_claims() calls _task_mappings()`
- c0031 ..> c0031: `_dispose() calls _check_namespaces()`
- c0031 ..> c0031: `_dispose() calls _keys()`
- c0031 ..> c0031: `_dispose() calls _mapping_identity()`
- c0031 ..> c0031: `_dispose() calls _overlaps()`
- c0031 ..> c0031: `_dispose() calls _read_problem()`
- c0031 ..> c0031: `_dispose() calls _still_completed()`
- c0031 ..> c0031: `_is_confirmed() calls _mapping_identity()`
- c0031 ..> c0031: `_read_plans() calls _read_problem()`
- c0031 ..> c0031: `_still_completed() calls _in_scope()`
- c0031 ..> c0031: `_task_mappings() calls _validate_claim_mapping()`
- c0031 ..> c0031: `poll() calls _candidates()`
- c0031 ..> c0031: `poll() calls _claim_indexes()`
- c0031 ..> c0031: `poll() calls _dispose()`
- c0031 ..> c0031: `poll() calls _in_scope()`
- c0031 ..> c0031: `poll() calls _is_confirmed()`
- c0031 ..> c0031: `poll() calls _order()`
- c0031 ..> c0031: `poll() calls _read_plans()`
- c0031 ..> c0031: `poll() calls _repository_identities()`
- c0031 ..> c0032: `_candidate() constructs CompletedWork`
- c0031 ..> c0032: `type in _candidate`
- c0031 ..> c0032: `type in _candidates`
- c0031 ..> c0032: `type in _dispose`
- c0031 ..> c0032: `type in _order`
- c0031 ..> c0032: `type in _still_completed`
- c0031 ..> c0033: `_candidate() calls _claim_path()`
- c0031 ..> c0033: `_claims() calls _claim_path()`
- c0031 ..> c0033: `_dispose() calls _claim_path()`
- c0031 ..> c0033: `_keys() calls _claim_path()`
- c0031 ..> c0033: `_overlaps() calls _claim_path()`
- c0031 ..> c0033: `_repository_identities() calls _claim_path()`
- c0031 ..> c0038: `_candidate() calls check_source()`
- c0031 ..> c0038: `_candidate() calls context()`
- c0031 ..> c0038: `_candidate() calls mapping_repository()`
- c0031 ..> c0038: `_candidate() calls ownership_records()`
- c0031 ..> c0038: `_dispose() calls check_repository()`
- c0031 ..> c0038: `_dispose() calls mapping_repository()`
- c0031 ..> c0038: `_still_completed() calls context()`
- c0031 ..> c0038: `_still_completed() calls ownership()`
- c0031 ..> c0038: `type in __init__`
- c0031 ..> c0040: `type in __init__`
- c0031 --> c0041: `field confirmed`
- c0031 ..> c0041: `_is_confirmed() calls overlaps()`
- c0031 ..> c0041: `_mapping_identity() constructs CleanupSet`
- c0031 ..> c0041: `type in _mapping_identity`
- c0031 ..> c0053: `_candidate() constructs ScaffoldProblem`
- c0031 ..> c0053: `_check_namespaces() constructs ScaffoldProblem`
- c0031 ..> c0053: `_dispose() constructs ScaffoldProblem`
- c0031 ..> c0053: `_is_confirmed() constructs ScaffoldProblem`
- c0031 ..> c0053: `_still_completed() constructs ScaffoldProblem`
- c0031 ..> c0053: `_task_mappings() constructs ScaffoldProblem`
- c0031 ..> c0053: `_validate_claim_mapping() constructs ScaffoldProblem`
- c0031 ..> c0056: `_dispose() calls clear()`
- c0031 ..> c0056: `_repository_identities() calls clear()`
- c0031 ..> c0056: `poll() calls clear()`
- c0031 ..> c0056: `type in _candidates`
- c0031 ..> c0056: `type in _claim_indexes`
- c0031 ..> c0056: `type in _dispose`
- c0031 ..> c0056: `type in _read_plans`
- c0031 ..> c0056: `type in _read_problem`
- c0031 ..> c0056: `type in _repository_identities`
- c0031 ..> c0056: `type in poll`
- c0031 ..> c0073: `_candidates() calls tasks()`
- c0031 ..> c0073: `_claim_indexes() calls tasks()`
- c0031 ..> c0073: `_in_scope() calls owns()`
- c0031 ..> c0073: `_mapping_identity() calls backend_identity()`
- c0031 ..> c0073: `_read_plans() calls get_plan()`
- c0031 ..> c0073: `_still_completed() calls get_plan()`
- c0031 ..> c0073: `poll() calls plans()`
- c0031 ..> c0080: `type in _read_problem`
- c0031 ..> c0088: `_in_scope() calls is_key()`
- c0031 ..> c0092: `type in __init__`
- c0031 ..> c0095: `_claims() calls repository_identity()`
- c0031 ..> c0095: `_dispose() calls dispose()`
- c0031 ..> c0095: `_repository_identities() calls repository_identity()`
- c0031 ..> c0095: `poll() calls begin_cleanup_cycle()`
- c0031 ..> c0100: `type in __init__`
- c0035 ..> c0034: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0035 ..> c0067: `validate_cleanup_marker() calls is_change_request()`
- c0035 ..> c0068: `type in validate_cleanup_marker`
- c0035 ..> c0069: `type in validate_cleanup_marker`
- c0036 --> c0066: `field repository`
- c0036 --> c0075: `field forgetful`
- c0037 ..> c0036: `from_mapping() constructs FactoryConfiguration`
- c0037 ..> c0036: `type in from_mapping`
- c0037 ..> c0036: `type in validate`
- c0037 ..> c0037: `from_mapping() calls validate()`
- c0037 ..> c0066: `from_mapping() constructs RepositoryReference`
- c0037 ..> c0075: `validate() calls validate()`
- c0037 ..> c0076: `from_mapping() calls connection_from_mapping()`
- c0037 ..> c0080: `from_mapping() constructs FactoryError`
- c0037 ..> c0080: `validate() constructs FactoryError`
- c0037 ..> c0085: `unique_labels() calls nonblank()`
- c0037 ..> c0085: `validate() calls nonblank()`
- c0037 ..> c0091: `from_mapping() constructs TicketSource`
- c0038 ..> c0036: `type in __init__`
- c0038 ..> c0038: `check_repository() calls check_source()`
- c0038 ..> c0038: `ownership() calls ownership_records()`
- c0038 ..> c0052: `check_repository() constructs RepositoryProblem`
- c0038 ..> c0052: `check_source() constructs RepositoryProblem`
- c0038 ..> c0053: `active() constructs ScaffoldProblem`
- c0038 ..> c0053: `context() constructs ScaffoldProblem`
- c0038 ..> c0053: `mapping_repository() constructs ScaffoldProblem`
- c0038 ..> c0053: `ownership_records() constructs ScaffoldProblem`
- c0038 ..> c0053: `snapshot() constructs ScaffoldProblem`
- c0038 ..> c0066: `type in check_repository`
- c0038 ..> c0066: `type in check_source`
- c0038 ..> c0066: `type in mapping_repository`
- c0038 ..> c0067: `check_source() calls repository()`
- c0038 ..> c0068: `type in check_source`
- c0038 ..> c0069: `type in __init__`
- c0038 ..> c0073: `ownership() calls tasks()`
- c0038 ..> c0077: `type in __init__`
- c0038 ..> c0090: `snapshot() constructs Ticket`
- c0038 ..> c0090: `type in snapshot`
- c0038 ..> c0091: `snapshot() constructs TicketSource`
- c0038 ..> c0093: `check_repository() calls origin()`
- c0038 ..> c0097: `type in __init__`
- c0039 ..> c0000: `load_existing() calls load()`
- c0039 ..> c0000: `prepare_foreman() calls confirm()`
- c0039 ..> c0002: `initialise() calls save()`
- c0039 ..> c0005: `prepare_foreman() calls install()`
- c0039 ..> c0020: `prepare_foreman() calls prepare()`
- c0039 ..> c0022: `check_foreman() calls check()`
- c0039 ..> c0022: `check_foreman() calls login()`
- c0039 ..> c0022: `prepare_foreman() calls installation()`
- c0039 ..> c0022: `prepare_foreman() calls missing_executables()`
- c0039 ..> c0036: `configure() constructs FactoryConfiguration`
- c0039 ..> c0036: `type in _preflight`
- c0039 ..> c0036: `type in check_foreman`
- c0039 ..> c0036: `type in configure`
- c0039 ..> c0036: `type in initialise`
- c0039 ..> c0036: `type in load_existing`
- c0039 ..> c0037: `_preflight() calls validate()`
- c0039 ..> c0037: `configure() calls unique_labels()`
- c0039 ..> c0037: `load_existing() calls unique_labels()`
- c0039 ..> c0039: `configure() calls inspect()`
- c0039 ..> c0039: `initialise() calls _ensure_label()`
- c0039 ..> c0039: `initialise() calls _preflight()`
- c0039 ..> c0042: `type in __init__`
- c0039 ..> c0043: `type in __init__`
- c0039 ..> c0066: `inspect() constructs RepositoryReference`
- c0039 ..> c0066: `type in inspect`
- c0039 ..> c0067: `_preflight() calls repository()`
- c0039 ..> c0067: `inspect() calls repository()`
- c0039 ..> c0069: `type in __init__`
- c0039 ..> c0075: `type in prepare_foreman`
- c0039 ..> c0080: `_preflight() constructs FactoryError`
- c0039 ..> c0080: `initialise() constructs FactoryError`
- c0039 ..> c0080: `inspect() constructs FactoryError`
- c0039 ..> c0080: `load_existing() constructs FactoryError`
- c0039 ..> c0080: `prepare_foreman() constructs FactoryError`
- c0039 ..> c0088: `_ensure_label() calls create_label()`
- c0039 ..> c0088: `_preflight() calls check_access()`
- c0039 ..> c0088: `_preflight() calls list_labels()`
- c0039 ..> c0088: `_preflight() calls validate_source()`
- c0039 ..> c0089: `_ensure_label() constructs Label`
- c0039 ..> c0089: `type in _preflight`
- c0039 ..> c0091: `inspect() constructs TicketSource`
- c0039 ..> c0091: `type in _ensure_label`
- c0039 ..> c0091: `type in _preflight`
- c0039 ..> c0092: `type in __init__`
- c0039 ..> c0093: `_preflight() calls origin()`
- c0039 ..> c0093: `discover() calls discover()`
- c0039 ..> c0093: `inspect() calls origin()`
- c0039 ..> c0097: `type in __init__`
- c0040 ..> c0041: `type in confirm`
- c0040 ..> c0041: `type in load`
- c0042 ..> c0036: `type in load`
- c0042 ..> c0036: `type in save`
- c0043 ..> c0028: `type in prepare_roles`
- c0043 ..> c0036: `type in prepare_roles`
- c0043 ..> c0036: `type in record_completion`
- c0043 ..> c0036: `type in selected_launch`
- c0043 ..> c0075: `type in check`
- c0043 ..> c0075: `type in create_project`
- c0043 ..> c0075: `type in list_models`
- c0043 ..> c0075: `type in login`
- c0043 ..> c0075: `type in missing_executables`
- c0043 ..> c0075: `type in prepare`
- c0043 ..> c0075: `type in projects`
- c0043 ..> c0075: `type in uses_browser_login`
- c0045 ..> c0008: `recover() calls snapshot()`
- c0045 ..> c0022: `check() calls check()`
- c0045 ..> c0035: `_ensure_mapping() calls validate_cleanup_marker()`
- c0045 ..> c0036: `type in __init__`
- c0045 ..> c0038: `__init__() constructs FactoryRecords`
- c0045 ..> c0038: `_create_ownership() calls ownership()`
- c0045 ..> c0038: `_ensure_mapping() calls check_source()`
- c0045 ..> c0038: `_ensure_worktrees() calls mapping_repository()`
- c0045 ..> c0038: `_prepare_plan() calls active()`
- c0045 ..> c0038: `_prepare_plan() calls context()`
- c0045 ..> c0038: `_setup_ownership() calls ownership()`
- c0045 ..> c0038: `check_repository() calls check_repository()`
- c0045 ..> c0038: `recover() calls active()`
- c0045 ..> c0038: `recover() calls context()`
- c0045 ..> c0038: `recover() calls ownership()`
- c0045 ..> c0039: `preflight() calls inspect()`
- c0045 ..> c0045: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0045 ..> c0045: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0045 ..> c0045: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0045 ..> c0045: `_initial_mappings() calls _repository()`
- c0045 ..> c0045: `_prepare_plan() calls _create_ownership()`
- c0045 ..> c0045: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0045 ..> c0045: `_prepare_plan() calls _setup_ownership()`
- c0045 ..> c0045: `preflight() calls _initial_mappings()`
- c0045 ..> c0045: `preflight() calls _repository()`
- c0045 ..> c0045: `preflight() calls check_repository()`
- c0045 ..> c0045: `prepare() calls _create_plan()`
- c0045 ..> c0045: `prepare() calls _prepare_plan()`
- c0045 ..> c0045: `prepare() calls lookup()`
- c0045 ..> c0045: `prepare() calls preflight()`
- c0045 ..> c0045: `prepare() calls recover()`
- c0045 ..> c0045: `recover() calls _ensure_worktrees()`
- c0045 ..> c0045: `recover() calls _recovery_plan()`
- c0045 ..> c0045: `recover() calls _repository()`
- c0045 ..> c0045: `recover() calls _sole_recovery_owner()`
- c0045 ..> c0045: `recover() calls _validate_recovery_candidates()`
- c0045 ..> c0045: `recover() calls check_repository()`
- c0045 ..> c0045: `unfinished() calls _is_unfinished_factory_plan()`
- c0045 ..> c0046: `_initial_mappings() calls worktree_name()`
- c0045 ..> c0051: `preflight() constructs IntakeProblem`
- c0045 ..> c0053: `_create_plan() constructs ScaffoldProblem`
- c0045 ..> c0053: `_ensure_mapping() constructs ScaffoldProblem`
- c0045 ..> c0053: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0045 ..> c0053: `_recovery_plan() constructs ScaffoldProblem`
- c0045 ..> c0053: `_setup_ownership() constructs ScaffoldProblem`
- c0045 ..> c0053: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0045 ..> c0053: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0045 ..> c0053: `lookup() constructs ScaffoldProblem`
- c0045 ..> c0054: `_create_plan() constructs ScaffoldReadProblem`
- c0045 ..> c0054: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0045 ..> c0054: `lookup() constructs ScaffoldReadProblem`
- c0045 ..> c0054: `prepare() constructs ScaffoldReadProblem`
- c0045 ..> c0054: `recover() constructs ScaffoldReadProblem`
- c0045 ..> c0055: `_create_ownership() constructs UncertainScaffold`
- c0045 ..> c0055: `_create_plan() constructs UncertainScaffold`
- c0045 ..> c0055: `_setup_ownership() constructs UncertainScaffold`
- c0045 ..> c0055: `_sole_recovery_owner() constructs UncertainScaffold`
- c0045 ..> c0055: `prepare() constructs UncertainScaffold`
- c0045 ..> c0066: `type in _ensure_validated_mapping`
- c0045 ..> c0066: `type in _repository`
- c0045 ..> c0066: `type in check_repository`
- c0045 ..> c0069: `type in __init__`
- c0045 ..> c0073: `_create_ownership() calls create_task()`
- c0045 ..> c0073: `_create_ownership() calls update_plan()`
- c0045 ..> c0073: `_create_plan() calls create_plan()`
- c0045 ..> c0073: `_create_plan() calls get_plan()`
- c0045 ..> c0073: `_create_plan() calls owns()`
- c0045 ..> c0073: `_create_plan() calls plans()`
- c0045 ..> c0073: `_is_unfinished_factory_plan() calls owns()`
- c0045 ..> c0073: `_recovery_plan() calls get_plan()`
- c0045 ..> c0073: `_recovery_plan() calls owns()`
- c0045 ..> c0073: `_recovery_plan() calls plans()`
- c0045 ..> c0073: `lookup() calls plans()`
- c0045 ..> c0073: `unfinished() calls plans()`
- c0045 ..> c0077: `type in __init__`
- c0045 ..> c0080: `_is_unfinished_factory_plan() constructs FactoryError`
- c0045 ..> c0090: `type in _create_plan`
- c0045 ..> c0090: `type in _initial_mappings`
- c0045 ..> c0090: `type in _prepare_plan`
- c0045 ..> c0090: `type in _setup_ownership`
- c0045 ..> c0090: `type in lookup`
- c0045 ..> c0090: `type in preflight`
- c0045 ..> c0090: `type in prepare`
- c0045 ..> c0090: `type in recover`
- c0045 ..> c0091: `type in _repository`
- c0045 ..> c0095: `_ensure_mapping() calls ensure()`
- c0045 ..> c0095: `_ensure_mapping() calls verify_removed()`
- c0045 ..> c0095: `_initial_mappings() calls target_branch()`
- c0045 ..> c0097: `type in __init__`
- c0045 ..> c0100: `type in __init__`
- c0046 ..> c0090: `type in worktree_name`
- c0047 --> c0090: `field issue`
- c0048 ..> c0007: `_alert_plan() calls send()`
- c0048 ..> c0007: `_check_pending_repositories() calls send()`
- c0048 ..> c0007: `_check_planning_access() calls send()`
- c0048 ..> c0007: `_handle_intake_read_problem() calls send()`
- c0048 ..> c0007: `_handle_intake_repository_problem() calls send()`
- c0048 ..> c0007: `_handle_recovery_read_problem() calls send()`
- c0048 ..> c0007: `_load_inventory() calls send()`
- c0048 ..> c0007: `_process_issue() calls send()`
- c0048 ..> c0007: `_read_issues() calls send()`
- c0048 ..> c0007: `_recover_work() calls send()`
- c0048 ..> c0007: `_submit() calls send()`
- c0048 ..> c0007: `_watch() calls close()`
- c0048 ..> c0007: `_watch() calls start()`
- c0048 ..> c0007: `_watch() calls wait()`
- c0048 ..> c0007: `run() calls startup_hint()`
- c0048 ..> c0020: `_process_issue() calls prepare()`
- c0048 ..> c0022: `_check_planning_access() calls check()`
- c0048 ..> c0030: `type in __init__`
- c0048 ..> c0031: `_watch() calls poll()`
- c0048 ..> c0031: `type in __init__`
- c0048 ..> c0036: `type in _poll_sources`
- c0048 ..> c0036: `type in _repository_for_source`
- c0048 ..> c0036: `type in _watch`
- c0048 ..> c0036: `type in run`
- c0048 ..> c0038: `_check_pending_repositories() calls check_repository()`
- c0048 ..> c0045: `_load_inventory() calls unfinished()`
- c0048 ..> c0045: `_process_issue() calls lookup()`
- c0048 ..> c0045: `_process_issue() calls recover()`
- c0048 ..> c0045: `_recover_work() calls recover()`
- c0048 ..> c0045: `type in __init__`
- c0048 ..> c0047: `_complete_intake() constructs BlockedWork`
- c0048 ..> c0047: `_handle_intake_read_problem() constructs BlockedWork`
- c0048 ..> c0047: `_handle_intake_repository_problem() constructs BlockedWork`
- c0048 ..> c0047: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0048 ..> c0047: `_process_issue() constructs BlockedWork`
- c0048 ..> c0047: `_remember_inventory_candidate() constructs BlockedWork`
- c0048 ..> c0047: `type in _alert_plan`
- c0048 ..> c0047: `type in _complete_intake`
- c0048 ..> c0047: `type in _complete_recovery`
- c0048 ..> c0047: `type in _handle_recovery_read_problem`
- c0048 ..> c0047: `type in _handle_recovery_repository_problem`
- c0048 ..> c0047: `type in _recover_work`
- c0048 ..> c0047: `type in _remember_task_ids`
- c0048 ..> c0048: `_complete_intake() calls _submit()`
- c0048 ..> c0048: `_complete_recovery() calls _submit()`
- c0048 ..> c0048: `_handle_intake_read_problem() calls _sole_task_id()`
- c0048 ..> c0048: `_handle_intake_repository_problem() calls _alert_plan()`
- c0048 ..> c0048: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0048 ..> c0048: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0048 ..> c0048: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0048 ..> c0048: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0048 ..> c0048: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0048 ..> c0048: `_load_inventory() calls _remember_inventory_candidate()`
- c0048 ..> c0048: `_poll_sources() calls _baseline_source()`
- c0048 ..> c0048: `_poll_sources() calls _process_source()`
- c0048 ..> c0048: `_poll_sources() calls _read_issues()`
- c0048 ..> c0048: `_poll_sources() calls _repository_for_source()`
- c0048 ..> c0048: `_process_issue() calls _complete_intake()`
- c0048 ..> c0048: `_process_issue() calls _handle_intake_read_problem()`
- c0048 ..> c0048: `_process_issue() calls _handle_intake_repository_problem()`
- c0048 ..> c0048: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0048 ..> c0048: `_process_issues() calls _process_issue()`
- c0048 ..> c0048: `_process_issues() calls _skip_issue()`
- c0048 ..> c0048: `_process_source() calls _include_pending_lookups()`
- c0048 ..> c0048: `_process_source() calls _process_issues()`
- c0048 ..> c0048: `_recover_blocked() calls _recover_work()`
- c0048 ..> c0048: `_recover_work() calls _alert_plan()`
- c0048 ..> c0048: `_recover_work() calls _complete_recovery()`
- c0048 ..> c0048: `_recover_work() calls _handle_recovery_read_problem()`
- c0048 ..> c0048: `_recover_work() calls _handle_recovery_repository_problem()`
- c0048 ..> c0048: `_recover_work() calls _remember_task_ids()`
- c0048 ..> c0048: `_remember_inventory_candidate() calls _alert_plan()`
- c0048 ..> c0048: `_watch() calls _check_pending_repositories()`
- c0048 ..> c0048: `_watch() calls _check_planning_access()`
- c0048 ..> c0048: `_watch() calls _load_inventory()`
- c0048 ..> c0048: `_watch() calls _poll_sources()`
- c0048 ..> c0048: `_watch() calls _recover_blocked()`
- c0048 ..> c0048: `run() calls _watch()`
- c0048 ..> c0049: `_watch() constructs _WatchState`
- c0048 ..> c0049: `type in _baseline_source`
- c0048 ..> c0049: `type in _check_pending_repositories`
- c0048 ..> c0049: `type in _check_planning_access`
- c0048 ..> c0049: `type in _complete_intake`
- c0048 ..> c0049: `type in _complete_recovery`
- c0048 ..> c0049: `type in _handle_intake_read_problem`
- c0048 ..> c0049: `type in _handle_intake_repository_problem`
- c0048 ..> c0049: `type in _handle_intake_scaffold_problem`
- c0048 ..> c0049: `type in _handle_recovery_repository_problem`
- c0048 ..> c0049: `type in _load_inventory`
- c0048 ..> c0049: `type in _poll_sources`
- c0048 ..> c0049: `type in _process_issue`
- c0048 ..> c0049: `type in _process_issues`
- c0048 ..> c0049: `type in _process_source`
- c0048 ..> c0049: `type in _recover_blocked`
- c0048 ..> c0049: `type in _recover_work`
- c0048 ..> c0049: `type in _remember_inventory_candidate`
- c0048 ..> c0049: `type in _skip_issue`
- c0048 ..> c0050: `type in _process_issue`
- c0048 ..> c0050: `type in _recover_work`
- c0048 ..> c0052: `type in _handle_intake_repository_problem`
- c0048 ..> c0052: `type in _handle_recovery_repository_problem`
- c0048 ..> c0053: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0048 ..> c0053: `type in _alert_plan`
- c0048 ..> c0053: `type in _handle_intake_scaffold_problem`
- c0048 ..> c0054: `type in _handle_intake_read_problem`
- c0048 ..> c0054: `type in _handle_recovery_read_problem`
- c0048 ..> c0056: `_check_pending_repositories() calls clear()`
- c0048 ..> c0056: `_check_planning_access() calls clear()`
- c0048 ..> c0056: `_complete_intake() calls clear()`
- c0048 ..> c0056: `_complete_recovery() calls clear()`
- c0048 ..> c0056: `_load_inventory() calls clear()`
- c0048 ..> c0056: `_process_issue() calls clear()`
- c0048 ..> c0056: `_read_issues() calls clear()`
- c0048 ..> c0056: `_watch() calls clear()`
- c0048 ..> c0056: `_watch() constructs WatcherAlerts`
- c0048 ..> c0056: `type in _alert_plan`
- c0048 ..> c0056: `type in _check_pending_repositories`
- c0048 ..> c0056: `type in _check_planning_access`
- c0048 ..> c0056: `type in _complete_intake`
- c0048 ..> c0056: `type in _complete_recovery`
- c0048 ..> c0056: `type in _handle_intake_read_problem`
- c0048 ..> c0056: `type in _handle_intake_repository_problem`
- c0048 ..> c0056: `type in _handle_intake_scaffold_problem`
- c0048 ..> c0056: `type in _handle_recovery_read_problem`
- c0048 ..> c0056: `type in _handle_recovery_repository_problem`
- c0048 ..> c0056: `type in _load_inventory`
- c0048 ..> c0056: `type in _poll_sources`
- c0048 ..> c0056: `type in _process_issue`
- c0048 ..> c0056: `type in _process_issues`
- c0048 ..> c0056: `type in _process_source`
- c0048 ..> c0056: `type in _read_issues`
- c0048 ..> c0056: `type in _recover_blocked`
- c0048 ..> c0056: `type in _recover_work`
- c0048 ..> c0056: `type in _remember_inventory_candidate`
- c0048 ..> c0066: `type in _handle_intake_repository_problem`
- c0048 ..> c0066: `type in _process_issue`
- c0048 ..> c0066: `type in _process_issues`
- c0048 ..> c0066: `type in _process_source`
- c0048 ..> c0066: `type in _repository_for_source`
- c0048 ..> c0080: `_read_issues() constructs FactoryError`
- c0048 ..> c0087: `_submit() calls check_watch_stop()`
- c0048 ..> c0087: `_watch() calls check_watch_stop()`
- c0048 ..> c0087: `run() calls check_watch_stop()`
- c0048 ..> c0088: `_read_issues() calls list_open()`
- c0048 ..> c0090: `type in _baseline_source`
- c0048 ..> c0090: `type in _complete_intake`
- c0048 ..> c0090: `type in _complete_recovery`
- c0048 ..> c0090: `type in _handle_intake_read_problem`
- c0048 ..> c0090: `type in _handle_intake_repository_problem`
- c0048 ..> c0090: `type in _handle_intake_scaffold_problem`
- c0048 ..> c0090: `type in _include_pending_lookups`
- c0048 ..> c0090: `type in _process_issue`
- c0048 ..> c0090: `type in _process_issues`
- c0048 ..> c0090: `type in _process_source`
- c0048 ..> c0090: `type in _read_issues`
- c0048 ..> c0090: `type in _skip_issue`
- c0048 ..> c0090: `type in _submit`
- c0048 ..> c0091: `_watch() constructs TicketSource`
- c0048 ..> c0091: `type in _baseline_source`
- c0048 ..> c0091: `type in _include_pending_lookups`
- c0048 ..> c0091: `type in _poll_sources`
- c0048 ..> c0091: `type in _process_source`
- c0048 ..> c0091: `type in _read_issues`
- c0048 ..> c0091: `type in _repository_for_source`
- c0048 ..> c0092: `type in __init__`
- c0049 --> c0047: `field blocked`
- c0049 --> c0047: `field known`
- c0049 --> c0066: `field pending_repositories`
- c0049 --> c0090: `field pending_lookup`
- c0049 --> c0091: `field baselined`
- c0051 --|> c0053: `inherits`
- c0052 --|> c0053: `inherits`
- c0053 --|> c0080: `inherits`
- c0054 --|> c0053: `inherits`
- c0055 --|> c0053: `inherits`
- c0056 ..> c0000: `__init__() calls __init__()`
- c0056 ..> c0007: `send() calls send()`
- c0056 ..> c0057: `send() calls _cleanup_recovery()`
- c0056 ..> c0080: `type in send`
- c0058 ..> c0000: `build_watcher() constructs FileCleanupReceipts`
- c0058 ..> c0002: `build_initialiser() constructs TomlConfigurationStore`
- c0058 ..> c0007: `build_watcher() constructs ObservedTerminal`
- c0058 ..> c0018: `build_watcher() constructs AgentShellTerminal`
- c0058 ..> c0022: `build_initialiser() constructs ForemanProfile`
- c0058 ..> c0022: `build_watcher() calls managed_memory_notice()`
- c0058 ..> c0022: `prepare_foreman_launch() calls pi_home()`
- c0058 ..> c0022: `prepare_foreman_launch() calls selected_launch()`
- c0058 ..> c0022: `prepare_foreman_launch() calls validate_completion()`
- c0058 ..> c0022: `prepare_foreman_launch() constructs ForemanProfile`
- c0058 ..> c0031: `build_watcher() constructs CleanupCompleted`
- c0058 ..> c0036: `type in build_watcher`
- c0058 ..> c0036: `type in prepare_foreman_launch`
- c0058 ..> c0036: `type in select_ticketing`
- c0058 ..> c0039: `build_initialiser() constructs InitialiseFactory`
- c0058 ..> c0039: `type in build_initialiser`
- c0058 ..> c0045: `build_watcher() constructs ScaffoldIssue`
- c0058 ..> c0048: `build_watcher() constructs WatchFactory`
- c0058 ..> c0048: `type in build_watcher`
- c0058 ..> c0058: `build_watcher() calls prepare_foreman_launch()`
- c0058 ..> c0058: `build_watcher() calls select_ticketing()`
- c0058 ..> c0065: `build_initialiser() constructs DeadlinePolicy`
- c0058 ..> c0065: `build_watcher() constructs DeadlinePolicy`
- c0058 ..> c0065: `type in build_initialiser`
- c0058 ..> c0065: `type in build_watcher`
- c0058 ..> c0067: `build_initialiser() constructs GitHubForge`
- c0058 ..> c0067: `build_watcher() constructs GitHubForge`
- c0058 ..> c0072: `prepare_foreman_launch() calls role_environment()`
- c0058 ..> c0073: `build_watcher() constructs ForgetfulPlanStore`
- c0058 ..> c0080: `build_watcher() constructs FactoryError`
- c0058 ..> c0080: `prepare_foreman_launch() constructs FactoryError`
- c0058 ..> c0080: `select_ticketing() constructs FactoryError`
- c0058 ..> c0088: `build_initialiser() constructs GitHubTicketing`
- c0058 ..> c0088: `build_watcher() calls check_ready()`
- c0058 ..> c0088: `select_ticketing() calls validate_source()`
- c0058 ..> c0092: `type in select_ticketing`
- c0058 ..> c0093: `build_initialiser() constructs GitRepositories`
- c0058 ..> c0093: `build_watcher() constructs GitRepositories`
- c0058 ..> c0095: `build_watcher() constructs GitWorktrees`
- c0059 ..> c0036: `type in agree_definition_of_done`
- c0059 ..> c0059: `agree_definition_of_done() calls _deployment_agreement()`
- c0059 ..> c0080: `_deployment_agreement() constructs FactoryError`
- c0059 ..> c0080: `agree_definition_of_done() constructs FactoryError`
- c0059 ..> c0082: `agree_definition_of_done() calls check_skill_file()`
- c0059 ..> c0082: `agree_definition_of_done() calls write_new()`
- c0060 --> c0036: `field config`
- c0060 --> c0075: `field connection`
- c0061 ..> c0000: `_initialise_locked() calls load()`
- c0061 ..> c0003: `_initialise() calls quote()`
- c0061 ..> c0003: `_launch_setup_foreman() calls quote()`
- c0061 ..> c0003: `_managed_watch_status() calls quote()`
- c0061 ..> c0003: `_select_model() calls quote()`
- c0061 ..> c0003: `_validate_setup_owner() calls quote()`
- c0061 ..> c0003: `_watch_locked() calls quote()`
- c0061 ..> c0004: `_foreman() calls hold()`
- c0061 ..> c0004: `_foreman() constructs WorkspaceWatchLease`
- c0061 ..> c0004: `_initialise() calls hold()`
- c0061 ..> c0004: `_initialise() constructs WorkspaceWatchLease`
- c0061 ..> c0004: `_watch() calls hold()`
- c0061 ..> c0004: `_watch() constructs WorkspaceWatchLease`
- c0061 ..> c0008: `_prompt_workers() calls update()`
- c0061 ..> c0009: `_managed_watch_status() calls unknown_status()`
- c0061 ..> c0009: `_watch_locked() calls observe_plain_watch()`
- c0061 ..> c0009: `_watch_status() calls plain_watch_status()`
- c0061 ..> c0009: `_watch_status() calls unknown_status()`
- c0061 ..> c0010: `_watch_locked() constructs BorrowedForemanTerminal`
- c0061 ..> c0015: `_watch_locked() calls run()`
- c0061 ..> c0017: `_change_managed_watch() calls request()`
- c0061 ..> c0017: `_finish_existing_setup() calls read_state()`
- c0061 ..> c0017: `_foreman() calls enter_terminal()`
- c0061 ..> c0017: `_foreman() calls read_state()`
- c0061 ..> c0017: `_foreman() calls request()`
- c0061 ..> c0017: `_foreman() calls start_owner()`
- c0061 ..> c0017: `_initialise() calls enter_terminal()`
- c0061 ..> c0017: `_initialise() calls request()`
- c0061 ..> c0017: `_initialise_locked() calls read_state()`
- c0061 ..> c0017: `_launch_setup_foreman() calls start_owner()`
- c0061 ..> c0017: `_managed_watch_status() calls read_state()`
- c0061 ..> c0017: `_managed_watch_status() calls request()`
- c0061 ..> c0017: `_offer_factory_launch() calls read_state()`
- c0061 ..> c0017: `_watch_locked() calls read_state()`
- c0061 ..> c0022: `_complete_setup() calls managed_memory_notice()`
- c0061 ..> c0022: `_complete_setup() calls record_completion()`
- c0061 ..> c0022: `_complete_setup() calls uses_browser_login()`
- c0061 ..> c0022: `_discover_worker_models() calls list_models()`
- c0061 ..> c0022: `_finish_existing_setup() calls choose_pi_home()`
- c0061 ..> c0022: `_finish_existing_setup() calls save_pi_choice()`
- c0061 ..> c0022: `_finish_existing_setup() calls selected_launch()`
- c0061 ..> c0022: `_foreman() calls managed_memory_notice()`
- c0061 ..> c0022: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0061 ..> c0022: `_select_model() calls list_models()`
- c0061 ..> c0022: `_select_project() calls create_project()`
- c0061 ..> c0022: `_select_project() calls projects()`
- c0061 ..> c0022: `_start_initial_setup() calls begin_setup()`
- c0061 ..> c0022: `_start_initial_setup() calls choose_pi_home()`
- c0061 ..> c0022: `_validate_initial_model() calls prepare_roles()`
- c0061 ..> c0022: `_watch_status() calls validate_completion()`
- c0061 ..> c0022: `_watch_status() constructs ForemanProfile`
- c0061 ..> c0028: `_configure_new_factory() constructs InitialAgentChoices`
- c0061 ..> c0028: `type in _configure_new_factory`
- c0061 ..> c0028: `type in _foreman_memory_choices`
- c0061 ..> c0028: `type in _owner_choices`
- c0061 ..> c0028: `type in _prompt_coordinator_choices`
- c0061 ..> c0028: `type in _validate_initial_model`
- c0061 ..> c0028: `type in _worker_choices`
- c0061 ..> c0029: `_start_initial_setup() calls validate_initial_agents()`
- c0061 ..> c0036: `type in _complete_setup`
- c0061 ..> c0036: `type in _configure_new_factory`
- c0061 ..> c0036: `type in _finish_existing_setup`
- c0061 ..> c0036: `type in _validate_initial_model`
- c0061 ..> c0037: `_connection() calls validate()`
- c0061 ..> c0039: `_complete_setup() calls check_foreman()`
- c0061 ..> c0039: `_configure_new_factory() calls configure()`
- c0061 ..> c0039: `_configure_new_factory() calls inspect()`
- c0061 ..> c0039: `_finish_existing_setup() calls initialise()`
- c0061 ..> c0039: `_initialise_locked() calls load_existing()`
- c0061 ..> c0039: `_launch_setup_foreman() calls check_foreman()`
- c0061 ..> c0039: `_prepare_foreman() calls prepare_foreman()`
- c0061 ..> c0039: `_start_initial_setup() calls initialise()`
- c0061 ..> c0039: `select_repositories() calls discover()`
- c0061 ..> c0039: `type in _complete_setup`
- c0061 ..> c0039: `type in _configure_new_factory`
- c0061 ..> c0039: `type in _discover_worker_models`
- c0061 ..> c0039: `type in _finish_existing_setup`
- c0061 ..> c0039: `type in _select_project`
- c0061 ..> c0039: `type in _start_initial_setup`
- c0061 ..> c0039: `type in _validate_initial_model`
- c0061 ..> c0039: `type in select_repositories`
- c0061 ..> c0058: `_foreman() calls prepare_foreman_launch()`
- c0061 ..> c0058: `_initialise_locked() calls build_initialiser()`
- c0061 ..> c0058: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0061 ..> c0058: `_watch_locked() calls build_watcher()`
- c0061 ..> c0059: `_finish_existing_setup() calls agree_definition_of_done()`
- c0061 ..> c0059: `_start_initial_setup() calls agree_definition_of_done()`
- c0061 ..> c0060: `_start_initial_setup() constructs _InitialSetupState`
- c0061 ..> c0060: `type in _discover_worker_models`
- c0061 ..> c0060: `type in _validate_initial_model`
- c0061 ..> c0061: `_complete_setup() calls _managed_rest_mapping_available()`
- c0061 ..> c0061: `_configure_new_factory() calls _prepare_foreman()`
- c0061 ..> c0061: `_configure_new_factory() calls _select_model()`
- c0061 ..> c0061: `_configure_new_factory() calls _select_numbered()`
- c0061 ..> c0061: `_configure_new_factory() calls select_repositories()`
- c0061 ..> c0061: `_connection() calls _check_existing_connection()`
- c0061 ..> c0061: `_discover_worker_models() calls _prepare_foreman()`
- c0061 ..> c0061: `_finish_existing_setup() calls _complete_setup()`
- c0061 ..> c0061: `_finish_existing_setup() calls _confirm_pi_home()`
- c0061 ..> c0061: `_finish_existing_setup() calls _connection()`
- c0061 ..> c0061: `_finish_existing_setup() calls _launch_setup_foreman()`
- c0061 ..> c0061: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0061 ..> c0061: `_foreman_memory_choices() calls _select_numbered()`
- c0061 ..> c0061: `_initialise() calls _initialise_locked()`
- c0061 ..> c0061: `_initialise() calls _offer_factory_launch()`
- c0061 ..> c0061: `_initialise_locked() calls _finish_existing_setup()`
- c0061 ..> c0061: `_initialise_locked() calls _start_initial_setup()`
- c0061 ..> c0061: `_initialise_locked() calls _validate_setup_owner()`
- c0061 ..> c0061: `_print_models() calls _safe_diagnostic()`
- c0061 ..> c0061: `_prompt_coordinator_choices() calls _select_numbered()`
- c0061 ..> c0061: `_prompt_worker() calls _select_numbered()`
- c0061 ..> c0061: `_prompt_workers() calls _prompt_worker()`
- c0061 ..> c0061: `_select_model() calls _print_models()`
- c0061 ..> c0061: `_select_model() calls _select_numbered()`
- c0061 ..> c0061: `_select_numbered() calls _safe_diagnostic()`
- c0061 ..> c0061: `_select_project() calls _listed_project_id()`
- c0061 ..> c0061: `_select_project() calls _safe_diagnostic()`
- c0061 ..> c0061: `_select_setup_route() calls _select_numbered()`
- c0061 ..> c0061: `_start_initial_setup() calls _complete_setup()`
- c0061 ..> c0061: `_start_initial_setup() calls _configure_new_factory()`
- c0061 ..> c0061: `_start_initial_setup() calls _confirm_pi_home()`
- c0061 ..> c0061: `_start_initial_setup() calls _connection()`
- c0061 ..> c0061: `_start_initial_setup() calls _foreman_memory_choices()`
- c0061 ..> c0061: `_start_initial_setup() calls _launch_setup_foreman()`
- c0061 ..> c0061: `_start_initial_setup() calls _owner_choices()`
- c0061 ..> c0061: `_start_initial_setup() calls _research_choices()`
- c0061 ..> c0061: `_start_initial_setup() calls _worker_choices()`
- c0061 ..> c0061: `_validate_initial_model() calls _prepare_foreman()`
- c0061 ..> c0061: `_validate_initial_model() calls _select_model()`
- c0061 ..> c0061: `_validate_initial_model() calls _select_project()`
- c0061 ..> c0061: `_watch() calls _change_managed_watch()`
- c0061 ..> c0061: `_watch() calls _watch_locked()`
- c0061 ..> c0061: `_watch() calls _watch_status()`
- c0061 ..> c0061: `_watch_locked() calls _choose_existing()`
- c0061 ..> c0061: `_watch_locked() calls _safe_diagnostic()`
- c0061 ..> c0061: `_watch_status() calls _managed_watch_status()`
- c0061 ..> c0061: `_worker_choices() calls _prompt_coordinator_choices()`
- c0061 ..> c0061: `_worker_choices() calls _prompt_workers()`
- c0061 ..> c0061: `_worker_choices() calls _select_setup_route()`
- c0061 ..> c0061: `_worker_choices() calls _worker_arguments()`
- c0061 ..> c0061: `main() calls _foreman()`
- c0061 ..> c0061: `main() calls _initialise()`
- c0061 ..> c0061: `main() calls _parse_arguments()`
- c0061 ..> c0061: `main() calls _safe_diagnostic()`
- c0061 ..> c0061: `main() calls _watch()`
- c0061 ..> c0062: `_select_numbered() calls parse_numbered_selection()`
- c0061 ..> c0063: `main() calls update_resources()`
- c0061 ..> c0064: `_foreman() calls load_configuration()`
- c0061 ..> c0064: `_watch_locked() calls load_configuration()`
- c0061 ..> c0064: `_watch_status() calls load_configuration()`
- c0061 ..> c0065: `main() constructs DeadlinePolicy`
- c0061 ..> c0065: `type in _finish_existing_setup`
- c0061 ..> c0065: `type in _foreman`
- c0061 ..> c0065: `type in _initialise`
- c0061 ..> c0065: `type in _initialise_locked`
- c0061 ..> c0065: `type in _start_initial_setup`
- c0061 ..> c0065: `type in _watch`
- c0061 ..> c0065: `type in _watch_locked`
- c0061 ..> c0065: `type in main`
- c0061 ..> c0075: `_connection() constructs ForgetfulConnection`
- c0061 ..> c0075: `type in _check_existing_connection`
- c0061 ..> c0075: `type in _configure_new_factory`
- c0061 ..> c0075: `type in _connection`
- c0061 ..> c0075: `type in _foreman_memory_choices`
- c0061 ..> c0075: `type in _managed_rest_mapping_available`
- c0061 ..> c0075: `type in _select_project`
- c0061 ..> c0080: `_change_managed_watch() constructs FactoryError`
- c0061 ..> c0080: `_check_existing_connection() constructs FactoryError`
- c0061 ..> c0080: `_choose_existing() constructs FactoryError`
- c0061 ..> c0080: `_configure_new_factory() constructs FactoryError`
- c0061 ..> c0080: `_finish_existing_setup() constructs FactoryError`
- c0061 ..> c0080: `_foreman() constructs FactoryError`
- c0061 ..> c0080: `_foreman_memory_choices() constructs FactoryError`
- c0061 ..> c0080: `_initialise() constructs FactoryError`
- c0061 ..> c0080: `_initialise_locked() constructs FactoryError`
- c0061 ..> c0080: `_install_missing() constructs FactoryError`
- c0061 ..> c0080: `_listed_project_id() constructs FactoryError`
- c0061 ..> c0080: `_prompt_coordinator_choices() constructs FactoryError`
- c0061 ..> c0080: `_prompt_worker() constructs FactoryError`
- c0061 ..> c0080: `_select_model() constructs FactoryError`
- c0061 ..> c0080: `_select_project() constructs FactoryError`
- c0061 ..> c0080: `_validate_setup_owner() constructs FactoryError`
- c0061 ..> c0080: `_watch_locked() constructs FactoryError`
- c0061 ..> c0080: `_worker_choices() constructs FactoryError`
- c0061 ..> c0080: `main() constructs FactoryError`
- c0061 ..> c0080: `select_repositories() constructs FactoryError`
- c0061 ..> c0082: `_discover_worker_models() calls check_real_path()`
- c0061 ..> c0087: `_watch_locked() calls watch_stop_scope()`
- c0062 ..> c0080: `parse_numbered_selection() constructs FactoryError`
- c0063 ..> c0004: `update_resources() calls hold()`
- c0063 ..> c0004: `update_resources() constructs WorkspaceWatchLease`
- c0063 ..> c0005: `update_resources() calls install()`
- c0063 ..> c0017: `update_resources() calls read_state()`
- c0063 ..> c0022: `update_resources() calls role_runtime_ready()`
- c0063 ..> c0022: `update_resources() calls validate_bundled_resources()`
- c0063 ..> c0022: `update_resources() constructs ForemanProfile`
- c0063 ..> c0024: `update_resources() calls apply_update()`
- c0063 ..> c0024: `update_resources() calls plan_update()`
- c0063 ..> c0063: `update_resources() calls _report()`
- c0063 ..> c0065: `type in update_resources`
- c0063 ..> c0080: `_report() constructs FactoryError`
- c0063 ..> c0080: `update_resources() constructs FactoryError`
- c0064 ..> c0000: `load_configuration() calls load()`
- c0064 ..> c0002: `load_configuration() constructs TomlConfigurationStore`
- c0064 ..> c0036: `type in load_configuration`
- c0064 ..> c0080: `load_configuration() constructs FactoryError`
- c0065 --> c0027: `field agentshell`
- c0065 ..> c0085: `__post_init__() calls positive_duration()`
- c0066 --> c0091: `field work_source`
- c0067 ..> c0068: `repository() constructs RepositoryRef`
- c0067 ..> c0068: `type in is_change_request`
- c0067 ..> c0068: `type in repository`
- c0067 ..> c0080: `repository() constructs FactoryError`
- c0069 ..> c0068: `type in is_change_request`
- c0069 ..> c0068: `type in repository`
- c0070 ..> c0017: `uses_browser_login() calls request()`
- c0070 ..> c0075: `type in uses_browser_login`
- c0071 ..> c0071: `call() calls command()`
- c0071 ..> c0071: `check() calls call()`
- c0071 ..> c0071: `check() calls command()`
- c0071 ..> c0071: `command() calls _environment()`
- c0071 ..> c0071: `create_project() calls call()`
- c0071 ..> c0071: `login() calls _environment()`
- c0071 ..> c0071: `projects() calls command()`
- c0071 ..> c0072: `_environment() calls role_environment()`
- c0071 ..> c0072: `check() calls _catalog_tools()`
- c0071 ..> c0075: `type in _environment`
- c0071 ..> c0075: `type in call`
- c0071 ..> c0075: `type in check`
- c0071 ..> c0075: `type in command`
- c0071 ..> c0075: `type in create_project`
- c0071 ..> c0075: `type in login`
- c0071 ..> c0075: `type in projects`
- c0071 ..> c0080: `check() constructs FactoryError`
- c0071 ..> c0080: `command() constructs FactoryError`
- c0071 ..> c0080: `create_project() constructs FactoryError`
- c0071 ..> c0080: `login() constructs FactoryError`
- c0071 ..> c0080: `projects() constructs FactoryError`
- c0071 ..> c0084: `command() calls run_owned()`
- c0071 ..> c0084: `login() calls run_owned()`
- c0071 ..> c0087: `command() calls check_watch_stop()`
- c0072 ..> c0008: `role_environment() calls update()`
- c0072 ..> c0075: `type in role_environment`
- c0072 ..> c0081: `role_environment() calls executable_path()`
- c0073 ..> c0022: `check() calls check()`
- c0073 ..> c0071: `__init__() constructs AgentForgetfulConnection`
- c0073 ..> c0071: `_call() calls call()`
- c0073 ..> c0073: `_read() calls _call()`
- c0073 ..> c0073: `_task() calls _read()`
- c0073 ..> c0073: `create_plan() calls _call()`
- c0073 ..> c0073: `create_task() calls _call()`
- c0073 ..> c0073: `get_plan() calls _read()`
- c0073 ..> c0073: `plans() calls _read()`
- c0073 ..> c0073: `plans() calls _rows()`
- c0073 ..> c0073: `tasks() calls _read()`
- c0073 ..> c0073: `tasks() calls _rows()`
- c0073 ..> c0073: `tasks() calls _task()`
- c0073 ..> c0073: `update_plan() calls _call()`
- c0073 ..> c0073: `update_task() calls _call()`
- c0073 ..> c0074: `_rows() calls _positive_id()`
- c0073 ..> c0074: `_task() calls _positive_id()`
- c0073 ..> c0074: `get_plan() calls _positive_id()`
- c0073 ..> c0075: `type in __init__`
- c0073 ..> c0078: `_read() constructs PlanningReadError`
- c0073 ..> c0078: `_rows() constructs PlanningReadError`
- c0073 ..> c0078: `_task() constructs PlanningReadError`
- c0073 ..> c0078: `get_plan() constructs PlanningReadError`
- c0075 ..> c0075: `validate() calls _validate_server()`
- c0075 ..> c0076: `_validate_server() calls loopback_host()`
- c0075 ..> c0080: `_validate_server() constructs FactoryError`
- c0075 ..> c0080: `validate() constructs FactoryError`
- c0075 ..> c0085: `_validate_server() calls nonblank()`
- c0075 ..> c0085: `validate() calls nonblank()`
- c0076 ..> c0075: `connection_from_mapping() calls validate()`
- c0076 ..> c0075: `connection_from_mapping() constructs ForgetfulConnection`
- c0076 ..> c0075: `type in connection_from_mapping`
- c0076 ..> c0080: `connection_from_mapping() constructs FactoryError`
- c0078 --|> c0080: `inherits`
- c0079 ..> c0015: `run_command() calls run()`
- c0079 ..> c0080: `run_command() constructs FactoryError`
- c0079 ..> c0087: `run_command() calls check_watch_stop()`
- c0082 ..> c0000: `read_generated_json() calls load()`
- c0082 ..> c0007: `_generated_parent() calls close()`
- c0082 ..> c0007: `check_skill_file() calls close()`
- c0082 ..> c0080: `_generated_parent() constructs FactoryError`
- c0082 ..> c0080: `check_real_path() constructs FactoryError`
- c0082 ..> c0080: `check_skill_file() constructs FactoryError`
- c0082 ..> c0080: `read_generated_json() constructs FactoryError`
- c0082 ..> c0080: `write_definition() constructs FactoryError`
- c0082 ..> c0080: `write_new() constructs FactoryError`
- c0082 ..> c0082: `_generated_parent() calls check_real_path()`
- c0082 ..> c0082: `check_skill_file() calls check_real_path()`
- c0082 ..> c0082: `read_generated_json() calls _generated_parent()`
- c0082 ..> c0082: `remove_generated() calls _generated_parent()`
- c0082 ..> c0082: `replace_generated_json() calls _generated_parent()`
- c0082 ..> c0082: `write_definition() calls read_generated_json()`
- c0082 ..> c0082: `write_definition() calls write_json()`
- c0082 ..> c0082: `write_json() calls write_new()`
- c0082 ..> c0082: `write_new() calls check_real_path()`
- c0084 ..> c0007: `_close_capture_streams() calls close()`
- c0084 ..> c0007: `_terminate_owned_process() calls wait()`
- c0084 ..> c0080: `run_owned() constructs FactoryError`
- c0084 ..> c0084: `_terminate_owned_process() calls _close_capture_streams()`
- c0084 ..> c0084: `run_owned() calls _terminate_owned_process()`
- c0084 ..> c0087: `run_owned() calls check_watch_stop()`
- c0085 ..> c0080: `nonblank() constructs FactoryError`
- c0087 ..> c0086: `watch_stop_scope() constructs WatchStop`
- c0088 ..> c0079: `_api() calls run_command()`
- c0088 ..> c0079: `check_ready() calls run_command()`
- c0088 ..> c0080: `_api() constructs FactoryError`
- c0088 ..> c0080: `_comments() constructs FactoryError`
- c0088 ..> c0080: `_validate_issue() constructs FactoryError`
- c0088 ..> c0080: `check_access() constructs FactoryError`
- c0088 ..> c0080: `check_ready() constructs FactoryError`
- c0088 ..> c0080: `create_label() constructs FactoryError`
- c0088 ..> c0080: `list_labels() constructs FactoryError`
- c0088 ..> c0080: `list_open() constructs FactoryError`
- c0088 ..> c0080: `validate_source() constructs FactoryError`
- c0088 ..> c0088: `_comments() calls _api()`
- c0088 ..> c0088: `_ticket() calls _comments()`
- c0088 ..> c0088: `_ticket() calls _milestone()`
- c0088 ..> c0088: `check_access() calls _api()`
- c0088 ..> c0088: `create_label() calls _api()`
- c0088 ..> c0088: `list_labels() calls _api()`
- c0088 ..> c0088: `list_open() calls _api()`
- c0088 ..> c0088: `list_open() calls _ticket()`
- c0088 ..> c0088: `list_open() calls _validate_issue()`
- c0088 ..> c0089: `list_labels() constructs Label`
- c0088 ..> c0089: `type in create_label`
- c0088 ..> c0089: `type in list_labels`
- c0088 ..> c0090: `_ticket() constructs Ticket`
- c0088 ..> c0090: `type in _ticket`
- c0088 ..> c0090: `type in list_open`
- c0088 ..> c0091: `type in _api`
- c0088 ..> c0091: `type in _comments`
- c0088 ..> c0091: `type in _ticket`
- c0088 ..> c0091: `type in _validate_issue`
- c0088 ..> c0091: `type in check_access`
- c0088 ..> c0091: `type in create_label`
- c0088 ..> c0091: `type in list_labels`
- c0088 ..> c0091: `type in list_open`
- c0088 ..> c0091: `type in validate_source`
- c0090 --> c0091: `field source`
- c0092 ..> c0089: `type in create_label`
- c0092 ..> c0089: `type in list_labels`
- c0092 ..> c0090: `type in list_open`
- c0092 ..> c0091: `type in check_access`
- c0092 ..> c0091: `type in create_label`
- c0092 ..> c0091: `type in list_labels`
- c0092 ..> c0091: `type in list_open`
- c0092 ..> c0091: `type in validate_source`
- c0093 ..> c0079: `origin() calls run_command()`
- c0093 ..> c0080: `origin() constructs FactoryError`
- c0093 ..> c0094: `origin() calls _resolve_repository()`
- c0094 ..> c0080: `_resolve_repository() constructs FactoryError`
- c0095 ..> c0003: `_network_git() calls quote()`
- c0095 ..> c0056: `begin_cleanup_cycle() calls clear()`
- c0095 ..> c0079: `_dispose() calls run_command()`
- c0095 ..> c0079: `_network_git() calls run_command()`
- c0095 ..> c0079: `_read_git() calls run_command()`
- c0095 ..> c0079: `ensure() calls run_command()`
- c0095 --> c0080: `field cleanup_defaults`
- c0095 ..> c0080: `ensure() constructs FactoryError`
- c0095 ..> c0087: `ensure() calls check_watch_stop()`
- c0095 ..> c0095: `_disposal_state() calls _repository_entries()`
- c0095 ..> c0095: `_disposal_state() calls _validate_disposal_origin()`
- c0095 ..> c0095: `_disposal_state() calls _validate_disposal_path()`
- c0095 ..> c0095: `_disposal_state() calls _validate_disposal_refs()`
- c0095 ..> c0095: `_disposal_state() calls _validate_registered_worktree()`
- c0095 ..> c0095: `_dispose() calls _disposal_state()`
- c0095 ..> c0095: `_dispose() calls _network_git()`
- c0095 ..> c0095: `_dispose() calls _network_read()`
- c0095 ..> c0095: `_dispose() calls _read_git()`
- c0095 ..> c0095: `_dispose() calls _repository_entries()`
- c0095 ..> c0095: `_dispose() calls _verify_local_ref_absent()`
- c0095 ..> c0095: `_inspect() calls _read_git()`
- c0095 ..> c0095: `_inspect() calls _repository_entries()`
- c0095 ..> c0095: `_inspect() calls _validate_registered_worktree()`
- c0095 ..> c0095: `_network_git() calls _read_git()`
- c0095 ..> c0095: `_network_read() calls _network_git()`
- c0095 ..> c0095: `_remote_default() calls _network_read()`
- c0095 ..> c0095: `_repository_entries() calls _read_git()`
- c0095 ..> c0095: `_validate_common_directory() calls _read_git()`
- c0095 ..> c0095: `_validate_disposal_origin() calls _read_git()`
- c0095 ..> c0095: `_validate_disposal_path() calls _read_git()`
- c0095 ..> c0095: `_validate_disposal_refs() calls _read_git()`
- c0095 ..> c0095: `_validate_disposal_refs() calls _remote_default()`
- c0095 ..> c0095: `_validate_registered_worktree() calls _validate_common_directory()`
- c0095 ..> c0095: `_validate_registered_worktree() calls _validate_registration()`
- c0095 ..> c0095: `_validate_registered_worktree() calls _validate_target_identity()`
- c0095 ..> c0095: `_validate_target_identity() calls _read_git()`
- c0095 ..> c0095: `_verify_local_ref_absent() calls _read_git()`
- c0095 ..> c0095: `_verify_removed() calls _repository_entries()`
- c0095 ..> c0095: `dispose() calls _dispose()`
- c0095 ..> c0095: `ensure() calls _inspect()`
- c0095 ..> c0095: `inspect() calls _inspect()`
- c0095 ..> c0095: `repository_identity() calls _read_git()`
- c0095 ..> c0095: `target_branch() calls _read_git()`
- c0095 ..> c0095: `verify_removed() calls _verify_removed()`
- c0095 ..> c0096: `_repository_entries() calls _worktree_entries()`
- c0095 ..> c0098: `_disposal_state() constructs WorktreeProblem`
- c0095 ..> c0098: `_dispose() constructs WorktreeProblem`
- c0095 ..> c0098: `_inspect() constructs WorktreeProblem`
- c0095 ..> c0098: `_network_read() constructs WorktreeProblem`
- c0095 ..> c0098: `_repository_entries() constructs WorktreeProblem`
- c0095 ..> c0098: `_validate_common_directory() constructs WorktreeProblem`
- c0095 ..> c0098: `_validate_disposal_origin() constructs WorktreeProblem`
- c0095 ..> c0098: `_validate_disposal_path() constructs WorktreeProblem`
- c0095 ..> c0098: `_validate_disposal_refs() constructs WorktreeProblem`
- c0095 ..> c0098: `_validate_registration() constructs WorktreeProblem`
- c0095 ..> c0098: `_validate_target_identity() constructs WorktreeProblem`
- c0095 ..> c0098: `_verify_local_ref_absent() constructs WorktreeProblem`
- c0095 ..> c0098: `_verify_removed() constructs WorktreeProblem`
- c0095 ..> c0098: `dispose() constructs WorktreeProblem`
- c0095 ..> c0099: `_read_git() constructs WorktreeReadError`
- c0095 ..> c0099: `ensure() constructs WorktreeReadError`
- c0095 ..> c0099: `inspect() constructs WorktreeReadError`
- c0095 ..> c0099: `repository_identity() constructs WorktreeReadError`
- c0095 ..> c0099: `target_branch() constructs WorktreeReadError`
- c0095 ..> c0099: `verify_removed() constructs WorktreeReadError`
- c0098 ..> c0000: `__init__() calls __init__()`
- c0098 --|> c0080: `inherits`
- c0099 --|> c0080: `inherits`

## Type key

- Type1: `FactoryConfiguration | None`
- Type2: `str | None`
- Type3: `dict[str, str]`
- Type4: `dict[str, str] | None`
- Type5: `tuple[Path, ...]`
- Type6: `tuple[int, int]`
- Type7: `dict | None`
- Type8: `Iterator[PlainWatchObservation | None]`
- Type9: `Callable[[str], None]`
- Type10: `object | None`
- Type11: `int | None`
- Type12: `tuple[Path, Path, int]`
- Type13: `subprocess.Popen | None`
- Type14: `dict[tuple[str, Path], list[str]]`
- Type15: `bool | None`
- Type16: `Path | None`
- Type17: `dict[str, bytes]`
- Type18: `tuple[str, ...]`
- Type19: `dict[Path, None]`
- Type20: `frozenset[tuple[int, int]]`
- Type21: `dict[int, int]`
- Type22: `tuple | None`
- Type23: `tuple[dict, dict] | None`
- Type24: `dict[int, list[dict]]`
- Type25: `list[dict] | None`
- Type26: `list[CompletedWork] | None`
- Type27: `CleanupState | None`
- Type28: `tuple[RepositoryReference, ...]`
- Type29: `ForgetfulConnection | None`
- Type30: `Callable[[list[str]], None]`
- Type31: `Callable[[str, str], bool]`
- Type32: `list[Path] | None`
- Type33: `list[str] | None`
- Type34: `dict[str, RepositoryReference]`
- Type35: `dict[TicketSource, tuple[Label, ...]]`
- Type36: `Callable[[], FactoryConfiguration | None]`
- Type37: `'CleanupSet'`
- Type38: `tuple[list[dict], list[dict]]`
- Type39: `tuple[Ticket, dict] | None`
- Type40: `Ticket | None`
- Type41: `tuple[int, ...] | None`
- Type42: `tuple[int, ...]`
- Type43: `Callable[[], bool]`
- Type44: `tuple[set[str], bool]`
- Type45: `tuple[TicketSource, ...]`
- Type46: `tuple[Ticket, ...]`
- Type47: `dict[str, Ticket]`
- Type48: `BlockedWork | None`
- Type49: `tuple[Ticket, ...] | None`
- Type50: `dict[str, BlockedWork]`
- Type51: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type52: `list[str] | tuple[str, ...]`
- Type53: `int | dict`
- Type54: `int | dict | str`
- Type55: `str | Path`
- Type56: `float | None`
- Type57: `tuple[Label, ...]`
- Type58: `list[tuple[int, str, str]]`
- Type59: `dict[str, list[str] | FactoryError]`
- Type60: `tuple[Path, list[dict]]`
- Type61: `tuple[Path, Path] | None`
- Type62: `tuple[Path, Path, dict | None]`

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
- Signature12: `-__init__(records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts,
  ticketing: Ticketing) unknown`
- Signature13: `-_claim_indexes(inventory: list[dict], plans: list[dict], tasks: dict[int,
  list[dict]], identities: dict[str, str], alerts: WatcherAlerts) tuple[dict, dict] | None`
- Signature14: `-_dispose(work: CompletedWork, mapping: dict, claims: dict, references: dict,
  identities: dict[str, str], alerts: WatcherAlerts, report: unknown) bool`
- Signature15: `-_mapping_identity(plan_id: int, reference: str, mapping: dict, workspace: str |
  None) CleanupSet`
- Signature16: `-__init__(planning: PlanStore, workspace: Path, config: FactoryConfiguration,
  repositories: LocalRepositories, forge: Forge) unknown`
- Signature17: `-__init__(tracking: Ticketing, storage: ConfigurationStore, repositories:
  LocalRepositories, forge: Forge, profile: ForemanProfile) unknown`
- Signature18: `-__init__(planning: PlanStore, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, forge: Forge) unknown`
- Signature19: `-_setup_ownership(plan_id: int, issue: Ticket, context: dict, initial_mappings:
  list[dict]) tuple[list[dict], list[dict]]`
- Signature20: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature21: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature22: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature23: `-__init__(tracking: Ticketing, terminal: ForemanTerminal, scaffold: ScaffoldIssue,
  cleanup: CleanupCompleted) unknown`
- Signature24: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature25: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature26: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature27: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature28: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature29: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature30: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Ticket, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature31: `-_poll_sources(sources: tuple[TicketSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature32: `-_process_source(source: TicketSource, issues: tuple[Ticket, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature33: `-_baseline_source(source: TicketSource, issues: tuple[Ticket, ...], state:
  _WatchState, report: Callable[[str], None]) None`
- Signature34: `-_repository_for_source(config: FactoryConfiguration, source: TicketSource)
  RepositoryReference`
- Signature35: `-_include_pending_lookups(source: TicketSource, current: dict[str, Ticket],
  pending_lookup: dict[str, Ticket]) None`
- Signature36: `-_process_issues(issues: tuple[Ticket, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature37: `-_process_issue(issue: Ticket, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature38: `-_handle_intake_repository_problem(issue: Ticket, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature39: `-_handle_intake_read_problem(issue: Ticket, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature40: `-_handle_intake_scaffold_problem(issue: Ticket, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature41: `-_complete_intake(issue: Ticket, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature42: `-_submit(issue: Ticket, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature43: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature44: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature45: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown, deadlines: DeadlinePolicy, observation: unknown) WatchFactory`
- Signature46: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown, term_grace: float) unknown`
- Signature47: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature48: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature49: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature50: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature51: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature52: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature53: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature54: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature55: `-_foreman_memory_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown, connection: ForgetfulConnection) InitialAgentChoices`
- Signature56: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature57: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature58: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int |
  dict`
- Signature59: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature60: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature61: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None, deadlines: DeadlinePolicy) int | dict`
- Signature62: `-_initialise_locked(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int | dict | str`
- Signature63: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown, deadlines: unknown) unknown`
- Signature64: `+update_resources(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int`
- Signature65: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature66: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool,
  term_grace: float) unknown`
- Signature67: `+run_owned(args: list[str], cwd: Path, env: dict[str, str], login: bool, timeout:
  float | None, term_grace: float) str`
- Signature68: `-_validate_registered_worktree(root: Path, target: Path, branch: str, path: str,
  match: dict) None`
- Signature69: `-_disposal_state(repository: str, branch: str, path: str, remote: str,
  target_branch: str) tuple[Path, Path, dict | None]`

## Extraction warnings

- `Unresolved or out-of-scope base: CleanupMarkerError -> ValueError`
- `Unresolved or out-of-scope base: CleanupReceipts -> Protocol`
- `Unresolved or out-of-scope base: ConfigurationStore -> Protocol`
- `Unresolved or out-of-scope base: FactoryError -> Exception`
- `Unresolved or out-of-scope base: ForemanProfile -> Protocol`
- `Unresolved or out-of-scope base: ForemanTerminal -> Protocol`
- `Unresolved or out-of-scope base: Forge -> Protocol`
- `Unresolved or out-of-scope base: LocalRepositories -> Protocol`
- `Unresolved or out-of-scope base: PlanStore -> Protocol`
- `Unresolved or out-of-scope base: Ticketing -> Protocol`
- `Unresolved or out-of-scope base: WatchLease -> Protocol`
- `Unresolved or out-of-scope base: Worktrees -> Protocol`
- `Unresolved or out-of-scope base: _WorkAction -> Enum`
