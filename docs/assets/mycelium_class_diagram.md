# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 115 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 5359. Type relationships removed: 106.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/contracts/agents.py`: 7 source occurrences (test-path).
- `tests/contracts/channels.py`: 5 source occurrences (test-path).
- `tests/contracts/forge.py`: 12 source occurrences (test-path).
- `tests/contracts/planning.py`: 16 source occurrences (test-path).
- `tests/contracts/runtime.py`: 6 source occurrences (test-path).
- `tests/contracts/ticketing.py`: 29 source occurrences (test-path).
- `tests/contracts/tools.py`: 7 source occurrences (test-path).
- `tests/deadline_support.py`: 2 source occurrences (test-path).
- `tests/fixtures/previous-pi-forgetful-factory.ts`: 18 source occurrences (test-path).
- `tests/lifecycle_support.py`: 21 source occurrences (test-path).
- `tests/poll_support.py`: 9 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_agent_definitions.py`: 21 source occurrences (test-path).
- `tests/test_agent_team_contract.py`: 5 source occurrences (test-path).
- `tests/test_architecture.py`: 26 source occurrences (test-path).
- `tests/test_assisted_lifecycle.py`: 16 source occurrences (test-path).
- `tests/test_assisted_review_fixes.py`: 20 source occurrences (test-path).
- `tests/test_assisted_setup.py`: 14 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_channel_contract.py`: 3 source occurrences (test-path).
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
- `tests/test_pi_runtime_install.py`: 4 source occurrences (test-path).
- `tests/test_planning_adapter.py`: 18 source occurrences (test-path).
- `tests/test_planning_contract.py`: 12 source occurrences (test-path).
- `tests/test_planning_setup.py`: 12 source occurrences (test-path).
- `tests/test_planning_watch.py`: 31 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_resource_update.py`: 18 source occurrences (test-path).
- `tests/test_review_regressions.py`: 54 source occurrences (test-path).
- `tests/test_runtime_host.py`: 8 source occurrences (test-path).
- `tests/test_saved_data.py`: 14 source occurrences (test-path).
- `tests/test_second_provider.py`: 8 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 24 source occurrences (test-path).
- `tests/test_ticketing.py`: 18 source occurrences (test-path).
- `tests/test_ticketing_contract.py`: 18 source occurrences (test-path).
- `tests/test_tool_installer_contract.py`: 21 source occurrences (test-path).
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
    class c0005["ObservedTerminal"] {
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
    class c0006["PlainWatchObservation"] {
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
    class c0007["src/forgetful_factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type2
        -_read_discovery(workspace: Path) dict
        +unknown_status(source: str, observation: str) dict
        +plain_watch_status(workspace: Path) Type3
        +observe_plain_watch(workspace: Path, report_unavailable: Type5) Type4
    }
    class c0008["BorrowedForemanTerminal"] {
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
    class c0009["SessionState"] {
        <<class>>
        +host: object
        +session: Type6
        +worker: Type7
        +worker_error: Type8
        +cleanup_known: bool
    }
    class c0010["src/forgetful_factory/agents/adapters/agentshell/controller.py"] {
        <<module>>
        +ready(session: unknown) None
        +interact(Signature1)
        +worker_exited(descriptor: unknown) None
        +resume_exit_observation(session: unknown) int
        +runtime() unknown
        +load_host(kind: str) unknown
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
    class c0011["src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0012["src/forgetful_factory/agents/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0013["ForemanOwner"] {
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
    class c0014["src/forgetful_factory/agents/adapters/agentshell/owner.py"] {
        <<module>>
        -_validate_target(target: unknown) None
        -_controller_event(line: bytes) dict
        -_watcher_request(line: bytes) dict
        -_acquire_owner_lock(directory: Path, workspace: Path) int
        -_prepare_owner_startup(workspace: Path) Type9
        +main(Signature7)
        -_report_startup_error(handover: unknown, error: unknown) None
        +entrypoint() None
    }
    class c0015["src/forgetful_factory/agents/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type3
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(Signature8)
    }
    class c0016["AgentShellRuntimeInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +project: unknown
        +term_grace: unknown
        -_inputs() Type10
        +absent() list[str]
        +unready() list[str]
        +ready() bool
        +describe(name: str) Type8
        +install(name: str) None
    }
    class c0017["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature9)
        +python: unknown
        +host: unknown
        +channel: unknown
        +environment: unknown
        +resources: unknown
        +prompt: unknown
        +cwd: unknown
        +model: unknown
        +effort: unknown
        +deadlines: unknown
        +process: Type12
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
    class c0018["src/forgetful_factory/agents/adapters/agentshell/tmux_host.py"] {
        <<module>>
        +retain_identity(session: unknown, reply: unknown) None
        +pin_worker(target: unknown) int
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
    class c0020["PiAgentTeam"] {
        <<class>>
        -__init__(Signature10)
        +workspace: unknown
        +term_grace: unknown
        +role_environment: unknown
        +missing_tools: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type3
        -_model_catalogs: Type15
        -_managed_memory_selected: Type16
        +prepare_setup_guidance() None
        +validate_setup(Signature11)
        +validate_bundled_resources(include_memory_extension: bool) None
        -_install_resources() None
        -_protect_runtime() None
        +prepare() None
        +save_pi_choice() None
        +prepare_roles(Signature12)
        +validate_worker_models(Signature13)
        +choose_pi_home(requested: Type8, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type17) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type8
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +begin_setup() None
        +validate_completion() None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0021["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(execution_enabled: bool, choices: unknown) None
        -_write_foreman_memory(choices: unknown) None
        -_write_agent(Signature14)
        +validate_guidance(execution_enabled: bool) None
    }
    class c0022["src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0023["src/forgetful_factory/agents/adapters/pi/native_home.py"] {
        <<module>>
        +saved_pi_home(workspace: Path) str
    }
    class c0024["ResourceUpdate"] {
        <<class>>
        +directory: Path
        +files: Type18
        +add: Type19
        +replace: Type19
        +edited: Type19
    }
    class c0025["src/forgetful_factory/agents/adapters/pi/role_resources.py"] {
        <<module>>
        -_digest(data: bytes) str
        +bundled_files() Type18
        +plan_update(directory: Path) ResourceUpdate
        -_back_up(update: ResourceUpdate, backups: Path) Path
        +apply_update(update: ResourceUpdate, backups: Path) Type17
    }
    class c0026["PiInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +directory: unknown
        +term_grace: unknown
        +absent() list[str]
        +unready() list[str]
        +ready(pi_home: str) bool
        +describe(name: str) Type8
        +install(name: str) None
    }
    class c0027["src/forgetful_factory/agents/adapters/pi/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type20) None
        -_walk_skill_directory(directory: Path, ancestors: Type21, files: Type20) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0028["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0029["AgentShellLifecycleDeadlines"] {
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
    class c0030["InitialAgentChoices"] {
        <<class>>
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +foreman_memory_enabled: bool
        +foreman_memory_model: Type8
        +feature_owner_agent_model: Type8
        +feature_owner_agent_effort: Type8
        +feature_owner_agent_harness: str
        +grill_me_skill: Type8
        +implementation_agent_model: Type8
        +implementation_agent_harness: Type8
        +implementation_agent_effort: Type8
        +review_agent_model: Type8
        +review_agent_harness: Type8
        +review_agent_effort: Type8
        +tdd_skill: Type8
        +implementation_skills: Type19
        +review_skills: Type19
        +research_agent_model: Type8
        +research_agent_harness: Type8
        +research_agent_effort: Type8
        +execution_enabled: bool
    }
    class c0031["src/forgetful_factory/agents/model.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type19
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0032["AgentTeam"] {
        <<class>>
        +prepare() None
        +prepare_setup_guidance() None
        +choose_pi_home(requested: Type8, confirm: Type22) str
        +save_pi_choice() None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type17) list[str]
        +prepare_roles(Signature12)
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type8
        +begin_setup() None
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +validate_completion() None
        +validate_bundled_resources(include_memory_extension: bool) None
    }
    class c0033["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0034["CleanupCompleted"] {
        <<class>>
        -__init__(Signature15)
        +records: unknown
        +ticketing: unknown
        +worktrees: unknown
        +owners: Type23
        +receipts: unknown
        +confirmed: set[CleanupSet]
        +cursor: Type24
        +poll(alerts: WatcherAlerts, report: unknown) None
        -_claim_indexes(Signature16)
        -_read_plans(inventory: list[dict], alerts: WatcherAlerts) Type28
        -_candidates(plans: list[dict], tasks: Type26, alerts: WatcherAlerts) Type29
        -_candidate(plan: dict, tasks: list[dict]) CompletedWork
        -_read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) None
        -_in_scope(plan: dict) bool
        -_repository_identities(alerts: WatcherAlerts) Type11
        -_keys(mapping: dict, identities: Type27) set[tuple]
        -_claims(tasks: list[dict], plan_id: int, claims: dict, identities: Type27) None
        -_task_mappings(task: dict) list[dict]
        -_validate_claim_mapping(mapping: object) None
        -_overlaps(mapping: dict, claims: dict) bool
        -_dispose(Signature17)
        -_order(work: CompletedWork, mapping: dict) tuple
        -_check_namespaces(mappings: list[dict], identities: Type27) None
        -_mapping_identity(Signature18)
        -_is_confirmed(plan_id: int, reference: str, mapping: dict, workspace: Type8) bool
        -_still_completed(work: CompletedWork) bool
    }
    class c0035["CompletedWork"] {
        <<class>>
        +plan_id: int
        +reference: str
        +task_id: int
        +mappings: list[dict]
    }
    class c0036["src/forgetful_factory/application/cleanup_completed.py"] {
        <<module>>
        -_claim_path(value: str) str
    }
    class c0037["CleanupMarkerError"] {
        <<class>>
    }
    class c0038["src/forgetful_factory/application/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict, forge: Forge, repository: RepositoryRef) Type30
    }
    class c0039["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type19
        +foreman_agent_file: str
        +repository: Type31
        +forgetful: Type32
        +execution_enabled: bool
    }
    class c0040["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type19
    }
    class c0041["FactoryRecords"] {
        <<class>>
        -__init__(Signature19)
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
    class c0042["InitialiseFactory"] {
        <<class>>
        -__init__(Signature20)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +forge: unknown
        +team: unknown
        +planning: unknown
        +tools: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type34, confirm: Type35) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type36, labels: Type37) Type1
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type38
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type39
        -_ensure_label(source: TicketSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type40, save: bool) list[str]
    }
    class c0043["src/forgetful_factory/application/initialise_factory.py"] {
        <<module>>
        +missing_tools(tools: Sequence[ToolInstaller]) list[str]
        -_reviewed_install(tools: Sequence[ToolInstaller], name: str) Type41
    }
    class c0044["CleanupReceipts"] {
        <<class>>
        +load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0045["CleanupSet"] {
        <<class>>
        +workspace: str
        +backend: str
        +plan_id: int
        +external_ref: str
        +repository: str
        +local_dir: str
        +branch: str
        +path: str
        +overlaps(other: Type42) bool
    }
    class c0046["ConfigurationStore"] {
        <<class>>
        +load() Type1
        +save(configuration: FactoryConfiguration) None
    }
    class c0047["ToolInstaller"] {
        <<class>>
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type8
        +install(name: str) None
    }
    class c0048["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0049["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature21)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +records: unknown
        +check() None
        +check_repository(repository: RepositoryReference) None
        +prepare(issue: Ticket) Type3
        -_repository(source: TicketSource) RepositoryReference
        -_initial_mappings(issue: Ticket) list[dict]
        +preflight(issue: Ticket) list[dict]
        -_prepare_plan(issue: Ticket, plan: dict, initial_mappings: list[dict]) Type3
        -_setup_ownership(Signature22)
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature23)
        +lookup(issue: Ticket) Type7
        -_create_plan(issue: Ticket) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type45, task_ids: Type46) Type44
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature24)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_is_unfinished_factory_plan(summary: dict, prefixes: set[str]) bool
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_validated_mapping(Signature25)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0050["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        +worktree_name(ticket: Ticket) str
    }
    class c0051["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type7
        +issue: Type45
        +task_ids: Type46
        +recovered: bool
        +setup_paths: Type19
        +setup_cause: Type8
    }
    class c0052["WatchFactory"] {
        <<class>>
        -__init__(Signature26)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +cleanup: unknown
        +run(Signature27)
        -_watch(Signature28)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type5) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature29)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type5) Type49
        -_recover_work(Signature30)
        -_handle_recovery_repository_problem(Signature31)
        -_handle_recovery_read_problem(Signature32)
        -_remember_task_ids(work: BlockedWork, task_ids: Type46) None
        -_complete_recovery(Signature33)
        -_poll_sources(Signature34)
        -_process_source(Signature35)
        -_baseline_source(Signature36)
        -_repository_for_source(Signature37)
        -_include_pending_lookups(Signature38)
        -_process_issues(Signature39)
        -_skip_issue(issue: Ticket, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature40)
        -_handle_intake_repository_problem(Signature41)
        -_handle_intake_read_problem(Signature42)
        -_handle_intake_scaffold_problem(Signature43)
        -_complete_intake(Signature44)
        -_sole_task_id(task_ids: Type46) Type7
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature45)
        -_read_issues(source: TicketSource, labels: Type19, alerts: WatcherAlerts) Type54
    }
    class c0053["_WatchState"] {
        <<class>>
        +seen: Type27
        +baseline: Type27
        +baselined: set[TicketSource]
        +blocked: Type55
        +pending_lookup: Type52
        +known: Type55
        +recovered: set[str]
        +pending_repositories: Type38
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0054["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0055["IntakeProblem"] {
        <<class>>
    }
    class c0056["RepositoryProblem"] {
        <<class>>
    }
    class c0057["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature46)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0058["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0059["UncertainScaffold"] {
        <<class>>
    }
    class c0060["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type27
        +last_diagnostic: Type27
        +clear(subject: str) None
        +send(Signature47)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0061["src/forgetful_factory/application/watcher_problems.py"] {
        <<module>>
        -_cleanup_recovery(code: str) str
    }
    class c0062["TerminalChannel"] {
        <<class>>
        -__init__(host: SessionHost) unknown
        +host: unknown
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0063["Channel"] {
        <<class>>
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0064["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_host() TmuxHost
        +build_channel() TerminalChannel
        +build_tools(Signature48)
        +build_team(workspace: Path, term_grace: float) PiAgentTeam
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +select_ticketing(config: FactoryConfiguration, command_timeout: float) Ticketing
        +build_watcher(Signature49)
        +prepare_foreman_launch(Signature50)
    }
    class c0065["src/forgetful_factory/cli/definition_of_done.py"] {
        <<module>>
        +agree_definition_of_done(workspace: Path, config: FactoryConfiguration) bool
        -_deployment_agreement(answer: str) str
    }
    class c0066["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0067["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature51)
        -_check_existing_connection(Signature52)
        -_connection(Signature53)
        -_prepare_foreman(Signature54)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type57, show_choices: bool, prompt: Type8) str
        -_select_model(Signature55)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_change_managed_watch(args: argparse.Namespace, workspace: Path) int
        -_managed_watch_status(workspace: Path) Type3
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
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type3) None
        -_finish_existing_setup(Signature62)
        -_discover_worker_models(Signature63)
        -_validate_initial_model(Signature64)
        -_start_initial_setup(Signature65)
        -_initialise_locked(Signature66)
        -_launch_setup_foreman(Signature67)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0068["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0069["src/forgetful_factory/cli/resource_update.py"] {
        <<module>>
        -_report(update: unknown, force: bool) None
        +update_resources(Signature68)
    }
    class c0070["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type60) FactoryConfiguration
    }
    class c0071["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0072["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: TicketSource
    }
    class c0073["GitHubForge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0074["RepositoryRef"] {
        <<class>>
        +forge: str
        +reference: str
    }
    class c0075["Forge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0076["src/forgetful_factory/planning/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0077["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +role: unknown
        +term_grace: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type27
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0078["src/forgetful_factory/planning/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature69)
        -_catalog_tools(catalog: object) dict
    }
    class c0079["ForgetfulInstall"] {
        <<class>>
        -__init__(workspace: Path, connection: ForgetfulConnection, term_grace: float) unknown
        +workspace: unknown
        +connection: unknown
        +directory: unknown
        +term_grace: unknown
        -_required() bool
        -_selected() Type8
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type8
        -_python() str
        +install(name: str) None
    }
    class c0080["ForgetfulPlanStore"] {
        <<class>>
        -__init__(Signature70)
        +cli: unknown
        +connection: unknown
        +execution_enabled: unknown
        +check() None
        -_call(tool: str, fields: unknown) dict
        -_read(tool: str, fields: unknown) dict
        +plans(external_ref: Type8) list[dict]
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
    class c0081["src/forgetful_factory/planning/adapters/forgetful/plan_store.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0082["ForgetfulSetup"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +term_grace: unknown
        -_native() AgentForgetfulConnection
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +prepare(connection: ForgetfulConnection) None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection, execution_enabled: bool) str
    }
    class c0083["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type8
        +server: Type8
        +project_id: Type7
        +validate() None
        -_validate_server() None
    }
    class c0084["src/forgetful_factory/planning/model.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type32
    }
    class c0085["PlanStore"] {
        <<class>>
        +check() None
        +plans(external_ref: Type8) list[dict]
        +get_plan(plan_id: int) dict
        +create_plan(fields: unknown) dict
        +update_plan(plan_id: int, fields: unknown) dict
        +tasks(plan_id: int) list[dict]
        +create_task(fields: unknown) dict
        +update_task(task_id: int, fields: unknown) dict
        +owns(plan: dict) bool
        +backend_identity() str
    }
    class c0086["PlanningReadError"] {
        <<class>>
    }
    class c0087["PlanningSetup"] {
        <<class>>
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +prepare(connection: ForgetfulConnection) None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection, execution_enabled: bool) str
    }
    class c0088["TmuxHost"] {
        <<class>>
        +spec() dict
        +how_to_attach(session_name: str) str
        +enter(target: dict) None
    }
    class c0089["TmuxInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +term_grace: unknown
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type8
        +install(name: str) None
    }
    class c0090["src/forgetful_factory/runtime/adapters/tmux.py"] {
        <<module>>
        +ubuntu_tmux() bool
    }
    class c0091["SessionHost"] {
        <<class>>
        +spec() dict
        +how_to_attach(session_name: str) str
        +enter(target: dict) None
    }
    class c0092["src/forgetful_factory/shared/command.py"] {
        <<module>>
        +run_command(arguments: list[str], timeout: float, env: Type11, stdin: Type7) str
    }
    class c0093["FactoryError"] {
        <<class>>
    }
    class c0094["src/forgetful_factory/shared/executables.py"] {
        <<module>>
        +executable_path(workspace: Path) str
    }
    class c0095["src/forgetful_factory/shared/installation.py"] {
        <<module>>
        +sync_fingerprint(inputs: Type61) str
        +runtime_ready(runtime: Path, inputs: Type61, probe: str, term_grace: float) bool
        +install_environment(extra: Type11) Type27
        +run_install(Signature71)
        +check_uv(workspace: Path, term_grace: float) None
        +require_manager(manager: str) None
        +install_locks(directory: Path, names: Type19) str
        +no_installer() FactoryError
    }
    class c0096["src/forgetful_factory/shared/resource_files.py"] {
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
    class c0097["src/forgetful_factory/shared/resources.py"] {
        <<module>>
        +resource_root() Path
    }
    class c0098["src/forgetful_factory/shared/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen, term_grace: float) None
        +run_owned(Signature72)
    }
    class c0099["src/forgetful_factory/shared/validation.py"] {
        <<module>>
        +nonblank(value: object, field: str) str
        +positive_duration(name: str, value: object) None
    }
    class c0100["WatchStop"] {
        <<class>>
        +requested: bool
        +interrupt(_signum: unknown, _frame: unknown) None
    }
    class c0101["src/forgetful_factory/shared/watch_stop.py"] {
        <<module>>
        +watch_stop_scope() unknown
        +check_watch_stop() None
    }
    class c0102["GitHubTicketing"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        -_api(source: TicketSource, suffix: str, #42;arguments: str) object
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type63
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type19) Type51
        -_ticket(source: TicketSource, item: dict) Ticket
        -_comments(source: TicketSource, number: int) Type64
        -_milestone(item: object) object
        -_validate_issue(source: TicketSource, item: dict) None
    }
    class c0103["Label"] {
        <<class>>
        +name: str
    }
    class c0104["Ticket"] {
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
    class c0105["TicketSource"] {
        <<class>>
        +provider: str
        +reference: str
        +id_prefix: str
    }
    class c0106["Ticketing"] {
        <<class>>
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type63
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type19) Type51
    }
    class c0107["GitRepositories"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0108["src/forgetful_factory/workspace/adapters/git/repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0109["GitWorktrees"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +cleanup_defaults: Type65
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        -_read_git(arguments: list[str]) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type66
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type67
        -_validate_registered_worktree(Signature73)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
        -_disposal_state(Signature74)
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
    class c0110["src/forgetful_factory/workspace/adapters/git/worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0111["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0112["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type8) unknown
        +code: unknown
        +paths: unknown
    }
    class c0113["WorktreeReadError"] {
        <<class>>
    }
    class c0114["Worktrees"] {
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
    c0000 ..> c0005 : _load() calls close()
    c0000 ..> c0045 : 3 relationships (see list)
    c0000 ..> c0093 : 2 relationships (see list)
    c0000 ..> c0096 : 2 relationships (see list)
    c0000 ..> c0101 : confirm() calls check_watch_stop()
    c0001 ..> c0045 : 2 relationships (see list)
    c0002 ..> c0000 : load() calls load()
    c0002 ..> c0003 : save() calls quote()
    c0002 ..> c0005 : 2 relationships (see list)
    c0002 ..> c0039 : 2 relationships (see list)
    c0002 ..> c0040 : load() calls from_mapping()
    c0002 ..> c0093 : 2 relationships (see list)
    c0004 ..> c0004 : hold() calls _hold_directory()
    c0004 ..> c0005 : _hold_directory() calls close()
    c0004 ..> c0093 : _hold_directory() constructs FactoryError
    c0005 ..> c0006 : 3 relationships (see list)
    c0005 ..> c0007 : __init__() calls unknown_status()
    c0005 ..> c0008 : 5 relationships (see list)
    c0005 ..> c0033 : type in __init__
    c0006 ..> c0005 : 2 relationships (see list)
    c0006 ..> c0006 : 9 relationships (see list)
    c0006 ..> c0007 : 6 relationships (see list)
    c0006 ..> c0093 : __enter__() constructs FactoryError
    c0006 ..> c0096 : 3 relationships (see list)
    c0007 ..> c0006 : 4 relationships (see list)
    c0007 ..> c0007 : 8 relationships (see list)
    c0007 ..> c0096 : _read_discovery() calls check_real_path()
    c0008 ..> c0005 : close() calls close()
    c0008 ..> c0008 : 2 relationships (see list)
    c0008 ..> c0093 : 2 relationships (see list)
    c0008 ..> c0101 : 2 relationships (see list)
    c0010 ..> c0005 : 5 relationships (see list)
    c0010 ..> c0009 : serve() constructs SessionState
    c0010 ..> c0010 : 16 relationships (see list)
    c0010 ..> c0018 : 2 relationships (see list)
    c0010 ..> c0080 : 4 relationships (see list)
    c0011 ..> c0093 : runtime_directory() constructs FactoryError
    c0011 ..> c0096 : runtime_directory() calls check_real_path()
    c0012 ..> c0020 : main() calls list_models()
    c0013 ..> c0003 : _apply_controller_problem() calls quote()
    c0013 ..> c0005 : 11 relationships (see list)
    c0013 ..> c0013 : 27 relationships (see list)
    c0013 ..> c0014 : 2 relationships (see list)
    c0013 ..> c0029 : 2 relationships (see list)
    c0013 ..> c0080 : 2 relationships (see list)
    c0013 ..> c0093 : 10 relationships (see list)
    c0013 ..> c0096 : save() calls replace_generated_json()
    c0014 ..> c0003 : _acquire_owner_lock() calls quote()
    c0014 ..> c0005 : 3 relationships (see list)
    c0014 ..> c0011 : _prepare_owner_startup() calls runtime_directory()
    c0014 ..> c0013 : 3 relationships (see list)
    c0014 ..> c0014 : 5 relationships (see list)
    c0014 ..> c0015 : _prepare_owner_startup() calls read_state()
    c0014 ..> c0080 : main() calls create_task()
    c0014 ..> c0093 : 3 relationships (see list)
    c0015 ..> c0003 : request() calls quote()
    c0015 ..> c0005 : 2 relationships (see list)
    c0015 ..> c0011 : 3 relationships (see list)
    c0015 ..> c0013 : start_owner() calls run()
    c0015 ..> c0015 : 3 relationships (see list)
    c0015 ..> c0029 : 2 relationships (see list)
    c0015 ..> c0088 : start_owner() calls spec()
    c0015 ..> c0091 : type in start_owner
    c0015 ..> c0093 : 4 relationships (see list)
    c0015 ..> c0096 : read_state() calls read_generated_json()
    c0016 ..> c0016 : 3 relationships (see list)
    c0016 ..> c0093 : install() constructs FactoryError
    c0016 ..> c0095 : 5 relationships (see list)
    c0017 ..> c0005 : close() calls close()
    c0017 ..> c0017 : 5 relationships (see list)
    c0017 ..> c0029 : 2 relationships (see list)
    c0017 ..> c0062 : startup_hint() calls how_to_reach()
    c0017 ..> c0063 : type in __init__
    c0017 ..> c0088 : start() calls spec()
    c0017 ..> c0091 : type in __init__
    c0017 ..> c0093 : 4 relationships (see list)
    c0017 ..> c0101 : 3 relationships (see list)
    c0018 ..> c0005 : pin_worker() calls close()
    c0019 ..> c0019 : 8 relationships (see list)
    c0019 ..> c0093 : 2 relationships (see list)
    c0019 ..> c0099 : 4 relationships (see list)
    c0020 ..> c0000 : choose_pi_home() calls confirm()
    c0020 ..> c0003 : require_pi_home() calls quote()
    c0020 ..> c0019 : selected_launch() calls foreman_launch()
    c0020 ..> c0020 : 20 relationships (see list)
    c0020 ..> c0021 : 4 relationships (see list)
    c0020 ..> c0023 : pi_home() calls saved_pi_home()
    c0020 ..> c0025 : _install_resources() calls bundled_files()
    c0020 ..> c0027 : selected_launch() calls selected_skill_files()
    c0020 ..> c0030 : 2 relationships (see list)
    c0020 ..> c0043 : validate_setup() calls missing_tools()
    c0020 ..> c0078 : list_models() calls role_environment()
    c0020 ..> c0083 : 7 relationships (see list)
    c0020 ..> c0093 : 13 relationships (see list)
    c0020 ..> c0094 : require_pi_home() calls executable_path()
    c0020 ..> c0096 : 10 relationships (see list)
    c0020 ..> c0098 : list_models() calls run_owned()
    c0021 ..> c0020 : prepare() calls prepare()
    c0021 ..> c0021 : 3 relationships (see list)
    c0021 ..> c0022 : prepare() calls selected_resources()
    c0021 ..> c0028 : __init__() constructs WorkerProfiles
    c0021 ..> c0093 : 4 relationships (see list)
    c0021 ..> c0096 : 5 relationships (see list)
    c0023 ..> c0093 : saved_pi_home() constructs FactoryError
    c0023 ..> c0096 : saved_pi_home() calls read_generated_json()
    c0025 ..> c0024 : 4 relationships (see list)
    c0025 ..> c0025 : 4 relationships (see list)
    c0025 ..> c0093 : 2 relationships (see list)
    c0025 ..> c0096 : plan_update() calls check_real_path()
    c0026 ..> c0023 : unready() calls saved_pi_home()
    c0026 ..> c0026 : unready() calls ready()
    c0026 ..> c0094 : 2 relationships (see list)
    c0026 ..> c0095 : 6 relationships (see list)
    c0026 ..> c0098 : ready() calls run_owned()
    c0027 ..> c0005 : _add_skill_file() calls close()
    c0027 ..> c0027 : 3 relationships (see list)
    c0027 ..> c0093 : 3 relationships (see list)
    c0028 ..> c0006 : prepare() calls update()
    c0028 ..> c0030 : type in prepare
    c0028 ..> c0096 : 3 relationships (see list)
    c0029 ..> c0099 : __post_init__() calls positive_duration()
    c0031 ..> c0030 : 3 relationships (see list)
    c0031 ..> c0031 : 4 relationships (see list)
    c0031 ..> c0093 : 5 relationships (see list)
    c0031 ..> c0099 : 4 relationships (see list)
    c0032 ..> c0030 : type in prepare_roles
    c0032 ..> c0083 : 4 relationships (see list)
    c0034 ..> c0000 : 2 relationships (see list)
    c0034 ..> c0005 : 5 relationships (see list)
    c0034 ..> c0006 : 4 relationships (see list)
    c0034 ..> c0034 : 27 relationships (see list)
    c0034 ..> c0035 : 6 relationships (see list)
    c0034 ..> c0036 : 6 relationships (see list)
    c0034 ..> c0041 : 9 relationships (see list)
    c0034 ..> c0044 : type in __init__
    c0034 --> c0045 : field confirmed
    c0034 ..> c0045 : 3 relationships (see list)
    c0034 ..> c0057 : 7 relationships (see list)
    c0034 ..> c0060 : 10 relationships (see list)
    c0034 ..> c0080 : 7 relationships (see list)
    c0034 ..> c0093 : type in _read_problem
    c0034 ..> c0102 : _in_scope() calls is_key()
    c0034 ..> c0106 : type in __init__
    c0034 ..> c0109 : 4 relationships (see list)
    c0034 ..> c0114 : type in __init__
    c0038 ..> c0037 : validate_cleanup_marker() constructs CleanupMarkerError
    c0038 ..> c0073 : validate_cleanup_marker() calls is_change_request()
    c0038 ..> c0074 : type in validate_cleanup_marker
    c0038 ..> c0075 : type in validate_cleanup_marker
    c0039 --> c0072 : field repository
    c0039 --> c0083 : field forgetful
    c0040 ..> c0039 : 3 relationships (see list)
    c0040 ..> c0040 : from_mapping() calls validate()
    c0040 ..> c0072 : from_mapping() constructs RepositoryReference
    c0040 ..> c0083 : validate() calls validate()
    c0040 ..> c0084 : from_mapping() calls connection_from_mapping()
    c0040 ..> c0093 : 2 relationships (see list)
    c0040 ..> c0099 : 2 relationships (see list)
    c0040 ..> c0105 : from_mapping() constructs TicketSource
    c0041 ..> c0039 : type in __init__
    c0041 ..> c0041 : 2 relationships (see list)
    c0041 ..> c0056 : 2 relationships (see list)
    c0041 ..> c0057 : 5 relationships (see list)
    c0041 ..> c0072 : 3 relationships (see list)
    c0041 ..> c0073 : check_source() calls repository()
    c0041 ..> c0074 : type in check_source
    c0041 ..> c0075 : type in __init__
    c0041 ..> c0080 : ownership() calls tasks()
    c0041 ..> c0085 : type in __init__
    c0041 ..> c0104 : 2 relationships (see list)
    c0041 ..> c0105 : snapshot() constructs TicketSource
    c0041 ..> c0107 : check_repository() calls origin()
    c0041 ..> c0111 : type in __init__
    c0042 ..> c0000 : 2 relationships (see list)
    c0042 ..> c0002 : initialise() calls save()
    c0042 ..> c0016 : prepare_foreman() calls install()
    c0042 ..> c0020 : prepare_foreman() calls prepare()
    c0042 ..> c0032 : type in __init__
    c0042 ..> c0039 : 6 relationships (see list)
    c0042 ..> c0040 : 3 relationships (see list)
    c0042 ..> c0042 : 3 relationships (see list)
    c0042 ..> c0043 : 2 relationships (see list)
    c0042 ..> c0046 : type in __init__
    c0042 ..> c0047 : type in __init__
    c0042 ..> c0049 : check_foreman() calls check()
    c0042 ..> c0072 : 2 relationships (see list)
    c0042 ..> c0073 : 2 relationships (see list)
    c0042 ..> c0075 : type in __init__
    c0042 ..> c0077 : check_foreman() calls login()
    c0042 ..> c0083 : 2 relationships (see list)
    c0042 ..> c0087 : type in __init__
    c0042 ..> c0093 : 5 relationships (see list)
    c0042 ..> c0102 : 4 relationships (see list)
    c0042 ..> c0103 : 2 relationships (see list)
    c0042 ..> c0105 : 3 relationships (see list)
    c0042 ..> c0106 : type in __init__
    c0042 ..> c0107 : 3 relationships (see list)
    c0042 ..> c0111 : type in __init__
    c0043 ..> c0016 : 3 relationships (see list)
    c0043 ..> c0047 : 2 relationships (see list)
    c0044 ..> c0045 : 2 relationships (see list)
    c0046 ..> c0039 : 2 relationships (see list)
    c0049 ..> c0006 : recover() calls snapshot()
    c0049 ..> c0038 : _ensure_mapping() calls validate_cleanup_marker()
    c0049 ..> c0039 : type in __init__
    c0049 ..> c0041 : 11 relationships (see list)
    c0049 ..> c0042 : preflight() calls inspect()
    c0049 ..> c0049 : 22 relationships (see list)
    c0049 ..> c0050 : _initial_mappings() calls worktree_name()
    c0049 ..> c0055 : preflight() constructs IntakeProblem
    c0049 ..> c0057 : 8 relationships (see list)
    c0049 ..> c0058 : 5 relationships (see list)
    c0049 ..> c0059 : 5 relationships (see list)
    c0049 ..> c0072 : 3 relationships (see list)
    c0049 ..> c0075 : type in __init__
    c0049 ..> c0077 : check() calls check()
    c0049 ..> c0080 : 12 relationships (see list)
    c0049 ..> c0085 : type in __init__
    c0049 ..> c0093 : _is_unfinished_factory_plan() constructs FactoryError
    c0049 ..> c0104 : 8 relationships (see list)
    c0049 ..> c0105 : type in _repository
    c0049 ..> c0109 : 3 relationships (see list)
    c0049 ..> c0111 : type in __init__
    c0049 ..> c0114 : type in __init__
    c0050 ..> c0104 : type in worktree_name
    c0051 --> c0104 : field issue
    c0052 ..> c0005 : 15 relationships (see list)
    c0052 ..> c0020 : _process_issue() calls prepare()
    c0052 ..> c0033 : type in __init__
    c0052 ..> c0034 : 2 relationships (see list)
    c0052 ..> c0039 : 4 relationships (see list)
    c0052 ..> c0041 : _check_pending_repositories() calls check_repository()
    c0052 ..> c0049 : 6 relationships (see list)
    c0052 ..> c0051 : 13 relationships (see list)
    c0052 ..> c0052 : 35 relationships (see list)
    c0052 ..> c0053 : 19 relationships (see list)
    c0052 ..> c0054 : 2 relationships (see list)
    c0052 ..> c0056 : 2 relationships (see list)
    c0052 ..> c0057 : 3 relationships (see list)
    c0052 ..> c0058 : 2 relationships (see list)
    c0052 ..> c0060 : 28 relationships (see list)
    c0052 ..> c0072 : 5 relationships (see list)
    c0052 ..> c0093 : _read_issues() constructs FactoryError
    c0052 ..> c0101 : 3 relationships (see list)
    c0052 ..> c0102 : _read_issues() calls list_open()
    c0052 ..> c0104 : 13 relationships (see list)
    c0052 ..> c0105 : 7 relationships (see list)
    c0052 ..> c0106 : type in __init__
    c0053 --> c0051 : 2 relationships (see list)
    c0053 --> c0072 : field pending_repositories
    c0053 --> c0104 : field pending_lookup
    c0053 --> c0105 : field baselined
    c0055 --|> c0057 : inherits
    c0056 --|> c0057 : inherits
    c0057 --|> c0093 : inherits
    c0058 --|> c0057 : inherits
    c0059 --|> c0057 : inherits
    c0060 ..> c0000 : __init__() calls __init__()
    c0060 ..> c0005 : send() calls send()
    c0060 ..> c0061 : send() calls _cleanup_recovery()
    c0060 ..> c0093 : type in send
    c0062 ..> c0088 : 2 relationships (see list)
    c0062 ..> c0091 : type in __init__
    c0064 ..> c0000 : build_watcher() constructs FileCleanupReceipts
    c0064 ..> c0002 : build_initialiser() constructs TomlConfigurationStore
    c0064 ..> c0005 : build_watcher() constructs ObservedTerminal
    c0064 ..> c0016 : build_tools() constructs AgentShellRuntimeInstall
    c0064 ..> c0017 : build_watcher() constructs AgentShellTerminal
    c0064 ..> c0020 : 6 relationships (see list)
    c0064 ..> c0026 : build_tools() constructs PiInstall
    c0064 ..> c0034 : build_watcher() constructs CleanupCompleted
    c0064 ..> c0039 : 3 relationships (see list)
    c0064 ..> c0042 : 2 relationships (see list)
    c0064 ..> c0043 : build_team() calls missing_tools()
    c0064 ..> c0049 : build_watcher() constructs ScaffoldIssue
    c0064 ..> c0052 : 2 relationships (see list)
    c0064 ..> c0062 : 2 relationships (see list)
    c0064 ..> c0064 : 8 relationships (see list)
    c0064 ..> c0071 : 4 relationships (see list)
    c0064 ..> c0073 : 2 relationships (see list)
    c0064 ..> c0078 : prepare_foreman_launch() calls role_environment()
    c0064 ..> c0079 : build_tools() constructs ForgetfulInstall
    c0064 ..> c0080 : build_watcher() constructs ForgetfulPlanStore
    c0064 ..> c0082 : build_initialiser() constructs ForgetfulSetup
    c0064 ..> c0083 : type in build_tools
    c0064 ..> c0088 : 2 relationships (see list)
    c0064 ..> c0089 : build_tools() constructs TmuxInstall
    c0064 ..> c0093 : 3 relationships (see list)
    c0064 ..> c0102 : 3 relationships (see list)
    c0064 ..> c0106 : type in select_ticketing
    c0064 ..> c0107 : 2 relationships (see list)
    c0064 ..> c0109 : build_watcher() constructs GitWorktrees
    c0065 ..> c0039 : type in agree_definition_of_done
    c0065 ..> c0065 : agree_definition_of_done() calls _deployment_agreement()
    c0065 ..> c0093 : 2 relationships (see list)
    c0065 ..> c0096 : 2 relationships (see list)
    c0066 --> c0039 : field config
    c0066 --> c0083 : field connection
    c0067 ..> c0000 : _initialise_locked() calls load()
    c0067 ..> c0003 : 6 relationships (see list)
    c0067 ..> c0004 : 6 relationships (see list)
    c0067 ..> c0006 : _prompt_workers() calls update()
    c0067 ..> c0007 : 4 relationships (see list)
    c0067 ..> c0008 : _watch_locked() constructs BorrowedForemanTerminal
    c0067 ..> c0013 : _watch_locked() calls run()
    c0067 ..> c0015 : 12 relationships (see list)
    c0067 ..> c0020 : 13 relationships (see list)
    c0067 ..> c0030 : 7 relationships (see list)
    c0067 ..> c0031 : _start_initial_setup() calls validate_initial_agents()
    c0067 ..> c0039 : 4 relationships (see list)
    c0067 ..> c0040 : _connection() calls validate()
    c0067 ..> c0042 : 17 relationships (see list)
    c0067 ..> c0064 : 9 relationships (see list)
    c0067 ..> c0065 : 2 relationships (see list)
    c0067 ..> c0066 : 3 relationships (see list)
    c0067 ..> c0067 : 55 relationships (see list)
    c0067 ..> c0068 : _select_numbered() calls parse_numbered_selection()
    c0067 ..> c0069 : main() calls update_resources()
    c0067 ..> c0070 : 3 relationships (see list)
    c0067 ..> c0071 : 9 relationships (see list)
    c0067 ..> c0076 : _complete_setup() calls uses_browser_login()
    c0067 ..> c0077 : 2 relationships (see list)
    c0067 ..> c0083 : 7 relationships (see list)
    c0067 ..> c0093 : 20 relationships (see list)
    c0067 ..> c0096 : _discover_worker_models() calls check_real_path()
    c0067 ..> c0101 : _watch_locked() calls watch_stop_scope()
    c0068 ..> c0093 : parse_numbered_selection() constructs FactoryError
    c0069 ..> c0004 : 2 relationships (see list)
    c0069 ..> c0010 : update_resources() calls ready()
    c0069 ..> c0015 : update_resources() calls read_state()
    c0069 ..> c0016 : 2 relationships (see list)
    c0069 ..> c0020 : update_resources() calls validate_bundled_resources()
    c0069 ..> c0025 : 2 relationships (see list)
    c0069 ..> c0064 : update_resources() calls build_team()
    c0069 ..> c0069 : update_resources() calls _report()
    c0069 ..> c0071 : type in update_resources
    c0069 ..> c0093 : 2 relationships (see list)
    c0070 ..> c0000 : load_configuration() calls load()
    c0070 ..> c0002 : load_configuration() constructs TomlConfigurationStore
    c0070 ..> c0039 : type in load_configuration
    c0070 ..> c0093 : load_configuration() constructs FactoryError
    c0071 --> c0029 : field agentshell
    c0071 ..> c0099 : __post_init__() calls positive_duration()
    c0072 --> c0105 : field work_source
    c0073 ..> c0074 : 3 relationships (see list)
    c0073 ..> c0093 : repository() constructs FactoryError
    c0075 ..> c0074 : 2 relationships (see list)
    c0076 ..> c0015 : uses_browser_login() calls request()
    c0076 ..> c0083 : type in uses_browser_login
    c0077 ..> c0077 : 7 relationships (see list)
    c0077 ..> c0078 : 2 relationships (see list)
    c0077 ..> c0083 : 7 relationships (see list)
    c0077 ..> c0093 : 5 relationships (see list)
    c0077 ..> c0098 : 2 relationships (see list)
    c0077 ..> c0101 : command() calls check_watch_stop()
    c0078 ..> c0006 : role_environment() calls update()
    c0078 ..> c0083 : type in role_environment
    c0078 ..> c0094 : role_environment() calls executable_path()
    c0079 ..> c0079 : 6 relationships (see list)
    c0079 ..> c0083 : type in __init__
    c0079 ..> c0093 : _python() constructs FactoryError
    c0079 ..> c0094 : _selected() calls executable_path()
    c0079 ..> c0095 : 7 relationships (see list)
    c0079 ..> c0098 : _python() calls run_owned()
    c0080 ..> c0049 : check() calls check()
    c0080 ..> c0077 : 2 relationships (see list)
    c0080 ..> c0080 : 12 relationships (see list)
    c0080 ..> c0081 : 3 relationships (see list)
    c0080 ..> c0083 : type in __init__
    c0080 ..> c0086 : 4 relationships (see list)
    c0082 ..> c0049 : check() calls check()
    c0082 ..> c0076 : uses_browser_login() calls uses_browser_login()
    c0082 ..> c0077 : 5 relationships (see list)
    c0082 ..> c0082 : 4 relationships (see list)
    c0082 ..> c0083 : 6 relationships (see list)
    c0083 ..> c0083 : validate() calls _validate_server()
    c0083 ..> c0084 : _validate_server() calls loopback_host()
    c0083 ..> c0093 : 2 relationships (see list)
    c0083 ..> c0099 : 2 relationships (see list)
    c0084 ..> c0083 : 3 relationships (see list)
    c0084 ..> c0093 : connection_from_mapping() constructs FactoryError
    c0086 --|> c0093 : inherits
    c0087 ..> c0083 : 6 relationships (see list)
    c0088 ..> c0013 : enter() calls run()
    c0088 ..> c0093 : enter() constructs FactoryError
    c0089 ..> c0090 : 2 relationships (see list)
    c0089 ..> c0093 : install() constructs FactoryError
    c0089 ..> c0094 : absent() calls executable_path()
    c0089 ..> c0095 : 2 relationships (see list)
    c0092 ..> c0013 : run_command() calls run()
    c0092 ..> c0093 : run_command() constructs FactoryError
    c0092 ..> c0101 : run_command() calls check_watch_stop()
    c0095 ..> c0093 : 6 relationships (see list)
    c0095 ..> c0095 : 4 relationships (see list)
    c0095 ..> c0096 : install_locks() calls write_new()
    c0095 ..> c0098 : 3 relationships (see list)
    c0096 ..> c0000 : read_generated_json() calls load()
    c0096 ..> c0005 : 2 relationships (see list)
    c0096 ..> c0093 : 6 relationships (see list)
    c0096 ..> c0096 : 9 relationships (see list)
    c0098 ..> c0005 : 2 relationships (see list)
    c0098 ..> c0093 : run_owned() constructs FactoryError
    c0098 ..> c0098 : 2 relationships (see list)
    c0098 ..> c0101 : run_owned() calls check_watch_stop()
    c0099 ..> c0093 : nonblank() constructs FactoryError
    c0101 ..> c0100 : watch_stop_scope() constructs WatchStop
    c0102 ..> c0092 : 2 relationships (see list)
    c0102 ..> c0093 : 9 relationships (see list)
    c0102 ..> c0102 : 9 relationships (see list)
    c0102 ..> c0103 : 3 relationships (see list)
    c0102 ..> c0104 : 3 relationships (see list)
    c0102 ..> c0105 : 9 relationships (see list)
    c0104 --> c0105 : field source
    c0106 ..> c0103 : 2 relationships (see list)
    c0106 ..> c0104 : type in list_open
    c0106 ..> c0105 : 5 relationships (see list)
    c0107 ..> c0092 : origin() calls run_command()
    c0107 ..> c0093 : origin() constructs FactoryError
    c0107 ..> c0108 : origin() calls _resolve_repository()
    c0108 ..> c0093 : _resolve_repository() constructs FactoryError
    c0109 ..> c0003 : _network_git() calls quote()
    c0109 ..> c0060 : begin_cleanup_cycle() calls clear()
    c0109 ..> c0092 : 4 relationships (see list)
    c0109 --> c0093 : field cleanup_defaults
    c0109 ..> c0093 : ensure() constructs FactoryError
    c0109 ..> c0101 : ensure() calls check_watch_stop()
    c0109 ..> c0109 : 35 relationships (see list)
    c0109 ..> c0110 : _repository_entries() calls _worktree_entries()
    c0109 ..> c0112 : 14 relationships (see list)
    c0109 ..> c0113 : 6 relationships (see list)
    c0112 ..> c0000 : __init__() calls __init__()
    c0112 --|> c0093 : inherits
    c0113 --|> c0093 : inherits
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
- c0005: `ObservedTerminal` — `src/forgetful_factory/adapters/watch_status.py`:252
- c0006: `PlainWatchObservation` — `src/forgetful_factory/adapters/watch_status.py`:129
- c0007: `src/forgetful_factory/adapters/watch_status.py` —
  `src/forgetful_factory/adapters/watch_status.py`:1
- c0008: `BorrowedForemanTerminal` —
  `src/forgetful_factory/agents/adapters/agentshell/borrowed_terminal.py`:10
- c0009: `SessionState` — `src/forgetful_factory/agents/adapters/agentshell/controller.py`:110
- c0010: `src/forgetful_factory/agents/adapters/agentshell/controller.py` —
  `src/forgetful_factory/agents/adapters/agentshell/controller.py`:1
- c0011: `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py` —
  `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py`:1
- c0012: `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py`:1
- c0013: `ForemanOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner.py`:104
- c0014: `src/forgetful_factory/agents/adapters/agentshell/owner.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner.py`:1
- c0015: `src/forgetful_factory/agents/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:1
- c0016: `AgentShellRuntimeInstall` —
  `src/forgetful_factory/agents/adapters/agentshell/runtime_install.py`:24
