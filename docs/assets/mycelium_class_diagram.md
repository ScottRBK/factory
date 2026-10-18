# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 47 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 1196. Type relationships removed: 19.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_architecture.py`: 12 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_cleanup_recovery.py`: 14 source occurrences (test-path).
- `tests/test_configuration.py`: 12 source occurrences (test-path).
- `tests/test_init.py`: 43 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 18 source occurrences (test-path).
- `tests/test_native_roles.py`: 3 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_planning_setup.py`: 13 source occurrences (test-path).
- `tests/test_planning_watch.py`: 27 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_setup_completion.py`: 30 source occurrences (test-path).
- `tests/test_shared_pi.py`: 21 source occurrences (test-path).
- `tests/test_watch.py`: 51 source occurrences (test-path).
- `tests/test_watch_lock.py`: 4 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 14 source occurrences (test-path).
- `tests/test_worker_profiles.py`: 8 source occurrences (test-path).
- `tests/test_worker_setup.py`: 15 source occurrences (test-path).
- `tests/worker_support.py`: 2 source occurrences (test-path).

## Diagram 1

```mermaid
classDiagram
    direction TB
    class c0000["src/forgetful_factory/adapters/agentshell/controller.py"] {
        <<module>>
        +ready(session: unknown) None
        +interact(session: unknown, reader: unknown, reply: unknown, name: unknown) None
        +serve(reader: unknown, config: unknown, reply: unknown) None
        +control(reply: unknown) None
        +main(reply: unknown) int
        +reply(value: unknown) unknown
    }
    class c0001["src/forgetful_factory/adapters/agentshell/model_catalog.py"] {
        <<module>>
        +main() None
    }
    class c0002["AgentShellTerminal"] {
        <<class>>
        -__init__(Signature1)
        +python: unknown
        +environment: unknown
        +resources: unknown
        +prompt: unknown
        +cwd: unknown
        +process: Type4
        +buffer: unknown
        +session_name: unknown
        +startup_hint() str
        -_write(value: dict, timeout: float) None
        -_read(timeout: float, expected: str) dict
        +start(cwd: str, model: str, effort: str) None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0003["src/forgetful_factory/adapters/command.py"] {
        <<module>>
        +run_command(arguments: list[str]) str
    }
    class c0004["CoordinatorProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workers: unknown
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(config: FactoryConfiguration) None
        -_worker_role(role: str, config: FactoryConfiguration) dict
        -_role(name: str, config: FactoryConfiguration) dict
        -_selection_files() dict
        +selection(config: FactoryConfiguration) dict
        +validate_guidance(config: FactoryConfiguration) None
    }
    class c0005["src/forgetful_factory/adapters/filesystem/coordinator_profiles.py"] {
        <<module>>
        -_selection_conflict(path: Path) FactoryError
        -_read_selection(path: Path) dict
        +selected_resources(skills: list[str], extensions: list[str]) dict
        -_local_resource_paths(directory: Path, paths: object) list[str]
    }
    class c0006["ForemanProfile"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +resources_path: unknown
        -_pi_choice: Type2
        -_model_catalogs: Type5
        +missing_executables(connection: ForgetfulConnection) list[str]
        +validate_setup(connection: ForgetfulConnection) None
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
        +prepare_roles(config: unknown) None
        +validate_worker_models(config: FactoryConfiguration) None
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type6) list[str]
        -_model_catalogs#91;key#93;: unknown
        -_selection(config: FactoryConfiguration) dict
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
        +validate_completion(config: FactoryConfiguration) None
        +launch_resources() dict
        -_local_resource_path(value: object) str
        -_read_guidance(relative: str) str
        +validate_guidance() None
    }
    class c0007["GitRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0008["GitWorktrees"] {
        <<class>>
        -_repository_entries(repository: str, remote: str) Type7
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
    }
    class c0009["src/forgetful_factory/adapters/filesystem/git_worktrees.py"] {
        <<module>>
        -_worktree_entries(output: str) list[dict]
    }
    class c0010["src/forgetful_factory/adapters/filesystem/resource_files.py"] {
        <<module>>
        +check_real_path(path: Path) None
        +write_new(path: Path, content: str) None
        +write_json(path: Path, value: dict) None
        -_generated_parent(path: Path) unknown
        +remove_generated(path: Path) None
        +replace_generated_json(path: Path, value: dict) None
        +read_generated_json(path: Path) dict
    }
    class c0011["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type8
        +save(configuration: FactoryConfiguration) None
    }
    class c0012["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0013["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +hold() Iterator[None]
    }
    class c0014["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +skills(role: str, config: FactoryConfiguration) list[str]
        -_skill_digest(value: str) str
        -_validate_skill_sources(config: FactoryConfiguration) None
        +prepare(config: FactoryConfiguration) None
        +resources(role: str, config: FactoryConfiguration) dict
        -_role_selection(role: str, config: FactoryConfiguration) dict
        +selection(config: FactoryConfiguration) dict
    }
    class c0015["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0016["AgentForgetfulConnection"] {
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
    class c0017["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature2)
        -_catalog_tools(catalog: object) dict
    }
    class c0018["ForgetfulPlanning"] {
        <<class>>
        -__init__(Signature3)
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
    class c0019["GitHubWorkTracking"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type10
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type12) Type11
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0020["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +runtime: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type1) Type9
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type1) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0021["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type13) str
        +runtime_ready(runtime: Path, inputs: Type13, probe: str) bool
    }
    class c0022["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        +run_owned(args: list[str], cwd: Path, env: Type9, login: bool, timeout: Type14) str
    }
    class c0023["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type12
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +repository: Type15
        +forgetful: Type16
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
        +execution_enabled: bool
    }
    class c0024["ForgetfulConnection"] {
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
    class c0025["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type16
        +validate_workers(configuration: FactoryConfiguration) None
        +skill_paths(data: dict, field: str) Type12
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type12
    }
    class c0026["InitialiseFactory"] {
        <<class>>
        -__init__(Signature4)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type18, confirm: Type19) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type20, labels: Type21, model: Type3, effort: Type3) Type8
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type22
        +configure(Signature5)
        -_preflight(config: FactoryConfiguration) Type23
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type24, save: bool) list[str]
    }
    class c0027["ConfigurationStore"] {
        <<class>>
        +load() Type8
        +save(configuration: FactoryConfiguration) None
    }
    class c0028["ForemanProfile"] {
        <<class>>
        +prepare_roles(config: FactoryConfiguration) None
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
        +list_models(connection: ForgetfulConnection, harness: str, cwd: Type6) list[str]
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
    }
    class c0029["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start(cwd: str, model: str, effort: str) None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0030["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0031["Planning"] {
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
    class c0032["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0033["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0034["Worktrees"] {
        <<class>>
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
    }
    class c0035["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature6)
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
    class c0036["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        -_cleanup_state(mapping: dict) Type3
    }
    class c0037["WatchFactory"] {
        <<class>>
        -__init__(Signature7)
        +tracking: unknown
        +terminal: unknown
        +lease: unknown
        +scaffold: unknown
        +run(Signature8)
        -_watch(Signature9)
        -_notify_issues(issues: Type11, seen: Type9, report: Type26, recovered: bool) None
        -_read_issues(source: WorkSource, labels: Type12, report_error: Type26) Type27
    }
    class c0038["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path) InitialiseFactory
        +build_watcher(python: str, config: FactoryConfiguration, workspace: Path) WatchFactory
    }
    class c0039["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature10)
        -_check_existing_connection(Signature11)
        -_connection(Signature12)
        -_prepare_foreman(Signature13)
        -_print_models(models: list[str]) None
        -_select_model(Signature14)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_watch(args: argparse.Namespace, workspace: Path) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature15)
        -_owner_configuration(Signature16)
        -_worker_arguments(args: argparse.Namespace) dict
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_worker_configuration(Signature17)
        -_complete_setup(Signature18)
        -_initialise(args: argparse.Namespace, workspace: Path) int
        +main() int
    }
    class c0040["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type28) FactoryConfiguration
    }
    class c0041["FactoryError"] {
        <<class>>
    }
    class c0042["Issue"] {
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
    class c0043["Label"] {
        <<class>>
        +name: str
    }
    class c0044["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0045["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0046["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type10
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type12) Type11
    }
    c0000 ..> c0000 : 4 relationships (see list)
    c0000 ..> c0002 : 4 relationships (see list)
    c0000 ..> c0018 : 3 relationships (see list)
    c0001 ..> c0006 : main() calls list_models()
    c0002 ..> c0002 : 5 relationships (see list)
    c0002 ..> c0029 : close() calls close()
    c0002 ..> c0041 : 4 relationships (see list)
    c0003 ..> c0037 : run_command() calls run()
    c0003 ..> c0041 : run_command() constructs FactoryError
    c0004 ..> c0004 : 7 relationships (see list)
    c0004 ..> c0005 : 8 relationships (see list)
    c0004 ..> c0006 : prepare() calls prepare()
    c0004 ..> c0010 : 2 relationships (see list)
    c0004 ..> c0014 : 3 relationships (see list)
    c0004 ..> c0023 : 5 relationships (see list)
    c0004 ..> c0041 : 4 relationships (see list)
    c0005 ..> c0005 : _read_selection() calls _selection_conflict()
    c0005 ..> c0010 : _read_selection() calls check_real_path()
    c0005 ..> c0041 : 2 relationships (see list)
    c0006 ..> c0004 : 7 relationships (see list)
    c0006 ..> c0006 : 25 relationships (see list)
    c0006 ..> c0010 : 7 relationships (see list)
    c0006 ..> c0012 : require_pi_home() calls quote()
    c0006 ..> c0015 : uses_browser_login() calls uses_browser_login()
    c0006 ..> c0016 : 8 relationships (see list)
    c0006 ..> c0017 : list_models() calls role_environment()
    c0006 ..> c0020 : 6 relationships (see list)
    c0006 ..> c0021 : 3 relationships (see list)
    c0006 ..> c0022 : list_models() calls run_owned()
    c0006 ..> c0023 : 4 relationships (see list)
    c0006 ..> c0024 : 9 relationships (see list)
    c0006 ..> c0041 : 13 relationships (see list)
    c0007 ..> c0003 : origin() calls run_command()
    c0007 ..> c0041 : origin() constructs FactoryError
    c0008 ..> c0003 : 2 relationships (see list)
    c0008 ..> c0008 : 2 relationships (see list)
    c0008 ..> c0009 : _repository_entries() calls _worktree_entries()
    c0008 ..> c0041 : 3 relationships (see list)
    c0010 ..> c0002 : _generated_parent() calls close()
    c0010 ..> c0010 : 6 relationships (see list)
    c0010 ..> c0011 : read_generated_json() calls load()
    c0010 ..> c0041 : 4 relationships (see list)
    c0011 ..> c0002 : 2 relationships (see list)
    c0011 ..> c0012 : save() calls quote()
    c0011 ..> c0023 : 2 relationships (see list)
    c0011 ..> c0025 : load() calls from_mapping()
    c0011 ..> c0027 : load() calls load()
    c0011 ..> c0041 : 2 relationships (see list)
    c0013 ..> c0002 : hold() calls close()
    c0013 ..> c0041 : hold() constructs FactoryError
    c0014 ..> c0010 : 4 relationships (see list)
    c0014 ..> c0014 : 8 relationships (see list)
    c0014 ..> c0021 : _role_selection() calls executable_path()
    c0014 ..> c0023 : 6 relationships (see list)
    c0014 ..> c0041 : 2 relationships (see list)
    c0015 ..> c0024 : type in uses_browser_login
    c0016 ..> c0016 : 7 relationships (see list)
    c0016 ..> c0017 : 2 relationships (see list)
    c0016 ..> c0022 : 2 relationships (see list)
    c0016 ..> c0024 : 7 relationships (see list)
    c0016 ..> c0041 : 5 relationships (see list)
    c0017 ..> c0021 : role_environment() calls executable_path()
    c0017 ..> c0024 : type in role_environment
    c0018 ..> c0006 : check() calls check()
    c0018 ..> c0016 : 2 relationships (see list)
    c0018 ..> c0018 : 9 relationships (see list)
    c0018 ..> c0024 : type in __init__
    c0018 ..> c0041 : _rows() constructs FactoryError
    c0019 ..> c0003 : _api() calls run_command()
    c0019 ..> c0019 : 5 relationships (see list)
    c0019 ..> c0041 : 7 relationships (see list)
    c0019 ..> c0042 : 2 relationships (see list)
    c0019 ..> c0043 : 3 relationships (see list)
    c0019 ..> c0045 : 8 relationships (see list)
    c0020 ..> c0010 : install() calls write_new()
    c0020 ..> c0020 : 15 relationships (see list)
    c0020 ..> c0021 : 3 relationships (see list)
    c0020 ..> c0022 : 4 relationships (see list)
    c0020 ..> c0041 : 6 relationships (see list)
    c0021 ..> c0021 : runtime_ready() calls sync_fingerprint()
    c0021 ..> c0022 : runtime_ready() calls run_owned()
    c0022 ..> c0041 : run_owned() constructs FactoryError
    c0023 --> c0024 : field forgetful
    c0023 --> c0044 : field repository
    c0024 ..> c0025 : 2 relationships (see list)
    c0024 ..> c0041 : _validate_server() constructs FactoryError
    c0025 ..> c0023 : 4 relationships (see list)
    c0025 ..> c0024 : 3 relationships (see list)
    c0025 ..> c0025 : 9 relationships (see list)
    c0025 ..> c0041 : 6 relationships (see list)
    c0025 ..> c0044 : from_mapping() constructs RepositoryReference
    c0025 ..> c0045 : from_mapping() constructs WorkSource
    c0026 ..> c0004 : prepare_foreman() calls prepare()
    c0026 ..> c0006 : 5 relationships (see list)
    c0026 ..> c0007 : 3 relationships (see list)
    c0026 ..> c0011 : 2 relationships (see list)
    c0026 ..> c0019 : 5 relationships (see list)
    c0026 ..> c0023 : 6 relationships (see list)
    c0026 ..> c0024 : 2 relationships (see list)
    c0026 ..> c0025 : 2 relationships (see list)
    c0026 ..> c0026 : 3 relationships (see list)
    c0026 ..> c0027 : type in __init__
    c0026 ..> c0028 : type in __init__
    c0026 ..> c0030 : type in __init__
    c0026 ..> c0033 : type in __init__
    c0026 ..> c0041 : 5 relationships (see list)
    c0026 ..> c0043 : 2 relationships (see list)
    c0026 ..> c0044 : 2 relationships (see list)
    c0026 ..> c0045 : 2 relationships (see list)
    c0026 ..> c0046 : type in __init__
    c0027 ..> c0023 : 2 relationships (see list)
    c0028 ..> c0023 : 2 relationships (see list)
    c0028 ..> c0024 : 8 relationships (see list)
    c0033 ..> c0045 : type in source_from_remote
    c0035 ..> c0006 : check() calls check()
    c0035 ..> c0008 : 2 relationships (see list)
    c0035 ..> c0018 : 8 relationships (see list)
    c0035 ..> c0023 : type in __init__
    c0035 ..> c0031 : type in __init__
    c0035 ..> c0034 : type in __init__
    c0035 ..> c0035 : 7 relationships (see list)
    c0035 ..> c0036 : _ensure_mapping() calls _cleanup_state()
    c0035 ..> c0041 : 7 relationships (see list)
    c0035 ..> c0042 : 4 relationships (see list)
    c0035 ..> c0045 : unfinished() constructs WorkSource
    c0036 ..> c0041 : _cleanup_state() constructs FactoryError
    c0037 ..> c0002 : 5 relationships (see list)
    c0037 ..> c0004 : _notify_issues() calls prepare()
    c0037 ..> c0006 : run() calls check()
    c0037 ..> c0013 : run() calls hold()
    c0037 ..> c0019 : _read_issues() calls list_issues()
    c0037 ..> c0023 : 2 relationships (see list)
    c0037 ..> c0029 : type in __init__
    c0037 ..> c0032 : type in __init__
    c0037 ..> c0035 : 2 relationships (see list)
    c0037 ..> c0037 : 3 relationships (see list)
    c0037 ..> c0042 : 2 relationships (see list)
    c0037 ..> c0045 : 2 relationships (see list)
    c0037 ..> c0046 : type in __init__
    c0038 ..> c0002 : build_watcher() constructs AgentShellTerminal
    c0038 ..> c0004 : build_watcher() calls validate_guidance()
    c0038 ..> c0006 : 6 relationships (see list)
    c0038 ..> c0007 : build_initialiser() constructs GitRepositories
    c0038 ..> c0008 : build_watcher() constructs GitWorktrees
    c0038 ..> c0011 : build_initialiser() constructs TomlConfigurationStore
    c0038 ..> c0013 : build_watcher() constructs WorkspaceWatchLease
    c0038 ..> c0017 : build_watcher() calls role_environment()
    c0038 ..> c0018 : build_watcher() constructs ForgetfulPlanning
    c0038 ..> c0019 : 3 relationships (see list)
    c0038 ..> c0023 : type in build_watcher
    c0038 ..> c0026 : 2 relationships (see list)
    c0038 ..> c0035 : build_watcher() constructs ScaffoldIssue
    c0038 ..> c0037 : 2 relationships (see list)
    c0038 ..> c0041 : build_watcher() constructs FactoryError
    c0039 ..> c0006 : 7 relationships (see list)
    c0039 ..> c0007 : select_repositories() calls discover()
    c0039 ..> c0012 : _select_model() calls quote()
    c0039 ..> c0023 : 4 relationships (see list)
    c0039 ..> c0024 : 6 relationships (see list)
    c0039 ..> c0026 : 10 relationships (see list)
    c0039 ..> c0037 : _watch() calls run()
    c0039 ..> c0038 : 2 relationships (see list)
    c0039 ..> c0039 : 24 relationships (see list)
    c0039 ..> c0040 : _watch() calls load_configuration()
    c0039 ..> c0041 : 14 relationships (see list)
    c0040 ..> c0011 : 2 relationships (see list)
    c0040 ..> c0023 : type in load_configuration
    c0040 ..> c0041 : load_configuration() constructs FactoryError
    c0042 --> c0045 : field source
    c0044 --> c0045 : field work_source
    c0046 ..> c0042 : type in list_issues
    c0046 ..> c0043 : 2 relationships (see list)
    c0046 ..> c0045 : 4 relationships (see list)
```

