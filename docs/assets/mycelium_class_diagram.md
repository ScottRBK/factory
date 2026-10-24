# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 56 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 1843. Type relationships removed: 42.

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
- `tests/test_init.py`: 43 source occurrences (test-path).
- `tests/test_init_launch.py`: 13 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 20 source occurrences (test-path).
- `tests/test_local_skills.py`: 21 source occurrences (test-path).
- `tests/test_native_assisted_reload.py`: 2 source occurrences (test-path).
- `tests/test_native_roles.py`: 4 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_normalized_lifecycle.py`: 8 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_planning_setup.py`: 13 source occurrences (test-path).
- `tests/test_planning_watch.py`: 27 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_review_regressions.py`: 54 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 23 source occurrences (test-path).
- `tests/test_watch.py`: 51 source occurrences (test-path).
- `tests/test_watch_lock.py`: 6 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 18 source occurrences (test-path).
- `tests/test_worker_profiles.py`: 8 source occurrences (test-path).
- `tests/test_worker_setup.py`: 15 source occurrences (test-path).
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
    class c0001["src/forgetful_factory/adapters/agentshell/controller.py"] {
        <<module>>
        +ready(session: unknown) None
        +interact(Signature1)
        +retain_identity(session: unknown, reply: unknown) None
        +pin_worker(target: unknown) int
        +worker_exited(descriptor: unknown) None
        +resume_exit_observation(session: unknown) int
        +runtime() unknown
        +serve(reader: unknown, config: unknown, reply: unknown, opened: unknown) None
        +control(reply: unknown) None
        +main(reply: unknown) int
        +reply(value: unknown) unknown
    }
    class c0002["src/forgetful_factory/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0003["ForemanOwner"] {
        <<class>>
        -__init__(workspace: Path, python: str) unknown
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
        +observe() unknown
        +state#91;#39;foreman#39;#93;: unknown
        +state#91;#39;warning#39;#93;: unknown
        +state#91;#39;target#39;#93;: unknown
        +relay(reader: unknown, writer: unknown) unknown
        +state#91;#39;watcher#39;#93;: unknown
        +reap_watcher(child: unknown, relay: unknown) unknown
        +start_watcher(value: unknown) unknown
        +stop_watcher() unknown
        +control(reader: unknown, writer: unknown) unknown
        +run(handover: unknown) unknown
    }
    class c0004["src/forgetful_factory/adapters/agentshell/owner.py"] {
        <<module>>
        +main() unknown
    }
    class c0005["src/forgetful_factory/adapters/agentshell/owner_client.py"] {
        <<module>>
        -_reply(stream: unknown) dict
        +read_state(workspace: Path) Type1
        +request(workspace: Path, operation: str, fields: unknown) dict
        +start_owner(workspace: Path, python: str, environment: dict, launch: dict) dict
        +enter_terminal(target: dict) None
    }
    class c0006["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature2)
        +python: unknown
        +environment: unknown
        +resources: unknown
        +prompt: unknown
        +cwd: unknown
        +model: unknown
        +effort: unknown
        +process: Type4
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
    class c0007["src/forgetful_factory/adapters/command.py"] {
        <<module>>
        +run_command(arguments: list[str]) str
    }
    class c0008["src/forgetful_factory/adapters/filesystem/agent_definitions.py"] {
        <<module>>
        +relative_path(directory: Path, value: str) Path
        +read_definition(path: Path) dict
        +foreman_launch(path: Path) dict
    }
    class c0009["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(config: FactoryConfiguration, choices: unknown) None
        -_write_agent(Signature3)
        +validate_guidance(config: FactoryConfiguration) None
    }
    class c0010["src/forgetful_factory/adapters/filesystem/coordinator_profiles.py"] {
        <<module>>
        +selected_resources(skills: list[str], extensions: list[str]) dict
    }
    class c0011["ForemanProfile"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +foreman_skill: unknown
        +bundle_directory: unknown
        -_pi_choice: Type1
        -_model_catalogs: Type5
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
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type6) list[str]
        -_model_catalogs#91;key#93;: unknown
        +selected_launch(config: FactoryConfiguration) dict
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
        +validate_completion(config: FactoryConfiguration) None
        -_read_guidance(path: Path) str
        +validate_guidance(include_home_system_prompt: bool) None
    }
    class c0012["src/forgetful_factory/adapters/filesystem/foreman_runtime.py"] {
        <<module>>
        +runtime_directory(workspace: Path, create: bool) Path
    }
    class c0013["GitRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0014["GitWorktrees"] {
        <<class>>
        -_repository_entries(repository: str, remote: str) Type7
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
    }
    class c0015["src/forgetful_factory/adapters/filesystem/git_worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0016["src/forgetful_factory/adapters/filesystem/resource_files.py"] {
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
    class c0017["src/forgetful_factory/adapters/filesystem/selected_skills.py"] {
        <<module>>
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0018["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type8
        +save(configuration: FactoryConfiguration) None
    }
    class c0019["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0020["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0021["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0022["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0023["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +role: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type9
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0024["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature4)
        -_catalog_tools(catalog: object) dict
    }
    class c0025["ForgetfulPlanning"] {
        <<class>>
        -__init__(Signature5)
        +cli: unknown
        +connection: unknown
        +execution_enabled: unknown
        +check() None
        -_call(tool: str, fields: unknown) dict
        +plans(external_ref: Type3) list[dict]
        -_rows(result: dict, key: str) list[dict]
        +get_plan(plan_id: int) dict
        +create_plan(fields: unknown) dict
        +update_plan(plan_id: int, fields: unknown) dict
        +tasks(plan_id: int) list[dict]
        +create_task(fields: unknown) dict
        +update_task(task_id: int, fields: unknown) dict
    }
    class c0026["GitHubWorkTracking"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type10
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type12) Type11
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0027["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +runtime: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type2) Type9
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type2) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0028["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type13) str
        +runtime_ready(runtime: Path, inputs: Type13, probe: str) bool
    }
    class c0029["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        +run_owned(args: list[str], cwd: Path, env: Type9, login: bool, timeout: Type14) str
    }
    class c0030["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type12
        +foreman_agent_file: str
        +repository: Type15
        +forgetful: Type16
        +execution_enabled: bool
    }
    class c0031["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type3
        +server: Type3
        +project_id: Type17
        +validate() None
        -_validate_server() None
    }
    class c0032["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type16
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type12
    }
    class c0033["InitialAgentChoices"] {
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
        +implementation_skills: Type12
        +review_skills: Type12
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0034["src/forgetful_factory/application/initial_agent_choices.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type12
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0035["InitialiseFactory"] {
        <<class>>
        -__init__(Signature6)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type18, confirm: Type19) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type20, labels: Type21) Type8
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type22
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type23
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type24, save: bool) list[str]
    }
    class c0036["ConfigurationStore"] {
        <<class>>
        +load() Type8
        +save(configuration: FactoryConfiguration) None
    }
    class c0037["ForemanProfile"] {
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
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type6) list[str]
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
    }
    class c0038["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0039["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0040["Planning"] {
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
    class c0041["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0042["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0043["Worktrees"] {
        <<class>>
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
    }
    class c0044["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature7)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +check() None
        +prepare(issue: Issue) dict
        -_issue_plan(issue: Issue) dict
        +unfinished() list[Issue]
        -_is_unfinished_factory_plan(summary: dict, sources: set[str]) bool
        -_context(plan: dict) dict
        -_ownership(plan_id: int, external_ref: str) list[dict]
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0045["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        -_cleanup_state(mapping: dict) Type3
    }
    class c0046["WatchFactory"] {
        <<class>>
        -__init__(Signature8)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +run(Signature9)
        -_watch(Signature10)
        -_notify_issues(issues: Type11, seen: Type9, report: Type26, recovered: bool) None
        -_read_issues(source: WorkSource, labels: Type12, report_error: Type26) Type27
    }
    class c0047["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path) InitialiseFactory
        +build_watcher(Signature11)
        +prepare_foreman_launch(Signature12)
    }
    class c0048["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature13)
        -_check_existing_connection(Signature14)
        -_connection(Signature15)
        -_prepare_foreman(Signature16)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type29, show_choices: bool, prompt: Type3) str
        -_select_model(Signature17)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_watch(args: argparse.Namespace, workspace: Path) int
        -_foreman(args: argparse.Namespace, workspace: Path) int
        -_watch_locked(args: argparse.Namespace, workspace: Path) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature18)
        -_owner_choices(Signature19)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_worker_choices(Signature20)
        -_complete_setup(Signature21)
        -_initialise(args: argparse.Namespace, workspace: Path) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_initialise_locked(args: argparse.Namespace, workspace: Path) Type30
        -_launch_setup_foreman(Signature22)
        +main() int
    }
    class c0049["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type31) FactoryConfiguration
    }
    class c0050["FactoryError"] {
        <<class>>
    }
    class c0051["Issue"] {
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
    class c0052["Label"] {
        <<class>>
        +name: str
    }
    class c0053["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0054["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0055["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type10
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type12) Type11
    }
    c0000 ..> c0000 : 2 relationships (see list)
    c0000 ..> c0006 : close() calls close()
    c0000 ..> c0050 : 2 relationships (see list)
    c0001 ..> c0000 : 6 relationships (see list)
    c0001 ..> c0001 : 9 relationships (see list)
    c0001 ..> c0025 : 3 relationships (see list)
    c0002 ..> c0011 : main() calls list_models()
    c0003 ..> c0000 : 6 relationships (see list)
    c0003 ..> c0003 : 10 relationships (see list)
    c0003 ..> c0005 : run() calls read_state()
    c0003 ..> c0012 : __init__() calls runtime_directory()
    c0003 ..> c0016 : save() calls replace_generated_json()
    c0003 ..> c0019 : 2 relationships (see list)
    c0003 ..> c0025 : 2 relationships (see list)
    c0003 ..> c0050 : 6 relationships (see list)
    c0004 ..> c0003 : 2 relationships (see list)
    c0004 ..> c0025 : main() calls create_task()
    c0005 ..> c0000 : 2 relationships (see list)
    c0005 ..> c0003 : 2 relationships (see list)
    c0005 ..> c0005 : 3 relationships (see list)
    c0005 ..> c0012 : 3 relationships (see list)
    c0005 ..> c0016 : read_state() calls read_generated_json()
    c0005 ..> c0019 : request() calls quote()
    c0005 ..> c0050 : 5 relationships (see list)
    c0006 ..> c0000 : close() calls close()
    c0006 ..> c0006 : 5 relationships (see list)
    c0006 ..> c0050 : 4 relationships (see list)
    c0007 ..> c0003 : run_command() calls run()
    c0007 ..> c0050 : run_command() constructs FactoryError
    c0008 ..> c0008 : 3 relationships (see list)
    c0008 ..> c0032 : 3 relationships (see list)
    c0008 ..> c0050 : 2 relationships (see list)
    c0009 ..> c0009 : 2 relationships (see list)
    c0009 ..> c0010 : prepare() calls selected_resources()
    c0009 ..> c0011 : prepare() calls prepare()
    c0009 ..> c0016 : 3 relationships (see list)
    c0009 ..> c0021 : __init__() constructs WorkerProfiles
    c0009 ..> c0030 : 2 relationships (see list)
    c0009 ..> c0050 : 3 relationships (see list)
    c0011 ..> c0008 : selected_launch() calls foreman_launch()
    c0011 ..> c0009 : 4 relationships (see list)
    c0011 ..> c0011 : 22 relationships (see list)
    c0011 ..> c0016 : 11 relationships (see list)
    c0011 ..> c0017 : selected_launch() calls selected_skill_files()
    c0011 ..> c0019 : require_pi_home() calls quote()
    c0011 ..> c0022 : uses_browser_login() calls uses_browser_login()
    c0011 ..> c0023 : 8 relationships (see list)
    c0011 ..> c0024 : list_models() calls role_environment()
    c0011 ..> c0027 : 6 relationships (see list)
    c0011 ..> c0028 : 3 relationships (see list)
    c0011 ..> c0029 : list_models() calls run_owned()
    c0011 ..> c0030 : 4 relationships (see list)
    c0011 ..> c0031 : 9 relationships (see list)
    c0011 ..> c0050 : 14 relationships (see list)
    c0012 ..> c0016 : runtime_directory() calls check_real_path()
    c0012 ..> c0050 : runtime_directory() constructs FactoryError
    c0013 ..> c0007 : origin() calls run_command()
    c0013 ..> c0050 : origin() constructs FactoryError
    c0014 ..> c0007 : 2 relationships (see list)
    c0014 ..> c0014 : 2 relationships (see list)
    c0014 ..> c0015 : _repository_entries() calls _worktree_entries()
    c0014 ..> c0050 : 3 relationships (see list)
    c0016 ..> c0000 : _generated_parent() calls close()
    c0016 ..> c0016 : 9 relationships (see list)
    c0016 ..> c0018 : read_generated_json() calls load()
    c0016 ..> c0050 : 6 relationships (see list)
    c0017 ..> c0050 : selected_skill_files() constructs FactoryError
    c0018 ..> c0000 : 2 relationships (see list)
    c0018 ..> c0019 : save() calls quote()
    c0018 ..> c0030 : 2 relationships (see list)
    c0018 ..> c0032 : load() calls from_mapping()
    c0018 ..> c0036 : load() calls load()
    c0018 ..> c0050 : 2 relationships (see list)
    c0020 ..> c0000 : _hold_directory() calls close()
    c0020 ..> c0020 : hold() calls _hold_directory()
    c0020 ..> c0050 : _hold_directory() constructs FactoryError
    c0021 ..> c0016 : 3 relationships (see list)
    c0021 ..> c0033 : type in prepare
    c0022 ..> c0005 : uses_browser_login() calls request()
    c0022 ..> c0031 : type in uses_browser_login
    c0023 ..> c0023 : 7 relationships (see list)
    c0023 ..> c0024 : 2 relationships (see list)
    c0023 ..> c0029 : 2 relationships (see list)
    c0023 ..> c0031 : 7 relationships (see list)
    c0023 ..> c0050 : 5 relationships (see list)
    c0024 ..> c0028 : role_environment() calls executable_path()
    c0024 ..> c0031 : type in role_environment
    c0025 ..> c0011 : check() calls check()
    c0025 ..> c0023 : 2 relationships (see list)
    c0025 ..> c0025 : 9 relationships (see list)
    c0025 ..> c0031 : type in __init__
    c0025 ..> c0050 : _rows() constructs FactoryError
    c0026 ..> c0007 : _api() calls run_command()
    c0026 ..> c0026 : 5 relationships (see list)
    c0026 ..> c0050 : 7 relationships (see list)
    c0026 ..> c0051 : 2 relationships (see list)
    c0026 ..> c0052 : 3 relationships (see list)
    c0026 ..> c0054 : 8 relationships (see list)
    c0027 ..> c0016 : install() calls write_new()
    c0027 ..> c0027 : 15 relationships (see list)
    c0027 ..> c0028 : 3 relationships (see list)
    c0027 ..> c0029 : 4 relationships (see list)
    c0027 ..> c0050 : 6 relationships (see list)
    c0028 ..> c0028 : runtime_ready() calls sync_fingerprint()
    c0028 ..> c0029 : runtime_ready() calls run_owned()
    c0029 ..> c0050 : run_owned() constructs FactoryError
    c0030 --> c0031 : field forgetful
    c0030 --> c0053 : field repository
    c0031 ..> c0032 : 2 relationships (see list)
    c0031 ..> c0050 : _validate_server() constructs FactoryError
    c0032 ..> c0030 : 3 relationships (see list)
    c0032 ..> c0031 : 3 relationships (see list)
    c0032 ..> c0032 : 5 relationships (see list)
    c0032 ..> c0050 : 4 relationships (see list)
    c0032 ..> c0053 : from_mapping() constructs RepositoryReference
    c0032 ..> c0054 : from_mapping() constructs WorkSource
    c0034 ..> c0032 : 3 relationships (see list)
    c0034 ..> c0033 : 2 relationships (see list)
    c0034 ..> c0034 : 3 relationships (see list)
    c0034 ..> c0050 : 4 relationships (see list)
    c0035 ..> c0003 : initialise() calls save()
    c0035 ..> c0009 : prepare_foreman() calls prepare()
    c0035 ..> c0011 : 5 relationships (see list)
    c0035 ..> c0013 : 3 relationships (see list)
    c0035 ..> c0018 : load_existing() calls load()
    c0035 ..> c0026 : 5 relationships (see list)
    c0035 ..> c0030 : 6 relationships (see list)
    c0035 ..> c0031 : 2 relationships (see list)
    c0035 ..> c0032 : 2 relationships (see list)
    c0035 ..> c0035 : 3 relationships (see list)
    c0035 ..> c0036 : type in __init__
    c0035 ..> c0037 : type in __init__
    c0035 ..> c0039 : type in __init__
    c0035 ..> c0042 : type in __init__
    c0035 ..> c0050 : 5 relationships (see list)
    c0035 ..> c0052 : 2 relationships (see list)
    c0035 ..> c0053 : 2 relationships (see list)
    c0035 ..> c0054 : 2 relationships (see list)
    c0035 ..> c0055 : type in __init__
    c0036 ..> c0030 : 2 relationships (see list)
    c0037 ..> c0030 : 3 relationships (see list)
    c0037 ..> c0031 : 8 relationships (see list)
    c0037 ..> c0033 : type in prepare_roles
    c0042 ..> c0054 : type in source_from_remote
    c0044 ..> c0011 : check() calls check()
    c0044 ..> c0014 : 2 relationships (see list)
    c0044 ..> c0025 : 8 relationships (see list)
    c0044 ..> c0030 : type in __init__
    c0044 ..> c0040 : type in __init__
    c0044 ..> c0043 : type in __init__
    c0044 ..> c0044 : 7 relationships (see list)
    c0044 ..> c0045 : _ensure_mapping() calls _cleanup_state()
    c0044 ..> c0050 : 7 relationships (see list)
    c0044 ..> c0051 : 4 relationships (see list)
    c0044 ..> c0054 : unfinished() constructs WorkSource
    c0045 ..> c0050 : _cleanup_state() constructs FactoryError
    c0046 ..> c0000 : 5 relationships (see list)
    c0046 ..> c0009 : _notify_issues() calls prepare()
    c0046 ..> c0011 : run() calls check()
    c0046 ..> c0026 : _read_issues() calls list_issues()
    c0046 ..> c0030 : 2 relationships (see list)
    c0046 ..> c0038 : type in __init__
    c0046 ..> c0044 : 2 relationships (see list)
    c0046 ..> c0046 : 3 relationships (see list)
    c0046 ..> c0051 : 2 relationships (see list)
    c0046 ..> c0054 : 2 relationships (see list)
    c0046 ..> c0055 : type in __init__
    c0047 ..> c0006 : build_watcher() constructs AgentShellTerminal
    c0047 ..> c0011 : 5 relationships (see list)
    c0047 ..> c0013 : build_initialiser() constructs GitRepositories
    c0047 ..> c0014 : build_watcher() constructs GitWorktrees
    c0047 ..> c0018 : build_initialiser() constructs TomlConfigurationStore
    c0047 ..> c0024 : prepare_foreman_launch() calls role_environment()
    c0047 ..> c0025 : build_watcher() constructs ForgetfulPlanning
    c0047 ..> c0026 : 3 relationships (see list)
    c0047 ..> c0030 : 2 relationships (see list)
    c0047 ..> c0035 : 2 relationships (see list)
    c0047 ..> c0044 : build_watcher() constructs ScaffoldIssue
    c0047 ..> c0046 : 2 relationships (see list)
    c0047 ..> c0047 : build_watcher() calls prepare_foreman_launch()
    c0047 ..> c0050 : 2 relationships (see list)
    c0048 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0048 ..> c0003 : _watch_locked() calls run()
    c0048 ..> c0005 : 12 relationships (see list)
    c0048 ..> c0011 : 12 relationships (see list)
    c0048 ..> c0013 : select_repositories() calls discover()
    c0048 ..> c0018 : _initialise_locked() calls load()
    c0048 ..> c0019 : 6 relationships (see list)
    c0048 ..> c0020 : 6 relationships (see list)
    c0048 ..> c0030 : 2 relationships (see list)
    c0048 ..> c0031 : 6 relationships (see list)
    c0048 ..> c0033 : 4 relationships (see list)
    c0048 ..> c0034 : _initialise_locked() calls validate_initial_agents()
    c0048 ..> c0035 : 11 relationships (see list)
    c0048 ..> c0047 : 4 relationships (see list)
    c0048 ..> c0048 : 34 relationships (see list)
    c0048 ..> c0049 : 3 relationships (see list)
    c0048 ..> c0050 : 17 relationships (see list)
    c0049 ..> c0018 : 2 relationships (see list)
    c0049 ..> c0030 : type in load_configuration
    c0049 ..> c0050 : load_configuration() constructs FactoryError
    c0051 --> c0054 : field source
    c0053 --> c0054 : field work_source
    c0055 ..> c0051 : type in list_issues
    c0055 ..> c0052 : 2 relationships (see list)
    c0055 ..> c0054 : 4 relationships (see list)
```