- c0017: `AgentShellTerminal` — `src/forgetful_factory/agents/adapters/agentshell/terminal.py`:17
- c0018: `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py` —
  `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py`:1
- c0019: `src/forgetful_factory/agents/adapters/pi/agent_definitions.py` —
  `src/forgetful_factory/agents/adapters/pi/agent_definitions.py`:1
- c0020: `PiAgentTeam` — `src/forgetful_factory/agents/adapters/pi/agent_team.py`:46
- c0021: `CoordinatorProfiles` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:29
- c0022: `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:1
- c0023: `src/forgetful_factory/agents/adapters/pi/native_home.py` —
  `src/forgetful_factory/agents/adapters/pi/native_home.py`:1
- c0024: `ResourceUpdate` — `src/forgetful_factory/agents/adapters/pi/role_resources.py`:39
- c0025: `src/forgetful_factory/agents/adapters/pi/role_resources.py` —
  `src/forgetful_factory/agents/adapters/pi/role_resources.py`:1
- c0026: `PiInstall` — `src/forgetful_factory/agents/adapters/pi/runtime_install.py`:22
- c0027: `src/forgetful_factory/agents/adapters/pi/selected_skills.py` —
  `src/forgetful_factory/agents/adapters/pi/selected_skills.py`:1
- c0028: `WorkerProfiles` — `src/forgetful_factory/agents/adapters/pi/worker_profiles.py`:16
- c0029: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/agents/model.py`:131
- c0030: `InitialAgentChoices` — `src/forgetful_factory/agents/model.py`:9
- c0031: `src/forgetful_factory/agents/model.py` — `src/forgetful_factory/agents/model.py`:1
- c0032: `AgentTeam` — `src/forgetful_factory/agents/ports.py`:21
- c0033: `ForemanTerminal` — `src/forgetful_factory/agents/ports.py`:9
- c0034: `CleanupCompleted` — `src/forgetful_factory/application/cleanup_completed.py`:37
- c0035: `CompletedWork` — `src/forgetful_factory/application/cleanup_completed.py`:22
- c0036: `src/forgetful_factory/application/cleanup_completed.py` —
  `src/forgetful_factory/application/cleanup_completed.py`:1
