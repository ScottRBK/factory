# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 121 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 5483. Type relationships removed: 113.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/contracts/agents.py`: 15 source occurrences (test-path).
- `tests/contracts/channels.py`: 5 source occurrences (test-path).
- `tests/contracts/factory.py`: 5 source occurrences (test-path).
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
- `tests/test_agreement_contract.py`: 4 source occurrences (test-path).
- `tests/test_architecture.py`: 33 source occurrences (test-path).
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
- `tests/test_init_sources.py`: 2 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 20 source occurrences (test-path).
- `tests/test_local_skills.py`: 21 source occurrences (test-path).
- `tests/test_managed_watcher_alerts.py`: 10 source occurrences (test-path).
- `tests/test_native_assisted_reload.py`: 3 source occurrences (test-path).
- `tests/test_native_roles.py`: 15 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_normalized_lifecycle.py`: 14 source occurrences (test-path).
- `tests/test_operator_transcripts.py`: 30 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_owner_startup.py`: 22 source occurrences (test-path).
- `tests/test_persistent_foreman_contract.py`: 7 source occurrences (test-path).
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
- `tests/test_runtime_host.py`: 12 source occurrences (test-path).
- `tests/test_saved_data.py`: 14 source occurrences (test-path).
- `tests/test_second_provider.py`: 8 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 24 source occurrences (test-path).
- `tests/test_ticketing.py`: 20 source occurrences (test-path).
- `tests/test_ticketing_contract.py`: 18 source occurrences (test-path).
- `tests/test_tool_installer_contract.py`: 24 source occurrences (test-path).
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
    class c0007["AgentShellOwner"] {
        <<class>>
        -__init__(Signature8)
        +workspace: unknown
        +python: unknown
        +deadlines: unknown
        +host: unknown
        +saved() Type5
        +status() dict
        +start(environment: Type6, launch: dict) dict
        +report() Type5
    }
    class c0008["src/forgetful_factory/agents/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type5
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(Signature9)
    }
    class c0009["AgentShellRuntimeInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +project: unknown
        +term_grace: unknown
        -_inputs() Type7
        +absent() list[str]
        +unready() list[str]
        +ready() bool
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0010["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature10)
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
        +process: Type9
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
    class c0011["src/forgetful_factory/agents/adapters/agentshell/tmux_host.py"] {
        <<module>>
        +retain_identity(session: unknown, reply: unknown) None
        +pin_worker(target: unknown) int
    }
    class c0012["src/forgetful_factory/agents/adapters/pi/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        -_local_selection(value: object, field: str, message: str) str
        -_validate_agent(value: object) dict
        -_validate_roster(path: Path, value: object, agent_type: str) None
        -_validate_resources(value: object) None
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0013["PiAgentTeam"] {
        <<class>>
        -__init__(Signature11)
        +workspace: unknown
        +term_grace: unknown
        +role_environment: unknown
        +missing_tools: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type5
        -_model_catalogs: Type12
        -_managed_memory_selected: Type13
        +prepare_setup_guidance() None
        +validate_setup(Signature12)
        +validate_bundled_resources(include_memory_extension: bool) None
        -_install_resources() None
        -_protect_runtime() None
        +prepare() None
        +save_pi_choice() None
        +prepare_roles(Signature13)
        +validate_worker_models(Signature14)
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type14) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type3
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +begin_setup() None
        +validate_completion() None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0014["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(execution_enabled: bool, choices: unknown) None
        -_write_foreman_memory(choices: unknown) None
        -_write_agent(Signature15)
        +validate_guidance(execution_enabled: bool) None
    }
    class c0015["src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0016["src/forgetful_factory/agents/adapters/pi/native_home.py"] {
        <<module>>
        +saved_pi_home(workspace: Path) str
    }
    class c0017["ResourceUpdate"] {
        <<class>>
        +directory: Path
        +files: Type15
        +add: Type16
        +replace: Type16
        +edited: Type16
    }
    class c0018["src/forgetful_factory/agents/adapters/pi/role_resources.py"] {
        <<module>>
        -_digest(data: bytes) str
        +bundled_files() Type15
        +plan_update(directory: Path) ResourceUpdate
        -_back_up(update: ResourceUpdate, backups: Path) Path
        +apply_update(update: ResourceUpdate, backups: Path) Type14
    }
    class c0019["PiInstall"] {
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
    class c0020["src/forgetful_factory/agents/adapters/pi/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type17) None
        -_walk_skill_directory(directory: Path, ancestors: Type18, files: Type17) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0021["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0022["AgentShellLifecycleDeadlines"] {
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
    class c0023["InitialAgentChoices"] {
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
    class c0024["src/forgetful_factory/agents/model.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type16
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
        +unknown_status(source: str, observation: str) dict
    }
    class c0025["AgentTeam"] {
        <<class>>
        +prepare() None
        +prepare_setup_guidance() None
        +choose_pi_home(requested: Type3, confirm: Type19) str
        +save_pi_choice() None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type14) list[str]
        +prepare_roles(Signature13)
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type3
        +begin_setup() None
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +validate_completion() None
        +validate_bundled_resources(include_memory_extension: bool) None
    }
    class c0026["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0027["PersistentForeman"] {
        <<class>>
        +saved() Type5
        +status() dict
        +report() Type5
        +start(environment: Type6, launch: dict) dict
    }
    class c0028["TerminalChannel"] {
        <<class>>
        -__init__(host: SessionHost) unknown
        +host: unknown
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0029["Channel"] {
        <<class>>
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0030["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_host() TmuxHost
        +build_channel() TerminalChannel
        +build_owner(workspace: Path, python: str, deadlines: DeadlinePolicy) AgentShellOwner
        +build_tools(Signature16)
        +build_team(workspace: Path, term_grace: float) PiAgentTeam
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +select_ticketing(config: FactoryConfiguration, command_timeout: float) Ticketing
        +build_watcher(Signature17)
        +prepare_foreman_launch(Signature18)
        +build_watch_status(workspace: Path, python: str, deadlines: DeadlinePolicy) WatchStatus
        +build_start_foreman(Signature19)
    }
    class c0031["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0032["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0033["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature20)
        -_check_existing_connection(Signature21)
        -_connection(Signature22)
        -_prepare_foreman(Signature23)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type23, show_choices: bool, prompt: Type3) str
        -_select_model(Signature24)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_change_managed_watch(args: argparse.Namespace, workspace: Path) int
        -_watch_status(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_watch(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_foreman(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_watch_locked(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature25)
        -_owner_choices(Signature26)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature27)
        -_foreman_memory_choices(Signature28)
        -_managed_rest_mapping_available(connection: ForgetfulConnection) bool
        -_worker_choices(Signature29)
        -_complete_setup(Signature30)
        -_initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type5) None
        -_finish_existing_setup(Signature31)
        -_discover_worker_models(Signature32)
        -_validate_initial_model(Signature33)
        -_start_initial_setup(Signature34)
        -_initialise_locked(Signature35)
        -_launch_setup_foreman(Signature36)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0034["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0035["src/forgetful_factory/cli/resource_update.py"] {
        <<module>>
        -_report(update: unknown, force: bool) None
        +update_resources(Signature37)
    }
    class c0036["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type26) FactoryConfiguration
    }
    class c0037["FileCleanupReceipts"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +path: unknown
        +load() set[CleanupSet]
        -_load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0038["src/forgetful_factory/factory/adapters/cleanup_receipts.py"] {
        <<module>>
        -_unique_object(pairs: unknown) unknown
        -_resource(value: object) CleanupSet
    }
    class c0039["MarkdownAgreement"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +location: str
        +found() bool
        +write(text: str) None
        +read() str
    }
    class c0040["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type27
        +save(configuration: FactoryConfiguration) None
    }
    class c0041["src/forgetful_factory/factory/adapters/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0042["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0043["ObservedTerminal"] {
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
    class c0044["PlainWatchObservation"] {
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
    class c0045["src/forgetful_factory/factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type28
        -_read_discovery(workspace: Path) dict
        +plain_watch_status(workspace: Path) Type5
        +observe_plain_watch(workspace: Path, report_unavailable: Type30) Type29
    }
    class c0046["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type16
        +foreman_agent_file: str
        +repository: Type31
        +forgetful: Type22
        +execution_enabled: bool
    }
    class c0047["src/forgetful_factory/factory/model/configuration.py"] {
        <<module>>
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type16
    }
    class c0048["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: TicketSource
    }
    class c0049["IntakeProblem"] {
        <<class>>
    }
    class c0050["RepositoryProblem"] {
        <<class>>
    }
    class c0051["ScaffoldProblem"] {
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
    class c0052["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0053["UncertainScaffold"] {
        <<class>>
    }
    class c0054["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type6
        +last_diagnostic: Type6
        +clear(subject: str) None
        +send(Signature39)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0055["src/forgetful_factory/factory/model/watcher_problems.py"] {
        <<module>>
        -_cleanup_recovery(code: str) str
    }
    class c0056["AgreementStore"] {
        <<class>>
        +location: str
        +found() bool
        +write(text: str) None
        +read() str
    }
    class c0057["CleanupReceipts"] {
        <<class>>
        +load() set[CleanupSet]
        +confirm(resource: CleanupSet) None
    }
    class c0058["CleanupSet"] {
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
    class c0059["ConfigurationStore"] {
        <<class>>
        +load() Type27
        +save(configuration: FactoryConfiguration) None
    }
    class c0060["ToolInstaller"] {
        <<class>>
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0061["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0062["CleanupCompleted"] {
        <<class>>
        -__init__(Signature40)
        +records: unknown
        +ticketing: unknown
        +worktrees: unknown
        +owners: Type34
        +receipts: unknown
        +confirmed: set[CleanupSet]
        +cursor: Type35
        +poll(alerts: WatcherAlerts, report: unknown) None
        -_claim_indexes(Signature41)
        -_read_plans(inventory: list[dict], alerts: WatcherAlerts) Type38
        -_candidates(plans: list[dict], tasks: Type37, alerts: WatcherAlerts) Type39
        -_candidate(plan: dict, tasks: list[dict]) CompletedWork
        -_read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) None
        -_in_scope(plan: dict) bool
        -_repository_identities(alerts: WatcherAlerts) Type8
        -_keys(mapping: dict, identities: Type6) set[tuple]
        -_claims(tasks: list[dict], plan_id: int, claims: dict, identities: Type6) None
        -_task_mappings(task: dict) list[dict]
        -_validate_claim_mapping(mapping: object) None
        -_overlaps(mapping: dict, claims: dict) bool
        -_dispose(Signature42)
        -_order(work: CompletedWork, mapping: dict) tuple
        -_check_namespaces(mappings: list[dict], identities: Type6) None
        -_mapping_identity(Signature43)
        -_is_confirmed(plan_id: int, reference: str, mapping: dict, workspace: Type3) bool
        -_still_completed(work: CompletedWork) bool
    }
    class c0063["CompletedWork"] {
        <<class>>
        +plan_id: int
        +reference: str
        +task_id: int
        +mappings: list[dict]
    }
    class c0064["src/forgetful_factory/factory/services/cleanup_completed.py"] {
        <<module>>
        -_claim_path(value: str) str
    }
    class c0065["CleanupMarkerError"] {
        <<class>>
    }
    class c0066["src/forgetful_factory/factory/services/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict, forge: Forge, repository: RepositoryRef) Type40
    }
    class c0067["src/forgetful_factory/factory/services/definition_of_done.py"] {
        <<module>>
        +agree_definition_of_done(Signature44)
        -_deployment_agreement(answer: str, ask: Type41, say: Type30) str
    }
    class c0068["FactoryRecords"] {
        <<class>>
        -__init__(Signature45)
        +planning: unknown
        +workspace: unknown
        +config: unknown
        +repositories: unknown
        +forge: unknown
        +ticketing: unknown
        +check_repository(repository: RepositoryReference) None
        +check_source(repository: RepositoryReference) RepositoryRef
        +snapshot(context: dict, external_ref: str) Ticket
        +active(plan: dict) bool
        +context(plan: dict) dict
        +ownership(plan_id: int, external_ref: str) list[dict]
        +ownership_records(plan_id: int, external_ref: str, tasks: list[dict]) list[dict]
        +mapping_repository(mapping: dict, seen: set[str]) RepositoryReference
    }
    class c0069["InitialiseFactory"] {
        <<class>>
        -__init__(Signature46)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +forge: unknown
        +team: unknown
        +planning: unknown
        +tools: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type43, confirm: Type44) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type21, labels: Type45) Type27
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type46
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type47
        -_ensure_label(source: TicketSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type48, save: bool) list[str]
    }
    class c0070["src/forgetful_factory/factory/services/initialise_factory.py"] {
        <<module>>
        +missing_tools(tools: Sequence[ToolInstaller]) list[str]
        -_reviewed_install(tools: Sequence[ToolInstaller], name: str) Type49
    }
    class c0071["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature47)
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
        -_setup_ownership(Signature48)
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature49)
        +lookup(issue: Ticket) Type2
        -_create_plan(issue: Ticket) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type52, task_ids: Type32) Type51
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature50)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_is_unfinished_factory_plan(summary: dict, prefixes: set[str]) bool
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_validated_mapping(Signature51)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0072["src/forgetful_factory/factory/services/scaffold_issue.py"] {
        <<module>>
        +worktree_name(ticket: Ticket) str
    }
    class c0073["StartForeman"] {
        <<class>>
        -__init__(Signature52)
        +lease: unknown
        +owner: unknown
        +channel: unknown
        +prepare: unknown
        +run(attach: bool, notify: Type30) None
    }
    class c0074["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type2
        +issue: Type52
        +task_ids: Type32
        +recovered: bool
        +setup_paths: Type16
        +setup_cause: Type3
    }
    class c0075["WatchFactory"] {
        <<class>>
        -__init__(Signature53)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +cleanup: unknown
        +run(Signature54)
        -_watch(Signature55)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type30) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature56)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type30) Type56
        -_recover_work(Signature57)
        -_handle_recovery_repository_problem(Signature58)
        -_handle_recovery_read_problem(Signature59)
        -_remember_task_ids(work: BlockedWork, task_ids: Type32) None
        -_complete_recovery(Signature60)
        -_poll_sources(Signature61)
        -_process_source(Signature62)
        -_baseline_source(Signature63)
        -_repository_for_source(Signature64)
        -_include_pending_lookups(Signature65)
        -_process_issues(Signature66)
        -_skip_issue(issue: Ticket, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature67)
        -_handle_intake_repository_problem(Signature68)
        -_handle_intake_read_problem(Signature69)
        -_handle_intake_scaffold_problem(Signature70)
        -_complete_intake(Signature71)
        -_sole_task_id(task_ids: Type32) Type2
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature72)
        -_read_issues(source: TicketSource, labels: Type16, alerts: WatcherAlerts) Type61
    }
    class c0076["_WatchState"] {
        <<class>>
        +seen: Type6
        +baseline: Type6
        +baselined: set[TicketSource]
        +blocked: Type62
        +pending_lookup: Type59
        +known: Type62
        +recovered: set[str]
        +pending_repositories: Type46
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0077["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0078["WatchStatus"] {
        <<class>>
        -__init__(Signature73)
        +plain: unknown
        +owner: unknown
        +storage: unknown
        +team: unknown
        +report() dict
        -_without_live_plain(plain: Type5) dict
        -_setup() str
    }
    class c0079["GitHubForge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0080["RepositoryRef"] {
        <<class>>
        +forge: str
        +reference: str
    }
    class c0081["Forge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0082["src/forgetful_factory/planning/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0083["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +role: unknown
        +term_grace: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type6
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0084["src/forgetful_factory/planning/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature74)
        -_catalog_tools(catalog: object) dict
    }
    class c0085["ForgetfulInstall"] {
        <<class>>
        -__init__(workspace: Path, connection: ForgetfulConnection, term_grace: float) unknown
        +workspace: unknown
        +connection: unknown
        +directory: unknown
        +term_grace: unknown
        -_was_absent: unknown
        -_required() bool
        -_selected() Type3
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
        -_python() str
        +install(name: str) None
    }
    class c0086["ForgetfulPlanStore"] {
        <<class>>
        -__init__(Signature75)
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
    class c0087["src/forgetful_factory/planning/adapters/forgetful/plan_store.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0088["ForgetfulSetup"] {
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
    class c0089["ForgetfulConnection"] {
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
    class c0090["src/forgetful_factory/planning/model.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type22
    }
    class c0091["PlanStore"] {
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
    class c0092["PlanningReadError"] {
        <<class>>
    }
    class c0093["PlanningSetup"] {
        <<class>>
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +prepare(connection: ForgetfulConnection) None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection, execution_enabled: bool) str
    }
    class c0094["TmuxHost"] {
        <<class>>
        +spec() dict
        +how_to_attach(session_name: str) str
        +enter(target: dict) None
    }
    class c0095["TmuxInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +term_grace: unknown
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0096["src/forgetful_factory/runtime/adapters/tmux.py"] {
        <<module>>
        +ubuntu_tmux() bool
    }
    class c0097["SessionHost"] {
        <<class>>
        +spec() dict
        +how_to_attach(session_name: str) str
        +enter(target: dict) None
    }
    class c0098["src/forgetful_factory/shared/command.py"] {
        <<module>>
        +run_command(arguments: list[str], timeout: float, env: Type8, stdin: Type2) str
    }
    class c0099["FactoryError"] {
        <<class>>
    }
    class c0100["src/forgetful_factory/shared/executables.py"] {
        <<module>>
        +executable_path(workspace: Path) str
    }
    class c0101["src/forgetful_factory/shared/installation.py"] {
        <<module>>
        +sync_fingerprint(inputs: Type64) str
        +runtime_ready(runtime: Path, inputs: Type64, probe: str, term_grace: float) bool
        +install_environment(extra: Type8) Type6
        +run_install(Signature76)
        +check_uv(workspace: Path, term_grace: float) None
        +require_manager(manager: str) None
        +install_locks(directory: Path, names: Type16) str
        +no_installer() FactoryError
    }
    class c0102["src/forgetful_factory/shared/resource_files.py"] {
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
    class c0103["src/forgetful_factory/shared/resources.py"] {
        <<module>>
        +resource_root() Path
    }
    class c0104["src/forgetful_factory/shared/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen, term_grace: float) None
        +run_owned(Signature77)
    }
    class c0105["src/forgetful_factory/shared/validation.py"] {
        <<module>>
        +nonblank(value: object, field: str) str
        +positive_duration(name: str, value: object) None
    }
    class c0106["WatchStop"] {
        <<class>>
        +requested: bool
        +interrupt(_signum: unknown, _frame: unknown) None
    }
    class c0107["src/forgetful_factory/shared/watch_stop.py"] {
        <<module>>
        +watch_stop_scope() unknown
        +check_watch_stop() None
    }
    class c0108["GitHubTicketing"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        -_api(source: TicketSource, suffix: str, #42;arguments: str) object
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type66
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type16) Type58
        -_ticket(source: TicketSource, item: dict) Ticket
        -_comments(source: TicketSource, number: int) Type67
        -_milestone(item: object) object
        -_validate_issue(source: TicketSource, item: dict) None
    }
    class c0109["Label"] {
        <<class>>
        +name: str
    }
    class c0110["Ticket"] {
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
    class c0111["TicketSource"] {
        <<class>>
        +provider: str
        +reference: str
        +id_prefix: str
    }
    class c0112["Ticketing"] {
        <<class>>
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type66
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type16) Type58
    }
    class c0113["GitRepositories"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0114["src/forgetful_factory/workspace/adapters/git/repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0115["GitWorktrees"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +cleanup_defaults: Type68
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        -_read_git(arguments: list[str]) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type69
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type70
        -_validate_registered_worktree(Signature78)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
        -_disposal_state(Signature79)
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
    class c0116["src/forgetful_factory/workspace/adapters/git/worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0117["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0118["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type3) unknown
        +code: unknown
        +paths: unknown
    }
    class c0119["WorktreeReadError"] {
        <<class>>
    }
    class c0120["Worktrees"] {
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
    c0000 ..> c0010 : close() calls close()
    c0000 ..> c0099 : 2 relationships (see list)
    c0000 ..> c0107 : 2 relationships (see list)
    c0002 ..> c0000 : 5 relationships (see list)
    c0002 ..> c0001 : serve() constructs SessionState
    c0002 ..> c0002 : 16 relationships (see list)
    c0002 ..> c0011 : 2 relationships (see list)
    c0002 ..> c0086 : 4 relationships (see list)
    c0003 ..> c0099 : runtime_directory() constructs FactoryError
    c0003 ..> c0102 : runtime_directory() calls check_real_path()
    c0004 ..> c0013 : main() calls list_models()
    c0005 ..> c0000 : 11 relationships (see list)
    c0005 ..> c0005 : 27 relationships (see list)
    c0005 ..> c0006 : 2 relationships (see list)
    c0005 ..> c0022 : 2 relationships (see list)
    c0005 ..> c0039 : 6 relationships (see list)
    c0005 ..> c0041 : _apply_controller_problem() calls quote()
    c0005 ..> c0086 : 2 relationships (see list)
    c0005 ..> c0099 : 10 relationships (see list)
    c0005 ..> c0102 : save() calls replace_generated_json()
    c0006 ..> c0000 : 3 relationships (see list)
    c0006 ..> c0003 : _prepare_owner_startup() calls runtime_directory()
    c0006 ..> c0005 : 3 relationships (see list)
    c0006 ..> c0006 : 5 relationships (see list)
    c0006 ..> c0008 : _prepare_owner_startup() calls read_state()
    c0006 ..> c0041 : _acquire_owner_lock() calls quote()
    c0006 ..> c0086 : main() calls create_task()
    c0006 ..> c0099 : 3 relationships (see list)
    c0007 ..> c0008 : 5 relationships (see list)
    c0007 ..> c0022 : 2 relationships (see list)
    c0007 ..> c0024 : report() calls unknown_status()
    c0007 ..> c0041 : report() calls quote()
    c0007 ..> c0097 : type in __init__
    c0008 ..> c0000 : 2 relationships (see list)
    c0008 ..> c0003 : 3 relationships (see list)
    c0008 ..> c0005 : start_owner() calls run()
    c0008 ..> c0008 : 3 relationships (see list)
    c0008 ..> c0022 : 2 relationships (see list)
    c0008 ..> c0041 : request() calls quote()
    c0008 ..> c0094 : start_owner() calls spec()
    c0008 ..> c0097 : type in start_owner
    c0008 ..> c0099 : 4 relationships (see list)
    c0008 ..> c0102 : read_state() calls read_generated_json()
    c0009 ..> c0009 : 3 relationships (see list)
    c0009 ..> c0099 : install() constructs FactoryError
    c0009 ..> c0101 : 5 relationships (see list)
    c0010 ..> c0000 : close() calls close()
    c0010 ..> c0010 : 5 relationships (see list)
    c0010 ..> c0022 : 2 relationships (see list)
    c0010 ..> c0028 : startup_hint() calls how_to_reach()
    c0010 ..> c0029 : type in __init__
    c0010 ..> c0039 : 2 relationships (see list)
    c0010 ..> c0094 : start() calls spec()
    c0010 ..> c0097 : type in __init__
    c0010 ..> c0099 : 4 relationships (see list)
    c0010 ..> c0107 : 3 relationships (see list)
    c0011 ..> c0000 : pin_worker() calls close()
    c0012 ..> c0012 : 8 relationships (see list)
    c0012 ..> c0099 : 2 relationships (see list)
    c0012 ..> c0105 : 4 relationships (see list)
    c0013 ..> c0012 : selected_launch() calls foreman_launch()
    c0013 ..> c0013 : 20 relationships (see list)
    c0013 ..> c0014 : 4 relationships (see list)
    c0013 ..> c0016 : pi_home() calls saved_pi_home()
    c0013 ..> c0018 : _install_resources() calls bundled_files()
    c0013 ..> c0020 : selected_launch() calls selected_skill_files()
    c0013 ..> c0023 : 2 relationships (see list)
    c0013 ..> c0037 : choose_pi_home() calls confirm()
    c0013 ..> c0039 : _protect_runtime() calls write()
    c0013 ..> c0041 : require_pi_home() calls quote()
    c0013 ..> c0070 : validate_setup() calls missing_tools()
    c0013 ..> c0084 : list_models() calls role_environment()
    c0013 ..> c0089 : 7 relationships (see list)
    c0013 ..> c0099 : 13 relationships (see list)
    c0013 ..> c0100 : require_pi_home() calls executable_path()
    c0013 ..> c0102 : 10 relationships (see list)
    c0013 ..> c0104 : list_models() calls run_owned()
    c0014 ..> c0013 : prepare() calls prepare()
    c0014 ..> c0014 : 3 relationships (see list)
    c0014 ..> c0015 : prepare() calls selected_resources()
    c0014 ..> c0021 : __init__() constructs WorkerProfiles
    c0014 ..> c0099 : 4 relationships (see list)
    c0014 ..> c0102 : 5 relationships (see list)
    c0016 ..> c0099 : saved_pi_home() constructs FactoryError
    c0016 ..> c0102 : saved_pi_home() calls read_generated_json()
    c0018 ..> c0017 : 4 relationships (see list)
    c0018 ..> c0018 : 4 relationships (see list)
    c0018 ..> c0039 : 2 relationships (see list)
    c0018 ..> c0099 : 2 relationships (see list)
    c0018 ..> c0102 : plan_update() calls check_real_path()
    c0019 ..> c0016 : unready() calls saved_pi_home()
    c0019 ..> c0019 : unready() calls ready()
    c0019 ..> c0100 : 2 relationships (see list)
    c0019 ..> c0101 : 6 relationships (see list)
    c0019 ..> c0104 : ready() calls run_owned()
    c0020 ..> c0000 : _add_skill_file() calls close()
    c0020 ..> c0020 : 3 relationships (see list)
    c0020 ..> c0099 : 3 relationships (see list)
    c0021 ..> c0023 : type in prepare
    c0021 ..> c0044 : prepare() calls update()
    c0021 ..> c0102 : 3 relationships (see list)
    c0022 ..> c0105 : __post_init__() calls positive_duration()
    c0024 ..> c0023 : 3 relationships (see list)
    c0024 ..> c0024 : 4 relationships (see list)
    c0024 ..> c0099 : 5 relationships (see list)
    c0024 ..> c0105 : 4 relationships (see list)
    c0025 ..> c0023 : type in prepare_roles
    c0025 ..> c0089 : 4 relationships (see list)
    c0028 ..> c0094 : 2 relationships (see list)
    c0028 ..> c0097 : type in __init__
    c0030 ..> c0007 : 2 relationships (see list)
    c0030 ..> c0009 : build_tools() constructs AgentShellRuntimeInstall
    c0030 ..> c0010 : build_watcher() constructs AgentShellTerminal
    c0030 ..> c0013 : 6 relationships (see list)
    c0030 ..> c0019 : build_tools() constructs PiInstall
    c0030 ..> c0028 : 2 relationships (see list)
    c0030 ..> c0030 : 13 relationships (see list)
    c0030 ..> c0031 : 10 relationships (see list)
    c0030 ..> c0037 : build_watcher() constructs FileCleanupReceipts
    c0030 ..> c0040 : 2 relationships (see list)
    c0030 ..> c0042 : build_start_foreman() constructs WorkspaceWatchLease
    c0030 ..> c0043 : build_watcher() constructs ObservedTerminal
    c0030 ..> c0046 : 3 relationships (see list)
    c0030 ..> c0062 : build_watcher() constructs CleanupCompleted
    c0030 ..> c0069 : 2 relationships (see list)
    c0030 ..> c0070 : build_team() calls missing_tools()
    c0030 ..> c0071 : build_watcher() constructs ScaffoldIssue
    c0030 ..> c0073 : 2 relationships (see list)
    c0030 ..> c0075 : 2 relationships (see list)
    c0030 ..> c0078 : 2 relationships (see list)
    c0030 ..> c0079 : 2 relationships (see list)
    c0030 ..> c0084 : prepare_foreman_launch() calls role_environment()
    c0030 ..> c0085 : build_tools() constructs ForgetfulInstall
    c0030 ..> c0086 : build_watcher() constructs ForgetfulPlanStore
    c0030 ..> c0088 : build_initialiser() constructs ForgetfulSetup
    c0030 ..> c0089 : type in build_tools
    c0030 ..> c0094 : 2 relationships (see list)
    c0030 ..> c0095 : build_tools() constructs TmuxInstall
    c0030 ..> c0099 : 3 relationships (see list)
    c0030 ..> c0108 : 3 relationships (see list)
    c0030 ..> c0112 : type in select_ticketing
    c0030 ..> c0113 : 2 relationships (see list)
    c0030 ..> c0115 : build_watcher() constructs GitWorktrees
    c0031 --> c0022 : field agentshell
    c0031 ..> c0105 : __post_init__() calls positive_duration()
    c0032 --> c0046 : field config
    c0032 --> c0089 : field connection
    c0033 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0033 ..> c0005 : 2 relationships (see list)
    c0033 ..> c0007 : _watch_status() calls report()
    c0033 ..> c0008 : 7 relationships (see list)
    c0033 ..> c0013 : 11 relationships (see list)
    c0033 ..> c0023 : 7 relationships (see list)
    c0033 ..> c0024 : _start_initial_setup() calls validate_initial_agents()
    c0033 ..> c0030 : 7 relationships (see list)
    c0033 ..> c0031 : 10 relationships (see list)
    c0033 ..> c0032 : 3 relationships (see list)
    c0033 ..> c0033 : 54 relationships (see list)
    c0033 ..> c0034 : _select_numbered() calls parse_numbered_selection()
    c0033 ..> c0035 : main() calls update_resources()
    c0033 ..> c0036 : _watch_locked() calls load_configuration()
    c0033 ..> c0037 : _initialise_locked() calls load()
    c0033 ..> c0039 : 2 relationships (see list)
    c0033 ..> c0041 : 5 relationships (see list)
    c0033 ..> c0042 : 4 relationships (see list)
    c0033 ..> c0044 : _prompt_workers() calls update()
    c0033 ..> c0045 : _watch_locked() calls observe_plain_watch()
    c0033 ..> c0046 : 4 relationships (see list)
    c0033 ..> c0047 : _connection() calls validate()
    c0033 ..> c0067 : 2 relationships (see list)
    c0033 ..> c0069 : 17 relationships (see list)
    c0033 ..> c0082 : _complete_setup() calls uses_browser_login()
    c0033 ..> c0083 : 2 relationships (see list)
    c0033 ..> c0089 : 7 relationships (see list)
    c0033 ..> c0099 : 19 relationships (see list)
    c0033 ..> c0102 : _discover_worker_models() calls check_real_path()
    c0033 ..> c0107 : _watch_locked() calls watch_stop_scope()
    c0034 ..> c0099 : parse_numbered_selection() constructs FactoryError
    c0035 ..> c0002 : update_resources() calls ready()
    c0035 ..> c0008 : update_resources() calls read_state()
    c0035 ..> c0009 : 2 relationships (see list)
    c0035 ..> c0013 : update_resources() calls validate_bundled_resources()
    c0035 ..> c0018 : 2 relationships (see list)
    c0035 ..> c0030 : update_resources() calls build_team()
    c0035 ..> c0031 : type in update_resources
    c0035 ..> c0035 : update_resources() calls _report()
    c0035 ..> c0042 : 2 relationships (see list)
    c0035 ..> c0099 : 2 relationships (see list)
    c0036 ..> c0037 : load_configuration() calls load()
    c0036 ..> c0040 : load_configuration() constructs TomlConfigurationStore
    c0036 ..> c0046 : type in load_configuration
    c0036 ..> c0099 : load_configuration() constructs FactoryError
    c0037 ..> c0000 : _load() calls close()
    c0037 ..> c0037 : 2 relationships (see list)
    c0037 ..> c0038 : _load() calls _resource()
    c0037 ..> c0039 : _load() calls read()
    c0037 ..> c0058 : 3 relationships (see list)
    c0037 ..> c0099 : 2 relationships (see list)
    c0037 ..> c0102 : 2 relationships (see list)
    c0037 ..> c0107 : confirm() calls check_watch_stop()
    c0038 ..> c0058 : 2 relationships (see list)
    c0039 ..> c0102 : 2 relationships (see list)
    c0040 ..> c0000 : 2 relationships (see list)
    c0040 ..> c0037 : load() calls load()
    c0040 ..> c0039 : save() calls write()
    c0040 ..> c0041 : save() calls quote()
    c0040 ..> c0046 : 2 relationships (see list)
    c0040 ..> c0047 : load() calls from_mapping()
    c0040 ..> c0099 : 2 relationships (see list)
    c0042 ..> c0000 : _hold_directory() calls close()
    c0042 ..> c0042 : hold() calls _hold_directory()
    c0042 ..> c0099 : _hold_directory() constructs FactoryError
    c0043 ..> c0000 : 5 relationships (see list)
    c0043 ..> c0024 : __init__() calls unknown_status()
    c0043 ..> c0026 : type in __init__
    c0043 ..> c0044 : 3 relationships (see list)
    c0044 ..> c0043 : 2 relationships (see list)
    c0044 ..> c0044 : 9 relationships (see list)
    c0044 ..> c0045 : 6 relationships (see list)
    c0044 ..> c0099 : __enter__() constructs FactoryError
    c0044 ..> c0102 : 3 relationships (see list)
    c0045 ..> c0024 : plain_watch_status() calls unknown_status()
    c0045 ..> c0039 : _read_discovery() calls read()
    c0045 ..> c0044 : 4 relationships (see list)
    c0045 ..> c0045 : 7 relationships (see list)
    c0045 ..> c0102 : _read_discovery() calls check_real_path()
    c0046 --> c0048 : field repository
    c0046 --> c0089 : field forgetful
    c0047 ..> c0046 : 3 relationships (see list)
    c0047 ..> c0047 : from_mapping() calls validate()
    c0047 ..> c0048 : from_mapping() constructs RepositoryReference
    c0047 ..> c0089 : validate() calls validate()
    c0047 ..> c0090 : from_mapping() calls connection_from_mapping()
    c0047 ..> c0099 : 2 relationships (see list)
    c0047 ..> c0105 : 2 relationships (see list)
    c0047 ..> c0111 : from_mapping() constructs TicketSource
    c0048 --> c0111 : field work_source
    c0049 --|> c0051 : inherits
    c0050 --|> c0051 : inherits
    c0051 --|> c0099 : inherits
    c0052 --|> c0051 : inherits
    c0053 --|> c0051 : inherits
    c0054 ..> c0000 : 2 relationships (see list)
    c0054 ..> c0055 : send() calls _cleanup_recovery()
    c0054 ..> c0099 : type in send
    c0057 ..> c0058 : 2 relationships (see list)
    c0059 ..> c0046 : 2 relationships (see list)
    c0062 ..> c0000 : 5 relationships (see list)
    c0062 ..> c0007 : _dispose() calls report()
    c0062 ..> c0037 : 2 relationships (see list)
    c0062 ..> c0044 : 4 relationships (see list)
    c0062 ..> c0051 : 7 relationships (see list)
    c0062 ..> c0054 : 10 relationships (see list)
    c0062 ..> c0057 : type in __init__
    c0062 --> c0058 : field confirmed
    c0062 ..> c0058 : 3 relationships (see list)
    c0062 ..> c0062 : 27 relationships (see list)
    c0062 ..> c0063 : 6 relationships (see list)
    c0062 ..> c0064 : 6 relationships (see list)
    c0062 ..> c0068 : 9 relationships (see list)
    c0062 ..> c0086 : 7 relationships (see list)
    c0062 ..> c0099 : type in _read_problem
    c0062 ..> c0108 : _in_scope() calls is_key()
    c0062 ..> c0112 : type in __init__
    c0062 ..> c0115 : 4 relationships (see list)
    c0062 ..> c0120 : type in __init__
    c0066 ..> c0065 : validate_cleanup_marker() constructs CleanupMarkerError
    c0066 ..> c0079 : validate_cleanup_marker() calls is_change_request()
    c0066 ..> c0080 : type in validate_cleanup_marker
    c0066 ..> c0081 : type in validate_cleanup_marker
    c0067 ..> c0039 : 3 relationships (see list)
    c0067 ..> c0046 : type in agree_definition_of_done
    c0067 ..> c0056 : type in agree_definition_of_done
    c0067 ..> c0067 : agree_definition_of_done() calls _deployment_agreement()
    c0067 ..> c0099 : 2 relationships (see list)
    c0068 ..> c0046 : type in __init__
    c0068 ..> c0048 : 3 relationships (see list)
    c0068 ..> c0050 : 2 relationships (see list)
    c0068 ..> c0051 : 5 relationships (see list)
    c0068 ..> c0068 : 2 relationships (see list)
    c0068 ..> c0079 : check_source() calls repository()
    c0068 ..> c0080 : type in check_source
    c0068 ..> c0081 : type in __init__
    c0068 ..> c0086 : ownership() calls tasks()
    c0068 ..> c0091 : type in __init__
    c0068 ..> c0108 : snapshot() calls is_key()
    c0068 ..> c0110 : 2 relationships (see list)
    c0068 ..> c0111 : snapshot() constructs TicketSource
    c0068 ..> c0112 : type in __init__
    c0068 ..> c0113 : check_repository() calls origin()
    c0068 ..> c0117 : type in __init__
    c0069 ..> c0005 : initialise() calls save()
    c0069 ..> c0009 : prepare_foreman() calls install()
    c0069 ..> c0013 : prepare_foreman() calls prepare()
    c0069 ..> c0025 : type in __init__
    c0069 ..> c0037 : 2 relationships (see list)
    c0069 ..> c0046 : 6 relationships (see list)
    c0069 ..> c0047 : 3 relationships (see list)
    c0069 ..> c0048 : 2 relationships (see list)
    c0069 ..> c0059 : type in __init__
    c0069 ..> c0060 : type in __init__
    c0069 ..> c0069 : 3 relationships (see list)
    c0069 ..> c0070 : 2 relationships (see list)
    c0069 ..> c0071 : check_foreman() calls check()
    c0069 ..> c0079 : 2 relationships (see list)
    c0069 ..> c0081 : type in __init__
    c0069 ..> c0083 : check_foreman() calls login()
    c0069 ..> c0089 : 2 relationships (see list)
    c0069 ..> c0093 : type in __init__
    c0069 ..> c0099 : 5 relationships (see list)
    c0069 ..> c0108 : 4 relationships (see list)
    c0069 ..> c0109 : 2 relationships (see list)
    c0069 ..> c0111 : 3 relationships (see list)
    c0069 ..> c0112 : type in __init__
    c0069 ..> c0113 : 3 relationships (see list)
    c0069 ..> c0117 : type in __init__
    c0070 ..> c0009 : 3 relationships (see list)
    c0070 ..> c0060 : 2 relationships (see list)
    c0071 ..> c0044 : recover() calls snapshot()
    c0071 ..> c0046 : type in __init__
    c0071 ..> c0048 : 3 relationships (see list)
    c0071 ..> c0049 : preflight() constructs IntakeProblem
    c0071 ..> c0051 : 8 relationships (see list)
    c0071 ..> c0052 : 5 relationships (see list)
    c0071 ..> c0053 : 5 relationships (see list)
    c0071 ..> c0066 : _ensure_mapping() calls validate_cleanup_marker()
    c0071 ..> c0068 : 11 relationships (see list)
    c0071 ..> c0069 : preflight() calls inspect()
    c0071 ..> c0071 : 22 relationships (see list)
    c0071 ..> c0072 : _initial_mappings() calls worktree_name()
    c0071 ..> c0081 : type in __init__
    c0071 ..> c0083 : check() calls check()
    c0071 ..> c0086 : 12 relationships (see list)
    c0071 ..> c0091 : type in __init__
    c0071 ..> c0099 : _is_unfinished_factory_plan() constructs FactoryError
    c0071 ..> c0110 : 8 relationships (see list)
    c0071 ..> c0111 : type in _repository
    c0071 ..> c0112 : type in __init__
    c0071 ..> c0115 : 3 relationships (see list)
    c0071 ..> c0117 : type in __init__
    c0071 ..> c0120 : type in __init__
    c0072 ..> c0110 : type in worktree_name
    c0073 ..> c0000 : run() calls start()
    c0073 ..> c0007 : 2 relationships (see list)
    c0073 ..> c0013 : run() calls prepare()
    c0073 ..> c0027 : type in __init__
    c0073 ..> c0029 : type in __init__
    c0073 ..> c0042 : run() calls hold()
    c0073 ..> c0061 : type in __init__
    c0073 ..> c0099 : run() constructs FactoryError
    c0074 --> c0110 : field issue
    c0075 ..> c0000 : 15 relationships (see list)
    c0075 ..> c0007 : 5 relationships (see list)
    c0075 ..> c0013 : _process_issue() calls prepare()
    c0075 ..> c0026 : type in __init__
    c0075 ..> c0046 : 4 relationships (see list)
    c0075 ..> c0048 : 5 relationships (see list)
    c0075 ..> c0050 : 2 relationships (see list)
    c0075 ..> c0051 : 3 relationships (see list)
    c0075 ..> c0052 : 2 relationships (see list)
    c0075 ..> c0054 : 28 relationships (see list)
    c0075 ..> c0062 : 2 relationships (see list)
    c0075 ..> c0068 : _check_pending_repositories() calls check_repository()
    c0075 ..> c0071 : 6 relationships (see list)
    c0075 ..> c0074 : 13 relationships (see list)
    c0075 ..> c0075 : 35 relationships (see list)
    c0075 ..> c0076 : 19 relationships (see list)
    c0075 ..> c0077 : 2 relationships (see list)
    c0075 ..> c0099 : _read_issues() constructs FactoryError
    c0075 ..> c0107 : 3 relationships (see list)
    c0075 ..> c0108 : _read_issues() calls list_open()
    c0075 ..> c0110 : 13 relationships (see list)
    c0075 ..> c0111 : 7 relationships (see list)
    c0075 ..> c0112 : type in __init__
    c0076 --> c0048 : field pending_repositories
    c0076 --> c0074 : 2 relationships (see list)
    c0076 --> c0110 : field pending_lookup
    c0076 --> c0111 : field baselined
    c0078 ..> c0013 : _setup() calls validate_completion()
    c0078 ..> c0024 : _without_live_plain() calls unknown_status()
    c0078 ..> c0025 : type in __init__
    c0078 ..> c0027 : type in __init__
    c0078 ..> c0037 : _setup() calls load()
    c0078 ..> c0059 : type in __init__
    c0078 ..> c0078 : 3 relationships (see list)
    c0079 ..> c0080 : 3 relationships (see list)
    c0079 ..> c0099 : repository() constructs FactoryError
    c0081 ..> c0080 : 2 relationships (see list)
    c0082 ..> c0008 : uses_browser_login() calls request()
    c0082 ..> c0039 : uses_browser_login() calls read()
    c0082 ..> c0089 : type in uses_browser_login
    c0083 ..> c0083 : 7 relationships (see list)
    c0083 ..> c0084 : 2 relationships (see list)
    c0083 ..> c0089 : 7 relationships (see list)
    c0083 ..> c0099 : 5 relationships (see list)
    c0083 ..> c0104 : 2 relationships (see list)
    c0083 ..> c0107 : command() calls check_watch_stop()
    c0084 ..> c0044 : role_environment() calls update()
    c0084 ..> c0089 : type in role_environment
    c0084 ..> c0100 : role_environment() calls executable_path()
    c0085 ..> c0085 : 6 relationships (see list)
    c0085 ..> c0089 : type in __init__
    c0085 ..> c0099 : _python() constructs FactoryError
    c0085 ..> c0100 : _selected() calls executable_path()
    c0085 ..> c0101 : 7 relationships (see list)
    c0085 ..> c0104 : _python() calls run_owned()
    c0086 ..> c0071 : check() calls check()
    c0086 ..> c0083 : 2 relationships (see list)
    c0086 ..> c0086 : 12 relationships (see list)
    c0086 ..> c0087 : 3 relationships (see list)
    c0086 ..> c0089 : type in __init__
    c0086 ..> c0092 : 4 relationships (see list)
    c0088 ..> c0071 : check() calls check()
    c0088 ..> c0082 : uses_browser_login() calls uses_browser_login()
    c0088 ..> c0083 : 5 relationships (see list)
    c0088 ..> c0088 : 4 relationships (see list)
    c0088 ..> c0089 : 6 relationships (see list)
    c0089 ..> c0089 : validate() calls _validate_server()
    c0089 ..> c0090 : _validate_server() calls loopback_host()
    c0089 ..> c0099 : 2 relationships (see list)
    c0089 ..> c0105 : 2 relationships (see list)
    c0090 ..> c0089 : 3 relationships (see list)
    c0090 ..> c0099 : connection_from_mapping() constructs FactoryError
    c0092 --|> c0099 : inherits
    c0093 ..> c0089 : 6 relationships (see list)
    c0094 ..> c0005 : enter() calls run()
    c0094 ..> c0099 : enter() constructs FactoryError
    c0095 ..> c0096 : 2 relationships (see list)
    c0095 ..> c0099 : install() constructs FactoryError
    c0095 ..> c0100 : absent() calls executable_path()
    c0095 ..> c0101 : 2 relationships (see list)
    c0098 ..> c0005 : run_command() calls run()
    c0098 ..> c0099 : run_command() constructs FactoryError
    c0098 ..> c0107 : run_command() calls check_watch_stop()
    c0101 ..> c0039 : install_locks() calls read()
    c0101 ..> c0099 : 6 relationships (see list)
    c0101 ..> c0101 : 4 relationships (see list)
    c0101 ..> c0102 : install_locks() calls write_new()
    c0101 ..> c0104 : 3 relationships (see list)
    c0102 ..> c0000 : 2 relationships (see list)
    c0102 ..> c0037 : read_generated_json() calls load()
    c0102 ..> c0039 : 2 relationships (see list)
    c0102 ..> c0099 : 6 relationships (see list)
    c0102 ..> c0102 : 9 relationships (see list)
    c0104 ..> c0000 : 2 relationships (see list)
    c0104 ..> c0099 : run_owned() constructs FactoryError
    c0104 ..> c0104 : 2 relationships (see list)
    c0104 ..> c0107 : run_owned() calls check_watch_stop()
    c0105 ..> c0099 : nonblank() constructs FactoryError
    c0107 ..> c0106 : watch_stop_scope() constructs WatchStop
    c0108 ..> c0098 : 2 relationships (see list)
    c0108 ..> c0099 : 9 relationships (see list)
    c0108 ..> c0108 : 9 relationships (see list)
    c0108 ..> c0109 : 3 relationships (see list)
    c0108 ..> c0110 : 3 relationships (see list)
    c0108 ..> c0111 : 9 relationships (see list)
    c0110 --> c0111 : field source
    c0112 ..> c0109 : 2 relationships (see list)
    c0112 ..> c0110 : type in list_open
    c0112 ..> c0111 : 5 relationships (see list)
    c0113 ..> c0098 : origin() calls run_command()
    c0113 ..> c0099 : origin() constructs FactoryError
    c0113 ..> c0114 : origin() calls _resolve_repository()
    c0114 ..> c0099 : _resolve_repository() constructs FactoryError
    c0115 ..> c0039 : ensure() calls write()
    c0115 ..> c0041 : _network_git() calls quote()
    c0115 ..> c0054 : begin_cleanup_cycle() calls clear()
    c0115 ..> c0098 : 4 relationships (see list)
    c0115 --> c0099 : field cleanup_defaults
    c0115 ..> c0099 : ensure() constructs FactoryError
    c0115 ..> c0107 : ensure() calls check_watch_stop()
    c0115 ..> c0115 : 35 relationships (see list)
    c0115 ..> c0116 : _repository_entries() calls _worktree_entries()
    c0115 ..> c0118 : 14 relationships (see list)
    c0115 ..> c0119 : 6 relationships (see list)
    c0118 ..> c0000 : __init__() calls __init__()
    c0118 --|> c0099 : inherits
    c0119 --|> c0099 : inherits
```

## Source index

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/agents/adapters/agentshell/borrowed_terminal.py`:10
- c0001: `SessionState` — `src/forgetful_factory/agents/adapters/agentshell/controller.py`:116
- c0002: `src/forgetful_factory/agents/adapters/agentshell/controller.py` —
  `src/forgetful_factory/agents/adapters/agentshell/controller.py`:1
- c0003: `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py` —
  `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py`:1
- c0004: `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py`:1
- c0005: `ForemanOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner.py`:104
- c0006: `src/forgetful_factory/agents/adapters/agentshell/owner.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner.py`:1
- c0007: `AgentShellOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:180
- c0008: `src/forgetful_factory/agents/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:1
- c0009: `AgentShellRuntimeInstall` —
  `src/forgetful_factory/agents/adapters/agentshell/runtime_install.py`:24
- c0010: `AgentShellTerminal` — `src/forgetful_factory/agents/adapters/agentshell/terminal.py`:17
- c0011: `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py` —
  `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py`:1
- c0012: `src/forgetful_factory/agents/adapters/pi/agent_definitions.py` —
  `src/forgetful_factory/agents/adapters/pi/agent_definitions.py`:1
- c0013: `PiAgentTeam` — `src/forgetful_factory/agents/adapters/pi/agent_team.py`:46
- c0014: `CoordinatorProfiles` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:29
- c0015: `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:1
- c0016: `src/forgetful_factory/agents/adapters/pi/native_home.py` —
  `src/forgetful_factory/agents/adapters/pi/native_home.py`:1
- c0017: `ResourceUpdate` — `src/forgetful_factory/agents/adapters/pi/role_resources.py`:39
- c0018: `src/forgetful_factory/agents/adapters/pi/role_resources.py` —
  `src/forgetful_factory/agents/adapters/pi/role_resources.py`:1
- c0019: `PiInstall` — `src/forgetful_factory/agents/adapters/pi/runtime_install.py`:22
- c0020: `src/forgetful_factory/agents/adapters/pi/selected_skills.py` —
  `src/forgetful_factory/agents/adapters/pi/selected_skills.py`:1
- c0021: `WorkerProfiles` — `src/forgetful_factory/agents/adapters/pi/worker_profiles.py`:16
- c0022: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/agents/model.py`:131
- c0023: `InitialAgentChoices` — `src/forgetful_factory/agents/model.py`:9
- c0024: `src/forgetful_factory/agents/model.py` — `src/forgetful_factory/agents/model.py`:1
- c0025: `AgentTeam` — `src/forgetful_factory/agents/ports.py`:37
- c0026: `ForemanTerminal` — `src/forgetful_factory/agents/ports.py`:9
- c0027: `PersistentForeman` — `src/forgetful_factory/agents/ports.py`:21
- c0028: `TerminalChannel` — `src/forgetful_factory/channels/adapters/terminal.py`:8
- c0029: `Channel` — `src/forgetful_factory/channels/ports.py`:4
- c0030: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0031: `DeadlinePolicy` — `src/forgetful_factory/cli/deadlines.py`:9
- c0032: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:670
- c0033: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0034: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0035: `src/forgetful_factory/cli/resource_update.py` —
  `src/forgetful_factory/cli/resource_update.py`:1
- c0036: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0037: `FileCleanupReceipts` — `src/forgetful_factory/factory/adapters/cleanup_receipts.py`:40
- c0038: `src/forgetful_factory/factory/adapters/cleanup_receipts.py` —
  `src/forgetful_factory/factory/adapters/cleanup_receipts.py`:1
- c0039: `MarkdownAgreement` — `src/forgetful_factory/factory/adapters/markdown_agreement.py`:7
- c0040: `TomlConfigurationStore` —
  `src/forgetful_factory/factory/adapters/toml_configuration.py`:17
- c0041: `src/forgetful_factory/factory/adapters/toml_configuration.py` —
  `src/forgetful_factory/factory/adapters/toml_configuration.py`:1
- c0042: `WorkspaceWatchLease` — `src/forgetful_factory/factory/adapters/watch_lease.py`:10
- c0043: `ObservedTerminal` — `src/forgetful_factory/factory/adapters/watch_status.py`:247
- c0044: `PlainWatchObservation` — `src/forgetful_factory/factory/adapters/watch_status.py`:124
- c0045: `src/forgetful_factory/factory/adapters/watch_status.py` —
  `src/forgetful_factory/factory/adapters/watch_status.py`:1
- c0046: `FactoryConfiguration` — `src/forgetful_factory/factory/model/configuration.py`:11
- c0047: `src/forgetful_factory/factory/model/configuration.py` —
  `src/forgetful_factory/factory/model/configuration.py`:1
- c0048: `RepositoryReference` — `src/forgetful_factory/factory/model/repositories.py`:7
- c0049: `IntakeProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:143
- c0050: `RepositoryProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:139
- c0051: `ScaffoldProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:119
- c0052: `ScaffoldReadProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:135
- c0053: `UncertainScaffold` — `src/forgetful_factory/factory/model/watcher_problems.py`:147
- c0054: `WatcherAlerts` — `src/forgetful_factory/factory/model/watcher_problems.py`:151
- c0055: `src/forgetful_factory/factory/model/watcher_problems.py` —
  `src/forgetful_factory/factory/model/watcher_problems.py`:1
- c0056: `AgreementStore` — `src/forgetful_factory/factory/ports.py`:45
- c0057: `CleanupReceipts` — `src/forgetful_factory/factory/ports.py`:37
- c0058: `CleanupSet` — `src/forgetful_factory/factory/ports.py`:20
- c0059: `ConfigurationStore` — `src/forgetful_factory/factory/ports.py`:9
- c0060: `ToolInstaller` — `src/forgetful_factory/factory/ports.py`:61
- c0061: `WatchLease` — `src/forgetful_factory/factory/ports.py`:15
- c0062: `CleanupCompleted` — `src/forgetful_factory/factory/services/cleanup_completed.py`:37
- c0063: `CompletedWork` — `src/forgetful_factory/factory/services/cleanup_completed.py`:22
- c0064: `src/forgetful_factory/factory/services/cleanup_completed.py` —
  `src/forgetful_factory/factory/services/cleanup_completed.py`:1
- c0065: `CleanupMarkerError` — `src/forgetful_factory/factory/services/cleanup_marker.py`:11
- c0066: `src/forgetful_factory/factory/services/cleanup_marker.py` —
  `src/forgetful_factory/factory/services/cleanup_marker.py`:1
- c0067: `src/forgetful_factory/factory/services/definition_of_done.py` —
  `src/forgetful_factory/factory/services/definition_of_done.py`:1
- c0068: `FactoryRecords` — `src/forgetful_factory/factory/services/factory_records.py`:17
- c0069: `InitialiseFactory` — `src/forgetful_factory/factory/services/initialise_factory.py`:37
- c0070: `src/forgetful_factory/factory/services/initialise_factory.py` —
  `src/forgetful_factory/factory/services/initialise_factory.py`:1
- c0071: `ScaffoldIssue` — `src/forgetful_factory/factory/services/scaffold_issue.py`:38
- c0072: `src/forgetful_factory/factory/services/scaffold_issue.py` —
  `src/forgetful_factory/factory/services/scaffold_issue.py`:1
- c0073: `StartForeman` — `src/forgetful_factory/factory/services/start_foreman.py`:14
- c0074: `BlockedWork` — `src/forgetful_factory/factory/services/watch_factory.py`:27
- c0075: `WatchFactory` — `src/forgetful_factory/factory/services/watch_factory.py`:59
- c0076: `_WatchState` — `src/forgetful_factory/factory/services/watch_factory.py`:38
- c0077: `_WorkAction` — `src/forgetful_factory/factory/services/watch_factory.py`:52
- c0078: `WatchStatus` — `src/forgetful_factory/factory/services/watch_status.py`:10
- c0079: `GitHubForge` — `src/forgetful_factory/forge/adapters/github.py`:8
- c0080: `RepositoryRef` — `src/forgetful_factory/forge/model.py`:6
- c0081: `Forge` — `src/forgetful_factory/forge/ports.py`:6
- c0082: `src/forgetful_factory/planning/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/planning/adapters/forgetful/authentication.py`:1
- c0083: `AgentForgetfulConnection` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:55
- c0084: `src/forgetful_factory/planning/adapters/forgetful/connection.py` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:1
- c0085: `ForgetfulInstall` — `src/forgetful_factory/planning/adapters/forgetful/install.py`:26
- c0086: `ForgetfulPlanStore` — `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:13
- c0087: `src/forgetful_factory/planning/adapters/forgetful/plan_store.py` —
  `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:1
- c0088: `ForgetfulSetup` — `src/forgetful_factory/planning/adapters/forgetful/setup.py`:9
- c0089: `ForgetfulConnection` — `src/forgetful_factory/planning/model.py`:13
- c0090: `src/forgetful_factory/planning/model.py` — `src/forgetful_factory/planning/model.py`:1
- c0091: `PlanStore` — `src/forgetful_factory/planning/ports.py`:11
- c0092: `PlanningReadError` — `src/forgetful_factory/planning/ports.py`:7
- c0093: `PlanningSetup` — `src/forgetful_factory/planning/ports.py`:38
- c0094: `TmuxHost` — `src/forgetful_factory/runtime/adapters/tmux.py`:28
- c0095: `TmuxInstall` — `src/forgetful_factory/runtime/adapters/tmux.py`:54
- c0096: `src/forgetful_factory/runtime/adapters/tmux.py` —
  `src/forgetful_factory/runtime/adapters/tmux.py`:1
- c0097: `SessionHost` — `src/forgetful_factory/runtime/ports.py`:4
- c0098: `src/forgetful_factory/shared/command.py` — `src/forgetful_factory/shared/command.py`:1
- c0099: `FactoryError` — `src/forgetful_factory/shared/errors.py`:1
- c0100: `src/forgetful_factory/shared/executables.py` —
  `src/forgetful_factory/shared/executables.py`:1
- c0101: `src/forgetful_factory/shared/installation.py` —
  `src/forgetful_factory/shared/installation.py`:1
- c0102: `src/forgetful_factory/shared/resource_files.py` —
  `src/forgetful_factory/shared/resource_files.py`:1
- c0103: `src/forgetful_factory/shared/resources.py` — `src/forgetful_factory/shared/resources.py`:1
- c0104: `src/forgetful_factory/shared/sensitive_command.py` —
  `src/forgetful_factory/shared/sensitive_command.py`:1
- c0105: `src/forgetful_factory/shared/validation.py` —
  `src/forgetful_factory/shared/validation.py`:1
- c0106: `WatchStop` — `src/forgetful_factory/shared/watch_stop.py`:8
- c0107: `src/forgetful_factory/shared/watch_stop.py` —
  `src/forgetful_factory/shared/watch_stop.py`:1
- c0108: `GitHubTicketing` — `src/forgetful_factory/ticketing/adapters/github.py`:15
- c0109: `Label` — `src/forgetful_factory/ticketing/model.py`:17
- c0110: `Ticket` — `src/forgetful_factory/ticketing/model.py`:22
- c0111: `TicketSource` — `src/forgetful_factory/ticketing/model.py`:6
- c0112: `Ticketing` — `src/forgetful_factory/ticketing/ports.py`:6
- c0113: `GitRepositories` — `src/forgetful_factory/workspace/adapters/git/repositories.py`:15
- c0114: `src/forgetful_factory/workspace/adapters/git/repositories.py` —
  `src/forgetful_factory/workspace/adapters/git/repositories.py`:1
- c0115: `GitWorktrees` — `src/forgetful_factory/workspace/adapters/git/worktrees.py`:33
- c0116: `src/forgetful_factory/workspace/adapters/git/worktrees.py` —
  `src/forgetful_factory/workspace/adapters/git/worktrees.py`:1
- c0117: `LocalRepositories` — `src/forgetful_factory/workspace/ports.py`:8
- c0118: `WorktreeProblem` — `src/forgetful_factory/workspace/ports.py`:18
- c0119: `WorktreeReadError` — `src/forgetful_factory/workspace/ports.py`:14
- c0120: `Worktrees` — `src/forgetful_factory/workspace/ports.py`:27

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0010: `close() calls close()`
- c0000 ..> c0099: `_request() constructs FactoryError`
- c0000 ..> c0099: `wait() constructs FactoryError`
- c0000 ..> c0107: `_request() calls check_watch_stop()`
- c0000 ..> c0107: `wait() calls check_watch_stop()`
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
- c0002 ..> c0011: `capture_worker() calls pin_worker()`
- c0002 ..> c0011: `supervise_session() calls retain_identity()`
- c0002 ..> c0086: `control() calls create_task()`
- c0002 ..> c0086: `main() calls create_task()`
- c0002 ..> c0086: `replace_failed_exit_task() calls create_task()`
- c0002 ..> c0086: `supervise_session() calls create_task()`
- c0003 ..> c0099: `runtime_directory() constructs FactoryError`
- c0003 ..> c0102: `runtime_directory() calls check_real_path()`
- c0004 ..> c0013: `main() calls list_models()`
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
- c0005 ..> c0022: `__init__() constructs AgentShellLifecycleDeadlines`
- c0005 ..> c0022: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0005 ..> c0039: `_complete_handover() calls write()`
- c0005 ..> c0039: `_relay_request() calls write()`
- c0005 ..> c0039: `_start_controller() calls write()`
- c0005 ..> c0039: `control() calls write()`
- c0005 ..> c0039: `relay() calls write()`
- c0005 ..> c0039: `run() calls write()`
- c0005 ..> c0041: `_apply_controller_problem() calls quote()`
- c0005 ..> c0086: `_start_controller() calls create_task()`
- c0005 ..> c0086: `start_watcher() calls create_task()`
- c0005 ..> c0099: `_apply_controller_problem() constructs FactoryError`
- c0005 ..> c0099: `_await_readiness() constructs FactoryError`
- c0005 ..> c0099: `_complete_handover() constructs FactoryError`
- c0005 ..> c0099: `_finish_observation() constructs FactoryError`
- c0005 ..> c0099: `_reject_controller_event() constructs FactoryError`
- c0005 ..> c0099: `_relay_request() constructs FactoryError`
- c0005 ..> c0099: `control() constructs FactoryError`
- c0005 ..> c0099: `observe() constructs FactoryError`
- c0005 ..> c0099: `reap_watcher() constructs FactoryError`
- c0005 ..> c0099: `start_watcher() constructs FactoryError`
- c0005 ..> c0102: `save() calls replace_generated_json()`
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
- c0006 ..> c0008: `_prepare_owner_startup() calls read_state()`
- c0006 ..> c0041: `_acquire_owner_lock() calls quote()`
- c0006 ..> c0086: `main() calls create_task()`
- c0006 ..> c0099: `_acquire_owner_lock() constructs FactoryError`
- c0006 ..> c0099: `_prepare_owner_startup() constructs FactoryError`
- c0006 ..> c0099: `_watcher_request() constructs FactoryError`
- c0007 ..> c0008: `report() calls read_state()`
- c0007 ..> c0008: `report() calls request()`
- c0007 ..> c0008: `saved() calls read_state()`
- c0007 ..> c0008: `start() calls start_owner()`
- c0007 ..> c0008: `status() calls request()`
- c0007 ..> c0022: `__init__() constructs AgentShellLifecycleDeadlines`
- c0007 ..> c0022: `type in __init__`
- c0007 ..> c0024: `report() calls unknown_status()`
- c0007 ..> c0041: `report() calls quote()`
- c0007 ..> c0097: `type in __init__`
- c0008 ..> c0000: `start_owner() calls close()`
- c0008 ..> c0000: `start_owner() calls wait()`
- c0008 ..> c0003: `read_state() calls runtime_directory()`
- c0008 ..> c0003: `request() calls runtime_directory()`
- c0008 ..> c0003: `start_owner() calls runtime_directory()`
- c0008 ..> c0005: `start_owner() calls run()`
- c0008 ..> c0008: `request() calls _reply()`
- c0008 ..> c0008: `request() calls read_state()`
- c0008 ..> c0008: `start_owner() calls _reply()`
- c0008 ..> c0022: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0008 ..> c0022: `type in start_owner`
- c0008 ..> c0041: `request() calls quote()`
- c0008 ..> c0094: `start_owner() calls spec()`
- c0008 ..> c0097: `type in start_owner`
- c0008 ..> c0099: `_reply() constructs FactoryError`
- c0008 ..> c0099: `read_state() constructs FactoryError`
- c0008 ..> c0099: `request() constructs FactoryError`
- c0008 ..> c0099: `start_owner() constructs FactoryError`
- c0008 ..> c0102: `read_state() calls read_generated_json()`
- c0009 ..> c0009: `install() calls _inputs()`
- c0009 ..> c0009: `ready() calls _inputs()`
- c0009 ..> c0009: `unready() calls ready()`
- c0009 ..> c0099: `install() constructs FactoryError`
- c0009 ..> c0101: `install() calls check_uv()`
- c0009 ..> c0101: `install() calls no_installer()`
- c0009 ..> c0101: `install() calls run_install()`
- c0009 ..> c0101: `install() calls sync_fingerprint()`
- c0009 ..> c0101: `ready() calls runtime_ready()`
- c0010 ..> c0000: `close() calls close()`
- c0010 ..> c0010: `send() calls _read()`
- c0010 ..> c0010: `send() calls _write()`
- c0010 ..> c0010: `start() calls _read()`
- c0010 ..> c0010: `start() calls _write()`
- c0010 ..> c0010: `wait() calls _read()`
- c0010 ..> c0022: `__init__() constructs AgentShellLifecycleDeadlines`
- c0010 ..> c0022: `type in __init__`
- c0010 ..> c0028: `startup_hint() calls how_to_reach()`
- c0010 ..> c0029: `type in __init__`
- c0010 ..> c0039: `_read() calls read()`
- c0010 ..> c0039: `_write() calls write()`
- c0010 ..> c0094: `start() calls spec()`
- c0010 ..> c0097: `type in __init__`
- c0010 ..> c0099: `_read() constructs FactoryError`
- c0010 ..> c0099: `_write() constructs FactoryError`
- c0010 ..> c0099: `close() constructs FactoryError`
- c0010 ..> c0099: `start() constructs FactoryError`
- c0010 ..> c0107: `_read() calls check_watch_stop()`
- c0010 ..> c0107: `_write() calls check_watch_stop()`
- c0010 ..> c0107: `wait() calls check_watch_stop()`
- c0011 ..> c0000: `pin_worker() calls close()`
- c0012 ..> c0012: `_validate_agent() calls _local_selection()`
- c0012 ..> c0012: `_validate_roster() calls _local_selection()`
- c0012 ..> c0012: `_validate_roster() calls relative_path()`
- c0012 ..> c0012: `foreman_launch() calls read_definition()`
- c0012 ..> c0012: `foreman_launch() calls relative_path()`
- c0012 ..> c0012: `read_definition() calls _validate_agent()`
- c0012 ..> c0012: `read_definition() calls _validate_resources()`
- c0012 ..> c0012: `read_definition() calls _validate_roster()`
- c0012 ..> c0099: `foreman_launch() constructs FactoryError`
- c0012 ..> c0099: `read_definition() constructs FactoryError`
- c0012 ..> c0105: `_local_selection() calls nonblank()`
- c0012 ..> c0105: `_validate_agent() calls nonblank()`
- c0012 ..> c0105: `foreman_launch() calls nonblank()`
- c0012 ..> c0105: `relative_path() calls nonblank()`
- c0013 ..> c0012: `selected_launch() calls foreman_launch()`
- c0013 ..> c0013: `choose_pi_home() calls pi_home()`
- c0013 ..> c0013: `choose_pi_home() calls require_pi_home()`
- c0013 ..> c0013: `list_models() calls pi_home()`
- c0013 ..> c0013: `list_models() calls require_pi_home()`
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
- c0013 ..> c0013: `validate_setup() calls pi_home()`
- c0013 ..> c0013: `validate_setup() calls require_pi_home()`
- c0013 ..> c0013: `validate_setup() calls validate_bundled_resources()`
- c0013 ..> c0013: `validate_setup() calls validate_guidance()`
- c0013 ..> c0013: `validate_worker_models() calls list_models()`
- c0013 ..> c0014: `prepare_roles() calls validate_depth()`
- c0013 ..> c0014: `prepare_roles() constructs CoordinatorProfiles`
- c0013 ..> c0014: `validate_setup() calls validate_depth()`
- c0013 ..> c0014: `validate_setup() constructs CoordinatorProfiles`
- c0013 ..> c0016: `pi_home() calls saved_pi_home()`
- c0013 ..> c0018: `_install_resources() calls bundled_files()`
- c0013 ..> c0020: `selected_launch() calls selected_skill_files()`
- c0013 ..> c0023: `type in prepare_roles`
- c0013 ..> c0023: `type in validate_worker_models`
- c0013 ..> c0037: `choose_pi_home() calls confirm()`
- c0013 ..> c0039: `_protect_runtime() calls write()`
- c0013 ..> c0041: `require_pi_home() calls quote()`
- c0013 ..> c0070: `validate_setup() calls missing_tools()`
- c0013 ..> c0084: `list_models() calls role_environment()`
- c0013 ..> c0089: `type in __init__`
- c0013 ..> c0089: `type in list_models`
- c0013 ..> c0089: `type in prepare_roles`
- c0013 ..> c0089: `type in record_completion`
- c0013 ..> c0089: `type in selected_launch`
- c0013 ..> c0089: `type in validate_setup`
- c0013 ..> c0089: `type in validate_worker_models`
- c0013 ..> c0099: `_install_resources() constructs FactoryError`
- c0013 ..> c0099: `_read_guidance() constructs FactoryError`
- c0013 ..> c0099: `choose_pi_home() constructs FactoryError`
- c0013 ..> c0099: `list_models() constructs FactoryError`
- c0013 ..> c0099: `prepare_roles() constructs FactoryError`
- c0013 ..> c0099: `prepare_setup_guidance() constructs FactoryError`
- c0013 ..> c0099: `require_pi_home() constructs FactoryError`
- c0013 ..> c0099: `selected_launch() constructs FactoryError`
- c0013 ..> c0099: `validate_bundled_resources() constructs FactoryError`
- c0013 ..> c0099: `validate_completion() constructs FactoryError`
- c0013 ..> c0099: `validate_guidance() constructs FactoryError`
- c0013 ..> c0099: `validate_setup() constructs FactoryError`
- c0013 ..> c0099: `validate_worker_models() constructs FactoryError`
- c0013 ..> c0100: `require_pi_home() calls executable_path()`
- c0013 ..> c0102: `_install_resources() calls write_new()`
- c0013 ..> c0102: `_protect_runtime() calls write_new()`
- c0013 ..> c0102: `begin_setup() calls remove_generated()`
- c0013 ..> c0102: `prepare() calls write_new()`
- c0013 ..> c0102: `prepare_roles() calls check_real_path()`
- c0013 ..> c0102: `prepare_setup_guidance() calls write_new()`
- c0013 ..> c0102: `record_completion() calls replace_generated_json()`
- c0013 ..> c0102: `save_pi_choice() calls write_json()`
- c0013 ..> c0102: `validate_bundled_resources() calls check_real_path()`
- c0013 ..> c0102: `validate_completion() calls read_generated_json()`
- c0013 ..> c0104: `list_models() calls run_owned()`
- c0014 ..> c0013: `prepare() calls prepare()`
- c0014 ..> c0014: `prepare() calls _write_agent()`
- c0014 ..> c0014: `prepare() calls _write_foreman_memory()`
- c0014 ..> c0014: `prepare() calls validate_guidance()`
- c0014 ..> c0015: `prepare() calls selected_resources()`
- c0014 ..> c0021: `__init__() constructs WorkerProfiles`
- c0014 ..> c0099: `_write_foreman_memory() constructs FactoryError`
- c0014 ..> c0099: `prepare() constructs FactoryError`
- c0014 ..> c0099: `validate_depth() constructs FactoryError`
- c0014 ..> c0099: `validate_guidance() constructs FactoryError`
- c0014 ..> c0102: `_write_agent() calls write_definition()`
- c0014 ..> c0102: `_write_foreman_memory() calls read_generated_json()`
- c0014 ..> c0102: `_write_foreman_memory() calls write_json()`
- c0014 ..> c0102: `prepare() calls check_skill_file()`
- c0014 ..> c0102: `prepare() calls write_new()`
- c0016 ..> c0099: `saved_pi_home() constructs FactoryError`
- c0016 ..> c0102: `saved_pi_home() calls read_generated_json()`
- c0018 ..> c0017: `plan_update() constructs ResourceUpdate`
- c0018 ..> c0017: `type in _back_up`
- c0018 ..> c0017: `type in apply_update`
- c0018 ..> c0017: `type in plan_update`
- c0018 ..> c0018: `apply_update() calls _back_up()`
- c0018 ..> c0018: `bundled_files() calls _digest()`
- c0018 ..> c0018: `plan_update() calls _digest()`
- c0018 ..> c0018: `plan_update() calls bundled_files()`
- c0018 ..> c0039: `apply_update() calls write()`
- c0018 ..> c0039: `bundled_files() calls read()`
- c0018 ..> c0099: `bundled_files() constructs FactoryError`
- c0018 ..> c0099: `plan_update() constructs FactoryError`
- c0018 ..> c0102: `plan_update() calls check_real_path()`
- c0019 ..> c0016: `unready() calls saved_pi_home()`
- c0019 ..> c0019: `unready() calls ready()`
- c0019 ..> c0100: `absent() calls executable_path()`
- c0019 ..> c0100: `unready() calls executable_path()`
- c0019 ..> c0101: `install() calls install_locks()`
- c0019 ..> c0101: `install() calls no_installer()`
- c0019 ..> c0101: `install() calls require_manager()`
- c0019 ..> c0101: `install() calls run_install()`
- c0019 ..> c0101: `ready() calls install_environment()`
- c0019 ..> c0101: `ready() calls sync_fingerprint()`
- c0019 ..> c0104: `ready() calls run_owned()`
- c0020 ..> c0000: `_add_skill_file() calls close()`
- c0020 ..> c0020: `_walk_skill_directory() calls _add_skill_file()`
- c0020 ..> c0020: `selected_skill_files() calls _add_skill_file()`
- c0020 ..> c0020: `selected_skill_files() calls _walk_skill_directory()`
- c0020 ..> c0099: `_add_skill_file() constructs FactoryError`
- c0020 ..> c0099: `_walk_skill_directory() constructs FactoryError`
- c0020 ..> c0099: `selected_skill_files() constructs FactoryError`
- c0021 ..> c0023: `type in prepare`
- c0021 ..> c0044: `prepare() calls update()`
- c0021 ..> c0102: `prepare() calls check_skill_file()`
- c0021 ..> c0102: `prepare() calls write_definition()`
- c0021 ..> c0102: `prepare() calls write_new()`
- c0022 ..> c0105: `__post_init__() calls positive_duration()`
- c0024 ..> c0023: `type in _validate_foreman_memory`
- c0024 ..> c0023: `type in validate_initial_agents`
- c0024 ..> c0023: `type in validate_workers`
- c0024 ..> c0024: `validate_initial_agents() calls _validate_foreman_memory()`
- c0024 ..> c0024: `validate_initial_agents() calls validate_role_app()`
- c0024 ..> c0024: `validate_initial_agents() calls validate_workers()`
- c0024 ..> c0024: `validate_workers() calls validate_role_app()`
- c0024 ..> c0099: `_validate_foreman_memory() constructs FactoryError`
- c0024 ..> c0099: `skill_paths() constructs FactoryError`
- c0024 ..> c0099: `validate_initial_agents() constructs FactoryError`
- c0024 ..> c0099: `validate_role_app() constructs FactoryError`
- c0024 ..> c0099: `validate_workers() constructs FactoryError`
- c0024 ..> c0105: `_validate_foreman_memory() calls nonblank()`
- c0024 ..> c0105: `skill_paths() calls nonblank()`
- c0024 ..> c0105: `validate_initial_agents() calls nonblank()`
- c0024 ..> c0105: `validate_workers() calls nonblank()`
- c0025 ..> c0023: `type in prepare_roles`
- c0025 ..> c0089: `type in list_models`
- c0025 ..> c0089: `type in prepare_roles`
- c0025 ..> c0089: `type in record_completion`
- c0025 ..> c0089: `type in selected_launch`
- c0028 ..> c0094: `how_to_reach() calls how_to_attach()`
- c0028 ..> c0094: `open() calls enter()`
- c0028 ..> c0097: `type in __init__`
- c0030 ..> c0007: `build_owner() constructs AgentShellOwner`
- c0030 ..> c0007: `type in build_owner`
- c0030 ..> c0009: `build_tools() constructs AgentShellRuntimeInstall`
- c0030 ..> c0010: `build_watcher() constructs AgentShellTerminal`
- c0030 ..> c0013: `build_team() constructs PiAgentTeam`
- c0030 ..> c0013: `build_watcher() calls managed_memory_notice()`
- c0030 ..> c0013: `prepare_foreman_launch() calls pi_home()`
- c0030 ..> c0013: `prepare_foreman_launch() calls selected_launch()`
- c0030 ..> c0013: `prepare_foreman_launch() calls validate_completion()`
- c0030 ..> c0013: `type in build_team`
- c0030 ..> c0019: `build_tools() constructs PiInstall`
- c0030 ..> c0028: `build_channel() constructs TerminalChannel`
- c0030 ..> c0028: `type in build_channel`
- c0030 ..> c0030: `build_channel() calls build_host()`
- c0030 ..> c0030: `build_initialiser() calls build_team()`
- c0030 ..> c0030: `build_owner() calls build_host()`
- c0030 ..> c0030: `build_start_foreman() calls build_channel()`
- c0030 ..> c0030: `build_start_foreman() calls build_owner()`
- c0030 ..> c0030: `build_team() calls build_tools()`
- c0030 ..> c0030: `build_watch_status() calls build_owner()`
- c0030 ..> c0030: `build_watch_status() calls build_team()`
- c0030 ..> c0030: `build_watcher() calls build_channel()`
- c0030 ..> c0030: `build_watcher() calls build_host()`
- c0030 ..> c0030: `build_watcher() calls prepare_foreman_launch()`
- c0030 ..> c0030: `build_watcher() calls select_ticketing()`
- c0030 ..> c0030: `prepare_foreman_launch() calls build_team()`
- c0030 ..> c0031: `build_initialiser() constructs DeadlinePolicy`
- c0030 ..> c0031: `build_owner() constructs DeadlinePolicy`
- c0030 ..> c0031: `build_start_foreman() constructs DeadlinePolicy`
- c0030 ..> c0031: `build_watch_status() constructs DeadlinePolicy`
- c0030 ..> c0031: `build_watcher() constructs DeadlinePolicy`
- c0030 ..> c0031: `type in build_initialiser`
- c0030 ..> c0031: `type in build_owner`
- c0030 ..> c0031: `type in build_start_foreman`
- c0030 ..> c0031: `type in build_watch_status`
- c0030 ..> c0031: `type in build_watcher`
- c0030 ..> c0037: `build_watcher() constructs FileCleanupReceipts`
- c0030 ..> c0040: `build_initialiser() constructs TomlConfigurationStore`
- c0030 ..> c0040: `build_watch_status() constructs TomlConfigurationStore`
- c0030 ..> c0042: `build_start_foreman() constructs WorkspaceWatchLease`
- c0030 ..> c0043: `build_watcher() constructs ObservedTerminal`
- c0030 ..> c0046: `type in build_watcher`
- c0030 ..> c0046: `type in prepare_foreman_launch`
- c0030 ..> c0046: `type in select_ticketing`
- c0030 ..> c0062: `build_watcher() constructs CleanupCompleted`
- c0030 ..> c0069: `build_initialiser() constructs InitialiseFactory`
- c0030 ..> c0069: `type in build_initialiser`
- c0030 ..> c0070: `build_team() calls missing_tools()`
- c0030 ..> c0071: `build_watcher() constructs ScaffoldIssue`
- c0030 ..> c0073: `build_start_foreman() constructs StartForeman`
- c0030 ..> c0073: `type in build_start_foreman`
- c0030 ..> c0075: `build_watcher() constructs WatchFactory`
- c0030 ..> c0075: `type in build_watcher`
- c0030 ..> c0078: `build_watch_status() constructs WatchStatus`
- c0030 ..> c0078: `type in build_watch_status`
- c0030 ..> c0079: `build_initialiser() constructs GitHubForge`
- c0030 ..> c0079: `build_watcher() constructs GitHubForge`
- c0030 ..> c0084: `prepare_foreman_launch() calls role_environment()`
- c0030 ..> c0085: `build_tools() constructs ForgetfulInstall`
- c0030 ..> c0086: `build_watcher() constructs ForgetfulPlanStore`
- c0030 ..> c0088: `build_initialiser() constructs ForgetfulSetup`
- c0030 ..> c0089: `type in build_tools`
- c0030 ..> c0094: `build_host() constructs TmuxHost`
- c0030 ..> c0094: `type in build_host`
- c0030 ..> c0095: `build_tools() constructs TmuxInstall`
- c0030 ..> c0099: `build_watcher() constructs FactoryError`
- c0030 ..> c0099: `prepare_foreman_launch() constructs FactoryError`
- c0030 ..> c0099: `select_ticketing() constructs FactoryError`
- c0030 ..> c0108: `build_initialiser() constructs GitHubTicketing`
- c0030 ..> c0108: `build_watcher() calls check_ready()`
- c0030 ..> c0108: `select_ticketing() calls validate_source()`
- c0030 ..> c0112: `type in select_ticketing`
- c0030 ..> c0113: `build_initialiser() constructs GitRepositories`
- c0030 ..> c0113: `build_watcher() constructs GitRepositories`
- c0030 ..> c0115: `build_watcher() constructs GitWorktrees`
- c0031 --> c0022: `field agentshell`
- c0031 ..> c0105: `__post_init__() calls positive_duration()`
- c0032 --> c0046: `field config`
- c0032 --> c0089: `field connection`
- c0033 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0033 ..> c0005: `_foreman() calls run()`
- c0033 ..> c0005: `_watch_locked() calls run()`
- c0033 ..> c0007: `_watch_status() calls report()`
- c0033 ..> c0008: `_change_managed_watch() calls request()`
- c0033 ..> c0008: `_finish_existing_setup() calls read_state()`
- c0033 ..> c0008: `_initialise() calls request()`
- c0033 ..> c0008: `_initialise_locked() calls read_state()`
- c0033 ..> c0008: `_launch_setup_foreman() calls start_owner()`
- c0033 ..> c0008: `_offer_factory_launch() calls read_state()`
- c0033 ..> c0008: `_watch_locked() calls read_state()`
- c0033 ..> c0013: `_complete_setup() calls managed_memory_notice()`
- c0033 ..> c0013: `_complete_setup() calls record_completion()`
- c0033 ..> c0013: `_discover_worker_models() calls list_models()`
- c0033 ..> c0013: `_finish_existing_setup() calls choose_pi_home()`
- c0033 ..> c0013: `_finish_existing_setup() calls save_pi_choice()`
- c0033 ..> c0013: `_finish_existing_setup() calls selected_launch()`
- c0033 ..> c0013: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0033 ..> c0013: `_select_model() calls list_models()`
- c0033 ..> c0013: `_start_initial_setup() calls begin_setup()`
- c0033 ..> c0013: `_start_initial_setup() calls choose_pi_home()`
- c0033 ..> c0013: `_validate_initial_model() calls prepare_roles()`
- c0033 ..> c0023: `_configure_new_factory() constructs InitialAgentChoices`
- c0033 ..> c0023: `type in _configure_new_factory`
- c0033 ..> c0023: `type in _foreman_memory_choices`
- c0033 ..> c0023: `type in _owner_choices`
- c0033 ..> c0023: `type in _prompt_coordinator_choices`
- c0033 ..> c0023: `type in _validate_initial_model`
- c0033 ..> c0023: `type in _worker_choices`
- c0033 ..> c0024: `_start_initial_setup() calls validate_initial_agents()`
- c0033 ..> c0030: `_foreman() calls build_start_foreman()`
- c0033 ..> c0030: `_initialise() calls build_channel()`
- c0033 ..> c0030: `_initialise_locked() calls build_initialiser()`
- c0033 ..> c0030: `_launch_setup_foreman() calls build_host()`
- c0033 ..> c0030: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0033 ..> c0030: `_watch_locked() calls build_watcher()`
- c0033 ..> c0030: `_watch_status() calls build_watch_status()`
- c0033 ..> c0031: `main() constructs DeadlinePolicy`
- c0033 ..> c0031: `type in _finish_existing_setup`
- c0033 ..> c0031: `type in _foreman`
- c0033 ..> c0031: `type in _initialise`
- c0033 ..> c0031: `type in _initialise_locked`
- c0033 ..> c0031: `type in _start_initial_setup`
- c0033 ..> c0031: `type in _watch`
- c0033 ..> c0031: `type in _watch_locked`
- c0033 ..> c0031: `type in _watch_status`
- c0033 ..> c0031: `type in main`
- c0033 ..> c0032: `_start_initial_setup() constructs _InitialSetupState`
- c0033 ..> c0032: `type in _discover_worker_models`
- c0033 ..> c0032: `type in _validate_initial_model`
- c0033 ..> c0033: `_complete_setup() calls _managed_rest_mapping_available()`
- c0033 ..> c0033: `_configure_new_factory() calls _prepare_foreman()`
- c0033 ..> c0033: `_configure_new_factory() calls _select_model()`
- c0033 ..> c0033: `_configure_new_factory() calls _select_numbered()`
- c0033 ..> c0033: `_configure_new_factory() calls select_repositories()`
- c0033 ..> c0033: `_connection() calls _check_existing_connection()`
- c0033 ..> c0033: `_discover_worker_models() calls _prepare_foreman()`
- c0033 ..> c0033: `_finish_existing_setup() calls _complete_setup()`
- c0033 ..> c0033: `_finish_existing_setup() calls _confirm_pi_home()`
- c0033 ..> c0033: `_finish_existing_setup() calls _connection()`
- c0033 ..> c0033: `_finish_existing_setup() calls _launch_setup_foreman()`
- c0033 ..> c0033: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0033 ..> c0033: `_foreman_memory_choices() calls _select_numbered()`
- c0033 ..> c0033: `_initialise() calls _initialise_locked()`
- c0033 ..> c0033: `_initialise() calls _offer_factory_launch()`
- c0033 ..> c0033: `_initialise_locked() calls _finish_existing_setup()`
- c0033 ..> c0033: `_initialise_locked() calls _start_initial_setup()`
- c0033 ..> c0033: `_initialise_locked() calls _validate_setup_owner()`
- c0033 ..> c0033: `_print_models() calls _safe_diagnostic()`
- c0033 ..> c0033: `_prompt_coordinator_choices() calls _select_numbered()`
- c0033 ..> c0033: `_prompt_worker() calls _select_numbered()`
- c0033 ..> c0033: `_prompt_workers() calls _prompt_worker()`
- c0033 ..> c0033: `_select_model() calls _print_models()`
- c0033 ..> c0033: `_select_model() calls _select_numbered()`
- c0033 ..> c0033: `_select_numbered() calls _safe_diagnostic()`
- c0033 ..> c0033: `_select_project() calls _listed_project_id()`
- c0033 ..> c0033: `_select_project() calls _safe_diagnostic()`
- c0033 ..> c0033: `_select_setup_route() calls _select_numbered()`
- c0033 ..> c0033: `_start_initial_setup() calls _complete_setup()`
- c0033 ..> c0033: `_start_initial_setup() calls _configure_new_factory()`
- c0033 ..> c0033: `_start_initial_setup() calls _confirm_pi_home()`
- c0033 ..> c0033: `_start_initial_setup() calls _connection()`
- c0033 ..> c0033: `_start_initial_setup() calls _foreman_memory_choices()`
- c0033 ..> c0033: `_start_initial_setup() calls _launch_setup_foreman()`
- c0033 ..> c0033: `_start_initial_setup() calls _owner_choices()`
- c0033 ..> c0033: `_start_initial_setup() calls _research_choices()`
- c0033 ..> c0033: `_start_initial_setup() calls _worker_choices()`
- c0033 ..> c0033: `_validate_initial_model() calls _prepare_foreman()`
- c0033 ..> c0033: `_validate_initial_model() calls _select_model()`
- c0033 ..> c0033: `_validate_initial_model() calls _select_project()`
- c0033 ..> c0033: `_watch() calls _change_managed_watch()`
- c0033 ..> c0033: `_watch() calls _watch_locked()`
- c0033 ..> c0033: `_watch() calls _watch_status()`
- c0033 ..> c0033: `_watch_locked() calls _choose_existing()`
- c0033 ..> c0033: `_watch_locked() calls _safe_diagnostic()`
- c0033 ..> c0033: `_worker_choices() calls _prompt_coordinator_choices()`
- c0033 ..> c0033: `_worker_choices() calls _prompt_workers()`
- c0033 ..> c0033: `_worker_choices() calls _select_setup_route()`
- c0033 ..> c0033: `_worker_choices() calls _worker_arguments()`
- c0033 ..> c0033: `main() calls _foreman()`
- c0033 ..> c0033: `main() calls _initialise()`
- c0033 ..> c0033: `main() calls _parse_arguments()`
- c0033 ..> c0033: `main() calls _safe_diagnostic()`
- c0033 ..> c0033: `main() calls _watch()`
- c0033 ..> c0034: `_select_numbered() calls parse_numbered_selection()`
- c0033 ..> c0035: `main() calls update_resources()`
- c0033 ..> c0036: `_watch_locked() calls load_configuration()`
- c0033 ..> c0037: `_initialise_locked() calls load()`
- c0033 ..> c0039: `_finish_existing_setup() constructs MarkdownAgreement`
- c0033 ..> c0039: `_start_initial_setup() constructs MarkdownAgreement`
- c0033 ..> c0041: `_initialise() calls quote()`
- c0033 ..> c0041: `_launch_setup_foreman() calls quote()`
- c0033 ..> c0041: `_select_model() calls quote()`
- c0033 ..> c0041: `_validate_setup_owner() calls quote()`
- c0033 ..> c0041: `_watch_locked() calls quote()`
- c0033 ..> c0042: `_initialise() calls hold()`
- c0033 ..> c0042: `_initialise() constructs WorkspaceWatchLease`
- c0033 ..> c0042: `_watch() calls hold()`
- c0033 ..> c0042: `_watch() constructs WorkspaceWatchLease`
- c0033 ..> c0044: `_prompt_workers() calls update()`
- c0033 ..> c0045: `_watch_locked() calls observe_plain_watch()`
- c0033 ..> c0046: `type in _complete_setup`
- c0033 ..> c0046: `type in _configure_new_factory`
- c0033 ..> c0046: `type in _finish_existing_setup`
- c0033 ..> c0046: `type in _validate_initial_model`
- c0033 ..> c0047: `_connection() calls validate()`
- c0033 ..> c0067: `_finish_existing_setup() calls agree_definition_of_done()`
- c0033 ..> c0067: `_start_initial_setup() calls agree_definition_of_done()`
- c0033 ..> c0069: `_complete_setup() calls check_foreman()`
- c0033 ..> c0069: `_configure_new_factory() calls configure()`
- c0033 ..> c0069: `_configure_new_factory() calls inspect()`
- c0033 ..> c0069: `_finish_existing_setup() calls initialise()`
- c0033 ..> c0069: `_initialise_locked() calls load_existing()`
- c0033 ..> c0069: `_launch_setup_foreman() calls check_foreman()`
- c0033 ..> c0069: `_prepare_foreman() calls prepare_foreman()`
- c0033 ..> c0069: `_start_initial_setup() calls initialise()`
- c0033 ..> c0069: `select_repositories() calls discover()`
- c0033 ..> c0069: `type in _complete_setup`
- c0033 ..> c0069: `type in _configure_new_factory`
- c0033 ..> c0069: `type in _discover_worker_models`
- c0033 ..> c0069: `type in _finish_existing_setup`
- c0033 ..> c0069: `type in _select_project`
- c0033 ..> c0069: `type in _start_initial_setup`
- c0033 ..> c0069: `type in _validate_initial_model`
- c0033 ..> c0069: `type in select_repositories`
- c0033 ..> c0082: `_complete_setup() calls uses_browser_login()`
- c0033 ..> c0083: `_select_project() calls create_project()`
- c0033 ..> c0083: `_select_project() calls projects()`
- c0033 ..> c0089: `_connection() constructs ForgetfulConnection`
- c0033 ..> c0089: `type in _check_existing_connection`
- c0033 ..> c0089: `type in _configure_new_factory`
- c0033 ..> c0089: `type in _connection`
- c0033 ..> c0089: `type in _foreman_memory_choices`
- c0033 ..> c0089: `type in _managed_rest_mapping_available`
- c0033 ..> c0089: `type in _select_project`
- c0033 ..> c0099: `_change_managed_watch() constructs FactoryError`
- c0033 ..> c0099: `_check_existing_connection() constructs FactoryError`
- c0033 ..> c0099: `_choose_existing() constructs FactoryError`
- c0033 ..> c0099: `_configure_new_factory() constructs FactoryError`
- c0033 ..> c0099: `_finish_existing_setup() constructs FactoryError`
- c0033 ..> c0099: `_foreman_memory_choices() constructs FactoryError`
- c0033 ..> c0099: `_initialise() constructs FactoryError`
- c0033 ..> c0099: `_initialise_locked() constructs FactoryError`
- c0033 ..> c0099: `_install_missing() constructs FactoryError`
- c0033 ..> c0099: `_listed_project_id() constructs FactoryError`
- c0033 ..> c0099: `_prompt_coordinator_choices() constructs FactoryError`
- c0033 ..> c0099: `_prompt_worker() constructs FactoryError`
- c0033 ..> c0099: `_select_model() constructs FactoryError`
- c0033 ..> c0099: `_select_project() constructs FactoryError`
- c0033 ..> c0099: `_validate_setup_owner() constructs FactoryError`
- c0033 ..> c0099: `_watch_locked() constructs FactoryError`
- c0033 ..> c0099: `_worker_choices() constructs FactoryError`
- c0033 ..> c0099: `main() constructs FactoryError`
- c0033 ..> c0099: `select_repositories() constructs FactoryError`
- c0033 ..> c0102: `_discover_worker_models() calls check_real_path()`
- c0033 ..> c0107: `_watch_locked() calls watch_stop_scope()`
- c0034 ..> c0099: `parse_numbered_selection() constructs FactoryError`
- c0035 ..> c0002: `update_resources() calls ready()`
- c0035 ..> c0008: `update_resources() calls read_state()`
- c0035 ..> c0009: `update_resources() calls install()`
- c0035 ..> c0009: `update_resources() constructs AgentShellRuntimeInstall`
- c0035 ..> c0013: `update_resources() calls validate_bundled_resources()`
- c0035 ..> c0018: `update_resources() calls apply_update()`
- c0035 ..> c0018: `update_resources() calls plan_update()`
- c0035 ..> c0030: `update_resources() calls build_team()`
- c0035 ..> c0031: `type in update_resources`
- c0035 ..> c0035: `update_resources() calls _report()`
- c0035 ..> c0042: `update_resources() calls hold()`
- c0035 ..> c0042: `update_resources() constructs WorkspaceWatchLease`
- c0035 ..> c0099: `_report() constructs FactoryError`
- c0035 ..> c0099: `update_resources() constructs FactoryError`
- c0036 ..> c0037: `load_configuration() calls load()`
- c0036 ..> c0040: `load_configuration() constructs TomlConfigurationStore`
- c0036 ..> c0046: `type in load_configuration`
- c0036 ..> c0099: `load_configuration() constructs FactoryError`
- c0037 ..> c0000: `_load() calls close()`
- c0037 ..> c0037: `confirm() calls load()`
- c0037 ..> c0037: `load() calls _load()`
- c0037 ..> c0038: `_load() calls _resource()`
- c0037 ..> c0039: `_load() calls read()`
- c0037 ..> c0058: `type in _load`
- c0037 ..> c0058: `type in confirm`
- c0037 ..> c0058: `type in load`
- c0037 ..> c0099: `confirm() constructs FactoryError`
- c0037 ..> c0099: `load() constructs FactoryError`
- c0037 ..> c0102: `_load() calls check_real_path()`
- c0037 ..> c0102: `confirm() calls replace_generated_json()`
- c0037 ..> c0107: `confirm() calls check_watch_stop()`
- c0038 ..> c0058: `_resource() constructs CleanupSet`
- c0038 ..> c0058: `type in _resource`
- c0039 ..> c0102: `found() calls check_skill_file()`
- c0039 ..> c0102: `write() calls write_new()`
- c0040 ..> c0000: `load() calls close()`
- c0040 ..> c0000: `save() calls close()`
- c0040 ..> c0037: `load() calls load()`
- c0040 ..> c0039: `save() calls write()`
- c0040 ..> c0041: `save() calls quote()`
- c0040 ..> c0046: `type in load`
- c0040 ..> c0046: `type in save`
- c0040 ..> c0047: `load() calls from_mapping()`
- c0040 ..> c0099: `load() constructs FactoryError`
- c0040 ..> c0099: `save() constructs FactoryError`
- c0042 ..> c0000: `_hold_directory() calls close()`
- c0042 ..> c0042: `hold() calls _hold_directory()`
- c0042 ..> c0099: `_hold_directory() constructs FactoryError`
- c0043 ..> c0000: `close() calls close()`
- c0043 ..> c0000: `send() calls send()`
- c0043 ..> c0000: `start() calls start()`
- c0043 ..> c0000: `startup_hint() calls startup_hint()`
- c0043 ..> c0000: `wait() calls wait()`
- c0043 ..> c0024: `__init__() calls unknown_status()`
- c0043 ..> c0026: `type in __init__`
- c0043 ..> c0044: `close() calls update()`
- c0043 ..> c0044: `start() calls update()`
- c0043 ..> c0044: `type in __init__`
- c0044 ..> c0043: `__enter__() calls start()`
- c0044 ..> c0043: `_close_resources() calls close()`
- c0044 ..> c0044: `__enter__() calls _close_resources()`
- c0044 ..> c0044: `__enter__() calls snapshot()`
- c0044 ..> c0044: `__enter__() calls update()`
- c0044 ..> c0044: `__exit__() calls _close_resources()`
- c0044 ..> c0044: `__exit__() calls _publish_history()`
- c0044 ..> c0044: `__exit__() calls snapshot()`
- c0044 ..> c0044: `__exit__() calls update()`
- c0044 ..> c0044: `_serve() calls snapshot()`
- c0044 ..> c0044: `update() calls _publish_history()`
- c0044 ..> c0045: `__enter__() calls _discovery_path()`
- c0044 ..> c0045: `__enter__() calls _endpoint()`
- c0044 ..> c0045: `_publish_history() calls _discovery_path()`
- c0044 ..> c0045: `_publish_history() calls _read_discovery()`
- c0044 ..> c0045: `_serve() calls _frame()`
- c0044 ..> c0045: `_serve() calls _peer()`
- c0044 ..> c0099: `__enter__() constructs FactoryError`
- c0044 ..> c0102: `__enter__() calls check_real_path()`
- c0044 ..> c0102: `__enter__() calls replace_generated_json()`
- c0044 ..> c0102: `_publish_history() calls replace_generated_json()`
- c0045 ..> c0024: `plain_watch_status() calls unknown_status()`
- c0045 ..> c0039: `_read_discovery() calls read()`
- c0045 ..> c0044: `observe_plain_watch() calls __enter__()`
- c0045 ..> c0044: `observe_plain_watch() calls __exit__()`
- c0045 ..> c0044: `observe_plain_watch() constructs PlainWatchObservation`
- c0045 ..> c0044: `type in observe_plain_watch`
- c0045 ..> c0045: `_frame() calls _observation_json()`
- c0045 ..> c0045: `_read_discovery() calls _discovery_path()`
- c0045 ..> c0045: `_read_discovery() calls _observation_json()`
- c0045 ..> c0045: `plain_watch_status() calls _endpoint()`
- c0045 ..> c0045: `plain_watch_status() calls _frame()`
- c0045 ..> c0045: `plain_watch_status() calls _peer()`
- c0045 ..> c0045: `plain_watch_status() calls _read_discovery()`
- c0045 ..> c0102: `_read_discovery() calls check_real_path()`
- c0046 --> c0048: `field repository`
- c0046 --> c0089: `field forgetful`
- c0047 ..> c0046: `from_mapping() constructs FactoryConfiguration`
- c0047 ..> c0046: `type in from_mapping`
- c0047 ..> c0046: `type in validate`
- c0047 ..> c0047: `from_mapping() calls validate()`
- c0047 ..> c0048: `from_mapping() constructs RepositoryReference`
- c0047 ..> c0089: `validate() calls validate()`
- c0047 ..> c0090: `from_mapping() calls connection_from_mapping()`
- c0047 ..> c0099: `from_mapping() constructs FactoryError`
- c0047 ..> c0099: `validate() constructs FactoryError`
- c0047 ..> c0105: `unique_labels() calls nonblank()`
- c0047 ..> c0105: `validate() calls nonblank()`
- c0047 ..> c0111: `from_mapping() constructs TicketSource`
- c0048 --> c0111: `field work_source`
- c0049 --|> c0051: `inherits`
- c0050 --|> c0051: `inherits`
- c0051 --|> c0099: `inherits`
- c0052 --|> c0051: `inherits`
- c0053 --|> c0051: `inherits`
- c0054 ..> c0000: `__init__() calls __init__()`
- c0054 ..> c0000: `send() calls send()`
- c0054 ..> c0055: `send() calls _cleanup_recovery()`
- c0054 ..> c0099: `type in send`
- c0057 ..> c0058: `type in confirm`
- c0057 ..> c0058: `type in load`
- c0059 ..> c0046: `type in load`
- c0059 ..> c0046: `type in save`
- c0062 ..> c0000: `_candidates() calls send()`
- c0062 ..> c0000: `_dispose() calls send()`
- c0062 ..> c0000: `_read_problem() calls send()`
- c0062 ..> c0000: `_repository_identities() calls send()`
- c0062 ..> c0000: `poll() calls send()`
- c0062 ..> c0007: `_dispose() calls report()`
- c0062 ..> c0037: `_dispose() calls confirm()`
- c0062 ..> c0037: `poll() calls load()`
- c0062 ..> c0044: `_candidate() calls snapshot()`
- c0062 ..> c0044: `_candidate() calls update()`
- c0062 ..> c0044: `_check_namespaces() calls update()`
- c0062 ..> c0044: `_still_completed() calls snapshot()`
- c0062 ..> c0051: `_candidate() constructs ScaffoldProblem`
- c0062 ..> c0051: `_check_namespaces() constructs ScaffoldProblem`
- c0062 ..> c0051: `_dispose() constructs ScaffoldProblem`
- c0062 ..> c0051: `_is_confirmed() constructs ScaffoldProblem`
- c0062 ..> c0051: `_still_completed() constructs ScaffoldProblem`
- c0062 ..> c0051: `_task_mappings() constructs ScaffoldProblem`
- c0062 ..> c0051: `_validate_claim_mapping() constructs ScaffoldProblem`
- c0062 ..> c0054: `_dispose() calls clear()`
- c0062 ..> c0054: `_repository_identities() calls clear()`
- c0062 ..> c0054: `poll() calls clear()`
- c0062 ..> c0054: `type in _candidates`
- c0062 ..> c0054: `type in _claim_indexes`
- c0062 ..> c0054: `type in _dispose`
- c0062 ..> c0054: `type in _read_plans`
- c0062 ..> c0054: `type in _read_problem`
- c0062 ..> c0054: `type in _repository_identities`
- c0062 ..> c0054: `type in poll`
- c0062 ..> c0057: `type in __init__`
- c0062 --> c0058: `field confirmed`
- c0062 ..> c0058: `_is_confirmed() calls overlaps()`
- c0062 ..> c0058: `_mapping_identity() constructs CleanupSet`
- c0062 ..> c0058: `type in _mapping_identity`
- c0062 ..> c0062: `_candidate() calls _keys()`
- c0062 ..> c0062: `_candidates() calls _candidate()`
- c0062 ..> c0062: `_candidates() calls _in_scope()`
- c0062 ..> c0062: `_check_namespaces() calls _keys()`
- c0062 ..> c0062: `_claim_indexes() calls _claims()`
- c0062 ..> c0062: `_claim_indexes() calls _read_problem()`
- c0062 ..> c0062: `_claims() calls _is_confirmed()`
- c0062 ..> c0062: `_claims() calls _keys()`
- c0062 ..> c0062: `_claims() calls _task_mappings()`
- c0062 ..> c0062: `_dispose() calls _check_namespaces()`
- c0062 ..> c0062: `_dispose() calls _keys()`
- c0062 ..> c0062: `_dispose() calls _mapping_identity()`
- c0062 ..> c0062: `_dispose() calls _overlaps()`
- c0062 ..> c0062: `_dispose() calls _read_problem()`
- c0062 ..> c0062: `_dispose() calls _still_completed()`
- c0062 ..> c0062: `_is_confirmed() calls _mapping_identity()`
- c0062 ..> c0062: `_read_plans() calls _read_problem()`
- c0062 ..> c0062: `_still_completed() calls _in_scope()`
- c0062 ..> c0062: `_task_mappings() calls _validate_claim_mapping()`
- c0062 ..> c0062: `poll() calls _candidates()`
- c0062 ..> c0062: `poll() calls _claim_indexes()`
- c0062 ..> c0062: `poll() calls _dispose()`
- c0062 ..> c0062: `poll() calls _in_scope()`
- c0062 ..> c0062: `poll() calls _is_confirmed()`
- c0062 ..> c0062: `poll() calls _order()`
- c0062 ..> c0062: `poll() calls _read_plans()`
- c0062 ..> c0062: `poll() calls _repository_identities()`
- c0062 ..> c0063: `_candidate() constructs CompletedWork`
- c0062 ..> c0063: `type in _candidate`
- c0062 ..> c0063: `type in _candidates`
- c0062 ..> c0063: `type in _dispose`
- c0062 ..> c0063: `type in _order`
- c0062 ..> c0063: `type in _still_completed`
- c0062 ..> c0064: `_candidate() calls _claim_path()`
- c0062 ..> c0064: `_claims() calls _claim_path()`
- c0062 ..> c0064: `_dispose() calls _claim_path()`
- c0062 ..> c0064: `_keys() calls _claim_path()`
- c0062 ..> c0064: `_overlaps() calls _claim_path()`
- c0062 ..> c0064: `_repository_identities() calls _claim_path()`
- c0062 ..> c0068: `_candidate() calls check_source()`
- c0062 ..> c0068: `_candidate() calls context()`
- c0062 ..> c0068: `_candidate() calls mapping_repository()`
- c0062 ..> c0068: `_candidate() calls ownership_records()`
- c0062 ..> c0068: `_dispose() calls check_repository()`
- c0062 ..> c0068: `_dispose() calls mapping_repository()`
- c0062 ..> c0068: `_still_completed() calls context()`
- c0062 ..> c0068: `_still_completed() calls ownership()`
- c0062 ..> c0068: `type in __init__`
- c0062 ..> c0086: `_candidates() calls tasks()`
- c0062 ..> c0086: `_claim_indexes() calls tasks()`
- c0062 ..> c0086: `_in_scope() calls owns()`
- c0062 ..> c0086: `_mapping_identity() calls backend_identity()`
- c0062 ..> c0086: `_read_plans() calls get_plan()`
- c0062 ..> c0086: `_still_completed() calls get_plan()`
- c0062 ..> c0086: `poll() calls plans()`
- c0062 ..> c0099: `type in _read_problem`
- c0062 ..> c0108: `_in_scope() calls is_key()`
- c0062 ..> c0112: `type in __init__`
- c0062 ..> c0115: `_claims() calls repository_identity()`
- c0062 ..> c0115: `_dispose() calls dispose()`
- c0062 ..> c0115: `_repository_identities() calls repository_identity()`
- c0062 ..> c0115: `poll() calls begin_cleanup_cycle()`
- c0062 ..> c0120: `type in __init__`
- c0066 ..> c0065: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0066 ..> c0079: `validate_cleanup_marker() calls is_change_request()`
- c0066 ..> c0080: `type in validate_cleanup_marker`
- c0066 ..> c0081: `type in validate_cleanup_marker`
- c0067 ..> c0039: `agree_definition_of_done() calls found()`
- c0067 ..> c0039: `agree_definition_of_done() calls read()`
- c0067 ..> c0039: `agree_definition_of_done() calls write()`
- c0067 ..> c0046: `type in agree_definition_of_done`
- c0067 ..> c0056: `type in agree_definition_of_done`
- c0067 ..> c0067: `agree_definition_of_done() calls _deployment_agreement()`
- c0067 ..> c0099: `_deployment_agreement() constructs FactoryError`
- c0067 ..> c0099: `agree_definition_of_done() constructs FactoryError`
- c0068 ..> c0046: `type in __init__`
- c0068 ..> c0048: `type in check_repository`
- c0068 ..> c0048: `type in check_source`
- c0068 ..> c0048: `type in mapping_repository`
- c0068 ..> c0050: `check_repository() constructs RepositoryProblem`
- c0068 ..> c0050: `check_source() constructs RepositoryProblem`
- c0068 ..> c0051: `active() constructs ScaffoldProblem`
- c0068 ..> c0051: `context() constructs ScaffoldProblem`
- c0068 ..> c0051: `mapping_repository() constructs ScaffoldProblem`
- c0068 ..> c0051: `ownership_records() constructs ScaffoldProblem`
- c0068 ..> c0051: `snapshot() constructs ScaffoldProblem`
- c0068 ..> c0068: `check_repository() calls check_source()`
- c0068 ..> c0068: `ownership() calls ownership_records()`
- c0068 ..> c0079: `check_source() calls repository()`
- c0068 ..> c0080: `type in check_source`
- c0068 ..> c0081: `type in __init__`
- c0068 ..> c0086: `ownership() calls tasks()`
- c0068 ..> c0091: `type in __init__`
- c0068 ..> c0108: `snapshot() calls is_key()`
- c0068 ..> c0110: `snapshot() constructs Ticket`
- c0068 ..> c0110: `type in snapshot`
- c0068 ..> c0111: `snapshot() constructs TicketSource`
- c0068 ..> c0112: `type in __init__`
- c0068 ..> c0113: `check_repository() calls origin()`
- c0068 ..> c0117: `type in __init__`
- c0069 ..> c0005: `initialise() calls save()`
- c0069 ..> c0009: `prepare_foreman() calls install()`
- c0069 ..> c0013: `prepare_foreman() calls prepare()`
- c0069 ..> c0025: `type in __init__`
- c0069 ..> c0037: `load_existing() calls load()`
- c0069 ..> c0037: `prepare_foreman() calls confirm()`
- c0069 ..> c0046: `configure() constructs FactoryConfiguration`
- c0069 ..> c0046: `type in _preflight`
- c0069 ..> c0046: `type in check_foreman`
- c0069 ..> c0046: `type in configure`
- c0069 ..> c0046: `type in initialise`
- c0069 ..> c0046: `type in load_existing`
- c0069 ..> c0047: `_preflight() calls validate()`
- c0069 ..> c0047: `configure() calls unique_labels()`
- c0069 ..> c0047: `load_existing() calls unique_labels()`
- c0069 ..> c0048: `inspect() constructs RepositoryReference`
- c0069 ..> c0048: `type in inspect`
- c0069 ..> c0059: `type in __init__`
- c0069 ..> c0060: `type in __init__`
- c0069 ..> c0069: `configure() calls inspect()`
- c0069 ..> c0069: `initialise() calls _ensure_label()`
- c0069 ..> c0069: `initialise() calls _preflight()`
- c0069 ..> c0070: `prepare_foreman() calls _reviewed_install()`
- c0069 ..> c0070: `prepare_foreman() calls missing_tools()`
- c0069 ..> c0071: `check_foreman() calls check()`
- c0069 ..> c0079: `_preflight() calls repository()`
- c0069 ..> c0079: `inspect() calls repository()`
- c0069 ..> c0081: `type in __init__`
- c0069 ..> c0083: `check_foreman() calls login()`
- c0069 ..> c0089: `type in __init__`
- c0069 ..> c0089: `type in prepare_foreman`
- c0069 ..> c0093: `type in __init__`
- c0069 ..> c0099: `_preflight() constructs FactoryError`
- c0069 ..> c0099: `initialise() constructs FactoryError`
- c0069 ..> c0099: `inspect() constructs FactoryError`
- c0069 ..> c0099: `load_existing() constructs FactoryError`
- c0069 ..> c0099: `prepare_foreman() constructs FactoryError`
- c0069 ..> c0108: `_ensure_label() calls create_label()`
- c0069 ..> c0108: `_preflight() calls check_access()`
- c0069 ..> c0108: `_preflight() calls list_labels()`
- c0069 ..> c0108: `_preflight() calls validate_source()`
- c0069 ..> c0109: `_ensure_label() constructs Label`
- c0069 ..> c0109: `type in _preflight`
- c0069 ..> c0111: `inspect() constructs TicketSource`
- c0069 ..> c0111: `type in _ensure_label`
- c0069 ..> c0111: `type in _preflight`
- c0069 ..> c0112: `type in __init__`
- c0069 ..> c0113: `_preflight() calls origin()`
- c0069 ..> c0113: `discover() calls discover()`
- c0069 ..> c0113: `inspect() calls origin()`
- c0069 ..> c0117: `type in __init__`
- c0070 ..> c0009: `_reviewed_install() calls describe()`
- c0070 ..> c0009: `missing_tools() calls absent()`
- c0070 ..> c0009: `missing_tools() calls unready()`
- c0070 ..> c0060: `type in _reviewed_install`
- c0070 ..> c0060: `type in missing_tools`
- c0071 ..> c0044: `recover() calls snapshot()`
- c0071 ..> c0046: `type in __init__`
- c0071 ..> c0048: `type in _ensure_validated_mapping`
- c0071 ..> c0048: `type in _repository`
- c0071 ..> c0048: `type in check_repository`
- c0071 ..> c0049: `preflight() constructs IntakeProblem`
- c0071 ..> c0051: `_create_plan() constructs ScaffoldProblem`
- c0071 ..> c0051: `_ensure_mapping() constructs ScaffoldProblem`
- c0071 ..> c0051: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0071 ..> c0051: `_recovery_plan() constructs ScaffoldProblem`
- c0071 ..> c0051: `_setup_ownership() constructs ScaffoldProblem`
- c0071 ..> c0051: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0071 ..> c0051: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0071 ..> c0051: `lookup() constructs ScaffoldProblem`
- c0071 ..> c0052: `_create_plan() constructs ScaffoldReadProblem`
- c0071 ..> c0052: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0071 ..> c0052: `lookup() constructs ScaffoldReadProblem`
- c0071 ..> c0052: `prepare() constructs ScaffoldReadProblem`
- c0071 ..> c0052: `recover() constructs ScaffoldReadProblem`
- c0071 ..> c0053: `_create_ownership() constructs UncertainScaffold`
- c0071 ..> c0053: `_create_plan() constructs UncertainScaffold`
- c0071 ..> c0053: `_setup_ownership() constructs UncertainScaffold`
- c0071 ..> c0053: `_sole_recovery_owner() constructs UncertainScaffold`
- c0071 ..> c0053: `prepare() constructs UncertainScaffold`
- c0071 ..> c0066: `_ensure_mapping() calls validate_cleanup_marker()`
- c0071 ..> c0068: `__init__() constructs FactoryRecords`
- c0071 ..> c0068: `_create_ownership() calls ownership()`
- c0071 ..> c0068: `_ensure_mapping() calls check_source()`
- c0071 ..> c0068: `_ensure_worktrees() calls mapping_repository()`
- c0071 ..> c0068: `_prepare_plan() calls active()`
- c0071 ..> c0068: `_prepare_plan() calls context()`
- c0071 ..> c0068: `_setup_ownership() calls ownership()`
- c0071 ..> c0068: `check_repository() calls check_repository()`
- c0071 ..> c0068: `recover() calls active()`
- c0071 ..> c0068: `recover() calls context()`
- c0071 ..> c0068: `recover() calls ownership()`
- c0071 ..> c0069: `preflight() calls inspect()`
- c0071 ..> c0071: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0071 ..> c0071: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0071 ..> c0071: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0071 ..> c0071: `_initial_mappings() calls _repository()`
- c0071 ..> c0071: `_prepare_plan() calls _create_ownership()`
- c0071 ..> c0071: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0071 ..> c0071: `_prepare_plan() calls _setup_ownership()`
- c0071 ..> c0071: `preflight() calls _initial_mappings()`
- c0071 ..> c0071: `preflight() calls _repository()`
- c0071 ..> c0071: `preflight() calls check_repository()`
- c0071 ..> c0071: `prepare() calls _create_plan()`
- c0071 ..> c0071: `prepare() calls _prepare_plan()`
- c0071 ..> c0071: `prepare() calls lookup()`
- c0071 ..> c0071: `prepare() calls preflight()`
- c0071 ..> c0071: `prepare() calls recover()`
- c0071 ..> c0071: `recover() calls _ensure_worktrees()`
- c0071 ..> c0071: `recover() calls _recovery_plan()`
- c0071 ..> c0071: `recover() calls _repository()`
- c0071 ..> c0071: `recover() calls _sole_recovery_owner()`
- c0071 ..> c0071: `recover() calls _validate_recovery_candidates()`
- c0071 ..> c0071: `recover() calls check_repository()`
- c0071 ..> c0071: `unfinished() calls _is_unfinished_factory_plan()`
- c0071 ..> c0072: `_initial_mappings() calls worktree_name()`
- c0071 ..> c0081: `type in __init__`
- c0071 ..> c0083: `check() calls check()`
- c0071 ..> c0086: `_create_ownership() calls create_task()`
- c0071 ..> c0086: `_create_ownership() calls update_plan()`
- c0071 ..> c0086: `_create_plan() calls create_plan()`
- c0071 ..> c0086: `_create_plan() calls get_plan()`
- c0071 ..> c0086: `_create_plan() calls owns()`
- c0071 ..> c0086: `_create_plan() calls plans()`
- c0071 ..> c0086: `_is_unfinished_factory_plan() calls owns()`
- c0071 ..> c0086: `_recovery_plan() calls get_plan()`
- c0071 ..> c0086: `_recovery_plan() calls owns()`
- c0071 ..> c0086: `_recovery_plan() calls plans()`
- c0071 ..> c0086: `lookup() calls plans()`
- c0071 ..> c0086: `unfinished() calls plans()`
- c0071 ..> c0091: `type in __init__`
- c0071 ..> c0099: `_is_unfinished_factory_plan() constructs FactoryError`
- c0071 ..> c0110: `type in _create_plan`
- c0071 ..> c0110: `type in _initial_mappings`
- c0071 ..> c0110: `type in _prepare_plan`
- c0071 ..> c0110: `type in _setup_ownership`
- c0071 ..> c0110: `type in lookup`
- c0071 ..> c0110: `type in preflight`
- c0071 ..> c0110: `type in prepare`
- c0071 ..> c0110: `type in recover`
- c0071 ..> c0111: `type in _repository`
- c0071 ..> c0112: `type in __init__`
- c0071 ..> c0115: `_ensure_mapping() calls ensure()`
- c0071 ..> c0115: `_ensure_mapping() calls verify_removed()`
- c0071 ..> c0115: `_initial_mappings() calls target_branch()`
- c0071 ..> c0117: `type in __init__`
- c0071 ..> c0120: `type in __init__`
- c0072 ..> c0110: `type in worktree_name`
- c0073 ..> c0000: `run() calls start()`
- c0073 ..> c0007: `run() calls saved()`
- c0073 ..> c0007: `run() calls status()`
- c0073 ..> c0013: `run() calls prepare()`
- c0073 ..> c0027: `type in __init__`
- c0073 ..> c0029: `type in __init__`
- c0073 ..> c0042: `run() calls hold()`
- c0073 ..> c0061: `type in __init__`
- c0073 ..> c0099: `run() constructs FactoryError`
- c0074 --> c0110: `field issue`
- c0075 ..> c0000: `_alert_plan() calls send()`
- c0075 ..> c0000: `_check_pending_repositories() calls send()`
- c0075 ..> c0000: `_check_planning_access() calls send()`
- c0075 ..> c0000: `_handle_intake_read_problem() calls send()`
- c0075 ..> c0000: `_handle_intake_repository_problem() calls send()`
- c0075 ..> c0000: `_handle_recovery_read_problem() calls send()`
- c0075 ..> c0000: `_load_inventory() calls send()`
- c0075 ..> c0000: `_process_issue() calls send()`
- c0075 ..> c0000: `_read_issues() calls send()`
- c0075 ..> c0000: `_recover_work() calls send()`
- c0075 ..> c0000: `_submit() calls send()`
- c0075 ..> c0000: `_watch() calls close()`
- c0075 ..> c0000: `_watch() calls start()`
- c0075 ..> c0000: `_watch() calls wait()`
- c0075 ..> c0000: `run() calls startup_hint()`
- c0075 ..> c0007: `_baseline_source() calls report()`
- c0075 ..> c0007: `_check_planning_access() calls report()`
- c0075 ..> c0007: `_submit() calls report()`
- c0075 ..> c0007: `_watch() calls report()`
- c0075 ..> c0007: `run() calls report()`
- c0075 ..> c0013: `_process_issue() calls prepare()`
- c0075 ..> c0026: `type in __init__`
- c0075 ..> c0046: `type in _poll_sources`
- c0075 ..> c0046: `type in _repository_for_source`
- c0075 ..> c0046: `type in _watch`
- c0075 ..> c0046: `type in run`
- c0075 ..> c0048: `type in _handle_intake_repository_problem`
- c0075 ..> c0048: `type in _process_issue`
- c0075 ..> c0048: `type in _process_issues`
- c0075 ..> c0048: `type in _process_source`
- c0075 ..> c0048: `type in _repository_for_source`
- c0075 ..> c0050: `type in _handle_intake_repository_problem`
- c0075 ..> c0050: `type in _handle_recovery_repository_problem`
- c0075 ..> c0051: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0075 ..> c0051: `type in _alert_plan`
- c0075 ..> c0051: `type in _handle_intake_scaffold_problem`
- c0075 ..> c0052: `type in _handle_intake_read_problem`
- c0075 ..> c0052: `type in _handle_recovery_read_problem`
- c0075 ..> c0054: `_check_pending_repositories() calls clear()`
- c0075 ..> c0054: `_check_planning_access() calls clear()`
- c0075 ..> c0054: `_complete_intake() calls clear()`
- c0075 ..> c0054: `_complete_recovery() calls clear()`
- c0075 ..> c0054: `_load_inventory() calls clear()`
- c0075 ..> c0054: `_process_issue() calls clear()`
- c0075 ..> c0054: `_read_issues() calls clear()`
- c0075 ..> c0054: `_watch() calls clear()`
- c0075 ..> c0054: `_watch() constructs WatcherAlerts`
- c0075 ..> c0054: `type in _alert_plan`
- c0075 ..> c0054: `type in _check_pending_repositories`
- c0075 ..> c0054: `type in _check_planning_access`
- c0075 ..> c0054: `type in _complete_intake`
- c0075 ..> c0054: `type in _complete_recovery`
- c0075 ..> c0054: `type in _handle_intake_read_problem`
- c0075 ..> c0054: `type in _handle_intake_repository_problem`
- c0075 ..> c0054: `type in _handle_intake_scaffold_problem`
- c0075 ..> c0054: `type in _handle_recovery_read_problem`
- c0075 ..> c0054: `type in _handle_recovery_repository_problem`
- c0075 ..> c0054: `type in _load_inventory`
- c0075 ..> c0054: `type in _poll_sources`
- c0075 ..> c0054: `type in _process_issue`
- c0075 ..> c0054: `type in _process_issues`
- c0075 ..> c0054: `type in _process_source`
- c0075 ..> c0054: `type in _read_issues`
- c0075 ..> c0054: `type in _recover_blocked`
- c0075 ..> c0054: `type in _recover_work`
- c0075 ..> c0054: `type in _remember_inventory_candidate`
- c0075 ..> c0062: `_watch() calls poll()`
- c0075 ..> c0062: `type in __init__`
- c0075 ..> c0068: `_check_pending_repositories() calls check_repository()`
- c0075 ..> c0071: `_check_planning_access() calls check()`
- c0075 ..> c0071: `_load_inventory() calls unfinished()`
- c0075 ..> c0071: `_process_issue() calls lookup()`
- c0075 ..> c0071: `_process_issue() calls recover()`
- c0075 ..> c0071: `_recover_work() calls recover()`
- c0075 ..> c0071: `type in __init__`
- c0075 ..> c0074: `_complete_intake() constructs BlockedWork`
- c0075 ..> c0074: `_handle_intake_read_problem() constructs BlockedWork`
- c0075 ..> c0074: `_handle_intake_repository_problem() constructs BlockedWork`
- c0075 ..> c0074: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0075 ..> c0074: `_process_issue() constructs BlockedWork`
- c0075 ..> c0074: `_remember_inventory_candidate() constructs BlockedWork`
- c0075 ..> c0074: `type in _alert_plan`
- c0075 ..> c0074: `type in _complete_intake`
- c0075 ..> c0074: `type in _complete_recovery`
- c0075 ..> c0074: `type in _handle_recovery_read_problem`
- c0075 ..> c0074: `type in _handle_recovery_repository_problem`
- c0075 ..> c0074: `type in _recover_work`
- c0075 ..> c0074: `type in _remember_task_ids`
- c0075 ..> c0075: `_complete_intake() calls _submit()`
- c0075 ..> c0075: `_complete_recovery() calls _submit()`
- c0075 ..> c0075: `_handle_intake_read_problem() calls _sole_task_id()`
- c0075 ..> c0075: `_handle_intake_repository_problem() calls _alert_plan()`
- c0075 ..> c0075: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0075 ..> c0075: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0075 ..> c0075: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0075 ..> c0075: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0075 ..> c0075: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0075 ..> c0075: `_load_inventory() calls _remember_inventory_candidate()`
- c0075 ..> c0075: `_poll_sources() calls _baseline_source()`
- c0075 ..> c0075: `_poll_sources() calls _process_source()`
- c0075 ..> c0075: `_poll_sources() calls _read_issues()`
- c0075 ..> c0075: `_poll_sources() calls _repository_for_source()`
- c0075 ..> c0075: `_process_issue() calls _complete_intake()`
- c0075 ..> c0075: `_process_issue() calls _handle_intake_read_problem()`
- c0075 ..> c0075: `_process_issue() calls _handle_intake_repository_problem()`
- c0075 ..> c0075: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0075 ..> c0075: `_process_issues() calls _process_issue()`
- c0075 ..> c0075: `_process_issues() calls _skip_issue()`
- c0075 ..> c0075: `_process_source() calls _include_pending_lookups()`
- c0075 ..> c0075: `_process_source() calls _process_issues()`
- c0075 ..> c0075: `_recover_blocked() calls _recover_work()`
- c0075 ..> c0075: `_recover_work() calls _alert_plan()`
- c0075 ..> c0075: `_recover_work() calls _complete_recovery()`
- c0075 ..> c0075: `_recover_work() calls _handle_recovery_read_problem()`
- c0075 ..> c0075: `_recover_work() calls _handle_recovery_repository_problem()`
- c0075 ..> c0075: `_recover_work() calls _remember_task_ids()`
- c0075 ..> c0075: `_remember_inventory_candidate() calls _alert_plan()`
- c0075 ..> c0075: `_watch() calls _check_pending_repositories()`
- c0075 ..> c0075: `_watch() calls _check_planning_access()`
- c0075 ..> c0075: `_watch() calls _load_inventory()`
- c0075 ..> c0075: `_watch() calls _poll_sources()`
- c0075 ..> c0075: `_watch() calls _recover_blocked()`
- c0075 ..> c0075: `run() calls _watch()`
- c0075 ..> c0076: `_watch() constructs _WatchState`
- c0075 ..> c0076: `type in _baseline_source`
- c0075 ..> c0076: `type in _check_pending_repositories`
- c0075 ..> c0076: `type in _check_planning_access`
- c0075 ..> c0076: `type in _complete_intake`
- c0075 ..> c0076: `type in _complete_recovery`
- c0075 ..> c0076: `type in _handle_intake_read_problem`
- c0075 ..> c0076: `type in _handle_intake_repository_problem`
- c0075 ..> c0076: `type in _handle_intake_scaffold_problem`
- c0075 ..> c0076: `type in _handle_recovery_repository_problem`
- c0075 ..> c0076: `type in _load_inventory`
- c0075 ..> c0076: `type in _poll_sources`
- c0075 ..> c0076: `type in _process_issue`
- c0075 ..> c0076: `type in _process_issues`
- c0075 ..> c0076: `type in _process_source`
- c0075 ..> c0076: `type in _recover_blocked`
- c0075 ..> c0076: `type in _recover_work`
- c0075 ..> c0076: `type in _remember_inventory_candidate`
- c0075 ..> c0076: `type in _skip_issue`
- c0075 ..> c0077: `type in _process_issue`
- c0075 ..> c0077: `type in _recover_work`
- c0075 ..> c0099: `_read_issues() constructs FactoryError`
- c0075 ..> c0107: `_submit() calls check_watch_stop()`
- c0075 ..> c0107: `_watch() calls check_watch_stop()`
- c0075 ..> c0107: `run() calls check_watch_stop()`
- c0075 ..> c0108: `_read_issues() calls list_open()`
- c0075 ..> c0110: `type in _baseline_source`
- c0075 ..> c0110: `type in _complete_intake`
- c0075 ..> c0110: `type in _complete_recovery`
- c0075 ..> c0110: `type in _handle_intake_read_problem`
- c0075 ..> c0110: `type in _handle_intake_repository_problem`
- c0075 ..> c0110: `type in _handle_intake_scaffold_problem`
- c0075 ..> c0110: `type in _include_pending_lookups`
- c0075 ..> c0110: `type in _process_issue`
- c0075 ..> c0110: `type in _process_issues`
- c0075 ..> c0110: `type in _process_source`
- c0075 ..> c0110: `type in _read_issues`
- c0075 ..> c0110: `type in _skip_issue`
- c0075 ..> c0110: `type in _submit`
- c0075 ..> c0111: `_watch() constructs TicketSource`
- c0075 ..> c0111: `type in _baseline_source`
- c0075 ..> c0111: `type in _include_pending_lookups`
- c0075 ..> c0111: `type in _poll_sources`
- c0075 ..> c0111: `type in _process_source`
- c0075 ..> c0111: `type in _read_issues`
- c0075 ..> c0111: `type in _repository_for_source`
- c0075 ..> c0112: `type in __init__`
- c0076 --> c0048: `field pending_repositories`
- c0076 --> c0074: `field blocked`
- c0076 --> c0074: `field known`
- c0076 --> c0110: `field pending_lookup`
- c0076 --> c0111: `field baselined`
- c0078 ..> c0013: `_setup() calls validate_completion()`
- c0078 ..> c0024: `_without_live_plain() calls unknown_status()`
- c0078 ..> c0025: `type in __init__`
- c0078 ..> c0027: `type in __init__`
- c0078 ..> c0037: `_setup() calls load()`
- c0078 ..> c0059: `type in __init__`
- c0078 ..> c0078: `_without_live_plain() calls report()`
- c0078 ..> c0078: `report() calls _setup()`
- c0078 ..> c0078: `report() calls _without_live_plain()`
- c0079 ..> c0080: `repository() constructs RepositoryRef`
- c0079 ..> c0080: `type in is_change_request`
- c0079 ..> c0080: `type in repository`
- c0079 ..> c0099: `repository() constructs FactoryError`
- c0081 ..> c0080: `type in is_change_request`
- c0081 ..> c0080: `type in repository`
- c0082 ..> c0008: `uses_browser_login() calls request()`
- c0082 ..> c0039: `uses_browser_login() calls read()`
- c0082 ..> c0089: `type in uses_browser_login`
- c0083 ..> c0083: `call() calls command()`
- c0083 ..> c0083: `check() calls call()`
- c0083 ..> c0083: `check() calls command()`
- c0083 ..> c0083: `command() calls _environment()`
- c0083 ..> c0083: `create_project() calls call()`
- c0083 ..> c0083: `login() calls _environment()`
- c0083 ..> c0083: `projects() calls command()`
- c0083 ..> c0084: `_environment() calls role_environment()`
- c0083 ..> c0084: `check() calls _catalog_tools()`
- c0083 ..> c0089: `type in _environment`
- c0083 ..> c0089: `type in call`
- c0083 ..> c0089: `type in check`
- c0083 ..> c0089: `type in command`
- c0083 ..> c0089: `type in create_project`
- c0083 ..> c0089: `type in login`
- c0083 ..> c0089: `type in projects`
- c0083 ..> c0099: `check() constructs FactoryError`
- c0083 ..> c0099: `command() constructs FactoryError`
- c0083 ..> c0099: `create_project() constructs FactoryError`
- c0083 ..> c0099: `login() constructs FactoryError`
- c0083 ..> c0099: `projects() constructs FactoryError`
- c0083 ..> c0104: `command() calls run_owned()`
- c0083 ..> c0104: `login() calls run_owned()`
- c0083 ..> c0107: `command() calls check_watch_stop()`
- c0084 ..> c0044: `role_environment() calls update()`
- c0084 ..> c0089: `type in role_environment`
- c0084 ..> c0100: `role_environment() calls executable_path()`
- c0085 ..> c0085: `absent() calls _required()`
- c0085 ..> c0085: `absent() calls _selected()`
- c0085 ..> c0085: `describe() calls _python()`
- c0085 ..> c0085: `install() calls _python()`
- c0085 ..> c0085: `unready() calls _required()`
- c0085 ..> c0085: `unready() calls _selected()`
- c0085 ..> c0089: `type in __init__`
- c0085 ..> c0099: `_python() constructs FactoryError`
- c0085 ..> c0100: `_selected() calls executable_path()`
- c0085 ..> c0101: `_python() calls check_uv()`
- c0085 ..> c0101: `_python() calls install_environment()`
- c0085 ..> c0101: `install() calls install_locks()`
- c0085 ..> c0101: `install() calls no_installer()`
- c0085 ..> c0101: `install() calls require_manager()`
- c0085 ..> c0101: `install() calls run_install()`
- c0085 ..> c0101: `unready() calls runtime_ready()`
- c0085 ..> c0104: `_python() calls run_owned()`
- c0086 ..> c0071: `check() calls check()`
- c0086 ..> c0083: `__init__() constructs AgentForgetfulConnection`
- c0086 ..> c0083: `_call() calls call()`
- c0086 ..> c0086: `_read() calls _call()`
- c0086 ..> c0086: `_task() calls _read()`
- c0086 ..> c0086: `create_plan() calls _call()`
- c0086 ..> c0086: `create_task() calls _call()`
- c0086 ..> c0086: `get_plan() calls _read()`
- c0086 ..> c0086: `plans() calls _read()`
- c0086 ..> c0086: `plans() calls _rows()`
- c0086 ..> c0086: `tasks() calls _read()`
- c0086 ..> c0086: `tasks() calls _rows()`
- c0086 ..> c0086: `tasks() calls _task()`
- c0086 ..> c0086: `update_plan() calls _call()`
- c0086 ..> c0086: `update_task() calls _call()`
- c0086 ..> c0087: `_rows() calls _positive_id()`
- c0086 ..> c0087: `_task() calls _positive_id()`
- c0086 ..> c0087: `get_plan() calls _positive_id()`
- c0086 ..> c0089: `type in __init__`
- c0086 ..> c0092: `_read() constructs PlanningReadError`
- c0086 ..> c0092: `_rows() constructs PlanningReadError`
- c0086 ..> c0092: `_task() constructs PlanningReadError`
- c0086 ..> c0092: `get_plan() constructs PlanningReadError`
- c0088 ..> c0071: `check() calls check()`
- c0088 ..> c0082: `uses_browser_login() calls uses_browser_login()`
- c0088 ..> c0083: `_native() constructs AgentForgetfulConnection`
- c0088 ..> c0083: `create_project() calls create_project()`
- c0088 ..> c0083: `login() calls login()`
- c0088 ..> c0083: `projects() calls projects()`
- c0088 ..> c0083: `type in _native`
- c0088 ..> c0088: `check() calls _native()`
- c0088 ..> c0088: `create_project() calls _native()`
- c0088 ..> c0088: `login() calls _native()`
- c0088 ..> c0088: `projects() calls _native()`
- c0088 ..> c0089: `type in check`
- c0088 ..> c0089: `type in create_project`
- c0088 ..> c0089: `type in login`
- c0088 ..> c0089: `type in prepare`
- c0088 ..> c0089: `type in projects`
- c0088 ..> c0089: `type in uses_browser_login`
- c0089 ..> c0089: `validate() calls _validate_server()`
- c0089 ..> c0090: `_validate_server() calls loopback_host()`
- c0089 ..> c0099: `_validate_server() constructs FactoryError`
- c0089 ..> c0099: `validate() constructs FactoryError`
- c0089 ..> c0105: `_validate_server() calls nonblank()`
- c0089 ..> c0105: `validate() calls nonblank()`
- c0090 ..> c0089: `connection_from_mapping() calls validate()`
- c0090 ..> c0089: `connection_from_mapping() constructs ForgetfulConnection`
- c0090 ..> c0089: `type in connection_from_mapping`
- c0090 ..> c0099: `connection_from_mapping() constructs FactoryError`
- c0092 --|> c0099: `inherits`
- c0093 ..> c0089: `type in check`
- c0093 ..> c0089: `type in create_project`
- c0093 ..> c0089: `type in login`
- c0093 ..> c0089: `type in prepare`
- c0093 ..> c0089: `type in projects`
- c0093 ..> c0089: `type in uses_browser_login`
- c0094 ..> c0005: `enter() calls run()`
- c0094 ..> c0099: `enter() constructs FactoryError`
- c0095 ..> c0096: `describe() calls ubuntu_tmux()`
- c0095 ..> c0096: `install() calls ubuntu_tmux()`
- c0095 ..> c0099: `install() constructs FactoryError`
- c0095 ..> c0100: `absent() calls executable_path()`
- c0095 ..> c0101: `install() calls no_installer()`
- c0095 ..> c0101: `install() calls run_install()`
- c0098 ..> c0005: `run_command() calls run()`
- c0098 ..> c0099: `run_command() constructs FactoryError`
- c0098 ..> c0107: `run_command() calls check_watch_stop()`
- c0101 ..> c0039: `install_locks() calls read()`
- c0101 ..> c0099: `check_uv() constructs FactoryError`
- c0101 ..> c0099: `install_locks() constructs FactoryError`
- c0101 ..> c0099: `no_installer() constructs FactoryError`
- c0101 ..> c0099: `require_manager() constructs FactoryError`
- c0101 ..> c0099: `run_install() constructs FactoryError`
- c0101 ..> c0099: `type in no_installer`
- c0101 ..> c0101: `check_uv() calls install_environment()`
- c0101 ..> c0101: `install_locks() calls sync_fingerprint()`
- c0101 ..> c0101: `run_install() calls install_environment()`
- c0101 ..> c0101: `runtime_ready() calls sync_fingerprint()`
- c0101 ..> c0102: `install_locks() calls write_new()`
- c0101 ..> c0104: `check_uv() calls run_owned()`
- c0101 ..> c0104: `run_install() calls run_owned()`
- c0101 ..> c0104: `runtime_ready() calls run_owned()`
- c0102 ..> c0000: `_generated_parent() calls close()`
- c0102 ..> c0000: `check_skill_file() calls close()`
- c0102 ..> c0037: `read_generated_json() calls load()`
- c0102 ..> c0039: `replace_generated_json() calls write()`
- c0102 ..> c0039: `write_new() calls write()`
- c0102 ..> c0099: `_generated_parent() constructs FactoryError`
- c0102 ..> c0099: `check_real_path() constructs FactoryError`
- c0102 ..> c0099: `check_skill_file() constructs FactoryError`
- c0102 ..> c0099: `read_generated_json() constructs FactoryError`
- c0102 ..> c0099: `write_definition() constructs FactoryError`
- c0102 ..> c0099: `write_new() constructs FactoryError`
- c0102 ..> c0102: `_generated_parent() calls check_real_path()`
- c0102 ..> c0102: `check_skill_file() calls check_real_path()`
- c0102 ..> c0102: `read_generated_json() calls _generated_parent()`
- c0102 ..> c0102: `remove_generated() calls _generated_parent()`
- c0102 ..> c0102: `replace_generated_json() calls _generated_parent()`
- c0102 ..> c0102: `write_definition() calls read_generated_json()`
- c0102 ..> c0102: `write_definition() calls write_json()`
- c0102 ..> c0102: `write_json() calls write_new()`
- c0102 ..> c0102: `write_new() calls check_real_path()`
- c0104 ..> c0000: `_close_capture_streams() calls close()`
- c0104 ..> c0000: `_terminate_owned_process() calls wait()`
- c0104 ..> c0099: `run_owned() constructs FactoryError`
- c0104 ..> c0104: `_terminate_owned_process() calls _close_capture_streams()`
- c0104 ..> c0104: `run_owned() calls _terminate_owned_process()`
- c0104 ..> c0107: `run_owned() calls check_watch_stop()`
- c0105 ..> c0099: `nonblank() constructs FactoryError`
- c0107 ..> c0106: `watch_stop_scope() constructs WatchStop`
- c0108 ..> c0098: `_api() calls run_command()`
- c0108 ..> c0098: `check_ready() calls run_command()`
- c0108 ..> c0099: `_api() constructs FactoryError`
- c0108 ..> c0099: `_comments() constructs FactoryError`
- c0108 ..> c0099: `_validate_issue() constructs FactoryError`
- c0108 ..> c0099: `check_access() constructs FactoryError`
- c0108 ..> c0099: `check_ready() constructs FactoryError`
- c0108 ..> c0099: `create_label() constructs FactoryError`
- c0108 ..> c0099: `list_labels() constructs FactoryError`
- c0108 ..> c0099: `list_open() constructs FactoryError`
- c0108 ..> c0099: `validate_source() constructs FactoryError`
- c0108 ..> c0108: `_comments() calls _api()`
- c0108 ..> c0108: `_ticket() calls _comments()`
- c0108 ..> c0108: `_ticket() calls _milestone()`
- c0108 ..> c0108: `check_access() calls _api()`
- c0108 ..> c0108: `create_label() calls _api()`
- c0108 ..> c0108: `list_labels() calls _api()`
- c0108 ..> c0108: `list_open() calls _api()`
- c0108 ..> c0108: `list_open() calls _ticket()`
- c0108 ..> c0108: `list_open() calls _validate_issue()`
- c0108 ..> c0109: `list_labels() constructs Label`
- c0108 ..> c0109: `type in create_label`
- c0108 ..> c0109: `type in list_labels`
- c0108 ..> c0110: `_ticket() constructs Ticket`
- c0108 ..> c0110: `type in _ticket`
- c0108 ..> c0110: `type in list_open`
- c0108 ..> c0111: `type in _api`
- c0108 ..> c0111: `type in _comments`
- c0108 ..> c0111: `type in _ticket`
- c0108 ..> c0111: `type in _validate_issue`
- c0108 ..> c0111: `type in check_access`
- c0108 ..> c0111: `type in create_label`
- c0108 ..> c0111: `type in list_labels`
- c0108 ..> c0111: `type in list_open`
- c0108 ..> c0111: `type in validate_source`
- c0110 --> c0111: `field source`
- c0112 ..> c0109: `type in create_label`
- c0112 ..> c0109: `type in list_labels`
- c0112 ..> c0110: `type in list_open`
- c0112 ..> c0111: `type in check_access`
- c0112 ..> c0111: `type in create_label`
- c0112 ..> c0111: `type in list_labels`
- c0112 ..> c0111: `type in list_open`
- c0112 ..> c0111: `type in validate_source`
- c0113 ..> c0098: `origin() calls run_command()`
- c0113 ..> c0099: `origin() constructs FactoryError`
- c0113 ..> c0114: `origin() calls _resolve_repository()`
- c0114 ..> c0099: `_resolve_repository() constructs FactoryError`
- c0115 ..> c0039: `ensure() calls write()`
- c0115 ..> c0041: `_network_git() calls quote()`
- c0115 ..> c0054: `begin_cleanup_cycle() calls clear()`
- c0115 ..> c0098: `_dispose() calls run_command()`
- c0115 ..> c0098: `_network_git() calls run_command()`
- c0115 ..> c0098: `_read_git() calls run_command()`
- c0115 ..> c0098: `ensure() calls run_command()`
- c0115 --> c0099: `field cleanup_defaults`
- c0115 ..> c0099: `ensure() constructs FactoryError`
- c0115 ..> c0107: `ensure() calls check_watch_stop()`
- c0115 ..> c0115: `_disposal_state() calls _repository_entries()`
- c0115 ..> c0115: `_disposal_state() calls _validate_disposal_origin()`
- c0115 ..> c0115: `_disposal_state() calls _validate_disposal_path()`
- c0115 ..> c0115: `_disposal_state() calls _validate_disposal_refs()`
- c0115 ..> c0115: `_disposal_state() calls _validate_registered_worktree()`
- c0115 ..> c0115: `_dispose() calls _disposal_state()`
- c0115 ..> c0115: `_dispose() calls _network_git()`
- c0115 ..> c0115: `_dispose() calls _network_read()`
- c0115 ..> c0115: `_dispose() calls _read_git()`
- c0115 ..> c0115: `_dispose() calls _repository_entries()`
- c0115 ..> c0115: `_dispose() calls _verify_local_ref_absent()`
- c0115 ..> c0115: `_inspect() calls _read_git()`
- c0115 ..> c0115: `_inspect() calls _repository_entries()`
- c0115 ..> c0115: `_inspect() calls _validate_registered_worktree()`
- c0115 ..> c0115: `_network_git() calls _read_git()`
- c0115 ..> c0115: `_network_read() calls _network_git()`
- c0115 ..> c0115: `_remote_default() calls _network_read()`
- c0115 ..> c0115: `_repository_entries() calls _read_git()`
- c0115 ..> c0115: `_validate_common_directory() calls _read_git()`
- c0115 ..> c0115: `_validate_disposal_origin() calls _read_git()`
- c0115 ..> c0115: `_validate_disposal_path() calls _read_git()`
- c0115 ..> c0115: `_validate_disposal_refs() calls _read_git()`
- c0115 ..> c0115: `_validate_disposal_refs() calls _remote_default()`
- c0115 ..> c0115: `_validate_registered_worktree() calls _validate_common_directory()`
- c0115 ..> c0115: `_validate_registered_worktree() calls _validate_registration()`
- c0115 ..> c0115: `_validate_registered_worktree() calls _validate_target_identity()`
- c0115 ..> c0115: `_validate_target_identity() calls _read_git()`
- c0115 ..> c0115: `_verify_local_ref_absent() calls _read_git()`
- c0115 ..> c0115: `_verify_removed() calls _repository_entries()`
- c0115 ..> c0115: `dispose() calls _dispose()`
- c0115 ..> c0115: `ensure() calls _inspect()`
- c0115 ..> c0115: `inspect() calls _inspect()`
- c0115 ..> c0115: `repository_identity() calls _read_git()`
- c0115 ..> c0115: `target_branch() calls _read_git()`
- c0115 ..> c0115: `verify_removed() calls _verify_removed()`
- c0115 ..> c0116: `_repository_entries() calls _worktree_entries()`
- c0115 ..> c0118: `_disposal_state() constructs WorktreeProblem`
- c0115 ..> c0118: `_dispose() constructs WorktreeProblem`
- c0115 ..> c0118: `_inspect() constructs WorktreeProblem`
- c0115 ..> c0118: `_network_read() constructs WorktreeProblem`
- c0115 ..> c0118: `_repository_entries() constructs WorktreeProblem`
- c0115 ..> c0118: `_validate_common_directory() constructs WorktreeProblem`
- c0115 ..> c0118: `_validate_disposal_origin() constructs WorktreeProblem`
- c0115 ..> c0118: `_validate_disposal_path() constructs WorktreeProblem`
- c0115 ..> c0118: `_validate_disposal_refs() constructs WorktreeProblem`
- c0115 ..> c0118: `_validate_registration() constructs WorktreeProblem`
- c0115 ..> c0118: `_validate_target_identity() constructs WorktreeProblem`
- c0115 ..> c0118: `_verify_local_ref_absent() constructs WorktreeProblem`
- c0115 ..> c0118: `_verify_removed() constructs WorktreeProblem`
- c0115 ..> c0118: `dispose() constructs WorktreeProblem`
- c0115 ..> c0119: `_read_git() constructs WorktreeReadError`
- c0115 ..> c0119: `ensure() constructs WorktreeReadError`
- c0115 ..> c0119: `inspect() constructs WorktreeReadError`
- c0115 ..> c0119: `repository_identity() constructs WorktreeReadError`
- c0115 ..> c0119: `target_branch() constructs WorktreeReadError`
- c0115 ..> c0119: `verify_removed() constructs WorktreeReadError`
- c0118 ..> c0000: `__init__() calls __init__()`
- c0118 --|> c0099: `inherits`
- c0119 --|> c0099: `inherits`

## Type key

- Type1: `object | None`
- Type2: `int | None`
- Type3: `str | None`
- Type4: `tuple[Path, Path, int]`
- Type5: `dict | None`
- Type6: `dict[str, str]`
- Type7: `tuple[Path, Path]`
- Type8: `dict[str, str] | None`
- Type9: `subprocess.Popen | None`
- Type10: `Callable[[ForgetfulConnection, str], dict[str, str]]`
- Type11: `Callable[[ForgetfulConnection], list[str]]`
- Type12: `dict[tuple[str, Path], list[str]]`
- Type13: `bool | None`
- Type14: `Path | None`
- Type15: `dict[str, bytes]`
- Type16: `tuple[str, ...]`
- Type17: `dict[Path, None]`
- Type18: `frozenset[tuple[int, int]]`
- Type19: `Callable[[str], bool]`
- Type20: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type21: `list[Path] | None`
- Type22: `ForgetfulConnection | None`
- Type23: `list[str] | tuple[str, ...]`
- Type24: `int | dict`
- Type25: `int | dict | str`
- Type26: `str | Path`
- Type27: `FactoryConfiguration | None`
- Type28: `tuple[int, int]`
- Type29: `Iterator[PlainWatchObservation | None]`
- Type30: `Callable[[str], None]`
- Type31: `tuple[RepositoryReference, ...]`
- Type32: `tuple[int, ...] | None`
- Type33: `'CleanupSet'`
- Type34: `dict[int, int]`
- Type35: `tuple | None`
- Type36: `tuple[dict, dict] | None`
- Type37: `dict[int, list[dict]]`
- Type38: `list[dict] | None`
- Type39: `list[CompletedWork] | None`
- Type40: `CleanupState | None`
- Type41: `Callable[[str], str]`
- Type42: `Callable[[ForgetfulConnection], Sequence[ToolInstaller]]`
- Type43: `Callable[[list[str]], None]`
- Type44: `Callable[[str, str], bool]`
- Type45: `list[str] | None`
- Type46: `dict[str, RepositoryReference]`
- Type47: `dict[TicketSource, tuple[Label, ...]]`
- Type48: `Callable[[], FactoryConfiguration | None]`
- Type49: `tuple[ToolInstaller | None, str | None]`
- Type50: `tuple[list[dict], list[dict]]`
- Type51: `tuple[Ticket, dict] | None`
- Type52: `Ticket | None`
- Type53: `tuple[int, ...]`
- Type54: `Callable[[], Launch]`
- Type55: `Callable[[], bool]`
- Type56: `tuple[set[str], bool]`
- Type57: `tuple[TicketSource, ...]`
- Type58: `tuple[Ticket, ...]`
- Type59: `dict[str, Ticket]`
- Type60: `BlockedWork | None`
- Type61: `tuple[Ticket, ...] | None`
- Type62: `dict[str, BlockedWork]`
- Type63: `Callable[[], dict | None]`
- Type64: `tuple[Path, ...]`
- Type65: `float | None`
- Type66: `tuple[Label, ...]`
- Type67: `list[tuple[int, str, str]]`
- Type68: `dict[str, list[str] | FactoryError]`
- Type69: `tuple[Path, list[dict]]`
- Type70: `tuple[Path, Path] | None`
- Type71: `tuple[Path, Path, dict | None]`

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
- Signature8: `-__init__(workspace: Path, python: str, deadlines: AgentShellLifecycleDeadlines,
  host: SessionHost) unknown`
- Signature9: `+start_owner(workspace: Path, python: str, environment: dict, launch: dict,
  deadlines: AgentShellLifecycleDeadlines, host: SessionHost) dict`
- Signature10: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None, model: str | None, effort: str | None, deadlines:
  AgentShellLifecycleDeadlines, host: SessionHost, channel: Channel) unknown`
- Signature11: `-__init__(workspace: Path, term_grace: float, role_environment:
  Callable[[ForgetfulConnection, str], dict[str, str]], missing_tools:
  Callable[[ForgetfulConnection], list[str]]) unknown`
- Signature12: `+validate_setup(connection: ForgetfulConnection, include_home_system_prompt: bool,
  include_memory_extension: bool) None`
- Signature13: `+prepare_roles(choices: InitialAgentChoices, execution_enabled: bool, repositories:
  Sequence[str], connection: ForgetfulConnection) None`
- Signature14: `+validate_worker_models(choices: InitialAgentChoices, repositories: Sequence[str],
  connection: ForgetfulConnection) None`
- Signature15: `-_write_agent(name: unknown, model: unknown, effort: unknown, description: unknown,
  children: unknown, resources: unknown) unknown`
- Signature16: `+build_tools(workspace: Path, connection: ForgetfulConnection, term_grace: float)
  unknown`
- Signature17: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown, deadlines: DeadlinePolicy, observation: unknown) WatchFactory`
- Signature18: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown, term_grace: float) unknown`
- Signature19: `+build_start_foreman(workspace: Path, python: str, deadlines: DeadlinePolicy)
  StartForeman`
- Signature20: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature21: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature22: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature23: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature24: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature25: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature26: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature27: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature28: `-_foreman_memory_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown, connection: ForgetfulConnection) InitialAgentChoices`
- Signature29: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature30: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature31: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int |
  dict`
- Signature32: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature33: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature34: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None, deadlines: DeadlinePolicy) int | dict`
- Signature35: `-_initialise_locked(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int | dict | str`
- Signature36: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown, deadlines: unknown) unknown`
- Signature37: `+update_resources(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int`
- Signature38: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature39: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature40: `-__init__(records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts,
  ticketing: Ticketing) unknown`
- Signature41: `-_claim_indexes(inventory: list[dict], plans: list[dict], tasks: dict[int,
  list[dict]], identities: dict[str, str], alerts: WatcherAlerts) tuple[dict, dict] | None`
- Signature42: `-_dispose(work: CompletedWork, mapping: dict, claims: dict, references: dict,
  identities: dict[str, str], alerts: WatcherAlerts, report: unknown) bool`
- Signature43: `-_mapping_identity(plan_id: int, reference: str, mapping: dict, workspace: str |
  None) CleanupSet`
- Signature44: `+agree_definition_of_done(agreement: AgreementStore, config: FactoryConfiguration,
  ask: Callable[[str], str], say: Callable[[str], None]) bool`
- Signature45: `-__init__(planning: PlanStore, workspace: Path, config: FactoryConfiguration,
  repositories: LocalRepositories, forge: Forge, ticketing: Ticketing) unknown`
- Signature46: `-__init__(tracking: Ticketing, storage: ConfigurationStore, repositories:
  LocalRepositories, forge: Forge, team: AgentTeam, planning: PlanningSetup, tools:
  Callable[[ForgetfulConnection], Sequence[ToolInstaller]]) unknown`
- Signature47: `-__init__(planning: PlanStore, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, forge: Forge, ticketing: Ticketing)
  unknown`
- Signature48: `-_setup_ownership(plan_id: int, issue: Ticket, context: dict, initial_mappings:
  list[dict]) tuple[list[dict], list[dict]]`
- Signature49: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature50: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature51: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature52: `-__init__(lease: WatchLease, owner: PersistentForeman, channel: Channel, prepare:
  Callable[[], Launch]) unknown`
- Signature53: `-__init__(tracking: Ticketing, terminal: ForemanTerminal, scaffold: ScaffoldIssue,
  cleanup: CleanupCompleted) unknown`
- Signature54: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature55: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature56: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature57: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature58: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature59: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature60: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Ticket, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature61: `-_poll_sources(sources: tuple[TicketSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature62: `-_process_source(source: TicketSource, issues: tuple[Ticket, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature63: `-_baseline_source(source: TicketSource, issues: tuple[Ticket, ...], state:
  _WatchState, report: Callable[[str], None]) None`
- Signature64: `-_repository_for_source(config: FactoryConfiguration, source: TicketSource)
  RepositoryReference`
- Signature65: `-_include_pending_lookups(source: TicketSource, current: dict[str, Ticket],
  pending_lookup: dict[str, Ticket]) None`
- Signature66: `-_process_issues(issues: tuple[Ticket, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature67: `-_process_issue(issue: Ticket, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature68: `-_handle_intake_repository_problem(issue: Ticket, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature69: `-_handle_intake_read_problem(issue: Ticket, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature70: `-_handle_intake_scaffold_problem(issue: Ticket, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature71: `-_complete_intake(issue: Ticket, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature72: `-_submit(issue: Ticket, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature73: `-__init__(plain: Callable[[], dict | None], owner: PersistentForeman, storage:
  ConfigurationStore, team: AgentTeam) unknown`
- Signature74: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature75: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool,
  term_grace: float) unknown`
- Signature76: `+run_install(args: list[str], cwd: Path, term_grace: float, interactive: bool,
  extra_env: dict[str, str] | None) str`
- Signature77: `+run_owned(args: list[str], cwd: Path, env: dict[str, str], login: bool, timeout:
  float | None, term_grace: float) str`
- Signature78: `-_validate_registered_worktree(root: Path, target: Path, branch: str, path: str,
  match: dict) None`
- Signature79: `-_disposal_state(repository: str, branch: str, path: str, remote: str,
  target_branch: str) tuple[Path, Path, dict | None]`

## Extraction warnings

- `Unresolved or out-of-scope base: AgentTeam -> Protocol`
- `Unresolved or out-of-scope base: AgreementStore -> Protocol`
- `Unresolved or out-of-scope base: Channel -> Protocol`
- `Unresolved or out-of-scope base: CleanupMarkerError -> ValueError`
- `Unresolved or out-of-scope base: CleanupReceipts -> Protocol`
- `Unresolved or out-of-scope base: ConfigurationStore -> Protocol`
- `Unresolved or out-of-scope base: FactoryError -> Exception`
- `Unresolved or out-of-scope base: ForemanTerminal -> Protocol`
- `Unresolved or out-of-scope base: Forge -> Protocol`
- `Unresolved or out-of-scope base: LocalRepositories -> Protocol`
- `Unresolved or out-of-scope base: PersistentForeman -> Protocol`
- `Unresolved or out-of-scope base: PlanStore -> Protocol`
- `Unresolved or out-of-scope base: PlanningSetup -> Protocol`
- `Unresolved or out-of-scope base: SessionHost -> Protocol`
- `Unresolved or out-of-scope base: Ticketing -> Protocol`
- `Unresolved or out-of-scope base: ToolInstaller -> Protocol`
- `Unresolved or out-of-scope base: WatchLease -> Protocol`
- `Unresolved or out-of-scope base: Worktrees -> Protocol`
- `Unresolved or out-of-scope base: _WorkAction -> Enum`