## Source index

- c0000: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0001: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0002: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:12
- c0003: `src/forgetful_factory/adapters/command.py` — `src/forgetful_factory/adapters/command.py`:1
- c0004: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:59
- c0005: `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:1
- c0006: `ForemanProfile` — `src/forgetful_factory/adapters/filesystem/foreman_profile.py`:45
- c0007: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:7
- c0008: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:21
- c0009: `src/forgetful_factory/adapters/filesystem/git_worktrees.py` —
  `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:1
- c0010: `src/forgetful_factory/adapters/filesystem/resource_files.py` —
  `src/forgetful_factory/adapters/filesystem/resource_files.py`:1
- c0011: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:21
- c0012: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0013: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0014: `WorkerProfiles` — `src/forgetful_factory/adapters/filesystem/worker_profiles.py`:21
- c0015: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0016: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:52
- c0017: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0018: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:8
- c0019: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0020: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:52
- c0021: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0022: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0023: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:80
- c0024: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0025: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0026: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0027: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0028: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:7
- c0029: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0030: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0031: `Planning` — `src/forgetful_factory/application/ports/planning.py`:4
- c0032: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0033: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0034: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:4
- c0035: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:31
- c0036: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0037: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:13
- c0038: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0039: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0040: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0041: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0042: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0043: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0044: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0045: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0046: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `control() calls serve()`
- c0000 ..> c0000: `interact() calls ready()`
- c0000 ..> c0000: `main() calls control()`
- c0000 ..> c0000: `serve() calls interact()`
- c0000 ..> c0002: `control() calls close()`
- c0000 ..> c0002: `control() calls wait()`
- c0000 ..> c0002: `serve() calls close()`
- c0000 ..> c0002: `serve() calls wait()`
- c0000 ..> c0018: `control() calls create_task()`
- c0000 ..> c0018: `main() calls create_task()`
- c0000 ..> c0018: `serve() calls create_task()`
- c0001 ..> c0006: `main() calls list_models()`
- c0002 ..> c0002: `send() calls _read()`
- c0002 ..> c0002: `send() calls _write()`
- c0002 ..> c0002: `start() calls _read()`
- c0002 ..> c0002: `start() calls _write()`
- c0002 ..> c0002: `wait() calls _read()`
- c0002 ..> c0029: `close() calls close()`
- c0002 ..> c0041: `_read() constructs FactoryError`
- c0002 ..> c0041: `_write() constructs FactoryError`
- c0002 ..> c0041: `close() constructs FactoryError`
- c0002 ..> c0041: `start() constructs FactoryError`
- c0003 ..> c0037: `run_command() calls run()`
- c0003 ..> c0041: `run_command() constructs FactoryError`
- c0004 ..> c0004: `prepare() calls _role()`
- c0004 ..> c0004: `prepare() calls _worker_role()`
- c0004 ..> c0004: `prepare() calls validate_guidance()`
- c0004 ..> c0004: `selection() calls _role()`
- c0004 ..> c0004: `selection() calls _selection_files()`
- c0004 ..> c0004: `selection() calls _worker_role()`
- c0004 ..> c0004: `selection() calls validate_guidance()`
- c0004 ..> c0005: `_role() calls _local_resource_paths()`
- c0004 ..> c0005: `_role() calls _read_selection()`
- c0004 ..> c0005: `_role() calls _selection_conflict()`
- c0004 ..> c0005: `_role() calls selected_resources()`
- c0004 ..> c0005: `_selection_files() calls _read_selection()`
- c0004 ..> c0005: `_worker_role() calls _local_resource_paths()`
- c0004 ..> c0005: `_worker_role() calls selected_resources()`
- c0004 ..> c0005: `selection() calls _selection_conflict()`
- c0004 ..> c0006: `prepare() calls prepare()`
- c0004 ..> c0010: `prepare() calls write_json()`
- c0004 ..> c0010: `prepare() calls write_new()`
- c0004 ..> c0014: `__init__() constructs WorkerProfiles`
- c0004 ..> c0014: `_worker_role() calls resources()`
- c0004 ..> c0014: `selection() calls selection()`
- c0004 ..> c0023: `type in _role`
- c0004 ..> c0023: `type in _worker_role`
- c0004 ..> c0023: `type in prepare`
- c0004 ..> c0023: `type in selection`
- c0004 ..> c0023: `type in validate_guidance`
- c0004 ..> c0041: `prepare() constructs FactoryError`
- c0004 ..> c0041: `selection() constructs FactoryError`
- c0004 ..> c0041: `validate_depth() constructs FactoryError`
- c0004 ..> c0041: `validate_guidance() constructs FactoryError`
- c0005 ..> c0005: `_read_selection() calls _selection_conflict()`
- c0005 ..> c0010: `_read_selection() calls check_real_path()`
- c0005 ..> c0041: `_selection_conflict() constructs FactoryError`
- c0005 ..> c0041: `type in _selection_conflict`
- c0006 ..> c0004: `_selection() calls selection()`
- c0006 ..> c0004: `_selection() constructs CoordinatorProfiles`
- c0006 ..> c0004: `prepare_roles() calls selection()`
- c0006 ..> c0004: `prepare_roles() calls validate_depth()`
- c0006 ..> c0004: `prepare_roles() constructs CoordinatorProfiles`
- c0006 ..> c0004: `validate_setup() calls validate_depth()`
- c0006 ..> c0004: `validate_setup() constructs CoordinatorProfiles`
- c0006 ..> c0006: `_selection() calls pi_home()`
- c0006 ..> c0006: `choose_pi_home() calls pi_home()`
- c0006 ..> c0006: `choose_pi_home() calls require_pi_home()`
- c0006 ..> c0006: `launch_resources() calls _local_resource_path()`
- c0006 ..> c0006: `list_models() calls pi_home()`
- c0006 ..> c0006: `list_models() calls require_pi_home()`
- c0006 ..> c0006: `missing_executables() calls pi_home()`
- c0006 ..> c0006: `prepare() calls _install_resources()`
- c0006 ..> c0006: `prepare() calls _protect_runtime()`
- c0006 ..> c0006: `prepare() calls launch_resources()`
- c0006 ..> c0006: `prepare() calls validate_guidance()`
- c0006 ..> c0006: `prepare_roles() calls pi_home()`
- c0006 ..> c0006: `prepare_roles() calls prepare()`
- c0006 ..> c0006: `prepare_roles() calls validate_worker_models()`
- c0006 ..> c0006: `record_completion() calls _selection()`
- c0006 ..> c0006: `record_completion() calls validate_completion()`
- c0006 ..> c0006: `validate_completion() calls _selection()`
- c0006 ..> c0006: `validate_guidance() calls _read_guidance()`
- c0006 ..> c0006: `validate_setup() calls launch_resources()`
- c0006 ..> c0006: `validate_setup() calls missing_executables()`
- c0006 ..> c0006: `validate_setup() calls pi_home()`
- c0006 ..> c0006: `validate_setup() calls require_pi_home()`
- c0006 ..> c0006: `validate_setup() calls validate_bundled_resources()`
- c0006 ..> c0006: `validate_setup() calls validate_guidance()`
- c0006 ..> c0006: `validate_worker_models() calls list_models()`
- c0006 ..> c0010: `_install_resources() calls write_new()`
- c0006 ..> c0010: `_protect_runtime() calls write_new()`
- c0006 ..> c0010: `begin_setup() calls remove_generated()`
- c0006 ..> c0010: `prepare() calls write_json()`
- c0006 ..> c0010: `prepare() calls write_new()`
- c0006 ..> c0010: `record_completion() calls replace_generated_json()`
- c0006 ..> c0010: `validate_completion() calls read_generated_json()`
- c0006 ..> c0012: `require_pi_home() calls quote()`
- c0006 ..> c0015: `uses_browser_login() calls uses_browser_login()`
- c0006 ..> c0016: `check() calls check()`
- c0006 ..> c0016: `check() constructs AgentForgetfulConnection`
- c0006 ..> c0016: `create_project() calls create_project()`
- c0006 ..> c0016: `create_project() constructs AgentForgetfulConnection`
- c0006 ..> c0016: `login() calls login()`
- c0006 ..> c0016: `login() constructs AgentForgetfulConnection`
- c0006 ..> c0016: `projects() calls projects()`
- c0006 ..> c0016: `projects() constructs AgentForgetfulConnection`
- c0006 ..> c0017: `list_models() calls role_environment()`
- c0006 ..> c0020: `install() calls install()`
- c0006 ..> c0020: `install() constructs HostDependencies`
- c0006 ..> c0020: `installation() calls description()`
- c0006 ..> c0020: `installation() constructs HostDependencies`
- c0006 ..> c0020: `missing_executables() calls pi_ready()`
- c0006 ..> c0020: `missing_executables() constructs HostDependencies`
- c0006 ..> c0021: `missing_executables() calls executable_path()`
- c0006 ..> c0021: `missing_executables() calls runtime_ready()`
- c0006 ..> c0021: `require_pi_home() calls executable_path()`
- c0006 ..> c0022: `list_models() calls run_owned()`
- c0006 ..> c0023: `type in _selection`
- c0006 ..> c0023: `type in record_completion`
- c0006 ..> c0023: `type in validate_completion`
- c0006 ..> c0023: `type in validate_worker_models`
- c0006 ..> c0024: `type in check`
- c0006 ..> c0024: `type in create_project`
- c0006 ..> c0024: `type in list_models`
- c0006 ..> c0024: `type in login`
- c0006 ..> c0024: `type in missing_executables`
- c0006 ..> c0024: `type in prepare`
- c0006 ..> c0024: `type in projects`
- c0006 ..> c0024: `type in uses_browser_login`
- c0006 ..> c0024: `type in validate_setup`
- c0006 ..> c0041: `_install_resources() constructs FactoryError`
- c0006 ..> c0041: `_read_guidance() constructs FactoryError`
- c0006 ..> c0041: `choose_pi_home() constructs FactoryError`
- c0006 ..> c0041: `launch_resources() constructs FactoryError`
- c0006 ..> c0041: `list_models() constructs FactoryError`
- c0006 ..> c0041: `pi_home() constructs FactoryError`
- c0006 ..> c0041: `prepare_roles() constructs FactoryError`
- c0006 ..> c0041: `require_pi_home() constructs FactoryError`
- c0006 ..> c0041: `validate_bundled_resources() constructs FactoryError`
- c0006 ..> c0041: `validate_completion() constructs FactoryError`
- c0006 ..> c0041: `validate_guidance() constructs FactoryError`
- c0006 ..> c0041: `validate_setup() constructs FactoryError`
- c0006 ..> c0041: `validate_worker_models() constructs FactoryError`
- c0007 ..> c0003: `origin() calls run_command()`
- c0007 ..> c0041: `origin() constructs FactoryError`
- c0008 ..> c0003: `_repository_entries() calls run_command()`
- c0008 ..> c0003: `ensure() calls run_command()`
- c0008 ..> c0008: `ensure() calls _repository_entries()`
- c0008 ..> c0008: `verify_removed() calls _repository_entries()`
- c0008 ..> c0009: `_repository_entries() calls _worktree_entries()`
- c0008 ..> c0041: `_repository_entries() constructs FactoryError`
- c0008 ..> c0041: `ensure() constructs FactoryError`
- c0008 ..> c0041: `verify_removed() constructs FactoryError`
- c0010 ..> c0002: `_generated_parent() calls close()`
- c0010 ..> c0010: `_generated_parent() calls check_real_path()`
- c0010 ..> c0010: `read_generated_json() calls _generated_parent()`
- c0010 ..> c0010: `remove_generated() calls _generated_parent()`
- c0010 ..> c0010: `replace_generated_json() calls _generated_parent()`
- c0010 ..> c0010: `write_json() calls write_new()`
- c0010 ..> c0010: `write_new() calls check_real_path()`
- c0010 ..> c0011: `read_generated_json() calls load()`
- c0010 ..> c0041: `_generated_parent() constructs FactoryError`
- c0010 ..> c0041: `check_real_path() constructs FactoryError`
- c0010 ..> c0041: `read_generated_json() constructs FactoryError`
- c0010 ..> c0041: `write_new() constructs FactoryError`
- c0011 ..> c0002: `load() calls close()`
- c0011 ..> c0002: `save() calls close()`
- c0011 ..> c0012: `save() calls quote()`
- c0011 ..> c0023: `type in load`
- c0011 ..> c0023: `type in save`
- c0011 ..> c0025: `load() calls from_mapping()`
- c0011 ..> c0027: `load() calls load()`
- c0011 ..> c0041: `load() constructs FactoryError`
- c0011 ..> c0041: `save() constructs FactoryError`
- c0013 ..> c0002: `hold() calls close()`
- c0013 ..> c0041: `hold() constructs FactoryError`
- c0014 ..> c0010: `_role_selection() calls check_real_path()`
- c0014 ..> c0010: `prepare() calls write_json()`
- c0014 ..> c0010: `prepare() calls write_new()`
- c0014 ..> c0010: `resources() calls check_real_path()`
- c0014 ..> c0014: `_role_selection() calls _skill_digest()`
- c0014 ..> c0014: `_role_selection() calls resources()`
- c0014 ..> c0014: `_validate_skill_sources() calls _skill_digest()`
- c0014 ..> c0014: `_validate_skill_sources() calls skills()`
- c0014 ..> c0014: `prepare() calls _validate_skill_sources()`
- c0014 ..> c0014: `prepare() calls skills()`
- c0014 ..> c0014: `resources() calls skills()`
- c0014 ..> c0014: `selection() calls _role_selection()`
- c0014 ..> c0021: `_role_selection() calls executable_path()`
- c0014 ..> c0023: `type in _role_selection`
- c0014 ..> c0023: `type in _validate_skill_sources`
- c0014 ..> c0023: `type in prepare`
- c0014 ..> c0023: `type in resources`
- c0014 ..> c0023: `type in selection`
- c0014 ..> c0023: `type in skills`
- c0014 ..> c0041: `_skill_digest() constructs FactoryError`
- c0014 ..> c0041: `selection() constructs FactoryError`
- c0015 ..> c0024: `type in uses_browser_login`
- c0016 ..> c0016: `call() calls command()`
- c0016 ..> c0016: `check() calls call()`
- c0016 ..> c0016: `check() calls command()`
- c0016 ..> c0016: `command() calls _environment()`
- c0016 ..> c0016: `create_project() calls call()`
- c0016 ..> c0016: `login() calls _environment()`
- c0016 ..> c0016: `projects() calls command()`
- c0016 ..> c0017: `_environment() calls role_environment()`
- c0016 ..> c0017: `check() calls _catalog_tools()`
- c0016 ..> c0022: `command() calls run_owned()`
- c0016 ..> c0022: `login() calls run_owned()`
- c0016 ..> c0024: `type in _environment`
- c0016 ..> c0024: `type in call`
- c0016 ..> c0024: `type in check`
- c0016 ..> c0024: `type in command`
- c0016 ..> c0024: `type in create_project`
- c0016 ..> c0024: `type in login`
- c0016 ..> c0024: `type in projects`
- c0016 ..> c0041: `check() constructs FactoryError`
- c0016 ..> c0041: `command() constructs FactoryError`
- c0016 ..> c0041: `create_project() constructs FactoryError`
- c0016 ..> c0041: `login() constructs FactoryError`
- c0016 ..> c0041: `projects() constructs FactoryError`
- c0017 ..> c0021: `role_environment() calls executable_path()`
- c0017 ..> c0024: `type in role_environment`
- c0018 ..> c0006: `check() calls check()`
- c0018 ..> c0016: `__init__() constructs AgentForgetfulConnection`
- c0018 ..> c0016: `_call() calls call()`
- c0018 ..> c0018: `create_plan() calls _call()`
- c0018 ..> c0018: `create_task() calls _call()`
- c0018 ..> c0018: `get_plan() calls _call()`
- c0018 ..> c0018: `plans() calls _call()`
- c0018 ..> c0018: `plans() calls _rows()`
- c0018 ..> c0018: `tasks() calls _call()`
- c0018 ..> c0018: `tasks() calls _rows()`
- c0018 ..> c0018: `update_plan() calls _call()`
- c0018 ..> c0018: `update_task() calls _call()`
- c0018 ..> c0024: `type in __init__`
- c0018 ..> c0041: `_rows() constructs FactoryError`
- c0019 ..> c0003: `_api() calls run_command()`
- c0019 ..> c0019: `check_access() calls _api()`
- c0019 ..> c0019: `create_label() calls _api()`
- c0019 ..> c0019: `list_issues() calls _api()`
- c0019 ..> c0019: `list_issues() calls _validate_issue()`
- c0019 ..> c0019: `list_labels() calls _api()`
- c0019 ..> c0041: `_api() constructs FactoryError`
- c0019 ..> c0041: `_validate_issue() constructs FactoryError`
- c0019 ..> c0041: `check_access() constructs FactoryError`
- c0019 ..> c0041: `create_label() constructs FactoryError`
- c0019 ..> c0041: `list_issues() constructs FactoryError`
- c0019 ..> c0041: `list_labels() constructs FactoryError`
- c0019 ..> c0041: `source_from_remote() constructs FactoryError`
- c0019 ..> c0042: `list_issues() constructs Issue`
- c0019 ..> c0042: `type in list_issues`
- c0019 ..> c0043: `list_labels() constructs Label`
- c0019 ..> c0043: `type in create_label`
- c0019 ..> c0043: `type in list_labels`
- c0019 ..> c0045: `source_from_remote() constructs WorkSource`
- c0019 ..> c0045: `type in _api`
- c0019 ..> c0045: `type in _validate_issue`
- c0019 ..> c0045: `type in check_access`
- c0019 ..> c0045: `type in create_label`
- c0019 ..> c0045: `type in list_issues`
- c0019 ..> c0045: `type in list_labels`
- c0019 ..> c0045: `type in source_from_remote`
- c0020 ..> c0010: `install() calls write_new()`
- c0020 ..> c0020: `_check_uv() calls _environment()`
- c0020 ..> c0020: `_forgetful_python() calls _check_uv()`
- c0020 ..> c0020: `_forgetful_python() calls _environment()`
- c0020 ..> c0020: `_install_role_runtime() calls _check_uv()`
- c0020 ..> c0020: `_install_role_runtime() calls _run()`
- c0020 ..> c0020: `_install_tmux() calls _run()`
- c0020 ..> c0020: `_run() calls _environment()`
- c0020 ..> c0020: `description() calls _forgetful_python()`
- c0020 ..> c0020: `description() calls _ubuntu_tmux()`
- c0020 ..> c0020: `install() calls _forgetful_python()`
- c0020 ..> c0020: `install() calls _install_role_runtime()`
- c0020 ..> c0020: `install() calls _install_tmux()`
- c0020 ..> c0020: `install() calls _run()`
- c0020 ..> c0020: `install() calls _ubuntu_tmux()`
- c0020 ..> c0020: `pi_ready() calls _environment()`
- c0020 ..> c0021: `_install_role_runtime() calls sync_fingerprint()`
- c0020 ..> c0021: `install() calls sync_fingerprint()`
- c0020 ..> c0021: `pi_ready() calls sync_fingerprint()`
- c0020 ..> c0022: `_check_uv() calls run_owned()`
- c0020 ..> c0022: `_forgetful_python() calls run_owned()`
- c0020 ..> c0022: `_run() calls run_owned()`
- c0020 ..> c0022: `pi_ready() calls run_owned()`
- c0020 ..> c0041: `_check_uv() constructs FactoryError`
- c0020 ..> c0041: `_forgetful_python() constructs FactoryError`
- c0020 ..> c0041: `_install_role_runtime() constructs FactoryError`
- c0020 ..> c0041: `_install_tmux() constructs FactoryError`
- c0020 ..> c0041: `_run() constructs FactoryError`
- c0020 ..> c0041: `install() constructs FactoryError`
- c0021 ..> c0021: `runtime_ready() calls sync_fingerprint()`
- c0021 ..> c0022: `runtime_ready() calls run_owned()`
- c0022 ..> c0041: `run_owned() constructs FactoryError`
- c0023 --> c0024: `field forgetful`
- c0023 --> c0044: `field repository`
- c0024 ..> c0025: `_validate_server() calls loopback_host()`
- c0024 ..> c0025: `_validate_server() calls nonblank()`
- c0024 ..> c0041: `_validate_server() constructs FactoryError`
- c0025 ..> c0023: `from_mapping() constructs FactoryConfiguration`
- c0025 ..> c0023: `type in from_mapping`
- c0025 ..> c0023: `type in validate`
- c0025 ..> c0023: `type in validate_workers`
- c0025 ..> c0024: `connection_from_mapping() constructs ForgetfulConnection`
- c0025 ..> c0024: `type in connection_from_mapping`
- c0025 ..> c0024: `validate() calls _validate_server()`
- c0025 ..> c0025: `connection_from_mapping() calls validate()`
- c0025 ..> c0025: `from_mapping() calls connection_from_mapping()`
- c0025 ..> c0025: `from_mapping() calls skill_paths()`
- c0025 ..> c0025: `from_mapping() calls validate()`
- c0025 ..> c0025: `skill_paths() calls nonblank()`
- c0025 ..> c0025: `unique_labels() calls nonblank()`
- c0025 ..> c0025: `validate() calls nonblank()`
- c0025 ..> c0025: `validate() calls validate_workers()`
- c0025 ..> c0025: `validate_workers() calls nonblank()`
- c0025 ..> c0041: `connection_from_mapping() constructs FactoryError`
- c0025 ..> c0041: `from_mapping() constructs FactoryError`
- c0025 ..> c0041: `nonblank() constructs FactoryError`
- c0025 ..> c0041: `skill_paths() constructs FactoryError`
- c0025 ..> c0041: `validate() constructs FactoryError`
- c0025 ..> c0041: `validate_workers() constructs FactoryError`
- c0025 ..> c0044: `from_mapping() constructs RepositoryReference`
- c0025 ..> c0045: `from_mapping() constructs WorkSource`
- c0026 ..> c0004: `prepare_foreman() calls prepare()`
- c0026 ..> c0006: `check_foreman() calls check()`
- c0026 ..> c0006: `check_foreman() calls login()`
- c0026 ..> c0006: `prepare_foreman() calls install()`
- c0026 ..> c0006: `prepare_foreman() calls installation()`
- c0026 ..> c0006: `prepare_foreman() calls missing_executables()`
- c0026 ..> c0007: `_preflight() calls origin()`
- c0026 ..> c0007: `discover() calls discover()`
- c0026 ..> c0007: `inspect() calls origin()`
- c0026 ..> c0011: `initialise() calls save()`
- c0026 ..> c0011: `load_existing() calls load()`
- c0026 ..> c0019: `_ensure_label() calls create_label()`
- c0026 ..> c0019: `_preflight() calls check_access()`
- c0026 ..> c0019: `_preflight() calls list_labels()`
- c0026 ..> c0019: `_preflight() calls source_from_remote()`
- c0026 ..> c0019: `inspect() calls source_from_remote()`
- c0026 ..> c0023: `configure() constructs FactoryConfiguration`
- c0026 ..> c0023: `type in _preflight`
- c0026 ..> c0023: `type in check_foreman`
- c0026 ..> c0023: `type in configure`
- c0026 ..> c0023: `type in initialise`
- c0026 ..> c0023: `type in load_existing`
- c0026 ..> c0024: `_preflight() calls validate()`
- c0026 ..> c0024: `type in prepare_foreman`
- c0026 ..> c0025: `configure() calls unique_labels()`
- c0026 ..> c0025: `load_existing() calls unique_labels()`
- c0026 ..> c0026: `configure() calls inspect()`
- c0026 ..> c0026: `initialise() calls _ensure_label()`
- c0026 ..> c0026: `initialise() calls _preflight()`
- c0026 ..> c0027: `type in __init__`
- c0026 ..> c0028: `type in __init__`
- c0026 ..> c0030: `type in __init__`
- c0026 ..> c0033: `type in __init__`
- c0026 ..> c0041: `_preflight() constructs FactoryError`
- c0026 ..> c0041: `initialise() constructs FactoryError`
- c0026 ..> c0041: `inspect() constructs FactoryError`
- c0026 ..> c0041: `load_existing() constructs FactoryError`
- c0026 ..> c0041: `prepare_foreman() constructs FactoryError`
- c0026 ..> c0043: `_ensure_label() constructs Label`
- c0026 ..> c0043: `type in _preflight`
- c0026 ..> c0044: `inspect() constructs RepositoryReference`
- c0026 ..> c0044: `type in inspect`
- c0026 ..> c0045: `type in _ensure_label`
- c0026 ..> c0045: `type in _preflight`
- c0026 ..> c0046: `type in __init__`
- c0027 ..> c0023: `type in load`
- c0027 ..> c0023: `type in save`
- c0028 ..> c0023: `type in prepare_roles`
- c0028 ..> c0023: `type in record_completion`
- c0028 ..> c0024: `type in check`
- c0028 ..> c0024: `type in create_project`
- c0028 ..> c0024: `type in list_models`
- c0028 ..> c0024: `type in login`
- c0028 ..> c0024: `type in missing_executables`
- c0028 ..> c0024: `type in prepare`
- c0028 ..> c0024: `type in projects`
- c0028 ..> c0024: `type in uses_browser_login`
- c0033 ..> c0045: `type in source_from_remote`
- c0035 ..> c0006: `check() calls check()`
- c0035 ..> c0008: `_ensure_mapping() calls ensure()`
- c0035 ..> c0008: `_ensure_mapping() calls verify_removed()`
- c0035 ..> c0018: `_issue_plan() calls create_plan()`
- c0035 ..> c0018: `_issue_plan() calls get_plan()`
- c0035 ..> c0018: `_issue_plan() calls plans()`
- c0035 ..> c0018: `_ownership() calls tasks()`
- c0035 ..> c0018: `prepare() calls create_task()`
- c0035 ..> c0018: `prepare() calls update_plan()`
- c0035 ..> c0018: `unfinished() calls get_plan()`
- c0035 ..> c0018: `unfinished() calls plans()`
- c0035 ..> c0023: `type in __init__`
- c0035 ..> c0031: `type in __init__`
- c0035 ..> c0034: `type in __init__`
- c0035 ..> c0035: `_ensure_worktrees() calls _ensure_mapping()`
- c0035 ..> c0035: `prepare() calls _context()`
- c0035 ..> c0035: `prepare() calls _ensure_worktrees()`
- c0035 ..> c0035: `prepare() calls _issue_plan()`
- c0035 ..> c0035: `prepare() calls _ownership()`
- c0035 ..> c0035: `unfinished() calls _context()`
- c0035 ..> c0035: `unfinished() calls _is_unfinished_factory_plan()`
- c0035 ..> c0036: `_ensure_mapping() calls _cleanup_state()`
- c0035 ..> c0041: `_context() constructs FactoryError`
- c0035 ..> c0041: `_ensure_mapping() constructs FactoryError`
- c0035 ..> c0041: `_ensure_worktrees() constructs FactoryError`
- c0035 ..> c0041: `_issue_plan() constructs FactoryError`
- c0035 ..> c0041: `_ownership() constructs FactoryError`
- c0035 ..> c0041: `prepare() constructs FactoryError`
- c0035 ..> c0041: `unfinished() constructs FactoryError`
- c0035 ..> c0042: `type in _issue_plan`
- c0035 ..> c0042: `type in prepare`
- c0035 ..> c0042: `type in unfinished`
- c0035 ..> c0042: `unfinished() constructs Issue`
- c0035 ..> c0045: `unfinished() constructs WorkSource`
- c0036 ..> c0041: `_cleanup_state() constructs FactoryError`
- c0037 ..> c0002: `_notify_issues() calls send()`
- c0037 ..> c0002: `_watch() calls close()`
- c0037 ..> c0002: `_watch() calls start()`
- c0037 ..> c0002: `_watch() calls wait()`
- c0037 ..> c0002: `run() calls startup_hint()`
- c0037 ..> c0004: `_notify_issues() calls prepare()`
- c0037 ..> c0006: `run() calls check()`
- c0037 ..> c0013: `run() calls hold()`
- c0037 ..> c0019: `_read_issues() calls list_issues()`
- c0037 ..> c0023: `type in _watch`
- c0037 ..> c0023: `type in run`
- c0037 ..> c0029: `type in __init__`
- c0037 ..> c0032: `type in __init__`
- c0037 ..> c0035: `_watch() calls unfinished()`
- c0037 ..> c0035: `type in __init__`
- c0037 ..> c0037: `_watch() calls _notify_issues()`
- c0037 ..> c0037: `_watch() calls _read_issues()`
- c0037 ..> c0037: `run() calls _watch()`
- c0037 ..> c0042: `type in _notify_issues`
- c0037 ..> c0042: `type in _read_issues`
- c0037 ..> c0045: `_watch() constructs WorkSource`
- c0037 ..> c0045: `type in _read_issues`
- c0037 ..> c0046: `type in __init__`
- c0038 ..> c0002: `build_watcher() constructs AgentShellTerminal`
- c0038 ..> c0004: `build_watcher() calls validate_guidance()`
- c0038 ..> c0006: `build_initialiser() constructs ForemanProfile`
- c0038 ..> c0006: `build_watcher() calls launch_resources()`
- c0038 ..> c0006: `build_watcher() calls pi_home()`
- c0038 ..> c0006: `build_watcher() calls validate_completion()`
- c0038 ..> c0006: `build_watcher() calls validate_setup()`
- c0038 ..> c0006: `build_watcher() constructs ForemanProfile`
- c0038 ..> c0007: `build_initialiser() constructs GitRepositories`
- c0038 ..> c0008: `build_watcher() constructs GitWorktrees`
- c0038 ..> c0011: `build_initialiser() constructs TomlConfigurationStore`
- c0038 ..> c0013: `build_watcher() constructs WorkspaceWatchLease`
- c0038 ..> c0017: `build_watcher() calls role_environment()`
- c0038 ..> c0018: `build_watcher() constructs ForgetfulPlanning`
- c0038 ..> c0019: `build_initialiser() constructs GitHubWorkTracking`
- c0038 ..> c0019: `build_watcher() calls source_from_remote()`
- c0038 ..> c0019: `build_watcher() constructs GitHubWorkTracking`
- c0038 ..> c0023: `type in build_watcher`
- c0038 ..> c0026: `build_initialiser() constructs InitialiseFactory`
- c0038 ..> c0026: `type in build_initialiser`
- c0038 ..> c0035: `build_watcher() constructs ScaffoldIssue`
- c0038 ..> c0037: `build_watcher() constructs WatchFactory`
- c0038 ..> c0037: `type in build_watcher`
- c0038 ..> c0041: `build_watcher() constructs FactoryError`
- c0039 ..> c0006: `_complete_setup() calls record_completion()`
- c0039 ..> c0006: `_complete_setup() calls uses_browser_login()`
- c0039 ..> c0006: `_initialise() calls begin_setup()`
- c0039 ..> c0006: `_initialise() calls choose_pi_home()`
- c0039 ..> c0006: `_select_model() calls list_models()`
- c0039 ..> c0006: `_select_project() calls create_project()`
- c0039 ..> c0006: `_select_project() calls projects()`
- c0039 ..> c0007: `select_repositories() calls discover()`
- c0039 ..> c0012: `_select_model() calls quote()`
- c0039 ..> c0023: `type in _complete_setup`
- c0039 ..> c0023: `type in _configure_new_factory`
- c0039 ..> c0023: `type in _owner_configuration`
- c0039 ..> c0023: `type in _worker_configuration`
- c0039 ..> c0024: `_connection() calls validate()`
- c0039 ..> c0024: `_connection() constructs ForgetfulConnection`
- c0039 ..> c0024: `type in _check_existing_connection`
- c0039 ..> c0024: `type in _configure_new_factory`
- c0039 ..> c0024: `type in _connection`
- c0039 ..> c0024: `type in _select_project`
- c0039 ..> c0026: `_complete_setup() calls check_foreman()`
- c0039 ..> c0026: `_configure_new_factory() calls configure()`
- c0039 ..> c0026: `_configure_new_factory() calls inspect()`
- c0039 ..> c0026: `_initialise() calls initialise()`
- c0039 ..> c0026: `_initialise() calls load_existing()`
- c0039 ..> c0026: `_prepare_foreman() calls prepare_foreman()`
- c0039 ..> c0026: `type in _complete_setup`
- c0039 ..> c0026: `type in _configure_new_factory`
- c0039 ..> c0026: `type in _select_project`
- c0039 ..> c0026: `type in select_repositories`
- c0039 ..> c0037: `_watch() calls run()`
- c0039 ..> c0038: `_initialise() calls build_initialiser()`
- c0039 ..> c0038: `_watch() calls build_watcher()`
- c0039 ..> c0039: `_configure_new_factory() calls _prepare_foreman()`
- c0039 ..> c0039: `_configure_new_factory() calls _select_model()`
- c0039 ..> c0039: `_configure_new_factory() calls select_repositories()`
- c0039 ..> c0039: `_connection() calls _check_existing_connection()`
- c0039 ..> c0039: `_initialise() calls _complete_setup()`
- c0039 ..> c0039: `_initialise() calls _configure_new_factory()`
- c0039 ..> c0039: `_initialise() calls _confirm_pi_home()`
- c0039 ..> c0039: `_initialise() calls _connection()`
- c0039 ..> c0039: `_initialise() calls _owner_configuration()`
- c0039 ..> c0039: `_initialise() calls _worker_configuration()`
- c0039 ..> c0039: `_print_models() calls _safe_diagnostic()`
- c0039 ..> c0039: `_prompt_worker() calls _safe_diagnostic()`
- c0039 ..> c0039: `_prompt_workers() calls _prompt_worker()`
- c0039 ..> c0039: `_select_model() calls _print_models()`
- c0039 ..> c0039: `_select_project() calls _listed_project_id()`
- c0039 ..> c0039: `_select_project() calls _safe_diagnostic()`
- c0039 ..> c0039: `_watch() calls _choose_existing()`
- c0039 ..> c0039: `_watch() calls _safe_diagnostic()`
- c0039 ..> c0039: `_worker_configuration() calls _prompt_workers()`
- c0039 ..> c0039: `_worker_configuration() calls _worker_arguments()`
- c0039 ..> c0039: `main() calls _initialise()`
- c0039 ..> c0039: `main() calls _parse_arguments()`
- c0039 ..> c0039: `main() calls _safe_diagnostic()`
- c0039 ..> c0039: `main() calls _watch()`
- c0039 ..> c0040: `_watch() calls load_configuration()`
- c0039 ..> c0041: `_check_existing_connection() constructs FactoryError`
- c0039 ..> c0041: `_choose_existing() constructs FactoryError`
- c0039 ..> c0041: `_configure_new_factory() constructs FactoryError`
- c0039 ..> c0041: `_install_missing() constructs FactoryError`
- c0039 ..> c0041: `_listed_project_id() constructs FactoryError`
- c0039 ..> c0041: `_owner_configuration() constructs FactoryError`
- c0039 ..> c0041: `_prompt_worker() constructs FactoryError`
- c0039 ..> c0041: `_prompt_workers() constructs FactoryError`
- c0039 ..> c0041: `_select_model() constructs FactoryError`
- c0039 ..> c0041: `_select_project() constructs FactoryError`
- c0039 ..> c0041: `_watch() constructs FactoryError`
- c0039 ..> c0041: `_worker_configuration() constructs FactoryError`
- c0039 ..> c0041: `main() constructs FactoryError`
- c0039 ..> c0041: `select_repositories() constructs FactoryError`
- c0040 ..> c0011: `load_configuration() calls load()`
- c0040 ..> c0011: `load_configuration() constructs TomlConfigurationStore`
- c0040 ..> c0023: `type in load_configuration`
- c0040 ..> c0041: `load_configuration() constructs FactoryError`
- c0042 --> c0045: `field source`
- c0044 --> c0045: `field work_source`
- c0046 ..> c0042: `type in list_issues`
- c0046 ..> c0043: `type in create_label`
- c0046 ..> c0043: `type in list_labels`
- c0046 ..> c0045: `type in check_access`
- c0046 ..> c0045: `type in create_label`
- c0046 ..> c0045: `type in list_issues`
- c0046 ..> c0045: `type in list_labels`