- c0037: `CleanupMarkerError` — `src/forgetful_factory/application/cleanup_marker.py`:11
- c0038: `src/forgetful_factory/application/cleanup_marker.py` —
  `src/forgetful_factory/application/cleanup_marker.py`:1
- c0039: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:11
- c0040: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0041: `FactoryRecords` — `src/forgetful_factory/application/factory_records.py`:16
- c0042: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:38
- c0043: `src/forgetful_factory/application/initialise_factory.py` —
  `src/forgetful_factory/application/initialise_factory.py`:1
- c0044: `CleanupReceipts` — `src/forgetful_factory/application/ports/cleanup_receipts.py`:24
- c0045: `CleanupSet` — `src/forgetful_factory/application/ports/cleanup_receipts.py`:7
- c0046: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0047: `ToolInstaller` — `src/forgetful_factory/application/ports/tool_installer.py`:4
- c0048: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0049: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:37
- c0050: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0051: `BlockedWork` — `src/forgetful_factory/application/watch_factory.py`:27
- c0052: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:59
- c0053: `_WatchState` — `src/forgetful_factory/application/watch_factory.py`:38
- c0054: `_WorkAction` — `src/forgetful_factory/application/watch_factory.py`:52
- c0055: `IntakeProblem` — `src/forgetful_factory/application/watcher_problems.py`:143
- c0056: `RepositoryProblem` — `src/forgetful_factory/application/watcher_problems.py`:139
- c0057: `ScaffoldProblem` — `src/forgetful_factory/application/watcher_problems.py`:119
- c0058: `ScaffoldReadProblem` — `src/forgetful_factory/application/watcher_problems.py`:135
- c0059: `UncertainScaffold` — `src/forgetful_factory/application/watcher_problems.py`:147
- c0060: `WatcherAlerts` — `src/forgetful_factory/application/watcher_problems.py`:151
- c0061: `src/forgetful_factory/application/watcher_problems.py` —
  `src/forgetful_factory/application/watcher_problems.py`:1
- c0062: `TerminalChannel` — `src/forgetful_factory/channels/adapters/terminal.py`:8
- c0063: `Channel` — `src/forgetful_factory/channels/ports.py`:4
- c0064: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0065: `src/forgetful_factory/cli/definition_of_done.py` —
  `src/forgetful_factory/cli/definition_of_done.py`:1
- c0066: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:752
- c0067: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0068: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0069: `src/forgetful_factory/cli/resource_update.py` —
  `src/forgetful_factory/cli/resource_update.py`:1
- c0070: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0071: `DeadlinePolicy` — `src/forgetful_factory/deadlines.py`:9
- c0072: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:7
- c0073: `GitHubForge` — `src/forgetful_factory/forge/adapters/github.py`:8
- c0074: `RepositoryRef` — `src/forgetful_factory/forge/model.py`:6
- c0075: `Forge` — `src/forgetful_factory/forge/ports.py`:6
- c0076: `src/forgetful_factory/planning/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/planning/adapters/forgetful/authentication.py`:1
- c0077: `AgentForgetfulConnection` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:55
- c0078: `src/forgetful_factory/planning/adapters/forgetful/connection.py` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:1
- c0079: `ForgetfulInstall` — `src/forgetful_factory/planning/adapters/forgetful/install.py`:26
- c0080: `ForgetfulPlanStore` — `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:13
- c0081: `src/forgetful_factory/planning/adapters/forgetful/plan_store.py` —
  `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:1
- c0082: `ForgetfulSetup` — `src/forgetful_factory/planning/adapters/forgetful/setup.py`:9
- c0083: `ForgetfulConnection` — `src/forgetful_factory/planning/model.py`:13
- c0084: `src/forgetful_factory/planning/model.py` — `src/forgetful_factory/planning/model.py`:1
- c0085: `PlanStore` — `src/forgetful_factory/planning/ports.py`:11
- c0086: `PlanningReadError` — `src/forgetful_factory/planning/ports.py`:7
- c0087: `PlanningSetup` — `src/forgetful_factory/planning/ports.py`:38
- c0088: `TmuxHost` — `src/forgetful_factory/runtime/adapters/tmux.py`:28
- c0089: `TmuxInstall` — `src/forgetful_factory/runtime/adapters/tmux.py`:54
- c0090: `src/forgetful_factory/runtime/adapters/tmux.py` —
  `src/forgetful_factory/runtime/adapters/tmux.py`:1
- c0091: `SessionHost` — `src/forgetful_factory/runtime/ports.py`:4
- c0092: `src/forgetful_factory/shared/command.py` — `src/forgetful_factory/shared/command.py`:1
- c0093: `FactoryError` — `src/forgetful_factory/shared/errors.py`:1
- c0094: `src/forgetful_factory/shared/executables.py` —
  `src/forgetful_factory/shared/executables.py`:1
- c0095: `src/forgetful_factory/shared/installation.py` —
  `src/forgetful_factory/shared/installation.py`:1
- c0096: `src/forgetful_factory/shared/resource_files.py` —
  `src/forgetful_factory/shared/resource_files.py`:1
- c0097: `src/forgetful_factory/shared/resources.py` — `src/forgetful_factory/shared/resources.py`:1
- c0098: `src/forgetful_factory/shared/sensitive_command.py` —
  `src/forgetful_factory/shared/sensitive_command.py`:1
- c0099: `src/forgetful_factory/shared/validation.py` —
  `src/forgetful_factory/shared/validation.py`:1
- c0100: `WatchStop` — `src/forgetful_factory/shared/watch_stop.py`:8
- c0101: `src/forgetful_factory/shared/watch_stop.py` —
  `src/forgetful_factory/shared/watch_stop.py`:1
- c0102: `GitHubTicketing` — `src/forgetful_factory/ticketing/adapters/github.py`:14
- c0103: `Label` — `src/forgetful_factory/ticketing/model.py`:17
- c0104: `Ticket` — `src/forgetful_factory/ticketing/model.py`:22
- c0105: `TicketSource` — `src/forgetful_factory/ticketing/model.py`:6
- c0106: `Ticketing` — `src/forgetful_factory/ticketing/ports.py`:6
- c0107: `GitRepositories` — `src/forgetful_factory/workspace/adapters/git/repositories.py`:15
- c0108: `src/forgetful_factory/workspace/adapters/git/repositories.py` —
  `src/forgetful_factory/workspace/adapters/git/repositories.py`:1
- c0109: `GitWorktrees` — `src/forgetful_factory/workspace/adapters/git/worktrees.py`:33
- c0110: `src/forgetful_factory/workspace/adapters/git/worktrees.py` —
  `src/forgetful_factory/workspace/adapters/git/worktrees.py`:1
- c0111: `LocalRepositories` — `src/forgetful_factory/workspace/ports.py`:8
- c0112: `WorktreeProblem` — `src/forgetful_factory/workspace/ports.py`:18
- c0113: `WorktreeReadError` — `src/forgetful_factory/workspace/ports.py`:14
- c0114: `Worktrees` — `src/forgetful_factory/workspace/ports.py`:27

## Relationships