## Source index

- c0000: `BorrowedForemanTerminal` —
  `src/forgetful_factory/adapters/agentshell/borrowed_terminal.py`:9
- c0001: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0002: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0003: `ForemanOwner` — `src/forgetful_factory/adapters/agentshell/owner.py`:22
- c0004: `src/forgetful_factory/adapters/agentshell/owner.py` —
  `src/forgetful_factory/adapters/agentshell/owner.py`:1
- c0005: `src/forgetful_factory/adapters/agentshell/owner_client.py` —
  `src/forgetful_factory/adapters/agentshell/owner_client.py`:1
- c0006: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:12
- c0007: `src/forgetful_factory/adapters/command.py` — `src/forgetful_factory/adapters/command.py`:1
- c0008: `src/forgetful_factory/adapters/filesystem/agent_definitions.py` —
  `src/forgetful_factory/adapters/filesystem/agent_definitions.py`:1
- c0009: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:26
- c0010: `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:1
- c0011: `ForemanProfile` — `src/forgetful_factory/adapters/filesystem/foreman_profile.py`:48
- c0012: `src/forgetful_factory/adapters/filesystem/foreman_runtime.py` —
  `src/forgetful_factory/adapters/filesystem/foreman_runtime.py`:1
- c0013: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:7
- c0014: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:21
- c0015: `src/forgetful_factory/adapters/filesystem/git_worktrees.py` —
  `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:1
