# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 137 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 5990. Type relationships removed: 125.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/contracts/agents.py`: 15 source occurrences (test-path).
- `tests/contracts/channels.py`: 16 source occurrences (test-path).
- `tests/contracts/factory.py`: 5 source occurrences (test-path).
- `tests/contracts/forge.py`: 12 source occurrences (test-path).
- `tests/contracts/planning.py`: 16 source occurrences (test-path).
- `tests/contracts/runtime.py`: 6 source occurrences (test-path).
- `tests/contracts/ticketing.py`: 31 source occurrences (test-path).
- `tests/contracts/tools.py`: 7 source occurrences (test-path).
- `tests/deadline_support.py`: 2 source occurrences (test-path).
- `tests/fake_discord.py`: 50 source occurrences (test-path).
- `tests/fixtures/previous-pi-forgetful-factory.ts`: 18 source occurrences (test-path).
- `tests/lifecycle_support.py`: 21 source occurrences (test-path).
- `tests/poll_support.py`: 9 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_agent_definitions.py`: 21 source occurrences (test-path).
- `tests/test_agent_team_contract.py`: 5 source occurrences (test-path).
- `tests/test_agreement_contract.py`: 4 source occurrences (test-path).
- `tests/test_architecture.py`: 35 source occurrences (test-path).
- `tests/test_assisted_lifecycle.py`: 16 source occurrences (test-path).
- `tests/test_assisted_review_fixes.py`: 20 source occurrences (test-path).
- `tests/test_assisted_setup.py`: 14 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_channel_contract.py`: 3 source occurrences (test-path).
- `tests/test_chat_relay.py`: 47 source occurrences (test-path).
- `tests/test_cleanup_boundaries.py`: 19 source occurrences (test-path).
- `tests/test_cleanup_damaged_reference.py`: 5 source occurrences (test-path).
- `tests/test_cleanup_performance.py`: 28 source occurrences (test-path).
- `tests/test_cleanup_receipts.py`: 30 source occurrences (test-path).
- `tests/test_cleanup_recovery.py`: 12 source occurrences (test-path).
- `tests/test_cleanup_review.py`: 25 source occurrences (test-path).
- `tests/test_cleanup_scheduling.py`: 5 source occurrences (test-path).
- `tests/test_completed_cleanup.py`: 30 source occurrences (test-path).
- `tests/test_completed_cleanup_recovery.py`: 28 source occurrences (test-path).
- `tests/test_configuration.py`: 23 source occurrences (test-path).
- `tests/test_controller_replies.py`: 17 source occurrences (test-path).
- `tests/test_definition_of_done.py`: 12 source occurrences (test-path).
- `tests/test_definition_of_done_lifecycle.py`: 3 source occurrences (test-path).
- `tests/test_definition_of_done_watch.py`: 2 source occurrences (test-path).
- `tests/test_discord_api.py`: 6 source occurrences (test-path).
- `tests/test_discord_link.py`: 25 source occurrences (test-path).
- `tests/test_discord_relay.py`: 31 source occurrences (test-path).
- `tests/test_discord_watch.py`: 20 source occurrences (test-path).
- `tests/test_env_file.py`: 11 source occurrences (test-path).
- `tests/test_factory_launcher.py`: 10 source occurrences (test-path).
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
- `tests/test_runtime_host.py`: 14 source occurrences (test-path).
- `tests/test_saved_data.py`: 14 source occurrences (test-path).
- `tests/test_second_provider.py`: 8 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 24 source occurrences (test-path).
- `tests/test_ticketing.py`: 22 source occurrences (test-path).
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
        +wait(interval: float) list[ForemanReply]
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
    class c0002["_UncachedLoader"] {
        <<class>>
        +set_data(path: unknown, data: unknown, _mode: unknown) unknown
    }
    class c0003["src/forgetful_factory/agents/adapters/agentshell/controller.py"] {
        <<module>>
        +ready(session: unknown) None
        +forward_replies(session: unknown, reply: unknown) None
        +interact(Signature1)
        +become_ready(session: unknown, name: unknown, deadlines: unknown) None
        +send_line(Signature2)
        +worker_exited(descriptor: unknown) None
        +resume_exit_observation(session: unknown) int
        +runtime() unknown
        +load_host(kind: str) unknown
        +validate_launch_config(config: unknown) None
        +build_shell(config: unknown) unknown
        +open_session(Signature3)
        +capture_worker(state: unknown, reply: unknown) None
        +replace_failed_exit_task(Signature4)
        +cancel_tasks(tasks: unknown) None
        +supervise_session(Signature5)
        +close_session(state: unknown, config: unknown, reply: unknown) None
        +serve(reader: unknown, config: unknown, reply: unknown, opened: unknown) None
        +control(reply: unknown) None
        +main(reply: unknown) int
        +reply(value: unknown) unknown
    }
    class c0004["src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
        +factory_launcher(workspace: Path, python: str) Path
    }
    class c0005["src/forgetful_factory/agents/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0006["ForemanOwner"] {
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
        -_remove_control_socket(Signature6)
        -_cleanup(Signature7)
        +run(handover: unknown, endpoint: unknown) unknown
    }
    class c0007["src/forgetful_factory/agents/adapters/agentshell/owner.py"] {
        <<module>>
        -_validate_target(target: unknown) None
        -_controller_event(line: bytes) dict
        -_watcher_request(line: bytes) dict
        -_acquire_owner_lock(directory: Path, workspace: Path) int
        -_prepare_owner_startup(workspace: Path) Type4
        +main(Signature8)
        -_report_startup_error(handover: unknown, error: unknown) None
        +entrypoint() None
    }
    class c0008["AgentShellOwner"] {
        <<class>>
        -__init__(Signature9)
        +workspace: unknown
        +python: unknown
        +deadlines: unknown
        +host: unknown
        +saved() Type5
        +status() dict
        +start(environment: Type6, launch: dict) dict
        +report() Type5
    }
    class c0009["src/forgetful_factory/agents/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type5
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(Signature10)
    }
    class c0010["AgentShellRuntimeInstall"] {
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
    class c0011["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature11)
        +python: unknown
        +replies: unknown
        +received: list[ForemanReply]
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
        -_receive() None
        -_take() Type5
        -_expect(reply: dict, expected: str) dict
        -_read(timeout: float, expected: str) dict
        +start() None
        +send(message: str) None
        +wait(interval: float) list[ForemanReply]
        +close() None
    }
    class c0012["src/forgetful_factory/agents/adapters/agentshell/tmux_host.py"] {
        <<module>>
        +retain_identity(session: unknown, reply: unknown) None
        +pin_worker(target: unknown) int
    }
    class c0013["src/forgetful_factory/agents/adapters/pi/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        -_local_selection(value: object, field: str, message: str) str
        -_validate_agent(value: object) dict
        -_validate_roster(path: Path, value: object, agent_type: str) None
        -_validate_resources(value: object) None
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0014["PiAgentTeam"] {
        <<class>>
        -__init__(Signature12)
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
        +validate_setup(Signature13)
        +validate_bundled_resources(include_memory_extension: bool) None
        -_install_resources() None
        -_protect_runtime() None
        +prepare() None
        +save_pi_choice() None
        +prepare_roles(Signature14)
        +validate_worker_models(Signature15)
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
    class c0015["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(execution_enabled: bool, choices: unknown) None
        -_write_foreman_memory(choices: unknown) None
        -_write_agent(Signature16)
        +validate_guidance(execution_enabled: bool) None
    }
    class c0016["src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0017["src/forgetful_factory/agents/adapters/pi/native_home.py"] {
        <<module>>
        +saved_pi_home(workspace: Path) str
    }
    class c0018["ResourceUpdate"] {
        <<class>>
        +directory: Path
        +files: Type15
        +add: Type16
        +replace: Type16
        +edited: Type16
    }
    class c0019["src/forgetful_factory/agents/adapters/pi/role_resources.py"] {
        <<module>>
        -_digest(data: bytes) str
        +bundled_files() Type15
        +plan_update(directory: Path) ResourceUpdate
        -_back_up(update: ResourceUpdate, backups: Path) Path
        +apply_update(update: ResourceUpdate, backups: Path) Type14
    }
    class c0020["PiInstall"] {
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
    class c0021["src/forgetful_factory/agents/adapters/pi/selected_skills.py"] {
        <<module>>
        -_add_skill_file(path: Path, files: Type17) None
        -_walk_skill_directory(directory: Path, ancestors: Type18, files: Type17) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0022["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0023["AgentShellLifecycleDeadlines"] {
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
    class c0024["ForemanReply"] {
        <<class>>
        +text: str
        +error: Type3
    }
    class c0025["InitialAgentChoices"] {
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
    class c0026["src/forgetful_factory/agents/model.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type16
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
        +unknown_status(source: str, observation: str) dict
    }
    class c0027["AgentTeam"] {
        <<class>>
        +prepare() None
        +prepare_setup_guidance() None
        +choose_pi_home(requested: Type3, confirm: Type19) str
        +save_pi_choice() None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type14) list[str]
        +prepare_roles(Signature14)
        +selected_launch(agent_file: str, connection: ForgetfulConnection) dict
        +managed_memory_notice() Type3
        +begin_setup() None
        +record_completion(agent_file: str, connection: ForgetfulConnection) bool
        +validate_completion() None
        +validate_bundled_resources(include_memory_extension: bool) None
    }
    class c0028["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) list[ForemanReply]
        +close() None
    }
    class c0029["PersistentForeman"] {
        <<class>>
        +saved() Type5
        +status() dict
        +report() Type5
        +start(environment: Type6, launch: dict) dict
    }
    class c0030["DiscordLink"] {
        <<class>>
        +name: unknown
        -__init__(Signature17)
        +settings: unknown
        +env_file: unknown
        +explicit_env_file: unknown
        +warn: unknown
        +command: unknown
        +environment: unknown
        +close_wait: unknown
        +process: Type9
        +connection: Type23
        +outgoing: unknown
        +incoming: unknown
        +inbox: list[ChatMessage]
        +finished: unknown
        +start() None
        +online() None
        +post(text: str) None
        +mark(message_id: str, delivery: Delivery) None
        +receive() list[ChatMessage]
        +close(reason: str) None
        -_send(value: dict) None
        -_pump() None
        -_read(data: bytes) bool
        -_lost() None
        -_end(deadline: float) Type2
    }
    class c0031["Relay"] {
        <<class>>
        -__init__(discord: unknown, reader: unknown, writer: unknown, start: dict) unknown
        +discord: unknown
        +reader#44; self.writer: unknown
        +token: unknown
        +variable: unknown
        +channel_id: unknown
        +allowed: unknown
        +client: unknown
        +channel: unknown
        +ready: unknown
        +ready_at: unknown
        +outbox: asyncio.Queue
        +stopped: unknown
        +unmarked: set[int]
        +reported: set[str]
        +tell(value: dict) None
        +problem(text: str, key: Type3, fatal: bool) None
        +run() int
        +connect() None
        +connected(client: unknown) None
        +listen() None
        +stop() None
        +addressed(message: unknown) bool
        +received(message: unknown) None
        +post() None
        +send(text: str) None
        +react(message_id: int, emoji: str) None
        +count_missed() None
    }
    class c0032["src/forgetful_factory/channels/adapters/discord/relay.py"] {
        <<module>>
        +split_reply(text: str) list[str]
        +intents(discord: unknown) unknown
        +client_type(discord: unknown) unknown
        +serve(connection: socket.socket) int
        +main(argv: list[str]) int
    }
    class c0033["TerminalChannel"] {
        <<class>>
        -__init__(host: SessionHost) unknown
        +host: unknown
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0034["ChatMessage"] {
        <<class>>
        +id: str
        +author: str
        +text: str
    }
    class c0035["Delivery"] {
        <<class>>
        +SENT: unknown
        +UNCERTAIN: unknown
        +NOT_READY: unknown
    }
    class c0036["DiscordSettings"] {
        <<class>>
        +channel_id: str
        +allowed_users: Type16
        +token_variable: str
    }
    class c0037["src/forgetful_factory/channels/model.py"] {
        <<module>>
        +discord_from_mapping(data: object) DiscordSettings
        +secret_names(settings: Type24) Type16
    }
    class c0038["Channel"] {
        <<class>>
        +how_to_reach(session_name: str) str
        +open(target: dict) None
    }
    class c0039["ChatChannel"] {
        <<class>>
        +name: str
        +start() None
        +online() None
        +post(text: str) None
        +receive() list[ChatMessage]
        +mark(message_id: str, delivery: Delivery) None
        +close(reason: str) None
    }
    class c0040["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_host() TmuxHost
        +build_channel() TerminalChannel
        +build_owner(workspace: Path, python: str, deadlines: DeadlinePolicy) AgentShellOwner
        +build_tools(Signature18)
        +build_team(workspace: Path, term_grace: float) PiAgentTeam
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +select_ticketing(config: FactoryConfiguration, command_timeout: float) Ticketing
        -_warn(message: str) None
        +build_chat(config: FactoryConfiguration, warn: Type20) Type25
        +build_watcher(Signature19)
        +prepare_foreman_launch(Signature20)
        +build_watch_status(workspace: Path, python: str, deadlines: DeadlinePolicy) WatchStatus
        +build_start_foreman(Signature21)
    }
    class c0041["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0042["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0043["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature22)
        -_check_existing_connection(Signature23)
        -_connection(Signature24)
        -_prepare_foreman(Signature25)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type29, show_choices: bool, prompt: Type3) str
        -_select_model(Signature26)
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
        -_select_project(Signature27)
        -_owner_choices(Signature28)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature29)
        -_foreman_memory_choices(Signature30)
        -_managed_rest_mapping_available(connection: ForgetfulConnection) bool
        -_worker_choices(Signature31)
        -_complete_setup(Signature32)
        -_initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type5) None
        -_finish_existing_setup(Signature33)
        -_discover_worker_models(Signature34)
        -_validate_initial_model(Signature35)
        -_start_initial_setup(Signature36)
        -_initialise_locked(Signature37)
        -_launch_setup_foreman(Signature38)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0044["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0045["src/forgetful_factory/cli/resource_update.py"] {
        <<module>>
        -_report(update: unknown, force: bool) None
        +update_resources(Signature39)
    }
    class c0046["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type32) FactoryConfiguration
    }
    class c0047["FileCleanupReceipts"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +path: unknown
        +load() FinishedCleanup
        -_load() FinishedCleanup
        +confirm(resource: CleanupSet) None
        +confirm_plans(plans: Collection[CleanupPlan]) None
        -_save(resources: unknown, plans: unknown, problem: str) None
    }
    class c0048["src/forgetful_factory/factory/adapters/cleanup_receipts.py"] {
        <<module>>
        -_unique_object(pairs: unknown) unknown
        -_identity(value: object, kind: type, paths: Type16) unknown
        -_rows(value: dict, key: str, kind: type, paths: Type16, workspace: str) list
        -_sorted(rows: unknown) list[dict]
    }
    class c0049["MarkdownAgreement"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +location: str
        +found() bool
        +write(text: str) None
        +read() str
    }
    class c0050["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type33
        +save(configuration: FactoryConfiguration) None
    }
    class c0051["src/forgetful_factory/factory/adapters/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0052["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0053["ObservedTerminal"] {
        <<class>>
        -__init__(terminal: ForemanTerminal, observation: PlainWatchObservation) unknown
        +terminal: unknown
        +observation: unknown
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) list[ForemanReply]
        +close() None
    }
    class c0054["PlainWatchObservation"] {
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
    class c0055["src/forgetful_factory/factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type34
        -_read_discovery(workspace: Path) dict
        +plain_watch_status(workspace: Path) Type5
        +observe_plain_watch(workspace: Path, report_unavailable: Type20) Type35
    }
    class c0056["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type16
        +foreman_agent_file: str
        +repository: Type36
        +forgetful: Type28
        +execution_enabled: bool
        +env_file: Type3
        +discord: Type24
    }
    class c0057["src/forgetful_factory/factory/model/configuration.py"] {
        <<module>>
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type16
    }
    class c0058["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: TicketSource
    }
    class c0059["IntakeProblem"] {
        <<class>>
    }
    class c0060["RepositoryProblem"] {
        <<class>>
    }
    class c0061["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature40)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0062["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0063["UncertainScaffold"] {
        <<class>>
    }
    class c0064["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type6
        +last_diagnostic: Type6
        +clear(subject: str) None
        +send(Signature41)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0065["src/forgetful_factory/factory/model/watcher_problems.py"] {
        <<module>>
        -_cleanup_recovery(code: str) str
    }
    class c0066["AgreementStore"] {
        <<class>>
        +location: str
        +found() bool
        +write(text: str) None
        +read() str
    }
    class c0067["CleanupPlan"] {
        <<class>>
        +workspace: str
        +backend: str
        +plan_id: int
        +external_ref: str
    }
    class c0068["CleanupReceipts"] {
        <<class>>
        +load() FinishedCleanup
        +confirm(resource: CleanupSet) None
        +confirm_plans(plans: Collection[CleanupPlan]) None
    }
    class c0069["CleanupSet"] {
        <<class>>
        +workspace: str
        +backend: str
        +plan_id: int
        +external_ref: str
        +repository: str
        +local_dir: str
        +branch: str
        +path: str
        +overlaps(other: Type38) bool
    }
    class c0070["ConfigurationStore"] {
        <<class>>
        +load() Type33
        +save(configuration: FactoryConfiguration) None
    }
    class c0071["FinishedCleanup"] {
        <<class>>
        +sets: frozenset[CleanupSet]
        +plans: frozenset[CleanupPlan]
    }
    class c0072["ToolInstaller"] {
        <<class>>
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0073["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0074["ChatRelay"] {
        <<class>>
        -__init__(terminal: ForemanTerminal, chat: Type39, interval: float) unknown
        +terminal: unknown
        +chat: unknown
        +interval: unknown
        +lock: unknown
        +turn: unknown
        +foreman: unknown
        +thread: Type40
        +stopping: unknown
        +failed: unknown
        +failure: Type41
        +start() None
        +online() None
        +wait(interval: float) None
        +check() None
        +halt() None
        +stop(error: Type41) None
        +use_terminal(action: unknown, arguments: unknown) unknown
        -_fail(error: BaseException) None
        -_run() None
        -_exchange() None
        -_post(reply: ForemanReply) None
        -_deliver(message: ChatMessage) None
    }
    class c0075["_SharedTerminal"] {
        <<class>>
        -__init__(relay: ChatRelay) unknown
        +relay: unknown
        +terminal: unknown
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) list[ForemanReply]
        +close() None
    }
    class c0076["src/forgetful_factory/factory/services/chat_relay.py"] {
        <<module>>
        +stop_reason(error: Type41) str
    }
    class c0077["CleanupCompleted"] {
        <<class>>
        -__init__(Signature42)
        +records: unknown
        +ticketing: unknown
        +worktrees: unknown
        +owners: Type42
        +receipts: unknown
        +confirmed: set[CleanupSet]
        +finished_plans: frozenset[CleanupPlan]
        +cursor: Type43
        +poll(alerts: WatcherAlerts, report: unknown) None
        -_check_summaries(inventory: list[dict]) None
        -_references(inventory: list[dict], plans: list[dict]) Type44
        -_open(plan: dict) bool
        -_plan_identity(plan_id: int, reference: str) CleanupPlan
        -_finish_plans(Signature43)
        -_claim_indexes(Signature44)
        -_read_plans(inventory: list[dict], alerts: WatcherAlerts) Type47
        -_candidates(plans: list[dict], tasks: Type46, alerts: WatcherAlerts) Type48
        -_candidate(plan: dict, tasks: list[dict]) CompletedWork
        -_read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) None
        -_in_scope(plan: dict) bool
        -_repository_identities(alerts: WatcherAlerts) Type8
        -_keys(mapping: dict, identities: Type6) set[tuple]
        -_claims(tasks: list[dict], plan_id: int, claims: dict, identities: Type6) None
        -_task_mappings(task: dict) list[dict]
        -_validate_claim_mapping(mapping: object) None
        -_overlaps(mapping: dict, claims: dict) bool
        -_dispose(Signature45)
        -_order(work: CompletedWork, mapping: dict) tuple
        -_check_namespaces(mappings: list[dict], identities: Type6) None
        -_mapping_identity(Signature46)
        -_is_confirmed(plan_id: int, reference: str, mapping: dict, workspace: Type3) bool
        -_still_completed(work: CompletedWork) bool
    }
    class c0078["CompletedWork"] {
        <<class>>
        +plan_id: int
        +reference: str
        +task_id: int
        +mappings: list[dict]
    }
    class c0079["src/forgetful_factory/factory/services/cleanup_completed.py"] {
        <<module>>
        -_claim_path(value: str) str
    }
    class c0080["CleanupMarkerError"] {
        <<class>>
    }
    class c0081["src/forgetful_factory/factory/services/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict, forge: Forge, repository: RepositoryRef) Type49
    }
    class c0082["src/forgetful_factory/factory/services/definition_of_done.py"] {
        <<module>>
        +agree_definition_of_done(Signature47)
        -_deployment_agreement(answer: str, ask: Type50, say: Type20) str
    }
    class c0083["FactoryRecords"] {
        <<class>>
        -__init__(Signature48)
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
    class c0084["InitialiseFactory"] {
        <<class>>
        -__init__(Signature49)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +forge: unknown
        +team: unknown
        +planning: unknown
        +tools: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type52, confirm: Type53) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type27, labels: Type54) Type33
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type55
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type56
        -_ensure_label(source: TicketSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type57, save: bool) list[str]
    }
    class c0085["src/forgetful_factory/factory/services/initialise_factory.py"] {
        <<module>>
        +missing_tools(tools: Sequence[ToolInstaller]) list[str]
        -_reviewed_install(tools: Sequence[ToolInstaller], name: str) Type58
    }
    class c0086["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature50)
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
        -_setup_ownership(Signature51)
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature52)
        +lookup(issue: Ticket) Type2
        -_create_plan(issue: Ticket) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type61, task_ids: Type37) Type60
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature53)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_is_unfinished_factory_plan(summary: dict, prefixes: set[str]) bool
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_validated_mapping(Signature54)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0087["src/forgetful_factory/factory/services/scaffold_issue.py"] {
        <<module>>
        +worktree_name(ticket: Ticket) str
    }
    class c0088["StartForeman"] {
        <<class>>
        -__init__(Signature55)
        +lease: unknown
        +owner: unknown
        +channel: unknown
        +prepare: unknown
        +run(attach: bool, notify: Type20) None
    }
    class c0089["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type2
        +issue: Type61
        +task_ids: Type37
        +recovered: bool
        +setup_paths: Type16
        +setup_cause: Type3
    }
    class c0090["WatchFactory"] {
        <<class>>
        -__init__(Signature56)
        +tracking: unknown
        +relay: unknown
        +terminal: unknown
        +scaffold: unknown
        +cleanup: unknown
        +run(Signature57)
        -_watch(Signature58)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type20) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature59)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type20) Type65
        -_recover_work(Signature60)
        -_handle_recovery_repository_problem(Signature61)
        -_handle_recovery_read_problem(Signature62)
        -_remember_task_ids(work: BlockedWork, task_ids: Type37) None
        -_complete_recovery(Signature63)
        -_poll_sources(Signature64)
        -_process_source(Signature65)
        -_baseline_source(Signature66)
        -_repository_for_source(Signature67)
        -_include_pending_lookups(Signature68)
        -_process_issues(Signature69)
        -_skip_issue(issue: Ticket, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature70)
        -_handle_intake_repository_problem(Signature71)
        -_handle_intake_read_problem(Signature72)
        -_handle_intake_scaffold_problem(Signature73)
        -_complete_intake(Signature74)
        -_sole_task_id(task_ids: Type37) Type2
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature75)
        -_read_issues(source: TicketSource, labels: Type16, alerts: WatcherAlerts) Type70
    }
    class c0091["_WatchState"] {
        <<class>>
        +seen: Type6
        +baseline: Type6
        +baselined: set[TicketSource]
        +blocked: Type71
        +pending_lookup: Type68
        +known: Type71
        +recovered: set[str]
        +pending_repositories: Type55
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0092["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0093["WatchStatus"] {
        <<class>>
        -__init__(Signature76)
        +plain: unknown
        +owner: unknown
        +storage: unknown
        +team: unknown
        +report() dict
        -_without_live_plain(plain: Type5) dict
        -_setup() str
    }
    class c0094["GitHubForge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0095["RepositoryRef"] {
        <<class>>
        +forge: str
        +reference: str
    }
    class c0096["Forge"] {
        <<class>>
        +repository(remote: str) RepositoryRef
        +is_change_request(repository: RepositoryRef, url: str) bool
    }
    class c0097["src/forgetful_factory/planning/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0098["AgentForgetfulConnection"] {
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
    class c0099["src/forgetful_factory/planning/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature77)
        -_catalog_tools(catalog: object) dict
    }
    class c0100["ForgetfulInstall"] {
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
    class c0101["ForgetfulPlanStore"] {
        <<class>>
        -__init__(Signature78)
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
    class c0102["src/forgetful_factory/planning/adapters/forgetful/plan_store.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0103["ForgetfulSetup"] {
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
    class c0104["ForgetfulConnection"] {
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
    class c0105["src/forgetful_factory/planning/model.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type28
    }
    class c0106["PlanStore"] {
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
    class c0107["PlanningReadError"] {
        <<class>>
    }
    class c0108["PlanningSetup"] {
        <<class>>
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +prepare(connection: ForgetfulConnection) None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection, execution_enabled: bool) str
    }
    class c0109["TmuxHost"] {
        <<class>>
        +spec() dict
        +how_to_attach(session_name: str) str
        +enter(target: dict) None
    }
    class c0110["TmuxInstall"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +term_grace: unknown
        +absent() list[str]
        +unready() list[str]
        +describe(name: str) Type3
        +install(name: str) None
    }
    class c0111["src/forgetful_factory/runtime/adapters/tmux.py"] {
        <<module>>
        +ubuntu_tmux() bool
    }
    class c0112["SessionHost"] {
        <<class>>
        +spec() dict
        +how_to_attach(session_name: str) str
        +enter(target: dict) None
    }
    class c0113["src/forgetful_factory/shared/command.py"] {
        <<module>>
        +run_command(arguments: list[str], timeout: float, env: Type8, stdin: Type2) str
    }
    class c0114["src/forgetful_factory/shared/env_file.py"] {
        <<module>>
        +read_env_file(path: Path) Type6
        +find_secret(name: str, env_file: Path, explicit: bool, environment: Type22) Type73
    }
    class c0115["FactoryError"] {
        <<class>>
    }
    class c0116["src/forgetful_factory/shared/executables.py"] {
        <<module>>
        +executable_path(workspace: Path) str
    }
    class c0117["src/forgetful_factory/shared/installation.py"] {
        <<module>>
        +sync_fingerprint(inputs: Type74) str
        +runtime_ready(runtime: Path, inputs: Type74, probe: str, term_grace: float) bool
        +install_environment(extra: Type8) Type6
        +run_install(Signature79)
        +check_uv(workspace: Path, term_grace: float) None
        +require_manager(manager: str) None
        +install_locks(directory: Path, names: Type16) str
        +no_installer() FactoryError
    }
    class c0118["src/forgetful_factory/shared/resource_files.py"] {
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
    class c0119["src/forgetful_factory/shared/resources.py"] {
        <<module>>
        +resource_root() Path
    }
    class c0120["src/forgetful_factory/shared/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen, term_grace: float) None
        +run_owned(Signature80)
    }
    class c0121["src/forgetful_factory/shared/validation.py"] {
        <<module>>
        +nonblank(value: object, field: str) str
        +positive_duration(name: str, value: object) None
    }
    class c0122["WatchStop"] {
        <<class>>
        +requested: bool
        +interrupt(_signum: unknown, _frame: unknown) None
    }
    class c0123["src/forgetful_factory/shared/watch_stop.py"] {
        <<module>>
        +watch_stop_scope() unknown
        +check_watch_stop() None
    }
    class c0124["GitHubTicketing"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        +could_be_key(text: str) bool
        -_api(source: TicketSource, suffix: str, #42;arguments: str) object
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type76
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type16) Type67
        -_ticket(source: TicketSource, item: dict) Ticket
        -_comments(source: TicketSource, number: int) Type77
        -_milestone(item: object) object
        -_validate_issue(source: TicketSource, item: dict) None
    }
    class c0125["Label"] {
        <<class>>
        +name: str
    }
    class c0126["Ticket"] {
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
    class c0127["TicketSource"] {
        <<class>>
        +provider: str
        +reference: str
        +id_prefix: str
    }
    class c0128["Ticketing"] {
        <<class>>
        +check_ready() None
        +validate_source(source: TicketSource) None
        +is_key(text: str) bool
        +could_be_key(text: str) bool
        +check_access(source: TicketSource) None
        +list_labels(source: TicketSource) Type76
        +create_label(source: TicketSource, label: Label) None
        +list_open(source: TicketSource, labels: Type16) Type67
    }
    class c0129["GitRepositories"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0130["src/forgetful_factory/workspace/adapters/git/repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0131["GitWorktrees"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +cleanup_defaults: Type78
        +begin_cleanup_cycle() None
        +repository_identity(repository: str) str
        +target_branch(repository: str) str
        -_read_git(arguments: list[str]) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type79
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type80
        -_validate_registered_worktree(Signature81)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
        +dispose(repository: str, branch: str, path: str, remote: str, target_branch: str) None
        -_disposal_state(Signature82)
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
    class c0132["src/forgetful_factory/workspace/adapters/git/worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0133["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0134["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type3) unknown
        +code: unknown
        +paths: unknown
    }
    class c0135["WorktreeReadError"] {
        <<class>>
    }
    class c0136["Worktrees"] {
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
    c0000 ..> c0011 : close() calls close()
    c0000 ..> c0024 : type in wait
    c0000 ..> c0115 : 2 relationships (see list)
    c0000 ..> c0123 : 2 relationships (see list)
    c0003 ..> c0000 : 5 relationships (see list)
    c0003 ..> c0001 : serve() constructs SessionState
    c0003 ..> c0002 : load_host() constructs _UncachedLoader
    c0003 ..> c0003 : 20 relationships (see list)
    c0003 ..> c0012 : 2 relationships (see list)
    c0003 ..> c0101 : 5 relationships (see list)
    c0004 ..> c0004 : factory_launcher() calls runtime_directory()
    c0004 ..> c0049 : factory_launcher() calls write()
    c0004 ..> c0051 : factory_launcher() calls quote()
    c0004 ..> c0115 : 2 relationships (see list)
    c0004 ..> c0118 : runtime_directory() calls check_real_path()
    c0005 ..> c0014 : main() calls list_models()
    c0006 ..> c0000 : 11 relationships (see list)
    c0006 ..> c0006 : 27 relationships (see list)
    c0006 ..> c0007 : 2 relationships (see list)
    c0006 ..> c0023 : 2 relationships (see list)
    c0006 ..> c0049 : 6 relationships (see list)
    c0006 ..> c0051 : _apply_controller_problem() calls quote()
    c0006 ..> c0101 : 2 relationships (see list)
    c0006 ..> c0115 : 10 relationships (see list)
    c0006 ..> c0118 : save() calls replace_generated_json()
    c0007 ..> c0000 : 3 relationships (see list)
    c0007 ..> c0004 : _prepare_owner_startup() calls runtime_directory()
    c0007 ..> c0006 : 3 relationships (see list)
    c0007 ..> c0007 : 5 relationships (see list)
    c0007 ..> c0009 : _prepare_owner_startup() calls read_state()
    c0007 ..> c0051 : _acquire_owner_lock() calls quote()
    c0007 ..> c0101 : main() calls create_task()
    c0007 ..> c0115 : 3 relationships (see list)
    c0008 ..> c0009 : 5 relationships (see list)
    c0008 ..> c0023 : 2 relationships (see list)
    c0008 ..> c0026 : report() calls unknown_status()
    c0008 ..> c0051 : report() calls quote()
    c0008 ..> c0112 : type in __init__
    c0009 ..> c0000 : 2 relationships (see list)
    c0009 ..> c0004 : 3 relationships (see list)
    c0009 ..> c0006 : start_owner() calls run()
    c0009 ..> c0009 : 3 relationships (see list)
    c0009 ..> c0023 : 2 relationships (see list)
    c0009 ..> c0031 : request() calls connect()
    c0009 ..> c0051 : request() calls quote()
    c0009 ..> c0109 : start_owner() calls spec()
    c0009 ..> c0112 : type in start_owner
    c0009 ..> c0115 : 4 relationships (see list)
    c0009 ..> c0118 : read_state() calls read_generated_json()
    c0010 ..> c0010 : 3 relationships (see list)
    c0010 ..> c0115 : install() constructs FactoryError
    c0010 ..> c0117 : 5 relationships (see list)
    c0011 ..> c0000 : close() calls close()
    c0011 ..> c0011 : 10 relationships (see list)
    c0011 ..> c0023 : 2 relationships (see list)
    c0011 --> c0024 : field received
    c0011 ..> c0024 : 2 relationships (see list)
    c0011 ..> c0033 : startup_hint() calls how_to_reach()
    c0011 ..> c0038 : type in __init__
    c0011 ..> c0049 : 2 relationships (see list)
    c0011 ..> c0109 : start() calls spec()
    c0011 ..> c0112 : type in __init__
    c0011 ..> c0115 : 7 relationships (see list)
    c0011 ..> c0123 : 3 relationships (see list)
    c0012 ..> c0000 : pin_worker() calls close()
    c0013 ..> c0013 : 8 relationships (see list)
    c0013 ..> c0115 : 2 relationships (see list)
    c0013 ..> c0121 : 4 relationships (see list)
    c0014 ..> c0013 : selected_launch() calls foreman_launch()
    c0014 ..> c0014 : 20 relationships (see list)
    c0014 ..> c0015 : 4 relationships (see list)
    c0014 ..> c0017 : pi_home() calls saved_pi_home()
    c0014 ..> c0019 : _install_resources() calls bundled_files()
    c0014 ..> c0021 : selected_launch() calls selected_skill_files()
    c0014 ..> c0025 : 2 relationships (see list)
    c0014 ..> c0047 : choose_pi_home() calls confirm()
    c0014 ..> c0049 : _protect_runtime() calls write()
    c0014 ..> c0051 : require_pi_home() calls quote()
    c0014 ..> c0085 : validate_setup() calls missing_tools()
    c0014 ..> c0099 : list_models() calls role_environment()
    c0014 ..> c0104 : 7 relationships (see list)
    c0014 ..> c0115 : 13 relationships (see list)
    c0014 ..> c0116 : require_pi_home() calls executable_path()
    c0014 ..> c0118 : 10 relationships (see list)
    c0014 ..> c0120 : list_models() calls run_owned()
    c0015 ..> c0014 : prepare() calls prepare()
    c0015 ..> c0015 : 3 relationships (see list)
    c0015 ..> c0016 : prepare() calls selected_resources()
    c0015 ..> c0022 : __init__() constructs WorkerProfiles
    c0015 ..> c0115 : 4 relationships (see list)
    c0015 ..> c0118 : 5 relationships (see list)
    c0017 ..> c0115 : saved_pi_home() constructs FactoryError
    c0017 ..> c0118 : saved_pi_home() calls read_generated_json()
    c0019 ..> c0018 : 4 relationships (see list)
    c0019 ..> c0019 : 4 relationships (see list)
    c0019 ..> c0049 : 2 relationships (see list)
    c0019 ..> c0115 : 2 relationships (see list)
    c0019 ..> c0118 : plan_update() calls check_real_path()
    c0020 ..> c0017 : unready() calls saved_pi_home()
    c0020 ..> c0020 : unready() calls ready()
    c0020 ..> c0116 : 2 relationships (see list)
    c0020 ..> c0117 : 6 relationships (see list)
    c0020 ..> c0120 : ready() calls run_owned()
    c0021 ..> c0000 : _add_skill_file() calls close()
    c0021 ..> c0021 : 3 relationships (see list)
    c0021 ..> c0115 : 3 relationships (see list)
    c0022 ..> c0025 : type in prepare
    c0022 ..> c0054 : prepare() calls update()
    c0022 ..> c0118 : 3 relationships (see list)
    c0023 ..> c0121 : __post_init__() calls positive_duration()
    c0026 ..> c0025 : 3 relationships (see list)
    c0026 ..> c0026 : 4 relationships (see list)
    c0026 ..> c0115 : 5 relationships (see list)
    c0026 ..> c0121 : 4 relationships (see list)
    c0027 ..> c0025 : type in prepare_roles
    c0027 ..> c0104 : 4 relationships (see list)
    c0028 ..> c0024 : type in wait
    c0030 ..> c0000 : 2 relationships (see list)
    c0030 ..> c0030 : 15 relationships (see list)
    c0030 --> c0034 : field inbox
    c0030 ..> c0034 : 2 relationships (see list)
    c0030 ..> c0035 : type in mark
    c0030 ..> c0036 : type in __init__
    c0030 ..> c0114 : start() calls find_secret()
    c0031 ..> c0000 : 7 relationships (see list)
    c0031 ..> c0031 : 16 relationships (see list)
    c0031 ..> c0032 : 3 relationships (see list)
    c0031 ..> c0049 : tell() calls write()
    c0031 ..> c0064 : stop() calls clear()
    c0031 ..> c0101 : run() calls create_task()
    c0032 ..> c0000 : serve() calls close()
    c0032 ..> c0031 : 3 relationships (see list)
    c0032 ..> c0032 : main() calls serve()
    c0032 ..> c0049 : serve() calls write()
    c0033 ..> c0109 : 2 relationships (see list)
    c0033 ..> c0112 : type in __init__
    c0037 ..> c0036 : 3 relationships (see list)
    c0037 ..> c0115 : discord_from_mapping() constructs FactoryError
    c0039 ..> c0034 : type in receive
    c0039 ..> c0035 : type in mark
    c0040 ..> c0004 : prepare_foreman_launch() calls factory_launcher()
    c0040 ..> c0008 : 2 relationships (see list)
    c0040 ..> c0010 : build_tools() constructs AgentShellRuntimeInstall
    c0040 ..> c0011 : build_watcher() constructs AgentShellTerminal
    c0040 ..> c0014 : 6 relationships (see list)
    c0040 ..> c0020 : build_tools() constructs PiInstall
    c0040 ..> c0030 : 2 relationships (see list)
    c0040 ..> c0033 : 2 relationships (see list)
    c0040 ..> c0037 : 2 relationships (see list)
    c0040 ..> c0040 : 14 relationships (see list)
    c0040 ..> c0041 : 10 relationships (see list)
    c0040 ..> c0047 : build_watcher() constructs FileCleanupReceipts
    c0040 ..> c0050 : 2 relationships (see list)
    c0040 ..> c0052 : build_start_foreman() constructs WorkspaceWatchLease
    c0040 ..> c0053 : build_watcher() constructs ObservedTerminal
    c0040 ..> c0056 : 4 relationships (see list)
    c0040 ..> c0077 : build_watcher() constructs CleanupCompleted
    c0040 ..> c0084 : 2 relationships (see list)
    c0040 ..> c0085 : build_team() calls missing_tools()
    c0040 ..> c0086 : build_watcher() constructs ScaffoldIssue
    c0040 ..> c0088 : 2 relationships (see list)
    c0040 ..> c0090 : 2 relationships (see list)
    c0040 ..> c0093 : 2 relationships (see list)
    c0040 ..> c0094 : 2 relationships (see list)
    c0040 ..> c0099 : prepare_foreman_launch() calls role_environment()
    c0040 ..> c0100 : build_tools() constructs ForgetfulInstall
    c0040 ..> c0101 : build_watcher() constructs ForgetfulPlanStore
    c0040 ..> c0103 : build_initialiser() constructs ForgetfulSetup
    c0040 ..> c0104 : type in build_tools
    c0040 ..> c0109 : 2 relationships (see list)
    c0040 ..> c0110 : build_tools() constructs TmuxInstall
    c0040 ..> c0115 : 3 relationships (see list)
    c0040 ..> c0124 : 3 relationships (see list)
    c0040 ..> c0128 : type in select_ticketing
    c0040 ..> c0129 : 2 relationships (see list)
    c0040 ..> c0131 : build_watcher() constructs GitWorktrees
    c0041 --> c0023 : field agentshell
    c0041 ..> c0121 : __post_init__() calls positive_duration()
    c0042 --> c0056 : field config
    c0042 --> c0104 : field connection
    c0043 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0043 ..> c0006 : 2 relationships (see list)
    c0043 ..> c0008 : _watch_status() calls report()
    c0043 ..> c0009 : 7 relationships (see list)
    c0043 ..> c0014 : 11 relationships (see list)
    c0043 ..> c0025 : 7 relationships (see list)
    c0043 ..> c0026 : _start_initial_setup() calls validate_initial_agents()
    c0043 ..> c0040 : 7 relationships (see list)
    c0043 ..> c0041 : 10 relationships (see list)
    c0043 ..> c0042 : 3 relationships (see list)
    c0043 ..> c0043 : 54 relationships (see list)
    c0043 ..> c0044 : _select_numbered() calls parse_numbered_selection()
    c0043 ..> c0045 : main() calls update_resources()
    c0043 ..> c0046 : _watch_locked() calls load_configuration()
    c0043 ..> c0047 : _initialise_locked() calls load()
    c0043 ..> c0049 : 2 relationships (see list)
    c0043 ..> c0051 : 5 relationships (see list)
    c0043 ..> c0052 : 4 relationships (see list)
    c0043 ..> c0054 : _prompt_workers() calls update()
    c0043 ..> c0055 : _watch_locked() calls observe_plain_watch()
    c0043 ..> c0056 : 4 relationships (see list)
    c0043 ..> c0057 : _connection() calls validate()
    c0043 ..> c0082 : 2 relationships (see list)
    c0043 ..> c0084 : 17 relationships (see list)
    c0043 ..> c0097 : _complete_setup() calls uses_browser_login()
    c0043 ..> c0098 : 2 relationships (see list)
    c0043 ..> c0104 : 7 relationships (see list)
    c0043 ..> c0115 : 20 relationships (see list)
    c0043 ..> c0118 : _discover_worker_models() calls check_real_path()
    c0043 ..> c0123 : _watch_locked() calls watch_stop_scope()
    c0044 ..> c0115 : parse_numbered_selection() constructs FactoryError
    c0045 ..> c0003 : update_resources() calls ready()
    c0045 ..> c0009 : update_resources() calls read_state()
    c0045 ..> c0010 : 2 relationships (see list)
    c0045 ..> c0014 : update_resources() calls validate_bundled_resources()
    c0045 ..> c0019 : 2 relationships (see list)
    c0045 ..> c0040 : update_resources() calls build_team()
    c0045 ..> c0041 : type in update_resources
    c0045 ..> c0045 : update_resources() calls _report()
    c0045 ..> c0052 : 2 relationships (see list)
    c0045 ..> c0115 : 2 relationships (see list)
    c0046 ..> c0047 : load_configuration() calls load()
    c0046 ..> c0050 : load_configuration() constructs TomlConfigurationStore
    c0046 ..> c0056 : type in load_configuration
    c0046 ..> c0115 : load_configuration() constructs FactoryError
    c0047 ..> c0000 : _load() calls close()
    c0047 ..> c0047 : 5 relationships (see list)
    c0047 ..> c0048 : 2 relationships (see list)
    c0047 ..> c0049 : _load() calls read()
    c0047 ..> c0067 : type in confirm_plans
    c0047 ..> c0069 : type in confirm
    c0047 ..> c0071 : 3 relationships (see list)
    c0047 ..> c0115 : 2 relationships (see list)
    c0047 ..> c0118 : 2 relationships (see list)
    c0047 ..> c0123 : 3 relationships (see list)
    c0048 ..> c0048 : _rows() calls _identity()
    c0049 ..> c0118 : 2 relationships (see list)
    c0050 ..> c0000 : 2 relationships (see list)
    c0050 ..> c0047 : load() calls load()
    c0050 ..> c0049 : save() calls write()
    c0050 ..> c0051 : save() calls quote()
    c0050 ..> c0056 : 2 relationships (see list)
    c0050 ..> c0057 : load() calls from_mapping()
    c0050 ..> c0115 : 2 relationships (see list)
    c0052 ..> c0000 : _hold_directory() calls close()
    c0052 ..> c0052 : hold() calls _hold_directory()
    c0052 ..> c0115 : _hold_directory() constructs FactoryError
    c0053 ..> c0000 : 5 relationships (see list)
    c0053 ..> c0024 : type in wait
    c0053 ..> c0026 : __init__() calls unknown_status()
    c0053 ..> c0028 : type in __init__
    c0053 ..> c0054 : 3 relationships (see list)
    c0054 ..> c0031 : __enter__() calls listen()
    c0054 ..> c0053 : 2 relationships (see list)
    c0054 ..> c0054 : 9 relationships (see list)
    c0054 ..> c0055 : 6 relationships (see list)
    c0054 ..> c0115 : __enter__() constructs FactoryError
    c0054 ..> c0118 : 3 relationships (see list)
    c0055 ..> c0026 : plain_watch_status() calls unknown_status()
    c0055 ..> c0031 : plain_watch_status() calls connect()
    c0055 ..> c0049 : _read_discovery() calls read()
    c0055 ..> c0054 : 4 relationships (see list)
    c0055 ..> c0055 : 7 relationships (see list)
    c0055 ..> c0118 : _read_discovery() calls check_real_path()
    c0056 --> c0036 : field discord
    c0056 --> c0058 : field repository
    c0056 --> c0104 : field forgetful
    c0057 ..> c0037 : from_mapping() calls discord_from_mapping()
    c0057 ..> c0056 : 3 relationships (see list)
    c0057 ..> c0057 : from_mapping() calls validate()
    c0057 ..> c0058 : from_mapping() constructs RepositoryReference
    c0057 ..> c0104 : validate() calls validate()
    c0057 ..> c0105 : from_mapping() calls connection_from_mapping()
    c0057 ..> c0115 : 2 relationships (see list)
    c0057 ..> c0121 : 2 relationships (see list)
    c0057 ..> c0127 : from_mapping() constructs TicketSource
    c0058 --> c0127 : field work_source
    c0059 --|> c0061 : inherits
    c0060 --|> c0061 : inherits
    c0061 --|> c0115 : inherits
    c0062 --|> c0061 : inherits
    c0063 --|> c0061 : inherits
    c0064 ..> c0000 : 2 relationships (see list)
    c0064 ..> c0065 : send() calls _cleanup_recovery()
    c0064 ..> c0115 : type in send
    c0068 ..> c0067 : type in confirm_plans
    c0068 ..> c0069 : type in confirm
    c0068 ..> c0071 : type in load
    c0070 ..> c0056 : 2 relationships (see list)
    c0071 --> c0067 : field plans
    c0071 --> c0069 : field sets
    c0074 ..> c0024 : type in _post
    c0074 ..> c0028 : type in __init__
    c0074 ..> c0030 : 4 relationships (see list)
    c0074 ..> c0034 : type in _deliver
    c0074 ..> c0039 : type in __init__
    c0074 ..> c0074 : 6 relationships (see list)
    c0074 ..> c0075 : 4 relationships (see list)
    c0074 ..> c0076 : stop() calls stop_reason()
    c0075 ..> c0000 : 4 relationships (see list)
    c0075 ..> c0024 : type in wait
    c0075 ..> c0074 : 4 relationships (see list)
    c0075 ..> c0075 : __init__() constructs _SharedTerminal
    c0077 ..> c0000 : 6 relationships (see list)
    c0077 ..> c0008 : _dispose() calls report()
    c0077 ..> c0047 : 3 relationships (see list)
    c0077 ..> c0054 : 4 relationships (see list)
    c0077 ..> c0061 : 8 relationships (see list)
    c0077 ..> c0064 : 12 relationships (see list)
    c0077 --> c0067 : field finished_plans
    c0077 ..> c0067 : 2 relationships (see list)
    c0077 ..> c0068 : type in __init__
    c0077 --> c0069 : field confirmed
    c0077 ..> c0069 : 3 relationships (see list)
    c0077 ..> c0077 : 35 relationships (see list)
    c0077 ..> c0078 : 7 relationships (see list)
    c0077 ..> c0079 : 6 relationships (see list)
    c0077 ..> c0083 : 9 relationships (see list)
    c0077 ..> c0101 : 8 relationships (see list)
    c0077 ..> c0107 : _check_summaries() constructs PlanningReadError
    c0077 ..> c0115 : type in _read_problem
    c0077 ..> c0124 : _in_scope() calls could_be_key()
    c0077 ..> c0128 : type in __init__
    c0077 ..> c0131 : 4 relationships (see list)
    c0077 ..> c0136 : type in __init__
    c0081 ..> c0080 : validate_cleanup_marker() constructs CleanupMarkerError
    c0081 ..> c0094 : validate_cleanup_marker() calls is_change_request()
    c0081 ..> c0095 : type in validate_cleanup_marker
    c0081 ..> c0096 : type in validate_cleanup_marker
    c0082 ..> c0049 : 3 relationships (see list)
    c0082 ..> c0056 : type in agree_definition_of_done
    c0082 ..> c0066 : type in agree_definition_of_done
    c0082 ..> c0082 : agree_definition_of_done() calls _deployment_agreement()
    c0082 ..> c0115 : 2 relationships (see list)
    c0083 ..> c0056 : type in __init__
    c0083 ..> c0058 : 3 relationships (see list)
    c0083 ..> c0060 : 2 relationships (see list)
    c0083 ..> c0061 : 5 relationships (see list)
    c0083 ..> c0083 : 2 relationships (see list)
    c0083 ..> c0094 : check_source() calls repository()
    c0083 ..> c0095 : type in check_source
    c0083 ..> c0096 : type in __init__
    c0083 ..> c0101 : ownership() calls tasks()
    c0083 ..> c0106 : type in __init__
    c0083 ..> c0124 : 2 relationships (see list)
    c0083 ..> c0126 : 2 relationships (see list)
    c0083 ..> c0127 : snapshot() constructs TicketSource
    c0083 ..> c0128 : type in __init__
    c0083 ..> c0129 : check_repository() calls origin()
    c0083 ..> c0133 : type in __init__
    c0084 ..> c0006 : initialise() calls save()
    c0084 ..> c0010 : prepare_foreman() calls install()
    c0084 ..> c0014 : prepare_foreman() calls prepare()
    c0084 ..> c0027 : type in __init__
    c0084 ..> c0047 : 2 relationships (see list)
    c0084 ..> c0056 : 6 relationships (see list)
    c0084 ..> c0057 : 3 relationships (see list)
    c0084 ..> c0058 : 2 relationships (see list)
    c0084 ..> c0070 : type in __init__
    c0084 ..> c0072 : type in __init__
    c0084 ..> c0074 : check_foreman() calls check()
    c0084 ..> c0084 : 3 relationships (see list)
    c0084 ..> c0085 : 2 relationships (see list)
    c0084 ..> c0094 : 2 relationships (see list)
    c0084 ..> c0096 : type in __init__
    c0084 ..> c0098 : check_foreman() calls login()
    c0084 ..> c0104 : 2 relationships (see list)
    c0084 ..> c0108 : type in __init__
    c0084 ..> c0115 : 5 relationships (see list)
    c0084 ..> c0124 : 4 relationships (see list)
    c0084 ..> c0125 : 2 relationships (see list)
    c0084 ..> c0127 : 3 relationships (see list)
    c0084 ..> c0128 : type in __init__
    c0084 ..> c0129 : 3 relationships (see list)
    c0084 ..> c0133 : type in __init__
    c0085 ..> c0010 : 3 relationships (see list)
    c0085 ..> c0072 : 2 relationships (see list)
    c0086 ..> c0054 : recover() calls snapshot()
    c0086 ..> c0056 : type in __init__
    c0086 ..> c0058 : 3 relationships (see list)
    c0086 ..> c0059 : preflight() constructs IntakeProblem
    c0086 ..> c0061 : 8 relationships (see list)
    c0086 ..> c0062 : 5 relationships (see list)
    c0086 ..> c0063 : 5 relationships (see list)
    c0086 ..> c0074 : check() calls check()
    c0086 ..> c0081 : _ensure_mapping() calls validate_cleanup_marker()
    c0086 ..> c0083 : 11 relationships (see list)
    c0086 ..> c0084 : preflight() calls inspect()
    c0086 ..> c0086 : 22 relationships (see list)
    c0086 ..> c0087 : _initial_mappings() calls worktree_name()
    c0086 ..> c0096 : type in __init__
    c0086 ..> c0101 : 12 relationships (see list)
    c0086 ..> c0106 : type in __init__
    c0086 ..> c0115 : _is_unfinished_factory_plan() constructs FactoryError
    c0086 ..> c0126 : 8 relationships (see list)
    c0086 ..> c0127 : type in _repository
    c0086 ..> c0128 : type in __init__
    c0086 ..> c0131 : 3 relationships (see list)
    c0086 ..> c0133 : type in __init__
    c0086 ..> c0136 : type in __init__
    c0087 ..> c0126 : type in worktree_name
    c0088 ..> c0000 : run() calls start()
    c0088 ..> c0008 : 2 relationships (see list)
    c0088 ..> c0014 : run() calls prepare()
    c0088 ..> c0029 : type in __init__
    c0088 ..> c0038 : type in __init__
    c0088 ..> c0052 : run() calls hold()
    c0088 ..> c0073 : type in __init__
    c0088 ..> c0115 : run() constructs FactoryError
    c0089 --> c0126 : field issue
    c0090 ..> c0000 : 15 relationships (see list)
    c0090 ..> c0008 : 5 relationships (see list)
    c0090 ..> c0014 : _process_issue() calls prepare()
    c0090 ..> c0028 : type in __init__
    c0090 ..> c0030 : _watch() calls online()
    c0090 ..> c0031 : _watch() calls stop()
    c0090 ..> c0039 : type in __init__
    c0090 ..> c0056 : 4 relationships (see list)
    c0090 ..> c0058 : 5 relationships (see list)
    c0090 ..> c0060 : 2 relationships (see list)
    c0090 ..> c0061 : 3 relationships (see list)
    c0090 ..> c0062 : 2 relationships (see list)
    c0090 ..> c0064 : 28 relationships (see list)
    c0090 ..> c0074 : 3 relationships (see list)
    c0090 ..> c0077 : 2 relationships (see list)
    c0090 ..> c0083 : _check_pending_repositories() calls check_repository()
    c0090 ..> c0086 : 5 relationships (see list)
    c0090 ..> c0089 : 13 relationships (see list)
    c0090 ..> c0090 : 35 relationships (see list)
    c0090 ..> c0091 : 19 relationships (see list)
    c0090 ..> c0092 : 2 relationships (see list)
    c0090 ..> c0115 : _read_issues() constructs FactoryError
    c0090 ..> c0123 : 3 relationships (see list)
    c0090 ..> c0124 : _read_issues() calls list_open()
    c0090 ..> c0126 : 13 relationships (see list)
    c0090 ..> c0127 : 7 relationships (see list)
    c0090 ..> c0128 : type in __init__
    c0091 --> c0058 : field pending_repositories
    c0091 --> c0089 : 2 relationships (see list)
    c0091 --> c0126 : field pending_lookup
    c0091 --> c0127 : field baselined
    c0093 ..> c0014 : _setup() calls validate_completion()
    c0093 ..> c0026 : _without_live_plain() calls unknown_status()
    c0093 ..> c0027 : type in __init__
    c0093 ..> c0029 : type in __init__
    c0093 ..> c0047 : _setup() calls load()
    c0093 ..> c0070 : type in __init__
    c0093 ..> c0093 : 3 relationships (see list)
    c0094 ..> c0095 : 3 relationships (see list)
    c0094 ..> c0115 : repository() constructs FactoryError
    c0096 ..> c0095 : 2 relationships (see list)
    c0097 ..> c0009 : uses_browser_login() calls request()
    c0097 ..> c0049 : uses_browser_login() calls read()
    c0097 ..> c0104 : type in uses_browser_login
    c0098 ..> c0098 : 7 relationships (see list)
    c0098 ..> c0099 : 2 relationships (see list)
    c0098 ..> c0104 : 7 relationships (see list)
    c0098 ..> c0115 : 5 relationships (see list)
    c0098 ..> c0120 : 2 relationships (see list)
    c0098 ..> c0123 : command() calls check_watch_stop()
    c0099 ..> c0054 : role_environment() calls update()
    c0099 ..> c0104 : type in role_environment
    c0099 ..> c0116 : role_environment() calls executable_path()
    c0100 ..> c0100 : 6 relationships (see list)
    c0100 ..> c0104 : type in __init__
    c0100 ..> c0115 : _python() constructs FactoryError
    c0100 ..> c0116 : _selected() calls executable_path()
    c0100 ..> c0117 : 7 relationships (see list)
    c0100 ..> c0120 : _python() calls run_owned()
    c0101 ..> c0074 : check() calls check()
    c0101 ..> c0098 : 2 relationships (see list)
    c0101 ..> c0101 : 12 relationships (see list)
    c0101 ..> c0102 : 3 relationships (see list)
    c0101 ..> c0104 : type in __init__
    c0101 ..> c0107 : 4 relationships (see list)
    c0103 ..> c0074 : check() calls check()
    c0103 ..> c0097 : uses_browser_login() calls uses_browser_login()
    c0103 ..> c0098 : 5 relationships (see list)
    c0103 ..> c0103 : 4 relationships (see list)
    c0103 ..> c0104 : 6 relationships (see list)
    c0104 ..> c0104 : validate() calls _validate_server()
    c0104 ..> c0105 : _validate_server() calls loopback_host()
    c0104 ..> c0115 : 2 relationships (see list)
    c0104 ..> c0121 : 2 relationships (see list)
    c0105 ..> c0104 : 3 relationships (see list)
    c0105 ..> c0115 : connection_from_mapping() constructs FactoryError
    c0107 --|> c0115 : inherits
    c0108 ..> c0104 : 6 relationships (see list)
    c0109 ..> c0006 : enter() calls run()
    c0109 ..> c0115 : enter() constructs FactoryError
    c0110 ..> c0111 : 2 relationships (see list)
    c0110 ..> c0115 : install() constructs FactoryError
    c0110 ..> c0116 : absent() calls executable_path()
    c0110 ..> c0117 : 2 relationships (see list)
    c0113 ..> c0006 : run_command() calls run()
    c0113 ..> c0115 : run_command() constructs FactoryError
    c0113 ..> c0123 : run_command() calls check_watch_stop()
    c0114 ..> c0114 : find_secret() calls read_env_file()
    c0117 ..> c0049 : install_locks() calls read()
    c0117 ..> c0115 : 6 relationships (see list)
    c0117 ..> c0117 : 4 relationships (see list)
    c0117 ..> c0118 : install_locks() calls write_new()
    c0117 ..> c0120 : 3 relationships (see list)
    c0118 ..> c0000 : 2 relationships (see list)
    c0118 ..> c0047 : read_generated_json() calls load()
    c0118 ..> c0049 : 2 relationships (see list)
    c0118 ..> c0115 : 6 relationships (see list)
    c0118 ..> c0118 : 9 relationships (see list)
    c0120 ..> c0000 : 2 relationships (see list)
    c0120 ..> c0115 : run_owned() constructs FactoryError
    c0120 ..> c0120 : 2 relationships (see list)
    c0120 ..> c0123 : run_owned() calls check_watch_stop()
    c0121 ..> c0115 : nonblank() constructs FactoryError
    c0123 ..> c0122 : watch_stop_scope() constructs WatchStop
    c0124 ..> c0113 : 2 relationships (see list)
    c0124 ..> c0115 : 9 relationships (see list)
    c0124 ..> c0124 : 9 relationships (see list)
    c0124 ..> c0125 : 3 relationships (see list)
    c0124 ..> c0126 : 3 relationships (see list)
    c0124 ..> c0127 : 9 relationships (see list)
    c0126 --> c0127 : field source
    c0128 ..> c0125 : 2 relationships (see list)
    c0128 ..> c0126 : type in list_open
    c0128 ..> c0127 : 5 relationships (see list)
    c0129 ..> c0113 : origin() calls run_command()
    c0129 ..> c0115 : origin() constructs FactoryError
    c0129 ..> c0130 : origin() calls _resolve_repository()
    c0130 ..> c0115 : _resolve_repository() constructs FactoryError
    c0131 ..> c0049 : ensure() calls write()
    c0131 ..> c0051 : _network_git() calls quote()
    c0131 ..> c0064 : begin_cleanup_cycle() calls clear()
    c0131 ..> c0113 : 4 relationships (see list)
    c0131 --> c0115 : field cleanup_defaults
    c0131 ..> c0115 : ensure() constructs FactoryError
    c0131 ..> c0123 : ensure() calls check_watch_stop()
    c0131 ..> c0131 : 35 relationships (see list)
    c0131 ..> c0132 : _repository_entries() calls _worktree_entries()
    c0131 ..> c0134 : 14 relationships (see list)
    c0131 ..> c0135 : 6 relationships (see list)
    c0134 ..> c0000 : __init__() calls __init__()
    c0134 --|> c0115 : inherits
    c0135 --|> c0115 : inherits
```

## Source index

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/agents/adapters/agentshell/borrowed_terminal.py`:11
- c0001: `SessionState` — `src/forgetful_factory/agents/adapters/agentshell/controller.py`:159
- c0002: `_UncachedLoader` — `src/forgetful_factory/agents/adapters/agentshell/controller.py`:135
- c0003: `src/forgetful_factory/agents/adapters/agentshell/controller.py` —
  `src/forgetful_factory/agents/adapters/agentshell/controller.py`:1
- c0004: `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py` —
  `src/forgetful_factory/agents/adapters/agentshell/foreman_runtime.py`:1
- c0005: `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/agents/adapters/agentshell/model_catalog.py`:1
- c0006: `ForemanOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner.py`:104
- c0007: `src/forgetful_factory/agents/adapters/agentshell/owner.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner.py`:1
- c0008: `AgentShellOwner` — `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:180
- c0009: `src/forgetful_factory/agents/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/agents/adapters/agentshell/owner_client.py`:1
- c0010: `AgentShellRuntimeInstall` —
  `src/forgetful_factory/agents/adapters/agentshell/runtime_install.py`:24
- c0011: `AgentShellTerminal` — `src/forgetful_factory/agents/adapters/agentshell/terminal.py`:17
- c0012: `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py` —
  `src/forgetful_factory/agents/adapters/agentshell/tmux_host.py`:1
- c0013: `src/forgetful_factory/agents/adapters/pi/agent_definitions.py` —
  `src/forgetful_factory/agents/adapters/pi/agent_definitions.py`:1
- c0014: `PiAgentTeam` — `src/forgetful_factory/agents/adapters/pi/agent_team.py`:46
- c0015: `CoordinatorProfiles` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:29
- c0016: `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py` —
  `src/forgetful_factory/agents/adapters/pi/coordinator_profiles.py`:1
- c0017: `src/forgetful_factory/agents/adapters/pi/native_home.py` —
  `src/forgetful_factory/agents/adapters/pi/native_home.py`:1
- c0018: `ResourceUpdate` — `src/forgetful_factory/agents/adapters/pi/role_resources.py`:39
- c0019: `src/forgetful_factory/agents/adapters/pi/role_resources.py` —
  `src/forgetful_factory/agents/adapters/pi/role_resources.py`:1
- c0020: `PiInstall` — `src/forgetful_factory/agents/adapters/pi/runtime_install.py`:22
- c0021: `src/forgetful_factory/agents/adapters/pi/selected_skills.py` —
  `src/forgetful_factory/agents/adapters/pi/selected_skills.py`:1
- c0022: `WorkerProfiles` — `src/forgetful_factory/agents/adapters/pi/worker_profiles.py`:16
- c0023: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/agents/model.py`:139
- c0024: `ForemanReply` — `src/forgetful_factory/agents/model.py`:9
- c0025: `InitialAgentChoices` — `src/forgetful_factory/agents/model.py`:17
- c0026: `src/forgetful_factory/agents/model.py` — `src/forgetful_factory/agents/model.py`:1
- c0027: `AgentTeam` — `src/forgetful_factory/agents/ports.py`:38
- c0028: `ForemanTerminal` — `src/forgetful_factory/agents/ports.py`:9
- c0029: `PersistentForeman` — `src/forgetful_factory/agents/ports.py`:22
- c0030: `DiscordLink` — `src/forgetful_factory/channels/adapters/discord/link.py`:25
- c0031: `Relay` — `src/forgetful_factory/channels/adapters/discord/relay.py`:78
- c0032: `src/forgetful_factory/channels/adapters/discord/relay.py` —
  `src/forgetful_factory/channels/adapters/discord/relay.py`:1
- c0033: `TerminalChannel` — `src/forgetful_factory/channels/adapters/terminal.py`:8
- c0034: `ChatMessage` — `src/forgetful_factory/channels/model.py`:22
- c0035: `Delivery` — `src/forgetful_factory/channels/model.py`:13
- c0036: `DiscordSettings` — `src/forgetful_factory/channels/model.py`:29
- c0037: `src/forgetful_factory/channels/model.py` — `src/forgetful_factory/channels/model.py`:1
- c0038: `Channel` — `src/forgetful_factory/channels/ports.py`:6
- c0039: `ChatChannel` — `src/forgetful_factory/channels/ports.py`:16
- c0040: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0041: `DeadlinePolicy` — `src/forgetful_factory/cli/deadlines.py`:9
- c0042: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:683
- c0043: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0044: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0045: `src/forgetful_factory/cli/resource_update.py` —
  `src/forgetful_factory/cli/resource_update.py`:1
- c0046: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0047: `FileCleanupReceipts` — `src/forgetful_factory/factory/adapters/cleanup_receipts.py`:60
- c0048: `src/forgetful_factory/factory/adapters/cleanup_receipts.py` —
  `src/forgetful_factory/factory/adapters/cleanup_receipts.py`:1
- c0049: `MarkdownAgreement` — `src/forgetful_factory/factory/adapters/markdown_agreement.py`:7
- c0050: `TomlConfigurationStore` —
  `src/forgetful_factory/factory/adapters/toml_configuration.py`:17
- c0051: `src/forgetful_factory/factory/adapters/toml_configuration.py` —
  `src/forgetful_factory/factory/adapters/toml_configuration.py`:1
- c0052: `WorkspaceWatchLease` — `src/forgetful_factory/factory/adapters/watch_lease.py`:10
- c0053: `ObservedTerminal` — `src/forgetful_factory/factory/adapters/watch_status.py`:247
- c0054: `PlainWatchObservation` — `src/forgetful_factory/factory/adapters/watch_status.py`:124
- c0055: `src/forgetful_factory/factory/adapters/watch_status.py` —
  `src/forgetful_factory/factory/adapters/watch_status.py`:1
- c0056: `FactoryConfiguration` — `src/forgetful_factory/factory/model/configuration.py`:12
- c0057: `src/forgetful_factory/factory/model/configuration.py` —
  `src/forgetful_factory/factory/model/configuration.py`:1
- c0058: `RepositoryReference` — `src/forgetful_factory/factory/model/repositories.py`:7
- c0059: `IntakeProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:143
- c0060: `RepositoryProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:139
- c0061: `ScaffoldProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:119
- c0062: `ScaffoldReadProblem` — `src/forgetful_factory/factory/model/watcher_problems.py`:135
- c0063: `UncertainScaffold` — `src/forgetful_factory/factory/model/watcher_problems.py`:147
- c0064: `WatcherAlerts` — `src/forgetful_factory/factory/model/watcher_problems.py`:151
- c0065: `src/forgetful_factory/factory/model/watcher_problems.py` —
  `src/forgetful_factory/factory/model/watcher_problems.py`:1
- c0066: `AgreementStore` — `src/forgetful_factory/factory/ports.py`:65
- c0067: `CleanupPlan` — `src/forgetful_factory/factory/ports.py`:39
- c0068: `CleanupReceipts` — `src/forgetful_factory/factory/ports.py`:53
- c0069: `CleanupSet` — `src/forgetful_factory/factory/ports.py`:21
- c0070: `ConfigurationStore` — `src/forgetful_factory/factory/ports.py`:10
- c0071: `FinishedCleanup` — `src/forgetful_factory/factory/ports.py`:48
- c0072: `ToolInstaller` — `src/forgetful_factory/factory/ports.py`:81
- c0073: `WatchLease` — `src/forgetful_factory/factory/ports.py`:16
- c0074: `ChatRelay` — `src/forgetful_factory/factory/services/chat_relay.py`:29
- c0075: `_SharedTerminal` — `src/forgetful_factory/factory/services/chat_relay.py`:161
- c0076: `src/forgetful_factory/factory/services/chat_relay.py` —
  `src/forgetful_factory/factory/services/chat_relay.py`:1
- c0077: `CleanupCompleted` — `src/forgetful_factory/factory/services/cleanup_completed.py`:39
- c0078: `CompletedWork` — `src/forgetful_factory/factory/services/cleanup_completed.py`:24
- c0079: `src/forgetful_factory/factory/services/cleanup_completed.py` —
  `src/forgetful_factory/factory/services/cleanup_completed.py`:1
- c0080: `CleanupMarkerError` — `src/forgetful_factory/factory/services/cleanup_marker.py`:11
- c0081: `src/forgetful_factory/factory/services/cleanup_marker.py` —
  `src/forgetful_factory/factory/services/cleanup_marker.py`:1
- c0082: `src/forgetful_factory/factory/services/definition_of_done.py` —
  `src/forgetful_factory/factory/services/definition_of_done.py`:1
- c0083: `FactoryRecords` — `src/forgetful_factory/factory/services/factory_records.py`:17
- c0084: `InitialiseFactory` — `src/forgetful_factory/factory/services/initialise_factory.py`:37
- c0085: `src/forgetful_factory/factory/services/initialise_factory.py` —
  `src/forgetful_factory/factory/services/initialise_factory.py`:1
- c0086: `ScaffoldIssue` — `src/forgetful_factory/factory/services/scaffold_issue.py`:38
- c0087: `src/forgetful_factory/factory/services/scaffold_issue.py` —
  `src/forgetful_factory/factory/services/scaffold_issue.py`:1
- c0088: `StartForeman` — `src/forgetful_factory/factory/services/start_foreman.py`:14
- c0089: `BlockedWork` — `src/forgetful_factory/factory/services/watch_factory.py`:29
- c0090: `WatchFactory` — `src/forgetful_factory/factory/services/watch_factory.py`:61
- c0091: `_WatchState` — `src/forgetful_factory/factory/services/watch_factory.py`:40
- c0092: `_WorkAction` — `src/forgetful_factory/factory/services/watch_factory.py`:54
- c0093: `WatchStatus` — `src/forgetful_factory/factory/services/watch_status.py`:10
- c0094: `GitHubForge` — `src/forgetful_factory/forge/adapters/github.py`:8
- c0095: `RepositoryRef` — `src/forgetful_factory/forge/model.py`:6
- c0096: `Forge` — `src/forgetful_factory/forge/ports.py`:6
- c0097: `src/forgetful_factory/planning/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/planning/adapters/forgetful/authentication.py`:1
- c0098: `AgentForgetfulConnection` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:59
- c0099: `src/forgetful_factory/planning/adapters/forgetful/connection.py` —
  `src/forgetful_factory/planning/adapters/forgetful/connection.py`:1
- c0100: `ForgetfulInstall` — `src/forgetful_factory/planning/adapters/forgetful/install.py`:26
- c0101: `ForgetfulPlanStore` — `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:13
- c0102: `src/forgetful_factory/planning/adapters/forgetful/plan_store.py` —
  `src/forgetful_factory/planning/adapters/forgetful/plan_store.py`:1
- c0103: `ForgetfulSetup` — `src/forgetful_factory/planning/adapters/forgetful/setup.py`:9
- c0104: `ForgetfulConnection` — `src/forgetful_factory/planning/model.py`:13
- c0105: `src/forgetful_factory/planning/model.py` — `src/forgetful_factory/planning/model.py`:1
- c0106: `PlanStore` — `src/forgetful_factory/planning/ports.py`:11
- c0107: `PlanningReadError` — `src/forgetful_factory/planning/ports.py`:7
- c0108: `PlanningSetup` — `src/forgetful_factory/planning/ports.py`:38
- c0109: `TmuxHost` — `src/forgetful_factory/runtime/adapters/tmux.py`:28
- c0110: `TmuxInstall` — `src/forgetful_factory/runtime/adapters/tmux.py`:54
- c0111: `src/forgetful_factory/runtime/adapters/tmux.py` —
  `src/forgetful_factory/runtime/adapters/tmux.py`:1
- c0112: `SessionHost` — `src/forgetful_factory/runtime/ports.py`:4
- c0113: `src/forgetful_factory/shared/command.py` — `src/forgetful_factory/shared/command.py`:1
- c0114: `src/forgetful_factory/shared/env_file.py` — `src/forgetful_factory/shared/env_file.py`:1
- c0115: `FactoryError` — `src/forgetful_factory/shared/errors.py`:1
- c0116: `src/forgetful_factory/shared/executables.py` —
  `src/forgetful_factory/shared/executables.py`:1
- c0117: `src/forgetful_factory/shared/installation.py` —
  `src/forgetful_factory/shared/installation.py`:1
- c0118: `src/forgetful_factory/shared/resource_files.py` —
  `src/forgetful_factory/shared/resource_files.py`:1
- c0119: `src/forgetful_factory/shared/resources.py` — `src/forgetful_factory/shared/resources.py`:1
- c0120: `src/forgetful_factory/shared/sensitive_command.py` —
  `src/forgetful_factory/shared/sensitive_command.py`:1
- c0121: `src/forgetful_factory/shared/validation.py` —
  `src/forgetful_factory/shared/validation.py`:1
- c0122: `WatchStop` — `src/forgetful_factory/shared/watch_stop.py`:8
- c0123: `src/forgetful_factory/shared/watch_stop.py` —
  `src/forgetful_factory/shared/watch_stop.py`:1
- c0124: `GitHubTicketing` — `src/forgetful_factory/ticketing/adapters/github.py`:17
- c0125: `Label` — `src/forgetful_factory/ticketing/model.py`:17
- c0126: `Ticket` — `src/forgetful_factory/ticketing/model.py`:22
- c0127: `TicketSource` — `src/forgetful_factory/ticketing/model.py`:6
- c0128: `Ticketing` — `src/forgetful_factory/ticketing/ports.py`:6
- c0129: `GitRepositories` — `src/forgetful_factory/workspace/adapters/git/repositories.py`:15
- c0130: `src/forgetful_factory/workspace/adapters/git/repositories.py` —
  `src/forgetful_factory/workspace/adapters/git/repositories.py`:1
- c0131: `GitWorktrees` — `src/forgetful_factory/workspace/adapters/git/worktrees.py`:33
- c0132: `src/forgetful_factory/workspace/adapters/git/worktrees.py` —
  `src/forgetful_factory/workspace/adapters/git/worktrees.py`:1
- c0133: `LocalRepositories` — `src/forgetful_factory/workspace/ports.py`:8
- c0134: `WorktreeProblem` — `src/forgetful_factory/workspace/ports.py`:18
- c0135: `WorktreeReadError` — `src/forgetful_factory/workspace/ports.py`:14
- c0136: `Worktrees` — `src/forgetful_factory/workspace/ports.py`:27

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0011: `close() calls close()`
- c0000 ..> c0024: `type in wait`
- c0000 ..> c0115: `_request() constructs FactoryError`
- c0000 ..> c0115: `wait() constructs FactoryError`
- c0000 ..> c0123: `_request() calls check_watch_stop()`
- c0000 ..> c0123: `wait() calls check_watch_stop()`
- c0003 ..> c0000: `close_session() calls close()`
- c0003 ..> c0000: `control() calls close()`
- c0003 ..> c0000: `control() calls wait()`
- c0003 ..> c0000: `resume_exit_observation() calls wait()`
- c0003 ..> c0000: `supervise_session() calls wait()`
- c0003 ..> c0001: `serve() constructs SessionState`
- c0003 ..> c0002: `load_host() constructs _UncachedLoader`
- c0003 ..> c0003: `become_ready() calls ready()`
- c0003 ..> c0003: `build_shell() calls runtime()`
- c0003 ..> c0003: `control() calls serve()`
- c0003 ..> c0003: `interact() calls become_ready()`
- c0003 ..> c0003: `interact() calls cancel_tasks()`
- c0003 ..> c0003: `interact() calls forward_replies()`
- c0003 ..> c0003: `interact() calls send_line()`
- c0003 ..> c0003: `main() calls control()`
- c0003 ..> c0003: `open_session() calls capture_worker()`
- c0003 ..> c0003: `replace_failed_exit_task() calls resume_exit_observation()`
- c0003 ..> c0003: `serve() calls build_shell()`
- c0003 ..> c0003: `serve() calls close_session()`
- c0003 ..> c0003: `serve() calls load_host()`
- c0003 ..> c0003: `serve() calls open_session()`
- c0003 ..> c0003: `serve() calls supervise_session()`
- c0003 ..> c0003: `serve() calls validate_launch_config()`
- c0003 ..> c0003: `supervise_session() calls cancel_tasks()`
- c0003 ..> c0003: `supervise_session() calls interact()`
- c0003 ..> c0003: `supervise_session() calls replace_failed_exit_task()`
- c0003 ..> c0003: `supervise_session() calls worker_exited()`
- c0003 ..> c0012: `capture_worker() calls pin_worker()`
- c0003 ..> c0012: `supervise_session() calls retain_identity()`
- c0003 ..> c0101: `control() calls create_task()`
- c0003 ..> c0101: `interact() calls create_task()`
- c0003 ..> c0101: `main() calls create_task()`
- c0003 ..> c0101: `replace_failed_exit_task() calls create_task()`
- c0003 ..> c0101: `supervise_session() calls create_task()`
- c0004 ..> c0004: `factory_launcher() calls runtime_directory()`
- c0004 ..> c0049: `factory_launcher() calls write()`
- c0004 ..> c0051: `factory_launcher() calls quote()`
- c0004 ..> c0115: `factory_launcher() constructs FactoryError`
- c0004 ..> c0115: `runtime_directory() constructs FactoryError`
- c0004 ..> c0118: `runtime_directory() calls check_real_path()`
- c0005 ..> c0014: `main() calls list_models()`
- c0006 ..> c0000: `_await_readiness() calls wait()`
- c0006 ..> c0000: `_cleanup() calls close()`
- c0006 ..> c0000: `_close_controller() calls close()`
- c0006 ..> c0000: `_close_controller() calls wait()`
- c0006 ..> c0000: `_complete_handover() calls close()`
- c0006 ..> c0000: `control() calls close()`
- c0006 ..> c0000: `reap_watcher() calls wait()`
- c0006 ..> c0000: `relay() calls close()`
- c0006 ..> c0000: `run() calls close()`
- c0006 ..> c0000: `run() calls wait()`
- c0006 ..> c0000: `start_watcher() calls close()`
- c0006 ..> c0006: `_apply_controller_event() calls _apply_controller_problem()`
- c0006 ..> c0006: `_apply_controller_event() calls save()`
- c0006 ..> c0006: `_apply_controller_problem() calls save()`
- c0006 ..> c0006: `_apply_controller_problem() calls stop_watcher()`
- c0006 ..> c0006: `_cleanup() calls _close_controller()`
- c0006 ..> c0006: `_cleanup() calls _remove_control_socket()`
- c0006 ..> c0006: `_cleanup() calls stop_watcher()`
- c0006 ..> c0006: `_close_controller() calls save()`
- c0006 ..> c0006: `_finish_observation() calls save()`
- c0006 ..> c0006: `_reject_controller_event() calls save()`
- c0006 ..> c0006: `_reject_controller_event() calls stop_watcher()`
- c0006 ..> c0006: `_start_controller() calls observe()`
- c0006 ..> c0006: `control() calls start_watcher()`
- c0006 ..> c0006: `control() calls stop_watcher()`
- c0006 ..> c0006: `observe() calls _apply_controller_event()`
- c0006 ..> c0006: `observe() calls _finish_observation()`
- c0006 ..> c0006: `observe() calls _reject_controller_event()`
- c0006 ..> c0006: `observe() calls _validate_readiness()`
- c0006 ..> c0006: `relay() calls _relay_request()`
- c0006 ..> c0006: `run() calls _await_readiness()`
- c0006 ..> c0006: `run() calls _cleanup()`
- c0006 ..> c0006: `run() calls _complete_handover()`
- c0006 ..> c0006: `run() calls _start_controller()`
- c0006 ..> c0006: `run() calls save()`
- c0006 ..> c0006: `start_watcher() calls reap_watcher()`
- c0006 ..> c0006: `start_watcher() calls relay()`
- c0006 ..> c0006: `start_watcher() calls stop_watcher()`
- c0006 ..> c0007: `observe() calls _controller_event()`
- c0006 ..> c0007: `relay() calls _watcher_request()`
- c0006 ..> c0023: `__init__() constructs AgentShellLifecycleDeadlines`
- c0006 ..> c0023: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0006 ..> c0049: `_complete_handover() calls write()`
- c0006 ..> c0049: `_relay_request() calls write()`
- c0006 ..> c0049: `_start_controller() calls write()`
- c0006 ..> c0049: `control() calls write()`
- c0006 ..> c0049: `relay() calls write()`
- c0006 ..> c0049: `run() calls write()`
- c0006 ..> c0051: `_apply_controller_problem() calls quote()`
- c0006 ..> c0101: `_start_controller() calls create_task()`
- c0006 ..> c0101: `start_watcher() calls create_task()`
- c0006 ..> c0115: `_apply_controller_problem() constructs FactoryError`
- c0006 ..> c0115: `_await_readiness() constructs FactoryError`
- c0006 ..> c0115: `_complete_handover() constructs FactoryError`
- c0006 ..> c0115: `_finish_observation() constructs FactoryError`
- c0006 ..> c0115: `_reject_controller_event() constructs FactoryError`
- c0006 ..> c0115: `_relay_request() constructs FactoryError`
- c0006 ..> c0115: `control() constructs FactoryError`
- c0006 ..> c0115: `observe() constructs FactoryError`
- c0006 ..> c0115: `reap_watcher() constructs FactoryError`
- c0006 ..> c0115: `start_watcher() constructs FactoryError`
- c0006 ..> c0118: `save() calls replace_generated_json()`
- c0007 ..> c0000: `_acquire_owner_lock() calls close()`
- c0007 ..> c0000: `_prepare_owner_startup() calls close()`
- c0007 ..> c0000: `entrypoint() calls close()`
- c0007 ..> c0004: `_prepare_owner_startup() calls runtime_directory()`
- c0007 ..> c0006: `entrypoint() calls run()`
- c0007 ..> c0006: `main() calls run()`
- c0007 ..> c0006: `main() constructs ForemanOwner`
- c0007 ..> c0007: `_controller_event() calls _validate_target()`
- c0007 ..> c0007: `_prepare_owner_startup() calls _acquire_owner_lock()`
- c0007 ..> c0007: `entrypoint() calls _prepare_owner_startup()`
- c0007 ..> c0007: `entrypoint() calls _report_startup_error()`
- c0007 ..> c0007: `entrypoint() calls main()`
- c0007 ..> c0009: `_prepare_owner_startup() calls read_state()`
- c0007 ..> c0051: `_acquire_owner_lock() calls quote()`
- c0007 ..> c0101: `main() calls create_task()`
- c0007 ..> c0115: `_acquire_owner_lock() constructs FactoryError`
- c0007 ..> c0115: `_prepare_owner_startup() constructs FactoryError`
- c0007 ..> c0115: `_watcher_request() constructs FactoryError`
- c0008 ..> c0009: `report() calls read_state()`
- c0008 ..> c0009: `report() calls request()`
- c0008 ..> c0009: `saved() calls read_state()`
- c0008 ..> c0009: `start() calls start_owner()`
- c0008 ..> c0009: `status() calls request()`
- c0008 ..> c0023: `__init__() constructs AgentShellLifecycleDeadlines`
- c0008 ..> c0023: `type in __init__`
- c0008 ..> c0026: `report() calls unknown_status()`
- c0008 ..> c0051: `report() calls quote()`
- c0008 ..> c0112: `type in __init__`
- c0009 ..> c0000: `start_owner() calls close()`
- c0009 ..> c0000: `start_owner() calls wait()`
- c0009 ..> c0004: `read_state() calls runtime_directory()`
- c0009 ..> c0004: `request() calls runtime_directory()`
- c0009 ..> c0004: `start_owner() calls runtime_directory()`
- c0009 ..> c0006: `start_owner() calls run()`
- c0009 ..> c0009: `request() calls _reply()`
- c0009 ..> c0009: `request() calls read_state()`
- c0009 ..> c0009: `start_owner() calls _reply()`
- c0009 ..> c0023: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0009 ..> c0023: `type in start_owner`
- c0009 ..> c0031: `request() calls connect()`
- c0009 ..> c0051: `request() calls quote()`
- c0009 ..> c0109: `start_owner() calls spec()`
- c0009 ..> c0112: `type in start_owner`
- c0009 ..> c0115: `_reply() constructs FactoryError`
- c0009 ..> c0115: `read_state() constructs FactoryError`
- c0009 ..> c0115: `request() constructs FactoryError`
- c0009 ..> c0115: `start_owner() constructs FactoryError`
- c0009 ..> c0118: `read_state() calls read_generated_json()`
- c0010 ..> c0010: `install() calls _inputs()`
- c0010 ..> c0010: `ready() calls _inputs()`
- c0010 ..> c0010: `unready() calls ready()`
- c0010 ..> c0115: `install() constructs FactoryError`
- c0010 ..> c0117: `install() calls check_uv()`
- c0010 ..> c0117: `install() calls no_installer()`
- c0010 ..> c0117: `install() calls run_install()`
- c0010 ..> c0117: `install() calls sync_fingerprint()`
- c0010 ..> c0117: `ready() calls runtime_ready()`
- c0011 ..> c0000: `close() calls close()`
- c0011 ..> c0011: `_read() calls _expect()`
- c0011 ..> c0011: `_read() calls _receive()`
- c0011 ..> c0011: `_read() calls _take()`
- c0011 ..> c0011: `send() calls _read()`
- c0011 ..> c0011: `send() calls _write()`
- c0011 ..> c0011: `start() calls _read()`
- c0011 ..> c0011: `start() calls _write()`
- c0011 ..> c0011: `wait() calls _expect()`
- c0011 ..> c0011: `wait() calls _receive()`
- c0011 ..> c0011: `wait() calls _take()`
- c0011 ..> c0023: `__init__() constructs AgentShellLifecycleDeadlines`
- c0011 ..> c0023: `type in __init__`
- c0011 --> c0024: `field received`
- c0011 ..> c0024: `_take() constructs ForemanReply`
- c0011 ..> c0024: `type in wait`
- c0011 ..> c0033: `startup_hint() calls how_to_reach()`
- c0011 ..> c0038: `type in __init__`
- c0011 ..> c0049: `_receive() calls read()`
- c0011 ..> c0049: `_write() calls write()`
- c0011 ..> c0109: `start() calls spec()`
- c0011 ..> c0112: `type in __init__`
- c0011 ..> c0115: `_expect() constructs FactoryError`
- c0011 ..> c0115: `_read() constructs FactoryError`
- c0011 ..> c0115: `_receive() constructs FactoryError`
- c0011 ..> c0115: `_take() constructs FactoryError`
- c0011 ..> c0115: `_write() constructs FactoryError`
- c0011 ..> c0115: `close() constructs FactoryError`
- c0011 ..> c0115: `start() constructs FactoryError`
- c0011 ..> c0123: `_read() calls check_watch_stop()`
- c0011 ..> c0123: `_write() calls check_watch_stop()`
- c0011 ..> c0123: `wait() calls check_watch_stop()`
- c0012 ..> c0000: `pin_worker() calls close()`
- c0013 ..> c0013: `_validate_agent() calls _local_selection()`
- c0013 ..> c0013: `_validate_roster() calls _local_selection()`
- c0013 ..> c0013: `_validate_roster() calls relative_path()`
- c0013 ..> c0013: `foreman_launch() calls read_definition()`
- c0013 ..> c0013: `foreman_launch() calls relative_path()`
- c0013 ..> c0013: `read_definition() calls _validate_agent()`
- c0013 ..> c0013: `read_definition() calls _validate_resources()`
- c0013 ..> c0013: `read_definition() calls _validate_roster()`
- c0013 ..> c0115: `foreman_launch() constructs FactoryError`
- c0013 ..> c0115: `read_definition() constructs FactoryError`
- c0013 ..> c0121: `_local_selection() calls nonblank()`
- c0013 ..> c0121: `_validate_agent() calls nonblank()`
- c0013 ..> c0121: `foreman_launch() calls nonblank()`
- c0013 ..> c0121: `relative_path() calls nonblank()`
- c0014 ..> c0013: `selected_launch() calls foreman_launch()`
- c0014 ..> c0014: `choose_pi_home() calls pi_home()`
- c0014 ..> c0014: `choose_pi_home() calls require_pi_home()`
- c0014 ..> c0014: `list_models() calls pi_home()`
- c0014 ..> c0014: `list_models() calls require_pi_home()`
- c0014 ..> c0014: `prepare() calls _install_resources()`
- c0014 ..> c0014: `prepare() calls _protect_runtime()`
- c0014 ..> c0014: `prepare() calls save_pi_choice()`
- c0014 ..> c0014: `prepare() calls validate_guidance()`
- c0014 ..> c0014: `prepare_roles() calls list_models()`
- c0014 ..> c0014: `prepare_roles() calls pi_home()`
- c0014 ..> c0014: `prepare_roles() calls prepare()`
- c0014 ..> c0014: `prepare_roles() calls validate_worker_models()`
- c0014 ..> c0014: `record_completion() calls selected_launch()`
- c0014 ..> c0014: `selected_launch() calls validate_setup()`
- c0014 ..> c0014: `validate_guidance() calls _read_guidance()`
- c0014 ..> c0014: `validate_setup() calls pi_home()`
- c0014 ..> c0014: `validate_setup() calls require_pi_home()`
- c0014 ..> c0014: `validate_setup() calls validate_bundled_resources()`
- c0014 ..> c0014: `validate_setup() calls validate_guidance()`
- c0014 ..> c0014: `validate_worker_models() calls list_models()`
- c0014 ..> c0015: `prepare_roles() calls validate_depth()`
- c0014 ..> c0015: `prepare_roles() constructs CoordinatorProfiles`
- c0014 ..> c0015: `validate_setup() calls validate_depth()`
- c0014 ..> c0015: `validate_setup() constructs CoordinatorProfiles`
- c0014 ..> c0017: `pi_home() calls saved_pi_home()`
- c0014 ..> c0019: `_install_resources() calls bundled_files()`
- c0014 ..> c0021: `selected_launch() calls selected_skill_files()`
- c0014 ..> c0025: `type in prepare_roles`
- c0014 ..> c0025: `type in validate_worker_models`
- c0014 ..> c0047: `choose_pi_home() calls confirm()`
- c0014 ..> c0049: `_protect_runtime() calls write()`
- c0014 ..> c0051: `require_pi_home() calls quote()`
- c0014 ..> c0085: `validate_setup() calls missing_tools()`
- c0014 ..> c0099: `list_models() calls role_environment()`
- c0014 ..> c0104: `type in __init__`
- c0014 ..> c0104: `type in list_models`
- c0014 ..> c0104: `type in prepare_roles`
- c0014 ..> c0104: `type in record_completion`
- c0014 ..> c0104: `type in selected_launch`
- c0014 ..> c0104: `type in validate_setup`
- c0014 ..> c0104: `type in validate_worker_models`
- c0014 ..> c0115: `_install_resources() constructs FactoryError`
- c0014 ..> c0115: `_read_guidance() constructs FactoryError`
- c0014 ..> c0115: `choose_pi_home() constructs FactoryError`
- c0014 ..> c0115: `list_models() constructs FactoryError`
- c0014 ..> c0115: `prepare_roles() constructs FactoryError`
- c0014 ..> c0115: `prepare_setup_guidance() constructs FactoryError`
- c0014 ..> c0115: `require_pi_home() constructs FactoryError`
- c0014 ..> c0115: `selected_launch() constructs FactoryError`
- c0014 ..> c0115: `validate_bundled_resources() constructs FactoryError`
- c0014 ..> c0115: `validate_completion() constructs FactoryError`
- c0014 ..> c0115: `validate_guidance() constructs FactoryError`
- c0014 ..> c0115: `validate_setup() constructs FactoryError`
- c0014 ..> c0115: `validate_worker_models() constructs FactoryError`
- c0014 ..> c0116: `require_pi_home() calls executable_path()`
- c0014 ..> c0118: `_install_resources() calls write_new()`
- c0014 ..> c0118: `_protect_runtime() calls write_new()`
- c0014 ..> c0118: `begin_setup() calls remove_generated()`
- c0014 ..> c0118: `prepare() calls write_new()`
- c0014 ..> c0118: `prepare_roles() calls check_real_path()`
- c0014 ..> c0118: `prepare_setup_guidance() calls write_new()`
- c0014 ..> c0118: `record_completion() calls replace_generated_json()`
- c0014 ..> c0118: `save_pi_choice() calls write_json()`
- c0014 ..> c0118: `validate_bundled_resources() calls check_real_path()`
- c0014 ..> c0118: `validate_completion() calls read_generated_json()`
- c0014 ..> c0120: `list_models() calls run_owned()`
- c0015 ..> c0014: `prepare() calls prepare()`
- c0015 ..> c0015: `prepare() calls _write_agent()`
- c0015 ..> c0015: `prepare() calls _write_foreman_memory()`
- c0015 ..> c0015: `prepare() calls validate_guidance()`
- c0015 ..> c0016: `prepare() calls selected_resources()`
- c0015 ..> c0022: `__init__() constructs WorkerProfiles`
- c0015 ..> c0115: `_write_foreman_memory() constructs FactoryError`
- c0015 ..> c0115: `prepare() constructs FactoryError`
- c0015 ..> c0115: `validate_depth() constructs FactoryError`
- c0015 ..> c0115: `validate_guidance() constructs FactoryError`
- c0015 ..> c0118: `_write_agent() calls write_definition()`
- c0015 ..> c0118: `_write_foreman_memory() calls read_generated_json()`
- c0015 ..> c0118: `_write_foreman_memory() calls write_json()`
- c0015 ..> c0118: `prepare() calls check_skill_file()`
- c0015 ..> c0118: `prepare() calls write_new()`
- c0017 ..> c0115: `saved_pi_home() constructs FactoryError`
- c0017 ..> c0118: `saved_pi_home() calls read_generated_json()`
- c0019 ..> c0018: `plan_update() constructs ResourceUpdate`
- c0019 ..> c0018: `type in _back_up`
- c0019 ..> c0018: `type in apply_update`
- c0019 ..> c0018: `type in plan_update`
- c0019 ..> c0019: `apply_update() calls _back_up()`
- c0019 ..> c0019: `bundled_files() calls _digest()`
- c0019 ..> c0019: `plan_update() calls _digest()`
- c0019 ..> c0019: `plan_update() calls bundled_files()`
- c0019 ..> c0049: `apply_update() calls write()`
- c0019 ..> c0049: `bundled_files() calls read()`
- c0019 ..> c0115: `bundled_files() constructs FactoryError`
- c0019 ..> c0115: `plan_update() constructs FactoryError`
- c0019 ..> c0118: `plan_update() calls check_real_path()`
- c0020 ..> c0017: `unready() calls saved_pi_home()`
- c0020 ..> c0020: `unready() calls ready()`
- c0020 ..> c0116: `absent() calls executable_path()`
- c0020 ..> c0116: `unready() calls executable_path()`
- c0020 ..> c0117: `install() calls install_locks()`
- c0020 ..> c0117: `install() calls no_installer()`
- c0020 ..> c0117: `install() calls require_manager()`
- c0020 ..> c0117: `install() calls run_install()`
- c0020 ..> c0117: `ready() calls install_environment()`
- c0020 ..> c0117: `ready() calls sync_fingerprint()`
- c0020 ..> c0120: `ready() calls run_owned()`
- c0021 ..> c0000: `_add_skill_file() calls close()`
- c0021 ..> c0021: `_walk_skill_directory() calls _add_skill_file()`
- c0021 ..> c0021: `selected_skill_files() calls _add_skill_file()`
- c0021 ..> c0021: `selected_skill_files() calls _walk_skill_directory()`
- c0021 ..> c0115: `_add_skill_file() constructs FactoryError`
- c0021 ..> c0115: `_walk_skill_directory() constructs FactoryError`
- c0021 ..> c0115: `selected_skill_files() constructs FactoryError`
- c0022 ..> c0025: `type in prepare`
- c0022 ..> c0054: `prepare() calls update()`
- c0022 ..> c0118: `prepare() calls check_skill_file()`
- c0022 ..> c0118: `prepare() calls write_definition()`
- c0022 ..> c0118: `prepare() calls write_new()`
- c0023 ..> c0121: `__post_init__() calls positive_duration()`
- c0026 ..> c0025: `type in _validate_foreman_memory`
- c0026 ..> c0025: `type in validate_initial_agents`
- c0026 ..> c0025: `type in validate_workers`
- c0026 ..> c0026: `validate_initial_agents() calls _validate_foreman_memory()`
- c0026 ..> c0026: `validate_initial_agents() calls validate_role_app()`
- c0026 ..> c0026: `validate_initial_agents() calls validate_workers()`
- c0026 ..> c0026: `validate_workers() calls validate_role_app()`
- c0026 ..> c0115: `_validate_foreman_memory() constructs FactoryError`
- c0026 ..> c0115: `skill_paths() constructs FactoryError`
- c0026 ..> c0115: `validate_initial_agents() constructs FactoryError`
- c0026 ..> c0115: `validate_role_app() constructs FactoryError`
- c0026 ..> c0115: `validate_workers() constructs FactoryError`
- c0026 ..> c0121: `_validate_foreman_memory() calls nonblank()`
- c0026 ..> c0121: `skill_paths() calls nonblank()`
- c0026 ..> c0121: `validate_initial_agents() calls nonblank()`
- c0026 ..> c0121: `validate_workers() calls nonblank()`
- c0027 ..> c0025: `type in prepare_roles`
- c0027 ..> c0104: `type in list_models`
- c0027 ..> c0104: `type in prepare_roles`
- c0027 ..> c0104: `type in record_completion`
- c0027 ..> c0104: `type in selected_launch`
- c0028 ..> c0024: `type in wait`
- c0030 ..> c0000: `_end() calls wait()`
- c0030 ..> c0000: `_pump() calls send()`
- c0030 ..> c0030: `_end() calls close()`
- c0030 ..> c0030: `_lost() calls _end()`
- c0030 ..> c0030: `_pump() calls _end()`
- c0030 ..> c0030: `_pump() calls _lost()`
- c0030 ..> c0030: `_pump() calls _read()`
- c0030 ..> c0030: `_send() calls _pump()`
- c0030 ..> c0030: `close() calls _end()`
- c0030 ..> c0030: `close() calls _read()`
- c0030 ..> c0030: `close() calls _send()`
- c0030 ..> c0030: `mark() calls _send()`
- c0030 ..> c0030: `online() calls _send()`
- c0030 ..> c0030: `post() calls _send()`
- c0030 ..> c0030: `receive() calls _pump()`
- c0030 ..> c0030: `start() calls _send()`
- c0030 ..> c0030: `start() calls close()`
- c0030 --> c0034: `field inbox`
- c0030 ..> c0034: `_read() constructs ChatMessage`
- c0030 ..> c0034: `type in receive`
- c0030 ..> c0035: `type in mark`
- c0030 ..> c0036: `type in __init__`
- c0030 ..> c0114: `start() calls find_secret()`
- c0031 ..> c0000: `__init__() calls __init__()`
- c0031 ..> c0000: `connect() calls close()`
- c0031 ..> c0000: `connect() calls start()`
- c0031 ..> c0000: `post() calls wait()`
- c0031 ..> c0000: `run() calls close()`
- c0031 ..> c0000: `run() calls wait()`
- c0031 ..> c0000: `send() calls send()`
- c0031 ..> c0031: `connect() calls problem()`
- c0031 ..> c0031: `connected() calls tell()`
- c0031 ..> c0031: `count_missed() calls addressed()`
- c0031 ..> c0031: `count_missed() calls problem()`
- c0031 ..> c0031: `count_missed() calls send()`
- c0031 ..> c0031: `listen() calls problem()`
- c0031 ..> c0031: `listen() calls stop()`
- c0031 ..> c0031: `post() calls count_missed()`
- c0031 ..> c0031: `post() calls problem()`
- c0031 ..> c0031: `problem() calls tell()`
- c0031 ..> c0031: `received() calls addressed()`
- c0031 ..> c0031: `received() calls tell()`
- c0031 ..> c0031: `run() calls connect()`
- c0031 ..> c0031: `run() calls listen()`
- c0031 ..> c0031: `run() calls post()`
- c0031 ..> c0031: `run() calls stop()`
- c0031 ..> c0032: `connect() calls client_type()`
- c0031 ..> c0032: `connect() calls intents()`
- c0031 ..> c0032: `send() calls split_reply()`
- c0031 ..> c0049: `tell() calls write()`
- c0031 ..> c0064: `stop() calls clear()`
- c0031 ..> c0101: `run() calls create_task()`
- c0032 ..> c0000: `serve() calls close()`
- c0032 ..> c0031: `main() calls run()`
- c0032 ..> c0031: `serve() calls run()`
- c0032 ..> c0031: `serve() constructs Relay`
- c0032 ..> c0032: `main() calls serve()`
- c0032 ..> c0049: `serve() calls write()`
- c0033 ..> c0109: `how_to_reach() calls how_to_attach()`
- c0033 ..> c0109: `open() calls enter()`
- c0033 ..> c0112: `type in __init__`
- c0037 ..> c0036: `discord_from_mapping() constructs DiscordSettings`
- c0037 ..> c0036: `type in discord_from_mapping`
- c0037 ..> c0036: `type in secret_names`
- c0037 ..> c0115: `discord_from_mapping() constructs FactoryError`
- c0039 ..> c0034: `type in receive`
- c0039 ..> c0035: `type in mark`
- c0040 ..> c0004: `prepare_foreman_launch() calls factory_launcher()`
- c0040 ..> c0008: `build_owner() constructs AgentShellOwner`
- c0040 ..> c0008: `type in build_owner`
- c0040 ..> c0010: `build_tools() constructs AgentShellRuntimeInstall`
- c0040 ..> c0011: `build_watcher() constructs AgentShellTerminal`
- c0040 ..> c0014: `build_team() constructs PiAgentTeam`
- c0040 ..> c0014: `build_watcher() calls managed_memory_notice()`
- c0040 ..> c0014: `prepare_foreman_launch() calls pi_home()`
- c0040 ..> c0014: `prepare_foreman_launch() calls selected_launch()`
- c0040 ..> c0014: `prepare_foreman_launch() calls validate_completion()`
- c0040 ..> c0014: `type in build_team`
- c0040 ..> c0020: `build_tools() constructs PiInstall`
- c0040 ..> c0030: `build_chat() constructs DiscordLink`
- c0040 ..> c0030: `type in build_chat`
- c0040 ..> c0033: `build_channel() constructs TerminalChannel`
- c0040 ..> c0033: `type in build_channel`
- c0040 ..> c0037: `build_team() calls secret_names()`
- c0040 ..> c0037: `prepare_foreman_launch() calls secret_names()`
- c0040 ..> c0040: `build_channel() calls build_host()`
- c0040 ..> c0040: `build_initialiser() calls build_team()`
- c0040 ..> c0040: `build_owner() calls build_host()`
- c0040 ..> c0040: `build_start_foreman() calls build_channel()`
- c0040 ..> c0040: `build_start_foreman() calls build_owner()`
- c0040 ..> c0040: `build_team() calls build_tools()`
- c0040 ..> c0040: `build_watch_status() calls build_owner()`
- c0040 ..> c0040: `build_watch_status() calls build_team()`
- c0040 ..> c0040: `build_watcher() calls build_channel()`
- c0040 ..> c0040: `build_watcher() calls build_chat()`
- c0040 ..> c0040: `build_watcher() calls build_host()`
- c0040 ..> c0040: `build_watcher() calls prepare_foreman_launch()`
- c0040 ..> c0040: `build_watcher() calls select_ticketing()`
- c0040 ..> c0040: `prepare_foreman_launch() calls build_team()`
- c0040 ..> c0041: `build_initialiser() constructs DeadlinePolicy`
- c0040 ..> c0041: `build_owner() constructs DeadlinePolicy`
- c0040 ..> c0041: `build_start_foreman() constructs DeadlinePolicy`
- c0040 ..> c0041: `build_watch_status() constructs DeadlinePolicy`
- c0040 ..> c0041: `build_watcher() constructs DeadlinePolicy`
- c0040 ..> c0041: `type in build_initialiser`
- c0040 ..> c0041: `type in build_owner`
- c0040 ..> c0041: `type in build_start_foreman`
- c0040 ..> c0041: `type in build_watch_status`
- c0040 ..> c0041: `type in build_watcher`
- c0040 ..> c0047: `build_watcher() constructs FileCleanupReceipts`
- c0040 ..> c0050: `build_initialiser() constructs TomlConfigurationStore`
- c0040 ..> c0050: `build_watch_status() constructs TomlConfigurationStore`
- c0040 ..> c0052: `build_start_foreman() constructs WorkspaceWatchLease`
- c0040 ..> c0053: `build_watcher() constructs ObservedTerminal`
- c0040 ..> c0056: `type in build_chat`
- c0040 ..> c0056: `type in build_watcher`
- c0040 ..> c0056: `type in prepare_foreman_launch`
- c0040 ..> c0056: `type in select_ticketing`
- c0040 ..> c0077: `build_watcher() constructs CleanupCompleted`
- c0040 ..> c0084: `build_initialiser() constructs InitialiseFactory`
- c0040 ..> c0084: `type in build_initialiser`
- c0040 ..> c0085: `build_team() calls missing_tools()`
- c0040 ..> c0086: `build_watcher() constructs ScaffoldIssue`
- c0040 ..> c0088: `build_start_foreman() constructs StartForeman`
- c0040 ..> c0088: `type in build_start_foreman`
- c0040 ..> c0090: `build_watcher() constructs WatchFactory`
- c0040 ..> c0090: `type in build_watcher`
- c0040 ..> c0093: `build_watch_status() constructs WatchStatus`
- c0040 ..> c0093: `type in build_watch_status`
- c0040 ..> c0094: `build_initialiser() constructs GitHubForge`
- c0040 ..> c0094: `build_watcher() constructs GitHubForge`
- c0040 ..> c0099: `prepare_foreman_launch() calls role_environment()`
- c0040 ..> c0100: `build_tools() constructs ForgetfulInstall`
- c0040 ..> c0101: `build_watcher() constructs ForgetfulPlanStore`
- c0040 ..> c0103: `build_initialiser() constructs ForgetfulSetup`
- c0040 ..> c0104: `type in build_tools`
- c0040 ..> c0109: `build_host() constructs TmuxHost`
- c0040 ..> c0109: `type in build_host`
- c0040 ..> c0110: `build_tools() constructs TmuxInstall`
- c0040 ..> c0115: `build_watcher() constructs FactoryError`
- c0040 ..> c0115: `prepare_foreman_launch() constructs FactoryError`
- c0040 ..> c0115: `select_ticketing() constructs FactoryError`
- c0040 ..> c0124: `build_initialiser() constructs GitHubTicketing`
- c0040 ..> c0124: `build_watcher() calls check_ready()`
- c0040 ..> c0124: `select_ticketing() calls validate_source()`
- c0040 ..> c0128: `type in select_ticketing`
- c0040 ..> c0129: `build_initialiser() constructs GitRepositories`
- c0040 ..> c0129: `build_watcher() constructs GitRepositories`
- c0040 ..> c0131: `build_watcher() constructs GitWorktrees`
- c0041 --> c0023: `field agentshell`
- c0041 ..> c0121: `__post_init__() calls positive_duration()`
- c0042 --> c0056: `field config`
- c0042 --> c0104: `field connection`
- c0043 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0043 ..> c0006: `_foreman() calls run()`
- c0043 ..> c0006: `_watch_locked() calls run()`
- c0043 ..> c0008: `_watch_status() calls report()`
- c0043 ..> c0009: `_change_managed_watch() calls request()`
- c0043 ..> c0009: `_finish_existing_setup() calls read_state()`
- c0043 ..> c0009: `_initialise() calls request()`
- c0043 ..> c0009: `_initialise_locked() calls read_state()`
- c0043 ..> c0009: `_launch_setup_foreman() calls start_owner()`
- c0043 ..> c0009: `_offer_factory_launch() calls read_state()`
- c0043 ..> c0009: `_watch_locked() calls read_state()`
- c0043 ..> c0014: `_complete_setup() calls managed_memory_notice()`
- c0043 ..> c0014: `_complete_setup() calls record_completion()`
- c0043 ..> c0014: `_discover_worker_models() calls list_models()`
- c0043 ..> c0014: `_finish_existing_setup() calls choose_pi_home()`
- c0043 ..> c0014: `_finish_existing_setup() calls save_pi_choice()`
- c0043 ..> c0014: `_finish_existing_setup() calls selected_launch()`
- c0043 ..> c0014: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0043 ..> c0014: `_select_model() calls list_models()`
- c0043 ..> c0014: `_start_initial_setup() calls begin_setup()`
- c0043 ..> c0014: `_start_initial_setup() calls choose_pi_home()`
- c0043 ..> c0014: `_validate_initial_model() calls prepare_roles()`
- c0043 ..> c0025: `_configure_new_factory() constructs InitialAgentChoices`
- c0043 ..> c0025: `type in _configure_new_factory`
- c0043 ..> c0025: `type in _foreman_memory_choices`
- c0043 ..> c0025: `type in _owner_choices`
- c0043 ..> c0025: `type in _prompt_coordinator_choices`
- c0043 ..> c0025: `type in _validate_initial_model`
- c0043 ..> c0025: `type in _worker_choices`
- c0043 ..> c0026: `_start_initial_setup() calls validate_initial_agents()`
- c0043 ..> c0040: `_foreman() calls build_start_foreman()`
- c0043 ..> c0040: `_initialise() calls build_channel()`
- c0043 ..> c0040: `_initialise_locked() calls build_initialiser()`
- c0043 ..> c0040: `_launch_setup_foreman() calls build_host()`
- c0043 ..> c0040: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0043 ..> c0040: `_watch_locked() calls build_watcher()`
- c0043 ..> c0040: `_watch_status() calls build_watch_status()`
- c0043 ..> c0041: `main() constructs DeadlinePolicy`
- c0043 ..> c0041: `type in _finish_existing_setup`
- c0043 ..> c0041: `type in _foreman`
- c0043 ..> c0041: `type in _initialise`
- c0043 ..> c0041: `type in _initialise_locked`
- c0043 ..> c0041: `type in _start_initial_setup`
- c0043 ..> c0041: `type in _watch`
- c0043 ..> c0041: `type in _watch_locked`
- c0043 ..> c0041: `type in _watch_status`
- c0043 ..> c0041: `type in main`
- c0043 ..> c0042: `_start_initial_setup() constructs _InitialSetupState`
- c0043 ..> c0042: `type in _discover_worker_models`
- c0043 ..> c0042: `type in _validate_initial_model`
- c0043 ..> c0043: `_complete_setup() calls _managed_rest_mapping_available()`
- c0043 ..> c0043: `_configure_new_factory() calls _prepare_foreman()`
- c0043 ..> c0043: `_configure_new_factory() calls _select_model()`
- c0043 ..> c0043: `_configure_new_factory() calls _select_numbered()`
- c0043 ..> c0043: `_configure_new_factory() calls select_repositories()`
- c0043 ..> c0043: `_connection() calls _check_existing_connection()`
- c0043 ..> c0043: `_discover_worker_models() calls _prepare_foreman()`
- c0043 ..> c0043: `_finish_existing_setup() calls _complete_setup()`
- c0043 ..> c0043: `_finish_existing_setup() calls _confirm_pi_home()`
- c0043 ..> c0043: `_finish_existing_setup() calls _connection()`
- c0043 ..> c0043: `_finish_existing_setup() calls _launch_setup_foreman()`
- c0043 ..> c0043: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0043 ..> c0043: `_foreman_memory_choices() calls _select_numbered()`
- c0043 ..> c0043: `_initialise() calls _initialise_locked()`
- c0043 ..> c0043: `_initialise() calls _offer_factory_launch()`
- c0043 ..> c0043: `_initialise_locked() calls _finish_existing_setup()`
- c0043 ..> c0043: `_initialise_locked() calls _start_initial_setup()`
- c0043 ..> c0043: `_initialise_locked() calls _validate_setup_owner()`
- c0043 ..> c0043: `_print_models() calls _safe_diagnostic()`
- c0043 ..> c0043: `_prompt_coordinator_choices() calls _select_numbered()`
- c0043 ..> c0043: `_prompt_worker() calls _select_numbered()`
- c0043 ..> c0043: `_prompt_workers() calls _prompt_worker()`
- c0043 ..> c0043: `_select_model() calls _print_models()`
- c0043 ..> c0043: `_select_model() calls _select_numbered()`
- c0043 ..> c0043: `_select_numbered() calls _safe_diagnostic()`
- c0043 ..> c0043: `_select_project() calls _listed_project_id()`
- c0043 ..> c0043: `_select_project() calls _safe_diagnostic()`
- c0043 ..> c0043: `_select_setup_route() calls _select_numbered()`
- c0043 ..> c0043: `_start_initial_setup() calls _complete_setup()`
- c0043 ..> c0043: `_start_initial_setup() calls _configure_new_factory()`
- c0043 ..> c0043: `_start_initial_setup() calls _confirm_pi_home()`
- c0043 ..> c0043: `_start_initial_setup() calls _connection()`
- c0043 ..> c0043: `_start_initial_setup() calls _foreman_memory_choices()`
- c0043 ..> c0043: `_start_initial_setup() calls _launch_setup_foreman()`
- c0043 ..> c0043: `_start_initial_setup() calls _owner_choices()`
- c0043 ..> c0043: `_start_initial_setup() calls _research_choices()`
- c0043 ..> c0043: `_start_initial_setup() calls _worker_choices()`
- c0043 ..> c0043: `_validate_initial_model() calls _prepare_foreman()`
- c0043 ..> c0043: `_validate_initial_model() calls _select_model()`
- c0043 ..> c0043: `_validate_initial_model() calls _select_project()`
- c0043 ..> c0043: `_watch() calls _change_managed_watch()`
- c0043 ..> c0043: `_watch() calls _watch_locked()`
- c0043 ..> c0043: `_watch() calls _watch_status()`
- c0043 ..> c0043: `_watch_locked() calls _choose_existing()`
- c0043 ..> c0043: `_watch_locked() calls _safe_diagnostic()`
- c0043 ..> c0043: `_worker_choices() calls _prompt_coordinator_choices()`
- c0043 ..> c0043: `_worker_choices() calls _prompt_workers()`
- c0043 ..> c0043: `_worker_choices() calls _select_setup_route()`
- c0043 ..> c0043: `_worker_choices() calls _worker_arguments()`
- c0043 ..> c0043: `main() calls _foreman()`
- c0043 ..> c0043: `main() calls _initialise()`
- c0043 ..> c0043: `main() calls _parse_arguments()`
- c0043 ..> c0043: `main() calls _safe_diagnostic()`
- c0043 ..> c0043: `main() calls _watch()`
- c0043 ..> c0044: `_select_numbered() calls parse_numbered_selection()`
- c0043 ..> c0045: `main() calls update_resources()`
- c0043 ..> c0046: `_watch_locked() calls load_configuration()`
- c0043 ..> c0047: `_initialise_locked() calls load()`
- c0043 ..> c0049: `_finish_existing_setup() constructs MarkdownAgreement`
- c0043 ..> c0049: `_start_initial_setup() constructs MarkdownAgreement`
- c0043 ..> c0051: `_initialise() calls quote()`
- c0043 ..> c0051: `_launch_setup_foreman() calls quote()`
- c0043 ..> c0051: `_select_model() calls quote()`
- c0043 ..> c0051: `_validate_setup_owner() calls quote()`
- c0043 ..> c0051: `_watch_locked() calls quote()`
- c0043 ..> c0052: `_initialise() calls hold()`
- c0043 ..> c0052: `_initialise() constructs WorkspaceWatchLease`
- c0043 ..> c0052: `_watch() calls hold()`
- c0043 ..> c0052: `_watch() constructs WorkspaceWatchLease`
- c0043 ..> c0054: `_prompt_workers() calls update()`
- c0043 ..> c0055: `_watch_locked() calls observe_plain_watch()`
- c0043 ..> c0056: `type in _complete_setup`
- c0043 ..> c0056: `type in _configure_new_factory`
- c0043 ..> c0056: `type in _finish_existing_setup`
- c0043 ..> c0056: `type in _validate_initial_model`
- c0043 ..> c0057: `_connection() calls validate()`
- c0043 ..> c0082: `_finish_existing_setup() calls agree_definition_of_done()`
- c0043 ..> c0082: `_start_initial_setup() calls agree_definition_of_done()`
- c0043 ..> c0084: `_complete_setup() calls check_foreman()`
- c0043 ..> c0084: `_configure_new_factory() calls configure()`
- c0043 ..> c0084: `_configure_new_factory() calls inspect()`
- c0043 ..> c0084: `_finish_existing_setup() calls initialise()`
- c0043 ..> c0084: `_initialise_locked() calls load_existing()`
- c0043 ..> c0084: `_launch_setup_foreman() calls check_foreman()`
- c0043 ..> c0084: `_prepare_foreman() calls prepare_foreman()`
- c0043 ..> c0084: `_start_initial_setup() calls initialise()`
- c0043 ..> c0084: `select_repositories() calls discover()`
- c0043 ..> c0084: `type in _complete_setup`
- c0043 ..> c0084: `type in _configure_new_factory`
- c0043 ..> c0084: `type in _discover_worker_models`
- c0043 ..> c0084: `type in _finish_existing_setup`
- c0043 ..> c0084: `type in _select_project`
- c0043 ..> c0084: `type in _start_initial_setup`
- c0043 ..> c0084: `type in _validate_initial_model`
- c0043 ..> c0084: `type in select_repositories`
- c0043 ..> c0097: `_complete_setup() calls uses_browser_login()`
- c0043 ..> c0098: `_select_project() calls create_project()`
- c0043 ..> c0098: `_select_project() calls projects()`
- c0043 ..> c0104: `_connection() constructs ForgetfulConnection`
- c0043 ..> c0104: `type in _check_existing_connection`
- c0043 ..> c0104: `type in _configure_new_factory`
- c0043 ..> c0104: `type in _connection`
- c0043 ..> c0104: `type in _foreman_memory_choices`
- c0043 ..> c0104: `type in _managed_rest_mapping_available`
- c0043 ..> c0104: `type in _select_project`
- c0043 ..> c0115: `_change_managed_watch() constructs FactoryError`
- c0043 ..> c0115: `_check_existing_connection() constructs FactoryError`
- c0043 ..> c0115: `_choose_existing() constructs FactoryError`
- c0043 ..> c0115: `_configure_new_factory() constructs FactoryError`
- c0043 ..> c0115: `_finish_existing_setup() constructs FactoryError`
- c0043 ..> c0115: `_foreman_memory_choices() constructs FactoryError`
- c0043 ..> c0115: `_initialise() constructs FactoryError`
- c0043 ..> c0115: `_initialise_locked() constructs FactoryError`
- c0043 ..> c0115: `_install_missing() constructs FactoryError`
- c0043 ..> c0115: `_listed_project_id() constructs FactoryError`
- c0043 ..> c0115: `_prompt_coordinator_choices() constructs FactoryError`
- c0043 ..> c0115: `_prompt_worker() constructs FactoryError`
- c0043 ..> c0115: `_select_model() constructs FactoryError`
- c0043 ..> c0115: `_select_project() constructs FactoryError`
- c0043 ..> c0115: `_validate_setup_owner() constructs FactoryError`
- c0043 ..> c0115: `_watch() constructs FactoryError`
- c0043 ..> c0115: `_watch_locked() constructs FactoryError`
- c0043 ..> c0115: `_worker_choices() constructs FactoryError`
- c0043 ..> c0115: `main() constructs FactoryError`
- c0043 ..> c0115: `select_repositories() constructs FactoryError`
- c0043 ..> c0118: `_discover_worker_models() calls check_real_path()`
- c0043 ..> c0123: `_watch_locked() calls watch_stop_scope()`
- c0044 ..> c0115: `parse_numbered_selection() constructs FactoryError`
- c0045 ..> c0003: `update_resources() calls ready()`
- c0045 ..> c0009: `update_resources() calls read_state()`
- c0045 ..> c0010: `update_resources() calls install()`
- c0045 ..> c0010: `update_resources() constructs AgentShellRuntimeInstall`
- c0045 ..> c0014: `update_resources() calls validate_bundled_resources()`
- c0045 ..> c0019: `update_resources() calls apply_update()`
- c0045 ..> c0019: `update_resources() calls plan_update()`
- c0045 ..> c0040: `update_resources() calls build_team()`
- c0045 ..> c0041: `type in update_resources`
- c0045 ..> c0045: `update_resources() calls _report()`
- c0045 ..> c0052: `update_resources() calls hold()`
- c0045 ..> c0052: `update_resources() constructs WorkspaceWatchLease`
- c0045 ..> c0115: `_report() constructs FactoryError`
- c0045 ..> c0115: `update_resources() constructs FactoryError`
- c0046 ..> c0047: `load_configuration() calls load()`
- c0046 ..> c0050: `load_configuration() constructs TomlConfigurationStore`
- c0046 ..> c0056: `type in load_configuration`
- c0046 ..> c0115: `load_configuration() constructs FactoryError`
- c0047 ..> c0000: `_load() calls close()`
- c0047 ..> c0047: `confirm() calls _save()`
- c0047 ..> c0047: `confirm() calls load()`
- c0047 ..> c0047: `confirm_plans() calls _save()`
- c0047 ..> c0047: `confirm_plans() calls load()`
- c0047 ..> c0047: `load() calls _load()`
- c0047 ..> c0048: `_load() calls _rows()`
- c0047 ..> c0048: `_save() calls _sorted()`
- c0047 ..> c0049: `_load() calls read()`
- c0047 ..> c0067: `type in confirm_plans`
- c0047 ..> c0069: `type in confirm`
- c0047 ..> c0071: `_load() constructs FinishedCleanup`
- c0047 ..> c0071: `type in _load`
- c0047 ..> c0071: `type in load`
- c0047 ..> c0115: `_save() constructs FactoryError`
- c0047 ..> c0115: `load() constructs FactoryError`
- c0047 ..> c0118: `_load() calls check_real_path()`
- c0047 ..> c0118: `_save() calls replace_generated_json()`
- c0047 ..> c0123: `_save() calls check_watch_stop()`
- c0047 ..> c0123: `confirm() calls check_watch_stop()`
- c0047 ..> c0123: `confirm_plans() calls check_watch_stop()`
- c0048 ..> c0048: `_rows() calls _identity()`
- c0049 ..> c0118: `found() calls check_skill_file()`
- c0049 ..> c0118: `write() calls write_new()`
- c0050 ..> c0000: `load() calls close()`
- c0050 ..> c0000: `save() calls close()`
- c0050 ..> c0047: `load() calls load()`
- c0050 ..> c0049: `save() calls write()`
- c0050 ..> c0051: `save() calls quote()`
- c0050 ..> c0056: `type in load`
- c0050 ..> c0056: `type in save`
- c0050 ..> c0057: `load() calls from_mapping()`
- c0050 ..> c0115: `load() constructs FactoryError`
- c0050 ..> c0115: `save() constructs FactoryError`
- c0052 ..> c0000: `_hold_directory() calls close()`
- c0052 ..> c0052: `hold() calls _hold_directory()`
- c0052 ..> c0115: `_hold_directory() constructs FactoryError`
- c0053 ..> c0000: `close() calls close()`
- c0053 ..> c0000: `send() calls send()`
- c0053 ..> c0000: `start() calls start()`
- c0053 ..> c0000: `startup_hint() calls startup_hint()`
- c0053 ..> c0000: `wait() calls wait()`
- c0053 ..> c0024: `type in wait`
- c0053 ..> c0026: `__init__() calls unknown_status()`
- c0053 ..> c0028: `type in __init__`
- c0053 ..> c0054: `close() calls update()`
- c0053 ..> c0054: `start() calls update()`
- c0053 ..> c0054: `type in __init__`
- c0054 ..> c0031: `__enter__() calls listen()`
- c0054 ..> c0053: `__enter__() calls start()`
- c0054 ..> c0053: `_close_resources() calls close()`
- c0054 ..> c0054: `__enter__() calls _close_resources()`
- c0054 ..> c0054: `__enter__() calls snapshot()`
- c0054 ..> c0054: `__enter__() calls update()`
- c0054 ..> c0054: `__exit__() calls _close_resources()`
- c0054 ..> c0054: `__exit__() calls _publish_history()`
- c0054 ..> c0054: `__exit__() calls snapshot()`
- c0054 ..> c0054: `__exit__() calls update()`
- c0054 ..> c0054: `_serve() calls snapshot()`
- c0054 ..> c0054: `update() calls _publish_history()`
- c0054 ..> c0055: `__enter__() calls _discovery_path()`
- c0054 ..> c0055: `__enter__() calls _endpoint()`
- c0054 ..> c0055: `_publish_history() calls _discovery_path()`
- c0054 ..> c0055: `_publish_history() calls _read_discovery()`
- c0054 ..> c0055: `_serve() calls _frame()`
- c0054 ..> c0055: `_serve() calls _peer()`
- c0054 ..> c0115: `__enter__() constructs FactoryError`
- c0054 ..> c0118: `__enter__() calls check_real_path()`
- c0054 ..> c0118: `__enter__() calls replace_generated_json()`
- c0054 ..> c0118: `_publish_history() calls replace_generated_json()`
- c0055 ..> c0026: `plain_watch_status() calls unknown_status()`
- c0055 ..> c0031: `plain_watch_status() calls connect()`
- c0055 ..> c0049: `_read_discovery() calls read()`
- c0055 ..> c0054: `observe_plain_watch() calls __enter__()`
- c0055 ..> c0054: `observe_plain_watch() calls __exit__()`
- c0055 ..> c0054: `observe_plain_watch() constructs PlainWatchObservation`
- c0055 ..> c0054: `type in observe_plain_watch`
- c0055 ..> c0055: `_frame() calls _observation_json()`
- c0055 ..> c0055: `_read_discovery() calls _discovery_path()`
- c0055 ..> c0055: `_read_discovery() calls _observation_json()`
- c0055 ..> c0055: `plain_watch_status() calls _endpoint()`
- c0055 ..> c0055: `plain_watch_status() calls _frame()`
- c0055 ..> c0055: `plain_watch_status() calls _peer()`
- c0055 ..> c0055: `plain_watch_status() calls _read_discovery()`
- c0055 ..> c0118: `_read_discovery() calls check_real_path()`
- c0056 --> c0036: `field discord`
- c0056 --> c0058: `field repository`
- c0056 --> c0104: `field forgetful`
- c0057 ..> c0037: `from_mapping() calls discord_from_mapping()`
- c0057 ..> c0056: `from_mapping() constructs FactoryConfiguration`
- c0057 ..> c0056: `type in from_mapping`
- c0057 ..> c0056: `type in validate`
- c0057 ..> c0057: `from_mapping() calls validate()`
- c0057 ..> c0058: `from_mapping() constructs RepositoryReference`
- c0057 ..> c0104: `validate() calls validate()`
- c0057 ..> c0105: `from_mapping() calls connection_from_mapping()`
- c0057 ..> c0115: `from_mapping() constructs FactoryError`
- c0057 ..> c0115: `validate() constructs FactoryError`
- c0057 ..> c0121: `unique_labels() calls nonblank()`
- c0057 ..> c0121: `validate() calls nonblank()`
- c0057 ..> c0127: `from_mapping() constructs TicketSource`
- c0058 --> c0127: `field work_source`
- c0059 --|> c0061: `inherits`
- c0060 --|> c0061: `inherits`
- c0061 --|> c0115: `inherits`
- c0062 --|> c0061: `inherits`
- c0063 --|> c0061: `inherits`
- c0064 ..> c0000: `__init__() calls __init__()`
- c0064 ..> c0000: `send() calls send()`
- c0064 ..> c0065: `send() calls _cleanup_recovery()`
- c0064 ..> c0115: `type in send`
- c0068 ..> c0067: `type in confirm_plans`
- c0068 ..> c0069: `type in confirm`
- c0068 ..> c0071: `type in load`
- c0070 ..> c0056: `type in load`
- c0070 ..> c0056: `type in save`
- c0071 --> c0067: `field plans`
- c0071 --> c0069: `field sets`
- c0074 ..> c0024: `type in _post`
- c0074 ..> c0028: `type in __init__`
- c0074 ..> c0030: `_deliver() calls mark()`
- c0074 ..> c0030: `_exchange() calls receive()`
- c0074 ..> c0030: `_post() calls post()`
- c0074 ..> c0030: `online() calls online()`
- c0074 ..> c0034: `type in _deliver`
- c0074 ..> c0039: `type in __init__`
- c0074 ..> c0074: `_exchange() calls _post()`
- c0074 ..> c0074: `_exchange() calls use_terminal()`
- c0074 ..> c0074: `_run() calls _exchange()`
- c0074 ..> c0074: `_run() calls _fail()`
- c0074 ..> c0074: `use_terminal() calls _fail()`
- c0074 ..> c0074: `use_terminal() calls check()`
- c0074 ..> c0075: `_deliver() calls send()`
- c0074 ..> c0075: `_run() calls wait()`
- c0074 ..> c0075: `online() calls start()`
- c0074 ..> c0075: `stop() calls close()`
- c0074 ..> c0076: `stop() calls stop_reason()`
- c0075 ..> c0000: `close() calls close()`
- c0075 ..> c0000: `start() calls start()`
- c0075 ..> c0000: `startup_hint() calls startup_hint()`
- c0075 ..> c0000: `wait() calls wait()`
- c0075 ..> c0024: `type in wait`
- c0075 ..> c0074: `send() calls use_terminal()`
- c0075 ..> c0074: `type in __init__`
- c0075 ..> c0074: `wait() calls check()`
- c0075 ..> c0074: `wait() calls use_terminal()`
- c0075 ..> c0075: `__init__() constructs _SharedTerminal`
- c0077 ..> c0000: `_candidates() calls send()`
- c0077 ..> c0000: `_dispose() calls send()`
- c0077 ..> c0000: `_finish_plans() calls send()`
- c0077 ..> c0000: `_read_problem() calls send()`
- c0077 ..> c0000: `_repository_identities() calls send()`
- c0077 ..> c0000: `poll() calls send()`
- c0077 ..> c0008: `_dispose() calls report()`
- c0077 ..> c0047: `_dispose() calls confirm()`
- c0077 ..> c0047: `_finish_plans() calls confirm_plans()`
- c0077 ..> c0047: `poll() calls load()`
- c0077 ..> c0054: `_candidate() calls snapshot()`
- c0077 ..> c0054: `_candidate() calls update()`
- c0077 ..> c0054: `_check_namespaces() calls update()`
- c0077 ..> c0054: `_still_completed() calls snapshot()`
- c0077 ..> c0061: `_candidate() constructs ScaffoldProblem`
- c0077 ..> c0061: `_check_namespaces() constructs ScaffoldProblem`
- c0077 ..> c0061: `_dispose() constructs ScaffoldProblem`
- c0077 ..> c0061: `_finish_plans() constructs ScaffoldProblem`
- c0077 ..> c0061: `_is_confirmed() constructs ScaffoldProblem`
- c0077 ..> c0061: `_still_completed() constructs ScaffoldProblem`
- c0077 ..> c0061: `_task_mappings() constructs ScaffoldProblem`
- c0077 ..> c0061: `_validate_claim_mapping() constructs ScaffoldProblem`
- c0077 ..> c0064: `_dispose() calls clear()`
- c0077 ..> c0064: `_finish_plans() calls clear()`
- c0077 ..> c0064: `_repository_identities() calls clear()`
- c0077 ..> c0064: `poll() calls clear()`
- c0077 ..> c0064: `type in _candidates`
- c0077 ..> c0064: `type in _claim_indexes`
- c0077 ..> c0064: `type in _dispose`
- c0077 ..> c0064: `type in _finish_plans`
- c0077 ..> c0064: `type in _read_plans`
- c0077 ..> c0064: `type in _read_problem`
- c0077 ..> c0064: `type in _repository_identities`
- c0077 ..> c0064: `type in poll`
- c0077 --> c0067: `field finished_plans`
- c0077 ..> c0067: `_plan_identity() constructs CleanupPlan`
- c0077 ..> c0067: `type in _plan_identity`
- c0077 ..> c0068: `type in __init__`
- c0077 --> c0069: `field confirmed`
- c0077 ..> c0069: `_is_confirmed() calls overlaps()`
- c0077 ..> c0069: `_mapping_identity() constructs CleanupSet`
- c0077 ..> c0069: `type in _mapping_identity`
- c0077 ..> c0077: `_candidate() calls _keys()`
- c0077 ..> c0077: `_candidates() calls _candidate()`
- c0077 ..> c0077: `_candidates() calls _open()`
- c0077 ..> c0077: `_check_namespaces() calls _keys()`
- c0077 ..> c0077: `_claim_indexes() calls _claims()`
- c0077 ..> c0077: `_claim_indexes() calls _read_problem()`
- c0077 ..> c0077: `_claim_indexes() calls _references()`
- c0077 ..> c0077: `_claims() calls _is_confirmed()`
- c0077 ..> c0077: `_claims() calls _keys()`
- c0077 ..> c0077: `_claims() calls _task_mappings()`
- c0077 ..> c0077: `_dispose() calls _check_namespaces()`
- c0077 ..> c0077: `_dispose() calls _keys()`
- c0077 ..> c0077: `_dispose() calls _mapping_identity()`
- c0077 ..> c0077: `_dispose() calls _overlaps()`
- c0077 ..> c0077: `_dispose() calls _read_problem()`
- c0077 ..> c0077: `_dispose() calls _still_completed()`
- c0077 ..> c0077: `_finish_plans() calls _plan_identity()`
- c0077 ..> c0077: `_is_confirmed() calls _mapping_identity()`
- c0077 ..> c0077: `_open() calls _in_scope()`
- c0077 ..> c0077: `_open() calls _plan_identity()`
- c0077 ..> c0077: `_read_plans() calls _read_problem()`
- c0077 ..> c0077: `_still_completed() calls _in_scope()`
- c0077 ..> c0077: `_task_mappings() calls _validate_claim_mapping()`
- c0077 ..> c0077: `poll() calls _candidates()`
- c0077 ..> c0077: `poll() calls _check_summaries()`
- c0077 ..> c0077: `poll() calls _claim_indexes()`
- c0077 ..> c0077: `poll() calls _dispose()`
- c0077 ..> c0077: `poll() calls _finish_plans()`
- c0077 ..> c0077: `poll() calls _is_confirmed()`
- c0077 ..> c0077: `poll() calls _mapping_identity()`
- c0077 ..> c0077: `poll() calls _open()`
- c0077 ..> c0077: `poll() calls _order()`
- c0077 ..> c0077: `poll() calls _read_plans()`
- c0077 ..> c0077: `poll() calls _references()`
- c0077 ..> c0077: `poll() calls _repository_identities()`
- c0077 ..> c0078: `_candidate() constructs CompletedWork`
- c0077 ..> c0078: `type in _candidate`
- c0077 ..> c0078: `type in _candidates`
- c0077 ..> c0078: `type in _dispose`
- c0077 ..> c0078: `type in _finish_plans`
- c0077 ..> c0078: `type in _order`
- c0077 ..> c0078: `type in _still_completed`
- c0077 ..> c0079: `_candidate() calls _claim_path()`
- c0077 ..> c0079: `_claims() calls _claim_path()`
- c0077 ..> c0079: `_dispose() calls _claim_path()`
- c0077 ..> c0079: `_keys() calls _claim_path()`
- c0077 ..> c0079: `_overlaps() calls _claim_path()`
- c0077 ..> c0079: `_repository_identities() calls _claim_path()`
- c0077 ..> c0083: `_candidate() calls check_source()`
- c0077 ..> c0083: `_candidate() calls context()`
- c0077 ..> c0083: `_candidate() calls mapping_repository()`
- c0077 ..> c0083: `_candidate() calls ownership_records()`
- c0077 ..> c0083: `_dispose() calls check_repository()`
- c0077 ..> c0083: `_dispose() calls mapping_repository()`
- c0077 ..> c0083: `_still_completed() calls context()`
- c0077 ..> c0083: `_still_completed() calls ownership()`
- c0077 ..> c0083: `type in __init__`
- c0077 ..> c0101: `_candidates() calls tasks()`
- c0077 ..> c0101: `_claim_indexes() calls tasks()`
- c0077 ..> c0101: `_in_scope() calls owns()`
- c0077 ..> c0101: `_mapping_identity() calls backend_identity()`
- c0077 ..> c0101: `_plan_identity() calls backend_identity()`
- c0077 ..> c0101: `_read_plans() calls get_plan()`
- c0077 ..> c0101: `_still_completed() calls get_plan()`
- c0077 ..> c0101: `poll() calls plans()`
- c0077 ..> c0107: `_check_summaries() constructs PlanningReadError`
- c0077 ..> c0115: `type in _read_problem`
- c0077 ..> c0124: `_in_scope() calls could_be_key()`
- c0077 ..> c0128: `type in __init__`
- c0077 ..> c0131: `_claims() calls repository_identity()`
- c0077 ..> c0131: `_dispose() calls dispose()`
- c0077 ..> c0131: `_repository_identities() calls repository_identity()`
- c0077 ..> c0131: `poll() calls begin_cleanup_cycle()`
- c0077 ..> c0136: `type in __init__`
- c0081 ..> c0080: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0081 ..> c0094: `validate_cleanup_marker() calls is_change_request()`
- c0081 ..> c0095: `type in validate_cleanup_marker`
- c0081 ..> c0096: `type in validate_cleanup_marker`
- c0082 ..> c0049: `agree_definition_of_done() calls found()`
- c0082 ..> c0049: `agree_definition_of_done() calls read()`
- c0082 ..> c0049: `agree_definition_of_done() calls write()`
- c0082 ..> c0056: `type in agree_definition_of_done`
- c0082 ..> c0066: `type in agree_definition_of_done`
- c0082 ..> c0082: `agree_definition_of_done() calls _deployment_agreement()`
- c0082 ..> c0115: `_deployment_agreement() constructs FactoryError`
- c0082 ..> c0115: `agree_definition_of_done() constructs FactoryError`
- c0083 ..> c0056: `type in __init__`
- c0083 ..> c0058: `type in check_repository`
- c0083 ..> c0058: `type in check_source`
- c0083 ..> c0058: `type in mapping_repository`
- c0083 ..> c0060: `check_repository() constructs RepositoryProblem`
- c0083 ..> c0060: `check_source() constructs RepositoryProblem`
- c0083 ..> c0061: `active() constructs ScaffoldProblem`
- c0083 ..> c0061: `context() constructs ScaffoldProblem`
- c0083 ..> c0061: `mapping_repository() constructs ScaffoldProblem`
- c0083 ..> c0061: `ownership_records() constructs ScaffoldProblem`
- c0083 ..> c0061: `snapshot() constructs ScaffoldProblem`
- c0083 ..> c0083: `check_repository() calls check_source()`
- c0083 ..> c0083: `ownership() calls ownership_records()`
- c0083 ..> c0094: `check_source() calls repository()`
- c0083 ..> c0095: `type in check_source`
- c0083 ..> c0096: `type in __init__`
- c0083 ..> c0101: `ownership() calls tasks()`
- c0083 ..> c0106: `type in __init__`
- c0083 ..> c0124: `context() calls could_be_key()`
- c0083 ..> c0124: `snapshot() calls is_key()`
- c0083 ..> c0126: `snapshot() constructs Ticket`
- c0083 ..> c0126: `type in snapshot`
- c0083 ..> c0127: `snapshot() constructs TicketSource`
- c0083 ..> c0128: `type in __init__`
- c0083 ..> c0129: `check_repository() calls origin()`
- c0083 ..> c0133: `type in __init__`
- c0084 ..> c0006: `initialise() calls save()`
- c0084 ..> c0010: `prepare_foreman() calls install()`
- c0084 ..> c0014: `prepare_foreman() calls prepare()`
- c0084 ..> c0027: `type in __init__`
- c0084 ..> c0047: `load_existing() calls load()`
- c0084 ..> c0047: `prepare_foreman() calls confirm()`
- c0084 ..> c0056: `configure() constructs FactoryConfiguration`
- c0084 ..> c0056: `type in _preflight`
- c0084 ..> c0056: `type in check_foreman`
- c0084 ..> c0056: `type in configure`
- c0084 ..> c0056: `type in initialise`
- c0084 ..> c0056: `type in load_existing`
- c0084 ..> c0057: `_preflight() calls validate()`
- c0084 ..> c0057: `configure() calls unique_labels()`
- c0084 ..> c0057: `load_existing() calls unique_labels()`
- c0084 ..> c0058: `inspect() constructs RepositoryReference`
- c0084 ..> c0058: `type in inspect`
- c0084 ..> c0070: `type in __init__`
- c0084 ..> c0072: `type in __init__`
- c0084 ..> c0074: `check_foreman() calls check()`
- c0084 ..> c0084: `configure() calls inspect()`
- c0084 ..> c0084: `initialise() calls _ensure_label()`
- c0084 ..> c0084: `initialise() calls _preflight()`
- c0084 ..> c0085: `prepare_foreman() calls _reviewed_install()`
- c0084 ..> c0085: `prepare_foreman() calls missing_tools()`
- c0084 ..> c0094: `_preflight() calls repository()`
- c0084 ..> c0094: `inspect() calls repository()`
- c0084 ..> c0096: `type in __init__`
- c0084 ..> c0098: `check_foreman() calls login()`
- c0084 ..> c0104: `type in __init__`
- c0084 ..> c0104: `type in prepare_foreman`
- c0084 ..> c0108: `type in __init__`
- c0084 ..> c0115: `_preflight() constructs FactoryError`
- c0084 ..> c0115: `initialise() constructs FactoryError`
- c0084 ..> c0115: `inspect() constructs FactoryError`
- c0084 ..> c0115: `load_existing() constructs FactoryError`
- c0084 ..> c0115: `prepare_foreman() constructs FactoryError`
- c0084 ..> c0124: `_ensure_label() calls create_label()`
- c0084 ..> c0124: `_preflight() calls check_access()`
- c0084 ..> c0124: `_preflight() calls list_labels()`
- c0084 ..> c0124: `_preflight() calls validate_source()`
- c0084 ..> c0125: `_ensure_label() constructs Label`
- c0084 ..> c0125: `type in _preflight`
- c0084 ..> c0127: `inspect() constructs TicketSource`
- c0084 ..> c0127: `type in _ensure_label`
- c0084 ..> c0127: `type in _preflight`
- c0084 ..> c0128: `type in __init__`
- c0084 ..> c0129: `_preflight() calls origin()`
- c0084 ..> c0129: `discover() calls discover()`
- c0084 ..> c0129: `inspect() calls origin()`
- c0084 ..> c0133: `type in __init__`
- c0085 ..> c0010: `_reviewed_install() calls describe()`
- c0085 ..> c0010: `missing_tools() calls absent()`
- c0085 ..> c0010: `missing_tools() calls unready()`
- c0085 ..> c0072: `type in _reviewed_install`
- c0085 ..> c0072: `type in missing_tools`
- c0086 ..> c0054: `recover() calls snapshot()`
- c0086 ..> c0056: `type in __init__`
- c0086 ..> c0058: `type in _ensure_validated_mapping`
- c0086 ..> c0058: `type in _repository`
- c0086 ..> c0058: `type in check_repository`
- c0086 ..> c0059: `preflight() constructs IntakeProblem`
- c0086 ..> c0061: `_create_plan() constructs ScaffoldProblem`
- c0086 ..> c0061: `_ensure_mapping() constructs ScaffoldProblem`
- c0086 ..> c0061: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0086 ..> c0061: `_recovery_plan() constructs ScaffoldProblem`
- c0086 ..> c0061: `_setup_ownership() constructs ScaffoldProblem`
- c0086 ..> c0061: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0086 ..> c0061: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0086 ..> c0061: `lookup() constructs ScaffoldProblem`
- c0086 ..> c0062: `_create_plan() constructs ScaffoldReadProblem`
- c0086 ..> c0062: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0086 ..> c0062: `lookup() constructs ScaffoldReadProblem`
- c0086 ..> c0062: `prepare() constructs ScaffoldReadProblem`
- c0086 ..> c0062: `recover() constructs ScaffoldReadProblem`
- c0086 ..> c0063: `_create_ownership() constructs UncertainScaffold`
- c0086 ..> c0063: `_create_plan() constructs UncertainScaffold`
- c0086 ..> c0063: `_setup_ownership() constructs UncertainScaffold`
- c0086 ..> c0063: `_sole_recovery_owner() constructs UncertainScaffold`
- c0086 ..> c0063: `prepare() constructs UncertainScaffold`
- c0086 ..> c0074: `check() calls check()`
- c0086 ..> c0081: `_ensure_mapping() calls validate_cleanup_marker()`
- c0086 ..> c0083: `__init__() constructs FactoryRecords`
- c0086 ..> c0083: `_create_ownership() calls ownership()`
- c0086 ..> c0083: `_ensure_mapping() calls check_source()`
- c0086 ..> c0083: `_ensure_worktrees() calls mapping_repository()`
- c0086 ..> c0083: `_prepare_plan() calls active()`
- c0086 ..> c0083: `_prepare_plan() calls context()`
- c0086 ..> c0083: `_setup_ownership() calls ownership()`
- c0086 ..> c0083: `check_repository() calls check_repository()`
- c0086 ..> c0083: `recover() calls active()`
- c0086 ..> c0083: `recover() calls context()`
- c0086 ..> c0083: `recover() calls ownership()`
- c0086 ..> c0084: `preflight() calls inspect()`
- c0086 ..> c0086: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0086 ..> c0086: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0086 ..> c0086: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0086 ..> c0086: `_initial_mappings() calls _repository()`
- c0086 ..> c0086: `_prepare_plan() calls _create_ownership()`
- c0086 ..> c0086: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0086 ..> c0086: `_prepare_plan() calls _setup_ownership()`
- c0086 ..> c0086: `preflight() calls _initial_mappings()`
- c0086 ..> c0086: `preflight() calls _repository()`
- c0086 ..> c0086: `preflight() calls check_repository()`
- c0086 ..> c0086: `prepare() calls _create_plan()`
- c0086 ..> c0086: `prepare() calls _prepare_plan()`
- c0086 ..> c0086: `prepare() calls lookup()`
- c0086 ..> c0086: `prepare() calls preflight()`
- c0086 ..> c0086: `prepare() calls recover()`
- c0086 ..> c0086: `recover() calls _ensure_worktrees()`
- c0086 ..> c0086: `recover() calls _recovery_plan()`
- c0086 ..> c0086: `recover() calls _repository()`
- c0086 ..> c0086: `recover() calls _sole_recovery_owner()`
- c0086 ..> c0086: `recover() calls _validate_recovery_candidates()`
- c0086 ..> c0086: `recover() calls check_repository()`
- c0086 ..> c0086: `unfinished() calls _is_unfinished_factory_plan()`
- c0086 ..> c0087: `_initial_mappings() calls worktree_name()`
- c0086 ..> c0096: `type in __init__`
- c0086 ..> c0101: `_create_ownership() calls create_task()`
- c0086 ..> c0101: `_create_ownership() calls update_plan()`
- c0086 ..> c0101: `_create_plan() calls create_plan()`
- c0086 ..> c0101: `_create_plan() calls get_plan()`
- c0086 ..> c0101: `_create_plan() calls owns()`
- c0086 ..> c0101: `_create_plan() calls plans()`
- c0086 ..> c0101: `_is_unfinished_factory_plan() calls owns()`
- c0086 ..> c0101: `_recovery_plan() calls get_plan()`
- c0086 ..> c0101: `_recovery_plan() calls owns()`
- c0086 ..> c0101: `_recovery_plan() calls plans()`
- c0086 ..> c0101: `lookup() calls plans()`
- c0086 ..> c0101: `unfinished() calls plans()`
- c0086 ..> c0106: `type in __init__`
- c0086 ..> c0115: `_is_unfinished_factory_plan() constructs FactoryError`
- c0086 ..> c0126: `type in _create_plan`
- c0086 ..> c0126: `type in _initial_mappings`
- c0086 ..> c0126: `type in _prepare_plan`
- c0086 ..> c0126: `type in _setup_ownership`
- c0086 ..> c0126: `type in lookup`
- c0086 ..> c0126: `type in preflight`
- c0086 ..> c0126: `type in prepare`
- c0086 ..> c0126: `type in recover`
- c0086 ..> c0127: `type in _repository`
- c0086 ..> c0128: `type in __init__`
- c0086 ..> c0131: `_ensure_mapping() calls ensure()`
- c0086 ..> c0131: `_ensure_mapping() calls verify_removed()`
- c0086 ..> c0131: `_initial_mappings() calls target_branch()`
- c0086 ..> c0133: `type in __init__`
- c0086 ..> c0136: `type in __init__`
- c0087 ..> c0126: `type in worktree_name`
- c0088 ..> c0000: `run() calls start()`
- c0088 ..> c0008: `run() calls saved()`
- c0088 ..> c0008: `run() calls status()`
- c0088 ..> c0014: `run() calls prepare()`
- c0088 ..> c0029: `type in __init__`
- c0088 ..> c0038: `type in __init__`
- c0088 ..> c0052: `run() calls hold()`
- c0088 ..> c0073: `type in __init__`
- c0088 ..> c0115: `run() constructs FactoryError`
- c0089 --> c0126: `field issue`
- c0090 ..> c0000: `_alert_plan() calls send()`
- c0090 ..> c0000: `_check_pending_repositories() calls send()`
- c0090 ..> c0000: `_check_planning_access() calls send()`
- c0090 ..> c0000: `_handle_intake_read_problem() calls send()`
- c0090 ..> c0000: `_handle_intake_repository_problem() calls send()`
- c0090 ..> c0000: `_handle_recovery_read_problem() calls send()`
- c0090 ..> c0000: `_load_inventory() calls send()`
- c0090 ..> c0000: `_process_issue() calls send()`
- c0090 ..> c0000: `_read_issues() calls send()`
- c0090 ..> c0000: `_recover_work() calls send()`
- c0090 ..> c0000: `_submit() calls send()`
- c0090 ..> c0000: `_watch() calls close()`
- c0090 ..> c0000: `_watch() calls start()`
- c0090 ..> c0000: `_watch() calls wait()`
- c0090 ..> c0000: `run() calls startup_hint()`
- c0090 ..> c0008: `_baseline_source() calls report()`
- c0090 ..> c0008: `_check_planning_access() calls report()`
- c0090 ..> c0008: `_submit() calls report()`
- c0090 ..> c0008: `_watch() calls report()`
- c0090 ..> c0008: `run() calls report()`
- c0090 ..> c0014: `_process_issue() calls prepare()`
- c0090 ..> c0028: `type in __init__`
- c0090 ..> c0030: `_watch() calls online()`
- c0090 ..> c0031: `_watch() calls stop()`
- c0090 ..> c0039: `type in __init__`
- c0090 ..> c0056: `type in _poll_sources`
- c0090 ..> c0056: `type in _repository_for_source`
- c0090 ..> c0056: `type in _watch`
- c0090 ..> c0056: `type in run`
- c0090 ..> c0058: `type in _handle_intake_repository_problem`
- c0090 ..> c0058: `type in _process_issue`
- c0090 ..> c0058: `type in _process_issues`
- c0090 ..> c0058: `type in _process_source`
- c0090 ..> c0058: `type in _repository_for_source`
- c0090 ..> c0060: `type in _handle_intake_repository_problem`
- c0090 ..> c0060: `type in _handle_recovery_repository_problem`
- c0090 ..> c0061: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0090 ..> c0061: `type in _alert_plan`
- c0090 ..> c0061: `type in _handle_intake_scaffold_problem`
- c0090 ..> c0062: `type in _handle_intake_read_problem`
- c0090 ..> c0062: `type in _handle_recovery_read_problem`
- c0090 ..> c0064: `_check_pending_repositories() calls clear()`
- c0090 ..> c0064: `_check_planning_access() calls clear()`
- c0090 ..> c0064: `_complete_intake() calls clear()`
- c0090 ..> c0064: `_complete_recovery() calls clear()`
- c0090 ..> c0064: `_load_inventory() calls clear()`
- c0090 ..> c0064: `_process_issue() calls clear()`
- c0090 ..> c0064: `_read_issues() calls clear()`
- c0090 ..> c0064: `_watch() calls clear()`
- c0090 ..> c0064: `_watch() constructs WatcherAlerts`
- c0090 ..> c0064: `type in _alert_plan`
- c0090 ..> c0064: `type in _check_pending_repositories`
- c0090 ..> c0064: `type in _check_planning_access`
- c0090 ..> c0064: `type in _complete_intake`
- c0090 ..> c0064: `type in _complete_recovery`
- c0090 ..> c0064: `type in _handle_intake_read_problem`
- c0090 ..> c0064: `type in _handle_intake_repository_problem`
- c0090 ..> c0064: `type in _handle_intake_scaffold_problem`
- c0090 ..> c0064: `type in _handle_recovery_read_problem`
- c0090 ..> c0064: `type in _handle_recovery_repository_problem`
- c0090 ..> c0064: `type in _load_inventory`
- c0090 ..> c0064: `type in _poll_sources`
- c0090 ..> c0064: `type in _process_issue`
- c0090 ..> c0064: `type in _process_issues`
- c0090 ..> c0064: `type in _process_source`
- c0090 ..> c0064: `type in _read_issues`
- c0090 ..> c0064: `type in _recover_blocked`
- c0090 ..> c0064: `type in _recover_work`
- c0090 ..> c0064: `type in _remember_inventory_candidate`
- c0090 ..> c0074: `__init__() constructs ChatRelay`
- c0090 ..> c0074: `_check_planning_access() calls check()`
- c0090 ..> c0074: `_watch() calls halt()`
- c0090 ..> c0077: `_watch() calls poll()`
- c0090 ..> c0077: `type in __init__`
- c0090 ..> c0083: `_check_pending_repositories() calls check_repository()`
- c0090 ..> c0086: `_load_inventory() calls unfinished()`
- c0090 ..> c0086: `_process_issue() calls lookup()`
- c0090 ..> c0086: `_process_issue() calls recover()`
- c0090 ..> c0086: `_recover_work() calls recover()`
- c0090 ..> c0086: `type in __init__`
- c0090 ..> c0089: `_complete_intake() constructs BlockedWork`
- c0090 ..> c0089: `_handle_intake_read_problem() constructs BlockedWork`
- c0090 ..> c0089: `_handle_intake_repository_problem() constructs BlockedWork`
- c0090 ..> c0089: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0090 ..> c0089: `_process_issue() constructs BlockedWork`
- c0090 ..> c0089: `_remember_inventory_candidate() constructs BlockedWork`
- c0090 ..> c0089: `type in _alert_plan`
- c0090 ..> c0089: `type in _complete_intake`
- c0090 ..> c0089: `type in _complete_recovery`
- c0090 ..> c0089: `type in _handle_recovery_read_problem`
- c0090 ..> c0089: `type in _handle_recovery_repository_problem`
- c0090 ..> c0089: `type in _recover_work`
- c0090 ..> c0089: `type in _remember_task_ids`
- c0090 ..> c0090: `_complete_intake() calls _submit()`
- c0090 ..> c0090: `_complete_recovery() calls _submit()`
- c0090 ..> c0090: `_handle_intake_read_problem() calls _sole_task_id()`
- c0090 ..> c0090: `_handle_intake_repository_problem() calls _alert_plan()`
- c0090 ..> c0090: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0090 ..> c0090: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0090 ..> c0090: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0090 ..> c0090: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0090 ..> c0090: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0090 ..> c0090: `_load_inventory() calls _remember_inventory_candidate()`
- c0090 ..> c0090: `_poll_sources() calls _baseline_source()`
- c0090 ..> c0090: `_poll_sources() calls _process_source()`
- c0090 ..> c0090: `_poll_sources() calls _read_issues()`
- c0090 ..> c0090: `_poll_sources() calls _repository_for_source()`
- c0090 ..> c0090: `_process_issue() calls _complete_intake()`
- c0090 ..> c0090: `_process_issue() calls _handle_intake_read_problem()`
- c0090 ..> c0090: `_process_issue() calls _handle_intake_repository_problem()`
- c0090 ..> c0090: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0090 ..> c0090: `_process_issues() calls _process_issue()`
- c0090 ..> c0090: `_process_issues() calls _skip_issue()`
- c0090 ..> c0090: `_process_source() calls _include_pending_lookups()`
- c0090 ..> c0090: `_process_source() calls _process_issues()`
- c0090 ..> c0090: `_recover_blocked() calls _recover_work()`
- c0090 ..> c0090: `_recover_work() calls _alert_plan()`
- c0090 ..> c0090: `_recover_work() calls _complete_recovery()`
- c0090 ..> c0090: `_recover_work() calls _handle_recovery_read_problem()`
- c0090 ..> c0090: `_recover_work() calls _handle_recovery_repository_problem()`
- c0090 ..> c0090: `_recover_work() calls _remember_task_ids()`
- c0090 ..> c0090: `_remember_inventory_candidate() calls _alert_plan()`
- c0090 ..> c0090: `_watch() calls _check_pending_repositories()`
- c0090 ..> c0090: `_watch() calls _check_planning_access()`
- c0090 ..> c0090: `_watch() calls _load_inventory()`
- c0090 ..> c0090: `_watch() calls _poll_sources()`
- c0090 ..> c0090: `_watch() calls _recover_blocked()`
- c0090 ..> c0090: `run() calls _watch()`
- c0090 ..> c0091: `_watch() constructs _WatchState`
- c0090 ..> c0091: `type in _baseline_source`
- c0090 ..> c0091: `type in _check_pending_repositories`
- c0090 ..> c0091: `type in _check_planning_access`
- c0090 ..> c0091: `type in _complete_intake`
- c0090 ..> c0091: `type in _complete_recovery`
- c0090 ..> c0091: `type in _handle_intake_read_problem`
- c0090 ..> c0091: `type in _handle_intake_repository_problem`
- c0090 ..> c0091: `type in _handle_intake_scaffold_problem`
- c0090 ..> c0091: `type in _handle_recovery_repository_problem`
- c0090 ..> c0091: `type in _load_inventory`
- c0090 ..> c0091: `type in _poll_sources`
- c0090 ..> c0091: `type in _process_issue`
- c0090 ..> c0091: `type in _process_issues`
- c0090 ..> c0091: `type in _process_source`
- c0090 ..> c0091: `type in _recover_blocked`
- c0090 ..> c0091: `type in _recover_work`
- c0090 ..> c0091: `type in _remember_inventory_candidate`
- c0090 ..> c0091: `type in _skip_issue`
- c0090 ..> c0092: `type in _process_issue`
- c0090 ..> c0092: `type in _recover_work`
- c0090 ..> c0115: `_read_issues() constructs FactoryError`
- c0090 ..> c0123: `_submit() calls check_watch_stop()`
- c0090 ..> c0123: `_watch() calls check_watch_stop()`
- c0090 ..> c0123: `run() calls check_watch_stop()`
- c0090 ..> c0124: `_read_issues() calls list_open()`
- c0090 ..> c0126: `type in _baseline_source`
- c0090 ..> c0126: `type in _complete_intake`
- c0090 ..> c0126: `type in _complete_recovery`
- c0090 ..> c0126: `type in _handle_intake_read_problem`
- c0090 ..> c0126: `type in _handle_intake_repository_problem`
- c0090 ..> c0126: `type in _handle_intake_scaffold_problem`
- c0090 ..> c0126: `type in _include_pending_lookups`
- c0090 ..> c0126: `type in _process_issue`
- c0090 ..> c0126: `type in _process_issues`
- c0090 ..> c0126: `type in _process_source`
- c0090 ..> c0126: `type in _read_issues`
- c0090 ..> c0126: `type in _skip_issue`
- c0090 ..> c0126: `type in _submit`
- c0090 ..> c0127: `_watch() constructs TicketSource`
- c0090 ..> c0127: `type in _baseline_source`
- c0090 ..> c0127: `type in _include_pending_lookups`
- c0090 ..> c0127: `type in _poll_sources`
- c0090 ..> c0127: `type in _process_source`
- c0090 ..> c0127: `type in _read_issues`
- c0090 ..> c0127: `type in _repository_for_source`
- c0090 ..> c0128: `type in __init__`
- c0091 --> c0058: `field pending_repositories`
- c0091 --> c0089: `field blocked`
- c0091 --> c0089: `field known`
- c0091 --> c0126: `field pending_lookup`
- c0091 --> c0127: `field baselined`
- c0093 ..> c0014: `_setup() calls validate_completion()`
- c0093 ..> c0026: `_without_live_plain() calls unknown_status()`
- c0093 ..> c0027: `type in __init__`
- c0093 ..> c0029: `type in __init__`
- c0093 ..> c0047: `_setup() calls load()`
- c0093 ..> c0070: `type in __init__`
- c0093 ..> c0093: `_without_live_plain() calls report()`
- c0093 ..> c0093: `report() calls _setup()`
- c0093 ..> c0093: `report() calls _without_live_plain()`
- c0094 ..> c0095: `repository() constructs RepositoryRef`
- c0094 ..> c0095: `type in is_change_request`
- c0094 ..> c0095: `type in repository`
- c0094 ..> c0115: `repository() constructs FactoryError`
- c0096 ..> c0095: `type in is_change_request`
- c0096 ..> c0095: `type in repository`
- c0097 ..> c0009: `uses_browser_login() calls request()`
- c0097 ..> c0049: `uses_browser_login() calls read()`
- c0097 ..> c0104: `type in uses_browser_login`
- c0098 ..> c0098: `call() calls command()`
- c0098 ..> c0098: `check() calls call()`
- c0098 ..> c0098: `check() calls command()`
- c0098 ..> c0098: `command() calls _environment()`
- c0098 ..> c0098: `create_project() calls call()`
- c0098 ..> c0098: `login() calls _environment()`
- c0098 ..> c0098: `projects() calls command()`
- c0098 ..> c0099: `_environment() calls role_environment()`
- c0098 ..> c0099: `check() calls _catalog_tools()`
- c0098 ..> c0104: `type in _environment`
- c0098 ..> c0104: `type in call`
- c0098 ..> c0104: `type in check`
- c0098 ..> c0104: `type in command`
- c0098 ..> c0104: `type in create_project`
- c0098 ..> c0104: `type in login`
- c0098 ..> c0104: `type in projects`
- c0098 ..> c0115: `check() constructs FactoryError`
- c0098 ..> c0115: `command() constructs FactoryError`
- c0098 ..> c0115: `create_project() constructs FactoryError`
- c0098 ..> c0115: `login() constructs FactoryError`
- c0098 ..> c0115: `projects() constructs FactoryError`
- c0098 ..> c0120: `command() calls run_owned()`
- c0098 ..> c0120: `login() calls run_owned()`
- c0098 ..> c0123: `command() calls check_watch_stop()`
- c0099 ..> c0054: `role_environment() calls update()`
- c0099 ..> c0104: `type in role_environment`
- c0099 ..> c0116: `role_environment() calls executable_path()`
- c0100 ..> c0100: `absent() calls _required()`
- c0100 ..> c0100: `absent() calls _selected()`
- c0100 ..> c0100: `describe() calls _python()`
- c0100 ..> c0100: `install() calls _python()`
- c0100 ..> c0100: `unready() calls _required()`
- c0100 ..> c0100: `unready() calls _selected()`
- c0100 ..> c0104: `type in __init__`
- c0100 ..> c0115: `_python() constructs FactoryError`
- c0100 ..> c0116: `_selected() calls executable_path()`
- c0100 ..> c0117: `_python() calls check_uv()`
- c0100 ..> c0117: `_python() calls install_environment()`
- c0100 ..> c0117: `install() calls install_locks()`
- c0100 ..> c0117: `install() calls no_installer()`
- c0100 ..> c0117: `install() calls require_manager()`
- c0100 ..> c0117: `install() calls run_install()`
- c0100 ..> c0117: `unready() calls runtime_ready()`
- c0100 ..> c0120: `_python() calls run_owned()`
- c0101 ..> c0074: `check() calls check()`
- c0101 ..> c0098: `__init__() constructs AgentForgetfulConnection`
- c0101 ..> c0098: `_call() calls call()`
- c0101 ..> c0101: `_read() calls _call()`
- c0101 ..> c0101: `_task() calls _read()`
- c0101 ..> c0101: `create_plan() calls _call()`
- c0101 ..> c0101: `create_task() calls _call()`
- c0101 ..> c0101: `get_plan() calls _read()`
- c0101 ..> c0101: `plans() calls _read()`
- c0101 ..> c0101: `plans() calls _rows()`
- c0101 ..> c0101: `tasks() calls _read()`
- c0101 ..> c0101: `tasks() calls _rows()`
- c0101 ..> c0101: `tasks() calls _task()`
- c0101 ..> c0101: `update_plan() calls _call()`
- c0101 ..> c0101: `update_task() calls _call()`
- c0101 ..> c0102: `_rows() calls _positive_id()`
- c0101 ..> c0102: `_task() calls _positive_id()`
- c0101 ..> c0102: `get_plan() calls _positive_id()`
- c0101 ..> c0104: `type in __init__`
- c0101 ..> c0107: `_read() constructs PlanningReadError`
- c0101 ..> c0107: `_rows() constructs PlanningReadError`
- c0101 ..> c0107: `_task() constructs PlanningReadError`
- c0101 ..> c0107: `get_plan() constructs PlanningReadError`
- c0103 ..> c0074: `check() calls check()`
- c0103 ..> c0097: `uses_browser_login() calls uses_browser_login()`
- c0103 ..> c0098: `_native() constructs AgentForgetfulConnection`
- c0103 ..> c0098: `create_project() calls create_project()`
- c0103 ..> c0098: `login() calls login()`
- c0103 ..> c0098: `projects() calls projects()`
- c0103 ..> c0098: `type in _native`
- c0103 ..> c0103: `check() calls _native()`
- c0103 ..> c0103: `create_project() calls _native()`
- c0103 ..> c0103: `login() calls _native()`
- c0103 ..> c0103: `projects() calls _native()`
- c0103 ..> c0104: `type in check`
- c0103 ..> c0104: `type in create_project`
- c0103 ..> c0104: `type in login`
- c0103 ..> c0104: `type in prepare`
- c0103 ..> c0104: `type in projects`
- c0103 ..> c0104: `type in uses_browser_login`
- c0104 ..> c0104: `validate() calls _validate_server()`
- c0104 ..> c0105: `_validate_server() calls loopback_host()`
- c0104 ..> c0115: `_validate_server() constructs FactoryError`
- c0104 ..> c0115: `validate() constructs FactoryError`
- c0104 ..> c0121: `_validate_server() calls nonblank()`
- c0104 ..> c0121: `validate() calls nonblank()`
- c0105 ..> c0104: `connection_from_mapping() calls validate()`
- c0105 ..> c0104: `connection_from_mapping() constructs ForgetfulConnection`
- c0105 ..> c0104: `type in connection_from_mapping`
- c0105 ..> c0115: `connection_from_mapping() constructs FactoryError`
- c0107 --|> c0115: `inherits`
- c0108 ..> c0104: `type in check`
- c0108 ..> c0104: `type in create_project`
- c0108 ..> c0104: `type in login`
- c0108 ..> c0104: `type in prepare`
- c0108 ..> c0104: `type in projects`
- c0108 ..> c0104: `type in uses_browser_login`
- c0109 ..> c0006: `enter() calls run()`
- c0109 ..> c0115: `enter() constructs FactoryError`
- c0110 ..> c0111: `describe() calls ubuntu_tmux()`
- c0110 ..> c0111: `install() calls ubuntu_tmux()`
- c0110 ..> c0115: `install() constructs FactoryError`
- c0110 ..> c0116: `absent() calls executable_path()`
- c0110 ..> c0117: `install() calls no_installer()`
- c0110 ..> c0117: `install() calls run_install()`
- c0113 ..> c0006: `run_command() calls run()`
- c0113 ..> c0115: `run_command() constructs FactoryError`
- c0113 ..> c0123: `run_command() calls check_watch_stop()`
- c0114 ..> c0114: `find_secret() calls read_env_file()`
- c0117 ..> c0049: `install_locks() calls read()`
- c0117 ..> c0115: `check_uv() constructs FactoryError`
- c0117 ..> c0115: `install_locks() constructs FactoryError`
- c0117 ..> c0115: `no_installer() constructs FactoryError`
- c0117 ..> c0115: `require_manager() constructs FactoryError`
- c0117 ..> c0115: `run_install() constructs FactoryError`
- c0117 ..> c0115: `type in no_installer`
- c0117 ..> c0117: `check_uv() calls install_environment()`
- c0117 ..> c0117: `install_locks() calls sync_fingerprint()`
- c0117 ..> c0117: `run_install() calls install_environment()`
- c0117 ..> c0117: `runtime_ready() calls sync_fingerprint()`
- c0117 ..> c0118: `install_locks() calls write_new()`
- c0117 ..> c0120: `check_uv() calls run_owned()`
- c0117 ..> c0120: `run_install() calls run_owned()`
- c0117 ..> c0120: `runtime_ready() calls run_owned()`
- c0118 ..> c0000: `_generated_parent() calls close()`
- c0118 ..> c0000: `check_skill_file() calls close()`
- c0118 ..> c0047: `read_generated_json() calls load()`
- c0118 ..> c0049: `replace_generated_json() calls write()`
- c0118 ..> c0049: `write_new() calls write()`
- c0118 ..> c0115: `_generated_parent() constructs FactoryError`
- c0118 ..> c0115: `check_real_path() constructs FactoryError`
- c0118 ..> c0115: `check_skill_file() constructs FactoryError`
- c0118 ..> c0115: `read_generated_json() constructs FactoryError`
- c0118 ..> c0115: `write_definition() constructs FactoryError`
- c0118 ..> c0115: `write_new() constructs FactoryError`
- c0118 ..> c0118: `_generated_parent() calls check_real_path()`
- c0118 ..> c0118: `check_skill_file() calls check_real_path()`
- c0118 ..> c0118: `read_generated_json() calls _generated_parent()`
- c0118 ..> c0118: `remove_generated() calls _generated_parent()`
- c0118 ..> c0118: `replace_generated_json() calls _generated_parent()`
- c0118 ..> c0118: `write_definition() calls read_generated_json()`
- c0118 ..> c0118: `write_definition() calls write_json()`
- c0118 ..> c0118: `write_json() calls write_new()`
- c0118 ..> c0118: `write_new() calls check_real_path()`
- c0120 ..> c0000: `_close_capture_streams() calls close()`
- c0120 ..> c0000: `_terminate_owned_process() calls wait()`
- c0120 ..> c0115: `run_owned() constructs FactoryError`
- c0120 ..> c0120: `_terminate_owned_process() calls _close_capture_streams()`
- c0120 ..> c0120: `run_owned() calls _terminate_owned_process()`
- c0120 ..> c0123: `run_owned() calls check_watch_stop()`
- c0121 ..> c0115: `nonblank() constructs FactoryError`
- c0123 ..> c0122: `watch_stop_scope() constructs WatchStop`
- c0124 ..> c0113: `_api() calls run_command()`
- c0124 ..> c0113: `check_ready() calls run_command()`
- c0124 ..> c0115: `_api() constructs FactoryError`
- c0124 ..> c0115: `_comments() constructs FactoryError`
- c0124 ..> c0115: `_validate_issue() constructs FactoryError`
- c0124 ..> c0115: `check_access() constructs FactoryError`
- c0124 ..> c0115: `check_ready() constructs FactoryError`
- c0124 ..> c0115: `create_label() constructs FactoryError`
- c0124 ..> c0115: `list_labels() constructs FactoryError`
- c0124 ..> c0115: `list_open() constructs FactoryError`
- c0124 ..> c0115: `validate_source() constructs FactoryError`
- c0124 ..> c0124: `_comments() calls _api()`
- c0124 ..> c0124: `_ticket() calls _comments()`
- c0124 ..> c0124: `_ticket() calls _milestone()`
- c0124 ..> c0124: `check_access() calls _api()`
- c0124 ..> c0124: `create_label() calls _api()`
- c0124 ..> c0124: `list_labels() calls _api()`
- c0124 ..> c0124: `list_open() calls _api()`
- c0124 ..> c0124: `list_open() calls _ticket()`
- c0124 ..> c0124: `list_open() calls _validate_issue()`
- c0124 ..> c0125: `list_labels() constructs Label`
- c0124 ..> c0125: `type in create_label`
- c0124 ..> c0125: `type in list_labels`
- c0124 ..> c0126: `_ticket() constructs Ticket`
- c0124 ..> c0126: `type in _ticket`
- c0124 ..> c0126: `type in list_open`
- c0124 ..> c0127: `type in _api`
- c0124 ..> c0127: `type in _comments`
- c0124 ..> c0127: `type in _ticket`
- c0124 ..> c0127: `type in _validate_issue`
- c0124 ..> c0127: `type in check_access`
- c0124 ..> c0127: `type in create_label`
- c0124 ..> c0127: `type in list_labels`
- c0124 ..> c0127: `type in list_open`
- c0124 ..> c0127: `type in validate_source`
- c0126 --> c0127: `field source`
- c0128 ..> c0125: `type in create_label`
- c0128 ..> c0125: `type in list_labels`
- c0128 ..> c0126: `type in list_open`
- c0128 ..> c0127: `type in check_access`
- c0128 ..> c0127: `type in create_label`
- c0128 ..> c0127: `type in list_labels`
- c0128 ..> c0127: `type in list_open`
- c0128 ..> c0127: `type in validate_source`
- c0129 ..> c0113: `origin() calls run_command()`
- c0129 ..> c0115: `origin() constructs FactoryError`
- c0129 ..> c0130: `origin() calls _resolve_repository()`
- c0130 ..> c0115: `_resolve_repository() constructs FactoryError`
- c0131 ..> c0049: `ensure() calls write()`
- c0131 ..> c0051: `_network_git() calls quote()`
- c0131 ..> c0064: `begin_cleanup_cycle() calls clear()`
- c0131 ..> c0113: `_dispose() calls run_command()`
- c0131 ..> c0113: `_network_git() calls run_command()`
- c0131 ..> c0113: `_read_git() calls run_command()`
- c0131 ..> c0113: `ensure() calls run_command()`
- c0131 --> c0115: `field cleanup_defaults`
- c0131 ..> c0115: `ensure() constructs FactoryError`
- c0131 ..> c0123: `ensure() calls check_watch_stop()`
- c0131 ..> c0131: `_disposal_state() calls _repository_entries()`
- c0131 ..> c0131: `_disposal_state() calls _validate_disposal_origin()`
- c0131 ..> c0131: `_disposal_state() calls _validate_disposal_path()`
- c0131 ..> c0131: `_disposal_state() calls _validate_disposal_refs()`
- c0131 ..> c0131: `_disposal_state() calls _validate_registered_worktree()`
- c0131 ..> c0131: `_dispose() calls _disposal_state()`
- c0131 ..> c0131: `_dispose() calls _network_git()`
- c0131 ..> c0131: `_dispose() calls _network_read()`
- c0131 ..> c0131: `_dispose() calls _read_git()`
- c0131 ..> c0131: `_dispose() calls _repository_entries()`
- c0131 ..> c0131: `_dispose() calls _verify_local_ref_absent()`
- c0131 ..> c0131: `_inspect() calls _read_git()`
- c0131 ..> c0131: `_inspect() calls _repository_entries()`
- c0131 ..> c0131: `_inspect() calls _validate_registered_worktree()`
- c0131 ..> c0131: `_network_git() calls _read_git()`
- c0131 ..> c0131: `_network_read() calls _network_git()`
- c0131 ..> c0131: `_remote_default() calls _network_read()`
- c0131 ..> c0131: `_repository_entries() calls _read_git()`
- c0131 ..> c0131: `_validate_common_directory() calls _read_git()`
- c0131 ..> c0131: `_validate_disposal_origin() calls _read_git()`
- c0131 ..> c0131: `_validate_disposal_path() calls _read_git()`
- c0131 ..> c0131: `_validate_disposal_refs() calls _read_git()`
- c0131 ..> c0131: `_validate_disposal_refs() calls _remote_default()`
- c0131 ..> c0131: `_validate_registered_worktree() calls _validate_common_directory()`
- c0131 ..> c0131: `_validate_registered_worktree() calls _validate_registration()`
- c0131 ..> c0131: `_validate_registered_worktree() calls _validate_target_identity()`
- c0131 ..> c0131: `_validate_target_identity() calls _read_git()`
- c0131 ..> c0131: `_verify_local_ref_absent() calls _read_git()`
- c0131 ..> c0131: `_verify_removed() calls _repository_entries()`
- c0131 ..> c0131: `dispose() calls _dispose()`
- c0131 ..> c0131: `ensure() calls _inspect()`
- c0131 ..> c0131: `inspect() calls _inspect()`
- c0131 ..> c0131: `repository_identity() calls _read_git()`
- c0131 ..> c0131: `target_branch() calls _read_git()`
- c0131 ..> c0131: `verify_removed() calls _verify_removed()`
- c0131 ..> c0132: `_repository_entries() calls _worktree_entries()`
- c0131 ..> c0134: `_disposal_state() constructs WorktreeProblem`
- c0131 ..> c0134: `_dispose() constructs WorktreeProblem`
- c0131 ..> c0134: `_inspect() constructs WorktreeProblem`
- c0131 ..> c0134: `_network_read() constructs WorktreeProblem`
- c0131 ..> c0134: `_repository_entries() constructs WorktreeProblem`
- c0131 ..> c0134: `_validate_common_directory() constructs WorktreeProblem`
- c0131 ..> c0134: `_validate_disposal_origin() constructs WorktreeProblem`
- c0131 ..> c0134: `_validate_disposal_path() constructs WorktreeProblem`
- c0131 ..> c0134: `_validate_disposal_refs() constructs WorktreeProblem`
- c0131 ..> c0134: `_validate_registration() constructs WorktreeProblem`
- c0131 ..> c0134: `_validate_target_identity() constructs WorktreeProblem`
- c0131 ..> c0134: `_verify_local_ref_absent() constructs WorktreeProblem`
- c0131 ..> c0134: `_verify_removed() constructs WorktreeProblem`
- c0131 ..> c0134: `dispose() constructs WorktreeProblem`
- c0131 ..> c0135: `_read_git() constructs WorktreeReadError`
- c0131 ..> c0135: `ensure() constructs WorktreeReadError`
- c0131 ..> c0135: `inspect() constructs WorktreeReadError`
- c0131 ..> c0135: `repository_identity() constructs WorktreeReadError`
- c0131 ..> c0135: `target_branch() constructs WorktreeReadError`
- c0131 ..> c0135: `verify_removed() constructs WorktreeReadError`
- c0134 ..> c0000: `__init__() calls __init__()`
- c0134 --|> c0115: `inherits`
- c0135 --|> c0115: `inherits`

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
- Type20: `Callable[[str], None]`
- Type21: `tuple[str, ...] | list[str]`
- Type22: `Mapping[str, str]`
- Type23: `socket.socket | None`
- Type24: `DiscordSettings | None`
- Type25: `DiscordLink | None`
- Type26: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type27: `list[Path] | None`
- Type28: `ForgetfulConnection | None`
- Type29: `list[str] | tuple[str, ...]`
- Type30: `int | dict`
- Type31: `int | dict | str`
- Type32: `str | Path`
- Type33: `FactoryConfiguration | None`
- Type34: `tuple[int, int]`
- Type35: `Iterator[PlainWatchObservation | None]`
- Type36: `tuple[RepositoryReference, ...]`
- Type37: `tuple[int, ...] | None`
- Type38: `'CleanupSet'`
- Type39: `ChatChannel | None`
- Type40: `threading.Thread | None`
- Type41: `BaseException | None`
- Type42: `dict[int, int]`
- Type43: `tuple | None`
- Type44: `dict[str, set[int]]`
- Type45: `tuple[dict, dict] | None`
- Type46: `dict[int, list[dict]]`
- Type47: `list[dict] | None`
- Type48: `list[CompletedWork] | None`
- Type49: `CleanupState | None`
- Type50: `Callable[[str], str]`
- Type51: `Callable[[ForgetfulConnection], Sequence[ToolInstaller]]`
- Type52: `Callable[[list[str]], None]`
- Type53: `Callable[[str, str], bool]`
- Type54: `list[str] | None`
- Type55: `dict[str, RepositoryReference]`
- Type56: `dict[TicketSource, tuple[Label, ...]]`
- Type57: `Callable[[], FactoryConfiguration | None]`
- Type58: `tuple[ToolInstaller | None, str | None]`
- Type59: `tuple[list[dict], list[dict]]`
- Type60: `tuple[Ticket, dict] | None`
- Type61: `Ticket | None`
- Type62: `tuple[int, ...]`
- Type63: `Callable[[], Launch]`
- Type64: `Callable[[], bool]`
- Type65: `tuple[set[str], bool]`
- Type66: `tuple[TicketSource, ...]`
- Type67: `tuple[Ticket, ...]`
- Type68: `dict[str, Ticket]`
- Type69: `BlockedWork | None`
- Type70: `tuple[Ticket, ...] | None`
- Type71: `dict[str, BlockedWork]`
- Type72: `Callable[[], dict | None]`
- Type73: `tuple[str | None, str | None]`
- Type74: `tuple[Path, ...]`
- Type75: `float | None`
- Type76: `tuple[Label, ...]`
- Type77: `list[tuple[int, str, str]]`
- Type78: `dict[str, list[str] | FactoryError]`
- Type79: `tuple[Path, list[dict]]`
- Type80: `tuple[Path, Path] | None`
- Type81: `tuple[Path, Path, dict | None]`

## Signature key

- Signature1: `+interact(session: unknown, reader: unknown, reply: unknown, name: unknown,
  deadlines: unknown, persistent: unknown, startup_warning: unknown, replies: unknown) None`
- Signature2: `+send_line(session: unknown, line: unknown, reply: unknown, deadlines: unknown,
  persistent: unknown) bool`
- Signature3: `+open_session(state: unknown, shell: unknown, resources_type: unknown, config:
  unknown, reply: unknown, opened: unknown) None`
- Signature4: `+replace_failed_exit_task(state: unknown, exit_task: unknown, session: unknown,
  config: unknown, reply: unknown, failed: unknown) unknown`
- Signature5: `+supervise_session(state: unknown, reader: unknown, config: unknown, reply: unknown)
  None`
- Signature6: `-_remove_control_socket(server: unknown, endpoint: unknown, socket_identity: unknown)
  None`
- Signature7: `-_cleanup(server: unknown, endpoint: unknown, socket_identity: unknown, observer:
  unknown, disconnected: unknown) None`
- Signature8: `+main(workspace: unknown, python: unknown, directory: unknown, endpoint: unknown,
  handover: unknown) unknown`
- Signature9: `-__init__(workspace: Path, python: str, deadlines: AgentShellLifecycleDeadlines,
  host: SessionHost) unknown`
- Signature10: `+start_owner(workspace: Path, python: str, environment: dict, launch: dict,
  deadlines: AgentShellLifecycleDeadlines, host: SessionHost) dict`
- Signature11: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None, model: str | None, effort: str | None, deadlines:
  AgentShellLifecycleDeadlines, host: SessionHost, channel: Channel, replies: bool) unknown`
- Signature12: `-__init__(workspace: Path, term_grace: float, role_environment:
  Callable[[ForgetfulConnection, str], dict[str, str]], missing_tools:
  Callable[[ForgetfulConnection], list[str]]) unknown`
- Signature13: `+validate_setup(connection: ForgetfulConnection, include_home_system_prompt: bool,
  include_memory_extension: bool) None`
- Signature14: `+prepare_roles(choices: InitialAgentChoices, execution_enabled: bool, repositories:
  Sequence[str], connection: ForgetfulConnection) None`
- Signature15: `+validate_worker_models(choices: InitialAgentChoices, repositories: Sequence[str],
  connection: ForgetfulConnection) None`
- Signature16: `-_write_agent(name: unknown, model: unknown, effort: unknown, description: unknown,
  children: unknown, resources: unknown) unknown`
- Signature17: `-__init__(settings: DiscordSettings, env_file: Path, explicit_env_file: bool, warn:
  Callable[[str], None], command: tuple[str, ...] | list[str], environment: Mapping[str, str],
  close_wait: float) unknown`
- Signature18: `+build_tools(workspace: Path, connection: ForgetfulConnection, term_grace: float)
  unknown`
- Signature19: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown, deadlines: DeadlinePolicy, observation: unknown, warn: Callable[[str], None],
  chat_interval: float) WatchFactory`
- Signature20: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown, term_grace: float) unknown`
- Signature21: `+build_start_foreman(workspace: Path, python: str, deadlines: DeadlinePolicy)
  StartForeman`
- Signature22: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature23: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature24: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature25: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature26: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature27: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature28: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature29: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature30: `-_foreman_memory_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown, connection: ForgetfulConnection) InitialAgentChoices`
- Signature31: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature32: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature33: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int |
  dict`
- Signature34: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature35: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature36: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None, deadlines: DeadlinePolicy) int | dict`
- Signature37: `-_initialise_locked(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int | dict | str`
- Signature38: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown, deadlines: unknown) unknown`
- Signature39: `+update_resources(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int`
- Signature40: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature41: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature42: `-__init__(records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts,
  ticketing: Ticketing) unknown`
- Signature43: `-_finish_plans(done: list[CompletedWork], references: dict[str, set[int]], alerts:
  WatcherAlerts) bool`
- Signature44: `-_claim_indexes(inventory: list[dict], plans: list[dict], tasks: dict[int,
  list[dict]], identities: dict[str, str], alerts: WatcherAlerts) tuple[dict, dict] | None`
- Signature45: `-_dispose(work: CompletedWork, mapping: dict, claims: dict, references: dict,
  identities: dict[str, str], alerts: WatcherAlerts, report: unknown) bool`
- Signature46: `-_mapping_identity(plan_id: int, reference: str, mapping: dict, workspace: str |
  None) CleanupSet`
- Signature47: `+agree_definition_of_done(agreement: AgreementStore, config: FactoryConfiguration,
  ask: Callable[[str], str], say: Callable[[str], None]) bool`
- Signature48: `-__init__(planning: PlanStore, workspace: Path, config: FactoryConfiguration,
  repositories: LocalRepositories, forge: Forge, ticketing: Ticketing) unknown`
- Signature49: `-__init__(tracking: Ticketing, storage: ConfigurationStore, repositories:
  LocalRepositories, forge: Forge, team: AgentTeam, planning: PlanningSetup, tools:
  Callable[[ForgetfulConnection], Sequence[ToolInstaller]]) unknown`
- Signature50: `-__init__(planning: PlanStore, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, forge: Forge, ticketing: Ticketing)
  unknown`
- Signature51: `-_setup_ownership(plan_id: int, issue: Ticket, context: dict, initial_mappings:
  list[dict]) tuple[list[dict], list[dict]]`
- Signature52: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature53: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature54: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature55: `-__init__(lease: WatchLease, owner: PersistentForeman, channel: Channel, prepare:
  Callable[[], Launch]) unknown`
- Signature56: `-__init__(tracking: Ticketing, terminal: ForemanTerminal, scaffold: ScaffoldIssue,
  cleanup: CleanupCompleted, chat: ChatChannel | None, chat_interval: float) unknown`
- Signature57: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature58: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature59: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature60: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature61: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature62: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature63: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Ticket, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature64: `-_poll_sources(sources: tuple[TicketSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature65: `-_process_source(source: TicketSource, issues: tuple[Ticket, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature66: `-_baseline_source(source: TicketSource, issues: tuple[Ticket, ...], state:
  _WatchState, report: Callable[[str], None]) None`
- Signature67: `-_repository_for_source(config: FactoryConfiguration, source: TicketSource)
  RepositoryReference`
- Signature68: `-_include_pending_lookups(source: TicketSource, current: dict[str, Ticket],
  pending_lookup: dict[str, Ticket]) None`
- Signature69: `-_process_issues(issues: tuple[Ticket, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature70: `-_process_issue(issue: Ticket, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature71: `-_handle_intake_repository_problem(issue: Ticket, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature72: `-_handle_intake_read_problem(issue: Ticket, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature73: `-_handle_intake_scaffold_problem(issue: Ticket, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature74: `-_complete_intake(issue: Ticket, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature75: `-_submit(issue: Ticket, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature76: `-__init__(plain: Callable[[], dict | None], owner: PersistentForeman, storage:
  ConfigurationStore, team: AgentTeam) unknown`
- Signature77: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None, hidden: Iterable[str]) dict[str, str]`
- Signature78: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool,
  term_grace: float) unknown`
- Signature79: `+run_install(args: list[str], cwd: Path, term_grace: float, interactive: bool,
  extra_env: dict[str, str] | None) str`
- Signature80: `+run_owned(args: list[str], cwd: Path, env: dict[str, str], login: bool, timeout:
  float | None, term_grace: float) str`
- Signature81: `-_validate_registered_worktree(root: Path, target: Path, branch: str, path: str,
  match: dict) None`
- Signature82: `-_disposal_state(repository: str, branch: str, path: str, remote: str,
  target_branch: str) tuple[Path, Path, dict | None]`

## Extraction warnings

- `Unresolved or out-of-scope base: AgentTeam -> Protocol`
- `Unresolved or out-of-scope base: AgreementStore -> Protocol`
- `Unresolved or out-of-scope base: Channel -> Protocol`
- `Unresolved or out-of-scope base: ChatChannel -> Protocol`
- `Unresolved or out-of-scope base: CleanupMarkerError -> ValueError`
- `Unresolved or out-of-scope base: CleanupReceipts -> Protocol`
- `Unresolved or out-of-scope base: ConfigurationStore -> Protocol`
- `Unresolved or out-of-scope base: Delivery -> Enum`
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
- `Unresolved or out-of-scope base: _UncachedLoader -> importlib.machinery.SourceFileLoader`
- `Unresolved or out-of-scope base: _WorkAction -> Enum`