- c0000 ..> c0000: `confirm() calls load()`
- c0000 ..> c0000: `load() calls _load()`
- c0000 ..> c0001: `_load() calls _resource()`
- c0000 ..> c0005: `_load() calls close()`
- c0000 ..> c0045: `type in _load`
- c0000 ..> c0045: `type in confirm`
- c0000 ..> c0045: `type in load`
- c0000 ..> c0093: `confirm() constructs FactoryError`
- c0000 ..> c0093: `load() constructs FactoryError`
- c0000 ..> c0096: `_load() calls check_real_path()`
- c0000 ..> c0096: `confirm() calls replace_generated_json()`
- c0000 ..> c0101: `confirm() calls check_watch_stop()`
- c0001 ..> c0045: `_resource() constructs CleanupSet`
- c0001 ..> c0045: `type in _resource`
- c0002 ..> c0000: `load() calls load()`
- c0002 ..> c0003: `save() calls quote()`
- c0002 ..> c0005: `load() calls close()`
- c0002 ..> c0005: `save() calls close()`
- c0002 ..> c0039: `type in load`
- c0002 ..> c0039: `type in save`
- c0002 ..> c0040: `load() calls from_mapping()`
- c0002 ..> c0093: `load() constructs FactoryError`
- c0002 ..> c0093: `save() constructs FactoryError`
- c0004 ..> c0004: `hold() calls _hold_directory()`
- c0004 ..> c0005: `_hold_directory() calls close()`
- c0004 ..> c0093: `_hold_directory() constructs FactoryError`
- c0005 ..> c0006: `close() calls update()`
- c0005 ..> c0006: `start() calls update()`
- c0005 ..> c0006: `type in __init__`
- c0005 ..> c0007: `__init__() calls unknown_status()`
- c0005 ..> c0008: `close() calls close()`
- c0005 ..> c0008: `send() calls send()`
- c0005 ..> c0008: `start() calls start()`
- c0005 ..> c0008: `startup_hint() calls startup_hint()`
- c0005 ..> c0008: `wait() calls wait()`
- c0005 ..> c0033: `type in __init__`
- c0006 ..> c0005: `__enter__() calls start()`
- c0006 ..> c0005: `_close_resources() calls close()`
- c0006 ..> c0006: `__enter__() calls _close_resources()`
- c0006 ..> c0006: `__enter__() calls snapshot()`
- c0006 ..> c0006: `__enter__() calls update()`
- c0006 ..> c0006: `__exit__() calls _close_resources()`
- c0006 ..> c0006: `__exit__() calls _publish_history()`
- c0006 ..> c0006: `__exit__() calls snapshot()`
- c0006 ..> c0006: `__exit__() calls update()`
- c0006 ..> c0006: `_serve() calls snapshot()`
- c0006 ..> c0006: `update() calls _publish_history()`
- c0006 ..> c0007: `__enter__() calls _discovery_path()`
- c0006 ..> c0007: `__enter__() calls _endpoint()`
- c0006 ..> c0007: `_publish_history() calls _discovery_path()`
- c0006 ..> c0007: `_publish_history() calls _read_discovery()`
- c0006 ..> c0007: `_serve() calls _frame()`
- c0006 ..> c0007: `_serve() calls _peer()`
- c0006 ..> c0093: `__enter__() constructs FactoryError`
- c0006 ..> c0096: `__enter__() calls check_real_path()`
- c0006 ..> c0096: `__enter__() calls replace_generated_json()`
- c0006 ..> c0096: `_publish_history() calls replace_generated_json()`
- c0007 ..> c0006: `observe_plain_watch() calls __enter__()`
- c0007 ..> c0006: `observe_plain_watch() calls __exit__()`
- c0007 ..> c0006: `observe_plain_watch() constructs PlainWatchObservation`
- c0007 ..> c0006: `type in observe_plain_watch`
- c0007 ..> c0007: `_frame() calls _observation_json()`
- c0007 ..> c0007: `_read_discovery() calls _discovery_path()`
- c0007 ..> c0007: `_read_discovery() calls _observation_json()`
- c0007 ..> c0007: `plain_watch_status() calls _endpoint()`
- c0007 ..> c0007: `plain_watch_status() calls _frame()`
- c0007 ..> c0007: `plain_watch_status() calls _peer()`
- c0007 ..> c0007: `plain_watch_status() calls _read_discovery()`
- c0007 ..> c0007: `plain_watch_status() calls unknown_status()`
- c0007 ..> c0096: `_read_discovery() calls check_real_path()`
- c0008 ..> c0005: `close() calls close()`
- c0008 ..> c0008: `send() calls _request()`
- c0008 ..> c0008: `start() calls _request()`
- c0008 ..> c0093: `_request() constructs FactoryError`
- c0008 ..> c0093: `wait() constructs FactoryError`
- c0008 ..> c0101: `_request() calls check_watch_stop()`
- c0008 ..> c0101: `wait() calls check_watch_stop()`
- c0010 ..> c0005: `close_session() calls close()`
- c0010 ..> c0005: `control() calls close()`
- c0010 ..> c0005: `control() calls wait()`
- c0010 ..> c0005: `resume_exit_observation() calls wait()`
- c0010 ..> c0005: `supervise_session() calls wait()`
- c0010 ..> c0009: `serve() constructs SessionState`
- c0010 ..> c0010: `build_shell() calls runtime()`
- c0010 ..> c0010: `control() calls serve()`
- c0010 ..> c0010: `interact() calls ready()`
- c0010 ..> c0010: `main() calls control()`
- c0010 ..> c0010: `open_session() calls capture_worker()`
- c0010 ..> c0010: `replace_failed_exit_task() calls resume_exit_observation()`
- c0010 ..> c0010: `serve() calls build_shell()`
- c0010 ..> c0010: `serve() calls close_session()`
- c0010 ..> c0010: `serve() calls load_host()`
- c0010 ..> c0010: `serve() calls open_session()`
- c0010 ..> c0010: `serve() calls supervise_session()`
- c0010 ..> c0010: `serve() calls validate_launch_config()`
- c0010 ..> c0010: `supervise_session() calls cancel_tasks()`
- c0010 ..> c0010: `supervise_session() calls interact()`
- c0010 ..> c0010: `supervise_session() calls replace_failed_exit_task()`
- c0010 ..> c0010: `supervise_session() calls worker_exited()`
- c0010 ..> c0018: `capture_worker() calls pin_worker()`
- c0010 ..> c0018: `supervise_session() calls retain_identity()`
- c0010 ..> c0080: `control() calls create_task()`
- c0010 ..> c0080: `main() calls create_task()`
- c0010 ..> c0080: `replace_failed_exit_task() calls create_task()`
- c0010 ..> c0080: `supervise_session() calls create_task()`
- c0011 ..> c0093: `runtime_directory() constructs FactoryError`
- c0011 ..> c0096: `runtime_directory() calls check_real_path()`
- c0012 ..> c0020: `main() calls list_models()`
- c0013 ..> c0003: `_apply_controller_problem() calls quote()`
- c0013 ..> c0005: `_await_readiness() calls wait()`
- c0013 ..> c0005: `_cleanup() calls close()`
- c0013 ..> c0005: `_close_controller() calls close()`
- c0013 ..> c0005: `_close_controller() calls wait()`
- c0013 ..> c0005: `_complete_handover() calls close()`
- c0013 ..> c0005: `control() calls close()`
- c0013 ..> c0005: `reap_watcher() calls wait()`
- c0013 ..> c0005: `relay() calls close()`
- c0013 ..> c0005: `run() calls close()`
- c0013 ..> c0005: `run() calls wait()`
- c0013 ..> c0005: `start_watcher() calls close()`
- c0013 ..> c0013: `_apply_controller_event() calls _apply_controller_problem()`
- c0013 ..> c0013: `_apply_controller_event() calls save()`
- c0013 ..> c0013: `_apply_controller_problem() calls save()`
- c0013 ..> c0013: `_apply_controller_problem() calls stop_watcher()`
- c0013 ..> c0013: `_cleanup() calls _close_controller()`
- c0013 ..> c0013: `_cleanup() calls _remove_control_socket()`
- c0013 ..> c0013: `_cleanup() calls stop_watcher()`
- c0013 ..> c0013: `_close_controller() calls save()`
- c0013 ..> c0013: `_finish_observation() calls save()`
- c0013 ..> c0013: `_reject_controller_event() calls save()`
- c0013 ..> c0013: `_reject_controller_event() calls stop_watcher()`
- c0013 ..> c0013: `_start_controller() calls observe()`
- c0013 ..> c0013: `control() calls start_watcher()`
- c0013 ..> c0013: `control() calls stop_watcher()`
- c0013 ..> c0013: `observe() calls _apply_controller_event()`
- c0013 ..> c0013: `observe() calls _finish_observation()`
- c0013 ..> c0013: `observe() calls _reject_controller_event()`
- c0013 ..> c0013: `observe() calls _validate_readiness()`
- c0013 ..> c0013: `relay() calls _relay_request()`
- c0013 ..> c0013: `run() calls _await_readiness()`
- c0013 ..> c0013: `run() calls _cleanup()`
- c0013 ..> c0013: `run() calls _complete_handover()`
- c0013 ..> c0013: `run() calls _start_controller()`
- c0013 ..> c0013: `run() calls save()`
- c0013 ..> c0013: `start_watcher() calls reap_watcher()`
- c0013 ..> c0013: `start_watcher() calls relay()`
- c0013 ..> c0013: `start_watcher() calls stop_watcher()`
- c0013 ..> c0014: `observe() calls _controller_event()`
- c0013 ..> c0014: `relay() calls _watcher_request()`
- c0013 ..> c0029: `__init__() constructs AgentShellLifecycleDeadlines`
- c0013 ..> c0029: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0013 ..> c0080: `_start_controller() calls create_task()`
- c0013 ..> c0080: `start_watcher() calls create_task()`
- c0013 ..> c0093: `_apply_controller_problem() constructs FactoryError`
- c0013 ..> c0093: `_await_readiness() constructs FactoryError`
- c0013 ..> c0093: `_complete_handover() constructs FactoryError`
- c0013 ..> c0093: `_finish_observation() constructs FactoryError`
- c0013 ..> c0093: `_reject_controller_event() constructs FactoryError`
- c0013 ..> c0093: `_relay_request() constructs FactoryError`
- c0013 ..> c0093: `control() constructs FactoryError`
- c0013 ..> c0093: `observe() constructs FactoryError`
- c0013 ..> c0093: `reap_watcher() constructs FactoryError`
- c0013 ..> c0093: `start_watcher() constructs FactoryError`
- c0013 ..> c0096: `save() calls replace_generated_json()`
- c0014 ..> c0003: `_acquire_owner_lock() calls quote()`
- c0014 ..> c0005: `_acquire_owner_lock() calls close()`
- c0014 ..> c0005: `_prepare_owner_startup() calls close()`
- c0014 ..> c0005: `entrypoint() calls close()`
- c0014 ..> c0011: `_prepare_owner_startup() calls runtime_directory()`
- c0014 ..> c0013: `entrypoint() calls run()`
- c0014 ..> c0013: `main() calls run()`
- c0014 ..> c0013: `main() constructs ForemanOwner`
- c0014 ..> c0014: `_controller_event() calls _validate_target()`
- c0014 ..> c0014: `_prepare_owner_startup() calls _acquire_owner_lock()`
- c0014 ..> c0014: `entrypoint() calls _prepare_owner_startup()`
- c0014 ..> c0014: `entrypoint() calls _report_startup_error()`
- c0014 ..> c0014: `entrypoint() calls main()`
- c0014 ..> c0015: `_prepare_owner_startup() calls read_state()`
- c0014 ..> c0080: `main() calls create_task()`
- c0014 ..> c0093: `_acquire_owner_lock() constructs FactoryError`
- c0014 ..> c0093: `_prepare_owner_startup() constructs FactoryError`
- c0014 ..> c0093: `_watcher_request() constructs FactoryError`
- c0015 ..> c0003: `request() calls quote()`
- c0015 ..> c0005: `start_owner() calls close()`
- c0015 ..> c0005: `start_owner() calls wait()`
- c0015 ..> c0011: `read_state() calls runtime_directory()`
- c0015 ..> c0011: `request() calls runtime_directory()`
- c0015 ..> c0011: `start_owner() calls runtime_directory()`
- c0015 ..> c0013: `start_owner() calls run()`
- c0015 ..> c0015: `request() calls _reply()`
- c0015 ..> c0015: `request() calls read_state()`
- c0015 ..> c0015: `start_owner() calls _reply()`
- c0015 ..> c0029: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0015 ..> c0029: `type in start_owner`
- c0015 ..> c0088: `start_owner() calls spec()`
- c0015 ..> c0091: `type in start_owner`
- c0015 ..> c0093: `_reply() constructs FactoryError`
- c0015 ..> c0093: `read_state() constructs FactoryError`
- c0015 ..> c0093: `request() constructs FactoryError`
- c0015 ..> c0093: `start_owner() constructs FactoryError`
- c0015 ..> c0096: `read_state() calls read_generated_json()`
- c0016 ..> c0016: `install() calls _inputs()`
- c0016 ..> c0016: `ready() calls _inputs()`
- c0016 ..> c0016: `unready() calls ready()`
- c0016 ..> c0093: `install() constructs FactoryError`
- c0016 ..> c0095: `install() calls check_uv()`
- c0016 ..> c0095: `install() calls no_installer()`
- c0016 ..> c0095: `install() calls run_install()`
- c0016 ..> c0095: `install() calls sync_fingerprint()`
- c0016 ..> c0095: `ready() calls runtime_ready()`
- c0017 ..> c0005: `close() calls close()`
- c0017 ..> c0017: `send() calls _read()`
- c0017 ..> c0017: `send() calls _write()`
- c0017 ..> c0017: `start() calls _read()`
- c0017 ..> c0017: `start() calls _write()`
- c0017 ..> c0017: `wait() calls _read()`
- c0017 ..> c0029: `__init__() constructs AgentShellLifecycleDeadlines`
- c0017 ..> c0029: `type in __init__`
- c0017 ..> c0062: `startup_hint() calls how_to_reach()`
- c0017 ..> c0063: `type in __init__`
- c0017 ..> c0088: `start() calls spec()`
- c0017 ..> c0091: `type in __init__`
- c0017 ..> c0093: `_read() constructs FactoryError`
- c0017 ..> c0093: `_write() constructs FactoryError`
- c0017 ..> c0093: `close() constructs FactoryError`
- c0017 ..> c0093: `start() constructs FactoryError`
- c0017 ..> c0101: `_read() calls check_watch_stop()`
- c0017 ..> c0101: `_write() calls check_watch_stop()`
- c0017 ..> c0101: `wait() calls check_watch_stop()`
- c0018 ..> c0005: `pin_worker() calls close()`
- c0019 ..> c0019: `_validate_agent() calls _local_selection()`
- c0019 ..> c0019: `_validate_roster() calls _local_selection()`
- c0019 ..> c0019: `_validate_roster() calls relative_path()`
- c0019 ..> c0019: `foreman_launch() calls read_definition()`
- c0019 ..> c0019: `foreman_launch() calls relative_path()`
- c0019 ..> c0019: `read_definition() calls _validate_agent()`
- c0019 ..> c0019: `read_definition() calls _validate_resources()`
- c0019 ..> c0019: `read_definition() calls _validate_roster()`
- c0019 ..> c0093: `foreman_launch() constructs FactoryError`
- c0019 ..> c0093: `read_definition() constructs FactoryError`
- c0019 ..> c0099: `_local_selection() calls nonblank()`
- c0019 ..> c0099: `_validate_agent() calls nonblank()`
- c0019 ..> c0099: `foreman_launch() calls nonblank()`
- c0019 ..> c0099: `relative_path() calls nonblank()`
- c0020 ..> c0000: `choose_pi_home() calls confirm()`
- c0020 ..> c0003: `require_pi_home() calls quote()`
- c0020 ..> c0019: `selected_launch() calls foreman_launch()`
- c0020 ..> c0020: `choose_pi_home() calls pi_home()`
- c0020 ..> c0020: `choose_pi_home() calls require_pi_home()`
- c0020 ..> c0020: `list_models() calls pi_home()`
- c0020 ..> c0020: `list_models() calls require_pi_home()`
- c0020 ..> c0020: `prepare() calls _install_resources()`
- c0020 ..> c0020: `prepare() calls _protect_runtime()`
- c0020 ..> c0020: `prepare() calls save_pi_choice()`
- c0020 ..> c0020: `prepare() calls validate_guidance()`
- c0020 ..> c0020: `prepare_roles() calls list_models()`
- c0020 ..> c0020: `prepare_roles() calls pi_home()`
- c0020 ..> c0020: `prepare_roles() calls prepare()`
- c0020 ..> c0020: `prepare_roles() calls validate_worker_models()`
- c0020 ..> c0020: `record_completion() calls selected_launch()`
- c0020 ..> c0020: `selected_launch() calls validate_setup()`
- c0020 ..> c0020: `validate_guidance() calls _read_guidance()`
- c0020 ..> c0020: `validate_setup() calls pi_home()`
- c0020 ..> c0020: `validate_setup() calls require_pi_home()`
- c0020 ..> c0020: `validate_setup() calls validate_bundled_resources()`
- c0020 ..> c0020: `validate_setup() calls validate_guidance()`
- c0020 ..> c0020: `validate_worker_models() calls list_models()`
- c0020 ..> c0021: `prepare_roles() calls validate_depth()`
- c0020 ..> c0021: `prepare_roles() constructs CoordinatorProfiles`
- c0020 ..> c0021: `validate_setup() calls validate_depth()`
- c0020 ..> c0021: `validate_setup() constructs CoordinatorProfiles`
- c0020 ..> c0023: `pi_home() calls saved_pi_home()`
- c0020 ..> c0025: `_install_resources() calls bundled_files()`
- c0020 ..> c0027: `selected_launch() calls selected_skill_files()`
- c0020 ..> c0030: `type in prepare_roles`
- c0020 ..> c0030: `type in validate_worker_models`
- c0020 ..> c0043: `validate_setup() calls missing_tools()`
- c0020 ..> c0078: `list_models() calls role_environment()`
- c0020 ..> c0083: `type in __init__`
- c0020 ..> c0083: `type in list_models`
- c0020 ..> c0083: `type in prepare_roles`
- c0020 ..> c0083: `type in record_completion`
- c0020 ..> c0083: `type in selected_launch`
- c0020 ..> c0083: `type in validate_setup`
- c0020 ..> c0083: `type in validate_worker_models`
- c0020 ..> c0093: `_install_resources() constructs FactoryError`
- c0020 ..> c0093: `_read_guidance() constructs FactoryError`
- c0020 ..> c0093: `choose_pi_home() constructs FactoryError`
- c0020 ..> c0093: `list_models() constructs FactoryError`
- c0020 ..> c0093: `prepare_roles() constructs FactoryError`
- c0020 ..> c0093: `prepare_setup_guidance() constructs FactoryError`
- c0020 ..> c0093: `require_pi_home() constructs FactoryError`
- c0020 ..> c0093: `selected_launch() constructs FactoryError`
- c0020 ..> c0093: `validate_bundled_resources() constructs FactoryError`
- c0020 ..> c0093: `validate_completion() constructs FactoryError`
- c0020 ..> c0093: `validate_guidance() constructs FactoryError`
- c0020 ..> c0093: `validate_setup() constructs FactoryError`
- c0020 ..> c0093: `validate_worker_models() constructs FactoryError`
- c0020 ..> c0094: `require_pi_home() calls executable_path()`
- c0020 ..> c0096: `_install_resources() calls write_new()`
- c0020 ..> c0096: `_protect_runtime() calls write_new()`
- c0020 ..> c0096: `begin_setup() calls remove_generated()`
- c0020 ..> c0096: `prepare() calls write_new()`
- c0020 ..> c0096: `prepare_roles() calls check_real_path()`
- c0020 ..> c0096: `prepare_setup_guidance() calls write_new()`
- c0020 ..> c0096: `record_completion() calls replace_generated_json()`
- c0020 ..> c0096: `save_pi_choice() calls write_json()`
- c0020 ..> c0096: `validate_bundled_resources() calls check_real_path()`
- c0020 ..> c0096: `validate_completion() calls read_generated_json()`
- c0020 ..> c0098: `list_models() calls run_owned()`
- c0021 ..> c0020: `prepare() calls prepare()`
- c0021 ..> c0021: `prepare() calls _write_agent()`
- c0021 ..> c0021: `prepare() calls _write_foreman_memory()`
- c0021 ..> c0021: `prepare() calls validate_guidance()`
- c0021 ..> c0022: `prepare() calls selected_resources()`
- c0021 ..> c0028: `__init__() constructs WorkerProfiles`
- c0021 ..> c0093: `_write_foreman_memory() constructs FactoryError`
- c0021 ..> c0093: `prepare() constructs FactoryError`
- c0021 ..> c0093: `validate_depth() constructs FactoryError`
- c0021 ..> c0093: `validate_guidance() constructs FactoryError`
- c0021 ..> c0096: `_write_agent() calls write_definition()`
- c0021 ..> c0096: `_write_foreman_memory() calls read_generated_json()`
- c0021 ..> c0096: `_write_foreman_memory() calls write_json()`
- c0021 ..> c0096: `prepare() calls check_skill_file()`
- c0021 ..> c0096: `prepare() calls write_new()`
- c0023 ..> c0093: `saved_pi_home() constructs FactoryError`
- c0023 ..> c0096: `saved_pi_home() calls read_generated_json()`
- c0025 ..> c0024: `plan_update() constructs ResourceUpdate`
- c0025 ..> c0024: `type in _back_up`
- c0025 ..> c0024: `type in apply_update`
- c0025 ..> c0024: `type in plan_update`
- c0025 ..> c0025: `apply_update() calls _back_up()`
- c0025 ..> c0025: `bundled_files() calls _digest()`
- c0025 ..> c0025: `plan_update() calls _digest()`
- c0025 ..> c0025: `plan_update() calls bundled_files()`
- c0025 ..> c0093: `bundled_files() constructs FactoryError`
- c0025 ..> c0093: `plan_update() constructs FactoryError`
- c0025 ..> c0096: `plan_update() calls check_real_path()`
- c0026 ..> c0023: `unready() calls saved_pi_home()`
- c0026 ..> c0026: `unready() calls ready()`
- c0026 ..> c0094: `absent() calls executable_path()`
- c0026 ..> c0094: `unready() calls executable_path()`
- c0026 ..> c0095: `install() calls install_locks()`
- c0026 ..> c0095: `install() calls no_installer()`
- c0026 ..> c0095: `install() calls require_manager()`
- c0026 ..> c0095: `install() calls run_install()`
- c0026 ..> c0095: `ready() calls install_environment()`
- c0026 ..> c0095: `ready() calls sync_fingerprint()`
- c0026 ..> c0098: `ready() calls run_owned()`
- c0027 ..> c0005: `_add_skill_file() calls close()`
- c0027 ..> c0027: `_walk_skill_directory() calls _add_skill_file()`
- c0027 ..> c0027: `selected_skill_files() calls _add_skill_file()`
- c0027 ..> c0027: `selected_skill_files() calls _walk_skill_directory()`
- c0027 ..> c0093: `_add_skill_file() constructs FactoryError`
- c0027 ..> c0093: `_walk_skill_directory() constructs FactoryError`
- c0027 ..> c0093: `selected_skill_files() constructs FactoryError`
- c0028 ..> c0006: `prepare() calls update()`
- c0028 ..> c0030: `type in prepare`
- c0028 ..> c0096: `prepare() calls check_skill_file()`
- c0028 ..> c0096: `prepare() calls write_definition()`
- c0028 ..> c0096: `prepare() calls write_new()`
- c0029 ..> c0099: `__post_init__() calls positive_duration()`
- c0031 ..> c0030: `type in _validate_foreman_memory`
- c0031 ..> c0030: `type in validate_initial_agents`
- c0031 ..> c0030: `type in validate_workers`
- c0031 ..> c0031: `validate_initial_agents() calls _validate_foreman_memory()`
- c0031 ..> c0031: `validate_initial_agents() calls validate_role_app()`
- c0031 ..> c0031: `validate_initial_agents() calls validate_workers()`
- c0031 ..> c0031: `validate_workers() calls validate_role_app()`
- c0031 ..> c0093: `_validate_foreman_memory() constructs FactoryError`
- c0031 ..> c0093: `skill_paths() constructs FactoryError`
- c0031 ..> c0093: `validate_initial_agents() constructs FactoryError`
- c0031 ..> c0093: `validate_role_app() constructs FactoryError`
- c0031 ..> c0093: `validate_workers() constructs FactoryError`
- c0031 ..> c0099: `_validate_foreman_memory() calls nonblank()`
- c0031 ..> c0099: `skill_paths() calls nonblank()`
- c0031 ..> c0099: `validate_initial_agents() calls nonblank()`
- c0031 ..> c0099: `validate_workers() calls nonblank()`
- c0032 ..> c0030: `type in prepare_roles`
- c0032 ..> c0083: `type in list_models`
- c0032 ..> c0083: `type in prepare_roles`
- c0032 ..> c0083: `type in record_completion`
- c0032 ..> c0083: `type in selected_launch`
- c0034 ..> c0000: `_dispose() calls confirm()`
- c0034 ..> c0000: `poll() calls load()`
- c0034 ..> c0005: `_candidates() calls send()`
- c0034 ..> c0005: `_dispose() calls send()`
- c0034 ..> c0005: `_read_problem() calls send()`
- c0034 ..> c0005: `_repository_identities() calls send()`
- c0034 ..> c0005: `poll() calls send()`
- c0034 ..> c0006: `_candidate() calls snapshot()`
- c0034 ..> c0006: `_candidate() calls update()`
- c0034 ..> c0006: `_check_namespaces() calls update()`
- c0034 ..> c0006: `_still_completed() calls snapshot()`
- c0034 ..> c0034: `_candidate() calls _keys()`
- c0034 ..> c0034: `_candidates() calls _candidate()`
- c0034 ..> c0034: `_candidates() calls _in_scope()`
- c0034 ..> c0034: `_check_namespaces() calls _keys()`
- c0034 ..> c0034: `_claim_indexes() calls _claims()`
- c0034 ..> c0034: `_claim_indexes() calls _read_problem()`
- c0034 ..> c0034: `_claims() calls _is_confirmed()`
- c0034 ..> c0034: `_claims() calls _keys()`
- c0034 ..> c0034: `_claims() calls _task_mappings()`
- c0034 ..> c0034: `_dispose() calls _check_namespaces()`
- c0034 ..> c0034: `_dispose() calls _keys()`
- c0034 ..> c0034: `_dispose() calls _mapping_identity()`
- c0034 ..> c0034: `_dispose() calls _overlaps()`
- c0034 ..> c0034: `_dispose() calls _read_problem()`
- c0034 ..> c0034: `_dispose() calls _still_completed()`
- c0034 ..> c0034: `_is_confirmed() calls _mapping_identity()`
- c0034 ..> c0034: `_read_plans() calls _read_problem()`
- c0034 ..> c0034: `_still_completed() calls _in_scope()`
- c0034 ..> c0034: `_task_mappings() calls _validate_claim_mapping()`
- c0034 ..> c0034: `poll() calls _candidates()`
- c0034 ..> c0034: `poll() calls _claim_indexes()`
- c0034 ..> c0034: `poll() calls _dispose()`
- c0034 ..> c0034: `poll() calls _in_scope()`
- c0034 ..> c0034: `poll() calls _is_confirmed()`
- c0034 ..> c0034: `poll() calls _order()`
- c0034 ..> c0034: `poll() calls _read_plans()`
- c0034 ..> c0034: `poll() calls _repository_identities()`
- c0034 ..> c0035: `_candidate() constructs CompletedWork`
- c0034 ..> c0035: `type in _candidate`
- c0034 ..> c0035: `type in _candidates`
- c0034 ..> c0035: `type in _dispose`
- c0034 ..> c0035: `type in _order`
- c0034 ..> c0035: `type in _still_completed`
- c0034 ..> c0036: `_candidate() calls _claim_path()`
- c0034 ..> c0036: `_claims() calls _claim_path()`
- c0034 ..> c0036: `_dispose() calls _claim_path()`
- c0034 ..> c0036: `_keys() calls _claim_path()`
- c0034 ..> c0036: `_overlaps() calls _claim_path()`
- c0034 ..> c0036: `_repository_identities() calls _claim_path()`
- c0034 ..> c0041: `_candidate() calls check_source()`
- c0034 ..> c0041: `_candidate() calls context()`
- c0034 ..> c0041: `_candidate() calls mapping_repository()`
- c0034 ..> c0041: `_candidate() calls ownership_records()`
- c0034 ..> c0041: `_dispose() calls check_repository()`
- c0034 ..> c0041: `_dispose() calls mapping_repository()`
- c0034 ..> c0041: `_still_completed() calls context()`
- c0034 ..> c0041: `_still_completed() calls ownership()`
- c0034 ..> c0041: `type in __init__`
- c0034 ..> c0044: `type in __init__`
- c0034 --> c0045: `field confirmed`
- c0034 ..> c0045: `_is_confirmed() calls overlaps()`
- c0034 ..> c0045: `_mapping_identity() constructs CleanupSet`
- c0034 ..> c0045: `type in _mapping_identity`
- c0034 ..> c0057: `_candidate() constructs ScaffoldProblem`
- c0034 ..> c0057: `_check_namespaces() constructs ScaffoldProblem`
- c0034 ..> c0057: `_dispose() constructs ScaffoldProblem`
- c0034 ..> c0057: `_is_confirmed() constructs ScaffoldProblem`
- c0034 ..> c0057: `_still_completed() constructs ScaffoldProblem`
- c0034 ..> c0057: `_task_mappings() constructs ScaffoldProblem`
- c0034 ..> c0057: `_validate_claim_mapping() constructs ScaffoldProblem`
- c0034 ..> c0060: `_dispose() calls clear()`
- c0034 ..> c0060: `_repository_identities() calls clear()`
- c0034 ..> c0060: `poll() calls clear()`
- c0034 ..> c0060: `type in _candidates`
- c0034 ..> c0060: `type in _claim_indexes`
- c0034 ..> c0060: `type in _dispose`
- c0034 ..> c0060: `type in _read_plans`
- c0034 ..> c0060: `type in _read_problem`
- c0034 ..> c0060: `type in _repository_identities`
- c0034 ..> c0060: `type in poll`
- c0034 ..> c0080: `_candidates() calls tasks()`
- c0034 ..> c0080: `_claim_indexes() calls tasks()`
- c0034 ..> c0080: `_in_scope() calls owns()`
- c0034 ..> c0080: `_mapping_identity() calls backend_identity()`
- c0034 ..> c0080: `_read_plans() calls get_plan()`
- c0034 ..> c0080: `_still_completed() calls get_plan()`
- c0034 ..> c0080: `poll() calls plans()`
- c0034 ..> c0093: `type in _read_problem`
- c0034 ..> c0102: `_in_scope() calls is_key()`
- c0034 ..> c0106: `type in __init__`
- c0034 ..> c0109: `_claims() calls repository_identity()`
- c0034 ..> c0109: `_dispose() calls dispose()`
- c0034 ..> c0109: `_repository_identities() calls repository_identity()`
- c0034 ..> c0109: `poll() calls begin_cleanup_cycle()`
- c0034 ..> c0114: `type in __init__`
- c0038 ..> c0037: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0038 ..> c0073: `validate_cleanup_marker() calls is_change_request()`
- c0038 ..> c0074: `type in validate_cleanup_marker`
- c0038 ..> c0075: `type in validate_cleanup_marker`
- c0039 --> c0072: `field repository`
- c0039 --> c0083: `field forgetful`
- c0040 ..> c0039: `from_mapping() constructs FactoryConfiguration`
- c0040 ..> c0039: `type in from_mapping`
- c0040 ..> c0039: `type in validate`
- c0040 ..> c0040: `from_mapping() calls validate()`
- c0040 ..> c0072: `from_mapping() constructs RepositoryReference`
- c0040 ..> c0083: `validate() calls validate()`
- c0040 ..> c0084: `from_mapping() calls connection_from_mapping()`
- c0040 ..> c0093: `from_mapping() constructs FactoryError`
- c0040 ..> c0093: `validate() constructs FactoryError`
- c0040 ..> c0099: `unique_labels() calls nonblank()`
- c0040 ..> c0099: `validate() calls nonblank()`
- c0040 ..> c0105: `from_mapping() constructs TicketSource`
- c0041 ..> c0039: `type in __init__`
- c0041 ..> c0041: `check_repository() calls check_source()`
- c0041 ..> c0041: `ownership() calls ownership_records()`
- c0041 ..> c0056: `check_repository() constructs RepositoryProblem`
- c0041 ..> c0056: `check_source() constructs RepositoryProblem`
- c0041 ..> c0057: `active() constructs ScaffoldProblem`
- c0041 ..> c0057: `context() constructs ScaffoldProblem`
- c0041 ..> c0057: `mapping_repository() constructs ScaffoldProblem`
- c0041 ..> c0057: `ownership_records() constructs ScaffoldProblem`
- c0041 ..> c0057: `snapshot() constructs ScaffoldProblem`
- c0041 ..> c0072: `type in check_repository`
- c0041 ..> c0072: `type in check_source`
- c0041 ..> c0072: `type in mapping_repository`
- c0041 ..> c0073: `check_source() calls repository()`
- c0041 ..> c0074: `type in check_source`
- c0041 ..> c0075: `type in __init__`
- c0041 ..> c0080: `ownership() calls tasks()`
- c0041 ..> c0085: `type in __init__`
- c0041 ..> c0104: `snapshot() constructs Ticket`
- c0041 ..> c0104: `type in snapshot`
- c0041 ..> c0105: `snapshot() constructs TicketSource`
- c0041 ..> c0107: `check_repository() calls origin()`
- c0041 ..> c0111: `type in __init__`
- c0042 ..> c0000: `load_existing() calls load()`
- c0042 ..> c0000: `prepare_foreman() calls confirm()`
- c0042 ..> c0002: `initialise() calls save()`
- c0042 ..> c0016: `prepare_foreman() calls install()`
- c0042 ..> c0020: `prepare_foreman() calls prepare()`
- c0042 ..> c0032: `type in __init__`
- c0042 ..> c0039: `configure() constructs FactoryConfiguration`
- c0042 ..> c0039: `type in _preflight`
- c0042 ..> c0039: `type in check_foreman`
- c0042 ..> c0039: `type in configure`
- c0042 ..> c0039: `type in initialise`
- c0042 ..> c0039: `type in load_existing`
- c0042 ..> c0040: `_preflight() calls validate()`
- c0042 ..> c0040: `configure() calls unique_labels()`
- c0042 ..> c0040: `load_existing() calls unique_labels()`
- c0042 ..> c0042: `configure() calls inspect()`
- c0042 ..> c0042: `initialise() calls _ensure_label()`
- c0042 ..> c0042: `initialise() calls _preflight()`
- c0042 ..> c0043: `prepare_foreman() calls _reviewed_install()`
- c0042 ..> c0043: `prepare_foreman() calls missing_tools()`
- c0042 ..> c0046: `type in __init__`
- c0042 ..> c0047: `type in __init__`
- c0042 ..> c0049: `check_foreman() calls check()`
- c0042 ..> c0072: `inspect() constructs RepositoryReference`
- c0042 ..> c0072: `type in inspect`
- c0042 ..> c0073: `_preflight() calls repository()`
- c0042 ..> c0073: `inspect() calls repository()`
- c0042 ..> c0075: `type in __init__`
- c0042 ..> c0077: `check_foreman() calls login()`
- c0042 ..> c0083: `type in __init__`
- c0042 ..> c0083: `type in prepare_foreman`
- c0042 ..> c0087: `type in __init__`
- c0042 ..> c0093: `_preflight() constructs FactoryError`
- c0042 ..> c0093: `initialise() constructs FactoryError`
- c0042 ..> c0093: `inspect() constructs FactoryError`
- c0042 ..> c0093: `load_existing() constructs FactoryError`
- c0042 ..> c0093: `prepare_foreman() constructs FactoryError`
- c0042 ..> c0102: `_ensure_label() calls create_label()`
- c0042 ..> c0102: `_preflight() calls check_access()`
- c0042 ..> c0102: `_preflight() calls list_labels()`
- c0042 ..> c0102: `_preflight() calls validate_source()`
- c0042 ..> c0103: `_ensure_label() constructs Label`
- c0042 ..> c0103: `type in _preflight`
- c0042 ..> c0105: `inspect() constructs TicketSource`
- c0042 ..> c0105: `type in _ensure_label`
- c0042 ..> c0105: `type in _preflight`
- c0042 ..> c0106: `type in __init__`
- c0042 ..> c0107: `_preflight() calls origin()`
- c0042 ..> c0107: `discover() calls discover()`
- c0042 ..> c0107: `inspect() calls origin()`
- c0042 ..> c0111: `type in __init__`
- c0043 ..> c0016: `_reviewed_install() calls describe()`
- c0043 ..> c0016: `missing_tools() calls absent()`
- c0043 ..> c0016: `missing_tools() calls unready()`
- c0043 ..> c0047: `type in _reviewed_install`
- c0043 ..> c0047: `type in missing_tools`
- c0044 ..> c0045: `type in confirm`
- c0044 ..> c0045: `type in load`
- c0046 ..> c0039: `type in load`
- c0046 ..> c0039: `type in save`
- c0049 ..> c0006: `recover() calls snapshot()`
- c0049 ..> c0038: `_ensure_mapping() calls validate_cleanup_marker()`
- c0049 ..> c0039: `type in __init__`
- c0049 ..> c0041: `__init__() constructs FactoryRecords`
- c0049 ..> c0041: `_create_ownership() calls ownership()`
- c0049 ..> c0041: `_ensure_mapping() calls check_source()`
- c0049 ..> c0041: `_ensure_worktrees() calls mapping_repository()`
- c0049 ..> c0041: `_prepare_plan() calls active()`
- c0049 ..> c0041: `_prepare_plan() calls context()`
- c0049 ..> c0041: `_setup_ownership() calls ownership()`
- c0049 ..> c0041: `check_repository() calls check_repository()`
- c0049 ..> c0041: `recover() calls active()`
- c0049 ..> c0041: `recover() calls context()`
- c0049 ..> c0041: `recover() calls ownership()`
- c0049 ..> c0042: `preflight() calls inspect()`
- c0049 ..> c0049: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0049 ..> c0049: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0049 ..> c0049: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0049 ..> c0049: `_initial_mappings() calls _repository()`
- c0049 ..> c0049: `_prepare_plan() calls _create_ownership()`
- c0049 ..> c0049: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0049 ..> c0049: `_prepare_plan() calls _setup_ownership()`
- c0049 ..> c0049: `preflight() calls _initial_mappings()`
- c0049 ..> c0049: `preflight() calls _repository()`
- c0049 ..> c0049: `preflight() calls check_repository()`
- c0049 ..> c0049: `prepare() calls _create_plan()`
- c0049 ..> c0049: `prepare() calls _prepare_plan()`
- c0049 ..> c0049: `prepare() calls lookup()`
- c0049 ..> c0049: `prepare() calls preflight()`
- c0049 ..> c0049: `prepare() calls recover()`
- c0049 ..> c0049: `recover() calls _ensure_worktrees()`
- c0049 ..> c0049: `recover() calls _recovery_plan()`
- c0049 ..> c0049: `recover() calls _repository()`
- c0049 ..> c0049: `recover() calls _sole_recovery_owner()`
- c0049 ..> c0049: `recover() calls _validate_recovery_candidates()`
- c0049 ..> c0049: `recover() calls check_repository()`
- c0049 ..> c0049: `unfinished() calls _is_unfinished_factory_plan()`
- c0049 ..> c0050: `_initial_mappings() calls worktree_name()`
- c0049 ..> c0055: `preflight() constructs IntakeProblem`
- c0049 ..> c0057: `_create_plan() constructs ScaffoldProblem`
- c0049 ..> c0057: `_ensure_mapping() constructs ScaffoldProblem`
- c0049 ..> c0057: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0049 ..> c0057: `_recovery_plan() constructs ScaffoldProblem`
- c0049 ..> c0057: `_setup_ownership() constructs ScaffoldProblem`
- c0049 ..> c0057: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0049 ..> c0057: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0049 ..> c0057: `lookup() constructs ScaffoldProblem`
- c0049 ..> c0058: `_create_plan() constructs ScaffoldReadProblem`
- c0049 ..> c0058: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0049 ..> c0058: `lookup() constructs ScaffoldReadProblem`
- c0049 ..> c0058: `prepare() constructs ScaffoldReadProblem`
- c0049 ..> c0058: `recover() constructs ScaffoldReadProblem`
- c0049 ..> c0059: `_create_ownership() constructs UncertainScaffold`
- c0049 ..> c0059: `_create_plan() constructs UncertainScaffold`
- c0049 ..> c0059: `_setup_ownership() constructs UncertainScaffold`
- c0049 ..> c0059: `_sole_recovery_owner() constructs UncertainScaffold`
- c0049 ..> c0059: `prepare() constructs UncertainScaffold`
- c0049 ..> c0072: `type in _ensure_validated_mapping`
- c0049 ..> c0072: `type in _repository`
- c0049 ..> c0072: `type in check_repository`
- c0049 ..> c0075: `type in __init__`
- c0049 ..> c0077: `check() calls check()`
- c0049 ..> c0080: `_create_ownership() calls create_task()`
- c0049 ..> c0080: `_create_ownership() calls update_plan()`
- c0049 ..> c0080: `_create_plan() calls create_plan()`
- c0049 ..> c0080: `_create_plan() calls get_plan()`
- c0049 ..> c0080: `_create_plan() calls owns()`
- c0049 ..> c0080: `_create_plan() calls plans()`
- c0049 ..> c0080: `_is_unfinished_factory_plan() calls owns()`
- c0049 ..> c0080: `_recovery_plan() calls get_plan()`
- c0049 ..> c0080: `_recovery_plan() calls owns()`
- c0049 ..> c0080: `_recovery_plan() calls plans()`
- c0049 ..> c0080: `lookup() calls plans()`
- c0049 ..> c0080: `unfinished() calls plans()`
- c0049 ..> c0085: `type in __init__`
- c0049 ..> c0093: `_is_unfinished_factory_plan() constructs FactoryError`
- c0049 ..> c0104: `type in _create_plan`
- c0049 ..> c0104: `type in _initial_mappings`
- c0049 ..> c0104: `type in _prepare_plan`
- c0049 ..> c0104: `type in _setup_ownership`
- c0049 ..> c0104: `type in lookup`
- c0049 ..> c0104: `type in preflight`
- c0049 ..> c0104: `type in prepare`
- c0049 ..> c0104: `type in recover`
- c0049 ..> c0105: `type in _repository`
- c0049 ..> c0109: `_ensure_mapping() calls ensure()`
- c0049 ..> c0109: `_ensure_mapping() calls verify_removed()`
- c0049 ..> c0109: `_initial_mappings() calls target_branch()`
- c0049 ..> c0111: `type in __init__`
- c0049 ..> c0114: `type in __init__`
- c0050 ..> c0104: `type in worktree_name`
- c0051 --> c0104: `field issue`
- c0052 ..> c0005: `_alert_plan() calls send()`
- c0052 ..> c0005: `_check_pending_repositories() calls send()`
- c0052 ..> c0005: `_check_planning_access() calls send()`
- c0052 ..> c0005: `_handle_intake_read_problem() calls send()`
- c0052 ..> c0005: `_handle_intake_repository_problem() calls send()`
- c0052 ..> c0005: `_handle_recovery_read_problem() calls send()`
- c0052 ..> c0005: `_load_inventory() calls send()`
- c0052 ..> c0005: `_process_issue() calls send()`
- c0052 ..> c0005: `_read_issues() calls send()`
- c0052 ..> c0005: `_recover_work() calls send()`
- c0052 ..> c0005: `_submit() calls send()`
- c0052 ..> c0005: `_watch() calls close()`
- c0052 ..> c0005: `_watch() calls start()`
- c0052 ..> c0005: `_watch() calls wait()`
- c0052 ..> c0005: `run() calls startup_hint()`
- c0052 ..> c0020: `_process_issue() calls prepare()`
- c0052 ..> c0033: `type in __init__`
- c0052 ..> c0034: `_watch() calls poll()`
- c0052 ..> c0034: `type in __init__`
- c0052 ..> c0039: `type in _poll_sources`
- c0052 ..> c0039: `type in _repository_for_source`
- c0052 ..> c0039: `type in _watch`
- c0052 ..> c0039: `type in run`
- c0052 ..> c0041: `_check_pending_repositories() calls check_repository()`
- c0052 ..> c0049: `_check_planning_access() calls check()`
- c0052 ..> c0049: `_load_inventory() calls unfinished()`
- c0052 ..> c0049: `_process_issue() calls lookup()`
- c0052 ..> c0049: `_process_issue() calls recover()`
- c0052 ..> c0049: `_recover_work() calls recover()`
- c0052 ..> c0049: `type in __init__`
- c0052 ..> c0051: `_complete_intake() constructs BlockedWork`
- c0052 ..> c0051: `_handle_intake_read_problem() constructs BlockedWork`
- c0052 ..> c0051: `_handle_intake_repository_problem() constructs BlockedWork`
- c0052 ..> c0051: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0052 ..> c0051: `_process_issue() constructs BlockedWork`
- c0052 ..> c0051: `_remember_inventory_candidate() constructs BlockedWork`
- c0052 ..> c0051: `type in _alert_plan`
- c0052 ..> c0051: `type in _complete_intake`
- c0052 ..> c0051: `type in _complete_recovery`
- c0052 ..> c0051: `type in _handle_recovery_read_problem`
- c0052 ..> c0051: `type in _handle_recovery_repository_problem`
- c0052 ..> c0051: `type in _recover_work`
- c0052 ..> c0051: `type in _remember_task_ids`
- c0052 ..> c0052: `_complete_intake() calls _submit()`
- c0052 ..> c0052: `_complete_recovery() calls _submit()`
- c0052 ..> c0052: `_handle_intake_read_problem() calls _sole_task_id()`
- c0052 ..> c0052: `_handle_intake_repository_problem() calls _alert_plan()`
- c0052 ..> c0052: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0052 ..> c0052: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0052 ..> c0052: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0052 ..> c0052: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0052 ..> c0052: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0052 ..> c0052: `_load_inventory() calls _remember_inventory_candidate()`
- c0052 ..> c0052: `_poll_sources() calls _baseline_source()`
- c0052 ..> c0052: `_poll_sources() calls _process_source()`
- c0052 ..> c0052: `_poll_sources() calls _read_issues()`
- c0052 ..> c0052: `_poll_sources() calls _repository_for_source()`
- c0052 ..> c0052: `_process_issue() calls _complete_intake()`
- c0052 ..> c0052: `_process_issue() calls _handle_intake_read_problem()`
- c0052 ..> c0052: `_process_issue() calls _handle_intake_repository_problem()`
- c0052 ..> c0052: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0052 ..> c0052: `_process_issues() calls _process_issue()`
- c0052 ..> c0052: `_process_issues() calls _skip_issue()`
- c0052 ..> c0052: `_process_source() calls _include_pending_lookups()`
- c0052 ..> c0052: `_process_source() calls _process_issues()`
- c0052 ..> c0052: `_recover_blocked() calls _recover_work()`
- c0052 ..> c0052: `_recover_work() calls _alert_plan()`
- c0052 ..> c0052: `_recover_work() calls _complete_recovery()`
- c0052 ..> c0052: `_recover_work() calls _handle_recovery_read_problem()`
- c0052 ..> c0052: `_recover_work() calls _handle_recovery_repository_problem()`
- c0052 ..> c0052: `_recover_work() calls _remember_task_ids()`
- c0052 ..> c0052: `_remember_inventory_candidate() calls _alert_plan()`
- c0052 ..> c0052: `_watch() calls _check_pending_repositories()`
- c0052 ..> c0052: `_watch() calls _check_planning_access()`
- c0052 ..> c0052: `_watch() calls _load_inventory()`
- c0052 ..> c0052: `_watch() calls _poll_sources()`
- c0052 ..> c0052: `_watch() calls _recover_blocked()`
- c0052 ..> c0052: `run() calls _watch()`
- c0052 ..> c0053: `_watch() constructs _WatchState`
- c0052 ..> c0053: `type in _baseline_source`
- c0052 ..> c0053: `type in _check_pending_repositories`
- c0052 ..> c0053: `type in _check_planning_access`
- c0052 ..> c0053: `type in _complete_intake`
- c0052 ..> c0053: `type in _complete_recovery`
- c0052 ..> c0053: `type in _handle_intake_read_problem`
- c0052 ..> c0053: `type in _handle_intake_repository_problem`
- c0052 ..> c0053: `type in _handle_intake_scaffold_problem`
- c0052 ..> c0053: `type in _handle_recovery_repository_problem`
- c0052 ..> c0053: `type in _load_inventory`
- c0052 ..> c0053: `type in _poll_sources`
- c0052 ..> c0053: `type in _process_issue`
- c0052 ..> c0053: `type in _process_issues`
- c0052 ..> c0053: `type in _process_source`
- c0052 ..> c0053: `type in _recover_blocked`
- c0052 ..> c0053: `type in _recover_work`
- c0052 ..> c0053: `type in _remember_inventory_candidate`
- c0052 ..> c0053: `type in _skip_issue`
- c0052 ..> c0054: `type in _process_issue`
- c0052 ..> c0054: `type in _recover_work`
- c0052 ..> c0056: `type in _handle_intake_repository_problem`
- c0052 ..> c0056: `type in _handle_recovery_repository_problem`
- c0052 ..> c0057: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0052 ..> c0057: `type in _alert_plan`
- c0052 ..> c0057: `type in _handle_intake_scaffold_problem`
- c0052 ..> c0058: `type in _handle_intake_read_problem`
- c0052 ..> c0058: `type in _handle_recovery_read_problem`
- c0052 ..> c0060: `_check_pending_repositories() calls clear()`
- c0052 ..> c0060: `_check_planning_access() calls clear()`
- c0052 ..> c0060: `_complete_intake() calls clear()`
- c0052 ..> c0060: `_complete_recovery() calls clear()`
- c0052 ..> c0060: `_load_inventory() calls clear()`
- c0052 ..> c0060: `_process_issue() calls clear()`
- c0052 ..> c0060: `_read_issues() calls clear()`
- c0052 ..> c0060: `_watch() calls clear()`
- c0052 ..> c0060: `_watch() constructs WatcherAlerts`
- c0052 ..> c0060: `type in _alert_plan`
- c0052 ..> c0060: `type in _check_pending_repositories`
- c0052 ..> c0060: `type in _check_planning_access`
- c0052 ..> c0060: `type in _complete_intake`
- c0052 ..> c0060: `type in _complete_recovery`
- c0052 ..> c0060: `type in _handle_intake_read_problem`
- c0052 ..> c0060: `type in _handle_intake_repository_problem`
- c0052 ..> c0060: `type in _handle_intake_scaffold_problem`
- c0052 ..> c0060: `type in _handle_recovery_read_problem`
- c0052 ..> c0060: `type in _handle_recovery_repository_problem`
- c0052 ..> c0060: `type in _load_inventory`
- c0052 ..> c0060: `type in _poll_sources`
- c0052 ..> c0060: `type in _process_issue`
- c0052 ..> c0060: `type in _process_issues`
- c0052 ..> c0060: `type in _process_source`
- c0052 ..> c0060: `type in _read_issues`
- c0052 ..> c0060: `type in _recover_blocked`
- c0052 ..> c0060: `type in _recover_work`
- c0052 ..> c0060: `type in _remember_inventory_candidate`
- c0052 ..> c0072: `type in _handle_intake_repository_problem`
- c0052 ..> c0072: `type in _process_issue`
- c0052 ..> c0072: `type in _process_issues`
- c0052 ..> c0072: `type in _process_source`
- c0052 ..> c0072: `type in _repository_for_source`
- c0052 ..> c0093: `_read_issues() constructs FactoryError`
- c0052 ..> c0101: `_submit() calls check_watch_stop()`
- c0052 ..> c0101: `_watch() calls check_watch_stop()`
- c0052 ..> c0101: `run() calls check_watch_stop()`
- c0052 ..> c0102: `_read_issues() calls list_open()`
- c0052 ..> c0104: `type in _baseline_source`
- c0052 ..> c0104: `type in _complete_intake`
- c0052 ..> c0104: `type in _complete_recovery`
- c0052 ..> c0104: `type in _handle_intake_read_problem`
- c0052 ..> c0104: `type in _handle_intake_repository_problem`
- c0052 ..> c0104: `type in _handle_intake_scaffold_problem`
- c0052 ..> c0104: `type in _include_pending_lookups`
- c0052 ..> c0104: `type in _process_issue`
- c0052 ..> c0104: `type in _process_issues`
- c0052 ..> c0104: `type in _process_source`
- c0052 ..> c0104: `type in _read_issues`
- c0052 ..> c0104: `type in _skip_issue`
- c0052 ..> c0104: `type in _submit`
- c0052 ..> c0105: `_watch() constructs TicketSource`
- c0052 ..> c0105: `type in _baseline_source`
- c0052 ..> c0105: `type in _include_pending_lookups`
- c0052 ..> c0105: `type in _poll_sources`
- c0052 ..> c0105: `type in _process_source`
- c0052 ..> c0105: `type in _read_issues`
- c0052 ..> c0105: `type in _repository_for_source`
- c0052 ..> c0106: `type in __init__`
- c0053 --> c0051: `field blocked`
- c0053 --> c0051: `field known`
- c0053 --> c0072: `field pending_repositories`
- c0053 --> c0104: `field pending_lookup`
- c0053 --> c0105: `field baselined`
- c0055 --|> c0057: `inherits`
- c0056 --|> c0057: `inherits`
- c0057 --|> c0093: `inherits`
- c0058 --|> c0057: `inherits`
- c0059 --|> c0057: `inherits`
- c0060 ..> c0000: `__init__() calls __init__()`
- c0060 ..> c0005: `send() calls send()`
- c0060 ..> c0061: `send() calls _cleanup_recovery()`
- c0060 ..> c0093: `type in send`
- c0062 ..> c0088: `how_to_reach() calls how_to_attach()`
- c0062 ..> c0088: `open() calls enter()`
- c0062 ..> c0091: `type in __init__`
- c0064 ..> c0000: `build_watcher() constructs FileCleanupReceipts`
- c0064 ..> c0002: `build_initialiser() constructs TomlConfigurationStore`
- c0064 ..> c0005: `build_watcher() constructs ObservedTerminal`
- c0064 ..> c0016: `build_tools() constructs AgentShellRuntimeInstall`
- c0064 ..> c0017: `build_watcher() constructs AgentShellTerminal`
- c0064 ..> c0020: `build_team() constructs PiAgentTeam`
- c0064 ..> c0020: `build_watcher() calls managed_memory_notice()`
- c0064 ..> c0020: `prepare_foreman_launch() calls pi_home()`
- c0064 ..> c0020: `prepare_foreman_launch() calls selected_launch()`
- c0064 ..> c0020: `prepare_foreman_launch() calls validate_completion()`
- c0064 ..> c0020: `type in build_team`
- c0064 ..> c0026: `build_tools() constructs PiInstall`
- c0064 ..> c0034: `build_watcher() constructs CleanupCompleted`
- c0064 ..> c0039: `type in build_watcher`
- c0064 ..> c0039: `type in prepare_foreman_launch`
- c0064 ..> c0039: `type in select_ticketing`
- c0064 ..> c0042: `build_initialiser() constructs InitialiseFactory`
- c0064 ..> c0042: `type in build_initialiser`
- c0064 ..> c0043: `build_team() calls missing_tools()`
- c0064 ..> c0049: `build_watcher() constructs ScaffoldIssue`
- c0064 ..> c0052: `build_watcher() constructs WatchFactory`
- c0064 ..> c0052: `type in build_watcher`
- c0064 ..> c0062: `build_channel() constructs TerminalChannel`
- c0064 ..> c0062: `type in build_channel`
- c0064 ..> c0064: `build_channel() calls build_host()`
- c0064 ..> c0064: `build_initialiser() calls build_team()`
- c0064 ..> c0064: `build_team() calls build_tools()`
- c0064 ..> c0064: `build_watcher() calls build_channel()`
- c0064 ..> c0064: `build_watcher() calls build_host()`
- c0064 ..> c0064: `build_watcher() calls prepare_foreman_launch()`
- c0064 ..> c0064: `build_watcher() calls select_ticketing()`
- c0064 ..> c0064: `prepare_foreman_launch() calls build_team()`
- c0064 ..> c0071: `build_initialiser() constructs DeadlinePolicy`
- c0064 ..> c0071: `build_watcher() constructs DeadlinePolicy`
- c0064 ..> c0071: `type in build_initialiser`
- c0064 ..> c0071: `type in build_watcher`
- c0064 ..> c0073: `build_initialiser() constructs GitHubForge`
- c0064 ..> c0073: `build_watcher() constructs GitHubForge`
- c0064 ..> c0078: `prepare_foreman_launch() calls role_environment()`
- c0064 ..> c0079: `build_tools() constructs ForgetfulInstall`
- c0064 ..> c0080: `build_watcher() constructs ForgetfulPlanStore`
- c0064 ..> c0082: `build_initialiser() constructs ForgetfulSetup`
- c0064 ..> c0083: `type in build_tools`
- c0064 ..> c0088: `build_host() constructs TmuxHost`
- c0064 ..> c0088: `type in build_host`
- c0064 ..> c0089: `build_tools() constructs TmuxInstall`
- c0064 ..> c0093: `build_watcher() constructs FactoryError`
- c0064 ..> c0093: `prepare_foreman_launch() constructs FactoryError`
- c0064 ..> c0093: `select_ticketing() constructs FactoryError`
- c0064 ..> c0102: `build_initialiser() constructs GitHubTicketing`
- c0064 ..> c0102: `build_watcher() calls check_ready()`
- c0064 ..> c0102: `select_ticketing() calls validate_source()`
- c0064 ..> c0106: `type in select_ticketing`
- c0064 ..> c0107: `build_initialiser() constructs GitRepositories`
- c0064 ..> c0107: `build_watcher() constructs GitRepositories`
- c0064 ..> c0109: `build_watcher() constructs GitWorktrees`
- c0065 ..> c0039: `type in agree_definition_of_done`
- c0065 ..> c0065: `agree_definition_of_done() calls _deployment_agreement()`
- c0065 ..> c0093: `_deployment_agreement() constructs FactoryError`
- c0065 ..> c0093: `agree_definition_of_done() constructs FactoryError`
- c0065 ..> c0096: `agree_definition_of_done() calls check_skill_file()`
- c0065 ..> c0096: `agree_definition_of_done() calls write_new()`
- c0066 --> c0039: `field config`
- c0066 --> c0083: `field connection`
- c0067 ..> c0000: `_initialise_locked() calls load()`
- c0067 ..> c0003: `_initialise() calls quote()`
- c0067 ..> c0003: `_launch_setup_foreman() calls quote()`
- c0067 ..> c0003: `_managed_watch_status() calls quote()`
- c0067 ..> c0003: `_select_model() calls quote()`
- c0067 ..> c0003: `_validate_setup_owner() calls quote()`
- c0067 ..> c0003: `_watch_locked() calls quote()`
- c0067 ..> c0004: `_foreman() calls hold()`
- c0067 ..> c0004: `_foreman() constructs WorkspaceWatchLease`
- c0067 ..> c0004: `_initialise() calls hold()`
- c0067 ..> c0004: `_initialise() constructs WorkspaceWatchLease`
- c0067 ..> c0004: `_watch() calls hold()`
- c0067 ..> c0004: `_watch() constructs WorkspaceWatchLease`
- c0067 ..> c0006: `_prompt_workers() calls update()`
- c0067 ..> c0007: `_managed_watch_status() calls unknown_status()`
- c0067 ..> c0007: `_watch_locked() calls observe_plain_watch()`
- c0067 ..> c0007: `_watch_status() calls plain_watch_status()`
- c0067 ..> c0007: `_watch_status() calls unknown_status()`
- c0067 ..> c0008: `_watch_locked() constructs BorrowedForemanTerminal`
- c0067 ..> c0013: `_watch_locked() calls run()`
- c0067 ..> c0015: `_change_managed_watch() calls request()`
- c0067 ..> c0015: `_finish_existing_setup() calls read_state()`
- c0067 ..> c0015: `_foreman() calls read_state()`
- c0067 ..> c0015: `_foreman() calls request()`
- c0067 ..> c0015: `_foreman() calls start_owner()`
- c0067 ..> c0015: `_initialise() calls request()`
- c0067 ..> c0015: `_initialise_locked() calls read_state()`
- c0067 ..> c0015: `_launch_setup_foreman() calls start_owner()`
- c0067 ..> c0015: `_managed_watch_status() calls read_state()`
- c0067 ..> c0015: `_managed_watch_status() calls request()`
- c0067 ..> c0015: `_offer_factory_launch() calls read_state()`
- c0067 ..> c0015: `_watch_locked() calls read_state()`
- c0067 ..> c0020: `_complete_setup() calls managed_memory_notice()`
- c0067 ..> c0020: `_complete_setup() calls record_completion()`
- c0067 ..> c0020: `_discover_worker_models() calls list_models()`
- c0067 ..> c0020: `_finish_existing_setup() calls choose_pi_home()`
- c0067 ..> c0020: `_finish_existing_setup() calls save_pi_choice()`
- c0067 ..> c0020: `_finish_existing_setup() calls selected_launch()`
- c0067 ..> c0020: `_foreman() calls managed_memory_notice()`
- c0067 ..> c0020: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0067 ..> c0020: `_select_model() calls list_models()`
- c0067 ..> c0020: `_start_initial_setup() calls begin_setup()`
- c0067 ..> c0020: `_start_initial_setup() calls choose_pi_home()`
- c0067 ..> c0020: `_validate_initial_model() calls prepare_roles()`
- c0067 ..> c0020: `_watch_status() calls validate_completion()`
- c0067 ..> c0030: `_configure_new_factory() constructs InitialAgentChoices`
- c0067 ..> c0030: `type in _configure_new_factory`
- c0067 ..> c0030: `type in _foreman_memory_choices`
- c0067 ..> c0030: `type in _owner_choices`
- c0067 ..> c0030: `type in _prompt_coordinator_choices`
- c0067 ..> c0030: `type in _validate_initial_model`
- c0067 ..> c0030: `type in _worker_choices`
- c0067 ..> c0031: `_start_initial_setup() calls validate_initial_agents()`
- c0067 ..> c0039: `type in _complete_setup`
- c0067 ..> c0039: `type in _configure_new_factory`
- c0067 ..> c0039: `type in _finish_existing_setup`
- c0067 ..> c0039: `type in _validate_initial_model`
- c0067 ..> c0040: `_connection() calls validate()`
- c0067 ..> c0042: `_complete_setup() calls check_foreman()`
- c0067 ..> c0042: `_configure_new_factory() calls configure()`
- c0067 ..> c0042: `_configure_new_factory() calls inspect()`
- c0067 ..> c0042: `_finish_existing_setup() calls initialise()`
- c0067 ..> c0042: `_initialise_locked() calls load_existing()`
- c0067 ..> c0042: `_launch_setup_foreman() calls check_foreman()`
- c0067 ..> c0042: `_prepare_foreman() calls prepare_foreman()`
- c0067 ..> c0042: `_start_initial_setup() calls initialise()`
- c0067 ..> c0042: `select_repositories() calls discover()`
- c0067 ..> c0042: `type in _complete_setup`
- c0067 ..> c0042: `type in _configure_new_factory`
- c0067 ..> c0042: `type in _discover_worker_models`
- c0067 ..> c0042: `type in _finish_existing_setup`
- c0067 ..> c0042: `type in _select_project`
- c0067 ..> c0042: `type in _start_initial_setup`
- c0067 ..> c0042: `type in _validate_initial_model`
- c0067 ..> c0042: `type in select_repositories`
- c0067 ..> c0064: `_foreman() calls build_channel()`
- c0067 ..> c0064: `_foreman() calls build_host()`
- c0067 ..> c0064: `_foreman() calls prepare_foreman_launch()`
- c0067 ..> c0064: `_initialise() calls build_channel()`
- c0067 ..> c0064: `_initialise_locked() calls build_initialiser()`
- c0067 ..> c0064: `_launch_setup_foreman() calls build_host()`
- c0067 ..> c0064: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0067 ..> c0064: `_watch_locked() calls build_watcher()`
- c0067 ..> c0064: `_watch_status() calls build_team()`
- c0067 ..> c0065: `_finish_existing_setup() calls agree_definition_of_done()`
- c0067 ..> c0065: `_start_initial_setup() calls agree_definition_of_done()`
- c0067 ..> c0066: `_start_initial_setup() constructs _InitialSetupState`
- c0067 ..> c0066: `type in _discover_worker_models`
- c0067 ..> c0066: `type in _validate_initial_model`
- c0067 ..> c0067: `_complete_setup() calls _managed_rest_mapping_available()`
- c0067 ..> c0067: `_configure_new_factory() calls _prepare_foreman()`
- c0067 ..> c0067: `_configure_new_factory() calls _select_model()`
- c0067 ..> c0067: `_configure_new_factory() calls _select_numbered()`
- c0067 ..> c0067: `_configure_new_factory() calls select_repositories()`
- c0067 ..> c0067: `_connection() calls _check_existing_connection()`
- c0067 ..> c0067: `_discover_worker_models() calls _prepare_foreman()`
- c0067 ..> c0067: `_finish_existing_setup() calls _complete_setup()`
- c0067 ..> c0067: `_finish_existing_setup() calls _confirm_pi_home()`
- c0067 ..> c0067: `_finish_existing_setup() calls _connection()`
- c0067 ..> c0067: `_finish_existing_setup() calls _launch_setup_foreman()`
- c0067 ..> c0067: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0067 ..> c0067: `_foreman_memory_choices() calls _select_numbered()`
- c0067 ..> c0067: `_initialise() calls _initialise_locked()`
- c0067 ..> c0067: `_initialise() calls _offer_factory_launch()`
- c0067 ..> c0067: `_initialise_locked() calls _finish_existing_setup()`
- c0067 ..> c0067: `_initialise_locked() calls _start_initial_setup()`
- c0067 ..> c0067: `_initialise_locked() calls _validate_setup_owner()`
- c0067 ..> c0067: `_print_models() calls _safe_diagnostic()`
- c0067 ..> c0067: `_prompt_coordinator_choices() calls _select_numbered()`
- c0067 ..> c0067: `_prompt_worker() calls _select_numbered()`
- c0067 ..> c0067: `_prompt_workers() calls _prompt_worker()`
- c0067 ..> c0067: `_select_model() calls _print_models()`
- c0067 ..> c0067: `_select_model() calls _select_numbered()`
- c0067 ..> c0067: `_select_numbered() calls _safe_diagnostic()`
- c0067 ..> c0067: `_select_project() calls _listed_project_id()`
- c0067 ..> c0067: `_select_project() calls _safe_diagnostic()`
- c0067 ..> c0067: `_select_setup_route() calls _select_numbered()`
- c0067 ..> c0067: `_start_initial_setup() calls _complete_setup()`
- c0067 ..> c0067: `_start_initial_setup() calls _configure_new_factory()`
- c0067 ..> c0067: `_start_initial_setup() calls _confirm_pi_home()`
- c0067 ..> c0067: `_start_initial_setup() calls _connection()`
- c0067 ..> c0067: `_start_initial_setup() calls _foreman_memory_choices()`
- c0067 ..> c0067: `_start_initial_setup() calls _launch_setup_foreman()`
- c0067 ..> c0067: `_start_initial_setup() calls _owner_choices()`
- c0067 ..> c0067: `_start_initial_setup() calls _research_choices()`
- c0067 ..> c0067: `_start_initial_setup() calls _worker_choices()`
- c0067 ..> c0067: `_validate_initial_model() calls _prepare_foreman()`
- c0067 ..> c0067: `_validate_initial_model() calls _select_model()`
- c0067 ..> c0067: `_validate_initial_model() calls _select_project()`
- c0067 ..> c0067: `_watch() calls _change_managed_watch()`
- c0067 ..> c0067: `_watch() calls _watch_locked()`
- c0067 ..> c0067: `_watch() calls _watch_status()`
- c0067 ..> c0067: `_watch_locked() calls _choose_existing()`
- c0067 ..> c0067: `_watch_locked() calls _safe_diagnostic()`
- c0067 ..> c0067: `_watch_status() calls _managed_watch_status()`
- c0067 ..> c0067: `_worker_choices() calls _prompt_coordinator_choices()`
- c0067 ..> c0067: `_worker_choices() calls _prompt_workers()`
- c0067 ..> c0067: `_worker_choices() calls _select_setup_route()`
- c0067 ..> c0067: `_worker_choices() calls _worker_arguments()`
- c0067 ..> c0067: `main() calls _foreman()`
- c0067 ..> c0067: `main() calls _initialise()`
- c0067 ..> c0067: `main() calls _parse_arguments()`
- c0067 ..> c0067: `main() calls _safe_diagnostic()`
- c0067 ..> c0067: `main() calls _watch()`
- c0067 ..> c0068: `_select_numbered() calls parse_numbered_selection()`
- c0067 ..> c0069: `main() calls update_resources()`
- c0067 ..> c0070: `_foreman() calls load_configuration()`
- c0067 ..> c0070: `_watch_locked() calls load_configuration()`
- c0067 ..> c0070: `_watch_status() calls load_configuration()`
- c0067 ..> c0071: `main() constructs DeadlinePolicy`
- c0067 ..> c0071: `type in _finish_existing_setup`
- c0067 ..> c0071: `type in _foreman`
- c0067 ..> c0071: `type in _initialise`
- c0067 ..> c0071: `type in _initialise_locked`
- c0067 ..> c0071: `type in _start_initial_setup`
- c0067 ..> c0071: `type in _watch`
- c0067 ..> c0071: `type in _watch_locked`
- c0067 ..> c0071: `type in main`
- c0067 ..> c0076: `_complete_setup() calls uses_browser_login()`
- c0067 ..> c0077: `_select_project() calls create_project()`
- c0067 ..> c0077: `_select_project() calls projects()`
- c0067 ..> c0083: `_connection() constructs ForgetfulConnection`
- c0067 ..> c0083: `type in _check_existing_connection`
- c0067 ..> c0083: `type in _configure_new_factory`
- c0067 ..> c0083: `type in _connection`
- c0067 ..> c0083: `type in _foreman_memory_choices`
- c0067 ..> c0083: `type in _managed_rest_mapping_available`
- c0067 ..> c0083: `type in _select_project`
- c0067 ..> c0093: `_change_managed_watch() constructs FactoryError`
- c0067 ..> c0093: `_check_existing_connection() constructs FactoryError`
- c0067 ..> c0093: `_choose_existing() constructs FactoryError`
- c0067 ..> c0093: `_configure_new_factory() constructs FactoryError`
- c0067 ..> c0093: `_finish_existing_setup() constructs FactoryError`
- c0067 ..> c0093: `_foreman() constructs FactoryError`
- c0067 ..> c0093: `_foreman_memory_choices() constructs FactoryError`
- c0067 ..> c0093: `_initialise() constructs FactoryError`
- c0067 ..> c0093: `_initialise_locked() constructs FactoryError`
- c0067 ..> c0093: `_install_missing() constructs FactoryError`
- c0067 ..> c0093: `_listed_project_id() constructs FactoryError`
- c0067 ..> c0093: `_prompt_coordinator_choices() constructs FactoryError`
- c0067 ..> c0093: `_prompt_worker() constructs FactoryError`
- c0067 ..> c0093: `_select_model() constructs FactoryError`
- c0067 ..> c0093: `_select_project() constructs FactoryError`
- c0067 ..> c0093: `_validate_setup_owner() constructs FactoryError`
- c0067 ..> c0093: `_watch_locked() constructs FactoryError`
- c0067 ..> c0093: `_worker_choices() constructs FactoryError`
- c0067 ..> c0093: `main() constructs FactoryError`
- c0067 ..> c0093: `select_repositories() constructs FactoryError`
- c0067 ..> c0096: `_discover_worker_models() calls check_real_path()`
- c0067 ..> c0101: `_watch_locked() calls watch_stop_scope()`
- c0068 ..> c0093: `parse_numbered_selection() constructs FactoryError`
- c0069 ..> c0004: `update_resources() calls hold()`
- c0069 ..> c0004: `update_resources() constructs WorkspaceWatchLease`
- c0069 ..> c0010: `update_resources() calls ready()`
- c0069 ..> c0015: `update_resources() calls read_state()`
- c0069 ..> c0016: `update_resources() calls install()`
- c0069 ..> c0016: `update_resources() constructs AgentShellRuntimeInstall`
- c0069 ..> c0020: `update_resources() calls validate_bundled_resources()`
- c0069 ..> c0025: `update_resources() calls apply_update()`
- c0069 ..> c0025: `update_resources() calls plan_update()`
- c0069 ..> c0064: `update_resources() calls build_team()`
- c0069 ..> c0069: `update_resources() calls _report()`
- c0069 ..> c0071: `type in update_resources`
- c0069 ..> c0093: `_report() constructs FactoryError`
- c0069 ..> c0093: `update_resources() constructs FactoryError`
- c0070 ..> c0000: `load_configuration() calls load()`
- c0070 ..> c0002: `load_configuration() constructs TomlConfigurationStore`
- c0070 ..> c0039: `type in load_configuration`
- c0070 ..> c0093: `load_configuration() constructs FactoryError`
- c0071 --> c0029: `field agentshell`
- c0071 ..> c0099: `__post_init__() calls positive_duration()`
- c0072 --> c0105: `field work_source`
- c0073 ..> c0074: `repository() constructs RepositoryRef`
- c0073 ..> c0074: `type in is_change_request`
- c0073 ..> c0074: `type in repository`
- c0073 ..> c0093: `repository() constructs FactoryError`
- c0075 ..> c0074: `type in is_change_request`
- c0075 ..> c0074: `type in repository`
- c0076 ..> c0015: `uses_browser_login() calls request()`
- c0076 ..> c0083: `type in uses_browser_login`
- c0077 ..> c0077: `call() calls command()`
- c0077 ..> c0077: `check() calls call()`
- c0077 ..> c0077: `check() calls command()`
- c0077 ..> c0077: `command() calls _environment()`
- c0077 ..> c0077: `create_project() calls call()`
- c0077 ..> c0077: `login() calls _environment()`
- c0077 ..> c0077: `projects() calls command()`
- c0077 ..> c0078: `_environment() calls role_environment()`
- c0077 ..> c0078: `check() calls _catalog_tools()`
- c0077 ..> c0083: `type in _environment`
- c0077 ..> c0083: `type in call`
- c0077 ..> c0083: `type in check`
- c0077 ..> c0083: `type in command`
- c0077 ..> c0083: `type in create_project`
- c0077 ..> c0083: `type in login`
- c0077 ..> c0083: `type in projects`
- c0077 ..> c0093: `check() constructs FactoryError`
- c0077 ..> c0093: `command() constructs FactoryError`
- c0077 ..> c0093: `create_project() constructs FactoryError`
- c0077 ..> c0093: `login() constructs FactoryError`
- c0077 ..> c0093: `projects() constructs FactoryError`
- c0077 ..> c0098: `command() calls run_owned()`
- c0077 ..> c0098: `login() calls run_owned()`
- c0077 ..> c0101: `command() calls check_watch_stop()`
- c0078 ..> c0006: `role_environment() calls update()`
- c0078 ..> c0083: `type in role_environment`
- c0078 ..> c0094: `role_environment() calls executable_path()`
- c0079 ..> c0079: `absent() calls _required()`
- c0079 ..> c0079: `absent() calls _selected()`
- c0079 ..> c0079: `describe() calls _python()`
- c0079 ..> c0079: `install() calls _python()`
- c0079 ..> c0079: `unready() calls _required()`
- c0079 ..> c0079: `unready() calls _selected()`
- c0079 ..> c0083: `type in __init__`
- c0079 ..> c0093: `_python() constructs FactoryError`
- c0079 ..> c0094: `_selected() calls executable_path()`
- c0079 ..> c0095: `_python() calls check_uv()`
- c0079 ..> c0095: `_python() calls install_environment()`
- c0079 ..> c0095: `install() calls install_locks()`
- c0079 ..> c0095: `install() calls no_installer()`
- c0079 ..> c0095: `install() calls require_manager()`
- c0079 ..> c0095: `install() calls run_install()`
- c0079 ..> c0095: `unready() calls runtime_ready()`
- c0079 ..> c0098: `_python() calls run_owned()`
- c0080 ..> c0049: `check() calls check()`
- c0080 ..> c0077: `__init__() constructs AgentForgetfulConnection`
- c0080 ..> c0077: `_call() calls call()`
- c0080 ..> c0080: `_read() calls _call()`
- c0080 ..> c0080: `_task() calls _read()`
- c0080 ..> c0080: `create_plan() calls _call()`
- c0080 ..> c0080: `create_task() calls _call()`
- c0080 ..> c0080: `get_plan() calls _read()`
- c0080 ..> c0080: `plans() calls _read()`
- c0080 ..> c0080: `plans() calls _rows()`
- c0080 ..> c0080: `tasks() calls _read()`
- c0080 ..> c0080: `tasks() calls _rows()`
- c0080 ..> c0080: `tasks() calls _task()`
- c0080 ..> c0080: `update_plan() calls _call()`
- c0080 ..> c0080: `update_task() calls _call()`
- c0080 ..> c0081: `_rows() calls _positive_id()`
- c0080 ..> c0081: `_task() calls _positive_id()`
- c0080 ..> c0081: `get_plan() calls _positive_id()`
- c0080 ..> c0083: `type in __init__`
- c0080 ..> c0086: `_read() constructs PlanningReadError`
- c0080 ..> c0086: `_rows() constructs PlanningReadError`
- c0080 ..> c0086: `_task() constructs PlanningReadError`
- c0080 ..> c0086: `get_plan() constructs PlanningReadError`
- c0082 ..> c0049: `check() calls check()`
- c0082 ..> c0076: `uses_browser_login() calls uses_browser_login()`
- c0082 ..> c0077: `_native() constructs AgentForgetfulConnection`
- c0082 ..> c0077: `create_project() calls create_project()`
- c0082 ..> c0077: `login() calls login()`
- c0082 ..> c0077: `projects() calls projects()`
- c0082 ..> c0077: `type in _native`
- c0082 ..> c0082: `check() calls _native()`
- c0082 ..> c0082: `create_project() calls _native()`
- c0082 ..> c0082: `login() calls _native()`
- c0082 ..> c0082: `projects() calls _native()`
- c0082 ..> c0083: `type in check`
- c0082 ..> c0083: `type in create_project`
- c0082 ..> c0083: `type in login`
- c0082 ..> c0083: `type in prepare`
- c0082 ..> c0083: `type in projects`
- c0082 ..> c0083: `type in uses_browser_login`
- c0083 ..> c0083: `validate() calls _validate_server()`
- c0083 ..> c0084: `_validate_server() calls loopback_host()`
- c0083 ..> c0093: `_validate_server() constructs FactoryError`
- c0083 ..> c0093: `validate() constructs FactoryError`
- c0083 ..> c0099: `_validate_server() calls nonblank()`
- c0083 ..> c0099: `validate() calls nonblank()`
- c0084 ..> c0083: `connection_from_mapping() calls validate()`
- c0084 ..> c0083: `connection_from_mapping() constructs ForgetfulConnection`
- c0084 ..> c0083: `type in connection_from_mapping`
- c0084 ..> c0093: `connection_from_mapping() constructs FactoryError`
- c0086 --|> c0093: `inherits`
- c0087 ..> c0083: `type in check`
- c0087 ..> c0083: `type in create_project`
- c0087 ..> c0083: `type in login`
- c0087 ..> c0083: `type in prepare`
- c0087 ..> c0083: `type in projects`
- c0087 ..> c0083: `type in uses_browser_login`
- c0088 ..> c0013: `enter() calls run()`
- c0088 ..> c0093: `enter() constructs FactoryError`
- c0089 ..> c0090: `describe() calls ubuntu_tmux()`
- c0089 ..> c0090: `install() calls ubuntu_tmux()`
- c0089 ..> c0093: `install() constructs FactoryError`
- c0089 ..> c0094: `absent() calls executable_path()`
- c0089 ..> c0095: `install() calls no_installer()`
- c0089 ..> c0095: `install() calls run_install()`
- c0092 ..> c0013: `run_command() calls run()`
- c0092 ..> c0093: `run_command() constructs FactoryError`
- c0092 ..> c0101: `run_command() calls check_watch_stop()`
- c0095 ..> c0093: `check_uv() constructs FactoryError`
- c0095 ..> c0093: `install_locks() constructs FactoryError`
- c0095 ..> c0093: `no_installer() constructs FactoryError`
- c0095 ..> c0093: `require_manager() constructs FactoryError`
- c0095 ..> c0093: `run_install() constructs FactoryError`
- c0095 ..> c0093: `type in no_installer`
- c0095 ..> c0095: `check_uv() calls install_environment()`
- c0095 ..> c0095: `install_locks() calls sync_fingerprint()`
- c0095 ..> c0095: `run_install() calls install_environment()`
- c0095 ..> c0095: `runtime_ready() calls sync_fingerprint()`
- c0095 ..> c0096: `install_locks() calls write_new()`
- c0095 ..> c0098: `check_uv() calls run_owned()`
- c0095 ..> c0098: `run_install() calls run_owned()`
- c0095 ..> c0098: `runtime_ready() calls run_owned()`
- c0096 ..> c0000: `read_generated_json() calls load()`
- c0096 ..> c0005: `_generated_parent() calls close()`
- c0096 ..> c0005: `check_skill_file() calls close()`
- c0096 ..> c0093: `_generated_parent() constructs FactoryError`
- c0096 ..> c0093: `check_real_path() constructs FactoryError`
- c0096 ..> c0093: `check_skill_file() constructs FactoryError`
- c0096 ..> c0093: `read_generated_json() constructs FactoryError`
- c0096 ..> c0093: `write_definition() constructs FactoryError`
- c0096 ..> c0093: `write_new() constructs FactoryError`
- c0096 ..> c0096: `_generated_parent() calls check_real_path()`
- c0096 ..> c0096: `check_skill_file() calls check_real_path()`
- c0096 ..> c0096: `read_generated_json() calls _generated_parent()`
- c0096 ..> c0096: `remove_generated() calls _generated_parent()`
- c0096 ..> c0096: `replace_generated_json() calls _generated_parent()`
- c0096 ..> c0096: `write_definition() calls read_generated_json()`
- c0096 ..> c0096: `write_definition() calls write_json()`
- c0096 ..> c0096: `write_json() calls write_new()`
- c0096 ..> c0096: `write_new() calls check_real_path()`
- c0098 ..> c0005: `_close_capture_streams() calls close()`
- c0098 ..> c0005: `_terminate_owned_process() calls wait()`
- c0098 ..> c0093: `run_owned() constructs FactoryError`
- c0098 ..> c0098: `_terminate_owned_process() calls _close_capture_streams()`
- c0098 ..> c0098: `run_owned() calls _terminate_owned_process()`
- c0098 ..> c0101: `run_owned() calls check_watch_stop()`
- c0099 ..> c0093: `nonblank() constructs FactoryError`
- c0101 ..> c0100: `watch_stop_scope() constructs WatchStop`
- c0102 ..> c0092: `_api() calls run_command()`
- c0102 ..> c0092: `check_ready() calls run_command()`
- c0102 ..> c0093: `_api() constructs FactoryError`
- c0102 ..> c0093: `_comments() constructs FactoryError`
- c0102 ..> c0093: `_validate_issue() constructs FactoryError`
- c0102 ..> c0093: `check_access() constructs FactoryError`
- c0102 ..> c0093: `check_ready() constructs FactoryError`
- c0102 ..> c0093: `create_label() constructs FactoryError`
- c0102 ..> c0093: `list_labels() constructs FactoryError`
- c0102 ..> c0093: `list_open() constructs FactoryError`
- c0102 ..> c0093: `validate_source() constructs FactoryError`
- c0102 ..> c0102: `_comments() calls _api()`
- c0102 ..> c0102: `_ticket() calls _comments()`
- c0102 ..> c0102: `_ticket() calls _milestone()`
- c0102 ..> c0102: `check_access() calls _api()`
- c0102 ..> c0102: `create_label() calls _api()`
- c0102 ..> c0102: `list_labels() calls _api()`
- c0102 ..> c0102: `list_open() calls _api()`
- c0102 ..> c0102: `list_open() calls _ticket()`
- c0102 ..> c0102: `list_open() calls _validate_issue()`
- c0102 ..> c0103: `list_labels() constructs Label`
- c0102 ..> c0103: `type in create_label`
- c0102 ..> c0103: `type in list_labels`
- c0102 ..> c0104: `_ticket() constructs Ticket`
- c0102 ..> c0104: `type in _ticket`
- c0102 ..> c0104: `type in list_open`
- c0102 ..> c0105: `type in _api`
- c0102 ..> c0105: `type in _comments`
- c0102 ..> c0105: `type in _ticket`
- c0102 ..> c0105: `type in _validate_issue`
- c0102 ..> c0105: `type in check_access`
- c0102 ..> c0105: `type in create_label`
- c0102 ..> c0105: `type in list_labels`
- c0102 ..> c0105: `type in list_open`
- c0102 ..> c0105: `type in validate_source`
- c0104 --> c0105: `field source`
- c0106 ..> c0103: `type in create_label`
- c0106 ..> c0103: `type in list_labels`
- c0106 ..> c0104: `type in list_open`
- c0106 ..> c0105: `type in check_access`
- c0106 ..> c0105: `type in create_label`
- c0106 ..> c0105: `type in list_labels`
- c0106 ..> c0105: `type in list_open`
- c0106 ..> c0105: `type in validate_source`
- c0107 ..> c0092: `origin() calls run_command()`
- c0107 ..> c0093: `origin() constructs FactoryError`
- c0107 ..> c0108: `origin() calls _resolve_repository()`
- c0108 ..> c0093: `_resolve_repository() constructs FactoryError`
- c0109 ..> c0003: `_network_git() calls quote()`
- c0109 ..> c0060: `begin_cleanup_cycle() calls clear()`
- c0109 ..> c0092: `_dispose() calls run_command()`
- c0109 ..> c0092: `_network_git() calls run_command()`
- c0109 ..> c0092: `_read_git() calls run_command()`
- c0109 ..> c0092: `ensure() calls run_command()`
- c0109 --> c0093: `field cleanup_defaults`
- c0109 ..> c0093: `ensure() constructs FactoryError`
- c0109 ..> c0101: `ensure() calls check_watch_stop()`
- c0109 ..> c0109: `_disposal_state() calls _repository_entries()`
- c0109 ..> c0109: `_disposal_state() calls _validate_disposal_origin()`
- c0109 ..> c0109: `_disposal_state() calls _validate_disposal_path()`
- c0109 ..> c0109: `_disposal_state() calls _validate_disposal_refs()`
- c0109 ..> c0109: `_disposal_state() calls _validate_registered_worktree()`
- c0109 ..> c0109: `_dispose() calls _disposal_state()`
- c0109 ..> c0109: `_dispose() calls _network_git()`
- c0109 ..> c0109: `_dispose() calls _network_read()`
- c0109 ..> c0109: `_dispose() calls _read_git()`
- c0109 ..> c0109: `_dispose() calls _repository_entries()`
- c0109 ..> c0109: `_dispose() calls _verify_local_ref_absent()`
- c0109 ..> c0109: `_inspect() calls _read_git()`
- c0109 ..> c0109: `_inspect() calls _repository_entries()`
- c0109 ..> c0109: `_inspect() calls _validate_registered_worktree()`
- c0109 ..> c0109: `_network_git() calls _read_git()`
- c0109 ..> c0109: `_network_read() calls _network_git()`
- c0109 ..> c0109: `_remote_default() calls _network_read()`
- c0109 ..> c0109: `_repository_entries() calls _read_git()`
- c0109 ..> c0109: `_validate_common_directory() calls _read_git()`
- c0109 ..> c0109: `_validate_disposal_origin() calls _read_git()`
- c0109 ..> c0109: `_validate_disposal_path() calls _read_git()`
- c0109 ..> c0109: `_validate_disposal_refs() calls _read_git()`
- c0109 ..> c0109: `_validate_disposal_refs() calls _remote_default()`
- c0109 ..> c0109: `_validate_registered_worktree() calls _validate_common_directory()`
- c0109 ..> c0109: `_validate_registered_worktree() calls _validate_registration()`
- c0109 ..> c0109: `_validate_registered_worktree() calls _validate_target_identity()`
- c0109 ..> c0109: `_validate_target_identity() calls _read_git()`
- c0109 ..> c0109: `_verify_local_ref_absent() calls _read_git()`
- c0109 ..> c0109: `_verify_removed() calls _repository_entries()`
- c0109 ..> c0109: `dispose() calls _dispose()`
- c0109 ..> c0109: `ensure() calls _inspect()`
- c0109 ..> c0109: `inspect() calls _inspect()`
- c0109 ..> c0109: `repository_identity() calls _read_git()`
- c0109 ..> c0109: `target_branch() calls _read_git()`
- c0109 ..> c0109: `verify_removed() calls _verify_removed()`
- c0109 ..> c0110: `_repository_entries() calls _worktree_entries()`
- c0109 ..> c0112: `_disposal_state() constructs WorktreeProblem`
- c0109 ..> c0112: `_dispose() constructs WorktreeProblem`
- c0109 ..> c0112: `_inspect() constructs WorktreeProblem`
- c0109 ..> c0112: `_network_read() constructs WorktreeProblem`
- c0109 ..> c0112: `_repository_entries() constructs WorktreeProblem`
- c0109 ..> c0112: `_validate_common_directory() constructs WorktreeProblem`
- c0109 ..> c0112: `_validate_disposal_origin() constructs WorktreeProblem`
- c0109 ..> c0112: `_validate_disposal_path() constructs WorktreeProblem`
- c0109 ..> c0112: `_validate_disposal_refs() constructs WorktreeProblem`
- c0109 ..> c0112: `_validate_registration() constructs WorktreeProblem`
- c0109 ..> c0112: `_validate_target_identity() constructs WorktreeProblem`
- c0109 ..> c0112: `_verify_local_ref_absent() constructs WorktreeProblem`
- c0109 ..> c0112: `_verify_removed() constructs WorktreeProblem`
- c0109 ..> c0112: `dispose() constructs WorktreeProblem`
- c0109 ..> c0113: `_read_git() constructs WorktreeReadError`
- c0109 ..> c0113: `ensure() constructs WorktreeReadError`
- c0109 ..> c0113: `inspect() constructs WorktreeReadError`
- c0109 ..> c0113: `repository_identity() constructs WorktreeReadError`
- c0109 ..> c0113: `target_branch() constructs WorktreeReadError`
- c0109 ..> c0113: `verify_removed() constructs WorktreeReadError`
- c0112 ..> c0000: `__init__() calls __init__()`
- c0112 --|> c0093: `inherits`
- c0113 --|> c0093: `inherits`