## Type key

- Type1: `dict[str, str] | None`
- Type2: `dict | None`
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
- Type28: `str | Path`

## Signature key

- Signature1: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None) unknown`
- Signature2: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature3: `-__init__(workspace: Path, connection: ForgetfulConnection, execution_enabled: bool)
  unknown`
- Signature4: `-__init__(tracking: WorkTrackingService, storage: ConfigurationStore, repositories:
  LocalRepositories, sources: WorkSourceResolver, profile: ForemanProfile) unknown`
- Signature5: `+configure(paths: list[Path], labels: list[str], model: str, effort: str)
  FactoryConfiguration`
- Signature6: `-__init__(planning: Planning, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration) unknown`
- Signature7: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, lease:
  WatchLease, scaffold: ScaffoldIssue) unknown`
- Signature8: `+run(config: FactoryConfiguration, workspace: Path, interval: float, choose_existing:
  Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature9: `-_watch(config: FactoryConfiguration, workspace: Path, interval: float, existing:
  bool, report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature10: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  FactoryConfiguration`
- Signature11: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature12: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature13: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature14: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature15: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature16: `-_owner_configuration(args: argparse.Namespace, config: FactoryConfiguration,
  existing: bool) FactoryConfiguration`
- Signature17: `-_worker_configuration(args: argparse.Namespace, config: FactoryConfiguration,
  existing: bool, discover_models: unknown) FactoryConfiguration`
- Signature18: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool) None`

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
