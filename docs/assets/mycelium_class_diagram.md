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
Calls removed by test filtering: 5363. Type relationships removed: 106.

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
- `tests/test_architecture.py`: 30 source occurrences (test-path).
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
        +host: object
        +session: Type1
        +worker: Type2
        +worker_error: Type3
        +cleanup_known: bool
    }
    class c0002["src/forgetful_factory/agents/adapters/agentshell/controller.py"] {
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
    class c0003["src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0004["src/forgetful_factory/agents/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0005["ForemanOwner"] {
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
    class c0006["src/forgetful_factory/agents/adapters/agentshell/owner.py"] {
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
    class c0007["src/forgetful_factory/agents/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type5
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(Signature8)
    }
    class c0008["AgentShellRuntimeInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +project: unknown
        +term_grace: unknown
        -_inputs() Type6
        +absent() list[str]
        +unready() list[str]
        +ready() bool
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0009["AgentShellTerminal"] {
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
        +process: Type8
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
    class c0010["src/forgetful_factory/agents/adapters/agentshell/tmux_host.py"] {
        <<module>>
        +retain_identity(session: unknown, reply: unknown) None
        +pin_worker(target: unknown) int
    }
    class c0011["src/forgetful_factory/agents/adapters/pi/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        -_local_selection(value: object, field: str, message: str) str
        -_validate_agent(value: object) dict
        -_validate_roster(path: Path, value: object, agent_type: str) None
        -_validate_resources(value: object) None
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0012["PiAgentTeam"] {
        <<class>>
        -__init__(Signature10)
        +workspace: unknown
        +term_grace: unknown
        +role_environment: unknown
        +missing_tools: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type5
        -_model_catalogs: Type11
        -_managed_memory_selected: Type12
        +prepare_setup_guidance() None
        +validate_setup(Signature11)
        +validate_bundled_resources(include_memory_extension: bool) None
        -_install_resources() None
        -_protect_runtime() None
        +prepare() None
        +save_pi_choice() None
        +prepare_roles(Signature12)
        +validate_worker_models(Signature13)
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type13) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type3
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +begin_setup() None
        +validate_completion() None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0013["CoordinatorProfiles"] {
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
    class c0014["src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0015["src/forgetful_factory/agents/adapters/pi/native_home.py"] {
        <<module>>
        +saved_pi_home(workspace: Path) str
    }
    class c0016["ResourceUpdate"] {
        <<class>>
        +directory: Path
        +files: Type14
        +add: Type15
        +replace: Type15
        +edited: Type15
    }
    class c0017["src/forgetful_factory/agents/adapters/pi/role_resources.py"] {
        <<module>>
        -_digest(data: bytes) str
        +bundled_files() Type14
        +plan_update(directory: Path) ResourceUpdate
        -_back_up(update: ResourceUpdate, backups: Path) Path
        +apply_update(update: ResourceUpdate, backups: Path) Type13
    }
    class c0018["PiInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +directory: unknown
        +term_grace: unknown
        +absent() list[str]
        +unready() list[str]
        +ready(pi_home: str) bool
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0019["src/forgetful_factory/agents/adapters/pi/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type16) None
        -_walk_skill_directory(directory: Path, ancestors: Type17, files: Type16) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0020["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0021["AgentShellLifecycleDeadlines"] {
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
    class c0022["InitialAgentChoices"] {
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
        +implementation_skills: Type15
        +review_skills: Type15
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0023["src/forgetful_factory/agents/model.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type15
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0024["AgentTeam"] {
        <<class>>
        +prepare() None
        +prepare_setup_guidance() None
        +choose_pi_home(requested: Type3, confirm: Type18) str
        +save_pi_choice() None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type13) list[str]
        +prepare_roles(Signature12)
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type3
        +begin_setup() None
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +validate_completion() None
        +validate_bundled_resources(include_memory_extension: bool) None
    }
    class c0025["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0026["TerminalChannel"] {
        <<class>>
        -__init__(host: SessionHost) unknown
        +host: unknown
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0027["Channel"] {
        <<class>>
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0028["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_host() TmuxHost
        +build_channel() TerminalChannel
        +build_tools(Signature15)
        +build_team(workspace: Path, term_grace: float) PiAgentTeam
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +select_ticketing(config: FactoryConfiguration, command_timeout: float) Ticketing
        +build_watcher(Signature16)
        +prepare_foreman_launch(Signature17)
    }
    class c0029["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0030["src/forgetful_factory/cli/definition_of_done.py"] {
        <<module>>
        +agree_definition_of_done(workspace: Path, config: FactoryConfiguration) bool
        -_deployment_agreement(answer: str) str
    }
    class c0031["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0032["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature18)
        -_check_existing_connection(Signature19)
        -_connection(Signature20)
        -_prepare_foreman(Signature21)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type22, show_choices: bool, prompt: Type3) str
        -_select_model(Signature22)
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
        -_select_project(Signature23)
        -_owner_choices(Signature24)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature25)
        -_foreman_memory_choices(Signature26)
        -_managed_rest_mapping_available(connection: ForgetfulConnection) bool
        -_worker_choices(Signature27)
        -_complete_setup(Signature28)
        -_initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type5) None
        -_finish_existing_setup(Signature29)
        -_discover_worker_models(Signature30)
        -_validate_initial_model(Signature31)
        -_start_initial_setup(Signature32)
        -_initialise_locked(Signature33)
        -_launch_setup_foreman(Signature34)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0033["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0034["src/forgetful_factory/cli/resource_update.py"] {
        <<module>>
        -_report(update: unknown, force: bool) None
        +update_resources(Signature35)
    }
    class c0035["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type25) FactoryConfiguration
    }
    class c0036["FileCleanupReceipts"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +path: unknown
        +load() set[CleanupSet]
        -_load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0037["src/forgetful_factory/factory/adapters/cleanup_receipts.py"] {
        <<module>>
        -_unique_object(pairs: unknown) unknown
        -_resource(value: object) CleanupSet
    }
    class c0038["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type26
        +save(configuration: FactoryConfiguration) None
    }
    class c0039["src/forgetful_factory/factory/adapters/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0040["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0041["ObservedTerminal"] {
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
    class c0042["PlainWatchObservation"] {
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
    class c0043["src/forgetful_factory/factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type27
        -_read_discovery(workspace: Path) dict
        +unknown_status(source: str, observation: str) dict
        +plain_watch_status(workspace: Path) Type5
        +observe_plain_watch(workspace: Path, report_unavailable: Type29) Type28
    }
    class c0044["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type15
        +foreman_agent_file: str
        +repository: Type30
        +forgetful: Type21
        +execution_enabled: bool
    }
    class c0045["src/forgetful_factory/factory/model/configuration.py"] {
        <<module>>
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type15
    }
    class c0046["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: TicketSource
    }
    class c0047["IntakeProblem"] {
        <<class>>
    }
    class c0048["RepositoryProblem"] {
        <<class>>
    }
    class c0049["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature36)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0050["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0051["UncertainScaffold"] {
        <<class>>
    }
    class c0052["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type32
        +last_diagnostic: Type32
        +clear(subject: str) None
        +send(Signature37)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0053["src/forgetful_factory/factory/model/watcher_problems.py"] {
        <<module>>
        -_cleanup_recovery(code: str) str
    }
    class c0054["CleanupReceipts"] {
        <<class>>
        +load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0055["CleanupSet"] {
        <<class>>
        +workspace: str
        +backend: str
        +plan_id: int
        +external_ref: str
        +repository: str
        +local_dir: str
        +branch: str
        +path: str
        +overlaps(other: Type33) bool
    }
    class c0056["ConfigurationStore"] {
        <<class>>
        +load() Type26
        +save(configuration: FactoryConfiguration) None
    }
    class c0057["ToolInstaller"] {
        <<class>>
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0058["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0059["CleanupCompleted"] {
        <<class>>
        -__init__(Signature38)
        +records: unknown
        +ticketing: unknown
        +worktrees: unknown
        +owners: Type34
        +receipts: unknown
        +confirmed: set[CleanupSet]
        +cursor: Type35
        +poll(alerts: WatcherAlerts, report: unknown) None
        -_claim_indexes(Signature39)
        -_read_plans(inventory: list[dict], alerts: WatcherAlerts) Type38
        -_candidates(plans: list[dict], tasks: Type37, alerts: WatcherAlerts) Type39
        -_candidate(plan: dict, tasks: list[dict]) CompletedWork
        -_read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) None
        -_in_scope(plan: dict) bool
        -_repository_identities(alerts: WatcherAlerts) Type7
        -_keys(mapping: dict, identities: Type32) set[tuple]
        -_claims(tasks: list[dict], plan_id: int, claims: dict, identities: Type32) None
        -_task_mappings(task: dict) list[dict]
        -_validate_claim_mapping(mapping: object) None
        -_overlaps(mapping: dict, claims: dict) bool
        -_dispose(Signature40)
        -_order(work: CompletedWork, mapping: dict) tuple
        -_check_namespaces(mappings: list[dict], identities: Type32) None
        -_mapping_identity(Signature41)
        -_is_confirmed(plan_id: int, reference: str, mapping: dict, workspace: Type3) bool
        -_still_completed(work: CompletedWork) bool
    }
    class c0060["CompletedWork"] {
        <<class>>
        +plan_id: int
        +reference: str
        +task_id: int
        +mappings: list[dict]
    }
    class c0061["src/forgetful_factory/factory/services/cleanup_completed.py"] {
        <<module>>
        -_claim_path(value: str) str
    }
    class c0062["CleanupMarkerError"] {
        <<class>>
    }
    class c0063["src/forgetful_factory/factory/services/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict, forge: Forge, repository: RepositoryRef) Type40
    }
    class c0064["FactoryRecords"] {
        <<class>>
        -__init__(Signature42)
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
    class c0065["InitialiseFactory"] {
        <<class>>
        -__init__(Signature43)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +forge: unknown
        +team: unknown
        +planning: unknown
        +tools: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type42, confirm: Type43) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type20, labels: Type44) Type26
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type45
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type46
        -_ensure_label(source: TicketSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type47, save: bool) list[str]
    }
    class c0066["src/forgetful_factory/factory/services/initialise_factory.py"] {
        <<module>>
        +missing_tools(tools: Sequence[ToolInstaller]) list[str]
        -_reviewed_install(tools: Sequence[ToolInstaller], name: str) Type48
    }
    class c0067["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature44)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +records: unknown
        +check() None
        +check_repository(repository: RepositoryReference) None
        +prepare(issue: Ticket) Type5
        -_repository(source: TicketSource) RepositoryReference
        -_initial_mappings(issue: Ticket) list[dict]
        +preflight(issue: Ticket) list[dict]
        -_prepare_plan(issue: Ticket, plan: dict, initial_mappings: list[dict]) Type5
        -_setup_ownership(Signature45)
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature46)
        +lookup(issue: Ticket) Type2
        -_create_plan(issue: Ticket) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type51, task_ids: Type31) Type50
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature47)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_is_unfinished_factory_plan(summary: dict, prefixes: set[str]) bool
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_validated_mapping(Signature48)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0068["src/forgetful_factory/factory/services/scaffold_issue.py"] {
        <<module>>
        +worktree_name(ticket: Ticket) str
    }
    class c0069["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type2
        +issue: Type51
        +task_ids: Type31
        +recovered: bool
        +setup_paths: Type15
        +setup_cause: Type3
    }
    class c0070["WatchFactory"] {
        <<class>>
        -__init__(Signature49)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +cleanup: unknown
        +run(Signature50)
        -_watch(Signature51)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type29) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature52)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type29) Type54
        -_recover_work(Signature53)
        -_handle_recovery_repository_problem(Signature54)
        -_handle_recovery_read_problem(Signature55)
        -_remember_task_ids(work: BlockedWork, task_ids: Type31) None
        -_complete_recovery(Signature56)
        -_poll_sources(Signature57)
        -_process_source(Signature58)
        -_baseline_source(Signature59)
        -_repository_for_source(Signature60)
        -_include_pending_lookups(Signature61)
        -_process_issues(Signature62)
        -_skip_issue(issue: Ticket, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature63)
        -_handle_intake_repository_problem(Signature64)
        -_handle_intake_read_problem(Signature65)
        -_handle_intake_scaffold_problem(Signature66)
        -_complete_intake(Signature67)
        -_sole_task_id(task_ids: Type31) Type2
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature68)
        -_read_issues(source: TicketSource, labels: Type15, alerts: WatcherAlerts) Type59
    }
    class c0071["_WatchState"] {
        <<class>>
        +seen: Type32
        +baseline: Type32
        +baselined: set[TicketSource]
        +blocked: Type60
        +pending_lookup: Type57
        +known: Type60
        +recovered: set[str]
        +pending_repositories: Type45
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0072["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
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
        -_environment(connection: ForgetfulConnection) Type32
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
        -_selected() Type3
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
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
        +plans(external_ref: Type3) list[dict]
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
        +database: Type3
        +server: Type3
        +project_id: Type2
        +validate() None
        -_validate_server() None
    }
    class c0084["src/forgetful_factory/planning/model.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type21
    }
    class c0085["PlanStore"] {
        <<class>>
        +check() None
        +plans(external_ref: Type3) list[dict]
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
        +describe(name: str) Type3
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
        +run_command(arguments: list[str], timeout: float, env: Type7, stdin: Type2) str
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
        +install_environment(extra: Type7) Type32
        +run_install(Signature71)
        +check_uv(workspace: Path, term_grace: float) None
        +require_manager(manager: str) None
        +install_locks(directory: Path, names: Type15) str
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
        +list_open(source: TicketSource, labels: Type15) Type56
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
        +list_open(source: TicketSource, labels: Type15) Type56
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
        -__init__(code: str, diagnostic: str, path: Type3) unknown
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
    c0000 ..> c0009 : close() calls close()
    c0000 ..> c0093 : 2 relationships (see list)
    c0000 ..> c0101 : 2 relationships (see list)
    c0002 ..> c0000 : 5 relationships (see list)
    c0002 ..> c0001 : serve() constructs SessionState
    c0002 ..> c0002 : 16 relationships (see list)
    c0002 ..> c0010 : 2 relationships (see list)
    c0002 ..> c0080 : 4 relationships (see list)
    c0003 ..> c0093 : runtime_directory() constructs FactoryError
    c0003 ..> c0096 : runtime_directory() calls check_real_path()
    c0004 ..> c0012 : main() calls list_models()
    c0005 ..> c0000 : 11 relationships (see list)
    c0005 ..> c0005 : 27 relationships (see list)
    c0005 ..> c0006 : 2 relationships (see list)
    c0005 ..> c0021 : 2 relationships (see list)
    c0005 ..> c0039 : _apply_controller_problem() calls quote()
    c0005 ..> c0080 : 2 relationships (see list)
    c0005 ..> c0093 : 10 relationships (see list)
    c0005 ..> c0096 : save() calls replace_generated_json()
    c0006 ..> c0000 : 3 relationships (see list)
    c0006 ..> c0003 : _prepare_owner_startup() calls runtime_directory()
    c0006 ..> c0005 : 3 relationships (see list)
    c0006 ..> c0006 : 5 relationships (see list)
    c0006 ..> c0007 : _prepare_owner_startup() calls read_state()
    c0006 ..> c0039 : _acquire_owner_lock() calls quote()
    c0006 ..> c0080 : main() calls create_task()
    c0006 ..> c0093 : 3 relationships (see list)
    c0007 ..> c0000 : 2 relationships (see list)
    c0007 ..> c0003 : 3 relationships (see list)
    c0007 ..> c0005 : start_owner() calls run()
    c0007 ..> c0007 : 3 relationships (see list)
    c0007 ..> c0021 : 2 relationships (see list)
    c0007 ..> c0039 : request() calls quote()
    c0007 ..> c0088 : start_owner() calls spec()
    c0007 ..> c0091 : type in start_owner
    c0007 ..> c0093 : 4 relationships (see list)
    c0007 ..> c0096 : read_state() calls read_generated_json()
    c0008 ..> c0008 : 3 relationships (see list)
    c0008 ..> c0093 : install() constructs FactoryError
    c0008 ..> c0095 : 5 relationships (see list)
    c0009 ..> c0000 : close() calls close()
    c0009 ..> c0009 : 5 relationships (see list)
    c0009 ..> c0021 : 2 relationships (see list)
    c0009 ..> c0026 : startup_hint() calls how_to_reach()
    c0009 ..> c0027 : type in __init__
    c0009 ..> c0088 : start() calls spec()
    c0009 ..> c0091 : type in __init__
    c0009 ..> c0093 : 4 relationships (see list)
    c0009 ..> c0101 : 3 relationships (see list)
    c0010 ..> c0000 : pin_worker() calls close()
    c0011 ..> c0011 : 8 relationships (see list)
    c0011 ..> c0093 : 2 relationships (see list)
    c0011 ..> c0099 : 4 relationships (see list)
    c0012 ..> c0011 : selected_launch() calls foreman_launch()
    c0012 ..> c0012 : 20 relationships (see list)
    c0012 ..> c0013 : 4 relationships (see list)
    c0012 ..> c0015 : pi_home() calls saved_pi_home()
    c0012 ..> c0017 : _install_resources() calls bundled_files()
    c0012 ..> c0019 : selected_launch() calls selected_skill_files()
    c0012 ..> c0022 : 2 relationships (see list)
    c0012 ..> c0036 : choose_pi_home() calls confirm()
    c0012 ..> c0039 : require_pi_home() calls quote()
    c0012 ..> c0066 : validate_setup() calls missing_tools()
    c0012 ..> c0078 : list_models() calls role_environment()
    c0012 ..> c0083 : 7 relationships (see list)
    c0012 ..> c0093 : 13 relationships (see list)
    c0012 ..> c0094 : require_pi_home() calls executable_path()
    c0012 ..> c0096 : 10 relationships (see list)
    c0012 ..> c0098 : list_models() calls run_owned()
    c0013 ..> c0012 : prepare() calls prepare()
    c0013 ..> c0013 : 3 relationships (see list)
    c0013 ..> c0014 : prepare() calls selected_resources()
    c0013 ..> c0020 : __init__() constructs WorkerProfiles
    c0013 ..> c0093 : 4 relationships (see list)
    c0013 ..> c0096 : 5 relationships (see list)
    c0015 ..> c0093 : saved_pi_home() constructs FactoryError
    c0015 ..> c0096 : saved_pi_home() calls read_generated_json()
    c0017 ..> c0016 : 4 relationships (see list)
    c0017 ..> c0017 : 4 relationships (see list)
    c0017 ..> c0093 : 2 relationships (see list)
    c0017 ..> c0096 : plan_update() calls check_real_path()
    c0018 ..> c0015 : unready() calls saved_pi_home()
    c0018 ..> c0018 : unready() calls ready()
    c0018 ..> c0094 : 2 relationships (see list)
    c0018 ..> c0095 : 6 relationships (see list)
    c0018 ..> c0098 : ready() calls run_owned()
    c0019 ..> c0000 : _add_skill_file() calls close()
    c0019 ..> c0019 : 3 relationships (see list)
    c0019 ..> c0093 : 3 relationships (see list)
    c0020 ..> c0022 : type in prepare
    c0020 ..> c0042 : prepare() calls update()
    c0020 ..> c0096 : 3 relationships (see list)
    c0021 ..> c0099 : __post_init__() calls positive_duration()
    c0023 ..> c0022 : 3 relationships (see list)
    c0023 ..> c0023 : 4 relationships (see list)
    c0023 ..> c0093 : 5 relationships (see list)
    c0023 ..> c0099 : 4 relationships (see list)
    c0024 ..> c0022 : type in prepare_roles
    c0024 ..> c0083 : 4 relationships (see list)
    c0026 ..> c0088 : 2 relationships (see list)
    c0026 ..> c0091 : type in __init__
    c0028 ..> c0008 : build_tools() constructs AgentShellRuntimeInstall
    c0028 ..> c0009 : build_watcher() constructs AgentShellTerminal
    c0028 ..> c0012 : 6 relationships (see list)
    c0028 ..> c0018 : build_tools() constructs PiInstall
    c0028 ..> c0026 : 2 relationships (see list)
    c0028 ..> c0028 : 8 relationships (see list)
    c0028 ..> c0029 : 4 relationships (see list)
    c0028 ..> c0036 : build_watcher() constructs FileCleanupReceipts
    c0028 ..> c0038 : build_initialiser() constructs TomlConfigurationStore
    c0028 ..> c0041 : build_watcher() constructs ObservedTerminal
    c0028 ..> c0044 : 3 relationships (see list)
    c0028 ..> c0059 : build_watcher() constructs CleanupCompleted
    c0028 ..> c0065 : 2 relationships (see list)
    c0028 ..> c0066 : build_team() calls missing_tools()
    c0028 ..> c0067 : build_watcher() constructs ScaffoldIssue
    c0028 ..> c0070 : 2 relationships (see list)
    c0028 ..> c0073 : 2 relationships (see list)
    c0028 ..> c0078 : prepare_foreman_launch() calls role_environment()
    c0028 ..> c0079 : build_tools() constructs ForgetfulInstall
    c0028 ..> c0080 : build_watcher() constructs ForgetfulPlanStore
    c0028 ..> c0082 : build_initialiser() constructs ForgetfulSetup
    c0028 ..> c0083 : type in build_tools
    c0028 ..> c0088 : 2 relationships (see list)
    c0028 ..> c0089 : build_tools() constructs TmuxInstall
    c0028 ..> c0093 : 3 relationships (see list)
    c0028 ..> c0102 : 3 relationships (see list)
    c0028 ..> c0106 : type in select_ticketing
    c0028 ..> c0107 : 2 relationships (see list)
    c0028 ..> c0109 : build_watcher() constructs GitWorktrees
    c0029 --> c0021 : field agentshell
    c0029 ..> c0099 : __post_init__() calls positive_duration()
    c0030 ..> c0030 : agree_definition_of_done() calls _deployment_agreement()
    c0030 ..> c0044 : type in agree_definition_of_done
    c0030 ..> c0093 : 2 relationships (see list)
    c0030 ..> c0096 : 2 relationships (see list)
    c0031 --> c0044 : field config
    c0031 --> c0083 : field connection
    c0032 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0032 ..> c0005 : _watch_locked() calls run()
    c0032 ..> c0007 : 12 relationships (see list)
    c0032 ..> c0012 : 13 relationships (see list)
    c0032 ..> c0022 : 7 relationships (see list)
    c0032 ..> c0023 : _start_initial_setup() calls validate_initial_agents()
    c0032 ..> c0028 : 9 relationships (see list)
    c0032 ..> c0029 : 9 relationships (see list)
    c0032 ..> c0030 : 2 relationships (see list)
    c0032 ..> c0031 : 3 relationships (see list)
    c0032 ..> c0032 : 55 relationships (see list)
    c0032 ..> c0033 : _select_numbered() calls parse_numbered_selection()
    c0032 ..> c0034 : main() calls update_resources()
    c0032 ..> c0035 : 3 relationships (see list)
    c0032 ..> c0036 : _initialise_locked() calls load()
    c0032 ..> c0039 : 6 relationships (see list)
    c0032 ..> c0040 : 6 relationships (see list)
    c0032 ..> c0042 : _prompt_workers() calls update()
    c0032 ..> c0043 : 4 relationships (see list)
    c0032 ..> c0044 : 4 relationships (see list)
    c0032 ..> c0045 : _connection() calls validate()
    c0032 ..> c0065 : 17 relationships (see list)
    c0032 ..> c0076 : _complete_setup() calls uses_browser_login()
    c0032 ..> c0077 : 2 relationships (see list)
    c0032 ..> c0083 : 7 relationships (see list)
    c0032 ..> c0093 : 20 relationships (see list)
    c0032 ..> c0096 : _discover_worker_models() calls check_real_path()
    c0032 ..> c0101 : _watch_locked() calls watch_stop_scope()
    c0033 ..> c0093 : parse_numbered_selection() constructs FactoryError
    c0034 ..> c0002 : update_resources() calls ready()
    c0034 ..> c0007 : update_resources() calls read_state()
    c0034 ..> c0008 : 2 relationships (see list)
    c0034 ..> c0012 : update_resources() calls validate_bundled_resources()
    c0034 ..> c0017 : 2 relationships (see list)
    c0034 ..> c0028 : update_resources() calls build_team()
    c0034 ..> c0029 : type in update_resources
    c0034 ..> c0034 : update_resources() calls _report()
    c0034 ..> c0040 : 2 relationships (see list)
    c0034 ..> c0093 : 2 relationships (see list)
    c0035 ..> c0036 : load_configuration() calls load()
    c0035 ..> c0038 : load_configuration() constructs TomlConfigurationStore
    c0035 ..> c0044 : type in load_configuration
    c0035 ..> c0093 : load_configuration() constructs FactoryError
    c0036 ..> c0000 : _load() calls close()
    c0036 ..> c0036 : 2 relationships (see list)
    c0036 ..> c0037 : _load() calls _resource()
    c0036 ..> c0055 : 3 relationships (see list)
    c0036 ..> c0093 : 2 relationships (see list)
    c0036 ..> c0096 : 2 relationships (see list)
    c0036 ..> c0101 : confirm() calls check_watch_stop()
    c0037 ..> c0055 : 2 relationships (see list)
    c0038 ..> c0000 : 2 relationships (see list)
    c0038 ..> c0036 : load() calls load()
    c0038 ..> c0039 : save() calls quote()
    c0038 ..> c0044 : 2 relationships (see list)
    c0038 ..> c0045 : load() calls from_mapping()
    c0038 ..> c0093 : 2 relationships (see list)
    c0040 ..> c0000 : _hold_directory() calls close()
    c0040 ..> c0040 : hold() calls _hold_directory()
    c0040 ..> c0093 : _hold_directory() constructs FactoryError
    c0041 ..> c0000 : 5 relationships (see list)
    c0041 ..> c0025 : type in __init__
    c0041 ..> c0042 : 3 relationships (see list)
    c0041 ..> c0043 : __init__() calls unknown_status()
    c0042 ..> c0041 : 2 relationships (see list)
    c0042 ..> c0042 : 9 relationships (see list)
    c0042 ..> c0043 : 6 relationships (see list)
    c0042 ..> c0093 : __enter__() constructs FactoryError
    c0042 ..> c0096 : 3 relationships (see list)
    c0043 ..> c0042 : 4 relationships (see list)
    c0043 ..> c0043 : 8 relationships (see list)
    c0043 ..> c0096 : _read_discovery() calls check_real_path()
    c0044 --> c0046 : field repository
    c0044 --> c0083 : field forgetful
    c0045 ..> c0044 : 3 relationships (see list)
    c0045 ..> c0045 : from_mapping() calls validate()
    c0045 ..> c0046 : from_mapping() constructs RepositoryReference
    c0045 ..> c0083 : validate() calls validate()
    c0045 ..> c0084 : from_mapping() calls connection_from_mapping()
    c0045 ..> c0093 : 2 relationships (see list)
    c0045 ..> c0099 : 2 relationships (see list)
    c0045 ..> c0105 : from_mapping() constructs TicketSource
    c0046 --> c0105 : field work_source
    c0047 --|> c0049 : inherits
    c0048 --|> c0049 : inherits
    c0049 --|> c0093 : inherits
    c0050 --|> c0049 : inherits
    c0051 --|> c0049 : inherits
    c0052 ..> c0000 : 2 relationships (see list)
    c0052 ..> c0053 : send() calls _cleanup_recovery()
    c0052 ..> c0093 : type in send
    c0054 ..> c0055 : 2 relationships (see list)
    c0056 ..> c0044 : 2 relationships (see list)
    c0059 ..> c0000 : 5 relationships (see list)
    c0059 ..> c0036 : 2 relationships (see list)
    c0059 ..> c0042 : 4 relationships (see list)
    c0059 ..> c0049 : 7 relationships (see list)
    c0059 ..> c0052 : 10 relationships (see list)
    c0059 ..> c0054 : type in __init__
    c0059 --> c0055 : field confirmed
    c0059 ..> c0055 : 3 relationships (see list)
    c0059 ..> c0059 : 27 relationships (see list)
    c0059 ..> c0060 : 6 relationships (see list)
    c0059 ..> c0061 : 6 relationships (see list)
    c0059 ..> c0064 : 9 relationships (see list)
    c0059 ..> c0080 : 7 relationships (see list)
    c0059 ..> c0093 : type in _read_problem
    c0059 ..> c0102 : _in_scope() calls is_key()
    c0059 ..> c0106 : type in __init__
    c0059 ..> c0109 : 4 relationships (see list)
    c0059 ..> c0114 : type in __init__
    c0063 ..> c0062 : validate_cleanup_marker() constructs CleanupMarkerError
    c0063 ..> c0073 : validate_cleanup_marker() calls is_change_request()
    c0063 ..> c0074 : type in validate_cleanup_marker
    c0063 ..> c0075 : type in validate_cleanup_marker
    c0064 ..> c0044 : type in __init__
    c0064 ..> c0046 : 3 relationships (see list)
    c0064 ..> c0048 : 2 relationships (see list)
    c0064 ..> c0049 : 5 relationships (see list)
    c0064 ..> c0064 : 2 relationships (see list)
    c0064 ..> c0073 : check_source() calls repository()
    c0064 ..> c0074 : type in check_source
    c0064 ..> c0075 : type in __init__
    c0064 ..> c0080 : ownership() calls tasks()
    c0064 ..> c0085 : type in __init__
    c0064 ..> c0104 : 2 relationships (see list)
    c0064 ..> c0105 : snapshot() constructs TicketSource
    c0064 ..> c0107 : check_repository() calls origin()
    c0064 ..> c0111 : type in __init__
    c0065 ..> c0005 : initialise() calls save()
    c0065 ..> c0008 : prepare_foreman() calls install()
    c0065 ..> c0012 : prepare_foreman() calls prepare()
    c0065 ..> c0024 : type in __init__
    c0065 ..> c0036 : 2 relationships (see list)
    c0065 ..> c0044 : 6 relationships (see list)
    c0065 ..> c0045 : 3 relationships (see list)
    c0065 ..> c0046 : 2 relationships (see list)
    c0065 ..> c0056 : type in __init__
    c0065 ..> c0057 : type in __init__
    c0065 ..> c0065 : 3 relationships (see list)
    c0065 ..> c0066 : 2 relationships (see list)
    c0065 ..> c0067 : check_foreman() calls check()
    c0065 ..> c0073 : 2 relationships (see list)
    c0065 ..> c0075 : type in __init__
    c0065 ..> c0077 : check_foreman() calls login()
    c0065 ..> c0083 : 2 relationships (see list)
    c0065 ..> c0087 : type in __init__
    c0065 ..> c0093 : 5 relationships (see list)
    c0065 ..> c0102 : 4 relationships (see list)
    c0065 ..> c0103 : 2 relationships (see list)
    c0065 ..> c0105 : 3 relationships (see list)
    c0065 ..> c0106 : type in __init__
    c0065 ..> c0107 : 3 relationships (see list)
    c0065 ..> c0111 : type in __init__
    c0066 ..> c0008 : 3 relationships (see list)
    c0066 ..> c0057 : 2 relationships (see list)
    c0067 ..> c0042 : recover() calls snapshot()
    c0067 ..> c0044 : type in __init__
    c0067 ..> c0046 : 3 relationships (see list)
    c0067 ..> c0047 : preflight() constructs IntakeProblem
    c0067 ..> c0049 : 8 relationships (see list)
    c0067 ..> c0050 : 5 relationships (see list)
    c0067 ..> c0051 : 5 relationships (see list)
    c0067 ..> c0063 : _ensure_mapping() calls validate_cleanup_marker()
    c0067 ..> c0064 : 11 relationships (see list)
    c0067 ..> c0065 : preflight() calls inspect()
    c0067 ..> c0067 : 22 relationships (see list)
    c0067 ..> c0068 : _initial_mappings() calls worktree_name()
    c0067 ..> c0075 : type in __init__
    c0067 ..> c0077 : check() calls check()
    c0067 ..> c0080 : 12 relationships (see list)
    c0067 ..> c0085 : type in __init__
    c0067 ..> c0093 : _is_unfinished_factory_plan() constructs FactoryError
    c0067 ..> c0104 : 8 relationships (see list)
    c0067 ..> c0105 : type in _repository
    c0067 ..> c0109 : 3 relationships (see list)
    c0067 ..> c0111 : type in __init__
    c0067 ..> c0114 : type in __init__
    c0068 ..> c0104 : type in worktree_name
    c0069 --> c0104 : field issue
    c0070 ..> c0000 : 15 relationships (see list)
    c0070 ..> c0012 : _process_issue() calls prepare()
    c0070 ..> c0025 : type in __init__
    c0070 ..> c0044 : 4 relationships (see list)
    c0070 ..> c0046 : 5 relationships (see list)
    c0070 ..> c0048 : 2 relationships (see list)
    c0070 ..> c0049 : 3 relationships (see list)
    c0070 ..> c0050 : 2 relationships (see list)
    c0070 ..> c0052 : 28 relationships (see list)
    c0070 ..> c0059 : 2 relationships (see list)
    c0070 ..> c0064 : _check_pending_repositories() calls check_repository()
    c0070 ..> c0067 : 6 relationships (see list)
    c0070 ..> c0069 : 13 relationships (see list)
    c0070 ..> c0070 : 35 relationships (see list)
    c0070 ..> c0071 : 19 relationships (see list)
    c0070 ..> c0072 : 2 relationships (see list)
    c0070 ..> c0093 : _read_issues() constructs FactoryError
    c0070 ..> c0101 : 3 relationships (see list)
    c0070 ..> c0102 : _read_issues() calls list_open()
    c0070 ..> c0104 : 13 relationships (see list)
    c0070 ..> c0105 : 7 relationships (see list)
    c0070 ..> c0106 : type in __init__
    c0071 --> c0046 : field pending_repositories
    c0071 --> c0069 : 2 relationships (see list)
    c0071 --> c0104 : field pending_lookup
    c0071 --> c0105 : field baselined
    c0073 ..> c0074 : 3 relationships (see list)
    c0073 ..> c0093 : repository() constructs FactoryError
    c0075 ..> c0074 : 2 relationships (see list)
    c0076 ..> c0007 : uses_browser_login() calls request()
    c0076 ..> c0083 : type in uses_browser_login
    c0077 ..> c0077 : 7 relationships (see list)
    c0077 ..> c0078 : 2 relationships (see list)
    c0077 ..> c0083 : 7 relationships (see list)
    c0077 ..> c0093 : 5 relationships (see list)
    c0077 ..> c0098 : 2 relationships (see list)
    c0077 ..> c0101 : command() calls check_watch_stop()
    c0078 ..> c0042 : role_environment() calls update()
    c0078 ..> c0083 : type in role_environment
    c0078 ..> c0094 : role_environment() calls executable_path()
    c0079 ..> c0079 : 6 relationships (see list)
    c0079 ..> c0083 : type in __init__
    c0079 ..> c0093 : _python() constructs FactoryError
    c0079 ..> c0094 : _selected() calls executable_path()
    c0079 ..> c0095 : 7 relationships (see list)
    c0079 ..> c0098 : _python() calls run_owned()
    c0080 ..> c0067 : check() calls check()
    c0080 ..> c0077 : 2 relationships (see list)
    c0080 ..> c0080 : 12 relationships (see list)
    c0080 ..> c0081 : 3 relationships (see list)
    c0080 ..> c0083 : type in __init__
    c0080 ..> c0086 : 4 relationships (see list)
    c0082 ..> c0067 : check() calls check()
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
    c0088 ..> c0005 : enter() calls run()
    c0088 ..> c0093 : enter() constructs FactoryError
    c0089 ..> c0090 : 2 relationships (see list)
    c0089 ..> c0093 : install() constructs FactoryError
    c0089 ..> c0094 : absent() calls executable_path()
    c0089 ..> c0095 : 2 relationships (see list)
    c0092 ..> c0005 : run_command() calls run()
    c0092 ..> c0093 : run_command() constructs FactoryError
    c0092 ..> c0101 : run_command() calls check_watch_stop()
    c0095 ..> c0093 : 6 relationships (see list)
    c0095 ..> c0095 : 4 relationships (see list)
    c0095 ..> c0096 : install_locks() calls write_new()
    c0095 ..> c0098 : 3 relationships (see list)
    c0096 ..> c0000 : 2 relationships (see list)
    c0096 ..> c0036 : read_generated_json() calls load()
    c0096 ..> c0093 : 6 relationships (see list)
    c0096 ..> c0096 : 9 relationships (see list)
    c0098 ..> c0000 : 2 relationships (see list)
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
    c0109 ..> c0039 : _network_git() calls quote()
    c0109 ..> c0052 : begin_cleanup_cycle() calls clear()
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

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/agents/adapters/agentshell/borrowed_terminal.py`:10
- c0001: `SessionState` — `src/forgetful_factory/agents/adapters/agentshell/controller.py`:110
- c0002: `src/forgetful_factory/agents/adapters/agentshell/controller.py` —
  `src/forgetful_factory/agents/adapters/agentshell/controller.py`:1
- c0003: `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py` —
  `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py`:1
- c0004: `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py`:1
- c0005: `ForemanOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner.py`:104
- c0006: `src/forgetful_factory/agents/adapters/agentshell/owner.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner.py`:1
- c0007: `src/forgetful_factory/agents/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:1
- c0008: `AgentShellRuntimeInstall` —
  `src/forgetful_factory/agents/adapters/agentshell/runtime_install.py`:24
- c0009: `AgentShellTerminal` — `src/forgetful_factory/agents/adapters/agentshell/terminal.py`:17
- c0010: `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py` —
  `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py`:1
- c0011: `src/forgetful_factory/agents/adapters/pi/agent_definitions.py` —
  `src/forgetful_factory/agents/adapters/pi/agent_definitions.py`:1
- c0012: `PiAgentTeam` — `src/forgetful_factory/agents/adapters/pi/agent_team.py`:46
- c0013: `CoordinatorProfiles` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:29
- c0014: `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:1
- c0015: `src/forgetful_factory/agents/adapters/pi/native_home.py` —
  `src/forgetful_factory/agents/adapters/pi/native_home.py`:1
- c0016: `ResourceUpdate` — `src/forgetful_factory/agents/adapters/pi/role_resources.py`:39
- c0017: `src/forgetful_factory/agents/adapters/pi/role_resources.py` —
  `src/forgetful_factory/agents/adapters/pi/role_resources.py`:1
- c0018: `PiInstall` — `src/forgetful_factory/agents/adapters/pi/runtime_install.py`:22
- c0019: `src/forgetful_factory/agents/adapters/pi/selected_skills.py` —
  `src/forgetful_factory/agents/adapters/pi/selected_skills.py`:1
- c0020: `WorkerProfiles` — `src/forgetful_factory/agents/adapters/pi/worker_profiles.py`:16
- c0021: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/agents/model.py`:131
- c0022: `InitialAgentChoices` — `src/forgetful_factory/agents/model.py`:9
- c0023: `src/forgetful_factory/agents/model.py` — `src/forgetful_factory/agents/model.py`:1
- c0024: `AgentTeam` — `src/forgetful_factory/agents/ports.py`:21
- c0025: `ForemanTerminal` — `src/forgetful_factory/agents/ports.py`:9
- c0026: `TerminalChannel` — `src/forgetful_factory/channels/adapters/terminal.py`:8
- c0027: `Channel` — `src/forgetful_factory/channels/ports.py`:4
- c0028: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0029: `DeadlinePolicy` — `src/forgetful_factory/cli/deadlines.py`:9
- c0030: `src/forgetful_factory/cli/definition_of_done.py` —
  `src/forgetful_factory/cli/definition_of_done.py`:1
- c0031: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:752
- c0032: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0033: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0034: `src/forgetful_factory/cli/resource_update.py` —
  `src/forgetful_factory/cli/resource_update.py`:1
- c0035: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0036: `FileCleanupReceipts` — `src/forgetful_factory/factory/adapters/cleanup_receipts.py`:40
- c0037: `src/forgetful_factory/factory/adapters/cleanup_receipts.py` —
  `src/forgetful_factory/factory/adapters/cleanup_receipts.py`:1
- c0038: `TomlConfigurationStore` —
  `src/forgetful_factory/factory/adapters/toml_configuration.py`:17
- c0039: `src/forgetful_factory/factory/adapters/toml_configuration.py` —
  `src/forgetful_factory/factory/adapters/toml_configuration.py`:1
- c0040: `WorkspaceWatchLease` — `src/forgetful_factory/factory/adapters/watch_lease.py`:10
- c0041: `ObservedTerminal` — `src/forgetful_factory/factory/adapters/watch_status.py`:252
- c0042: `PlainWatchObservation` — `src/forgetful_factory/factory/adapters/watch_status.py`:129
- c0043: `src/forgetful_factory/factory/adapters/watch_status.py` —
  `src/forgetful_factory/factory/adapters/watch_status.py`:1
- c0044: `FactoryConfiguration` — `src/forgetful_factory/factory/model/configuration.py`:11
- c0045: `src/forgetful_factory/factory/model/configuration.py` —
  `src/forgetful_factory/factory/model/configuration.py`:1
- c0046: `RepositoryReference` — `src/forgetful_factory/factory/model/repositories.py`:7
- c0047: `IntakeProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:143
- c0048: `RepositoryProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:139
- c0049: `ScaffoldProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:119
- c0050: `ScaffoldReadProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:135
- c0051: `UncertainScaffold` — `src/forgetful_factory/factory/model/watcher_problems.py`:147
- c0052: `WatcherAlerts` — `src/forgetful_factory/factory/model/watcher_problems.py`:151
- c0053: `src/forgetful_factory/factory/model/watcher_problems.py` —
  `src/forgetful_factory/factory/model/watcher_problems.py`:1
- c0054: `CleanupReceipts` — `src/forgetful_factory/factory/ports.py`:37
- c0055: `CleanupSet` — `src/forgetful_factory/factory/ports.py`:20
- c0056: `ConfigurationStore` — `src/forgetful_factory/factory/ports.py`:9
- c0057: `ToolInstaller` — `src/forgetful_factory/factory/ports.py`:45
- c0058: `WatchLease` — `src/forgetful_factory/factory/ports.py`:15
- c0059: `CleanupCompleted` — `src/forgetful_factory/factory/services/cleanup_completed.py`:37
- c0060: `CompletedWork` — `src/forgetful_factory/factory/services/cleanup_completed.py`:22
- c0061: `src/forgetful_factory/factory/services/cleanup_completed.py` —
  `src/forgetful_factory/factory/services/cleanup_completed.py`:1
- c0062: `CleanupMarkerError` — `src/forgetful_factory/factory/services/cleanup_marker.py`:11
- c0063: `src/forgetful_factory/factory/services/cleanup_marker.py` —
  `src/forgetful_factory/factory/services/cleanup_marker.py`:1
- c0064: `FactoryRecords` — `src/forgetful_factory/factory/services/factory_records.py`:16
- c0065: `InitialiseFactory` — `src/forgetful_factory/factory/services/initialise_factory.py`:37
- c0066: `src/forgetful_factory/factory/services/initialise_factory.py` —
  `src/forgetful_factory/factory/services/initialise_factory.py`:1
- c0067: `ScaffoldIssue` — `src/forgetful_factory/factory/services/scaffold_issue.py`:37
- c0068: `src/forgetful_factory/factory/services/scaffold_issue.py` —
  `src/forgetful_factory/factory/services/scaffold_issue.py`:1
- c0069: `BlockedWork` — `src/forgetful_factory/factory/services/watch_factory.py`:27
- c0070: `WatchFactory` — `src/forgetful_factory/factory/services/watch_factory.py`:59
- c0071: `_WatchState` — `src/forgetful_factory/factory/services/watch_factory.py`:38
- c0072: `_WorkAction` — `src/forgetful_factory/factory/services/watch_factory.py`:52
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

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0009: `close() calls close()`
- c0000 ..> c0093: `_request() constructs FactoryError`
- c0000 ..> c0093: `wait() constructs FactoryError`
- c0000 ..> c0101: `_request() calls check_watch_stop()`
- c0000 ..> c0101: `wait() calls check_watch_stop()`
- c0002 ..> c0000: `close_session() calls close()`
- c0002 ..> c0000: `control() calls close()`
- c0002 ..> c0000: `control() calls wait()`
- c0002 ..> c0000: `resume_exit_observation() calls wait()`
- c0002 ..> c0000: `supervise_session() calls wait()`
- c0002 ..> c0001: `serve() constructs SessionState`
- c0002 ..> c0002: `build_shell() calls runtime()`
- c0002 ..> c0002: `control() calls serve()`
- c0002 ..> c0002: `interact() calls ready()`
- c0002 ..> c0002: `main() calls control()`
- c0002 ..> c0002: `open_session() calls capture_worker()`
- c0002 ..> c0002: `replace_failed_exit_task() calls resume_exit_observation()`
- c0002 ..> c0002: `serve() calls build_shell()`
- c0002 ..> c0002: `serve() calls close_session()`
- c0002 ..> c0002: `serve() calls load_host()`
- c0002 ..> c0002: `serve() calls open_session()`
- c0002 ..> c0002: `serve() calls supervise_session()`
- c0002 ..> c0002: `serve() calls validate_launch_config()`
- c0002 ..> c0002: `supervise_session() calls cancel_tasks()`
- c0002 ..> c0002: `supervise_session() calls interact()`
- c0002 ..> c0002: `supervise_session() calls replace_failed_exit_task()`
- c0002 ..> c0002: `supervise_session() calls worker_exited()`
- c0002 ..> c0010: `capture_worker() calls pin_worker()`
- c0002 ..> c0010: `supervise_session() calls retain_identity()`
- c0002 ..> c0080: `control() calls create_task()`
- c0002 ..> c0080: `main() calls create_task()`
- c0002 ..> c0080: `replace_failed_exit_task() calls create_task()`
- c0002 ..> c0080: `supervise_session() calls create_task()`
- c0003 ..> c0093: `runtime_directory() constructs FactoryError`
- c0003 ..> c0096: `runtime_directory() calls check_real_path()`
- c0004 ..> c0012: `main() calls list_models()`
- c0005 ..> c0000: `_await_readiness() calls wait()`
- c0005 ..> c0000: `_cleanup() calls close()`
- c0005 ..> c0000: `_close_controller() calls close()`
- c0005 ..> c0000: `_close_controller() calls wait()`
- c0005 ..> c0000: `_complete_handover() calls close()`
- c0005 ..> c0000: `control() calls close()`
- c0005 ..> c0000: `reap_watcher() calls wait()`
- c0005 ..> c0000: `relay() calls close()`
- c0005 ..> c0000: `run() calls close()`
- c0005 ..> c0000: `run() calls wait()`
- c0005 ..> c0000: `start_watcher() calls close()`
- c0005 ..> c0005: `_apply_controller_event() calls _apply_controller_problem()`
- c0005 ..> c0005: `_apply_controller_event() calls save()`
- c0005 ..> c0005: `_apply_controller_problem() calls save()`
- c0005 ..> c0005: `_apply_controller_problem() calls stop_watcher()`
- c0005 ..> c0005: `_cleanup() calls _close_controller()`
- c0005 ..> c0005: `_cleanup() calls _remove_control_socket()`
- c0005 ..> c0005: `_cleanup() calls stop_watcher()`
- c0005 ..> c0005: `_close_controller() calls save()`
- c0005 ..> c0005: `_finish_observation() calls save()`
- c0005 ..> c0005: `_reject_controller_event() calls save()`
- c0005 ..> c0005: `_reject_controller_event() calls stop_watcher()`
- c0005 ..> c0005: `_start_controller() calls observe()`
- c0005 ..> c0005: `control() calls start_watcher()`
- c0005 ..> c0005: `control() calls stop_watcher()`
- c0005 ..> c0005: `observe() calls _apply_controller_event()`
- c0005 ..> c0005: `observe() calls _finish_observation()`
- c0005 ..> c0005: `observe() calls _reject_controller_event()`
- c0005 ..> c0005: `observe() calls _validate_readiness()`
- c0005 ..> c0005: `relay() calls _relay_request()`
- c0005 ..> c0005: `run() calls _await_readiness()`
- c0005 ..> c0005: `run() calls _cleanup()`
- c0005 ..> c0005: `run() calls _complete_handover()`
- c0005 ..> c0005: `run() calls _start_controller()`
- c0005 ..> c0005: `run() calls save()`
- c0005 ..> c0005: `start_watcher() calls reap_watcher()`
- c0005 ..> c0005: `start_watcher() calls relay()`
- c0005 ..> c0005: `start_watcher() calls stop_watcher()`
- c0005 ..> c0006: `observe() calls _controller_event()`
- c0005 ..> c0006: `relay() calls _watcher_request()`
- c0005 ..> c0021: `__init__() constructs AgentShellLifecycleDeadlines`
- c0005 ..> c0021: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0005 ..> c0039: `_apply_controller_problem() calls quote()`
- c0005 ..> c0080: `_start_controller() calls create_task()`
- c0005 ..> c0080: `start_watcher() calls create_task()`
- c0005 ..> c0093: `_apply_controller_problem() constructs FactoryError`
- c0005 ..> c0093: `_await_readiness() constructs FactoryError`
- c0005 ..> c0093: `_complete_handover() constructs FactoryError`
- c0005 ..> c0093: `_finish_observation() constructs FactoryError`
- c0005 ..> c0093: `_reject_controller_event() constructs FactoryError`
- c0005 ..> c0093: `_relay_request() constructs FactoryError`
- c0005 ..> c0093: `control() constructs FactoryError`
- c0005 ..> c0093: `observe() constructs FactoryError`
- c0005 ..> c0093: `reap_watcher() constructs FactoryError`
- c0005 ..> c0093: `start_watcher() constructs FactoryError`
- c0005 ..> c0096: `save() calls replace_generated_json()`
- c0006 ..> c0000: `_acquire_owner_lock() calls close()`
- c0006 ..> c0000: `_prepare_owner_startup() calls close()`
- c0006 ..> c0000: `entrypoint() calls close()`
- c0006 ..> c0003: `_prepare_owner_startup() calls runtime_directory()`
- c0006 ..> c0005: `entrypoint() calls run()`
- c0006 ..> c0005: `main() calls run()`
- c0006 ..> c0005: `main() constructs ForemanOwner`
- c0006 ..> c0006: `_controller_event() calls _validate_target()`
- c0006 ..> c0006: `_prepare_owner_startup() calls _acquire_owner_lock()`
- c0006 ..> c0006: `entrypoint() calls _prepare_owner_startup()`
- c0006 ..> c0006: `entrypoint() calls _report_startup_error()`
- c0006 ..> c0006: `entrypoint() calls main()`
- c0006 ..> c0007: `_prepare_owner_startup() calls read_state()`
- c0006 ..> c0039: `_acquire_owner_lock() calls quote()`
- c0006 ..> c0080: `main() calls create_task()`
- c0006 ..> c0093: `_acquire_owner_lock() constructs FactoryError`
- c0006 ..> c0093: `_prepare_owner_startup() constructs FactoryError`
- c0006 ..> c0093: `_watcher_request() constructs FactoryError`
- c0007 ..> c0000: `start_owner() calls close()`
- c0007 ..> c0000: `start_owner() calls wait()`
- c0007 ..> c0003: `read_state() calls runtime_directory()`
- c0007 ..> c0003: `request() calls runtime_directory()`
- c0007 ..> c0003: `start_owner() calls runtime_directory()`
- c0007 ..> c0005: `start_owner() calls run()`
- c0007 ..> c0007: `request() calls _reply()`
- c0007 ..> c0007: `request() calls read_state()`
- c0007 ..> c0007: `start_owner() calls _reply()`
- c0007 ..> c0021: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0007 ..> c0021: `type in start_owner`
- c0007 ..> c0039: `request() calls quote()`
- c0007 ..> c0088: `start_owner() calls spec()`
- c0007 ..> c0091: `type in start_owner`
- c0007 ..> c0093: `_reply() constructs FactoryError`
- c0007 ..> c0093: `read_state() constructs FactoryError`
- c0007 ..> c0093: `request() constructs FactoryError`
- c0007 ..> c0093: `start_owner() constructs FactoryError`
- c0007 ..> c0096: `read_state() calls read_generated_json()`
- c0008 ..> c0008: `install() calls _inputs()`
- c0008 ..> c0008: `ready() calls _inputs()`
- c0008 ..> c0008: `unready() calls ready()`
- c0008 ..> c0093: `install() constructs FactoryError`
- c0008 ..> c0095: `install() calls check_uv()`
- c0008 ..> c0095: `install() calls no_installer()`
- c0008 ..> c0095: `install() calls run_install()`
- c0008 ..> c0095: `install() calls sync_fingerprint()`
- c0008 ..> c0095: `ready() calls runtime_ready()`
- c0009 ..> c0000: `close() calls close()`
- c0009 ..> c0009: `send() calls _read()`
- c0009 ..> c0009: `send() calls _write()`
- c0009 ..> c0009: `start() calls _read()`
- c0009 ..> c0009: `start() calls _write()`
- c0009 ..> c0009: `wait() calls _read()`
- c0009 ..> c0021: `__init__() constructs AgentShellLifecycleDeadlines`
- c0009 ..> c0021: `type in __init__`
- c0009 ..> c0026: `startup_hint() calls how_to_reach()`
- c0009 ..> c0027: `type in __init__`
- c0009 ..> c0088: `start() calls spec()`
- c0009 ..> c0091: `type in __init__`
- c0009 ..> c0093: `_read() constructs FactoryError`
- c0009 ..> c0093: `_write() constructs FactoryError`
- c0009 ..> c0093: `close() constructs FactoryError`
- c0009 ..> c0093: `start() constructs FactoryError`
- c0009 ..> c0101: `_read() calls check_watch_stop()`
- c0009 ..> c0101: `_write() calls check_watch_stop()`
- c0009 ..> c0101: `wait() calls check_watch_stop()`
- c0010 ..> c0000: `pin_worker() calls close()`
- c0011 ..> c0011: `_validate_agent() calls _local_selection()`
- c0011 ..> c0011: `_validate_roster() calls _local_selection()`
- c0011 ..> c0011: `_validate_roster() calls relative_path()`
- c0011 ..> c0011: `foreman_launch() calls read_definition()`
- c0011 ..> c0011: `foreman_launch() calls relative_path()`
- c0011 ..> c0011: `read_definition() calls _validate_agent()`
- c0011 ..> c0011: `read_definition() calls _validate_resources()`
- c0011 ..> c0011: `read_definition() calls _validate_roster()`
- c0011 ..> c0093: `foreman_launch() constructs FactoryError`
- c0011 ..> c0093: `read_definition() constructs FactoryError`
- c0011 ..> c0099: `_local_selection() calls nonblank()`
- c0011 ..> c0099: `_validate_agent() calls nonblank()`
- c0011 ..> c0099: `foreman_launch() calls nonblank()`
- c0011 ..> c0099: `relative_path() calls nonblank()`
- c0012 ..> c0011: `selected_launch() calls foreman_launch()`
- c0012 ..> c0012: `choose_pi_home() calls pi_home()`
- c0012 ..> c0012: `choose_pi_home() calls require_pi_home()`
- c0012 ..> c0012: `list_models() calls pi_home()`
- c0012 ..> c0012: `list_models() calls require_pi_home()`
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
- c0012 ..> c0012: `validate_setup() calls pi_home()`
- c0012 ..> c0012: `validate_setup() calls require_pi_home()`
- c0012 ..> c0012: `validate_setup() calls validate_bundled_resources()`
- c0012 ..> c0012: `validate_setup() calls validate_guidance()`
- c0012 ..> c0012: `validate_worker_models() calls list_models()`
- c0012 ..> c0013: `prepare_roles() calls validate_depth()`
- c0012 ..> c0013: `prepare_roles() constructs CoordinatorProfiles`
- c0012 ..> c0013: `validate_setup() calls validate_depth()`
- c0012 ..> c0013: `validate_setup() constructs CoordinatorProfiles`
- c0012 ..> c0015: `pi_home() calls saved_pi_home()`
- c0012 ..> c0017: `_install_resources() calls bundled_files()`
- c0012 ..> c0019: `selected_launch() calls selected_skill_files()`
- c0012 ..> c0022: `type in prepare_roles`
- c0012 ..> c0022: `type in validate_worker_models`
- c0012 ..> c0036: `choose_pi_home() calls confirm()`
- c0012 ..> c0039: `require_pi_home() calls quote()`
- c0012 ..> c0066: `validate_setup() calls missing_tools()`
- c0012 ..> c0078: `list_models() calls role_environment()`
- c0012 ..> c0083: `type in __init__`
- c0012 ..> c0083: `type in list_models`
- c0012 ..> c0083: `type in prepare_roles`
- c0012 ..> c0083: `type in record_completion`
- c0012 ..> c0083: `type in selected_launch`
- c0012 ..> c0083: `type in validate_setup`
- c0012 ..> c0083: `type in validate_worker_models`
- c0012 ..> c0093: `_install_resources() constructs FactoryError`
- c0012 ..> c0093: `_read_guidance() constructs FactoryError`
- c0012 ..> c0093: `choose_pi_home() constructs FactoryError`
- c0012 ..> c0093: `list_models() constructs FactoryError`
- c0012 ..> c0093: `prepare_roles() constructs FactoryError`
- c0012 ..> c0093: `prepare_setup_guidance() constructs FactoryError`
- c0012 ..> c0093: `require_pi_home() constructs FactoryError`
- c0012 ..> c0093: `selected_launch() constructs FactoryError`
- c0012 ..> c0093: `validate_bundled_resources() constructs FactoryError`
- c0012 ..> c0093: `validate_completion() constructs FactoryError`
- c0012 ..> c0093: `validate_guidance() constructs FactoryError`
- c0012 ..> c0093: `validate_setup() constructs FactoryError`
- c0012 ..> c0093: `validate_worker_models() constructs FactoryError`
- c0012 ..> c0094: `require_pi_home() calls executable_path()`
- c0012 ..> c0096: `_install_resources() calls write_new()`
- c0012 ..> c0096: `_protect_runtime() calls write_new()`
- c0012 ..> c0096: `begin_setup() calls remove_generated()`
- c0012 ..> c0096: `prepare() calls write_new()`
- c0012 ..> c0096: `prepare_roles() calls check_real_path()`
- c0012 ..> c0096: `prepare_setup_guidance() calls write_new()`
- c0012 ..> c0096: `record_completion() calls replace_generated_json()`
- c0012 ..> c0096: `save_pi_choice() calls write_json()`
- c0012 ..> c0096: `validate_bundled_resources() calls check_real_path()`
- c0012 ..> c0096: `validate_completion() calls read_generated_json()`
- c0012 ..> c0098: `list_models() calls run_owned()`
- c0013 ..> c0012: `prepare() calls prepare()`
- c0013 ..> c0013: `prepare() calls _write_agent()`
- c0013 ..> c0013: `prepare() calls _write_foreman_memory()`
- c0013 ..> c0013: `prepare() calls validate_guidance()`
- c0013 ..> c0014: `prepare() calls selected_resources()`
- c0013 ..> c0020: `__init__() constructs WorkerProfiles`
- c0013 ..> c0093: `_write_foreman_memory() constructs FactoryError`
- c0013 ..> c0093: `prepare() constructs FactoryError`
- c0013 ..> c0093: `validate_depth() constructs FactoryError`
- c0013 ..> c0093: `validate_guidance() constructs FactoryError`
- c0013 ..> c0096: `_write_agent() calls write_definition()`
- c0013 ..> c0096: `_write_foreman_memory() calls read_generated_json()`
- c0013 ..> c0096: `_write_foreman_memory() calls write_json()`
- c0013 ..> c0096: `prepare() calls check_skill_file()`
- c0013 ..> c0096: `prepare() calls write_new()`
- c0015 ..> c0093: `saved_pi_home() constructs FactoryError`
- c0015 ..> c0096: `saved_pi_home() calls read_generated_json()`
- c0017 ..> c0016: `plan_update() constructs ResourceUpdate`
- c0017 ..> c0016: `type in _back_up`
- c0017 ..> c0016: `type in apply_update`
- c0017 ..> c0016: `type in plan_update`
- c0017 ..> c0017: `apply_update() calls _back_up()`
- c0017 ..> c0017: `bundled_files() calls _digest()`
- c0017 ..> c0017: `plan_update() calls _digest()`
- c0017 ..> c0017: `plan_update() calls bundled_files()`
- c0017 ..> c0093: `bundled_files() constructs FactoryError`
- c0017 ..> c0093: `plan_update() constructs FactoryError`
- c0017 ..> c0096: `plan_update() calls check_real_path()`
- c0018 ..> c0015: `unready() calls saved_pi_home()`
- c0018 ..> c0018: `unready() calls ready()`
- c0018 ..> c0094: `absent() calls executable_path()`
- c0018 ..> c0094: `unready() calls executable_path()`
- c0018 ..> c0095: `install() calls install_locks()`
- c0018 ..> c0095: `install() calls no_installer()`
- c0018 ..> c0095: `install() calls require_manager()`
- c0018 ..> c0095: `install() calls run_install()`
- c0018 ..> c0095: `ready() calls install_environment()`
- c0018 ..> c0095: `ready() calls sync_fingerprint()`
- c0018 ..> c0098: `ready() calls run_owned()`
- c0019 ..> c0000: `_add_skill_file() calls close()`
- c0019 ..> c0019: `_walk_skill_directory() calls _add_skill_file()`
- c0019 ..> c0019: `selected_skill_files() calls _add_skill_file()`
- c0019 ..> c0019: `selected_skill_files() calls _walk_skill_directory()`
- c0019 ..> c0093: `_add_skill_file() constructs FactoryError`
- c0019 ..> c0093: `_walk_skill_directory() constructs FactoryError`
- c0019 ..> c0093: `selected_skill_files() constructs FactoryError`
- c0020 ..> c0022: `type in prepare`
- c0020 ..> c0042: `prepare() calls update()`
- c0020 ..> c0096: `prepare() calls check_skill_file()`
- c0020 ..> c0096: `prepare() calls write_definition()`
- c0020 ..> c0096: `prepare() calls write_new()`
- c0021 ..> c0099: `__post_init__() calls positive_duration()`
- c0023 ..> c0022: `type in _validate_foreman_memory`
- c0023 ..> c0022: `type in validate_initial_agents`
- c0023 ..> c0022: `type in validate_workers`
- c0023 ..> c0023: `validate_initial_agents() calls _validate_foreman_memory()`
- c0023 ..> c0023: `validate_initial_agents() calls validate_role_app()`
- c0023 ..> c0023: `validate_initial_agents() calls validate_workers()`
- c0023 ..> c0023: `validate_workers() calls validate_role_app()`
- c0023 ..> c0093: `_validate_foreman_memory() constructs FactoryError`
- c0023 ..> c0093: `skill_paths() constructs FactoryError`
- c0023 ..> c0093: `validate_initial_agents() constructs FactoryError`
- c0023 ..> c0093: `validate_role_app() constructs FactoryError`
- c0023 ..> c0093: `validate_workers() constructs FactoryError`
- c0023 ..> c0099: `_validate_foreman_memory() calls nonblank()`
- c0023 ..> c0099: `skill_paths() calls nonblank()`
- c0023 ..> c0099: `validate_initial_agents() calls nonblank()`
- c0023 ..> c0099: `validate_workers() calls nonblank()`
- c0024 ..> c0022: `type in prepare_roles`
- c0024 ..> c0083: `type in list_models`
- c0024 ..> c0083: `type in prepare_roles`
- c0024 ..> c0083: `type in record_completion`
- c0024 ..> c0083: `type in selected_launch`
- c0026 ..> c0088: `how_to_reach() calls how_to_attach()`
- c0026 ..> c0088: `open() calls enter()`
- c0026 ..> c0091: `type in __init__`
- c0028 ..> c0008: `build_tools() constructs AgentShellRuntimeInstall`
- c0028 ..> c0009: `build_watcher() constructs AgentShellTerminal`
- c0028 ..> c0012: `build_team() constructs PiAgentTeam`
- c0028 ..> c0012: `build_watcher() calls managed_memory_notice()`
- c0028 ..> c0012: `prepare_foreman_launch() calls pi_home()`
- c0028 ..> c0012: `prepare_foreman_launch() calls selected_launch()`
- c0028 ..> c0012: `prepare_foreman_launch() calls validate_completion()`
- c0028 ..> c0012: `type in build_team`
- c0028 ..> c0018: `build_tools() constructs PiInstall`
- c0028 ..> c0026: `build_channel() constructs TerminalChannel`
- c0028 ..> c0026: `type in build_channel`
- c0028 ..> c0028: `build_channel() calls build_host()`
- c0028 ..> c0028: `build_initialiser() calls build_team()`
- c0028 ..> c0028: `build_team() calls build_tools()`
- c0028 ..> c0028: `build_watcher() calls build_channel()`
- c0028 ..> c0028: `build_watcher() calls build_host()`
- c0028 ..> c0028: `build_watcher() calls prepare_foreman_launch()`
- c0028 ..> c0028: `build_watcher() calls select_ticketing()`
- c0028 ..> c0028: `prepare_foreman_launch() calls build_team()`
- c0028 ..> c0029: `build_initialiser() constructs DeadlinePolicy`
- c0028 ..> c0029: `build_watcher() constructs DeadlinePolicy`
- c0028 ..> c0029: `type in build_initialiser`
- c0028 ..> c0029: `type in build_watcher`
- c0028 ..> c0036: `build_watcher() constructs FileCleanupReceipts`
- c0028 ..> c0038: `build_initialiser() constructs TomlConfigurationStore`
- c0028 ..> c0041: `build_watcher() constructs ObservedTerminal`
- c0028 ..> c0044: `type in build_watcher`
- c0028 ..> c0044: `type in prepare_foreman_launch`
- c0028 ..> c0044: `type in select_ticketing`
- c0028 ..> c0059: `build_watcher() constructs CleanupCompleted`
- c0028 ..> c0065: `build_initialiser() constructs InitialiseFactory`
- c0028 ..> c0065: `type in build_initialiser`
- c0028 ..> c0066: `build_team() calls missing_tools()`
- c0028 ..> c0067: `build_watcher() constructs ScaffoldIssue`
- c0028 ..> c0070: `build_watcher() constructs WatchFactory`
- c0028 ..> c0070: `type in build_watcher`
- c0028 ..> c0073: `build_initialiser() constructs GitHubForge`
- c0028 ..> c0073: `build_watcher() constructs GitHubForge`
- c0028 ..> c0078: `prepare_foreman_launch() calls role_environment()`
- c0028 ..> c0079: `build_tools() constructs ForgetfulInstall`
- c0028 ..> c0080: `build_watcher() constructs ForgetfulPlanStore`
- c0028 ..> c0082: `build_initialiser() constructs ForgetfulSetup`
- c0028 ..> c0083: `type in build_tools`
- c0028 ..> c0088: `build_host() constructs TmuxHost`
- c0028 ..> c0088: `type in build_host`
- c0028 ..> c0089: `build_tools() constructs TmuxInstall`
- c0028 ..> c0093: `build_watcher() constructs FactoryError`
- c0028 ..> c0093: `prepare_foreman_launch() constructs FactoryError`
- c0028 ..> c0093: `select_ticketing() constructs FactoryError`
- c0028 ..> c0102: `build_initialiser() constructs GitHubTicketing`
- c0028 ..> c0102: `build_watcher() calls check_ready()`
- c0028 ..> c0102: `select_ticketing() calls validate_source()`
- c0028 ..> c0106: `type in select_ticketing`
- c0028 ..> c0107: `build_initialiser() constructs GitRepositories`
- c0028 ..> c0107: `build_watcher() constructs GitRepositories`
- c0028 ..> c0109: `build_watcher() constructs GitWorktrees`
- c0029 --> c0021: `field agentshell`
- c0029 ..> c0099: `__post_init__() calls positive_duration()`
- c0030 ..> c0030: `agree_definition_of_done() calls _deployment_agreement()`
- c0030 ..> c0044: `type in agree_definition_of_done`
- c0030 ..> c0093: `_deployment_agreement() constructs FactoryError`
- c0030 ..> c0093: `agree_definition_of_done() constructs FactoryError`
- c0030 ..> c0096: `agree_definition_of_done() calls check_skill_file()`
- c0030 ..> c0096: `agree_definition_of_done() calls write_new()`
- c0031 --> c0044: `field config`
- c0031 --> c0083: `field connection`
- c0032 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0032 ..> c0005: `_watch_locked() calls run()`
- c0032 ..> c0007: `_change_managed_watch() calls request()`
- c0032 ..> c0007: `_finish_existing_setup() calls read_state()`
- c0032 ..> c0007: `_foreman() calls read_state()`
- c0032 ..> c0007: `_foreman() calls request()`
- c0032 ..> c0007: `_foreman() calls start_owner()`
- c0032 ..> c0007: `_initialise() calls request()`
- c0032 ..> c0007: `_initialise_locked() calls read_state()`
- c0032 ..> c0007: `_launch_setup_foreman() calls start_owner()`
- c0032 ..> c0007: `_managed_watch_status() calls read_state()`
- c0032 ..> c0007: `_managed_watch_status() calls request()`
- c0032 ..> c0007: `_offer_factory_launch() calls read_state()`
- c0032 ..> c0007: `_watch_locked() calls read_state()`
- c0032 ..> c0012: `_complete_setup() calls managed_memory_notice()`
- c0032 ..> c0012: `_complete_setup() calls record_completion()`
- c0032 ..> c0012: `_discover_worker_models() calls list_models()`
- c0032 ..> c0012: `_finish_existing_setup() calls choose_pi_home()`
- c0032 ..> c0012: `_finish_existing_setup() calls save_pi_choice()`
- c0032 ..> c0012: `_finish_existing_setup() calls selected_launch()`
- c0032 ..> c0012: `_foreman() calls managed_memory_notice()`
- c0032 ..> c0012: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0032 ..> c0012: `_select_model() calls list_models()`
- c0032 ..> c0012: `_start_initial_setup() calls begin_setup()`
- c0032 ..> c0012: `_start_initial_setup() calls choose_pi_home()`
- c0032 ..> c0012: `_validate_initial_model() calls prepare_roles()`
- c0032 ..> c0012: `_watch_status() calls validate_completion()`
- c0032 ..> c0022: `_configure_new_factory() constructs InitialAgentChoices`
- c0032 ..> c0022: `type in _configure_new_factory`
- c0032 ..> c0022: `type in _foreman_memory_choices`
- c0032 ..> c0022: `type in _owner_choices`
- c0032 ..> c0022: `type in _prompt_coordinator_choices`
- c0032 ..> c0022: `type in _validate_initial_model`
- c0032 ..> c0022: `type in _worker_choices`
- c0032 ..> c0023: `_start_initial_setup() calls validate_initial_agents()`
- c0032 ..> c0028: `_foreman() calls build_channel()`
- c0032 ..> c0028: `_foreman() calls build_host()`
- c0032 ..> c0028: `_foreman() calls prepare_foreman_launch()`
- c0032 ..> c0028: `_initialise() calls build_channel()`
- c0032 ..> c0028: `_initialise_locked() calls build_initialiser()`
- c0032 ..> c0028: `_launch_setup_foreman() calls build_host()`
- c0032 ..> c0028: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0032 ..> c0028: `_watch_locked() calls build_watcher()`
- c0032 ..> c0028: `_watch_status() calls build_team()`
- c0032 ..> c0029: `main() constructs DeadlinePolicy`
- c0032 ..> c0029: `type in _finish_existing_setup`
- c0032 ..> c0029: `type in _foreman`
- c0032 ..> c0029: `type in _initialise`
- c0032 ..> c0029: `type in _initialise_locked`
- c0032 ..> c0029: `type in _start_initial_setup`
- c0032 ..> c0029: `type in _watch`
- c0032 ..> c0029: `type in _watch_locked`
- c0032 ..> c0029: `type in main`
- c0032 ..> c0030: `_finish_existing_setup() calls agree_definition_of_done()`
- c0032 ..> c0030: `_start_initial_setup() calls agree_definition_of_done()`
- c0032 ..> c0031: `_start_initial_setup() constructs _InitialSetupState`
- c0032 ..> c0031: `type in _discover_worker_models`
- c0032 ..> c0031: `type in _validate_initial_model`
- c0032 ..> c0032: `_complete_setup() calls _managed_rest_mapping_available()`
- c0032 ..> c0032: `_configure_new_factory() calls _prepare_foreman()`
- c0032 ..> c0032: `_configure_new_factory() calls _select_model()`
- c0032 ..> c0032: `_configure_new_factory() calls _select_numbered()`
- c0032 ..> c0032: `_configure_new_factory() calls select_repositories()`
- c0032 ..> c0032: `_connection() calls _check_existing_connection()`
- c0032 ..> c0032: `_discover_worker_models() calls _prepare_foreman()`
- c0032 ..> c0032: `_finish_existing_setup() calls _complete_setup()`
- c0032 ..> c0032: `_finish_existing_setup() calls _confirm_pi_home()`
- c0032 ..> c0032: `_finish_existing_setup() calls _connection()`
- c0032 ..> c0032: `_finish_existing_setup() calls _launch_setup_foreman()`
- c0032 ..> c0032: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0032 ..> c0032: `_foreman_memory_choices() calls _select_numbered()`
- c0032 ..> c0032: `_initialise() calls _initialise_locked()`
- c0032 ..> c0032: `_initialise() calls _offer_factory_launch()`
- c0032 ..> c0032: `_initialise_locked() calls _finish_existing_setup()`
- c0032 ..> c0032: `_initialise_locked() calls _start_initial_setup()`
- c0032 ..> c0032: `_initialise_locked() calls _validate_setup_owner()`
- c0032 ..> c0032: `_print_models() calls _safe_diagnostic()`
- c0032 ..> c0032: `_prompt_coordinator_choices() calls _select_numbered()`
- c0032 ..> c0032: `_prompt_worker() calls _select_numbered()`
- c0032 ..> c0032: `_prompt_workers() calls _prompt_worker()`
- c0032 ..> c0032: `_select_model() calls _print_models()`
- c0032 ..> c0032: `_select_model() calls _select_numbered()`
- c0032 ..> c0032: `_select_numbered() calls _safe_diagnostic()`
- c0032 ..> c0032: `_select_project() calls _listed_project_id()`
- c0032 ..> c0032: `_select_project() calls _safe_diagnostic()`
- c0032 ..> c0032: `_select_setup_route() calls _select_numbered()`
- c0032 ..> c0032: `_start_initial_setup() calls _complete_setup()`
- c0032 ..> c0032: `_start_initial_setup() calls _configure_new_factory()`
- c0032 ..> c0032: `_start_initial_setup() calls _confirm_pi_home()`
- c0032 ..> c0032: `_start_initial_setup() calls _connection()`
- c0032 ..> c0032: `_start_initial_setup() calls _foreman_memory_choices()`
- c0032 ..> c0032: `_start_initial_setup() calls _launch_setup_foreman()`
- c0032 ..> c0032: `_start_initial_setup() calls _owner_choices()`
- c0032 ..> c0032: `_start_initial_setup() calls _research_choices()`
- c0032 ..> c0032: `_start_initial_setup() calls _worker_choices()`
- c0032 ..> c0032: `_validate_initial_model() calls _prepare_foreman()`
- c0032 ..> c0032: `_validate_initial_model() calls _select_model()`
- c0032 ..> c0032: `_validate_initial_model() calls _select_project()`
- c0032 ..> c0032: `_watch() calls _change_managed_watch()`
- c0032 ..> c0032: `_watch() calls _watch_locked()`
- c0032 ..> c0032: `_watch() calls _watch_status()`
- c0032 ..> c0032: `_watch_locked() calls _choose_existing()`
- c0032 ..> c0032: `_watch_locked() calls _safe_diagnostic()`
- c0032 ..> c0032: `_watch_status() calls _managed_watch_status()`
- c0032 ..> c0032: `_worker_choices() calls _prompt_coordinator_choices()`
- c0032 ..> c0032: `_worker_choices() calls _prompt_workers()`
- c0032 ..> c0032: `_worker_choices() calls _select_setup_route()`
- c0032 ..> c0032: `_worker_choices() calls _worker_arguments()`
- c0032 ..> c0032: `main() calls _foreman()`
- c0032 ..> c0032: `main() calls _initialise()`
- c0032 ..> c0032: `main() calls _parse_arguments()`
- c0032 ..> c0032: `main() calls _safe_diagnostic()`
- c0032 ..> c0032: `main() calls _watch()`
- c0032 ..> c0033: `_select_numbered() calls parse_numbered_selection()`
- c0032 ..> c0034: `main() calls update_resources()`
- c0032 ..> c0035: `_foreman() calls load_configuration()`
- c0032 ..> c0035: `_watch_locked() calls load_configuration()`
- c0032 ..> c0035: `_watch_status() calls load_configuration()`
- c0032 ..> c0036: `_initialise_locked() calls load()`
- c0032 ..> c0039: `_initialise() calls quote()`
- c0032 ..> c0039: `_launch_setup_foreman() calls quote()`
- c0032 ..> c0039: `_managed_watch_status() calls quote()`
- c0032 ..> c0039: `_select_model() calls quote()`
- c0032 ..> c0039: `_validate_setup_owner() calls quote()`
- c0032 ..> c0039: `_watch_locked() calls quote()`
- c0032 ..> c0040: `_foreman() calls hold()`
- c0032 ..> c0040: `_foreman() constructs WorkspaceWatchLease`
- c0032 ..> c0040: `_initialise() calls hold()`
- c0032 ..> c0040: `_initialise() constructs WorkspaceWatchLease`
- c0032 ..> c0040: `_watch() calls hold()`
- c0032 ..> c0040: `_watch() constructs WorkspaceWatchLease`
- c0032 ..> c0042: `_prompt_workers() calls update()`
- c0032 ..> c0043: `_managed_watch_status() calls unknown_status()`
- c0032 ..> c0043: `_watch_locked() calls observe_plain_watch()`
- c0032 ..> c0043: `_watch_status() calls plain_watch_status()`
- c0032 ..> c0043: `_watch_status() calls unknown_status()`
- c0032 ..> c0044: `type in _complete_setup`
- c0032 ..> c0044: `type in _configure_new_factory`
- c0032 ..> c0044: `type in _finish_existing_setup`
- c0032 ..> c0044: `type in _validate_initial_model`
- c0032 ..> c0045: `_connection() calls validate()`
- c0032 ..> c0065: `_complete_setup() calls check_foreman()`
- c0032 ..> c0065: `_configure_new_factory() calls configure()`
- c0032 ..> c0065: `_configure_new_factory() calls inspect()`
- c0032 ..> c0065: `_finish_existing_setup() calls initialise()`
- c0032 ..> c0065: `_initialise_locked() calls load_existing()`
- c0032 ..> c0065: `_launch_setup_foreman() calls check_foreman()`
- c0032 ..> c0065: `_prepare_foreman() calls prepare_foreman()`
- c0032 ..> c0065: `_start_initial_setup() calls initialise()`
- c0032 ..> c0065: `select_repositories() calls discover()`
- c0032 ..> c0065: `type in _complete_setup`
- c0032 ..> c0065: `type in _configure_new_factory`
- c0032 ..> c0065: `type in _discover_worker_models`
- c0032 ..> c0065: `type in _finish_existing_setup`
- c0032 ..> c0065: `type in _select_project`
- c0032 ..> c0065: `type in _start_initial_setup`
- c0032 ..> c0065: `type in _validate_initial_model`
- c0032 ..> c0065: `type in select_repositories`
- c0032 ..> c0076: `_complete_setup() calls uses_browser_login()`
- c0032 ..> c0077: `_select_project() calls create_project()`
- c0032 ..> c0077: `_select_project() calls projects()`
- c0032 ..> c0083: `_connection() constructs ForgetfulConnection`
- c0032 ..> c0083: `type in _check_existing_connection`
- c0032 ..> c0083: `type in _configure_new_factory`
- c0032 ..> c0083: `type in _connection`
- c0032 ..> c0083: `type in _foreman_memory_choices`
- c0032 ..> c0083: `type in _managed_rest_mapping_available`
- c0032 ..> c0083: `type in _select_project`
- c0032 ..> c0093: `_change_managed_watch() constructs FactoryError`
- c0032 ..> c0093: `_check_existing_connection() constructs FactoryError`
- c0032 ..> c0093: `_choose_existing() constructs FactoryError`
- c0032 ..> c0093: `_configure_new_factory() constructs FactoryError`
- c0032 ..> c0093: `_finish_existing_setup() constructs FactoryError`
- c0032 ..> c0093: `_foreman() constructs FactoryError`
- c0032 ..> c0093: `_foreman_memory_choices() constructs FactoryError`
- c0032 ..> c0093: `_initialise() constructs FactoryError`
- c0032 ..> c0093: `_initialise_locked() constructs FactoryError`
- c0032 ..> c0093: `_install_missing() constructs FactoryError`
- c0032 ..> c0093: `_listed_project_id() constructs FactoryError`
- c0032 ..> c0093: `_prompt_coordinator_choices() constructs FactoryError`
- c0032 ..> c0093: `_prompt_worker() constructs FactoryError`
- c0032 ..> c0093: `_select_model() constructs FactoryError`
- c0032 ..> c0093: `_select_project() constructs FactoryError`
- c0032 ..> c0093: `_validate_setup_owner() constructs FactoryError`
- c0032 ..> c0093: `_watch_locked() constructs FactoryError`
- c0032 ..> c0093: `_worker_choices() constructs FactoryError`
- c0032 ..> c0093: `main() constructs FactoryError`
- c0032 ..> c0093: `select_repositories() constructs FactoryError`
- c0032 ..> c0096: `_discover_worker_models() calls check_real_path()`
- c0032 ..> c0101: `_watch_locked() calls watch_stop_scope()`
- c0033 ..> c0093: `parse_numbered_selection() constructs FactoryError`
- c0034 ..> c0002: `update_resources() calls ready()`
- c0034 ..> c0007: `update_resources() calls read_state()`
- c0034 ..> c0008: `update_resources() calls install()`
- c0034 ..> c0008: `update_resources() constructs AgentShellRuntimeInstall`
- c0034 ..> c0012: `update_resources() calls validate_bundled_resources()`
- c0034 ..> c0017: `update_resources() calls apply_update()`
- c0034 ..> c0017: `update_resources() calls plan_update()`
- c0034 ..> c0028: `update_resources() calls build_team()`
- c0034 ..> c0029: `type in update_resources`
- c0034 ..> c0034: `update_resources() calls _report()`
- c0034 ..> c0040: `update_resources() calls hold()`
- c0034 ..> c0040: `update_resources() constructs WorkspaceWatchLease`
- c0034 ..> c0093: `_report() constructs FactoryError`
- c0034 ..> c0093: `update_resources() constructs FactoryError`
- c0035 ..> c0036: `load_configuration() calls load()`
- c0035 ..> c0038: `load_configuration() constructs TomlConfigurationStore`
- c0035 ..> c0044: `type in load_configuration`
- c0035 ..> c0093: `load_configuration() constructs FactoryError`
- c0036 ..> c0000: `_load() calls close()`
- c0036 ..> c0036: `confirm() calls load()`
- c0036 ..> c0036: `load() calls _load()`
- c0036 ..> c0037: `_load() calls _resource()`
- c0036 ..> c0055: `type in _load`
- c0036 ..> c0055: `type in confirm`
- c0036 ..> c0055: `type in load`
- c0036 ..> c0093: `confirm() constructs FactoryError`
- c0036 ..> c0093: `load() constructs FactoryError`
- c0036 ..> c0096: `_load() calls check_real_path()`
- c0036 ..> c0096: `confirm() calls replace_generated_json()`
- c0036 ..> c0101: `confirm() calls check_watch_stop()`
- c0037 ..> c0055: `_resource() constructs CleanupSet`
- c0037 ..> c0055: `type in _resource`
- c0038 ..> c0000: `load() calls close()`
- c0038 ..> c0000: `save() calls close()`
- c0038 ..> c0036: `load() calls load()`
- c0038 ..> c0039: `save() calls quote()`
- c0038 ..> c0044: `type in load`
- c0038 ..> c0044: `type in save`
- c0038 ..> c0045: `load() calls from_mapping()`
- c0038 ..> c0093: `load() constructs FactoryError`
- c0038 ..> c0093: `save() constructs FactoryError`
- c0040 ..> c0000: `_hold_directory() calls close()`
- c0040 ..> c0040: `hold() calls _hold_directory()`
- c0040 ..> c0093: `_hold_directory() constructs FactoryError`
- c0041 ..> c0000: `close() calls close()`
- c0041 ..> c0000: `send() calls send()`
- c0041 ..> c0000: `start() calls start()`
- c0041 ..> c0000: `startup_hint() calls startup_hint()`
- c0041 ..> c0000: `wait() calls wait()`
- c0041 ..> c0025: `type in __init__`
- c0041 ..> c0042: `close() calls update()`
- c0041 ..> c0042: `start() calls update()`
- c0041 ..> c0042: `type in __init__`
- c0041 ..> c0043: `__init__() calls unknown_status()`
- c0042 ..> c0041: `__enter__() calls start()`
- c0042 ..> c0041: `_close_resources() calls close()`
- c0042 ..> c0042: `__enter__() calls _close_resources()`
- c0042 ..> c0042: `__enter__() calls snapshot()`
- c0042 ..> c0042: `__enter__() calls update()`
- c0042 ..> c0042: `__exit__() calls _close_resources()`
- c0042 ..> c0042: `__exit__() calls _publish_history()`
- c0042 ..> c0042: `__exit__() calls snapshot()`
- c0042 ..> c0042: `__exit__() calls update()`
- c0042 ..> c0042: `_serve() calls snapshot()`
- c0042 ..> c0042: `update() calls _publish_history()`
- c0042 ..> c0043: `__enter__() calls _discovery_path()`
- c0042 ..> c0043: `__enter__() calls _endpoint()`
- c0042 ..> c0043: `_publish_history() calls _discovery_path()`
- c0042 ..> c0043: `_publish_history() calls _read_discovery()`
- c0042 ..> c0043: `_serve() calls _frame()`
- c0042 ..> c0043: `_serve() calls _peer()`
- c0042 ..> c0093: `__enter__() constructs FactoryError`
- c0042 ..> c0096: `__enter__() calls check_real_path()`
- c0042 ..> c0096: `__enter__() calls replace_generated_json()`
- c0042 ..> c0096: `_publish_history() calls replace_generated_json()`
- c0043 ..> c0042: `observe_plain_watch() calls __enter__()`
- c0043 ..> c0042: `observe_plain_watch() calls __exit__()`
- c0043 ..> c0042: `observe_plain_watch() constructs PlainWatchObservation`
- c0043 ..> c0042: `type in observe_plain_watch`
- c0043 ..> c0043: `_frame() calls _observation_json()`
- c0043 ..> c0043: `_read_discovery() calls _discovery_path()`
- c0043 ..> c0043: `_read_discovery() calls _observation_json()`
- c0043 ..> c0043: `plain_watch_status() calls _endpoint()`
- c0043 ..> c0043: `plain_watch_status() calls _frame()`
- c0043 ..> c0043: `plain_watch_status() calls _peer()`
- c0043 ..> c0043: `plain_watch_status() calls _read_discovery()`
- c0043 ..> c0043: `plain_watch_status() calls unknown_status()`
- c0043 ..> c0096: `_read_discovery() calls check_real_path()`
- c0044 --> c0046: `field repository`
- c0044 --> c0083: `field forgetful`
- c0045 ..> c0044: `from_mapping() constructs FactoryConfiguration`
- c0045 ..> c0044: `type in from_mapping`
- c0045 ..> c0044: `type in validate`
- c0045 ..> c0045: `from_mapping() calls validate()`
- c0045 ..> c0046: `from_mapping() constructs RepositoryReference`
- c0045 ..> c0083: `validate() calls validate()`
- c0045 ..> c0084: `from_mapping() calls connection_from_mapping()`
- c0045 ..> c0093: `from_mapping() constructs FactoryError`
- c0045 ..> c0093: `validate() constructs FactoryError`
- c0045 ..> c0099: `unique_labels() calls nonblank()`
- c0045 ..> c0099: `validate() calls nonblank()`
- c0045 ..> c0105: `from_mapping() constructs TicketSource`
- c0046 --> c0105: `field work_source`
- c0047 --|> c0049: `inherits`
- c0048 --|> c0049: `inherits`
- c0049 --|> c0093: `inherits`
- c0050 --|> c0049: `inherits`
- c0051 --|> c0049: `inherits`
- c0052 ..> c0000: `__init__() calls __init__()`
- c0052 ..> c0000: `send() calls send()`
- c0052 ..> c0053: `send() calls _cleanup_recovery()`
- c0052 ..> c0093: `type in send`
- c0054 ..> c0055: `type in confirm`
- c0054 ..> c0055: `type in load`
- c0056 ..> c0044: `type in load`
- c0056 ..> c0044: `type in save`
- c0059 ..> c0000: `_candidates() calls send()`
- c0059 ..> c0000: `_dispose() calls send()`
- c0059 ..> c0000: `_read_problem() calls send()`
- c0059 ..> c0000: `_repository_identities() calls send()`
- c0059 ..> c0000: `poll() calls send()`
- c0059 ..> c0036: `_dispose() calls confirm()`
- c0059 ..> c0036: `poll() calls load()`
- c0059 ..> c0042: `_candidate() calls snapshot()`
- c0059 ..> c0042: `_candidate() calls update()`
- c0059 ..> c0042: `_check_namespaces() calls update()`
- c0059 ..> c0042: `_still_completed() calls snapshot()`
- c0059 ..> c0049: `_candidate() constructs ScaffoldProblem`
- c0059 ..> c0049: `_check_namespaces() constructs ScaffoldProblem`
- c0059 ..> c0049: `_dispose() constructs ScaffoldProblem`
- c0059 ..> c0049: `_is_confirmed() constructs ScaffoldProblem`
- c0059 ..> c0049: `_still_completed() constructs ScaffoldProblem`
- c0059 ..> c0049: `_task_mappings() constructs ScaffoldProblem`
- c0059 ..> c0049: `_validate_claim_mapping() constructs ScaffoldProblem`
- c0059 ..> c0052: `_dispose() calls clear()`
- c0059 ..> c0052: `_repository_identities() calls clear()`
- c0059 ..> c0052: `poll() calls clear()`
- c0059 ..> c0052: `type in _candidates`
- c0059 ..> c0052: `type in _claim_indexes`
- c0059 ..> c0052: `type in _dispose`
- c0059 ..> c0052: `type in _read_plans`
- c0059 ..> c0052: `type in _read_problem`
- c0059 ..> c0052: `type in _repository_identities`
- c0059 ..> c0052: `type in poll`
- c0059 ..> c0054: `type in __init__`
- c0059 --> c0055: `field confirmed`
- c0059 ..> c0055: `_is_confirmed() calls overlaps()`
- c0059 ..> c0055: `_mapping_identity() constructs CleanupSet`
- c0059 ..> c0055: `type in _mapping_identity`
- c0059 ..> c0059: `_candidate() calls _keys()`
- c0059 ..> c0059: `_candidates() calls _candidate()`
- c0059 ..> c0059: `_candidates() calls _in_scope()`
- c0059 ..> c0059: `_check_namespaces() calls _keys()`
- c0059 ..> c0059: `_claim_indexes() calls _claims()`
- c0059 ..> c0059: `_claim_indexes() calls _read_problem()`
- c0059 ..> c0059: `_claims() calls _is_confirmed()`
- c0059 ..> c0059: `_claims() calls _keys()`
- c0059 ..> c0059: `_claims() calls _task_mappings()`
- c0059 ..> c0059: `_dispose() calls _check_namespaces()`
- c0059 ..> c0059: `_dispose() calls _keys()`
- c0059 ..> c0059: `_dispose() calls _mapping_identity()`
- c0059 ..> c0059: `_dispose() calls _overlaps()`
- c0059 ..> c0059: `_dispose() calls _read_problem()`
- c0059 ..> c0059: `_dispose() calls _still_completed()`
- c0059 ..> c0059: `_is_confirmed() calls _mapping_identity()`
- c0059 ..> c0059: `_read_plans() calls _read_problem()`
- c0059 ..> c0059: `_still_completed() calls _in_scope()`
- c0059 ..> c0059: `_task_mappings() calls _validate_claim_mapping()`
- c0059 ..> c0059: `poll() calls _candidates()`
- c0059 ..> c0059: `poll() calls _claim_indexes()`
- c0059 ..> c0059: `poll() calls _dispose()`
- c0059 ..> c0059: `poll() calls _in_scope()`
- c0059 ..> c0059: `poll() calls _is_confirmed()`
- c0059 ..> c0059: `poll() calls _order()`
- c0059 ..> c0059: `poll() calls _read_plans()`
- c0059 ..> c0059: `poll() calls _repository_identities()`
- c0059 ..> c0060: `_candidate() constructs CompletedWork`
- c0059 ..> c0060: `type in _candidate`
- c0059 ..> c0060: `type in _candidates`
- c0059 ..> c0060: `type in _dispose`
- c0059 ..> c0060: `type in _order`
- c0059 ..> c0060: `type in _still_completed`
- c0059 ..> c0061: `_candidate() calls _claim_path()`
- c0059 ..> c0061: `_claims() calls _claim_path()`
- c0059 ..> c0061: `_dispose() calls _claim_path()`
- c0059 ..> c0061: `_keys() calls _claim_path()`
- c0059 ..> c0061: `_overlaps() calls _claim_path()`
- c0059 ..> c0061: `_repository_identities() calls _claim_path()`
- c0059 ..> c0064: `_candidate() calls check_source()`
- c0059 ..> c0064: `_candidate() calls context()`
- c0059 ..> c0064: `_candidate() calls mapping_repository()`
- c0059 ..> c0064: `_candidate() calls ownership_records()`
- c0059 ..> c0064: `_dispose() calls check_repository()`
- c0059 ..> c0064: `_dispose() calls mapping_repository()`
- c0059 ..> c0064: `_still_completed() calls context()`
- c0059 ..> c0064: `_still_completed() calls ownership()`
- c0059 ..> c0064: `type in __init__`
- c0059 ..> c0080: `_candidates() calls tasks()`
- c0059 ..> c0080: `_claim_indexes() calls tasks()`
- c0059 ..> c0080: `_in_scope() calls owns()`
- c0059 ..> c0080: `_mapping_identity() calls backend_identity()`
- c0059 ..> c0080: `_read_plans() calls get_plan()`
- c0059 ..> c0080: `_still_completed() calls get_plan()`
- c0059 ..> c0080: `poll() calls plans()`
- c0059 ..> c0093: `type in _read_problem`
- c0059 ..> c0102: `_in_scope() calls is_key()`
- c0059 ..> c0106: `type in __init__`
- c0059 ..> c0109: `_claims() calls repository_identity()`
- c0059 ..> c0109: `_dispose() calls dispose()`
- c0059 ..> c0109: `_repository_identities() calls repository_identity()`
- c0059 ..> c0109: `poll() calls begin_cleanup_cycle()`
- c0059 ..> c0114: `type in __init__`
- c0063 ..> c0062: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0063 ..> c0073: `validate_cleanup_marker() calls is_change_request()`
- c0063 ..> c0074: `type in validate_cleanup_marker`
- c0063 ..> c0075: `type in validate_cleanup_marker`
- c0064 ..> c0044: `type in __init__`
- c0064 ..> c0046: `type in check_repository`
- c0064 ..> c0046: `type in check_source`
- c0064 ..> c0046: `type in mapping_repository`
- c0064 ..> c0048: `check_repository() constructs RepositoryProblem`
- c0064 ..> c0048: `check_source() constructs RepositoryProblem`
- c0064 ..> c0049: `active() constructs ScaffoldProblem`
- c0064 ..> c0049: `context() constructs ScaffoldProblem`
- c0064 ..> c0049: `mapping_repository() constructs ScaffoldProblem`
- c0064 ..> c0049: `ownership_records() constructs ScaffoldProblem`
- c0064 ..> c0049: `snapshot() constructs ScaffoldProblem`
- c0064 ..> c0064: `check_repository() calls check_source()`
- c0064 ..> c0064: `ownership() calls ownership_records()`
- c0064 ..> c0073: `check_source() calls repository()`
- c0064 ..> c0074: `type in check_source`
- c0064 ..> c0075: `type in __init__`
- c0064 ..> c0080: `ownership() calls tasks()`
- c0064 ..> c0085: `type in __init__`
- c0064 ..> c0104: `snapshot() constructs Ticket`
- c0064 ..> c0104: `type in snapshot`
- c0064 ..> c0105: `snapshot() constructs TicketSource`
- c0064 ..> c0107: `check_repository() calls origin()`
- c0064 ..> c0111: `type in __init__`
- c0065 ..> c0005: `initialise() calls save()`
- c0065 ..> c0008: `prepare_foreman() calls install()`
- c0065 ..> c0012: `prepare_foreman() calls prepare()`
- c0065 ..> c0024: `type in __init__`
- c0065 ..> c0036: `load_existing() calls load()`
- c0065 ..> c0036: `prepare_foreman() calls confirm()`
- c0065 ..> c0044: `configure() constructs FactoryConfiguration`
- c0065 ..> c0044: `type in _preflight`
- c0065 ..> c0044: `type in check_foreman`
- c0065 ..> c0044: `type in configure`
- c0065 ..> c0044: `type in initialise`
- c0065 ..> c0044: `type in load_existing`
- c0065 ..> c0045: `_preflight() calls validate()`
- c0065 ..> c0045: `configure() calls unique_labels()`
- c0065 ..> c0045: `load_existing() calls unique_labels()`
- c0065 ..> c0046: `inspect() constructs RepositoryReference`
- c0065 ..> c0046: `type in inspect`
- c0065 ..> c0056: `type in __init__`
- c0065 ..> c0057: `type in __init__`
- c0065 ..> c0065: `configure() calls inspect()`
- c0065 ..> c0065: `initialise() calls _ensure_label()`
- c0065 ..> c0065: `initialise() calls _preflight()`
- c0065 ..> c0066: `prepare_foreman() calls _reviewed_install()`
- c0065 ..> c0066: `prepare_foreman() calls missing_tools()`
- c0065 ..> c0067: `check_foreman() calls check()`
- c0065 ..> c0073: `_preflight() calls repository()`
- c0065 ..> c0073: `inspect() calls repository()`
- c0065 ..> c0075: `type in __init__`
- c0065 ..> c0077: `check_foreman() calls login()`
- c0065 ..> c0083: `type in __init__`
- c0065 ..> c0083: `type in prepare_foreman`
- c0065 ..> c0087: `type in __init__`
- c0065 ..> c0093: `_preflight() constructs FactoryError`
- c0065 ..> c0093: `initialise() constructs FactoryError`
- c0065 ..> c0093: `inspect() constructs FactoryError`
- c0065 ..> c0093: `load_existing() constructs FactoryError`
- c0065 ..> c0093: `prepare_foreman() constructs FactoryError`
- c0065 ..> c0102: `_ensure_label() calls create_label()`
- c0065 ..> c0102: `_preflight() calls check_access()`
- c0065 ..> c0102: `_preflight() calls list_labels()`
- c0065 ..> c0102: `_preflight() calls validate_source()`
- c0065 ..> c0103: `_ensure_label() constructs Label`
- c0065 ..> c0103: `type in _preflight`
- c0065 ..> c0105: `inspect() constructs TicketSource`
- c0065 ..> c0105: `type in _ensure_label`
- c0065 ..> c0105: `type in _preflight`
- c0065 ..> c0106: `type in __init__`
- c0065 ..> c0107: `_preflight() calls origin()`
- c0065 ..> c0107: `discover() calls discover()`
- c0065 ..> c0107: `inspect() calls origin()`
- c0065 ..> c0111: `type in __init__`
- c0066 ..> c0008: `_reviewed_install() calls describe()`
- c0066 ..> c0008: `missing_tools() calls absent()`
- c0066 ..> c0008: `missing_tools() calls unready()`
- c0066 ..> c0057: `type in _reviewed_install`
- c0066 ..> c0057: `type in missing_tools`
- c0067 ..> c0042: `recover() calls snapshot()`
- c0067 ..> c0044: `type in __init__`
- c0067 ..> c0046: `type in _ensure_validated_mapping`
- c0067 ..> c0046: `type in _repository`
- c0067 ..> c0046: `type in check_repository`
- c0067 ..> c0047: `preflight() constructs IntakeProblem`
- c0067 ..> c0049: `_create_plan() constructs ScaffoldProblem`
- c0067 ..> c0049: `_ensure_mapping() constructs ScaffoldProblem`
- c0067 ..> c0049: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0067 ..> c0049: `_recovery_plan() constructs ScaffoldProblem`
- c0067 ..> c0049: `_setup_ownership() constructs ScaffoldProblem`
- c0067 ..> c0049: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0067 ..> c0049: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0067 ..> c0049: `lookup() constructs ScaffoldProblem`
- c0067 ..> c0050: `_create_plan() constructs ScaffoldReadProblem`
- c0067 ..> c0050: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0067 ..> c0050: `lookup() constructs ScaffoldReadProblem`
- c0067 ..> c0050: `prepare() constructs ScaffoldReadProblem`
- c0067 ..> c0050: `recover() constructs ScaffoldReadProblem`
- c0067 ..> c0051: `_create_ownership() constructs UncertainScaffold`
- c0067 ..> c0051: `_create_plan() constructs UncertainScaffold`
- c0067 ..> c0051: `_setup_ownership() constructs UncertainScaffold`
- c0067 ..> c0051: `_sole_recovery_owner() constructs UncertainScaffold`
- c0067 ..> c0051: `prepare() constructs UncertainScaffold`
- c0067 ..> c0063: `_ensure_mapping() calls validate_cleanup_marker()`
- c0067 ..> c0064: `__init__() constructs FactoryRecords`
- c0067 ..> c0064: `_create_ownership() calls ownership()`
- c0067 ..> c0064: `_ensure_mapping() calls check_source()`
- c0067 ..> c0064: `_ensure_worktrees() calls mapping_repository()`
- c0067 ..> c0064: `_prepare_plan() calls active()`
- c0067 ..> c0064: `_prepare_plan() calls context()`
- c0067 ..> c0064: `_setup_ownership() calls ownership()`
- c0067 ..> c0064: `check_repository() calls check_repository()`
- c0067 ..> c0064: `recover() calls active()`
- c0067 ..> c0064: `recover() calls context()`
- c0067 ..> c0064: `recover() calls ownership()`
- c0067 ..> c0065: `preflight() calls inspect()`
- c0067 ..> c0067: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0067 ..> c0067: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0067 ..> c0067: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0067 ..> c0067: `_initial_mappings() calls _repository()`
- c0067 ..> c0067: `_prepare_plan() calls _create_ownership()`
- c0067 ..> c0067: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0067 ..> c0067: `_prepare_plan() calls _setup_ownership()`
- c0067 ..> c0067: `preflight() calls _initial_mappings()`
- c0067 ..> c0067: `preflight() calls _repository()`
- c0067 ..> c0067: `preflight() calls check_repository()`
- c0067 ..> c0067: `prepare() calls _create_plan()`
- c0067 ..> c0067: `prepare() calls _prepare_plan()`
- c0067 ..> c0067: `prepare() calls lookup()`
- c0067 ..> c0067: `prepare() calls preflight()`
- c0067 ..> c0067: `prepare() calls recover()`
- c0067 ..> c0067: `recover() calls _ensure_worktrees()`
- c0067 ..> c0067: `recover() calls _recovery_plan()`
- c0067 ..> c0067: `recover() calls _repository()`
- c0067 ..> c0067: `recover() calls _sole_recovery_owner()`
- c0067 ..> c0067: `recover() calls _validate_recovery_candidates()`
- c0067 ..> c0067: `recover() calls check_repository()`
- c0067 ..> c0067: `unfinished() calls _is_unfinished_factory_plan()`
- c0067 ..> c0068: `_initial_mappings() calls worktree_name()`
- c0067 ..> c0075: `type in __init__`
- c0067 ..> c0077: `check() calls check()`
- c0067 ..> c0080: `_create_ownership() calls create_task()`
- c0067 ..> c0080: `_create_ownership() calls update_plan()`
- c0067 ..> c0080: `_create_plan() calls create_plan()`
- c0067 ..> c0080: `_create_plan() calls get_plan()`
- c0067 ..> c0080: `_create_plan() calls owns()`
- c0067 ..> c0080: `_create_plan() calls plans()`
- c0067 ..> c0080: `_is_unfinished_factory_plan() calls owns()`
- c0067 ..> c0080: `_recovery_plan() calls get_plan()`
- c0067 ..> c0080: `_recovery_plan() calls owns()`
- c0067 ..> c0080: `_recovery_plan() calls plans()`
- c0067 ..> c0080: `lookup() calls plans()`
- c0067 ..> c0080: `unfinished() calls plans()`
- c0067 ..> c0085: `type in __init__`
- c0067 ..> c0093: `_is_unfinished_factory_plan() constructs FactoryError`
- c0067 ..> c0104: `type in _create_plan`
- c0067 ..> c0104: `type in _initial_mappings`
- c0067 ..> c0104: `type in _prepare_plan`
- c0067 ..> c0104: `type in _setup_ownership`
- c0067 ..> c0104: `type in lookup`
- c0067 ..> c0104: `type in preflight`
- c0067 ..> c0104: `type in prepare`
- c0067 ..> c0104: `type in recover`
- c0067 ..> c0105: `type in _repository`
- c0067 ..> c0109: `_ensure_mapping() calls ensure()`
- c0067 ..> c0109: `_ensure_mapping() calls verify_removed()`
- c0067 ..> c0109: `_initial_mappings() calls target_branch()`
- c0067 ..> c0111: `type in __init__`
- c0067 ..> c0114: `type in __init__`
- c0068 ..> c0104: `type in worktree_name`
- c0069 --> c0104: `field issue`
- c0070 ..> c0000: `_alert_plan() calls send()`
- c0070 ..> c0000: `_check_pending_repositories() calls send()`
- c0070 ..> c0000: `_check_planning_access() calls send()`
- c0070 ..> c0000: `_handle_intake_read_problem() calls send()`
- c0070 ..> c0000: `_handle_intake_repository_problem() calls send()`
- c0070 ..> c0000: `_handle_recovery_read_problem() calls send()`
- c0070 ..> c0000: `_load_inventory() calls send()`
- c0070 ..> c0000: `_process_issue() calls send()`
- c0070 ..> c0000: `_read_issues() calls send()`
- c0070 ..> c0000: `_recover_work() calls send()`
- c0070 ..> c0000: `_submit() calls send()`
- c0070 ..> c0000: `_watch() calls close()`
- c0070 ..> c0000: `_watch() calls start()`
- c0070 ..> c0000: `_watch() calls wait()`
- c0070 ..> c0000: `run() calls startup_hint()`
- c0070 ..> c0012: `_process_issue() calls prepare()`
- c0070 ..> c0025: `type in __init__`
- c0070 ..> c0044: `type in _poll_sources`
- c0070 ..> c0044: `type in _repository_for_source`
- c0070 ..> c0044: `type in _watch`
- c0070 ..> c0044: `type in run`
- c0070 ..> c0046: `type in _handle_intake_repository_problem`
- c0070 ..> c0046: `type in _process_issue`
- c0070 ..> c0046: `type in _process_issues`
- c0070 ..> c0046: `type in _process_source`
- c0070 ..> c0046: `type in _repository_for_source`
- c0070 ..> c0048: `type in _handle_intake_repository_problem`
- c0070 ..> c0048: `type in _handle_recovery_repository_problem`
- c0070 ..> c0049: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0070 ..> c0049: `type in _alert_plan`
- c0070 ..> c0049: `type in _handle_intake_scaffold_problem`
- c0070 ..> c0050: `type in _handle_intake_read_problem`
- c0070 ..> c0050: `type in _handle_recovery_read_problem`
- c0070 ..> c0052: `_check_pending_repositories() calls clear()`
- c0070 ..> c0052: `_check_planning_access() calls clear()`
- c0070 ..> c0052: `_complete_intake() calls clear()`
- c0070 ..> c0052: `_complete_recovery() calls clear()`
- c0070 ..> c0052: `_load_inventory() calls clear()`
- c0070 ..> c0052: `_process_issue() calls clear()`
- c0070 ..> c0052: `_read_issues() calls clear()`
- c0070 ..> c0052: `_watch() calls clear()`
- c0070 ..> c0052: `_watch() constructs WatcherAlerts`
- c0070 ..> c0052: `type in _alert_plan`
- c0070 ..> c0052: `type in _check_pending_repositories`
- c0070 ..> c0052: `type in _check_planning_access`
- c0070 ..> c0052: `type in _complete_intake`
- c0070 ..> c0052: `type in _complete_recovery`
- c0070 ..> c0052: `type in _handle_intake_read_problem`
- c0070 ..> c0052: `type in _handle_intake_repository_problem`
- c0070 ..> c0052: `type in _handle_intake_scaffold_problem`
- c0070 ..> c0052: `type in _handle_recovery_read_problem`
- c0070 ..> c0052: `type in _handle_recovery_repository_problem`
- c0070 ..> c0052: `type in _load_inventory`
- c0070 ..> c0052: `type in _poll_sources`
- c0070 ..> c0052: `type in _process_issue`
- c0070 ..> c0052: `type in _process_issues`
- c0070 ..> c0052: `type in _process_source`
- c0070 ..> c0052: `type in _read_issues`
- c0070 ..> c0052: `type in _recover_blocked`
- c0070 ..> c0052: `type in _recover_work`
- c0070 ..> c0052: `type in _remember_inventory_candidate`
- c0070 ..> c0059: `_watch() calls poll()`
- c0070 ..> c0059: `type in __init__`
- c0070 ..> c0064: `_check_pending_repositories() calls check_repository()`
- c0070 ..> c0067: `_check_planning_access() calls check()`
- c0070 ..> c0067: `_load_inventory() calls unfinished()`
- c0070 ..> c0067: `_process_issue() calls lookup()`
- c0070 ..> c0067: `_process_issue() calls recover()`
- c0070 ..> c0067: `_recover_work() calls recover()`
- c0070 ..> c0067: `type in __init__`
- c0070 ..> c0069: `_complete_intake() constructs BlockedWork`
- c0070 ..> c0069: `_handle_intake_read_problem() constructs BlockedWork`
- c0070 ..> c0069: `_handle_intake_repository_problem() constructs BlockedWork`
- c0070 ..> c0069: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0070 ..> c0069: `_process_issue() constructs BlockedWork`
- c0070 ..> c0069: `_remember_inventory_candidate() constructs BlockedWork`
- c0070 ..> c0069: `type in _alert_plan`
- c0070 ..> c0069: `type in _complete_intake`
- c0070 ..> c0069: `type in _complete_recovery`
- c0070 ..> c0069: `type in _handle_recovery_read_problem`
- c0070 ..> c0069: `type in _handle_recovery_repository_problem`
- c0070 ..> c0069: `type in _recover_work`
- c0070 ..> c0069: `type in _remember_task_ids`
- c0070 ..> c0070: `_complete_intake() calls _submit()`
- c0070 ..> c0070: `_complete_recovery() calls _submit()`
- c0070 ..> c0070: `_handle_intake_read_problem() calls _sole_task_id()`
- c0070 ..> c0070: `_handle_intake_repository_problem() calls _alert_plan()`
- c0070 ..> c0070: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0070 ..> c0070: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0070 ..> c0070: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0070 ..> c0070: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0070 ..> c0070: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0070 ..> c0070: `_load_inventory() calls _remember_inventory_candidate()`
- c0070 ..> c0070: `_poll_sources() calls _baseline_source()`
- c0070 ..> c0070: `_poll_sources() calls _process_source()`
- c0070 ..> c0070: `_poll_sources() calls _read_issues()`
- c0070 ..> c0070: `_poll_sources() calls _repository_for_source()`
- c0070 ..> c0070: `_process_issue() calls _complete_intake()`
- c0070 ..> c0070: `_process_issue() calls _handle_intake_read_problem()`
- c0070 ..> c0070: `_process_issue() calls _handle_intake_repository_problem()`
- c0070 ..> c0070: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0070 ..> c0070: `_process_issues() calls _process_issue()`
- c0070 ..> c0070: `_process_issues() calls _skip_issue()`
- c0070 ..> c0070: `_process_source() calls _include_pending_lookups()`
- c0070 ..> c0070: `_process_source() calls _process_issues()`
- c0070 ..> c0070: `_recover_blocked() calls _recover_work()`
- c0070 ..> c0070: `_recover_work() calls _alert_plan()`
- c0070 ..> c0070: `_recover_work() calls _complete_recovery()`
- c0070 ..> c0070: `_recover_work() calls _handle_recovery_read_problem()`
- c0070 ..> c0070: `_recover_work() calls _handle_recovery_repository_problem()`
- c0070 ..> c0070: `_recover_work() calls _remember_task_ids()`
- c0070 ..> c0070: `_remember_inventory_candidate() calls _alert_plan()`
- c0070 ..> c0070: `_watch() calls _check_pending_repositories()`
- c0070 ..> c0070: `_watch() calls _check_planning_access()`
- c0070 ..> c0070: `_watch() calls _load_inventory()`
- c0070 ..> c0070: `_watch() calls _poll_sources()`
- c0070 ..> c0070: `_watch() calls _recover_blocked()`
- c0070 ..> c0070: `run() calls _watch()`
- c0070 ..> c0071: `_watch() constructs _WatchState`
- c0070 ..> c0071: `type in _baseline_source`
- c0070 ..> c0071: `type in _check_pending_repositories`
- c0070 ..> c0071: `type in _check_planning_access`
- c0070 ..> c0071: `type in _complete_intake`
- c0070 ..> c0071: `type in _complete_recovery`
- c0070 ..> c0071: `type in _handle_intake_read_problem`
- c0070 ..> c0071: `type in _handle_intake_repository_problem`
- c0070 ..> c0071: `type in _handle_intake_scaffold_problem`
- c0070 ..> c0071: `type in _handle_recovery_repository_problem`
- c0070 ..> c0071: `type in _load_inventory`
- c0070 ..> c0071: `type in _poll_sources`
- c0070 ..> c0071: `type in _process_issue`
- c0070 ..> c0071: `type in _process_issues`
- c0070 ..> c0071: `type in _process_source`
- c0070 ..> c0071: `type in _recover_blocked`
- c0070 ..> c0071: `type in _recover_work`
- c0070 ..> c0071: `type in _remember_inventory_candidate`
- c0070 ..> c0071: `type in _skip_issue`
- c0070 ..> c0072: `type in _process_issue`
- c0070 ..> c0072: `type in _recover_work`
- c0070 ..> c0093: `_read_issues() constructs FactoryError`
- c0070 ..> c0101: `_submit() calls check_watch_stop()`
- c0070 ..> c0101: `_watch() calls check_watch_stop()`
- c0070 ..> c0101: `run() calls check_watch_stop()`
- c0070 ..> c0102: `_read_issues() calls list_open()`
- c0070 ..> c0104: `type in _baseline_source`
- c0070 ..> c0104: `type in _complete_intake`
- c0070 ..> c0104: `type in _complete_recovery`
- c0070 ..> c0104: `type in _handle_intake_read_problem`
- c0070 ..> c0104: `type in _handle_intake_repository_problem`
- c0070 ..> c0104: `type in _handle_intake_scaffold_problem`
- c0070 ..> c0104: `type in _include_pending_lookups`
- c0070 ..> c0104: `type in _process_issue`
- c0070 ..> c0104: `type in _process_issues`
- c0070 ..> c0104: `type in _process_source`
- c0070 ..> c0104: `type in _read_issues`
- c0070 ..> c0104: `type in _skip_issue`
- c0070 ..> c0104: `type in _submit`
- c0070 ..> c0105: `_watch() constructs TicketSource`
- c0070 ..> c0105: `type in _baseline_source`
- c0070 ..> c0105: `type in _include_pending_lookups`
- c0070 ..> c0105: `type in _poll_sources`
- c0070 ..> c0105: `type in _process_source`
- c0070 ..> c0105: `type in _read_issues`
- c0070 ..> c0105: `type in _repository_for_source`
- c0070 ..> c0106: `type in __init__`
- c0071 --> c0046: `field pending_repositories`
- c0071 --> c0069: `field blocked`
- c0071 --> c0069: `field known`
- c0071 --> c0104: `field pending_lookup`
- c0071 --> c0105: `field baselined`
- c0073 ..> c0074: `repository() constructs RepositoryRef`
- c0073 ..> c0074: `type in is_change_request`
- c0073 ..> c0074: `type in repository`
- c0073 ..> c0093: `repository() constructs FactoryError`
- c0075 ..> c0074: `type in is_change_request`
- c0075 ..> c0074: `type in repository`
- c0076 ..> c0007: `uses_browser_login() calls request()`
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
- c0078 ..> c0042: `role_environment() calls update()`
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
- c0080 ..> c0067: `check() calls check()`
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
- c0082 ..> c0067: `check() calls check()`
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
- c0088 ..> c0005: `enter() calls run()`
- c0088 ..> c0093: `enter() constructs FactoryError`
- c0089 ..> c0090: `describe() calls ubuntu_tmux()`
- c0089 ..> c0090: `install() calls ubuntu_tmux()`
- c0089 ..> c0093: `install() constructs FactoryError`
- c0089 ..> c0094: `absent() calls executable_path()`
- c0089 ..> c0095: `install() calls no_installer()`
- c0089 ..> c0095: `install() calls run_install()`
- c0092 ..> c0005: `run_command() calls run()`
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
- c0096 ..> c0000: `_generated_parent() calls close()`
- c0096 ..> c0000: `check_skill_file() calls close()`
- c0096 ..> c0036: `read_generated_json() calls load()`
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
- c0098 ..> c0000: `_close_capture_streams() calls close()`
- c0098 ..> c0000: `_terminate_owned_process() calls wait()`
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
- c0109 ..> c0039: `_network_git() calls quote()`
- c0109 ..> c0052: `begin_cleanup_cycle() calls clear()`
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

- Type1: `object | None`
- Type2: `int | None`
- Type3: `str | None`
- Type4: `tuple[Path, Path, int]`
- Type5: `dict | None`
- Type6: `tuple[Path, Path]`
- Type7: `dict[str, str] | None`
- Type8: `subprocess.Popen | None`
- Type9: `Callable[[ForgetfulConnection, str], dict[str, str]]`
- Type10: `Callable[[ForgetfulConnection], list[str]]`
- Type11: `dict[tuple[str, Path], list[str]]`
- Type12: `bool | None`
- Type13: `Path | None`
- Type14: `dict[str, bytes]`
- Type15: `tuple[str, ...]`
- Type16: `dict[Path, None]`
- Type17: `frozenset[tuple[int, int]]`
- Type18: `Callable[[str], bool]`
- Type19: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type20: `list[Path] | None`
- Type21: `ForgetfulConnection | None`
- Type22: `list[str] | tuple[str, ...]`
- Type23: `int | dict`
- Type24: `int | dict | str`
- Type25: `str | Path`
- Type26: `FactoryConfiguration | None`
- Type27: `tuple[int, int]`
- Type28: `Iterator[PlainWatchObservation | None]`
- Type29: `Callable[[str], None]`
- Type30: `tuple[RepositoryReference, ...]`
- Type31: `tuple[int, ...] | None`
- Type32: `dict[str, str]`
- Type33: `'CleanupSet'`
- Type34: `dict[int, int]`
- Type35: `tuple | None`
- Type36: `tuple[dict, dict] | None`
- Type37: `dict[int, list[dict]]`
- Type38: `list[dict] | None`
- Type39: `list[CompletedWork] | None`
- Type40: `CleanupState | None`
- Type41: `Callable[[ForgetfulConnection], Sequence[ToolInstaller]]`
- Type42: `Callable[[list[str]], None]`
- Type43: `Callable[[str, str], bool]`
- Type44: `list[str] | None`
- Type45: `dict[str, RepositoryReference]`
- Type46: `dict[TicketSource, tuple[Label, ...]]`
- Type47: `Callable[[], FactoryConfiguration | None]`
- Type48: `tuple[ToolInstaller | None, str | None]`
- Type49: `tuple[list[dict], list[dict]]`
- Type50: `tuple[Ticket, dict] | None`
- Type51: `Ticket | None`
- Type52: `tuple[int, ...]`
- Type53: `Callable[[], bool]`
- Type54: `tuple[set[str], bool]`
- Type55: `tuple[TicketSource, ...]`
- Type56: `tuple[Ticket, ...]`
- Type57: `dict[str, Ticket]`
- Type58: `BlockedWork | None`
- Type59: `tuple[Ticket, ...] | None`
- Type60: `dict[str, BlockedWork]`
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
- Signature15: `+build_tools(workspace: Path, connection: ForgetfulConnection, term_grace: float)
  unknown`
- Signature16: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown, deadlines: DeadlinePolicy, observation: unknown) WatchFactory`
- Signature17: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown, term_grace: float) unknown`
- Signature18: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature19: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature20: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature21: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature22: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature23: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature24: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature25: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature26: `-_foreman_memory_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown, connection: ForgetfulConnection) InitialAgentChoices`
- Signature27: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature28: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature29: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int |
  dict`
- Signature30: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature31: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature32: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None, deadlines: DeadlinePolicy) int | dict`
- Signature33: `-_initialise_locked(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int | dict | str`
- Signature34: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown, deadlines: unknown) unknown`
- Signature35: `+update_resources(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int`
- Signature36: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature37: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature38: `-__init__(records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts,
  ticketing: Ticketing) unknown`
- Signature39: `-_claim_indexes(inventory: list[dict], plans: list[dict], tasks: dict[int,
  list[dict]], identities: dict[str, str], alerts: WatcherAlerts) tuple[dict, dict] | None`
- Signature40: `-_dispose(work: CompletedWork, mapping: dict, claims: dict, references: dict,
  identities: dict[str, str], alerts: WatcherAlerts, report: unknown) bool`
- Signature41: `-_mapping_identity(plan_id: int, reference: str, mapping: dict, workspace: str |
  None) CleanupSet`
- Signature42: `-__init__(planning: PlanStore, workspace: Path, config: FactoryConfiguration,
  repositories: LocalRepositories, forge: Forge) unknown`
- Signature43: `-__init__(tracking: Ticketing, storage: ConfigurationStore, repositories:
  LocalRepositories, forge: Forge, team: AgentTeam, planning: PlanningSetup, tools:
  Callable[[ForgetfulConnection], Sequence[ToolInstaller]]) unknown`
- Signature44: `-__init__(planning: PlanStore, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, forge: Forge) unknown`
- Signature45: `-_setup_ownership(plan_id: int, issue: Ticket, context: dict, initial_mappings:
  list[dict]) tuple[list[dict], list[dict]]`
- Signature46: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature47: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature48: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature49: `-__init__(tracking: Ticketing, terminal: ForemanTerminal, scaffold: ScaffoldIssue,
  cleanup: CleanupCompleted) unknown`
- Signature50: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature51: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature52: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature53: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature54: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature55: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature56: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Ticket, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature57: `-_poll_sources(sources: tuple[TicketSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature58: `-_process_source(source: TicketSource, issues: tuple[Ticket, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature59: `-_baseline_source(source: TicketSource, issues: tuple[Ticket, ...], state:
  _WatchState, report: Callable[[str], None]) None`
- Signature60: `-_repository_for_source(config: FactoryConfiguration, source: TicketSource)
  RepositoryReference`
- Signature61: `-_include_pending_lookups(source: TicketSource, current: dict[str, Ticket],
  pending_lookup: dict[str, Ticket]) None`
- Signature62: `-_process_issues(issues: tuple[Ticket, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature63: `-_process_issue(issue: Ticket, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature64: `-_handle_intake_repository_problem(issue: Ticket, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature65: `-_handle_intake_read_problem(issue: Ticket, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature66: `-_handle_intake_scaffold_problem(issue: Ticket, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature67: `-_complete_intake(issue: Ticket, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature68: `-_submit(issue: Ticket, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
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
