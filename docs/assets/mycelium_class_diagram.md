# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 80 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 3914. Type relationships removed: 65.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/check_package.py`: 2 source occurrences (test-path).
- `tests/deadline_support.py`: 2 source occurrences (test-path).
- `tests/lifecycle_support.py`: 21 source occurrences (test-path).
- `tests/poll_support.py`: 9 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_agent_definitions.py`: 21 source occurrences (test-path).
- `tests/test_architecture.py`: 12 source occurrences (test-path).
- `tests/test_assisted_lifecycle.py`: 16 source occurrences (test-path).
- `tests/test_assisted_review_fixes.py`: 20 source occurrences (test-path).
- `tests/test_assisted_setup.py`: 15 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_cleanup_boundaries.py`: 19 source occurrences (test-path).
- `tests/test_cleanup_recovery.py`: 12 source occurrences (test-path).
- `tests/test_configuration.py`: 14 source occurrences (test-path).
- `tests/test_factory_maintenance.py`: 8 source occurrences (test-path).
- `tests/test_foreman_issue_intake.py`: 4 source occurrences (test-path).
- `tests/test_foreman_memory_setup.py`: 20 source occurrences (test-path).
- `tests/test_foreman_setup_repair.py`: 31 source occurrences (test-path).
- `tests/test_init.py`: 47 source occurrences (test-path).
- `tests/test_init_launch.py`: 13 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 20 source occurrences (test-path).
- `tests/test_local_skills.py`: 21 source occurrences (test-path).
- `tests/test_managed_watcher_alerts.py`: 10 source occurrences (test-path).
- `tests/test_native_assisted_reload.py`: 3 source occurrences (test-path).
- `tests/test_native_roles.py`: 5 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_normalized_lifecycle.py`: 14 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 11 source occurrences (test-path).
- `tests/test_owner_startup.py`: 22 source occurrences (test-path).
- `tests/test_pi_runtime_install.py`: 3 source occurrences (test-path).
- `tests/test_planning_adapter.py`: 18 source occurrences (test-path).
- `tests/test_planning_setup.py`: 12 source occurrences (test-path).
- `tests/test_planning_watch.py`: 31 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_review_regressions.py`: 56 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 24 source occurrences (test-path).
- `tests/test_watch.py`: 61 source occurrences (test-path).
- `tests/test_watch_lock.py`: 6 source occurrences (test-path).
- `tests/test_watch_status.py`: 22 source occurrences (test-path).
- `tests/test_watch_status_review.py`: 35 source occurrences (test-path).
- `tests/test_watcher_alerts.py`: 61 source occurrences (test-path).
- `tests/test_watcher_cancellation.py`: 5 source occurrences (test-path).
- `tests/test_watcher_followup.py`: 35 source occurrences (test-path).
- `tests/test_watcher_guidance.py`: 4 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 19 source occurrences (test-path).
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
    class c0008["src/forgetful_factory/adapters/command.py"] {
        <<module>>
        +run_command(arguments: list[str], timeout: float) str
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
        -_write_foreman_memory(choices: unknown) None
        -_write_agent(Signature10)
        +validate_guidance(config: FactoryConfiguration) None
    }
    class c0011["src/forgetful_factory/adapters/filesystem/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0012["ForemanProfile"] {
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
    class c0013["src/forgetful_factory/adapters/filesystem/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0014["GitRepositories"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0015["src/forgetful_factory/adapters/filesystem/git_repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0016["GitWorktrees"] {
        <<class>>
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        -_read_git(arguments: list[str]) str
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type11
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type12
        -_validate_registered_worktree(Signature12)
        -_validate_registration(target: Path, branch: str, path: str, match: dict) None
        -_validate_common_directory(root: Path, target: Path, path: str) str
        -_validate_target_identity(target: Path, path: str, match: dict, expected: str) None
    }
    class c0017["src/forgetful_factory/adapters/filesystem/git_worktrees.py"] {
        <<module>>
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
        -_add_skill_file(path: Path, files: Type13) None
        -_walk_skill_directory(directory: Path, ancestors: Type14, files: Type13) None
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0020["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type15
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
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +role: unknown
        +term_grace: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type16
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0026["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature13)
        -_catalog_tools(catalog: object) dict
    }
    class c0027["ForgetfulPlanning"] {
        <<class>>
        -__init__(Signature14)
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
        -__init__(command_timeout: float) unknown
        +command_timeout: unknown
        +check_cli() None
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type17
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type19) Type18
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0030["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path, term_grace: float) unknown
        +workspace: unknown
        +runtime: unknown
        +term_grace: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type6) Type16
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
        +sync_fingerprint(inputs: Type20) str
        +runtime_ready(runtime: Path, inputs: Type20, probe: str, term_grace: float) bool
    }
    class c0032["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        -_close_capture_streams(process: subprocess.Popen) None
        -_terminate_owned_process(process: subprocess.Popen, term_grace: float) None
        +run_owned(Signature15)
    }
    class c0033["ObservedTerminal"] {
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
    class c0034["PlainWatchObservation"] {
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
    class c0035["src/forgetful_factory/adapters/watch_status.py"] {
        <<module>>
        -_observation_json(data: bytes) object
        -_discovery_path(workspace: Path) Path
        -_endpoint(run_id: str) str
        -_frame(connection: socket.socket) dict
        -_peer(connection: socket.socket) Type22
        -_read_discovery(workspace: Path) dict
        +unknown_status(source: str, observation: str) dict
        +plain_watch_status(workspace: Path) Type5
        +observe_plain_watch(workspace: Path, report_unavailable: Type24) Type23
    }
    class c0036["CleanupMarkerError"] {
        <<class>>
    }
    class c0037["src/forgetful_factory/application/cleanup_marker.py"] {
        <<module>>
        +validate_cleanup_marker(mapping: dict) Type25
    }
    class c0038["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type19
        +foreman_agent_file: str
        +repository: Type26
        +forgetful: Type27
        +execution_enabled: bool
    }
    class c0039["ForgetfulConnection"] {
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
    class c0040["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type27
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type19
    }
    class c0041["InitialAgentChoices"] {
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
        +implementation_skills: Type19
        +review_skills: Type19
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0042["src/forgetful_factory/application/initial_agent_choices.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type19
        -_validate_foreman_memory(configuration: InitialAgentChoices) None
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0043["InitialiseFactory"] {
        <<class>>
        -__init__(Signature16)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type28, confirm: Type29) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type30, labels: Type31) Type15
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type32
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type33
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type34, save: bool) list[str]
    }
    class c0044["ConfigurationStore"] {
        <<class>>
        +load() Type15
        +save(configuration: FactoryConfiguration) None
    }
    class c0045["ForemanProfile"] {
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
    class c0046["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0047["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0048["Planning"] {
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
    class c0049["PlanningReadError"] {
        <<class>>
    }
    class c0050["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0051["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0052["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type3) unknown
        +code: unknown
        +paths: unknown
    }
    class c0053["WorktreeReadError"] {
        <<class>>
    }
    class c0054["Worktrees"] {
        <<class>>
        +inspect(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
    }
    class c0055["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature17)
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
        -_setup_ownership(plan_id: int, issue: Issue, context: dict) Type35
        -_ensure_setup_worktrees(mappings: list[dict], tasks: list[dict]) None
        -_create_ownership(Signature18)
        +lookup(issue: Issue) Type2
        -_create_plan(issue: Issue) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type37, task_ids: Type38) Type36
        -_recovery_plan(plan_id: int, external_ref: str) dict
        -_validate_recovery_candidates(Signature19)
        -_sole_recovery_owner(owners: list[dict], context: dict) dict
        -_snapshot(context: dict, external_ref: str) Issue
        -_is_unfinished_factory_plan(summary: dict, sources: set[str]) bool
        -_active(plan: dict) bool
        -_context(plan: dict) dict
        -_ownership(plan_id: int, external_ref: str) list[dict]
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_mapping_repository(mapping: dict, seen: set[str]) RepositoryReference
        -_ensure_validated_mapping(Signature20)
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0056["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type2
        +issue: Type37
        +task_ids: Type38
        +recovered: bool
        +setup_paths: Type19
        +setup_cause: Type3
    }
    class c0057["WatchFactory"] {
        <<class>>
        -__init__(Signature21)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +run(Signature22)
        -_watch(Signature23)
        -_check_pending_repositories(state: _WatchState, alerts: WatcherAlerts) None
        -_check_planning_access(state: _WatchState, alerts: WatcherAlerts, report: Type24) bool
        -_load_inventory(state: _WatchState, alerts: WatcherAlerts) bool
        -_remember_inventory_candidate(Signature24)
        -_recover_blocked(state: _WatchState, alerts: WatcherAlerts, report: Type24) Type41
        -_recover_work(Signature25)
        -_handle_recovery_repository_problem(Signature26)
        -_handle_recovery_read_problem(Signature27)
        -_remember_task_ids(work: BlockedWork, task_ids: Type38) None
        -_complete_recovery(Signature28)
        -_poll_sources(Signature29)
        -_process_source(Signature30)
        -_baseline_source(Signature31)
        -_repository_for_source(Signature32)
        -_include_pending_lookups(Signature33)
        -_process_issues(Signature34)
        -_skip_issue(issue: Issue, state: _WatchState, attempted: set[str]) bool
        -_process_issue(Signature35)
        -_handle_intake_repository_problem(Signature36)
        -_handle_intake_read_problem(Signature37)
        -_handle_intake_scaffold_problem(Signature38)
        -_complete_intake(Signature39)
        -_sole_task_id(task_ids: Type38) Type2
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature40)
        -_read_issues(source: WorkSource, labels: Type19, alerts: WatcherAlerts) Type45
    }
    class c0058["_WatchState"] {
        <<class>>
        +seen: Type16
        +baseline: Type16
        +baselined: set[WorkSource]
        +blocked: Type46
        +pending_lookup: Type43
        +known: Type46
        +recovered: set[str]
        +pending_repositories: Type32
        +checked: bool
        +inventoried: bool
        +manual_pause: bool
    }
    class c0059["_WorkAction"] {
        <<class>>
        +COMPLETE: unknown
        +RETRY: unknown
        +PAUSE_READS: unknown
        +PAUSE_MANUAL: unknown
    }
    class c0060["IntakeProblem"] {
        <<class>>
    }
    class c0061["RepositoryProblem"] {
        <<class>>
    }
    class c0062["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature41)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0063["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0064["UncertainScaffold"] {
        <<class>>
    }
    class c0065["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type16
        +last_diagnostic: Type16
        +clear(subject: str) None
        +send(Signature42)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0066["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path, deadlines: DeadlinePolicy) InitialiseFactory
        +build_watcher(Signature43)
        +prepare_foreman_launch(Signature44)
    }
    class c0067["_InitialSetupState"] {
        <<class>>
        +connection: ForgetfulConnection
        +config: FactoryConfiguration
        +prepared: bool
    }
    class c0068["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature45)
        -_check_existing_connection(Signature46)
        -_connection(Signature47)
        -_prepare_foreman(Signature48)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type48, show_choices: bool, prompt: Type3) str
        -_select_model(Signature49)
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
        -_select_project(Signature50)
        -_owner_choices(Signature51)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_select_setup_route(args: argparse.Namespace) bool
        -_prompt_coordinator_choices(Signature52)
        -_foreman_memory_choices(Signature53)
        -_managed_rest_mapping_available(connection: ForgetfulConnection) bool
        -_worker_choices(Signature54)
        -_complete_setup(Signature55)
        -_initialise(args: argparse.Namespace, workspace: Path, deadlines: DeadlinePolicy) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_validate_setup_owner(args: argparse.Namespace, workspace: Path, state: Type5) None
        -_finish_existing_setup(Signature56)
        -_discover_worker_models(Signature57)
        -_validate_initial_model(Signature58)
        -_start_initial_setup(Signature59)
        -_initialise_locked(Signature60)
        -_launch_setup_foreman(Signature61)
        +main(deadlines: DeadlinePolicy) int
    }
    class c0069["src/forgetful_factory/cli/numbered_selection.py"] {
        <<module>>
        +parse_numbered_selection(label: str, answer: str, choice_count: int) int
    }
    class c0070["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type51) FactoryConfiguration
    }
    class c0071["AgentShellLifecycleDeadlines"] {
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
    class c0072["DeadlinePolicy"] {
        <<class>>
        +external_command: float
        +owned_process_term_grace: float
        +agentshell: AgentShellLifecycleDeadlines
        -__post_init__() None
    }
    class c0073["src/forgetful_factory/deadlines.py"] {
        <<module>>
        -_validate_duration(name: str, value: object) None
    }
    class c0074["FactoryError"] {
        <<class>>
    }
    class c0075["Issue"] {
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
    class c0076["Label"] {
        <<class>>
        +name: str
    }
    class c0077["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0078["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0079["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type17
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type19) Type18
    }
    c0000 ..> c0000 : 2 relationships (see list)
    c0000 ..> c0007 : close() calls close()
    c0000 ..> c0074 : 2 relationships (see list)
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
    c0004 ..> c0071 : 2 relationships (see list)
    c0004 ..> c0074 : 10 relationships (see list)
    c0005 ..> c0000 : 3 relationships (see list)
    c0005 ..> c0004 : 3 relationships (see list)
    c0005 ..> c0005 : 5 relationships (see list)
    c0005 ..> c0006 : _prepare_owner_startup() calls read_state()
    c0005 ..> c0013 : _prepare_owner_startup() calls runtime_directory()
    c0005 ..> c0021 : _acquire_owner_lock() calls quote()
    c0005 ..> c0027 : main() calls create_task()
    c0005 ..> c0074 : 3 relationships (see list)
    c0006 ..> c0000 : 2 relationships (see list)
    c0006 ..> c0004 : 2 relationships (see list)
    c0006 ..> c0006 : 3 relationships (see list)
    c0006 ..> c0013 : 3 relationships (see list)
    c0006 ..> c0018 : read_state() calls read_generated_json()
    c0006 ..> c0021 : request() calls quote()
    c0006 ..> c0071 : 2 relationships (see list)
    c0006 ..> c0074 : 5 relationships (see list)
    c0007 ..> c0000 : close() calls close()
    c0007 ..> c0007 : 5 relationships (see list)
    c0007 ..> c0071 : 2 relationships (see list)
    c0007 ..> c0074 : 4 relationships (see list)
    c0008 ..> c0004 : run_command() calls run()
    c0008 ..> c0074 : run_command() constructs FactoryError
    c0009 ..> c0009 : 8 relationships (see list)
    c0009 ..> c0040 : 4 relationships (see list)
    c0009 ..> c0074 : 2 relationships (see list)
    c0010 ..> c0010 : 3 relationships (see list)
    c0010 ..> c0011 : prepare() calls selected_resources()
    c0010 ..> c0012 : prepare() calls prepare()
    c0010 ..> c0018 : 5 relationships (see list)
    c0010 ..> c0023 : __init__() constructs WorkerProfiles
    c0010 ..> c0038 : 2 relationships (see list)
    c0010 ..> c0074 : 4 relationships (see list)
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
    c0012 ..> c0038 : 4 relationships (see list)
    c0012 ..> c0039 : 9 relationships (see list)
    c0012 ..> c0074 : 14 relationships (see list)
    c0013 ..> c0018 : runtime_directory() calls check_real_path()
    c0013 ..> c0074 : runtime_directory() constructs FactoryError
    c0014 ..> c0008 : origin() calls run_command()
    c0014 ..> c0015 : origin() calls _resolve_repository()
    c0014 ..> c0074 : origin() constructs FactoryError
    c0015 ..> c0074 : _resolve_repository() constructs FactoryError
    c0016 ..> c0008 : 2 relationships (see list)
    c0016 ..> c0016 : 13 relationships (see list)
    c0016 ..> c0017 : _repository_entries() calls _worktree_entries()
    c0016 ..> c0052 : 6 relationships (see list)
    c0016 ..> c0053 : 4 relationships (see list)
    c0016 ..> c0074 : ensure() constructs FactoryError
    c0018 ..> c0000 : 2 relationships (see list)
    c0018 ..> c0018 : 9 relationships (see list)
    c0018 ..> c0020 : read_generated_json() calls load()
    c0018 ..> c0074 : 6 relationships (see list)
    c0019 ..> c0000 : _add_skill_file() calls close()
    c0019 ..> c0019 : 3 relationships (see list)
    c0019 ..> c0074 : 3 relationships (see list)
    c0020 ..> c0000 : 2 relationships (see list)
    c0020 ..> c0021 : save() calls quote()
    c0020 ..> c0038 : 2 relationships (see list)
    c0020 ..> c0040 : load() calls from_mapping()
    c0020 ..> c0044 : load() calls load()
    c0020 ..> c0074 : 2 relationships (see list)
    c0022 ..> c0000 : _hold_directory() calls close()
    c0022 ..> c0022 : hold() calls _hold_directory()
    c0022 ..> c0074 : _hold_directory() constructs FactoryError
    c0023 ..> c0018 : 3 relationships (see list)
    c0023 ..> c0034 : prepare() calls update()
    c0023 ..> c0041 : type in prepare
    c0024 ..> c0006 : uses_browser_login() calls request()
    c0024 ..> c0039 : type in uses_browser_login
    c0025 ..> c0025 : 7 relationships (see list)
    c0025 ..> c0026 : 2 relationships (see list)
    c0025 ..> c0032 : 2 relationships (see list)
    c0025 ..> c0039 : 7 relationships (see list)
    c0025 ..> c0074 : 5 relationships (see list)
    c0026 ..> c0031 : role_environment() calls executable_path()
    c0026 ..> c0034 : role_environment() calls update()
    c0026 ..> c0039 : type in role_environment
    c0027 ..> c0012 : check() calls check()
    c0027 ..> c0025 : 2 relationships (see list)
    c0027 ..> c0027 : 12 relationships (see list)
    c0027 ..> c0028 : 3 relationships (see list)
    c0027 ..> c0039 : type in __init__
    c0027 ..> c0049 : 4 relationships (see list)
    c0029 ..> c0008 : 2 relationships (see list)
    c0029 ..> c0029 : 5 relationships (see list)
    c0029 ..> c0074 : 8 relationships (see list)
    c0029 ..> c0075 : 2 relationships (see list)
    c0029 ..> c0076 : 3 relationships (see list)
    c0029 ..> c0078 : 8 relationships (see list)
    c0030 ..> c0018 : install() calls write_new()
    c0030 ..> c0030 : 15 relationships (see list)
    c0030 ..> c0031 : 3 relationships (see list)
    c0030 ..> c0032 : 4 relationships (see list)
    c0030 ..> c0074 : 6 relationships (see list)
    c0031 ..> c0031 : runtime_ready() calls sync_fingerprint()
    c0031 ..> c0032 : runtime_ready() calls run_owned()
    c0032 ..> c0000 : 2 relationships (see list)
    c0032 ..> c0032 : 2 relationships (see list)
    c0032 ..> c0074 : run_owned() constructs FactoryError
    c0033 ..> c0000 : 5 relationships (see list)
    c0033 ..> c0034 : 3 relationships (see list)
    c0033 ..> c0035 : __init__() calls unknown_status()
    c0033 ..> c0046 : type in __init__
    c0034 ..> c0018 : 3 relationships (see list)
    c0034 ..> c0033 : 2 relationships (see list)
    c0034 ..> c0034 : 9 relationships (see list)
    c0034 ..> c0035 : 6 relationships (see list)
    c0034 ..> c0074 : __enter__() constructs FactoryError
    c0035 ..> c0018 : _read_discovery() calls check_real_path()
    c0035 ..> c0034 : 4 relationships (see list)
    c0035 ..> c0035 : 8 relationships (see list)
    c0037 ..> c0036 : validate_cleanup_marker() constructs CleanupMarkerError
    c0038 --> c0039 : field forgetful
    c0038 --> c0077 : field repository
    c0039 ..> c0040 : 2 relationships (see list)
    c0039 ..> c0074 : _validate_server() constructs FactoryError
    c0040 ..> c0038 : 3 relationships (see list)
    c0040 ..> c0039 : 3 relationships (see list)
    c0040 ..> c0040 : 5 relationships (see list)
    c0040 ..> c0074 : 4 relationships (see list)
    c0040 ..> c0077 : from_mapping() constructs RepositoryReference
    c0040 ..> c0078 : from_mapping() constructs WorkSource
    c0042 ..> c0040 : 4 relationships (see list)
    c0042 ..> c0041 : 3 relationships (see list)
    c0042 ..> c0042 : 4 relationships (see list)
    c0042 ..> c0074 : 5 relationships (see list)
    c0043 ..> c0004 : initialise() calls save()
    c0043 ..> c0010 : prepare_foreman() calls prepare()
    c0043 ..> c0012 : 5 relationships (see list)
    c0043 ..> c0014 : 3 relationships (see list)
    c0043 ..> c0020 : load_existing() calls load()
    c0043 ..> c0029 : 5 relationships (see list)
    c0043 ..> c0038 : 6 relationships (see list)
    c0043 ..> c0039 : 2 relationships (see list)
    c0043 ..> c0040 : 2 relationships (see list)
    c0043 ..> c0043 : 3 relationships (see list)
    c0043 ..> c0044 : type in __init__
    c0043 ..> c0045 : type in __init__
    c0043 ..> c0047 : type in __init__
    c0043 ..> c0051 : type in __init__
    c0043 ..> c0074 : 5 relationships (see list)
    c0043 ..> c0076 : 2 relationships (see list)
    c0043 ..> c0077 : 2 relationships (see list)
    c0043 ..> c0078 : 2 relationships (see list)
    c0043 ..> c0079 : type in __init__
    c0044 ..> c0038 : 2 relationships (see list)
    c0045 ..> c0038 : 3 relationships (see list)
    c0045 ..> c0039 : 8 relationships (see list)
    c0045 ..> c0041 : type in prepare_roles
    c0049 --|> c0074 : inherits
    c0051 ..> c0078 : type in source_from_remote
    c0052 ..> c0000 : __init__() calls __init__()
    c0052 --|> c0074 : inherits
    c0053 --|> c0074 : inherits
    c0055 ..> c0012 : check() calls check()
    c0055 ..> c0014 : check_repository() calls origin()
    c0055 ..> c0016 : 3 relationships (see list)
    c0055 ..> c0027 : 10 relationships (see list)
    c0055 ..> c0029 : _check_source() calls source_from_remote()
    c0055 ..> c0037 : _ensure_mapping() calls validate_cleanup_marker()
    c0055 ..> c0038 : type in __init__
    c0055 ..> c0047 : type in __init__
    c0055 ..> c0048 : type in __init__
    c0055 ..> c0051 : type in __init__
    c0055 ..> c0054 : type in __init__
    c0055 ..> c0055 : 34 relationships (see list)
    c0055 ..> c0060 : preflight() constructs IntakeProblem
    c0055 ..> c0061 : 2 relationships (see list)
    c0055 ..> c0062 : 13 relationships (see list)
    c0055 ..> c0063 : 5 relationships (see list)
    c0055 ..> c0064 : 5 relationships (see list)
    c0055 ..> c0074 : _is_unfinished_factory_plan() constructs FactoryError
    c0055 ..> c0075 : 10 relationships (see list)
    c0055 ..> c0077 : 5 relationships (see list)
    c0055 ..> c0078 : 3 relationships (see list)
    c0056 --> c0075 : field issue
    c0057 ..> c0000 : 15 relationships (see list)
    c0057 ..> c0010 : _process_issue() calls prepare()
    c0057 ..> c0012 : _check_planning_access() calls check()
    c0057 ..> c0029 : _read_issues() calls list_issues()
    c0057 ..> c0038 : 4 relationships (see list)
    c0057 ..> c0046 : type in __init__
    c0057 ..> c0055 : 6 relationships (see list)
    c0057 ..> c0056 : 13 relationships (see list)
    c0057 ..> c0057 : 35 relationships (see list)
    c0057 ..> c0058 : 19 relationships (see list)
    c0057 ..> c0059 : 2 relationships (see list)
    c0057 ..> c0061 : 2 relationships (see list)
    c0057 ..> c0062 : 3 relationships (see list)
    c0057 ..> c0063 : 2 relationships (see list)
    c0057 ..> c0065 : 28 relationships (see list)
    c0057 ..> c0074 : _read_issues() constructs FactoryError
    c0057 ..> c0075 : 13 relationships (see list)
    c0057 ..> c0077 : 5 relationships (see list)
    c0057 ..> c0078 : 7 relationships (see list)
    c0057 ..> c0079 : type in __init__
    c0058 --> c0056 : 2 relationships (see list)
    c0058 --> c0075 : field pending_lookup
    c0058 --> c0077 : field pending_repositories
    c0058 --> c0078 : field baselined
    c0060 --|> c0062 : inherits
    c0061 --|> c0062 : inherits
    c0062 --|> c0074 : inherits
    c0063 --|> c0062 : inherits
    c0064 --|> c0062 : inherits
    c0065 ..> c0000 : 2 relationships (see list)
    c0065 ..> c0074 : type in send
    c0066 ..> c0007 : build_watcher() constructs AgentShellTerminal
    c0066 ..> c0012 : 6 relationships (see list)
    c0066 ..> c0014 : 2 relationships (see list)
    c0066 ..> c0016 : build_watcher() constructs GitWorktrees
    c0066 ..> c0020 : build_initialiser() constructs TomlConfigurationStore
    c0066 ..> c0026 : prepare_foreman_launch() calls role_environment()
    c0066 ..> c0027 : build_watcher() constructs ForgetfulPlanning
    c0066 ..> c0029 : 4 relationships (see list)
    c0066 ..> c0033 : build_watcher() constructs ObservedTerminal
    c0066 ..> c0038 : 2 relationships (see list)
    c0066 ..> c0043 : 2 relationships (see list)
    c0066 ..> c0055 : build_watcher() constructs ScaffoldIssue
    c0066 ..> c0057 : 2 relationships (see list)
    c0066 ..> c0066 : build_watcher() calls prepare_foreman_launch()
    c0066 ..> c0072 : 4 relationships (see list)
    c0066 ..> c0074 : 2 relationships (see list)
    c0067 --> c0038 : field config
    c0067 --> c0039 : field connection
    c0068 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0068 ..> c0004 : _watch_locked() calls run()
    c0068 ..> c0006 : 13 relationships (see list)
    c0068 ..> c0012 : 17 relationships (see list)
    c0068 ..> c0014 : select_repositories() calls discover()
    c0068 ..> c0016 : _configure_new_factory() calls inspect()
    c0068 ..> c0018 : _discover_worker_models() calls check_real_path()
    c0068 ..> c0020 : _initialise_locked() calls load()
    c0068 ..> c0021 : 6 relationships (see list)
    c0068 ..> c0022 : 6 relationships (see list)
    c0068 ..> c0034 : _prompt_workers() calls update()
    c0068 ..> c0035 : 4 relationships (see list)
    c0068 ..> c0038 : 4 relationships (see list)
    c0068 ..> c0039 : 8 relationships (see list)
    c0068 ..> c0041 : 7 relationships (see list)
    c0068 ..> c0042 : _start_initial_setup() calls validate_initial_agents()
    c0068 ..> c0043 : 15 relationships (see list)
    c0068 ..> c0066 : 4 relationships (see list)
    c0068 ..> c0067 : 3 relationships (see list)
    c0068 ..> c0068 : 54 relationships (see list)
    c0068 ..> c0069 : _select_numbered() calls parse_numbered_selection()
    c0068 ..> c0070 : 3 relationships (see list)
    c0068 ..> c0072 : 8 relationships (see list)
    c0068 ..> c0074 : 19 relationships (see list)
    c0069 ..> c0074 : parse_numbered_selection() constructs FactoryError
    c0070 ..> c0020 : 2 relationships (see list)
    c0070 ..> c0038 : type in load_configuration
    c0070 ..> c0074 : load_configuration() constructs FactoryError
    c0072 --> c0071 : field agentshell
    c0072 ..> c0073 : __post_init__() calls _validate_duration()
    c0075 --> c0078 : field source
    c0077 --> c0078 : field work_source
    c0079 ..> c0075 : type in list_issues
    c0079 ..> c0076 : 2 relationships (see list)
    c0079 ..> c0078 : 4 relationships (see list)
```

## Source index

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/adapters/agentshell/borrowed_terminal.py`:9
- c0001: `SessionState` — `src/forgetful_factory/adapters/agentshell/controller.py`:140
- c0002: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0003: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0004: `ForemanOwner` — `src/forgetful_factory/adapters/agentshell/owner.py`:103
- c0005: `src/forgetful_factory/adapters/agentshell/owner.py` —
  `src/forgetful_factory/adapters/agentshell/owner.py`:1
- c0006: `src/forgetful_factory/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/adapters/agentshell/owner_client.py`:1
- c0007: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:14
- c0008: `src/forgetful_factory/adapters/command.py` — `src/forgetful_factory/adapters/command.py`:1
- c0009: `src/forgetful_factory/adapters/filesystem/agent_definitions.py` —
  `src/forgetful_factory/adapters/filesystem/agent_definitions.py`:1
- c0010: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:29
- c0011: `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:1
- c0012: `ForemanProfile` — `src/forgetful_factory/adapters/filesystem/foreman_profile.py`:50
- c0013: `src/forgetful_factory/adapters/filesystem/foreman_runtime.py` —
  `src/forgetful_factory/adapters/filesystem/foreman_runtime.py`:1
- c0014: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:15
- c0015: `src/forgetful_factory/adapters/filesystem/git_repositories.py` —
  `src/forgetful_factory/adapters/filesystem/git_repositories.py`:1
- c0016: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:25
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
- c0025: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:54
- c0026: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0027: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:13
- c0028: `src/forgetful_factory/adapters/forgetful/planning.py` —
  `src/forgetful_factory/adapters/forgetful/planning.py`:1
- c0029: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0030: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:53
- c0031: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0032: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0033: `ObservedTerminal` — `src/forgetful_factory/adapters/watch_status.py`:252
- c0034: `PlainWatchObservation` — `src/forgetful_factory/adapters/watch_status.py`:129
- c0035: `src/forgetful_factory/adapters/watch_status.py` —
  `src/forgetful_factory/adapters/watch_status.py`:1
- c0036: `CleanupMarkerError` — `src/forgetful_factory/application/cleanup_marker.py`:8
- c0037: `src/forgetful_factory/application/cleanup_marker.py` —
  `src/forgetful_factory/application/cleanup_marker.py`:1
- c0038: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:82
- c0039: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0040: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0041: `InitialAgentChoices` — `src/forgetful_factory/application/initial_agent_choices.py`:9
- c0042: `src/forgetful_factory/application/initial_agent_choices.py` —
  `src/forgetful_factory/application/initial_agent_choices.py`:1
- c0043: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0044: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0045: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:8
- c0046: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0047: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0048: `Planning` — `src/forgetful_factory/application/ports/planning.py`:10
- c0049: `PlanningReadError` — `src/forgetful_factory/application/ports/planning.py`:6
- c0050: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0051: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0052: `WorktreeProblem` — `src/forgetful_factory/application/ports/worktrees.py`:10
- c0053: `WorktreeReadError` — `src/forgetful_factory/application/ports/worktrees.py`:6
- c0054: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:19
- c0055: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:28
- c0056: `BlockedWork` — `src/forgetful_factory/application/watch_factory.py`:28
- c0057: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:60
- c0058: `_WatchState` — `src/forgetful_factory/application/watch_factory.py`:39
- c0059: `_WorkAction` — `src/forgetful_factory/application/watch_factory.py`:53
- c0060: `IntakeProblem` — `src/forgetful_factory/application/watcher_problems.py`:104
- c0061: `RepositoryProblem` — `src/forgetful_factory/application/watcher_problems.py`:100
- c0062: `ScaffoldProblem` — `src/forgetful_factory/application/watcher_problems.py`:80
- c0063: `ScaffoldReadProblem` — `src/forgetful_factory/application/watcher_problems.py`:96
- c0064: `UncertainScaffold` — `src/forgetful_factory/application/watcher_problems.py`:108
- c0065: `WatcherAlerts` — `src/forgetful_factory/application/watcher_problems.py`:112
- c0066: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0067: `_InitialSetupState` — `src/forgetful_factory/cli/main.py`:739
- c0068: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0069: `src/forgetful_factory/cli/numbered_selection.py` —
  `src/forgetful_factory/cli/numbered_selection.py`:1
- c0070: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0071: `AgentShellLifecycleDeadlines` — `src/forgetful_factory/deadlines.py`:12
- c0072: `DeadlinePolicy` — `src/forgetful_factory/deadlines.py`:29
- c0073: `src/forgetful_factory/deadlines.py` — `src/forgetful_factory/deadlines.py`:1
- c0074: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0075: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0076: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0077: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0078: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0079: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0007: `close() calls close()`
- c0000 ..> c0074: `_request() constructs FactoryError`
- c0000 ..> c0074: `wait() constructs FactoryError`
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
- c0004 ..> c0071: `__init__() constructs AgentShellLifecycleDeadlines`
- c0004 ..> c0071: `_start_controller() constructs AgentShellLifecycleDeadlines`
- c0004 ..> c0074: `_apply_controller_problem() constructs FactoryError`
- c0004 ..> c0074: `_await_readiness() constructs FactoryError`
- c0004 ..> c0074: `_complete_handover() constructs FactoryError`
- c0004 ..> c0074: `_finish_observation() constructs FactoryError`
- c0004 ..> c0074: `_reject_controller_event() constructs FactoryError`
- c0004 ..> c0074: `_relay_request() constructs FactoryError`
- c0004 ..> c0074: `control() constructs FactoryError`
- c0004 ..> c0074: `observe() constructs FactoryError`
- c0004 ..> c0074: `reap_watcher() constructs FactoryError`
- c0004 ..> c0074: `start_watcher() constructs FactoryError`
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
- c0005 ..> c0074: `_acquire_owner_lock() constructs FactoryError`
- c0005 ..> c0074: `_prepare_owner_startup() constructs FactoryError`
- c0005 ..> c0074: `_watcher_request() constructs FactoryError`
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
- c0006 ..> c0071: `start_owner() constructs AgentShellLifecycleDeadlines`
- c0006 ..> c0071: `type in start_owner`
- c0006 ..> c0074: `_reply() constructs FactoryError`
- c0006 ..> c0074: `enter_terminal() constructs FactoryError`
- c0006 ..> c0074: `read_state() constructs FactoryError`
- c0006 ..> c0074: `request() constructs FactoryError`
- c0006 ..> c0074: `start_owner() constructs FactoryError`
- c0007 ..> c0000: `close() calls close()`
- c0007 ..> c0007: `send() calls _read()`
- c0007 ..> c0007: `send() calls _write()`
- c0007 ..> c0007: `start() calls _read()`
- c0007 ..> c0007: `start() calls _write()`
- c0007 ..> c0007: `wait() calls _read()`
- c0007 ..> c0071: `__init__() constructs AgentShellLifecycleDeadlines`
- c0007 ..> c0071: `type in __init__`
- c0007 ..> c0074: `_read() constructs FactoryError`
- c0007 ..> c0074: `_write() constructs FactoryError`
- c0007 ..> c0074: `close() constructs FactoryError`
- c0007 ..> c0074: `start() constructs FactoryError`
- c0008 ..> c0004: `run_command() calls run()`
- c0008 ..> c0074: `run_command() constructs FactoryError`
- c0009 ..> c0009: `_validate_agent() calls _local_selection()`
- c0009 ..> c0009: `_validate_roster() calls _local_selection()`
- c0009 ..> c0009: `_validate_roster() calls relative_path()`
- c0009 ..> c0009: `foreman_launch() calls read_definition()`
- c0009 ..> c0009: `foreman_launch() calls relative_path()`
- c0009 ..> c0009: `read_definition() calls _validate_agent()`
- c0009 ..> c0009: `read_definition() calls _validate_resources()`
- c0009 ..> c0009: `read_definition() calls _validate_roster()`
- c0009 ..> c0040: `_local_selection() calls nonblank()`
- c0009 ..> c0040: `_validate_agent() calls nonblank()`
- c0009 ..> c0040: `foreman_launch() calls nonblank()`
- c0009 ..> c0040: `relative_path() calls nonblank()`
- c0009 ..> c0074: `foreman_launch() constructs FactoryError`
- c0009 ..> c0074: `read_definition() constructs FactoryError`
- c0010 ..> c0010: `prepare() calls _write_agent()`
- c0010 ..> c0010: `prepare() calls _write_foreman_memory()`
- c0010 ..> c0010: `prepare() calls validate_guidance()`
- c0010 ..> c0011: `prepare() calls selected_resources()`
- c0010 ..> c0012: `prepare() calls prepare()`
- c0010 ..> c0018: `_write_agent() calls write_definition()`
- c0010 ..> c0018: `_write_foreman_memory() calls read_generated_json()`
- c0010 ..> c0018: `_write_foreman_memory() calls write_json()`
- c0010 ..> c0018: `prepare() calls check_skill_file()`
- c0010 ..> c0018: `prepare() calls write_new()`
- c0010 ..> c0023: `__init__() constructs WorkerProfiles`
- c0010 ..> c0038: `type in prepare`
- c0010 ..> c0038: `type in validate_guidance`
- c0010 ..> c0074: `_write_foreman_memory() constructs FactoryError`
- c0010 ..> c0074: `prepare() constructs FactoryError`
- c0010 ..> c0074: `validate_depth() constructs FactoryError`
- c0010 ..> c0074: `validate_guidance() constructs FactoryError`
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
- c0012 ..> c0038: `type in record_completion`
- c0012 ..> c0038: `type in selected_launch`
- c0012 ..> c0038: `type in validate_completion`
- c0012 ..> c0038: `type in validate_worker_models`
- c0012 ..> c0039: `type in check`
- c0012 ..> c0039: `type in create_project`
- c0012 ..> c0039: `type in list_models`
- c0012 ..> c0039: `type in login`
- c0012 ..> c0039: `type in missing_executables`
- c0012 ..> c0039: `type in prepare`
- c0012 ..> c0039: `type in projects`
- c0012 ..> c0039: `type in uses_browser_login`
- c0012 ..> c0039: `type in validate_setup`
- c0012 ..> c0074: `_install_resources() constructs FactoryError`
- c0012 ..> c0074: `_read_guidance() constructs FactoryError`
- c0012 ..> c0074: `choose_pi_home() constructs FactoryError`
- c0012 ..> c0074: `list_models() constructs FactoryError`
- c0012 ..> c0074: `pi_home() constructs FactoryError`
- c0012 ..> c0074: `prepare_roles() constructs FactoryError`
- c0012 ..> c0074: `prepare_setup_guidance() constructs FactoryError`
- c0012 ..> c0074: `require_pi_home() constructs FactoryError`
- c0012 ..> c0074: `selected_launch() constructs FactoryError`
- c0012 ..> c0074: `validate_bundled_resources() constructs FactoryError`
- c0012 ..> c0074: `validate_completion() constructs FactoryError`
- c0012 ..> c0074: `validate_guidance() constructs FactoryError`
- c0012 ..> c0074: `validate_setup() constructs FactoryError`
- c0012 ..> c0074: `validate_worker_models() constructs FactoryError`
- c0013 ..> c0018: `runtime_directory() calls check_real_path()`
- c0013 ..> c0074: `runtime_directory() constructs FactoryError`
- c0014 ..> c0008: `origin() calls run_command()`
- c0014 ..> c0015: `origin() calls _resolve_repository()`
- c0014 ..> c0074: `origin() constructs FactoryError`
- c0015 ..> c0074: `_resolve_repository() constructs FactoryError`
- c0016 ..> c0008: `_read_git() calls run_command()`
- c0016 ..> c0008: `ensure() calls run_command()`
- c0016 ..> c0016: `_inspect() calls _read_git()`
- c0016 ..> c0016: `_inspect() calls _repository_entries()`
- c0016 ..> c0016: `_inspect() calls _validate_registered_worktree()`
- c0016 ..> c0016: `_repository_entries() calls _read_git()`
- c0016 ..> c0016: `_validate_common_directory() calls _read_git()`
- c0016 ..> c0016: `_validate_registered_worktree() calls _validate_common_directory()`
- c0016 ..> c0016: `_validate_registered_worktree() calls _validate_registration()`
- c0016 ..> c0016: `_validate_registered_worktree() calls _validate_target_identity()`
- c0016 ..> c0016: `_validate_target_identity() calls _read_git()`
- c0016 ..> c0016: `_verify_removed() calls _repository_entries()`
- c0016 ..> c0016: `ensure() calls _inspect()`
- c0016 ..> c0016: `inspect() calls _inspect()`
- c0016 ..> c0016: `verify_removed() calls _verify_removed()`
- c0016 ..> c0017: `_repository_entries() calls _worktree_entries()`
- c0016 ..> c0052: `_inspect() constructs WorktreeProblem`
- c0016 ..> c0052: `_repository_entries() constructs WorktreeProblem`
- c0016 ..> c0052: `_validate_common_directory() constructs WorktreeProblem`
- c0016 ..> c0052: `_validate_registration() constructs WorktreeProblem`
- c0016 ..> c0052: `_validate_target_identity() constructs WorktreeProblem`
- c0016 ..> c0052: `_verify_removed() constructs WorktreeProblem`
- c0016 ..> c0053: `_read_git() constructs WorktreeReadError`
- c0016 ..> c0053: `ensure() constructs WorktreeReadError`
- c0016 ..> c0053: `inspect() constructs WorktreeReadError`
- c0016 ..> c0053: `verify_removed() constructs WorktreeReadError`
- c0016 ..> c0074: `ensure() constructs FactoryError`
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
- c0018 ..> c0074: `_generated_parent() constructs FactoryError`
- c0018 ..> c0074: `check_real_path() constructs FactoryError`
- c0018 ..> c0074: `check_skill_file() constructs FactoryError`
- c0018 ..> c0074: `read_generated_json() constructs FactoryError`
- c0018 ..> c0074: `write_definition() constructs FactoryError`
- c0018 ..> c0074: `write_new() constructs FactoryError`
- c0019 ..> c0000: `_add_skill_file() calls close()`
- c0019 ..> c0019: `_walk_skill_directory() calls _add_skill_file()`
- c0019 ..> c0019: `selected_skill_files() calls _add_skill_file()`
- c0019 ..> c0019: `selected_skill_files() calls _walk_skill_directory()`
- c0019 ..> c0074: `_add_skill_file() constructs FactoryError`
- c0019 ..> c0074: `_walk_skill_directory() constructs FactoryError`
- c0019 ..> c0074: `selected_skill_files() constructs FactoryError`
- c0020 ..> c0000: `load() calls close()`
- c0020 ..> c0000: `save() calls close()`
- c0020 ..> c0021: `save() calls quote()`
- c0020 ..> c0038: `type in load`
- c0020 ..> c0038: `type in save`
- c0020 ..> c0040: `load() calls from_mapping()`
- c0020 ..> c0044: `load() calls load()`
- c0020 ..> c0074: `load() constructs FactoryError`
- c0020 ..> c0074: `save() constructs FactoryError`
- c0022 ..> c0000: `_hold_directory() calls close()`
- c0022 ..> c0022: `hold() calls _hold_directory()`
- c0022 ..> c0074: `_hold_directory() constructs FactoryError`
- c0023 ..> c0018: `prepare() calls check_skill_file()`
- c0023 ..> c0018: `prepare() calls write_definition()`
- c0023 ..> c0018: `prepare() calls write_new()`
- c0023 ..> c0034: `prepare() calls update()`
- c0023 ..> c0041: `type in prepare`
- c0024 ..> c0006: `uses_browser_login() calls request()`
- c0024 ..> c0039: `type in uses_browser_login`
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
- c0025 ..> c0039: `type in _environment`
- c0025 ..> c0039: `type in call`
- c0025 ..> c0039: `type in check`
- c0025 ..> c0039: `type in command`
- c0025 ..> c0039: `type in create_project`
- c0025 ..> c0039: `type in login`
- c0025 ..> c0039: `type in projects`
- c0025 ..> c0074: `check() constructs FactoryError`
- c0025 ..> c0074: `command() constructs FactoryError`
- c0025 ..> c0074: `create_project() constructs FactoryError`
- c0025 ..> c0074: `login() constructs FactoryError`
- c0025 ..> c0074: `projects() constructs FactoryError`
- c0026 ..> c0031: `role_environment() calls executable_path()`
- c0026 ..> c0034: `role_environment() calls update()`
- c0026 ..> c0039: `type in role_environment`
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
- c0027 ..> c0039: `type in __init__`
- c0027 ..> c0049: `_read() constructs PlanningReadError`
- c0027 ..> c0049: `_rows() constructs PlanningReadError`
- c0027 ..> c0049: `_task() constructs PlanningReadError`
- c0027 ..> c0049: `get_plan() constructs PlanningReadError`
- c0029 ..> c0008: `_api() calls run_command()`
- c0029 ..> c0008: `check_cli() calls run_command()`
- c0029 ..> c0029: `check_access() calls _api()`
- c0029 ..> c0029: `create_label() calls _api()`
- c0029 ..> c0029: `list_issues() calls _api()`
- c0029 ..> c0029: `list_issues() calls _validate_issue()`
- c0029 ..> c0029: `list_labels() calls _api()`
- c0029 ..> c0074: `_api() constructs FactoryError`
- c0029 ..> c0074: `_validate_issue() constructs FactoryError`
- c0029 ..> c0074: `check_access() constructs FactoryError`
- c0029 ..> c0074: `check_cli() constructs FactoryError`
- c0029 ..> c0074: `create_label() constructs FactoryError`
- c0029 ..> c0074: `list_issues() constructs FactoryError`
- c0029 ..> c0074: `list_labels() constructs FactoryError`
- c0029 ..> c0074: `source_from_remote() constructs FactoryError`
- c0029 ..> c0075: `list_issues() constructs Issue`
- c0029 ..> c0075: `type in list_issues`
- c0029 ..> c0076: `list_labels() constructs Label`
- c0029 ..> c0076: `type in create_label`
- c0029 ..> c0076: `type in list_labels`
- c0029 ..> c0078: `source_from_remote() constructs WorkSource`
- c0029 ..> c0078: `type in _api`
- c0029 ..> c0078: `type in _validate_issue`
- c0029 ..> c0078: `type in check_access`
- c0029 ..> c0078: `type in create_label`
- c0029 ..> c0078: `type in list_issues`
- c0029 ..> c0078: `type in list_labels`
- c0029 ..> c0078: `type in source_from_remote`
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
- c0030 ..> c0074: `_check_uv() constructs FactoryError`
- c0030 ..> c0074: `_forgetful_python() constructs FactoryError`
- c0030 ..> c0074: `_install_role_runtime() constructs FactoryError`
- c0030 ..> c0074: `_install_tmux() constructs FactoryError`
- c0030 ..> c0074: `_run() constructs FactoryError`
- c0030 ..> c0074: `install() constructs FactoryError`
- c0031 ..> c0031: `runtime_ready() calls sync_fingerprint()`
- c0031 ..> c0032: `runtime_ready() calls run_owned()`
- c0032 ..> c0000: `_close_capture_streams() calls close()`
- c0032 ..> c0000: `_terminate_owned_process() calls wait()`
- c0032 ..> c0032: `_terminate_owned_process() calls _close_capture_streams()`
- c0032 ..> c0032: `run_owned() calls _terminate_owned_process()`
- c0032 ..> c0074: `run_owned() constructs FactoryError`
- c0033 ..> c0000: `close() calls close()`
- c0033 ..> c0000: `send() calls send()`
- c0033 ..> c0000: `start() calls start()`
- c0033 ..> c0000: `startup_hint() calls startup_hint()`
- c0033 ..> c0000: `wait() calls wait()`
- c0033 ..> c0034: `close() calls update()`
- c0033 ..> c0034: `start() calls update()`
- c0033 ..> c0034: `type in __init__`
- c0033 ..> c0035: `__init__() calls unknown_status()`
- c0033 ..> c0046: `type in __init__`
- c0034 ..> c0018: `__enter__() calls check_real_path()`
- c0034 ..> c0018: `__enter__() calls replace_generated_json()`
- c0034 ..> c0018: `_publish_history() calls replace_generated_json()`
- c0034 ..> c0033: `__enter__() calls start()`
- c0034 ..> c0033: `_close_resources() calls close()`
- c0034 ..> c0034: `__enter__() calls _close_resources()`
- c0034 ..> c0034: `__enter__() calls snapshot()`
- c0034 ..> c0034: `__enter__() calls update()`
- c0034 ..> c0034: `__exit__() calls _close_resources()`
- c0034 ..> c0034: `__exit__() calls _publish_history()`
- c0034 ..> c0034: `__exit__() calls snapshot()`
- c0034 ..> c0034: `__exit__() calls update()`
- c0034 ..> c0034: `_serve() calls snapshot()`
- c0034 ..> c0034: `update() calls _publish_history()`
- c0034 ..> c0035: `__enter__() calls _discovery_path()`
- c0034 ..> c0035: `__enter__() calls _endpoint()`
- c0034 ..> c0035: `_publish_history() calls _discovery_path()`
- c0034 ..> c0035: `_publish_history() calls _read_discovery()`
- c0034 ..> c0035: `_serve() calls _frame()`
- c0034 ..> c0035: `_serve() calls _peer()`
- c0034 ..> c0074: `__enter__() constructs FactoryError`
- c0035 ..> c0018: `_read_discovery() calls check_real_path()`
- c0035 ..> c0034: `observe_plain_watch() calls __enter__()`
- c0035 ..> c0034: `observe_plain_watch() calls __exit__()`
- c0035 ..> c0034: `observe_plain_watch() constructs PlainWatchObservation`
- c0035 ..> c0034: `type in observe_plain_watch`
- c0035 ..> c0035: `_frame() calls _observation_json()`
- c0035 ..> c0035: `_read_discovery() calls _discovery_path()`
- c0035 ..> c0035: `_read_discovery() calls _observation_json()`
- c0035 ..> c0035: `plain_watch_status() calls _endpoint()`
- c0035 ..> c0035: `plain_watch_status() calls _frame()`
- c0035 ..> c0035: `plain_watch_status() calls _peer()`
- c0035 ..> c0035: `plain_watch_status() calls _read_discovery()`
- c0035 ..> c0035: `plain_watch_status() calls unknown_status()`
- c0037 ..> c0036: `validate_cleanup_marker() constructs CleanupMarkerError`
- c0038 --> c0039: `field forgetful`
- c0038 --> c0077: `field repository`
- c0039 ..> c0040: `_validate_server() calls loopback_host()`
- c0039 ..> c0040: `_validate_server() calls nonblank()`
- c0039 ..> c0074: `_validate_server() constructs FactoryError`
- c0040 ..> c0038: `from_mapping() constructs FactoryConfiguration`
- c0040 ..> c0038: `type in from_mapping`
- c0040 ..> c0038: `type in validate`
- c0040 ..> c0039: `connection_from_mapping() constructs ForgetfulConnection`
- c0040 ..> c0039: `type in connection_from_mapping`
- c0040 ..> c0039: `validate() calls _validate_server()`
- c0040 ..> c0040: `connection_from_mapping() calls validate()`
- c0040 ..> c0040: `from_mapping() calls connection_from_mapping()`
- c0040 ..> c0040: `from_mapping() calls validate()`
- c0040 ..> c0040: `unique_labels() calls nonblank()`
- c0040 ..> c0040: `validate() calls nonblank()`
- c0040 ..> c0074: `connection_from_mapping() constructs FactoryError`
- c0040 ..> c0074: `from_mapping() constructs FactoryError`
- c0040 ..> c0074: `nonblank() constructs FactoryError`
- c0040 ..> c0074: `validate() constructs FactoryError`
- c0040 ..> c0077: `from_mapping() constructs RepositoryReference`
- c0040 ..> c0078: `from_mapping() constructs WorkSource`
- c0042 ..> c0040: `_validate_foreman_memory() calls nonblank()`
- c0042 ..> c0040: `skill_paths() calls nonblank()`
- c0042 ..> c0040: `validate_initial_agents() calls nonblank()`
- c0042 ..> c0040: `validate_workers() calls nonblank()`
- c0042 ..> c0041: `type in _validate_foreman_memory`
- c0042 ..> c0041: `type in validate_initial_agents`
- c0042 ..> c0041: `type in validate_workers`
- c0042 ..> c0042: `validate_initial_agents() calls _validate_foreman_memory()`
- c0042 ..> c0042: `validate_initial_agents() calls validate_role_app()`
- c0042 ..> c0042: `validate_initial_agents() calls validate_workers()`
- c0042 ..> c0042: `validate_workers() calls validate_role_app()`
- c0042 ..> c0074: `_validate_foreman_memory() constructs FactoryError`
- c0042 ..> c0074: `skill_paths() constructs FactoryError`
- c0042 ..> c0074: `validate_initial_agents() constructs FactoryError`
- c0042 ..> c0074: `validate_role_app() constructs FactoryError`
- c0042 ..> c0074: `validate_workers() constructs FactoryError`
- c0043 ..> c0004: `initialise() calls save()`
- c0043 ..> c0010: `prepare_foreman() calls prepare()`
- c0043 ..> c0012: `check_foreman() calls check()`
- c0043 ..> c0012: `check_foreman() calls login()`
- c0043 ..> c0012: `prepare_foreman() calls install()`
- c0043 ..> c0012: `prepare_foreman() calls installation()`
- c0043 ..> c0012: `prepare_foreman() calls missing_executables()`
- c0043 ..> c0014: `_preflight() calls origin()`
- c0043 ..> c0014: `discover() calls discover()`
- c0043 ..> c0014: `inspect() calls origin()`
- c0043 ..> c0020: `load_existing() calls load()`
- c0043 ..> c0029: `_ensure_label() calls create_label()`
- c0043 ..> c0029: `_preflight() calls check_access()`
- c0043 ..> c0029: `_preflight() calls list_labels()`
- c0043 ..> c0029: `_preflight() calls source_from_remote()`
- c0043 ..> c0029: `inspect() calls source_from_remote()`
- c0043 ..> c0038: `configure() constructs FactoryConfiguration`
- c0043 ..> c0038: `type in _preflight`
- c0043 ..> c0038: `type in check_foreman`
- c0043 ..> c0038: `type in configure`
- c0043 ..> c0038: `type in initialise`
- c0043 ..> c0038: `type in load_existing`
- c0043 ..> c0039: `_preflight() calls validate()`
- c0043 ..> c0039: `type in prepare_foreman`
- c0043 ..> c0040: `configure() calls unique_labels()`
- c0043 ..> c0040: `load_existing() calls unique_labels()`
- c0043 ..> c0043: `configure() calls inspect()`
- c0043 ..> c0043: `initialise() calls _ensure_label()`
- c0043 ..> c0043: `initialise() calls _preflight()`
- c0043 ..> c0044: `type in __init__`
- c0043 ..> c0045: `type in __init__`
- c0043 ..> c0047: `type in __init__`
- c0043 ..> c0051: `type in __init__`
- c0043 ..> c0074: `_preflight() constructs FactoryError`
- c0043 ..> c0074: `initialise() constructs FactoryError`
- c0043 ..> c0074: `inspect() constructs FactoryError`
- c0043 ..> c0074: `load_existing() constructs FactoryError`
- c0043 ..> c0074: `prepare_foreman() constructs FactoryError`
- c0043 ..> c0076: `_ensure_label() constructs Label`
- c0043 ..> c0076: `type in _preflight`
- c0043 ..> c0077: `inspect() constructs RepositoryReference`
- c0043 ..> c0077: `type in inspect`
- c0043 ..> c0078: `type in _ensure_label`
- c0043 ..> c0078: `type in _preflight`
- c0043 ..> c0079: `type in __init__`
- c0044 ..> c0038: `type in load`
- c0044 ..> c0038: `type in save`
- c0045 ..> c0038: `type in prepare_roles`
- c0045 ..> c0038: `type in record_completion`
- c0045 ..> c0038: `type in selected_launch`
- c0045 ..> c0039: `type in check`
- c0045 ..> c0039: `type in create_project`
- c0045 ..> c0039: `type in list_models`
- c0045 ..> c0039: `type in login`
- c0045 ..> c0039: `type in missing_executables`
- c0045 ..> c0039: `type in prepare`
- c0045 ..> c0039: `type in projects`
- c0045 ..> c0039: `type in uses_browser_login`
- c0045 ..> c0041: `type in prepare_roles`
- c0049 --|> c0074: `inherits`
- c0051 ..> c0078: `type in source_from_remote`
- c0052 ..> c0000: `__init__() calls __init__()`
- c0052 --|> c0074: `inherits`
- c0053 --|> c0074: `inherits`
- c0055 ..> c0012: `check() calls check()`
- c0055 ..> c0014: `check_repository() calls origin()`
- c0055 ..> c0016: `_ensure_mapping() calls ensure()`
- c0055 ..> c0016: `_ensure_mapping() calls verify_removed()`
- c0055 ..> c0016: `preflight() calls inspect()`
- c0055 ..> c0027: `_create_ownership() calls create_task()`
- c0055 ..> c0027: `_create_ownership() calls update_plan()`
- c0055 ..> c0027: `_create_plan() calls create_plan()`
- c0055 ..> c0027: `_create_plan() calls get_plan()`
- c0055 ..> c0027: `_create_plan() calls plans()`
- c0055 ..> c0027: `_ownership() calls tasks()`
- c0055 ..> c0027: `_recovery_plan() calls get_plan()`
- c0055 ..> c0027: `_recovery_plan() calls plans()`
- c0055 ..> c0027: `lookup() calls plans()`
- c0055 ..> c0027: `unfinished() calls plans()`
- c0055 ..> c0029: `_check_source() calls source_from_remote()`
- c0055 ..> c0037: `_ensure_mapping() calls validate_cleanup_marker()`
- c0055 ..> c0038: `type in __init__`
- c0055 ..> c0047: `type in __init__`
- c0055 ..> c0048: `type in __init__`
- c0055 ..> c0051: `type in __init__`
- c0055 ..> c0054: `type in __init__`
- c0055 ..> c0055: `_create_ownership() calls _ownership()`
- c0055 ..> c0055: `_ensure_mapping() calls _check_source()`
- c0055 ..> c0055: `_ensure_setup_worktrees() calls _ensure_worktrees()`
- c0055 ..> c0055: `_ensure_validated_mapping() calls _ensure_mapping()`
- c0055 ..> c0055: `_ensure_worktrees() calls _ensure_validated_mapping()`
- c0055 ..> c0055: `_ensure_worktrees() calls _mapping_repository()`
- c0055 ..> c0055: `_initial_mappings() calls _repository()`
- c0055 ..> c0055: `_prepare_plan() calls _active()`
- c0055 ..> c0055: `_prepare_plan() calls _context()`
- c0055 ..> c0055: `_prepare_plan() calls _create_ownership()`
- c0055 ..> c0055: `_prepare_plan() calls _ensure_setup_worktrees()`
- c0055 ..> c0055: `_prepare_plan() calls _setup_ownership()`
- c0055 ..> c0055: `_setup_ownership() calls _initial_mappings()`
- c0055 ..> c0055: `_setup_ownership() calls _ownership()`
- c0055 ..> c0055: `check_repository() calls _check_source()`
- c0055 ..> c0055: `preflight() calls _initial_mappings()`
- c0055 ..> c0055: `preflight() calls _repository()`
- c0055 ..> c0055: `preflight() calls check_repository()`
- c0055 ..> c0055: `prepare() calls _create_plan()`
- c0055 ..> c0055: `prepare() calls _prepare_plan()`
- c0055 ..> c0055: `prepare() calls lookup()`
- c0055 ..> c0055: `prepare() calls preflight()`
- c0055 ..> c0055: `prepare() calls recover()`
- c0055 ..> c0055: `recover() calls _active()`
- c0055 ..> c0055: `recover() calls _context()`
- c0055 ..> c0055: `recover() calls _ensure_worktrees()`
- c0055 ..> c0055: `recover() calls _ownership()`
- c0055 ..> c0055: `recover() calls _recovery_plan()`
- c0055 ..> c0055: `recover() calls _repository()`
- c0055 ..> c0055: `recover() calls _snapshot()`
- c0055 ..> c0055: `recover() calls _sole_recovery_owner()`
- c0055 ..> c0055: `recover() calls _validate_recovery_candidates()`
- c0055 ..> c0055: `recover() calls check_repository()`
- c0055 ..> c0055: `unfinished() calls _is_unfinished_factory_plan()`
- c0055 ..> c0060: `preflight() constructs IntakeProblem`
- c0055 ..> c0061: `_check_source() constructs RepositoryProblem`
- c0055 ..> c0061: `check_repository() constructs RepositoryProblem`
- c0055 ..> c0062: `_active() constructs ScaffoldProblem`
- c0055 ..> c0062: `_context() constructs ScaffoldProblem`
- c0055 ..> c0062: `_create_plan() constructs ScaffoldProblem`
- c0055 ..> c0062: `_ensure_mapping() constructs ScaffoldProblem`
- c0055 ..> c0062: `_ensure_validated_mapping() constructs ScaffoldProblem`
- c0055 ..> c0062: `_mapping_repository() constructs ScaffoldProblem`
- c0055 ..> c0062: `_ownership() constructs ScaffoldProblem`
- c0055 ..> c0062: `_recovery_plan() constructs ScaffoldProblem`
- c0055 ..> c0062: `_setup_ownership() constructs ScaffoldProblem`
- c0055 ..> c0062: `_snapshot() constructs ScaffoldProblem`
- c0055 ..> c0062: `_sole_recovery_owner() constructs ScaffoldProblem`
- c0055 ..> c0062: `_validate_recovery_candidates() constructs ScaffoldProblem`
- c0055 ..> c0062: `lookup() constructs ScaffoldProblem`
- c0055 ..> c0063: `_create_plan() constructs ScaffoldReadProblem`
- c0055 ..> c0063: `_ensure_setup_worktrees() constructs ScaffoldReadProblem`
- c0055 ..> c0063: `lookup() constructs ScaffoldReadProblem`
- c0055 ..> c0063: `prepare() constructs ScaffoldReadProblem`
- c0055 ..> c0063: `recover() constructs ScaffoldReadProblem`
- c0055 ..> c0064: `_create_ownership() constructs UncertainScaffold`
- c0055 ..> c0064: `_create_plan() constructs UncertainScaffold`
- c0055 ..> c0064: `_setup_ownership() constructs UncertainScaffold`
- c0055 ..> c0064: `_sole_recovery_owner() constructs UncertainScaffold`
- c0055 ..> c0064: `prepare() constructs UncertainScaffold`
- c0055 ..> c0074: `_is_unfinished_factory_plan() constructs FactoryError`
- c0055 ..> c0075: `_snapshot() constructs Issue`
- c0055 ..> c0075: `type in _create_plan`
- c0055 ..> c0075: `type in _initial_mappings`
- c0055 ..> c0075: `type in _prepare_plan`
- c0055 ..> c0075: `type in _setup_ownership`
- c0055 ..> c0075: `type in _snapshot`
- c0055 ..> c0075: `type in lookup`
- c0055 ..> c0075: `type in preflight`
- c0055 ..> c0075: `type in prepare`
- c0055 ..> c0075: `type in recover`
- c0055 ..> c0077: `type in _check_source`
- c0055 ..> c0077: `type in _ensure_validated_mapping`
- c0055 ..> c0077: `type in _mapping_repository`
- c0055 ..> c0077: `type in _repository`
- c0055 ..> c0077: `type in check_repository`
- c0055 ..> c0078: `_check_source() constructs WorkSource`
- c0055 ..> c0078: `_snapshot() constructs WorkSource`
- c0055 ..> c0078: `type in _repository`
- c0056 --> c0075: `field issue`
- c0057 ..> c0000: `_alert_plan() calls send()`
- c0057 ..> c0000: `_check_pending_repositories() calls send()`
- c0057 ..> c0000: `_check_planning_access() calls send()`
- c0057 ..> c0000: `_handle_intake_read_problem() calls send()`
- c0057 ..> c0000: `_handle_intake_repository_problem() calls send()`
- c0057 ..> c0000: `_handle_recovery_read_problem() calls send()`
- c0057 ..> c0000: `_load_inventory() calls send()`
- c0057 ..> c0000: `_process_issue() calls send()`
- c0057 ..> c0000: `_read_issues() calls send()`
- c0057 ..> c0000: `_recover_work() calls send()`
- c0057 ..> c0000: `_submit() calls send()`
- c0057 ..> c0000: `_watch() calls close()`
- c0057 ..> c0000: `_watch() calls start()`
- c0057 ..> c0000: `_watch() calls wait()`
- c0057 ..> c0000: `run() calls startup_hint()`
- c0057 ..> c0010: `_process_issue() calls prepare()`
- c0057 ..> c0012: `_check_planning_access() calls check()`
- c0057 ..> c0029: `_read_issues() calls list_issues()`
- c0057 ..> c0038: `type in _poll_sources`
- c0057 ..> c0038: `type in _repository_for_source`
- c0057 ..> c0038: `type in _watch`
- c0057 ..> c0038: `type in run`
- c0057 ..> c0046: `type in __init__`
- c0057 ..> c0055: `_check_pending_repositories() calls check_repository()`
- c0057 ..> c0055: `_load_inventory() calls unfinished()`
- c0057 ..> c0055: `_process_issue() calls lookup()`
- c0057 ..> c0055: `_process_issue() calls recover()`
- c0057 ..> c0055: `_recover_work() calls recover()`
- c0057 ..> c0055: `type in __init__`
- c0057 ..> c0056: `_complete_intake() constructs BlockedWork`
- c0057 ..> c0056: `_handle_intake_read_problem() constructs BlockedWork`
- c0057 ..> c0056: `_handle_intake_repository_problem() constructs BlockedWork`
- c0057 ..> c0056: `_handle_intake_scaffold_problem() constructs BlockedWork`
- c0057 ..> c0056: `_process_issue() constructs BlockedWork`
- c0057 ..> c0056: `_remember_inventory_candidate() constructs BlockedWork`
- c0057 ..> c0056: `type in _alert_plan`
- c0057 ..> c0056: `type in _complete_intake`
- c0057 ..> c0056: `type in _complete_recovery`
- c0057 ..> c0056: `type in _handle_recovery_read_problem`
- c0057 ..> c0056: `type in _handle_recovery_repository_problem`
- c0057 ..> c0056: `type in _recover_work`
- c0057 ..> c0056: `type in _remember_task_ids`
- c0057 ..> c0057: `_complete_intake() calls _submit()`
- c0057 ..> c0057: `_complete_recovery() calls _submit()`
- c0057 ..> c0057: `_handle_intake_read_problem() calls _sole_task_id()`
- c0057 ..> c0057: `_handle_intake_repository_problem() calls _alert_plan()`
- c0057 ..> c0057: `_handle_intake_scaffold_problem() calls _alert_plan()`
- c0057 ..> c0057: `_handle_recovery_read_problem() calls _remember_task_ids()`
- c0057 ..> c0057: `_handle_recovery_read_problem() calls _sole_task_id()`
- c0057 ..> c0057: `_handle_recovery_repository_problem() calls _alert_plan()`
- c0057 ..> c0057: `_handle_recovery_repository_problem() calls _remember_task_ids()`
- c0057 ..> c0057: `_load_inventory() calls _remember_inventory_candidate()`
- c0057 ..> c0057: `_poll_sources() calls _baseline_source()`
- c0057 ..> c0057: `_poll_sources() calls _process_source()`
- c0057 ..> c0057: `_poll_sources() calls _read_issues()`
- c0057 ..> c0057: `_poll_sources() calls _repository_for_source()`
- c0057 ..> c0057: `_process_issue() calls _complete_intake()`
- c0057 ..> c0057: `_process_issue() calls _handle_intake_read_problem()`
- c0057 ..> c0057: `_process_issue() calls _handle_intake_repository_problem()`
- c0057 ..> c0057: `_process_issue() calls _handle_intake_scaffold_problem()`
- c0057 ..> c0057: `_process_issues() calls _process_issue()`
- c0057 ..> c0057: `_process_issues() calls _skip_issue()`
- c0057 ..> c0057: `_process_source() calls _include_pending_lookups()`
- c0057 ..> c0057: `_process_source() calls _process_issues()`
- c0057 ..> c0057: `_recover_blocked() calls _recover_work()`
- c0057 ..> c0057: `_recover_work() calls _alert_plan()`
- c0057 ..> c0057: `_recover_work() calls _complete_recovery()`
- c0057 ..> c0057: `_recover_work() calls _handle_recovery_read_problem()`
- c0057 ..> c0057: `_recover_work() calls _handle_recovery_repository_problem()`
- c0057 ..> c0057: `_recover_work() calls _remember_task_ids()`
- c0057 ..> c0057: `_remember_inventory_candidate() calls _alert_plan()`
- c0057 ..> c0057: `_watch() calls _check_pending_repositories()`
- c0057 ..> c0057: `_watch() calls _check_planning_access()`
- c0057 ..> c0057: `_watch() calls _load_inventory()`
- c0057 ..> c0057: `_watch() calls _poll_sources()`
- c0057 ..> c0057: `_watch() calls _recover_blocked()`
- c0057 ..> c0057: `run() calls _watch()`
- c0057 ..> c0058: `_watch() constructs _WatchState`
- c0057 ..> c0058: `type in _baseline_source`
- c0057 ..> c0058: `type in _check_pending_repositories`
- c0057 ..> c0058: `type in _check_planning_access`
- c0057 ..> c0058: `type in _complete_intake`
- c0057 ..> c0058: `type in _complete_recovery`
- c0057 ..> c0058: `type in _handle_intake_read_problem`
- c0057 ..> c0058: `type in _handle_intake_repository_problem`
- c0057 ..> c0058: `type in _handle_intake_scaffold_problem`
- c0057 ..> c0058: `type in _handle_recovery_repository_problem`
- c0057 ..> c0058: `type in _load_inventory`
- c0057 ..> c0058: `type in _poll_sources`
- c0057 ..> c0058: `type in _process_issue`
- c0057 ..> c0058: `type in _process_issues`
- c0057 ..> c0058: `type in _process_source`
- c0057 ..> c0058: `type in _recover_blocked`
- c0057 ..> c0058: `type in _recover_work`
- c0057 ..> c0058: `type in _remember_inventory_candidate`
- c0057 ..> c0058: `type in _skip_issue`
- c0057 ..> c0059: `type in _process_issue`
- c0057 ..> c0059: `type in _recover_work`
- c0057 ..> c0061: `type in _handle_intake_repository_problem`
- c0057 ..> c0061: `type in _handle_recovery_repository_problem`
- c0057 ..> c0062: `_remember_inventory_candidate() constructs ScaffoldProblem`
- c0057 ..> c0062: `type in _alert_plan`
- c0057 ..> c0062: `type in _handle_intake_scaffold_problem`
- c0057 ..> c0063: `type in _handle_intake_read_problem`
- c0057 ..> c0063: `type in _handle_recovery_read_problem`
- c0057 ..> c0065: `_check_pending_repositories() calls clear()`
- c0057 ..> c0065: `_check_planning_access() calls clear()`
- c0057 ..> c0065: `_complete_intake() calls clear()`
- c0057 ..> c0065: `_complete_recovery() calls clear()`
- c0057 ..> c0065: `_load_inventory() calls clear()`
- c0057 ..> c0065: `_process_issue() calls clear()`
- c0057 ..> c0065: `_read_issues() calls clear()`
- c0057 ..> c0065: `_watch() calls clear()`
- c0057 ..> c0065: `_watch() constructs WatcherAlerts`
- c0057 ..> c0065: `type in _alert_plan`
- c0057 ..> c0065: `type in _check_pending_repositories`
- c0057 ..> c0065: `type in _check_planning_access`
- c0057 ..> c0065: `type in _complete_intake`
- c0057 ..> c0065: `type in _complete_recovery`
- c0057 ..> c0065: `type in _handle_intake_read_problem`
- c0057 ..> c0065: `type in _handle_intake_repository_problem`
- c0057 ..> c0065: `type in _handle_intake_scaffold_problem`
- c0057 ..> c0065: `type in _handle_recovery_read_problem`
- c0057 ..> c0065: `type in _handle_recovery_repository_problem`
- c0057 ..> c0065: `type in _load_inventory`
- c0057 ..> c0065: `type in _poll_sources`
- c0057 ..> c0065: `type in _process_issue`
- c0057 ..> c0065: `type in _process_issues`
- c0057 ..> c0065: `type in _process_source`
- c0057 ..> c0065: `type in _read_issues`
- c0057 ..> c0065: `type in _recover_blocked`
- c0057 ..> c0065: `type in _recover_work`
- c0057 ..> c0065: `type in _remember_inventory_candidate`
- c0057 ..> c0074: `_read_issues() constructs FactoryError`
- c0057 ..> c0075: `type in _baseline_source`
- c0057 ..> c0075: `type in _complete_intake`
- c0057 ..> c0075: `type in _complete_recovery`
- c0057 ..> c0075: `type in _handle_intake_read_problem`
- c0057 ..> c0075: `type in _handle_intake_repository_problem`
- c0057 ..> c0075: `type in _handle_intake_scaffold_problem`
- c0057 ..> c0075: `type in _include_pending_lookups`
- c0057 ..> c0075: `type in _process_issue`
- c0057 ..> c0075: `type in _process_issues`
- c0057 ..> c0075: `type in _process_source`
- c0057 ..> c0075: `type in _read_issues`
- c0057 ..> c0075: `type in _skip_issue`
- c0057 ..> c0075: `type in _submit`
- c0057 ..> c0077: `type in _handle_intake_repository_problem`
- c0057 ..> c0077: `type in _process_issue`
- c0057 ..> c0077: `type in _process_issues`
- c0057 ..> c0077: `type in _process_source`
- c0057 ..> c0077: `type in _repository_for_source`
- c0057 ..> c0078: `_watch() constructs WorkSource`
- c0057 ..> c0078: `type in _baseline_source`
- c0057 ..> c0078: `type in _include_pending_lookups`
- c0057 ..> c0078: `type in _poll_sources`
- c0057 ..> c0078: `type in _process_source`
- c0057 ..> c0078: `type in _read_issues`
- c0057 ..> c0078: `type in _repository_for_source`
- c0057 ..> c0079: `type in __init__`
- c0058 --> c0056: `field blocked`
- c0058 --> c0056: `field known`
- c0058 --> c0075: `field pending_lookup`
- c0058 --> c0077: `field pending_repositories`
- c0058 --> c0078: `field baselined`
- c0060 --|> c0062: `inherits`
- c0061 --|> c0062: `inherits`
- c0062 --|> c0074: `inherits`
- c0063 --|> c0062: `inherits`
- c0064 --|> c0062: `inherits`
- c0065 ..> c0000: `__init__() calls __init__()`
- c0065 ..> c0000: `send() calls send()`
- c0065 ..> c0074: `type in send`
- c0066 ..> c0007: `build_watcher() constructs AgentShellTerminal`
- c0066 ..> c0012: `build_initialiser() constructs ForemanProfile`
- c0066 ..> c0012: `build_watcher() calls managed_memory_notice()`
- c0066 ..> c0012: `prepare_foreman_launch() calls pi_home()`
- c0066 ..> c0012: `prepare_foreman_launch() calls selected_launch()`
- c0066 ..> c0012: `prepare_foreman_launch() calls validate_completion()`
- c0066 ..> c0012: `prepare_foreman_launch() constructs ForemanProfile`
- c0066 ..> c0014: `build_initialiser() constructs GitRepositories`
- c0066 ..> c0014: `build_watcher() constructs GitRepositories`
- c0066 ..> c0016: `build_watcher() constructs GitWorktrees`
- c0066 ..> c0020: `build_initialiser() constructs TomlConfigurationStore`
- c0066 ..> c0026: `prepare_foreman_launch() calls role_environment()`
- c0066 ..> c0027: `build_watcher() constructs ForgetfulPlanning`
- c0066 ..> c0029: `build_initialiser() constructs GitHubWorkTracking`
- c0066 ..> c0029: `build_watcher() calls check_cli()`
- c0066 ..> c0029: `build_watcher() calls source_from_remote()`
- c0066 ..> c0029: `build_watcher() constructs GitHubWorkTracking`
- c0066 ..> c0033: `build_watcher() constructs ObservedTerminal`
- c0066 ..> c0038: `type in build_watcher`
- c0066 ..> c0038: `type in prepare_foreman_launch`
- c0066 ..> c0043: `build_initialiser() constructs InitialiseFactory`
- c0066 ..> c0043: `type in build_initialiser`
- c0066 ..> c0055: `build_watcher() constructs ScaffoldIssue`
- c0066 ..> c0057: `build_watcher() constructs WatchFactory`
- c0066 ..> c0057: `type in build_watcher`
- c0066 ..> c0066: `build_watcher() calls prepare_foreman_launch()`
- c0066 ..> c0072: `build_initialiser() constructs DeadlinePolicy`
- c0066 ..> c0072: `build_watcher() constructs DeadlinePolicy`
- c0066 ..> c0072: `type in build_initialiser`
- c0066 ..> c0072: `type in build_watcher`
- c0066 ..> c0074: `build_watcher() constructs FactoryError`
- c0066 ..> c0074: `prepare_foreman_launch() constructs FactoryError`
- c0067 --> c0038: `field config`
- c0067 --> c0039: `field connection`
- c0068 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0068 ..> c0004: `_watch_locked() calls run()`
- c0068 ..> c0006: `_change_managed_watch() calls request()`
- c0068 ..> c0006: `_foreman() calls enter_terminal()`
- c0068 ..> c0006: `_foreman() calls read_state()`
- c0068 ..> c0006: `_foreman() calls request()`
- c0068 ..> c0006: `_foreman() calls start_owner()`
- c0068 ..> c0006: `_initialise() calls enter_terminal()`
- c0068 ..> c0006: `_initialise() calls request()`
- c0068 ..> c0006: `_initialise_locked() calls read_state()`
- c0068 ..> c0006: `_launch_setup_foreman() calls start_owner()`
- c0068 ..> c0006: `_managed_watch_status() calls read_state()`
- c0068 ..> c0006: `_managed_watch_status() calls request()`
- c0068 ..> c0006: `_offer_factory_launch() calls read_state()`
- c0068 ..> c0006: `_watch_locked() calls read_state()`
- c0068 ..> c0012: `_complete_setup() calls managed_memory_notice()`
- c0068 ..> c0012: `_complete_setup() calls record_completion()`
- c0068 ..> c0012: `_complete_setup() calls uses_browser_login()`
- c0068 ..> c0012: `_discover_worker_models() calls list_models()`
- c0068 ..> c0012: `_finish_existing_setup() calls choose_pi_home()`
- c0068 ..> c0012: `_finish_existing_setup() calls save_pi_choice()`
- c0068 ..> c0012: `_finish_existing_setup() calls selected_launch()`
- c0068 ..> c0012: `_foreman() calls managed_memory_notice()`
- c0068 ..> c0012: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0068 ..> c0012: `_select_model() calls list_models()`
- c0068 ..> c0012: `_select_project() calls create_project()`
- c0068 ..> c0012: `_select_project() calls projects()`
- c0068 ..> c0012: `_start_initial_setup() calls begin_setup()`
- c0068 ..> c0012: `_start_initial_setup() calls choose_pi_home()`
- c0068 ..> c0012: `_validate_initial_model() calls prepare_roles()`
- c0068 ..> c0012: `_watch_status() calls validate_completion()`
- c0068 ..> c0012: `_watch_status() constructs ForemanProfile`
- c0068 ..> c0014: `select_repositories() calls discover()`
- c0068 ..> c0016: `_configure_new_factory() calls inspect()`
- c0068 ..> c0018: `_discover_worker_models() calls check_real_path()`
- c0068 ..> c0020: `_initialise_locked() calls load()`
- c0068 ..> c0021: `_initialise() calls quote()`
- c0068 ..> c0021: `_launch_setup_foreman() calls quote()`
- c0068 ..> c0021: `_managed_watch_status() calls quote()`
- c0068 ..> c0021: `_select_model() calls quote()`
- c0068 ..> c0021: `_validate_setup_owner() calls quote()`
- c0068 ..> c0021: `_watch_locked() calls quote()`
- c0068 ..> c0022: `_foreman() calls hold()`
- c0068 ..> c0022: `_foreman() constructs WorkspaceWatchLease`
- c0068 ..> c0022: `_initialise() calls hold()`
- c0068 ..> c0022: `_initialise() constructs WorkspaceWatchLease`
- c0068 ..> c0022: `_watch() calls hold()`
- c0068 ..> c0022: `_watch() constructs WorkspaceWatchLease`
- c0068 ..> c0034: `_prompt_workers() calls update()`
- c0068 ..> c0035: `_managed_watch_status() calls unknown_status()`
- c0068 ..> c0035: `_watch_locked() calls observe_plain_watch()`
- c0068 ..> c0035: `_watch_status() calls plain_watch_status()`
- c0068 ..> c0035: `_watch_status() calls unknown_status()`
- c0068 ..> c0038: `type in _complete_setup`
- c0068 ..> c0038: `type in _configure_new_factory`
- c0068 ..> c0038: `type in _finish_existing_setup`
- c0068 ..> c0038: `type in _validate_initial_model`
- c0068 ..> c0039: `_connection() calls validate()`
- c0068 ..> c0039: `_connection() constructs ForgetfulConnection`
- c0068 ..> c0039: `type in _check_existing_connection`
- c0068 ..> c0039: `type in _configure_new_factory`
- c0068 ..> c0039: `type in _connection`
- c0068 ..> c0039: `type in _foreman_memory_choices`
- c0068 ..> c0039: `type in _managed_rest_mapping_available`
- c0068 ..> c0039: `type in _select_project`
- c0068 ..> c0041: `_configure_new_factory() constructs InitialAgentChoices`
- c0068 ..> c0041: `type in _configure_new_factory`
- c0068 ..> c0041: `type in _foreman_memory_choices`
- c0068 ..> c0041: `type in _owner_choices`
- c0068 ..> c0041: `type in _prompt_coordinator_choices`
- c0068 ..> c0041: `type in _validate_initial_model`
- c0068 ..> c0041: `type in _worker_choices`
- c0068 ..> c0042: `_start_initial_setup() calls validate_initial_agents()`
- c0068 ..> c0043: `_complete_setup() calls check_foreman()`
- c0068 ..> c0043: `_configure_new_factory() calls configure()`
- c0068 ..> c0043: `_finish_existing_setup() calls initialise()`
- c0068 ..> c0043: `_initialise_locked() calls load_existing()`
- c0068 ..> c0043: `_launch_setup_foreman() calls check_foreman()`
- c0068 ..> c0043: `_prepare_foreman() calls prepare_foreman()`
- c0068 ..> c0043: `_start_initial_setup() calls initialise()`
- c0068 ..> c0043: `type in _complete_setup`
- c0068 ..> c0043: `type in _configure_new_factory`
- c0068 ..> c0043: `type in _discover_worker_models`
- c0068 ..> c0043: `type in _finish_existing_setup`
- c0068 ..> c0043: `type in _select_project`
- c0068 ..> c0043: `type in _start_initial_setup`
- c0068 ..> c0043: `type in _validate_initial_model`
- c0068 ..> c0043: `type in select_repositories`
- c0068 ..> c0066: `_foreman() calls prepare_foreman_launch()`
- c0068 ..> c0066: `_initialise_locked() calls build_initialiser()`
- c0068 ..> c0066: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0068 ..> c0066: `_watch_locked() calls build_watcher()`
- c0068 ..> c0067: `_start_initial_setup() constructs _InitialSetupState`
- c0068 ..> c0067: `type in _discover_worker_models`
- c0068 ..> c0067: `type in _validate_initial_model`
- c0068 ..> c0068: `_complete_setup() calls _managed_rest_mapping_available()`
- c0068 ..> c0068: `_configure_new_factory() calls _prepare_foreman()`
- c0068 ..> c0068: `_configure_new_factory() calls _select_model()`
- c0068 ..> c0068: `_configure_new_factory() calls _select_numbered()`
- c0068 ..> c0068: `_configure_new_factory() calls select_repositories()`
- c0068 ..> c0068: `_connection() calls _check_existing_connection()`
- c0068 ..> c0068: `_discover_worker_models() calls _prepare_foreman()`
- c0068 ..> c0068: `_finish_existing_setup() calls _complete_setup()`
- c0068 ..> c0068: `_finish_existing_setup() calls _confirm_pi_home()`
- c0068 ..> c0068: `_finish_existing_setup() calls _connection()`
- c0068 ..> c0068: `_foreman_memory_choices() calls _managed_rest_mapping_available()`
- c0068 ..> c0068: `_foreman_memory_choices() calls _select_numbered()`
- c0068 ..> c0068: `_initialise() calls _initialise_locked()`
- c0068 ..> c0068: `_initialise() calls _offer_factory_launch()`
- c0068 ..> c0068: `_initialise_locked() calls _finish_existing_setup()`
- c0068 ..> c0068: `_initialise_locked() calls _start_initial_setup()`
- c0068 ..> c0068: `_initialise_locked() calls _validate_setup_owner()`
- c0068 ..> c0068: `_print_models() calls _safe_diagnostic()`
- c0068 ..> c0068: `_prompt_coordinator_choices() calls _select_numbered()`
- c0068 ..> c0068: `_prompt_worker() calls _select_numbered()`
- c0068 ..> c0068: `_prompt_workers() calls _prompt_worker()`
- c0068 ..> c0068: `_select_model() calls _print_models()`
- c0068 ..> c0068: `_select_model() calls _select_numbered()`
- c0068 ..> c0068: `_select_numbered() calls _safe_diagnostic()`
- c0068 ..> c0068: `_select_project() calls _listed_project_id()`
- c0068 ..> c0068: `_select_project() calls _safe_diagnostic()`
- c0068 ..> c0068: `_select_setup_route() calls _select_numbered()`
- c0068 ..> c0068: `_start_initial_setup() calls _complete_setup()`
- c0068 ..> c0068: `_start_initial_setup() calls _configure_new_factory()`
- c0068 ..> c0068: `_start_initial_setup() calls _confirm_pi_home()`
- c0068 ..> c0068: `_start_initial_setup() calls _connection()`
- c0068 ..> c0068: `_start_initial_setup() calls _foreman_memory_choices()`
- c0068 ..> c0068: `_start_initial_setup() calls _launch_setup_foreman()`
- c0068 ..> c0068: `_start_initial_setup() calls _owner_choices()`
- c0068 ..> c0068: `_start_initial_setup() calls _research_choices()`
- c0068 ..> c0068: `_start_initial_setup() calls _worker_choices()`
- c0068 ..> c0068: `_validate_initial_model() calls _prepare_foreman()`
- c0068 ..> c0068: `_validate_initial_model() calls _select_model()`
- c0068 ..> c0068: `_validate_initial_model() calls _select_project()`
- c0068 ..> c0068: `_watch() calls _change_managed_watch()`
- c0068 ..> c0068: `_watch() calls _watch_locked()`
- c0068 ..> c0068: `_watch() calls _watch_status()`
- c0068 ..> c0068: `_watch_locked() calls _choose_existing()`
- c0068 ..> c0068: `_watch_locked() calls _safe_diagnostic()`
- c0068 ..> c0068: `_watch_status() calls _managed_watch_status()`
- c0068 ..> c0068: `_worker_choices() calls _prompt_coordinator_choices()`
- c0068 ..> c0068: `_worker_choices() calls _prompt_workers()`
- c0068 ..> c0068: `_worker_choices() calls _select_setup_route()`
- c0068 ..> c0068: `_worker_choices() calls _worker_arguments()`
- c0068 ..> c0068: `main() calls _foreman()`
- c0068 ..> c0068: `main() calls _initialise()`
- c0068 ..> c0068: `main() calls _parse_arguments()`
- c0068 ..> c0068: `main() calls _safe_diagnostic()`
- c0068 ..> c0068: `main() calls _watch()`
- c0068 ..> c0069: `_select_numbered() calls parse_numbered_selection()`
- c0068 ..> c0070: `_foreman() calls load_configuration()`
- c0068 ..> c0070: `_watch_locked() calls load_configuration()`
- c0068 ..> c0070: `_watch_status() calls load_configuration()`
- c0068 ..> c0072: `main() constructs DeadlinePolicy`
- c0068 ..> c0072: `type in _foreman`
- c0068 ..> c0072: `type in _initialise`
- c0068 ..> c0072: `type in _initialise_locked`
- c0068 ..> c0072: `type in _start_initial_setup`
- c0068 ..> c0072: `type in _watch`
- c0068 ..> c0072: `type in _watch_locked`
- c0068 ..> c0072: `type in main`
- c0068 ..> c0074: `_change_managed_watch() constructs FactoryError`
- c0068 ..> c0074: `_check_existing_connection() constructs FactoryError`
- c0068 ..> c0074: `_choose_existing() constructs FactoryError`
- c0068 ..> c0074: `_configure_new_factory() constructs FactoryError`
- c0068 ..> c0074: `_foreman() constructs FactoryError`
- c0068 ..> c0074: `_foreman_memory_choices() constructs FactoryError`
- c0068 ..> c0074: `_initialise() constructs FactoryError`
- c0068 ..> c0074: `_initialise_locked() constructs FactoryError`
- c0068 ..> c0074: `_install_missing() constructs FactoryError`
- c0068 ..> c0074: `_listed_project_id() constructs FactoryError`
- c0068 ..> c0074: `_prompt_coordinator_choices() constructs FactoryError`
- c0068 ..> c0074: `_prompt_worker() constructs FactoryError`
- c0068 ..> c0074: `_select_model() constructs FactoryError`
- c0068 ..> c0074: `_select_project() constructs FactoryError`
- c0068 ..> c0074: `_validate_setup_owner() constructs FactoryError`
- c0068 ..> c0074: `_watch_locked() constructs FactoryError`
- c0068 ..> c0074: `_worker_choices() constructs FactoryError`
- c0068 ..> c0074: `main() constructs FactoryError`
- c0068 ..> c0074: `select_repositories() constructs FactoryError`
- c0069 ..> c0074: `parse_numbered_selection() constructs FactoryError`
- c0070 ..> c0020: `load_configuration() calls load()`
- c0070 ..> c0020: `load_configuration() constructs TomlConfigurationStore`
- c0070 ..> c0038: `type in load_configuration`
- c0070 ..> c0074: `load_configuration() constructs FactoryError`
- c0072 --> c0071: `field agentshell`
- c0072 ..> c0073: `__post_init__() calls _validate_duration()`
- c0075 --> c0078: `field source`
- c0077 --> c0078: `field work_source`
- c0079 ..> c0075: `type in list_issues`
- c0079 ..> c0076: `type in create_label`
- c0079 ..> c0076: `type in list_labels`
- c0079 ..> c0078: `type in check_access`
- c0079 ..> c0078: `type in create_label`
- c0079 ..> c0078: `type in list_issues`
- c0079 ..> c0078: `type in list_labels`

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
- Type11: `tuple[Path, list[dict]]`
- Type12: `tuple[Path, Path] | None`
- Type13: `dict[Path, None]`
- Type14: `frozenset[tuple[int, int]]`
- Type15: `FactoryConfiguration | None`
- Type16: `dict[str, str]`
- Type17: `tuple[Label, ...]`
- Type18: `tuple[Issue, ...]`
- Type19: `tuple[str, ...]`
- Type20: `tuple[Path, ...]`
- Type21: `float | None`
- Type22: `tuple[int, int]`
- Type23: `Iterator[PlainWatchObservation | None]`
- Type24: `Callable[[str], None]`
- Type25: `CleanupState | None`
- Type26: `tuple[RepositoryReference, ...]`
- Type27: `ForgetfulConnection | None`
- Type28: `Callable[[list[str]], None]`
- Type29: `Callable[[str, str], bool]`
- Type30: `list[Path] | None`
- Type31: `list[str] | None`
- Type32: `dict[str, RepositoryReference]`
- Type33: `dict[WorkSource, tuple[Label, ...]]`
- Type34: `Callable[[], FactoryConfiguration | None]`
- Type35: `tuple[list[dict], list[dict]]`
- Type36: `tuple[Issue, dict] | None`
- Type37: `Issue | None`
- Type38: `tuple[int, ...] | None`
- Type39: `tuple[int, ...]`
- Type40: `Callable[[], bool]`
- Type41: `tuple[set[str], bool]`
- Type42: `tuple[WorkSource, ...]`
- Type43: `dict[str, Issue]`
- Type44: `BlockedWork | None`
- Type45: `tuple[Issue, ...] | None`
- Type46: `dict[str, BlockedWork]`
- Type47: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type48: `list[str] | tuple[str, ...]`
- Type49: `int | dict`
- Type50: `int | dict | str`
- Type51: `str | Path`

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
- Signature13: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature14: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool,
  term_grace: float) unknown`
- Signature15: `+run_owned(args: list[str], cwd: Path, env: dict[str, str], login: bool, timeout:
  float | None, term_grace: float) str`
- Signature16: `-__init__(tracking: WorkTrackingService, storage: ConfigurationStore, repositories:
  LocalRepositories, sources: WorkSourceResolver, profile: ForemanProfile) unknown`
- Signature17: `-__init__(planning: Planning, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration, repositories: LocalRepositories, sources: WorkSourceResolver) unknown`
- Signature18: `-_create_ownership(plan_id: int, external_ref: str, context: dict, mappings:
  list[dict]) list[dict]`
- Signature19: `-_validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
  known_ids: tuple[int, ...] | None) None`
- Signature20: `-_ensure_validated_mapping(repository: RepositoryReference, mapping: dict, recorded:
  bool) None`
- Signature21: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, scaffold:
  ScaffoldIssue) unknown`
- Signature22: `+run(config: FactoryConfiguration, workspace: Path, interval: float,
  choose_existing: Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str],
  None]) None`
- Signature23: `-_watch(config: FactoryConfiguration, interval: float, existing: bool, report:
  Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature24: `-_remember_inventory_candidate(reference: str, plan_ids: list[int], state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature25: `-_recover_work(subject: str, work: BlockedWork, state: _WatchState, alerts:
  WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature26: `-_handle_recovery_repository_problem(work: BlockedWork, error: RepositoryProblem,
  state: _WatchState, alerts: WatcherAlerts) None`
- Signature27: `-_handle_recovery_read_problem(work: BlockedWork, error: ScaffoldReadProblem,
  alerts: WatcherAlerts) None`
- Signature28: `-_complete_recovery(subject: str, work: BlockedWork, result: tuple[Issue, dict] |
  None, state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature29: `-_poll_sources(sources: tuple[WorkSource, ...], config: FactoryConfiguration,
  existing: bool, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature30: `-_process_source(source: WorkSource, issues: tuple[Issue, ...], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature31: `-_baseline_source(source: WorkSource, issues: tuple[Issue, ...], state: _WatchState,
  report: Callable[[str], None]) None`
- Signature32: `-_repository_for_source(config: FactoryConfiguration, source: WorkSource)
  RepositoryReference`
- Signature33: `-_include_pending_lookups(source: WorkSource, current: dict[str, Issue],
  pending_lookup: dict[str, Issue]) None`
- Signature34: `-_process_issues(issues: tuple[Issue, ...], eligible: set[str], repository:
  RepositoryReference, state: _WatchState, attempted: set[str], alerts: WatcherAlerts, report:
  Callable[[str], None]) bool`
- Signature35: `-_process_issue(issue: Issue, eligible: set[str], repository: RepositoryReference,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) _WorkAction`
- Signature36: `-_handle_intake_repository_problem(issue: Issue, repository: RepositoryReference,
  error: RepositoryProblem, state: _WatchState, alerts: WatcherAlerts) None`
- Signature37: `-_handle_intake_read_problem(issue: Issue, error: ScaffoldReadProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature38: `-_handle_intake_scaffold_problem(issue: Issue, error: ScaffoldProblem, state:
  _WatchState, alerts: WatcherAlerts) None`
- Signature39: `-_complete_intake(issue: Issue, scaffold: dict | None, work: BlockedWork | None,
  state: _WatchState, alerts: WatcherAlerts, report: Callable[[str], None]) None`
- Signature40: `-_submit(issue: Issue, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature41: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature42: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature43: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown, deadlines: DeadlinePolicy, observation: unknown) WatchFactory`
- Signature44: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown, term_grace: float) unknown`
- Signature45: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature46: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature47: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature48: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature49: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature50: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature51: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature52: `-_prompt_coordinator_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature53: `-_foreman_memory_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown, connection: ForgetfulConnection) InitialAgentChoices`
- Signature54: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature55: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature56: `-_finish_existing_setup(application: InitialiseFactory, config:
  FactoryConfiguration, args: argparse.Namespace, workspace: Path) int`
- Signature57: `-_discover_worker_models(harness: unknown, role: unknown, application:
  InitialiseFactory, args: argparse.Namespace, workspace: Path, state: _InitialSetupState) unknown`
- Signature58: `-_validate_initial_model(application: InitialiseFactory, args: argparse.Namespace,
  choices: InitialAgentChoices, home: str, workspace: Path, state: _InitialSetupState)
  FactoryConfiguration`
- Signature59: `-_start_initial_setup(application: InitialiseFactory, args: argparse.Namespace,
  workspace: Path, paths: list[Path] | None, deadlines: DeadlinePolicy) int | dict`
- Signature60: `-_initialise_locked(args: argparse.Namespace, workspace: Path, deadlines:
  DeadlinePolicy) int | dict | str`
- Signature61: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
  args: unknown, deadlines: unknown) unknown`

## Extraction warnings

- `Unresolved or out-of-scope base: CleanupMarkerError -> ValueError`
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