## Type key

- Type1: `FactoryConfiguration | None`
- Type2: `tuple[int, int]`
- Type3: `dict | None`
- Type4: `Iterator[PlainWatchObservation | None]`
- Type5: `Callable[[str], None]`
- Type6: `object | None`
- Type7: `int | None`
- Type8: `str | None`
- Type9: `tuple[Path, Path, int]`
- Type10: `tuple[Path, Path]`
- Type11: `dict[str, str] | None`
- Type12: `subprocess.Popen | None`
- Type13: `Callable[[ForgetfulConnection, str], dict[str, str]]`
- Type14: `Callable[[ForgetfulConnection], list[str]]`
- Type15: `dict[tuple[str, Path], list[str]]`
- Type16: `bool | None`
- Type17: `Path | None`
- Type18: `dict[str, bytes]`
- Type19: `tuple[str, ...]`
- Type20: `dict[Path, None]`
- Type21: `frozenset[tuple[int, int]]`
- Type22: `Callable[[str], bool]`
- Type23: `dict[int, int]`
- Type24: `tuple | None`
- Type25: `tuple[dict, dict] | None`
- Type26: `dict[int, list[dict]]`
- Type27: `dict[str, str]`
- Type28: `list[dict] | None`
- Type29: `list[CompletedWork] | None`
- Type30: `CleanupState | None`
- Type31: `tuple[RepositoryReference, ...]`
- Type32: `ForgetfulConnection | None`
- Type33: `Callable[[ForgetfulConnection], Sequence[ToolInstaller]]`
- Type34: `Callable[[list[str]], None]`
- Type35: `Callable[[str, str], bool]`
- Type36: `list[Path] | None`
- Type37: `list[str] | None`
- Type38: `dict[str, RepositoryReference]`
- Type39: `dict[TicketSource, tuple[Label, ...]]`
- Type40: `Callable[[], FactoryConfiguration | None]`
- Type41: `tuple[ToolInstaller | None, str | None]`
- Type42: `'CleanupSet'`
- Type43: `tuple[list[dict], list[dict]]`
- Type44: `tuple[Ticket, dict] | None`
- Type45: `Ticket | None`
- Type46: `tuple[int, ...] | None`
- Type47: `tuple[int, ...]`
- Type48: `Callable[[], bool]`
- Type49: `tuple[set[str], bool]`
- Type50: `tuple[TicketSource, ...]`
- Type51: `tuple[Ticket, ...]`
- Type52: `dict[str, Ticket]`
- Type53: `BlockedWork | None`
- Type54: `tuple[Ticket, ...] | None`
- Type55: `dict[str, BlockedWork]`
- Type56: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type57: `list[str] | tuple[str, ...]`
- Type58: `int | dict`
- Type59: `int | dict | str`
- Type60: `str | Path`
- Type61: `tuple[Path, ...]`
- Type62: `float | None`
- Type63: `tuple[Label, ...]`
- Type64: `list[tuple[int, str, str]]`
- Type65: `dict[str, list[str] | FactoryError]`
- Type66: `tuple[Path, list[dict]]`
- Type67: `tuple[Path, Path] | None`
- Type68: `tuple[Path, Path, dict | None]`

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
  deadlines: AgentShellLifecycleDeadlines, host: SessionHost) dict`
- Signature9: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None, model: str | None, effort: str | None, deadlines:
  AgentShellLifecycleDeadlines, host: SessionHost, channel: Channel) unknown`