- c0016: `src/forgetful_factory/adapters/filesystem/resource_files.py` —
  `src/forgetful_factory/adapters/filesystem/resource_files.py`:1
- c0017: `src/forgetful_factory/adapters/filesystem/selected_skills.py` —
  `src/forgetful_factory/adapters/filesystem/selected_skills.py`:1
- c0018: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:20
- c0019: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0020: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0021: `WorkerProfiles` — `src/forgetful_factory/adapters/filesystem/worker_profiles.py`:15
- c0022: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0023: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:52
- c0024: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0025: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:8
- c0026: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0027: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:52
- c0028: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0029: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0030: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:82
- c0031: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0032: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0033: `InitialAgentChoices` — `src/forgetful_factory/application/initial_agent_choices.py`:9
- c0034: `src/forgetful_factory/application/initial_agent_choices.py` —
  `src/forgetful_factory/application/initial_agent_choices.py`:1
- c0035: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0036: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0037: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:8
- c0038: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0039: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0040: `Planning` — `src/forgetful_factory/application/ports/planning.py`:4
- c0041: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0042: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0043: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:4
- c0044: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:31
- c0045: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0046: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:12
- c0047: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0048: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0049: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0050: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0051: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0052: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0053: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0054: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0055: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0006: `close() calls close()`
- c0000 ..> c0050: `_request() constructs FactoryError`
- c0000 ..> c0050: `wait() constructs FactoryError`
- c0001 ..> c0000: `control() calls close()`
- c0001 ..> c0000: `control() calls wait()`
- c0001 ..> c0000: `pin_worker() calls close()`
- c0001 ..> c0000: `resume_exit_observation() calls wait()`
- c0001 ..> c0000: `serve() calls close()`
- c0001 ..> c0000: `serve() calls wait()`
- c0001 ..> c0001: `control() calls serve()`
- c0001 ..> c0001: `interact() calls ready()`
- c0001 ..> c0001: `main() calls control()`
- c0001 ..> c0001: `serve() calls interact()`
- c0001 ..> c0001: `serve() calls pin_worker()`
- c0001 ..> c0001: `serve() calls resume_exit_observation()`
- c0001 ..> c0001: `serve() calls retain_identity()`
- c0001 ..> c0001: `serve() calls runtime()`
- c0001 ..> c0001: `serve() calls worker_exited()`
- c0001 ..> c0025: `control() calls create_task()`
- c0001 ..> c0025: `main() calls create_task()`
- c0001 ..> c0025: `serve() calls create_task()`
- c0002 ..> c0011: `main() calls list_models()`
- c0003 ..> c0000: `control() calls close()`
- c0003 ..> c0000: `reap_watcher() calls wait()`
- c0003 ..> c0000: `relay() calls close()`
- c0003 ..> c0000: `run() calls close()`
- c0003 ..> c0000: `run() calls wait()`
- c0003 ..> c0000: `start_watcher() calls close()`
- c0003 ..> c0003: `control() calls start_watcher()`
- c0003 ..> c0003: `control() calls stop_watcher()`
- c0003 ..> c0003: `observe() calls save()`
- c0003 ..> c0003: `observe() calls stop_watcher()`
- c0003 ..> c0003: `run() calls observe()`
- c0003 ..> c0003: `run() calls save()`
- c0003 ..> c0003: `run() calls stop_watcher()`
- c0003 ..> c0003: `start_watcher() calls reap_watcher()`
- c0003 ..> c0003: `start_watcher() calls relay()`
- c0003 ..> c0003: `start_watcher() calls stop_watcher()`
- c0003 ..> c0005: `run() calls read_state()`
- c0003 ..> c0012: `__init__() calls runtime_directory()`
- c0003 ..> c0016: `save() calls replace_generated_json()`
- c0003 ..> c0019: `observe() calls quote()`
- c0003 ..> c0019: `run() calls quote()`
- c0003 ..> c0025: `run() calls create_task()`
- c0003 ..> c0025: `start_watcher() calls create_task()`
- c0003 ..> c0050: `control() constructs FactoryError`
- c0003 ..> c0050: `observe() constructs FactoryError`
- c0003 ..> c0050: `reap_watcher() constructs FactoryError`
- c0003 ..> c0050: `relay() constructs FactoryError`
- c0003 ..> c0050: `run() constructs FactoryError`
- c0003 ..> c0050: `start_watcher() constructs FactoryError`
- c0004 ..> c0003: `main() calls run()`
- c0004 ..> c0003: `main() constructs ForemanOwner`
- c0004 ..> c0025: `main() calls create_task()`
- c0005 ..> c0000: `start_owner() calls close()`
- c0005 ..> c0000: `start_owner() calls wait()`
- c0005 ..> c0003: `enter_terminal() calls run()`
- c0005 ..> c0003: `start_owner() calls run()`
- c0005 ..> c0005: `request() calls _reply()`
- c0005 ..> c0005: `request() calls read_state()`
- c0005 ..> c0005: `start_owner() calls _reply()`
- c0005 ..> c0012: `read_state() calls runtime_directory()`
- c0005 ..> c0012: `request() calls runtime_directory()`
- c0005 ..> c0012: `start_owner() calls runtime_directory()`
- c0005 ..> c0016: `read_state() calls read_generated_json()`
- c0005 ..> c0019: `request() calls quote()`
- c0005 ..> c0050: `_reply() constructs FactoryError`
- c0005 ..> c0050: `enter_terminal() constructs FactoryError`
- c0005 ..> c0050: `read_state() constructs FactoryError`
- c0005 ..> c0050: `request() constructs FactoryError`
- c0005 ..> c0050: `start_owner() constructs FactoryError`
- c0006 ..> c0000: `close() calls close()`
- c0006 ..> c0006: `send() calls _read()`
- c0006 ..> c0006: `send() calls _write()`
- c0006 ..> c0006: `start() calls _read()`
- c0006 ..> c0006: `start() calls _write()`
- c0006 ..> c0006: `wait() calls _read()`
- c0006 ..> c0050: `_read() constructs FactoryError`
- c0006 ..> c0050: `_write() constructs FactoryError`
- c0006 ..> c0050: `close() constructs FactoryError`
- c0006 ..> c0050: `start() constructs FactoryError`
- c0007 ..> c0003: `run_command() calls run()`
- c0007 ..> c0050: `run_command() constructs FactoryError`
- c0008 ..> c0008: `foreman_launch() calls read_definition()`
- c0008 ..> c0008: `foreman_launch() calls relative_path()`
- c0008 ..> c0008: `read_definition() calls relative_path()`
- c0008 ..> c0032: `foreman_launch() calls nonblank()`
- c0008 ..> c0032: `read_definition() calls nonblank()`
- c0008 ..> c0032: `relative_path() calls nonblank()`
- c0008 ..> c0050: `foreman_launch() constructs FactoryError`
- c0008 ..> c0050: `read_definition() constructs FactoryError`
- c0009 ..> c0009: `prepare() calls _write_agent()`
- c0009 ..> c0009: `prepare() calls validate_guidance()`
- c0009 ..> c0010: `prepare() calls selected_resources()`
- c0009 ..> c0011: `prepare() calls prepare()`
- c0009 ..> c0016: `_write_agent() calls write_definition()`
- c0009 ..> c0016: `prepare() calls check_skill_file()`
- c0009 ..> c0016: `prepare() calls write_new()`
- c0009 ..> c0021: `__init__() constructs WorkerProfiles`
- c0009 ..> c0030: `type in prepare`
- c0009 ..> c0030: `type in validate_guidance`
- c0009 ..> c0050: `prepare() constructs FactoryError`
- c0009 ..> c0050: `validate_depth() constructs FactoryError`
- c0009 ..> c0050: `validate_guidance() constructs FactoryError`
- c0011 ..> c0008: `selected_launch() calls foreman_launch()`
- c0011 ..> c0009: `prepare_roles() calls validate_depth()`
- c0011 ..> c0009: `prepare_roles() constructs CoordinatorProfiles`
- c0011 ..> c0009: `validate_setup() calls validate_depth()`
- c0011 ..> c0009: `validate_setup() constructs CoordinatorProfiles`
- c0011 ..> c0011: `choose_pi_home() calls pi_home()`
- c0011 ..> c0011: `choose_pi_home() calls require_pi_home()`
- c0011 ..> c0011: `list_models() calls pi_home()`
- c0011 ..> c0011: `list_models() calls require_pi_home()`
- c0011 ..> c0011: `missing_executables() calls pi_home()`
- c0011 ..> c0011: `prepare() calls _install_resources()`
- c0011 ..> c0011: `prepare() calls _protect_runtime()`
- c0011 ..> c0011: `prepare() calls save_pi_choice()`
- c0011 ..> c0011: `prepare() calls validate_guidance()`
- c0011 ..> c0011: `prepare_roles() calls list_models()`
- c0011 ..> c0011: `prepare_roles() calls pi_home()`
- c0011 ..> c0011: `prepare_roles() calls prepare()`
- c0011 ..> c0011: `prepare_roles() calls validate_worker_models()`
- c0011 ..> c0011: `record_completion() calls selected_launch()`
- c0011 ..> c0011: `selected_launch() calls validate_setup()`
- c0011 ..> c0011: `validate_guidance() calls _read_guidance()`
- c0011 ..> c0011: `validate_setup() calls missing_executables()`
- c0011 ..> c0011: `validate_setup() calls pi_home()`
- c0011 ..> c0011: `validate_setup() calls require_pi_home()`
- c0011 ..> c0011: `validate_setup() calls validate_bundled_resources()`
- c0011 ..> c0011: `validate_setup() calls validate_guidance()`
- c0011 ..> c0011: `validate_worker_models() calls list_models()`
- c0011 ..> c0016: `_install_resources() calls write_new()`
- c0011 ..> c0016: `_protect_runtime() calls write_new()`
- c0011 ..> c0016: `begin_setup() calls remove_generated()`
- c0011 ..> c0016: `pi_home() calls read_generated_json()`
- c0011 ..> c0016: `prepare() calls write_new()`
- c0011 ..> c0016: `prepare_roles() calls check_real_path()`
- c0011 ..> c0016: `prepare_setup_guidance() calls write_new()`
- c0011 ..> c0016: `record_completion() calls replace_generated_json()`
- c0011 ..> c0016: `save_pi_choice() calls write_json()`
- c0011 ..> c0016: `validate_bundled_resources() calls check_real_path()`
- c0011 ..> c0016: `validate_completion() calls read_generated_json()`
- c0011 ..> c0017: `selected_launch() calls selected_skill_files()`
- c0011 ..> c0019: `require_pi_home() calls quote()`
- c0011 ..> c0022: `uses_browser_login() calls uses_browser_login()`
- c0011 ..> c0023: `check() calls check()`
- c0011 ..> c0023: `check() constructs AgentForgetfulConnection`
- c0011 ..> c0023: `create_project() calls create_project()`
- c0011 ..> c0023: `create_project() constructs AgentForgetfulConnection`
- c0011 ..> c0023: `login() calls login()`
- c0011 ..> c0023: `login() constructs AgentForgetfulConnection`
- c0011 ..> c0023: `projects() calls projects()`
- c0011 ..> c0023: `projects() constructs AgentForgetfulConnection`
- c0011 ..> c0024: `list_models() calls role_environment()`
- c0011 ..> c0027: `install() calls install()`
- c0011 ..> c0027: `install() constructs HostDependencies`
- c0011 ..> c0027: `installation() calls description()`
- c0011 ..> c0027: `installation() constructs HostDependencies`
- c0011 ..> c0027: `missing_executables() calls pi_ready()`
- c0011 ..> c0027: `missing_executables() constructs HostDependencies`
- c0011 ..> c0028: `missing_executables() calls executable_path()`
- c0011 ..> c0028: `missing_executables() calls runtime_ready()`
- c0011 ..> c0028: `require_pi_home() calls executable_path()`
- c0011 ..> c0029: `list_models() calls run_owned()`
- c0011 ..> c0030: `type in record_completion`
- c0011 ..> c0030: `type in selected_launch`
- c0011 ..> c0030: `type in validate_completion`
- c0011 ..> c0030: `type in validate_worker_models`
- c0011 ..> c0031: `type in check`
- c0011 ..> c0031: `type in create_project`
- c0011 ..> c0031: `type in list_models`
- c0011 ..> c0031: `type in login`
- c0011 ..> c0031: `type in missing_executables`
- c0011 ..> c0031: `type in prepare`
- c0011 ..> c0031: `type in projects`
- c0011 ..> c0031: `type in uses_browser_login`
- c0011 ..> c0031: `type in validate_setup`
- c0011 ..> c0050: `_install_resources() constructs FactoryError`
- c0011 ..> c0050: `_read_guidance() constructs FactoryError`
- c0011 ..> c0050: `choose_pi_home() constructs FactoryError`
- c0011 ..> c0050: `list_models() constructs FactoryError`
- c0011 ..> c0050: `pi_home() constructs FactoryError`
- c0011 ..> c0050: `prepare_roles() constructs FactoryError`
- c0011 ..> c0050: `prepare_setup_guidance() constructs FactoryError`
- c0011 ..> c0050: `require_pi_home() constructs FactoryError`
- c0011 ..> c0050: `selected_launch() constructs FactoryError`
- c0011 ..> c0050: `validate_bundled_resources() constructs FactoryError`
- c0011 ..> c0050: `validate_completion() constructs FactoryError`
- c0011 ..> c0050: `validate_guidance() constructs FactoryError`
- c0011 ..> c0050: `validate_setup() constructs FactoryError`
- c0011 ..> c0050: `validate_worker_models() constructs FactoryError`
- c0012 ..> c0016: `runtime_directory() calls check_real_path()`
- c0012 ..> c0050: `runtime_directory() constructs FactoryError`
- c0013 ..> c0007: `origin() calls run_command()`
- c0013 ..> c0050: `origin() constructs FactoryError`
- c0014 ..> c0007: `_repository_entries() calls run_command()`
- c0014 ..> c0007: `ensure() calls run_command()`
- c0014 ..> c0014: `ensure() calls _repository_entries()`
- c0014 ..> c0014: `verify_removed() calls _repository_entries()`
- c0014 ..> c0015: `_repository_entries() calls _worktree_entries()`
- c0014 ..> c0050: `_repository_entries() constructs FactoryError`
- c0014 ..> c0050: `ensure() constructs FactoryError`
- c0014 ..> c0050: `verify_removed() constructs FactoryError`
- c0016 ..> c0000: `_generated_parent() calls close()`
- c0016 ..> c0016: `_generated_parent() calls check_real_path()`
- c0016 ..> c0016: `check_skill_file() calls check_real_path()`
- c0016 ..> c0016: `read_generated_json() calls _generated_parent()`
- c0016 ..> c0016: `remove_generated() calls _generated_parent()`
- c0016 ..> c0016: `replace_generated_json() calls _generated_parent()`
- c0016 ..> c0016: `write_definition() calls read_generated_json()`
- c0016 ..> c0016: `write_definition() calls write_json()`
- c0016 ..> c0016: `write_json() calls write_new()`
- c0016 ..> c0016: `write_new() calls check_real_path()`
- c0016 ..> c0018: `read_generated_json() calls load()`
- c0016 ..> c0050: `_generated_parent() constructs FactoryError`
- c0016 ..> c0050: `check_real_path() constructs FactoryError`
- c0016 ..> c0050: `check_skill_file() constructs FactoryError`
- c0016 ..> c0050: `read_generated_json() constructs FactoryError`
- c0016 ..> c0050: `write_definition() constructs FactoryError`
- c0016 ..> c0050: `write_new() constructs FactoryError`
- c0017 ..> c0050: `selected_skill_files() constructs FactoryError`
- c0018 ..> c0000: `load() calls close()`
- c0018 ..> c0000: `save() calls close()`
- c0018 ..> c0019: `save() calls quote()`
- c0018 ..> c0030: `type in load`
- c0018 ..> c0030: `type in save`
- c0018 ..> c0032: `load() calls from_mapping()`
- c0018 ..> c0036: `load() calls load()`
- c0018 ..> c0050: `load() constructs FactoryError`
- c0018 ..> c0050: `save() constructs FactoryError`
- c0020 ..> c0000: `_hold_directory() calls close()`
- c0020 ..> c0020: `hold() calls _hold_directory()`
- c0020 ..> c0050: `_hold_directory() constructs FactoryError`
- c0021 ..> c0016: `prepare() calls check_skill_file()`
- c0021 ..> c0016: `prepare() calls write_definition()`
- c0021 ..> c0016: `prepare() calls write_new()`
- c0021 ..> c0033: `type in prepare`
- c0022 ..> c0005: `uses_browser_login() calls request()`
- c0022 ..> c0031: `type in uses_browser_login`
- c0023 ..> c0023: `call() calls command()`
- c0023 ..> c0023: `check() calls call()`
- c0023 ..> c0023: `check() calls command()`
- c0023 ..> c0023: `command() calls _environment()`
- c0023 ..> c0023: `create_project() calls call()`
- c0023 ..> c0023: `login() calls _environment()`
- c0023 ..> c0023: `projects() calls command()`
- c0023 ..> c0024: `_environment() calls role_environment()`
- c0023 ..> c0024: `check() calls _catalog_tools()`
- c0023 ..> c0029: `command() calls run_owned()`
- c0023 ..> c0029: `login() calls run_owned()`
- c0023 ..> c0031: `type in _environment`
- c0023 ..> c0031: `type in call`
- c0023 ..> c0031: `type in check`
- c0023 ..> c0031: `type in command`
- c0023 ..> c0031: `type in create_project`
- c0023 ..> c0031: `type in login`
- c0023 ..> c0031: `type in projects`
- c0023 ..> c0050: `check() constructs FactoryError`
- c0023 ..> c0050: `command() constructs FactoryError`
- c0023 ..> c0050: `create_project() constructs FactoryError`
- c0023 ..> c0050: `login() constructs FactoryError`
- c0023 ..> c0050: `projects() constructs FactoryError`
- c0024 ..> c0028: `role_environment() calls executable_path()`
- c0024 ..> c0031: `type in role_environment`
- c0025 ..> c0011: `check() calls check()`
- c0025 ..> c0023: `__init__() constructs AgentForgetfulConnection`
- c0025 ..> c0023: `_call() calls call()`
- c0025 ..> c0025: `create_plan() calls _call()`
- c0025 ..> c0025: `create_task() calls _call()`
- c0025 ..> c0025: `get_plan() calls _call()`
- c0025 ..> c0025: `plans() calls _call()`
- c0025 ..> c0025: `plans() calls _rows()`
- c0025 ..> c0025: `tasks() calls _call()`
- c0025 ..> c0025: `tasks() calls _rows()`
- c0025 ..> c0025: `update_plan() calls _call()`
- c0025 ..> c0025: `update_task() calls _call()`
- c0025 ..> c0031: `type in __init__`
- c0025 ..> c0050: `_rows() constructs FactoryError`
- c0026 ..> c0007: `_api() calls run_command()`
- c0026 ..> c0026: `check_access() calls _api()`
- c0026 ..> c0026: `create_label() calls _api()`
- c0026 ..> c0026: `list_issues() calls _api()`
- c0026 ..> c0026: `list_issues() calls _validate_issue()`
- c0026 ..> c0026: `list_labels() calls _api()`
- c0026 ..> c0050: `_api() constructs FactoryError`
- c0026 ..> c0050: `_validate_issue() constructs FactoryError`
- c0026 ..> c0050: `check_access() constructs FactoryError`
- c0026 ..> c0050: `create_label() constructs FactoryError`
- c0026 ..> c0050: `list_issues() constructs FactoryError`
- c0026 ..> c0050: `list_labels() constructs FactoryError`
- c0026 ..> c0050: `source_from_remote() constructs FactoryError`
- c0026 ..> c0051: `list_issues() constructs Issue`
- c0026 ..> c0051: `type in list_issues`
- c0026 ..> c0052: `list_labels() constructs Label`
- c0026 ..> c0052: `type in create_label`
- c0026 ..> c0052: `type in list_labels`
- c0026 ..> c0054: `source_from_remote() constructs WorkSource`
- c0026 ..> c0054: `type in _api`
- c0026 ..> c0054: `type in _validate_issue`
- c0026 ..> c0054: `type in check_access`
- c0026 ..> c0054: `type in create_label`
- c0026 ..> c0054: `type in list_issues`
- c0026 ..> c0054: `type in list_labels`
- c0026 ..> c0054: `type in source_from_remote`
- c0027 ..> c0016: `install() calls write_new()`
- c0027 ..> c0027: `_check_uv() calls _environment()`
- c0027 ..> c0027: `_forgetful_python() calls _check_uv()`
- c0027 ..> c0027: `_forgetful_python() calls _environment()`
- c0027 ..> c0027: `_install_role_runtime() calls _check_uv()`
- c0027 ..> c0027: `_install_role_runtime() calls _run()`
- c0027 ..> c0027: `_install_tmux() calls _run()`
- c0027 ..> c0027: `_run() calls _environment()`
- c0027 ..> c0027: `description() calls _forgetful_python()`
- c0027 ..> c0027: `description() calls _ubuntu_tmux()`
- c0027 ..> c0027: `install() calls _forgetful_python()`
- c0027 ..> c0027: `install() calls _install_role_runtime()`
- c0027 ..> c0027: `install() calls _install_tmux()`
- c0027 ..> c0027: `install() calls _run()`
- c0027 ..> c0027: `install() calls _ubuntu_tmux()`
- c0027 ..> c0027: `pi_ready() calls _environment()`
- c0027 ..> c0028: `_install_role_runtime() calls sync_fingerprint()`
- c0027 ..> c0028: `install() calls sync_fingerprint()`
- c0027 ..> c0028: `pi_ready() calls sync_fingerprint()`
- c0027 ..> c0029: `_check_uv() calls run_owned()`
- c0027 ..> c0029: `_forgetful_python() calls run_owned()`
- c0027 ..> c0029: `_run() calls run_owned()`
- c0027 ..> c0029: `pi_ready() calls run_owned()`
- c0027 ..> c0050: `_check_uv() constructs FactoryError`
- c0027 ..> c0050: `_forgetful_python() constructs FactoryError`
- c0027 ..> c0050: `_install_role_runtime() constructs FactoryError`
- c0027 ..> c0050: `_install_tmux() constructs FactoryError`
- c0027 ..> c0050: `_run() constructs FactoryError`
- c0027 ..> c0050: `install() constructs FactoryError`
- c0028 ..> c0028: `runtime_ready() calls sync_fingerprint()`
- c0028 ..> c0029: `runtime_ready() calls run_owned()`
- c0029 ..> c0050: `run_owned() constructs FactoryError`
- c0030 --> c0031: `field forgetful`
- c0030 --> c0053: `field repository`
- c0031 ..> c0032: `_validate_server() calls loopback_host()`
- c0031 ..> c0032: `_validate_server() calls nonblank()`
- c0031 ..> c0050: `_validate_server() constructs FactoryError`
- c0032 ..> c0030: `from_mapping() constructs FactoryConfiguration`
- c0032 ..> c0030: `type in from_mapping`
- c0032 ..> c0030: `type in validate`
- c0032 ..> c0031: `connection_from_mapping() constructs ForgetfulConnection`
- c0032 ..> c0031: `type in connection_from_mapping`
- c0032 ..> c0031: `validate() calls _validate_server()`
- c0032 ..> c0032: `connection_from_mapping() calls validate()`
- c0032 ..> c0032: `from_mapping() calls connection_from_mapping()`
- c0032 ..> c0032: `from_mapping() calls validate()`
- c0032 ..> c0032: `unique_labels() calls nonblank()`
- c0032 ..> c0032: `validate() calls nonblank()`
- c0032 ..> c0050: `connection_from_mapping() constructs FactoryError`
- c0032 ..> c0050: `from_mapping() constructs FactoryError`
- c0032 ..> c0050: `nonblank() constructs FactoryError`
- c0032 ..> c0050: `validate() constructs FactoryError`
- c0032 ..> c0053: `from_mapping() constructs RepositoryReference`
- c0032 ..> c0054: `from_mapping() constructs WorkSource`
- c0034 ..> c0032: `skill_paths() calls nonblank()`
- c0034 ..> c0032: `validate_initial_agents() calls nonblank()`
- c0034 ..> c0032: `validate_workers() calls nonblank()`
- c0034 ..> c0033: `type in validate_initial_agents`
- c0034 ..> c0033: `type in validate_workers`
- c0034 ..> c0034: `validate_initial_agents() calls validate_role_app()`
- c0034 ..> c0034: `validate_initial_agents() calls validate_workers()`
- c0034 ..> c0034: `validate_workers() calls validate_role_app()`
- c0034 ..> c0050: `skill_paths() constructs FactoryError`
- c0034 ..> c0050: `validate_initial_agents() constructs FactoryError`
- c0034 ..> c0050: `validate_role_app() constructs FactoryError`
- c0034 ..> c0050: `validate_workers() constructs FactoryError`
- c0035 ..> c0003: `initialise() calls save()`
- c0035 ..> c0009: `prepare_foreman() calls prepare()`
- c0035 ..> c0011: `check_foreman() calls check()`
- c0035 ..> c0011: `check_foreman() calls login()`
- c0035 ..> c0011: `prepare_foreman() calls install()`
- c0035 ..> c0011: `prepare_foreman() calls installation()`
- c0035 ..> c0011: `prepare_foreman() calls missing_executables()`
- c0035 ..> c0013: `_preflight() calls origin()`
- c0035 ..> c0013: `discover() calls discover()`
- c0035 ..> c0013: `inspect() calls origin()`
- c0035 ..> c0018: `load_existing() calls load()`
- c0035 ..> c0026: `_ensure_label() calls create_label()`
- c0035 ..> c0026: `_preflight() calls check_access()`
- c0035 ..> c0026: `_preflight() calls list_labels()`
- c0035 ..> c0026: `_preflight() calls source_from_remote()`
- c0035 ..> c0026: `inspect() calls source_from_remote()`
- c0035 ..> c0030: `configure() constructs FactoryConfiguration`
- c0035 ..> c0030: `type in _preflight`
- c0035 ..> c0030: `type in check_foreman`
- c0035 ..> c0030: `type in configure`
- c0035 ..> c0030: `type in initialise`
- c0035 ..> c0030: `type in load_existing`
- c0035 ..> c0031: `_preflight() calls validate()`
- c0035 ..> c0031: `type in prepare_foreman`
- c0035 ..> c0032: `configure() calls unique_labels()`
- c0035 ..> c0032: `load_existing() calls unique_labels()`
- c0035 ..> c0035: `configure() calls inspect()`
- c0035 ..> c0035: `initialise() calls _ensure_label()`
- c0035 ..> c0035: `initialise() calls _preflight()`
- c0035 ..> c0036: `type in __init__`
- c0035 ..> c0037: `type in __init__`
- c0035 ..> c0039: `type in __init__`
- c0035 ..> c0042: `type in __init__`
- c0035 ..> c0050: `_preflight() constructs FactoryError`
- c0035 ..> c0050: `initialise() constructs FactoryError`
- c0035 ..> c0050: `inspect() constructs FactoryError`
- c0035 ..> c0050: `load_existing() constructs FactoryError`
- c0035 ..> c0050: `prepare_foreman() constructs FactoryError`
- c0035 ..> c0052: `_ensure_label() constructs Label`
- c0035 ..> c0052: `type in _preflight`
- c0035 ..> c0053: `inspect() constructs RepositoryReference`
- c0035 ..> c0053: `type in inspect`
- c0035 ..> c0054: `type in _ensure_label`
- c0035 ..> c0054: `type in _preflight`
- c0035 ..> c0055: `type in __init__`
- c0036 ..> c0030: `type in load`
- c0036 ..> c0030: `type in save`
- c0037 ..> c0030: `type in prepare_roles`
- c0037 ..> c0030: `type in record_completion`
- c0037 ..> c0030: `type in selected_launch`
- c0037 ..> c0031: `type in check`
- c0037 ..> c0031: `type in create_project`
- c0037 ..> c0031: `type in list_models`
- c0037 ..> c0031: `type in login`
- c0037 ..> c0031: `type in missing_executables`
- c0037 ..> c0031: `type in prepare`
- c0037 ..> c0031: `type in projects`
- c0037 ..> c0031: `type in uses_browser_login`
- c0037 ..> c0033: `type in prepare_roles`
- c0042 ..> c0054: `type in source_from_remote`
- c0044 ..> c0011: `check() calls check()`
- c0044 ..> c0014: `_ensure_mapping() calls ensure()`
- c0044 ..> c0014: `_ensure_mapping() calls verify_removed()`
- c0044 ..> c0025: `_issue_plan() calls create_plan()`
- c0044 ..> c0025: `_issue_plan() calls get_plan()`
- c0044 ..> c0025: `_issue_plan() calls plans()`
- c0044 ..> c0025: `_ownership() calls tasks()`
- c0044 ..> c0025: `prepare() calls create_task()`
- c0044 ..> c0025: `prepare() calls update_plan()`
- c0044 ..> c0025: `unfinished() calls get_plan()`
- c0044 ..> c0025: `unfinished() calls plans()`
- c0044 ..> c0030: `type in __init__`
- c0044 ..> c0040: `type in __init__`
- c0044 ..> c0043: `type in __init__`
- c0044 ..> c0044: `_ensure_worktrees() calls _ensure_mapping()`
- c0044 ..> c0044: `prepare() calls _context()`
- c0044 ..> c0044: `prepare() calls _ensure_worktrees()`
- c0044 ..> c0044: `prepare() calls _issue_plan()`
- c0044 ..> c0044: `prepare() calls _ownership()`
- c0044 ..> c0044: `unfinished() calls _context()`
- c0044 ..> c0044: `unfinished() calls _is_unfinished_factory_plan()`
- c0044 ..> c0045: `_ensure_mapping() calls _cleanup_state()`
- c0044 ..> c0050: `_context() constructs FactoryError`
- c0044 ..> c0050: `_ensure_mapping() constructs FactoryError`
- c0044 ..> c0050: `_ensure_worktrees() constructs FactoryError`
- c0044 ..> c0050: `_issue_plan() constructs FactoryError`
- c0044 ..> c0050: `_ownership() constructs FactoryError`
- c0044 ..> c0050: `prepare() constructs FactoryError`
- c0044 ..> c0050: `unfinished() constructs FactoryError`
- c0044 ..> c0051: `type in _issue_plan`
- c0044 ..> c0051: `type in prepare`
- c0044 ..> c0051: `type in unfinished`
- c0044 ..> c0051: `unfinished() constructs Issue`
- c0044 ..> c0054: `unfinished() constructs WorkSource`
- c0045 ..> c0050: `_cleanup_state() constructs FactoryError`
- c0046 ..> c0000: `_notify_issues() calls send()`
- c0046 ..> c0000: `_watch() calls close()`
- c0046 ..> c0000: `_watch() calls start()`
- c0046 ..> c0000: `_watch() calls wait()`
- c0046 ..> c0000: `run() calls startup_hint()`
- c0046 ..> c0009: `_notify_issues() calls prepare()`
- c0046 ..> c0011: `run() calls check()`
- c0046 ..> c0026: `_read_issues() calls list_issues()`
- c0046 ..> c0030: `type in _watch`
- c0046 ..> c0030: `type in run`
- c0046 ..> c0038: `type in __init__`
- c0046 ..> c0044: `_watch() calls unfinished()`
- c0046 ..> c0044: `type in __init__`
- c0046 ..> c0046: `_watch() calls _notify_issues()`
- c0046 ..> c0046: `_watch() calls _read_issues()`
- c0046 ..> c0046: `run() calls _watch()`
- c0046 ..> c0051: `type in _notify_issues`
- c0046 ..> c0051: `type in _read_issues`
- c0046 ..> c0054: `_watch() constructs WorkSource`
- c0046 ..> c0054: `type in _read_issues`
- c0046 ..> c0055: `type in __init__`
- c0047 ..> c0006: `build_watcher() constructs AgentShellTerminal`
- c0047 ..> c0011: `build_initialiser() constructs ForemanProfile`
- c0047 ..> c0011: `prepare_foreman_launch() calls pi_home()`
- c0047 ..> c0011: `prepare_foreman_launch() calls selected_launch()`
- c0047 ..> c0011: `prepare_foreman_launch() calls validate_completion()`
- c0047 ..> c0011: `prepare_foreman_launch() constructs ForemanProfile`
- c0047 ..> c0013: `build_initialiser() constructs GitRepositories`
- c0047 ..> c0014: `build_watcher() constructs GitWorktrees`
- c0047 ..> c0018: `build_initialiser() constructs TomlConfigurationStore`
- c0047 ..> c0024: `prepare_foreman_launch() calls role_environment()`
- c0047 ..> c0025: `build_watcher() constructs ForgetfulPlanning`
- c0047 ..> c0026: `build_initialiser() constructs GitHubWorkTracking`
- c0047 ..> c0026: `build_watcher() calls source_from_remote()`
- c0047 ..> c0026: `build_watcher() constructs GitHubWorkTracking`
- c0047 ..> c0030: `type in build_watcher`
- c0047 ..> c0030: `type in prepare_foreman_launch`
- c0047 ..> c0035: `build_initialiser() constructs InitialiseFactory`
- c0047 ..> c0035: `type in build_initialiser`
- c0047 ..> c0044: `build_watcher() constructs ScaffoldIssue`
- c0047 ..> c0046: `build_watcher() constructs WatchFactory`
- c0047 ..> c0046: `type in build_watcher`
- c0047 ..> c0047: `build_watcher() calls prepare_foreman_launch()`
- c0047 ..> c0050: `build_watcher() constructs FactoryError`
- c0047 ..> c0050: `prepare_foreman_launch() constructs FactoryError`
- c0048 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0048 ..> c0003: `_watch_locked() calls run()`
- c0048 ..> c0005: `_foreman() calls enter_terminal()`
- c0048 ..> c0005: `_foreman() calls read_state()`
- c0048 ..> c0005: `_foreman() calls request()`
- c0048 ..> c0005: `_foreman() calls start_owner()`
- c0048 ..> c0005: `_initialise() calls enter_terminal()`
- c0048 ..> c0005: `_initialise() calls request()`
- c0048 ..> c0005: `_initialise_locked() calls read_state()`
- c0048 ..> c0005: `_launch_setup_foreman() calls start_owner()`
- c0048 ..> c0005: `_offer_factory_launch() calls read_state()`
- c0048 ..> c0005: `_watch() calls read_state()`
- c0048 ..> c0005: `_watch() calls request()`
- c0048 ..> c0005: `_watch_locked() calls read_state()`
- c0048 ..> c0011: `_complete_setup() calls record_completion()`
- c0048 ..> c0011: `_complete_setup() calls uses_browser_login()`
- c0048 ..> c0011: `_initialise_locked() calls begin_setup()`
- c0048 ..> c0011: `_initialise_locked() calls choose_pi_home()`
- c0048 ..> c0011: `_initialise_locked() calls save_pi_choice()`
- c0048 ..> c0011: `_initialise_locked() calls selected_launch()`
- c0048 ..> c0011: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0048 ..> c0011: `_select_model() calls list_models()`
- c0048 ..> c0011: `_select_project() calls create_project()`
- c0048 ..> c0011: `_select_project() calls projects()`
- c0048 ..> c0011: `_watch() calls validate_completion()`
- c0048 ..> c0011: `_watch() constructs ForemanProfile`
- c0048 ..> c0013: `select_repositories() calls discover()`
- c0048 ..> c0018: `_initialise_locked() calls load()`
- c0048 ..> c0019: `_initialise() calls quote()`
- c0048 ..> c0019: `_initialise_locked() calls quote()`
- c0048 ..> c0019: `_launch_setup_foreman() calls quote()`
- c0048 ..> c0019: `_select_model() calls quote()`
- c0048 ..> c0019: `_watch() calls quote()`
- c0048 ..> c0019: `_watch_locked() calls quote()`
- c0048 ..> c0020: `_foreman() calls hold()`
- c0048 ..> c0020: `_foreman() constructs WorkspaceWatchLease`
- c0048 ..> c0020: `_initialise() calls hold()`
- c0048 ..> c0020: `_initialise() constructs WorkspaceWatchLease`
- c0048 ..> c0020: `_watch() calls hold()`
- c0048 ..> c0020: `_watch() constructs WorkspaceWatchLease`
- c0048 ..> c0030: `type in _complete_setup`
- c0048 ..> c0030: `type in _configure_new_factory`
- c0048 ..> c0031: `_connection() calls validate()`
- c0048 ..> c0031: `_connection() constructs ForgetfulConnection`
- c0048 ..> c0031: `type in _check_existing_connection`
- c0048 ..> c0031: `type in _configure_new_factory`
- c0048 ..> c0031: `type in _connection`
- c0048 ..> c0031: `type in _select_project`
- c0048 ..> c0033: `_configure_new_factory() constructs InitialAgentChoices`
- c0048 ..> c0033: `type in _configure_new_factory`
- c0048 ..> c0033: `type in _owner_choices`
- c0048 ..> c0033: `type in _worker_choices`
- c0048 ..> c0034: `_initialise_locked() calls validate_initial_agents()`
- c0048 ..> c0035: `_complete_setup() calls check_foreman()`
- c0048 ..> c0035: `_configure_new_factory() calls configure()`
- c0048 ..> c0035: `_configure_new_factory() calls inspect()`
- c0048 ..> c0035: `_initialise_locked() calls initialise()`
- c0048 ..> c0035: `_initialise_locked() calls load_existing()`
- c0048 ..> c0035: `_launch_setup_foreman() calls check_foreman()`
- c0048 ..> c0035: `_prepare_foreman() calls prepare_foreman()`
- c0048 ..> c0035: `type in _complete_setup`
- c0048 ..> c0035: `type in _configure_new_factory`
- c0048 ..> c0035: `type in _select_project`
- c0048 ..> c0035: `type in select_repositories`
- c0048 ..> c0047: `_foreman() calls prepare_foreman_launch()`
- c0048 ..> c0047: `_initialise_locked() calls build_initialiser()`
- c0048 ..> c0047: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0048 ..> c0047: `_watch_locked() calls build_watcher()`
- c0048 ..> c0048: `_configure_new_factory() calls _prepare_foreman()`
- c0048 ..> c0048: `_configure_new_factory() calls _select_model()`
- c0048 ..> c0048: `_configure_new_factory() calls _select_numbered()`
- c0048 ..> c0048: `_configure_new_factory() calls select_repositories()`
- c0048 ..> c0048: `_connection() calls _check_existing_connection()`
- c0048 ..> c0048: `_initialise() calls _initialise_locked()`
- c0048 ..> c0048: `_initialise() calls _offer_factory_launch()`
- c0048 ..> c0048: `_initialise_locked() calls _complete_setup()`
- c0048 ..> c0048: `_initialise_locked() calls _configure_new_factory()`
- c0048 ..> c0048: `_initialise_locked() calls _confirm_pi_home()`
- c0048 ..> c0048: `_initialise_locked() calls _connection()`
- c0048 ..> c0048: `_initialise_locked() calls _launch_setup_foreman()`
- c0048 ..> c0048: `_initialise_locked() calls _owner_choices()`
- c0048 ..> c0048: `_initialise_locked() calls _research_choices()`
- c0048 ..> c0048: `_initialise_locked() calls _worker_choices()`
- c0048 ..> c0048: `_print_models() calls _safe_diagnostic()`
- c0048 ..> c0048: `_prompt_worker() calls _select_numbered()`
- c0048 ..> c0048: `_prompt_workers() calls _prompt_worker()`
- c0048 ..> c0048: `_select_model() calls _print_models()`
- c0048 ..> c0048: `_select_model() calls _select_numbered()`
- c0048 ..> c0048: `_select_numbered() calls _safe_diagnostic()`
- c0048 ..> c0048: `_select_project() calls _listed_project_id()`
- c0048 ..> c0048: `_select_project() calls _safe_diagnostic()`
- c0048 ..> c0048: `_watch() calls _watch_locked()`
- c0048 ..> c0048: `_watch_locked() calls _choose_existing()`
- c0048 ..> c0048: `_watch_locked() calls _safe_diagnostic()`
- c0048 ..> c0048: `_worker_choices() calls _prompt_workers()`
- c0048 ..> c0048: `_worker_choices() calls _select_numbered()`
- c0048 ..> c0048: `_worker_choices() calls _worker_arguments()`
- c0048 ..> c0048: `main() calls _foreman()`
- c0048 ..> c0048: `main() calls _initialise()`
- c0048 ..> c0048: `main() calls _parse_arguments()`
- c0048 ..> c0048: `main() calls _safe_diagnostic()`
- c0048 ..> c0048: `main() calls _watch()`
- c0048 ..> c0049: `_foreman() calls load_configuration()`
- c0048 ..> c0049: `_watch() calls load_configuration()`
- c0048 ..> c0049: `_watch_locked() calls load_configuration()`
- c0048 ..> c0050: `_check_existing_connection() constructs FactoryError`
- c0048 ..> c0050: `_choose_existing() constructs FactoryError`
- c0048 ..> c0050: `_configure_new_factory() constructs FactoryError`
- c0048 ..> c0050: `_foreman() constructs FactoryError`
- c0048 ..> c0050: `_initialise() constructs FactoryError`
- c0048 ..> c0050: `_initialise_locked() constructs FactoryError`
- c0048 ..> c0050: `_install_missing() constructs FactoryError`
- c0048 ..> c0050: `_listed_project_id() constructs FactoryError`
- c0048 ..> c0050: `_prompt_worker() constructs FactoryError`
- c0048 ..> c0050: `_select_model() constructs FactoryError`
- c0048 ..> c0050: `_select_numbered() constructs FactoryError`
- c0048 ..> c0050: `_select_project() constructs FactoryError`
- c0048 ..> c0050: `_watch() constructs FactoryError`
- c0048 ..> c0050: `_watch_locked() constructs FactoryError`
- c0048 ..> c0050: `_worker_choices() constructs FactoryError`
- c0048 ..> c0050: `main() constructs FactoryError`
- c0048 ..> c0050: `select_repositories() constructs FactoryError`
- c0049 ..> c0018: `load_configuration() calls load()`
- c0049 ..> c0018: `load_configuration() constructs TomlConfigurationStore`
- c0049 ..> c0030: `type in load_configuration`
- c0049 ..> c0050: `load_configuration() constructs FactoryError`
- c0051 --> c0054: `field source`
- c0053 --> c0054: `field work_source`
- c0055 ..> c0051: `type in list_issues`
- c0055 ..> c0052: `type in create_label`
- c0055 ..> c0052: `type in list_labels`
- c0055 ..> c0054: `type in check_access`
- c0055 ..> c0054: `type in create_label`
- c0055 ..> c0054: `type in list_issues`
- c0055 ..> c0054: `type in list_labels`

