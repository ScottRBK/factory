# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 45 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 991. Type relationships removed: 13.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_architecture.py`: 12 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_configuration.py`: 12 source occurrences (test-path).
- `tests/test_init.py`: 43 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 18 source occurrences (test-path).
- `tests/test_native_roles.py`: 3 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_planning_setup.py`: 13 source occurrences (test-path).
- `tests/test_planning_watch.py`: 26 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_setup_completion.py`: 30 source occurrences (test-path).
- `tests/test_shared_pi.py`: 21 source occurrences (test-path).
- `tests/test_watch.py`: 51 source occurrences (test-path).
- `tests/test_watch_lock.py`: 4 source occurrences (test-path).

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
        +directory: unknown
        +validate_depth(pi_home: str) None
        +prepare(config: FactoryConfiguration) None
        -_role(name: str, config: FactoryConfiguration) dict
        -_selection_files() dict
        +selection(config: FactoryConfiguration) dict
    }
    class c0005["src/forgetful_factory/adapters/filesystem/coordinator_profiles.py"] {
        <<module>>
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
        +missing_executables(connection: ForgetfulConnection) list[str]
        +validate_setup(connection: ForgetfulConnection) None
        +validate_bundled_resources() None
        +installation(command: str) Type3
        +install(command: str) None
        -_install_resources() None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection) str
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        -_protect_runtime() None
        +prepare(connection: ForgetfulConnection) None
        +prepare_roles(config: unknown) None
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +require_pi_home(directory: str) None
        +pi_home() str
        +list_models(connection: ForgetfulConnection) list[str]
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
        +load() Type5
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
    class c0014["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0015["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +role: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type6
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection) None
    }
    class c0016["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature2)
        -_catalog_tools(catalog: object) dict
    }
    class c0017["ForgetfulPlanning"] {
        <<class>>
        -__init__(workspace: Path, connection: ForgetfulConnection) unknown
        +cli: unknown
        +connection: unknown
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
    class c0018["GitHubWorkTracking"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type7
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type9) Type8
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0019["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +runtime: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type1) Type6
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type1) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0020["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type10) str
        +runtime_ready(runtime: Path, inputs: Type10, probe: str) bool
    }
    class c0021["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        +run_owned(args: list[str], cwd: Path, env: Type6, login: bool, timeout: Type11) str
    }
    class c0022["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type9
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +repository: Type12
        +forgetful: Type13
        +feature_owner_agent_model: Type3
        +feature_owner_agent_effort: Type3
        +feature_owner_agent_harness: str
        +grill_me_skill: Type3
    }
    class c0023["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type3
        +server: Type3
        +project_id: Type14
        +validate() None
        -_validate_server() None
    }
    class c0024["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type13
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type9
    }
    class c0025["InitialiseFactory"] {
        <<class>>
        -__init__(Signature3)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type15, confirm: Type16) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type17, labels: Type18, model: Type3, effort: Type3) Type5
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type19
        +configure(Signature4)
        -_preflight(config: FactoryConfiguration) Type20
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type21, save: bool) list[str]
    }
    class c0026["ConfigurationStore"] {
        <<class>>
        +load() Type5
        +save(configuration: FactoryConfiguration) None
    }
    class c0027["ForemanProfile"] {
        <<class>>
        +prepare_roles(config: FactoryConfiguration) None
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +prepare(connection: ForgetfulConnection) None
        +uses_browser_login(connection: ForgetfulConnection) bool
        +login(connection: ForgetfulConnection) None
        +check(connection: ForgetfulConnection) str
        +missing_executables(connection: ForgetfulConnection) list[str]
        +installation(command: str) Type3
        +install(command: str) None
        +choose_pi_home(requested: Type3, confirm: unknown) str
        +list_models(connection: ForgetfulConnection) list[str]
        +record_completion(config: FactoryConfiguration) None
        +begin_setup() None
    }
    class c0028["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start(cwd: str, model: str, effort: str) None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0029["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0030["Planning"] {
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
    class c0031["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0032["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0033["Worktrees"] {
        <<class>>
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
    }
    class c0034["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature5)
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
    }
    class c0035["WatchFactory"] {
        <<class>>
        -__init__(Signature6)
        +tracking: unknown
        +terminal: unknown
        +lease: unknown
        +scaffold: unknown
        +run(Signature7)
        -_watch(Signature8)
        -_notify_issues(issues: Type8, seen: Type6, report: Type23, recovered: bool) None
        -_read_issues(source: WorkSource, labels: Type9, report_error: Type23) Type24
    }
    class c0036["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path) InitialiseFactory
        +build_watcher(python: str, config: FactoryConfiguration, workspace: Path) WatchFactory
    }
    class c0037["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature9)
        -_check_existing_connection(Signature10)
        -_connection(Signature11)
        -_prepare_foreman(application: unknown, connection: unknown, args: unknown) unknown
        -_print_models(models: list[str]) None
        -_select_model(Signature12)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_watch(args: argparse.Namespace, workspace: Path) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature13)
        -_owner_configuration(Signature14)
        -_initialise(args: argparse.Namespace, workspace: Path) int
        +main() int
    }
    class c0038["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type25) FactoryConfiguration
    }
    class c0039["FactoryError"] {
        <<class>>
    }
    class c0040["Issue"] {
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
    class c0041["Label"] {
        <<class>>
        +name: str
    }
    class c0042["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0043["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0044["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type7
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type9) Type8
    }
    c0000 ..> c0000 : 4 relationships (see list)
    c0000 ..> c0002 : 4 relationships (see list)
    c0000 ..> c0017 : 3 relationships (see list)
    c0001 ..> c0006 : main() calls list_models()
    c0002 ..> c0002 : 5 relationships (see list)
    c0002 ..> c0028 : close() calls close()
    c0002 ..> c0039 : 4 relationships (see list)
    c0003 ..> c0035 : run_command() calls run()
    c0003 ..> c0039 : run_command() constructs FactoryError
    c0004 ..> c0004 : 3 relationships (see list)
    c0004 ..> c0005 : 2 relationships (see list)
    c0004 ..> c0010 : 2 relationships (see list)
    c0004 ..> c0022 : 3 relationships (see list)
    c0004 ..> c0039 : 3 relationships (see list)
    c0006 ..> c0004 : 7 relationships (see list)
    c0006 ..> c0006 : 23 relationships (see list)
    c0006 ..> c0010 : 7 relationships (see list)
    c0006 ..> c0012 : require_pi_home() calls quote()
    c0006 ..> c0014 : uses_browser_login() calls uses_browser_login()
    c0006 ..> c0015 : 8 relationships (see list)
    c0006 ..> c0016 : list_models() calls role_environment()
    c0006 ..> c0019 : 6 relationships (see list)
    c0006 ..> c0020 : 3 relationships (see list)
    c0006 ..> c0021 : list_models() calls run_owned()
    c0006 ..> c0022 : 3 relationships (see list)
    c0006 ..> c0023 : 9 relationships (see list)
    c0006 ..> c0039 : 12 relationships (see list)
    c0007 ..> c0003 : origin() calls run_command()
    c0007 ..> c0039 : origin() constructs FactoryError
    c0008 ..> c0003 : ensure() calls run_command()
    c0008 ..> c0009 : ensure() calls _worktree_entries()
    c0008 ..> c0039 : ensure() constructs FactoryError
    c0010 ..> c0002 : _generated_parent() calls close()
    c0010 ..> c0010 : 6 relationships (see list)
    c0010 ..> c0011 : read_generated_json() calls load()
    c0010 ..> c0039 : 4 relationships (see list)
    c0011 ..> c0002 : 2 relationships (see list)
    c0011 ..> c0012 : save() calls quote()
    c0011 ..> c0022 : 2 relationships (see list)
    c0011 ..> c0024 : load() calls from_mapping()
    c0011 ..> c0026 : load() calls load()
    c0011 ..> c0039 : 2 relationships (see list)
    c0013 ..> c0002 : hold() calls close()
    c0013 ..> c0039 : hold() constructs FactoryError
    c0014 ..> c0023 : type in uses_browser_login
    c0015 ..> c0015 : 7 relationships (see list)
    c0015 ..> c0016 : 2 relationships (see list)
    c0015 ..> c0021 : 2 relationships (see list)
    c0015 ..> c0023 : 7 relationships (see list)
    c0015 ..> c0039 : 5 relationships (see list)
    c0016 ..> c0020 : role_environment() calls executable_path()
    c0016 ..> c0023 : type in role_environment
    c0017 ..> c0006 : check() calls check()
    c0017 ..> c0015 : 2 relationships (see list)
    c0017 ..> c0017 : 9 relationships (see list)
    c0017 ..> c0023 : type in __init__
    c0017 ..> c0039 : _rows() constructs FactoryError
    c0018 ..> c0003 : _api() calls run_command()
    c0018 ..> c0018 : 5 relationships (see list)
    c0018 ..> c0039 : 7 relationships (see list)
    c0018 ..> c0040 : 2 relationships (see list)
    c0018 ..> c0041 : 3 relationships (see list)
    c0018 ..> c0043 : 8 relationships (see list)
    c0019 ..> c0010 : install() calls write_new()
    c0019 ..> c0019 : 15 relationships (see list)
    c0019 ..> c0020 : 3 relationships (see list)
    c0019 ..> c0021 : 4 relationships (see list)
    c0019 ..> c0039 : 6 relationships (see list)
    c0020 ..> c0020 : runtime_ready() calls sync_fingerprint()
    c0020 ..> c0021 : runtime_ready() calls run_owned()
    c0021 ..> c0039 : run_owned() constructs FactoryError
    c0022 --> c0023 : field forgetful
    c0022 --> c0042 : field repository
    c0023 ..> c0024 : 2 relationships (see list)
    c0023 ..> c0039 : _validate_server() constructs FactoryError
    c0024 ..> c0022 : 3 relationships (see list)
    c0024 ..> c0023 : 3 relationships (see list)
    c0024 ..> c0024 : 5 relationships (see list)
    c0024 ..> c0039 : 4 relationships (see list)
    c0024 ..> c0042 : from_mapping() constructs RepositoryReference
    c0024 ..> c0043 : from_mapping() constructs WorkSource
    c0025 ..> c0004 : prepare_foreman() calls prepare()
    c0025 ..> c0006 : 5 relationships (see list)
    c0025 ..> c0007 : 3 relationships (see list)
    c0025 ..> c0011 : 2 relationships (see list)
    c0025 ..> c0018 : 5 relationships (see list)
    c0025 ..> c0022 : 6 relationships (see list)
    c0025 ..> c0023 : 2 relationships (see list)
    c0025 ..> c0024 : 2 relationships (see list)
    c0025 ..> c0025 : 3 relationships (see list)
    c0025 ..> c0026 : type in __init__
    c0025 ..> c0027 : type in __init__
    c0025 ..> c0029 : type in __init__
    c0025 ..> c0032 : type in __init__
    c0025 ..> c0039 : 5 relationships (see list)
    c0025 ..> c0041 : 2 relationships (see list)
    c0025 ..> c0042 : 2 relationships (see list)
    c0025 ..> c0043 : 2 relationships (see list)
    c0025 ..> c0044 : type in __init__
    c0026 ..> c0022 : 2 relationships (see list)
    c0027 ..> c0022 : 2 relationships (see list)
    c0027 ..> c0023 : 8 relationships (see list)
    c0032 ..> c0043 : type in source_from_remote
    c0034 ..> c0006 : check() calls check()
    c0034 ..> c0008 : _ensure_worktrees() calls ensure()
    c0034 ..> c0017 : 8 relationships (see list)
    c0034 ..> c0022 : type in __init__
    c0034 ..> c0030 : type in __init__
    c0034 ..> c0033 : type in __init__
    c0034 ..> c0034 : 6 relationships (see list)
    c0034 ..> c0039 : 6 relationships (see list)
    c0034 ..> c0040 : 4 relationships (see list)
    c0034 ..> c0043 : unfinished() constructs WorkSource
    c0035 ..> c0002 : 5 relationships (see list)
    c0035 ..> c0004 : _notify_issues() calls prepare()
    c0035 ..> c0006 : run() calls check()
    c0035 ..> c0013 : run() calls hold()
    c0035 ..> c0018 : _read_issues() calls list_issues()
    c0035 ..> c0022 : 2 relationships (see list)
    c0035 ..> c0028 : type in __init__
    c0035 ..> c0031 : type in __init__
    c0035 ..> c0034 : 2 relationships (see list)
    c0035 ..> c0035 : 3 relationships (see list)
    c0035 ..> c0040 : 2 relationships (see list)
    c0035 ..> c0043 : 2 relationships (see list)
    c0035 ..> c0044 : type in __init__
    c0036 ..> c0002 : build_watcher() constructs AgentShellTerminal
    c0036 ..> c0006 : 7 relationships (see list)
    c0036 ..> c0007 : build_initialiser() constructs GitRepositories
    c0036 ..> c0008 : build_watcher() constructs GitWorktrees
    c0036 ..> c0011 : build_initialiser() constructs TomlConfigurationStore
    c0036 ..> c0013 : build_watcher() constructs WorkspaceWatchLease
    c0036 ..> c0016 : build_watcher() calls role_environment()
    c0036 ..> c0017 : build_watcher() constructs ForgetfulPlanning
    c0036 ..> c0018 : 3 relationships (see list)
    c0036 ..> c0022 : type in build_watcher
    c0036 ..> c0025 : 2 relationships (see list)
    c0036 ..> c0034 : build_watcher() constructs ScaffoldIssue
    c0036 ..> c0035 : 2 relationships (see list)
    c0036 ..> c0039 : build_watcher() constructs FactoryError
    c0037 ..> c0006 : 7 relationships (see list)
    c0037 ..> c0007 : select_repositories() calls discover()
    c0037 ..> c0012 : _select_model() calls quote()
    c0037 ..> c0022 : 2 relationships (see list)
    c0037 ..> c0023 : 6 relationships (see list)
    c0037 ..> c0025 : 9 relationships (see list)
    c0037 ..> c0035 : _watch() calls run()
    c0037 ..> c0036 : 2 relationships (see list)
    c0037 ..> c0037 : 18 relationships (see list)
    c0037 ..> c0038 : _watch() calls load_configuration()
    c0037 ..> c0039 : 11 relationships (see list)
    c0038 ..> c0011 : 2 relationships (see list)
    c0038 ..> c0022 : type in load_configuration
    c0038 ..> c0039 : load_configuration() constructs FactoryError
    c0040 --> c0043 : field source
    c0042 --> c0043 : field work_source
    c0044 ..> c0040 : type in list_issues
    c0044 ..> c0041 : 2 relationships (see list)
    c0044 ..> c0043 : 4 relationships (see list)
```

## Source index

- c0000: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0001: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0002: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:12
- c0003: `src/forgetful_factory/adapters/command.py` — `src/forgetful_factory/adapters/command.py`:1
- c0004: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:39
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
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:17
- c0012: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0013: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0014: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0015: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:52
- c0016: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0017: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:8
- c0018: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0019: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:52
- c0020: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0021: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0022: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:80
- c0023: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0024: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0025: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0026: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0027: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:6
- c0028: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0029: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0030: `Planning` — `src/forgetful_factory/application/ports/planning.py`:4
- c0031: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0032: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0033: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:4
- c0034: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:11
- c0035: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:13
- c0036: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0037: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0038: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0039: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0040: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0041: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0042: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0043: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0044: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `control() calls serve()`
- c0000 ..> c0000: `interact() calls ready()`
- c0000 ..> c0000: `main() calls control()`
- c0000 ..> c0000: `serve() calls interact()`
- c0000 ..> c0002: `control() calls close()`
- c0000 ..> c0002: `control() calls wait()`
- c0000 ..> c0002: `serve() calls close()`
- c0000 ..> c0002: `serve() calls wait()`
- c0000 ..> c0017: `control() calls create_task()`
- c0000 ..> c0017: `main() calls create_task()`
- c0000 ..> c0017: `serve() calls create_task()`
- c0001 ..> c0006: `main() calls list_models()`
- c0002 ..> c0002: `send() calls _read()`
- c0002 ..> c0002: `send() calls _write()`
- c0002 ..> c0002: `start() calls _read()`
- c0002 ..> c0002: `start() calls _write()`
- c0002 ..> c0002: `wait() calls _read()`
- c0002 ..> c0028: `close() calls close()`
- c0002 ..> c0039: `_read() constructs FactoryError`
- c0002 ..> c0039: `_write() constructs FactoryError`
- c0002 ..> c0039: `close() constructs FactoryError`
- c0002 ..> c0039: `start() constructs FactoryError`
- c0003 ..> c0035: `run_command() calls run()`
- c0003 ..> c0039: `run_command() constructs FactoryError`
- c0004 ..> c0004: `prepare() calls _role()`
- c0004 ..> c0004: `selection() calls _role()`
- c0004 ..> c0004: `selection() calls _selection_files()`
- c0004 ..> c0005: `_role() calls _local_resource_paths()`
- c0004 ..> c0005: `_role() calls selected_resources()`
- c0004 ..> c0010: `prepare() calls write_json()`
- c0004 ..> c0010: `prepare() calls write_new()`
- c0004 ..> c0022: `type in _role`
- c0004 ..> c0022: `type in prepare`
- c0004 ..> c0022: `type in selection`
- c0004 ..> c0039: `prepare() constructs FactoryError`
- c0004 ..> c0039: `selection() constructs FactoryError`
- c0004 ..> c0039: `validate_depth() constructs FactoryError`
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
- c0006 ..> c0010: `_install_resources() calls write_new()`
- c0006 ..> c0010: `_protect_runtime() calls write_new()`
- c0006 ..> c0010: `begin_setup() calls remove_generated()`
- c0006 ..> c0010: `prepare() calls write_json()`
- c0006 ..> c0010: `prepare() calls write_new()`
- c0006 ..> c0010: `record_completion() calls replace_generated_json()`
- c0006 ..> c0010: `validate_completion() calls read_generated_json()`
- c0006 ..> c0012: `require_pi_home() calls quote()`
- c0006 ..> c0014: `uses_browser_login() calls uses_browser_login()`
- c0006 ..> c0015: `check() calls check()`
- c0006 ..> c0015: `check() constructs AgentForgetfulConnection`
- c0006 ..> c0015: `create_project() calls create_project()`
- c0006 ..> c0015: `create_project() constructs AgentForgetfulConnection`
- c0006 ..> c0015: `login() calls login()`
- c0006 ..> c0015: `login() constructs AgentForgetfulConnection`
- c0006 ..> c0015: `projects() calls projects()`
- c0006 ..> c0015: `projects() constructs AgentForgetfulConnection`
- c0006 ..> c0016: `list_models() calls role_environment()`
- c0006 ..> c0019: `install() calls install()`
- c0006 ..> c0019: `install() constructs HostDependencies`
- c0006 ..> c0019: `installation() calls description()`
- c0006 ..> c0019: `installation() constructs HostDependencies`
- c0006 ..> c0019: `missing_executables() calls pi_ready()`
- c0006 ..> c0019: `missing_executables() constructs HostDependencies`
- c0006 ..> c0020: `missing_executables() calls executable_path()`
- c0006 ..> c0020: `missing_executables() calls runtime_ready()`
- c0006 ..> c0020: `require_pi_home() calls executable_path()`
- c0006 ..> c0021: `list_models() calls run_owned()`
- c0006 ..> c0022: `type in _selection`
- c0006 ..> c0022: `type in record_completion`
- c0006 ..> c0022: `type in validate_completion`
- c0006 ..> c0023: `type in check`
- c0006 ..> c0023: `type in create_project`
- c0006 ..> c0023: `type in list_models`
- c0006 ..> c0023: `type in login`
- c0006 ..> c0023: `type in missing_executables`
- c0006 ..> c0023: `type in prepare`
- c0006 ..> c0023: `type in projects`
- c0006 ..> c0023: `type in uses_browser_login`
- c0006 ..> c0023: `type in validate_setup`
- c0006 ..> c0039: `_install_resources() constructs FactoryError`
- c0006 ..> c0039: `_read_guidance() constructs FactoryError`
- c0006 ..> c0039: `choose_pi_home() constructs FactoryError`
- c0006 ..> c0039: `launch_resources() constructs FactoryError`
- c0006 ..> c0039: `list_models() constructs FactoryError`
- c0006 ..> c0039: `pi_home() constructs FactoryError`
- c0006 ..> c0039: `prepare_roles() constructs FactoryError`
- c0006 ..> c0039: `require_pi_home() constructs FactoryError`
- c0006 ..> c0039: `validate_bundled_resources() constructs FactoryError`
- c0006 ..> c0039: `validate_completion() constructs FactoryError`
- c0006 ..> c0039: `validate_guidance() constructs FactoryError`
- c0006 ..> c0039: `validate_setup() constructs FactoryError`
- c0007 ..> c0003: `origin() calls run_command()`
- c0007 ..> c0039: `origin() constructs FactoryError`
- c0008 ..> c0003: `ensure() calls run_command()`
- c0008 ..> c0009: `ensure() calls _worktree_entries()`
- c0008 ..> c0039: `ensure() constructs FactoryError`
- c0010 ..> c0002: `_generated_parent() calls close()`
- c0010 ..> c0010: `_generated_parent() calls check_real_path()`
- c0010 ..> c0010: `read_generated_json() calls _generated_parent()`
- c0010 ..> c0010: `remove_generated() calls _generated_parent()`
- c0010 ..> c0010: `replace_generated_json() calls _generated_parent()`
- c0010 ..> c0010: `write_json() calls write_new()`
- c0010 ..> c0010: `write_new() calls check_real_path()`
- c0010 ..> c0011: `read_generated_json() calls load()`
- c0010 ..> c0039: `_generated_parent() constructs FactoryError`
- c0010 ..> c0039: `check_real_path() constructs FactoryError`
- c0010 ..> c0039: `read_generated_json() constructs FactoryError`
- c0010 ..> c0039: `write_new() constructs FactoryError`
- c0011 ..> c0002: `load() calls close()`
- c0011 ..> c0002: `save() calls close()`
- c0011 ..> c0012: `save() calls quote()`
- c0011 ..> c0022: `type in load`
- c0011 ..> c0022: `type in save`
- c0011 ..> c0024: `load() calls from_mapping()`
- c0011 ..> c0026: `load() calls load()`
- c0011 ..> c0039: `load() constructs FactoryError`
- c0011 ..> c0039: `save() constructs FactoryError`
- c0013 ..> c0002: `hold() calls close()`
- c0013 ..> c0039: `hold() constructs FactoryError`
- c0014 ..> c0023: `type in uses_browser_login`
- c0015 ..> c0015: `call() calls command()`
- c0015 ..> c0015: `check() calls call()`
- c0015 ..> c0015: `check() calls command()`
- c0015 ..> c0015: `command() calls _environment()`
- c0015 ..> c0015: `create_project() calls call()`
- c0015 ..> c0015: `login() calls _environment()`
- c0015 ..> c0015: `projects() calls command()`
- c0015 ..> c0016: `_environment() calls role_environment()`
- c0015 ..> c0016: `check() calls _catalog_tools()`
- c0015 ..> c0021: `command() calls run_owned()`
- c0015 ..> c0021: `login() calls run_owned()`
- c0015 ..> c0023: `type in _environment`
- c0015 ..> c0023: `type in call`
- c0015 ..> c0023: `type in check`
- c0015 ..> c0023: `type in command`
- c0015 ..> c0023: `type in create_project`
- c0015 ..> c0023: `type in login`
- c0015 ..> c0023: `type in projects`
- c0015 ..> c0039: `check() constructs FactoryError`
- c0015 ..> c0039: `command() constructs FactoryError`
- c0015 ..> c0039: `create_project() constructs FactoryError`
- c0015 ..> c0039: `login() constructs FactoryError`
- c0015 ..> c0039: `projects() constructs FactoryError`
- c0016 ..> c0020: `role_environment() calls executable_path()`
- c0016 ..> c0023: `type in role_environment`
- c0017 ..> c0006: `check() calls check()`
- c0017 ..> c0015: `__init__() constructs AgentForgetfulConnection`
- c0017 ..> c0015: `_call() calls call()`
- c0017 ..> c0017: `create_plan() calls _call()`
- c0017 ..> c0017: `create_task() calls _call()`
- c0017 ..> c0017: `get_plan() calls _call()`
- c0017 ..> c0017: `plans() calls _call()`
- c0017 ..> c0017: `plans() calls _rows()`
- c0017 ..> c0017: `tasks() calls _call()`
- c0017 ..> c0017: `tasks() calls _rows()`
- c0017 ..> c0017: `update_plan() calls _call()`
- c0017 ..> c0017: `update_task() calls _call()`
- c0017 ..> c0023: `type in __init__`
- c0017 ..> c0039: `_rows() constructs FactoryError`
- c0018 ..> c0003: `_api() calls run_command()`
- c0018 ..> c0018: `check_access() calls _api()`
- c0018 ..> c0018: `create_label() calls _api()`
- c0018 ..> c0018: `list_issues() calls _api()`
- c0018 ..> c0018: `list_issues() calls _validate_issue()`
- c0018 ..> c0018: `list_labels() calls _api()`
- c0018 ..> c0039: `_api() constructs FactoryError`
- c0018 ..> c0039: `_validate_issue() constructs FactoryError`
- c0018 ..> c0039: `check_access() constructs FactoryError`
- c0018 ..> c0039: `create_label() constructs FactoryError`
- c0018 ..> c0039: `list_issues() constructs FactoryError`
- c0018 ..> c0039: `list_labels() constructs FactoryError`
- c0018 ..> c0039: `source_from_remote() constructs FactoryError`
- c0018 ..> c0040: `list_issues() constructs Issue`
- c0018 ..> c0040: `type in list_issues`
- c0018 ..> c0041: `list_labels() constructs Label`
- c0018 ..> c0041: `type in create_label`
- c0018 ..> c0041: `type in list_labels`
- c0018 ..> c0043: `source_from_remote() constructs WorkSource`
- c0018 ..> c0043: `type in _api`
- c0018 ..> c0043: `type in _validate_issue`
- c0018 ..> c0043: `type in check_access`
- c0018 ..> c0043: `type in create_label`
- c0018 ..> c0043: `type in list_issues`
- c0018 ..> c0043: `type in list_labels`
- c0018 ..> c0043: `type in source_from_remote`
- c0019 ..> c0010: `install() calls write_new()`
- c0019 ..> c0019: `_check_uv() calls _environment()`
- c0019 ..> c0019: `_forgetful_python() calls _check_uv()`
- c0019 ..> c0019: `_forgetful_python() calls _environment()`
- c0019 ..> c0019: `_install_role_runtime() calls _check_uv()`
- c0019 ..> c0019: `_install_role_runtime() calls _run()`
- c0019 ..> c0019: `_install_tmux() calls _run()`
- c0019 ..> c0019: `_run() calls _environment()`
- c0019 ..> c0019: `description() calls _forgetful_python()`
- c0019 ..> c0019: `description() calls _ubuntu_tmux()`
- c0019 ..> c0019: `install() calls _forgetful_python()`
- c0019 ..> c0019: `install() calls _install_role_runtime()`
- c0019 ..> c0019: `install() calls _install_tmux()`
- c0019 ..> c0019: `install() calls _run()`
- c0019 ..> c0019: `install() calls _ubuntu_tmux()`
- c0019 ..> c0019: `pi_ready() calls _environment()`
- c0019 ..> c0020: `_install_role_runtime() calls sync_fingerprint()`
- c0019 ..> c0020: `install() calls sync_fingerprint()`
- c0019 ..> c0020: `pi_ready() calls sync_fingerprint()`
- c0019 ..> c0021: `_check_uv() calls run_owned()`
- c0019 ..> c0021: `_forgetful_python() calls run_owned()`
- c0019 ..> c0021: `_run() calls run_owned()`
- c0019 ..> c0021: `pi_ready() calls run_owned()`
- c0019 ..> c0039: `_check_uv() constructs FactoryError`
- c0019 ..> c0039: `_forgetful_python() constructs FactoryError`
- c0019 ..> c0039: `_install_role_runtime() constructs FactoryError`
- c0019 ..> c0039: `_install_tmux() constructs FactoryError`
- c0019 ..> c0039: `_run() constructs FactoryError`
- c0019 ..> c0039: `install() constructs FactoryError`
- c0020 ..> c0020: `runtime_ready() calls sync_fingerprint()`
- c0020 ..> c0021: `runtime_ready() calls run_owned()`
- c0021 ..> c0039: `run_owned() constructs FactoryError`
- c0022 --> c0023: `field forgetful`
- c0022 --> c0042: `field repository`
- c0023 ..> c0024: `_validate_server() calls loopback_host()`
- c0023 ..> c0024: `_validate_server() calls nonblank()`
- c0023 ..> c0039: `_validate_server() constructs FactoryError`
- c0024 ..> c0022: `from_mapping() constructs FactoryConfiguration`
- c0024 ..> c0022: `type in from_mapping`
- c0024 ..> c0022: `type in validate`
- c0024 ..> c0023: `connection_from_mapping() constructs ForgetfulConnection`
- c0024 ..> c0023: `type in connection_from_mapping`
- c0024 ..> c0023: `validate() calls _validate_server()`
- c0024 ..> c0024: `connection_from_mapping() calls validate()`
- c0024 ..> c0024: `from_mapping() calls connection_from_mapping()`
- c0024 ..> c0024: `from_mapping() calls validate()`
- c0024 ..> c0024: `unique_labels() calls nonblank()`
- c0024 ..> c0024: `validate() calls nonblank()`
- c0024 ..> c0039: `connection_from_mapping() constructs FactoryError`
- c0024 ..> c0039: `from_mapping() constructs FactoryError`
- c0024 ..> c0039: `nonblank() constructs FactoryError`
- c0024 ..> c0039: `validate() constructs FactoryError`
- c0024 ..> c0042: `from_mapping() constructs RepositoryReference`
- c0024 ..> c0043: `from_mapping() constructs WorkSource`
- c0025 ..> c0004: `prepare_foreman() calls prepare()`
- c0025 ..> c0006: `check_foreman() calls check()`
- c0025 ..> c0006: `check_foreman() calls login()`
- c0025 ..> c0006: `prepare_foreman() calls install()`
- c0025 ..> c0006: `prepare_foreman() calls installation()`
- c0025 ..> c0006: `prepare_foreman() calls missing_executables()`
- c0025 ..> c0007: `_preflight() calls origin()`
- c0025 ..> c0007: `discover() calls discover()`
- c0025 ..> c0007: `inspect() calls origin()`
- c0025 ..> c0011: `initialise() calls save()`
- c0025 ..> c0011: `load_existing() calls load()`
- c0025 ..> c0018: `_ensure_label() calls create_label()`
- c0025 ..> c0018: `_preflight() calls check_access()`
- c0025 ..> c0018: `_preflight() calls list_labels()`
- c0025 ..> c0018: `_preflight() calls source_from_remote()`
- c0025 ..> c0018: `inspect() calls source_from_remote()`
- c0025 ..> c0022: `configure() constructs FactoryConfiguration`
- c0025 ..> c0022: `type in _preflight`
- c0025 ..> c0022: `type in check_foreman`
- c0025 ..> c0022: `type in configure`
- c0025 ..> c0022: `type in initialise`
- c0025 ..> c0022: `type in load_existing`
- c0025 ..> c0023: `_preflight() calls validate()`
- c0025 ..> c0023: `type in prepare_foreman`
- c0025 ..> c0024: `configure() calls unique_labels()`
- c0025 ..> c0024: `load_existing() calls unique_labels()`
- c0025 ..> c0025: `configure() calls inspect()`
- c0025 ..> c0025: `initialise() calls _ensure_label()`
- c0025 ..> c0025: `initialise() calls _preflight()`
- c0025 ..> c0026: `type in __init__`
- c0025 ..> c0027: `type in __init__`
- c0025 ..> c0029: `type in __init__`
- c0025 ..> c0032: `type in __init__`
- c0025 ..> c0039: `_preflight() constructs FactoryError`
- c0025 ..> c0039: `initialise() constructs FactoryError`
- c0025 ..> c0039: `inspect() constructs FactoryError`
- c0025 ..> c0039: `load_existing() constructs FactoryError`
- c0025 ..> c0039: `prepare_foreman() constructs FactoryError`
- c0025 ..> c0041: `_ensure_label() constructs Label`
- c0025 ..> c0041: `type in _preflight`
- c0025 ..> c0042: `inspect() constructs RepositoryReference`
- c0025 ..> c0042: `type in inspect`
- c0025 ..> c0043: `type in _ensure_label`
- c0025 ..> c0043: `type in _preflight`
- c0025 ..> c0044: `type in __init__`
- c0026 ..> c0022: `type in load`
- c0026 ..> c0022: `type in save`
- c0027 ..> c0022: `type in prepare_roles`
- c0027 ..> c0022: `type in record_completion`
- c0027 ..> c0023: `type in check`
- c0027 ..> c0023: `type in create_project`
- c0027 ..> c0023: `type in list_models`
- c0027 ..> c0023: `type in login`
- c0027 ..> c0023: `type in missing_executables`
- c0027 ..> c0023: `type in prepare`
- c0027 ..> c0023: `type in projects`
- c0027 ..> c0023: `type in uses_browser_login`
- c0032 ..> c0043: `type in source_from_remote`
- c0034 ..> c0006: `check() calls check()`
- c0034 ..> c0008: `_ensure_worktrees() calls ensure()`
- c0034 ..> c0017: `_issue_plan() calls create_plan()`
- c0034 ..> c0017: `_issue_plan() calls get_plan()`
- c0034 ..> c0017: `_issue_plan() calls plans()`
- c0034 ..> c0017: `_ownership() calls tasks()`
- c0034 ..> c0017: `prepare() calls create_task()`
- c0034 ..> c0017: `prepare() calls update_plan()`
- c0034 ..> c0017: `unfinished() calls get_plan()`
- c0034 ..> c0017: `unfinished() calls plans()`
- c0034 ..> c0022: `type in __init__`
- c0034 ..> c0030: `type in __init__`
- c0034 ..> c0033: `type in __init__`
- c0034 ..> c0034: `prepare() calls _context()`
- c0034 ..> c0034: `prepare() calls _ensure_worktrees()`
- c0034 ..> c0034: `prepare() calls _issue_plan()`
- c0034 ..> c0034: `prepare() calls _ownership()`
- c0034 ..> c0034: `unfinished() calls _context()`
- c0034 ..> c0034: `unfinished() calls _is_unfinished_factory_plan()`
- c0034 ..> c0039: `_context() constructs FactoryError`
- c0034 ..> c0039: `_ensure_worktrees() constructs FactoryError`
- c0034 ..> c0039: `_issue_plan() constructs FactoryError`
- c0034 ..> c0039: `_ownership() constructs FactoryError`
- c0034 ..> c0039: `prepare() constructs FactoryError`
- c0034 ..> c0039: `unfinished() constructs FactoryError`
- c0034 ..> c0040: `type in _issue_plan`
- c0034 ..> c0040: `type in prepare`
- c0034 ..> c0040: `type in unfinished`
- c0034 ..> c0040: `unfinished() constructs Issue`
- c0034 ..> c0043: `unfinished() constructs WorkSource`
- c0035 ..> c0002: `_notify_issues() calls send()`
- c0035 ..> c0002: `_watch() calls close()`
- c0035 ..> c0002: `_watch() calls start()`
- c0035 ..> c0002: `_watch() calls wait()`
- c0035 ..> c0002: `run() calls startup_hint()`
- c0035 ..> c0004: `_notify_issues() calls prepare()`
- c0035 ..> c0006: `run() calls check()`
- c0035 ..> c0013: `run() calls hold()`
- c0035 ..> c0018: `_read_issues() calls list_issues()`
- c0035 ..> c0022: `type in _watch`
- c0035 ..> c0022: `type in run`
- c0035 ..> c0028: `type in __init__`
- c0035 ..> c0031: `type in __init__`
- c0035 ..> c0034: `_watch() calls unfinished()`
- c0035 ..> c0034: `type in __init__`
- c0035 ..> c0035: `_watch() calls _notify_issues()`
- c0035 ..> c0035: `_watch() calls _read_issues()`
- c0035 ..> c0035: `run() calls _watch()`
- c0035 ..> c0040: `type in _notify_issues`
- c0035 ..> c0040: `type in _read_issues`
- c0035 ..> c0043: `_watch() constructs WorkSource`
- c0035 ..> c0043: `type in _read_issues`
- c0035 ..> c0044: `type in __init__`
- c0036 ..> c0002: `build_watcher() constructs AgentShellTerminal`
- c0036 ..> c0006: `build_initialiser() constructs ForemanProfile`
- c0036 ..> c0006: `build_watcher() calls launch_resources()`
- c0036 ..> c0006: `build_watcher() calls pi_home()`
- c0036 ..> c0006: `build_watcher() calls validate_completion()`
- c0036 ..> c0006: `build_watcher() calls validate_guidance()`
- c0036 ..> c0006: `build_watcher() calls validate_setup()`
- c0036 ..> c0006: `build_watcher() constructs ForemanProfile`
- c0036 ..> c0007: `build_initialiser() constructs GitRepositories`
- c0036 ..> c0008: `build_watcher() constructs GitWorktrees`
- c0036 ..> c0011: `build_initialiser() constructs TomlConfigurationStore`
- c0036 ..> c0013: `build_watcher() constructs WorkspaceWatchLease`
- c0036 ..> c0016: `build_watcher() calls role_environment()`
- c0036 ..> c0017: `build_watcher() constructs ForgetfulPlanning`
- c0036 ..> c0018: `build_initialiser() constructs GitHubWorkTracking`
- c0036 ..> c0018: `build_watcher() calls source_from_remote()`
- c0036 ..> c0018: `build_watcher() constructs GitHubWorkTracking`
- c0036 ..> c0022: `type in build_watcher`
- c0036 ..> c0025: `build_initialiser() constructs InitialiseFactory`
- c0036 ..> c0025: `type in build_initialiser`
- c0036 ..> c0034: `build_watcher() constructs ScaffoldIssue`
- c0036 ..> c0035: `build_watcher() constructs WatchFactory`
- c0036 ..> c0035: `type in build_watcher`
- c0036 ..> c0039: `build_watcher() constructs FactoryError`
- c0037 ..> c0006: `_initialise() calls begin_setup()`
- c0037 ..> c0006: `_initialise() calls choose_pi_home()`
- c0037 ..> c0006: `_initialise() calls record_completion()`
- c0037 ..> c0006: `_initialise() calls uses_browser_login()`
- c0037 ..> c0006: `_select_model() calls list_models()`
- c0037 ..> c0006: `_select_project() calls create_project()`
- c0037 ..> c0006: `_select_project() calls projects()`
- c0037 ..> c0007: `select_repositories() calls discover()`
- c0037 ..> c0012: `_select_model() calls quote()`
- c0037 ..> c0022: `type in _configure_new_factory`
- c0037 ..> c0022: `type in _owner_configuration`
- c0037 ..> c0023: `_connection() calls validate()`
- c0037 ..> c0023: `_connection() constructs ForgetfulConnection`
- c0037 ..> c0023: `type in _check_existing_connection`
- c0037 ..> c0023: `type in _configure_new_factory`
- c0037 ..> c0023: `type in _connection`
- c0037 ..> c0023: `type in _select_project`
- c0037 ..> c0025: `_configure_new_factory() calls configure()`
- c0037 ..> c0025: `_configure_new_factory() calls inspect()`
- c0037 ..> c0025: `_initialise() calls check_foreman()`
- c0037 ..> c0025: `_initialise() calls initialise()`
- c0037 ..> c0025: `_initialise() calls load_existing()`
- c0037 ..> c0025: `_prepare_foreman() calls prepare_foreman()`
- c0037 ..> c0025: `type in _configure_new_factory`
- c0037 ..> c0025: `type in _select_project`
- c0037 ..> c0025: `type in select_repositories`
- c0037 ..> c0035: `_watch() calls run()`
- c0037 ..> c0036: `_initialise() calls build_initialiser()`
- c0037 ..> c0036: `_watch() calls build_watcher()`
- c0037 ..> c0037: `_configure_new_factory() calls _prepare_foreman()`
- c0037 ..> c0037: `_configure_new_factory() calls _select_model()`
- c0037 ..> c0037: `_configure_new_factory() calls select_repositories()`
- c0037 ..> c0037: `_connection() calls _check_existing_connection()`
- c0037 ..> c0037: `_initialise() calls _configure_new_factory()`
- c0037 ..> c0037: `_initialise() calls _confirm_pi_home()`
- c0037 ..> c0037: `_initialise() calls _connection()`
- c0037 ..> c0037: `_initialise() calls _owner_configuration()`
- c0037 ..> c0037: `_print_models() calls _safe_diagnostic()`
- c0037 ..> c0037: `_select_model() calls _print_models()`
- c0037 ..> c0037: `_select_project() calls _listed_project_id()`
- c0037 ..> c0037: `_select_project() calls _safe_diagnostic()`
- c0037 ..> c0037: `_watch() calls _choose_existing()`
- c0037 ..> c0037: `_watch() calls _safe_diagnostic()`
- c0037 ..> c0037: `main() calls _initialise()`
- c0037 ..> c0037: `main() calls _parse_arguments()`
- c0037 ..> c0037: `main() calls _safe_diagnostic()`
- c0037 ..> c0037: `main() calls _watch()`
- c0037 ..> c0038: `_watch() calls load_configuration()`
- c0037 ..> c0039: `_check_existing_connection() constructs FactoryError`
- c0037 ..> c0039: `_choose_existing() constructs FactoryError`
- c0037 ..> c0039: `_configure_new_factory() constructs FactoryError`
- c0037 ..> c0039: `_install_missing() constructs FactoryError`
- c0037 ..> c0039: `_listed_project_id() constructs FactoryError`
- c0037 ..> c0039: `_owner_configuration() constructs FactoryError`
- c0037 ..> c0039: `_select_model() constructs FactoryError`
- c0037 ..> c0039: `_select_project() constructs FactoryError`
- c0037 ..> c0039: `_watch() constructs FactoryError`
- c0037 ..> c0039: `main() constructs FactoryError`
- c0037 ..> c0039: `select_repositories() constructs FactoryError`
- c0038 ..> c0011: `load_configuration() calls load()`
- c0038 ..> c0011: `load_configuration() constructs TomlConfigurationStore`
- c0038 ..> c0022: `type in load_configuration`
- c0038 ..> c0039: `load_configuration() constructs FactoryError`
- c0040 --> c0043: `field source`
- c0042 --> c0043: `field work_source`
- c0044 ..> c0040: `type in list_issues`
- c0044 ..> c0041: `type in create_label`
- c0044 ..> c0041: `type in list_labels`
- c0044 ..> c0043: `type in check_access`
- c0044 ..> c0043: `type in create_label`
- c0044 ..> c0043: `type in list_issues`
- c0044 ..> c0043: `type in list_labels`

## Type key

- Type1: `dict[str, str] | None`
- Type2: `dict | None`
- Type3: `str | None`
- Type4: `subprocess.Popen | None`
- Type5: `FactoryConfiguration | None`
- Type6: `dict[str, str]`
- Type7: `tuple[Label, ...]`
- Type8: `tuple[Issue, ...]`
- Type9: `tuple[str, ...]`
- Type10: `tuple[Path, ...]`
- Type11: `float | None`
- Type12: `tuple[RepositoryReference, ...]`
- Type13: `ForgetfulConnection | None`
- Type14: `int | None`
- Type15: `Callable[[list[str]], None]`
- Type16: `Callable[[str, str], bool]`
- Type17: `list[Path] | None`
- Type18: `list[str] | None`
- Type19: `dict[str, RepositoryReference]`
- Type20: `dict[WorkSource, tuple[Label, ...]]`
- Type21: `Callable[[], FactoryConfiguration | None]`
- Type22: `Callable[[], bool]`
- Type23: `Callable[[str], None]`
- Type24: `tuple[Issue, ...] | None`
- Type25: `str | Path`

## Signature key

- Signature1: `-__init__(python: str, environment: dict[str, str] | None, resources: dict | None,
  prompt: str | None, cwd: str | None) unknown`
- Signature2: `+role_environment(workspace: Path, connection: ForgetfulConnection, pi_home: str |
  None) dict[str, str]`
- Signature3: `-__init__(tracking: WorkTrackingService, storage: ConfigurationStore, repositories:
  LocalRepositories, sources: WorkSourceResolver, profile: ForemanProfile) unknown`
- Signature4: `+configure(paths: list[Path], labels: list[str], model: str, effort: str)
  FactoryConfiguration`
- Signature5: `-__init__(planning: Planning, worktrees: Worktrees, workspace: Path, config:
  FactoryConfiguration) unknown`
- Signature6: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, lease:
  WatchLease, scaffold: ScaffoldIssue) unknown`
- Signature7: `+run(config: FactoryConfiguration, workspace: Path, interval: float, choose_existing:
  Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature8: `-_watch(config: FactoryConfiguration, workspace: Path, interval: float, existing:
  bool, report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature9: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  FactoryConfiguration`
- Signature10: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature11: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature12: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature13: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature14: `-_owner_configuration(args: argparse.Namespace, config: FactoryConfiguration,
  existing: bool) FactoryConfiguration`

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