- Signature10: `-__init__(workspace: Path, term_grace: float, role_environment:
  Callable[[ForgetfulConnection, str], dict[str, str]], missing_tools:
  Callable[[ForgetfulConnection], list[str]]) unknown`
- Signature11: `+validate_setup(connection: ForgetfulConnection, include_home_system_prompt: bool,
  include_memory_extension: bool) None`
- Signature12: `+prepare_roles(choices: InitialAgentChoices, execution_enabled: bool, repositories:
  Sequence[str], connection: ForgetfulConnection) None`
- Signature13: `+validate_worker_models(choices: InitialAgentChoices, repositories: Sequence[str],
  connection: ForgetfulConnection) None`
- Signature14: `-_write_agent(name: unknown, model: unknown, effort: unknown, description: unknown,
  children: unknown, resources: unknown) unknown`
- Signature15: `-__init__(records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts,
  ticketing: Ticketing) unknown`
- Signature16: `-_claim_indexes(inventory: list[dict], plans: list[dict], tasks: dict[int,
  list[dict]], identities: dict[str, str], alerts: WatcherAlerts) tuple[dict, dict] | None`
- Signature17: `-_dispose(work: CompletedWork, mapping: dict, claims: dict, references: dict,
  identities: dict[str, str], alerts: WatcherAlerts, report: unknown) bool`