## Type key

- Type1: `dict | None`
- Type2: `dict[str, str] | None`
- Type3: `str | None`
- Type4: `subprocess.Popen | None`
- Type5: `dict[tuple[str, Path], list[str]]`
- Type6: `Path | None`
- Type7: `tuple[Path, list[dict]]`
- Type8: `FactoryConfiguration | None`
- Type9: `dict[str, str]`
- Type10: `tuple[Label, ...]`
- Type11: `tuple[Issue, ...]`
- Type12: `tuple[str, ...]`
- Type13: `tuple[Path, ...]`
- Type14: `float | None`
- Type15: `tuple[RepositoryReference, ...]`
- Type16: `ForgetfulConnection | None`
- Type17: `int | None`
- Type18: `Callable[[list[str]], None]`
- Type19: `Callable[[str, str], bool]`
- Type20: `list[Path] | None`
- Type21: `list[str] | None`
- Type22: `dict[str, RepositoryReference]`
- Type23: `dict[WorkSource, tuple[Label, ...]]`
- Type24: `Callable[[], FactoryConfiguration | None]`
- Type25: `Callable[[], bool]`
- Type26: `Callable[[str], None]`
- Type27: `tuple[Issue, ...] | None`
- Type28: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type29: `list[str] | tuple[str, ...]`
- Type30: `int | dict | str`
- Type31: `str | Path`

## Signature key

- Signature1: `+interact(session: unknown, reader: unknown, reply: unknown, name: unknown,
  persistent: unknown, startup_warning: unknown) None`
- Signature2: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None, model: str | None, effort: str | None) unknown`
- Signature3: `-_write_agent(name: unknown, model: unknown, effort: unknown, description: unknown,
  children: unknown, resources: unknown) unknown`
- Signature4: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature5: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool)
  unknown`
- Signature6: `-__init__(tracking: WorkTrackingService, storage: ConfigurationStore, repositories:
  LocalRepositories, sources: WorkSourceResolver, profile: ForemanProfile) unknown`
- Signature7: `-__init__(planning: Planning, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration) unknown`
- Signature8: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, scaffold:
  ScaffoldIssue) unknown`
- Signature9: `+run(config: FactoryConfiguration, workspace: Path, interval: float, choose_existing:
  Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature10: `-_watch(config: FactoryConfiguration, workspace: Path, interval: float, existing:
  bool, report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature11: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown) WatchFactory`
- Signature12: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown) unknown`
- Signature13: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature14: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature15: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature16: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature17: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature18: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature19: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature20: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature21: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature22: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
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