- Signature18: `-_mapping_identity(plan_id: int, reference: str, mapping: dict, workspace: str |
  None) CleanupSet`
- Signature19: `-__init__(planning: PlanStore, workspace: Path, config: FactoryConfiguration,
  repositories: LocalRepositories, forge: Forge) unknown`
- Signature20: `-__init__(tracking: Ticketing, storage: ConfigurationStore, repositories:
  LocalRepositories, forge: Forge, team: AgentTeam, planning: PlanningSetup, tools:
  Callable[[ForgetfulConnection], Sequence[ToolInstaller]]) unknown`
- Signature21: `-__init__(planning: PlanStore, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, forge: Forge) unknown`
- Signature22: `-_setup_ownership(plan_id: int, issue: Ticket, context: dict, initial_mappings:
  list[dict]) tuple[list[dict], list[dict]]`
- Signature23: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature24: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature25: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature26: `-__init__(tracking: Ticketing, terminal: ForemanTerminal, scaffold: ScaffoldIssue,
  cleanup: CleanupCompleted) unknown`
- Signature27: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature28: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature29: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature30: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature31: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature32: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature33: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Ticket, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature34: `-_poll_sources(sources: tuple[TicketSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature35: `-_process_source(source: TicketSource, issues: tuple[Ticket, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature36: `-_baseline_source(source: TicketSource, issues: tuple[Ticket, ...], state:
  _WatchState, report: Callable[[str], None]) None`
- Signature37: `-_repository_for_source(config: FactoryConfiguration, source: TicketSource)
  RepositoryReference`
- Signature38: `-_include_pending_lookups(source: TicketSource, current: dict[str, Ticket],
  pending_lookup: dict[str, Ticket]) None`
- Signature39: `-_process_issues(issues: tuple[Ticket, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature40: `-_process_issue(issue: Ticket, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature41: `-_handle_intake_repository_problem(issue: Ticket, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature42: `-_handle_intake_read_problem(issue: Ticket, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature43: `-_handle_intake_scaffold_problem(issue: Ticket, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature44: `-_complete_intake(issue: Ticket, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature45: `-_submit(issue: Ticket, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature46: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature47: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature48: `+build_tools(workspace: Path, connection: ForgetfulConnection, term_grace: float)
  unknown`
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
- Signature69: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature70: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool,
  term_grace: float) unknown`
- Signature71: `+run_install(args: list[str], cwd: Path, term_grace: float, interactive: bool,
  extra_env: dict[str, str] | None) str`
- Signature72: `+run_owned(args: list[str], cwd: Path, env: dict[str, str], login: bool, timeout:
  float | None, term_grace: float) str`
- Signature73: `-_validate_registered_worktree(root: Path, target: Path, branch: str, path: str,
  match: dict) None`
- Signature74: `-_disposal_state(repository: str, branch: str, path: str, remote: str,
  target_branch: str) tuple[Path, Path, dict | None]`

## Extraction warnings

- `Unresolved or out-of-scope base: AgentTeam -> Protocol`
- `Unresolved or out-of-scope base: Channel -> Protocol`
- `Unresolved or out-of-scope base: CleanupMarkerError -> ValueError`
- `Unresolved or out-of-scope base: CleanupReceipts -> Protocol`
- `Unresolved or out-of-scope base: ConfigurationStore -> Protocol`
- `Unresolved or out-of-scope base: FactoryError -> Exception`
- `Unresolved or out-of-scope base: ForemanTerminal -> Protocol`
- `Unresolved or out-of-scope base: Forge -> Protocol`
- `Unresolved or out-of-scope base: LocalRepositories -> Protocol`
- `Unresolved or out-of-scope base: PlanStore -> Protocol`
- `Unresolved or out-of-scope base: PlanningSetup -> Protocol`
- `Unresolved or out-of-scope base: SessionHost -> Protocol`
- `Unresolved or out-of-scope base: Ticketing -> Protocol`
- `Unresolved or out-of-scope base: ToolInstaller -> Protocol`
- `Unresolved or out-of-scope base: WatchLease -> Protocol`
- `Unresolved or out-of-scope base: Worktrees -> Protocol`
- `Unresolved or out-of-scope base: _WorkAction -> Enum`
