# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 48 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 1323. Type relationships removed: 22.

- `tests/agentshell_support.py`: 2 source occurrences (test-path).
- `tests/profile_support.py`: 4 source occurrences (test-path).
- `tests/smoke_foreman.py`: 14 source occurrences (test-path).
- `tests/test_architecture.py`: 12 source occurrences (test-path).
- `tests/test_auth_notice.py`: 16 source occurrences (test-path).
- `tests/test_cleanup_recovery.py`: 14 source occurrences (test-path).
- `tests/test_configuration.py`: 12 source occurrences (test-path).
- `tests/test_factory_maintenance.py`: 6 source occurrences (test-path).
- `tests/test_init.py`: 43 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 18 source occurrences (test-path).
- `tests/test_local_skills.py`: 17 source occurrences (test-path).
- `tests/test_native_roles.py`: 4 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_planning_setup.py`: 13 source occurrences (test-path).
- `tests/test_planning_watch.py`: 27 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 7 source occurrences (test-path).
- `tests/test_setup_completion.py`: 30 source occurrences (test-path).
- `tests/test_shared_pi.py`: 23 source occurrences (test-path).
- `tests/test_watch.py`: 51 source occurrences (test-path).
- `tests/test_watch_lock.py`: 6 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 16 source occurrences (test-path).
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
        +register_local_skills(config: FactoryConfiguration) None
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
        +check_skill_file(path: Path) None
        +write_new(path: Path, content: str) None
        +write_json(path: Path, value: dict) None
        -_generated_parent(path: Path) unknown
        +remove_generated(path: Path) None
        +replace_generated_json(path: Path, value: dict) None
        +read_generated_json(path: Path) dict
    }
    class c0011["SkillRegistration"] {
        <<class>>
        -__init__(directory: Path) unknown
        +directory: unknown
        +path: unknown
        -_error() FactoryError
        -_strings(value: unknown) bool
        -_owned(role: str, value: str) bool
        -_absolute(role: str, values: list[str]) list[str]
        +read() dict
        -_parent(role: str, files: dict) Type8
        -_resources(role: str, files: dict) list
        +update(changes: Type9) None
        -_finish() None
        +recover() None
    }
    class c0012["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type10
        +save(configuration: FactoryConfiguration) None
    }
    class c0013["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0014["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0015["WorkerProfiles"] {
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
    class c0016["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0017["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +role: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type11
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0018["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature2)
        -_catalog_tools(catalog: object) dict
    }
    class c0019["ForgetfulPlanning"] {
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
    class c0020["GitHubWorkTracking"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type12
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type14) Type13
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0021["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +runtime: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type1) Type11
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type1) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0022["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type15) str
        +runtime_ready(runtime: Path, inputs: Type15, probe: str) bool
    }
    class c0023["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        +run_owned(args: list[str], cwd: Path, env: Type11, login: bool, timeout: Type16) str
    }
    class c0024["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type14
        +foreman_agent_model: str
        +foreman_agent_effort: str
        +repository: Type17
        +forgetful: Type18
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
        +implementation_skills: Type14
        +review_skills: Type14
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0025["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type3
        +server: Type3
        +project_id: Type19
        +validate() None
        -_validate_server() None
    }
    class c0026["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type18
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: FactoryConfiguration) None
        +skill_paths(data: dict, field: str) Type14
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type14
    }
    class c0027["InitialiseFactory"] {
        <<class>>
        -__init__(Signature4)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type20, confirm: Type21) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type22, labels: Type23, model: Type3, effort: Type3) Type10
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type24
        +configure(Signature5)
        -_preflight(config: FactoryConfiguration) Type25
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type26, save: bool) list[str]
    }
    class c0028["ConfigurationStore"] {
        <<class>>
        +load() Type10
        +save(configuration: FactoryConfiguration) None
    }
    class c0029["ForemanProfile"] {
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
    class c0030["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start(cwd: str, model: str, effort: str) None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0031["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0032["Planning"] {
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
    class c0033["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0034["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0035["Worktrees"] {
        <<class>>
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
    }
    class c0036["ScaffoldIssue"] {
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
    class c0037["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        -_cleanup_state(mapping: dict) Type3
    }
    class c0038["WatchFactory"] {
        <<class>>
        -__init__(Signature7)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +run(Signature8)
        -_watch(Signature9)
        -_notify_issues(issues: Type13, seen: Type11, report: Type28, recovered: bool) None
        -_read_issues(source: WorkSource, labels: Type14, report_error: Type28) Type29
    }
    class c0039["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path) InitialiseFactory
        +build_watcher(python: str, config: FactoryConfiguration, workspace: Path) WatchFactory
    }
    class c0040["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature10)
        -_check_existing_connection(Signature11)
        -_connection(Signature12)
        -_prepare_foreman(Signature13)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type30, show_choices: bool) str
        -_select_model(Signature14)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_watch(args: argparse.Namespace, workspace: Path) int
        -_watch_locked(args: argparse.Namespace, workspace: Path) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature15)
        -_owner_configuration(Signature16)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_configuration(args: unknown, config: unknown, existing: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_worker_configuration(Signature17)
        -_complete_setup(Signature18)
        -_initialise(args: argparse.Namespace, workspace: Path) int
        -_initialise_locked(args: argparse.Namespace, workspace: Path) int
        +main() int
    }
    class c0041["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type31) FactoryConfiguration
    }
    class c0042["FactoryError"] {
        <<class>>
    }
    class c0043["Issue"] {
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
    class c0044["Label"] {
        <<class>>
        +name: str
    }
    class c0045["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0046["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0047["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type12
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type14) Type13
    }
    c0000 ..> c0000 : 4 relationships (see list)
    c0000 ..> c0002 : 4 relationships (see list)
    c0000 ..> c0019 : 3 relationships (see list)
    c0001 ..> c0006 : main() calls list_models()
    c0002 ..> c0002 : 5 relationships (see list)
    c0002 ..> c0011 : _read() calls read()
    c0002 ..> c0030 : close() calls close()
    c0002 ..> c0042 : 4 relationships (see list)
    c0003 ..> c0038 : run_command() calls run()
    c0003 ..> c0042 : run_command() constructs FactoryError
    c0004 ..> c0004 : 7 relationships (see list)
    c0004 ..> c0005 : 9 relationships (see list)
    c0004 ..> c0006 : prepare() calls prepare()
    c0004 ..> c0010 : 3 relationships (see list)
    c0004 ..> c0011 : 2 relationships (see list)
    c0004 ..> c0015 : 3 relationships (see list)
    c0004 ..> c0024 : 6 relationships (see list)
    c0004 ..> c0042 : 4 relationships (see list)
    c0005 ..> c0005 : _read_selection() calls _selection_conflict()
    c0005 ..> c0010 : _read_selection() calls check_real_path()
    c0005 ..> c0042 : 2 relationships (see list)
    c0006 ..> c0004 : 8 relationships (see list)
    c0006 ..> c0006 : 26 relationships (see list)
    c0006 ..> c0010 : 8 relationships (see list)
    c0006 ..> c0011 : 3 relationships (see list)
    c0006 ..> c0013 : require_pi_home() calls quote()
    c0006 ..> c0016 : uses_browser_login() calls uses_browser_login()
    c0006 ..> c0017 : 8 relationships (see list)
    c0006 ..> c0018 : list_models() calls role_environment()
    c0006 ..> c0021 : 6 relationships (see list)
    c0006 ..> c0022 : 3 relationships (see list)
    c0006 ..> c0023 : list_models() calls run_owned()
    c0006 ..> c0024 : 4 relationships (see list)
    c0006 ..> c0025 : 9 relationships (see list)
    c0006 ..> c0042 : 13 relationships (see list)
    c0007 ..> c0003 : origin() calls run_command()
    c0007 ..> c0042 : origin() constructs FactoryError
    c0008 ..> c0003 : 2 relationships (see list)
    c0008 ..> c0008 : 2 relationships (see list)
    c0008 ..> c0009 : _repository_entries() calls _worktree_entries()
    c0008 ..> c0042 : 3 relationships (see list)
    c0010 ..> c0002 : _generated_parent() calls close()
    c0010 ..> c0010 : 7 relationships (see list)
    c0010 ..> c0012 : read_generated_json() calls load()
    c0010 ..> c0042 : 5 relationships (see list)
    c0011 ..> c0010 : 9 relationships (see list)
    c0011 ..> c0011 : 23 relationships (see list)
    c0011 ..> c0042 : 2 relationships (see list)
    c0012 ..> c0002 : 2 relationships (see list)
    c0012 ..> c0013 : save() calls quote()
    c0012 ..> c0024 : 2 relationships (see list)
    c0012 ..> c0026 : load() calls from_mapping()
    c0012 ..> c0028 : load() calls load()
    c0012 ..> c0042 : 2 relationships (see list)
    c0014 ..> c0002 : _hold_directory() calls close()
    c0014 ..> c0014 : hold() calls _hold_directory()
    c0014 ..> c0042 : _hold_directory() constructs FactoryError
    c0015 ..> c0010 : 4 relationships (see list)
    c0015 ..> c0015 : 8 relationships (see list)
    c0015 ..> c0022 : _role_selection() calls executable_path()
    c0015 ..> c0024 : 6 relationships (see list)
    c0015 ..> c0042 : 2 relationships (see list)
    c0016 ..> c0011 : uses_browser_login() calls read()
    c0016 ..> c0025 : type in uses_browser_login
    c0017 ..> c0017 : 7 relationships (see list)
    c0017 ..> c0018 : 2 relationships (see list)
    c0017 ..> c0023 : 2 relationships (see list)
    c0017 ..> c0025 : 7 relationships (see list)
    c0017 ..> c0042 : 5 relationships (see list)
    c0018 ..> c0011 : role_environment() calls update()
    c0018 ..> c0022 : role_environment() calls executable_path()
    c0018 ..> c0025 : type in role_environment
    c0019 ..> c0006 : check() calls check()
    c0019 ..> c0017 : 2 relationships (see list)
    c0019 ..> c0019 : 9 relationships (see list)
    c0019 ..> c0025 : type in __init__
    c0019 ..> c0042 : _rows() constructs FactoryError
    c0020 ..> c0003 : _api() calls run_command()
    c0020 ..> c0020 : 5 relationships (see list)
    c0020 ..> c0042 : 7 relationships (see list)
    c0020 ..> c0043 : 2 relationships (see list)
    c0020 ..> c0044 : 3 relationships (see list)
    c0020 ..> c0046 : 8 relationships (see list)
    c0021 ..> c0010 : install() calls write_new()
    c0021 ..> c0011 : install() calls read()
    c0021 ..> c0021 : 15 relationships (see list)
    c0021 ..> c0022 : 3 relationships (see list)
    c0021 ..> c0023 : 4 relationships (see list)
    c0021 ..> c0042 : 6 relationships (see list)
    c0022 ..> c0022 : runtime_ready() calls sync_fingerprint()
    c0022 ..> c0023 : runtime_ready() calls run_owned()
    c0023 ..> c0042 : run_owned() constructs FactoryError
    c0024 --> c0025 : field forgetful
    c0024 --> c0045 : field repository
    c0025 ..> c0026 : 2 relationships (see list)
    c0025 ..> c0042 : _validate_server() constructs FactoryError
    c0026 ..> c0024 : 4 relationships (see list)
    c0026 ..> c0025 : 3 relationships (see list)
    c0026 ..> c0026 : 11 relationships (see list)
    c0026 ..> c0042 : 7 relationships (see list)
    c0026 ..> c0045 : from_mapping() constructs RepositoryReference
    c0026 ..> c0046 : from_mapping() constructs WorkSource
    c0027 ..> c0004 : prepare_foreman() calls prepare()
    c0027 ..> c0006 : 5 relationships (see list)
    c0027 ..> c0007 : 3 relationships (see list)
    c0027 ..> c0012 : 2 relationships (see list)
    c0027 ..> c0020 : 5 relationships (see list)
    c0027 ..> c0024 : 6 relationships (see list)
    c0027 ..> c0025 : 2 relationships (see list)
    c0027 ..> c0026 : 2 relationships (see list)
    c0027 ..> c0027 : 3 relationships (see list)
    c0027 ..> c0028 : type in __init__
    c0027 ..> c0029 : type in __init__
    c0027 ..> c0031 : type in __init__
    c0027 ..> c0034 : type in __init__
    c0027 ..> c0042 : 5 relationships (see list)
    c0027 ..> c0044 : 2 relationships (see list)
    c0027 ..> c0045 : 2 relationships (see list)
    c0027 ..> c0046 : 2 relationships (see list)
    c0027 ..> c0047 : type in __init__
    c0028 ..> c0024 : 2 relationships (see list)
    c0029 ..> c0024 : 2 relationships (see list)
    c0029 ..> c0025 : 8 relationships (see list)
    c0034 ..> c0046 : type in source_from_remote
    c0036 ..> c0006 : check() calls check()
    c0036 ..> c0008 : 2 relationships (see list)
    c0036 ..> c0019 : 8 relationships (see list)
    c0036 ..> c0024 : type in __init__
    c0036 ..> c0032 : type in __init__
    c0036 ..> c0035 : type in __init__
    c0036 ..> c0036 : 7 relationships (see list)
    c0036 ..> c0037 : _ensure_mapping() calls _cleanup_state()
    c0036 ..> c0042 : 7 relationships (see list)
    c0036 ..> c0043 : 4 relationships (see list)
    c0036 ..> c0046 : unfinished() constructs WorkSource
    c0037 ..> c0042 : _cleanup_state() constructs FactoryError
    c0038 ..> c0002 : 5 relationships (see list)
    c0038 ..> c0004 : _notify_issues() calls prepare()
    c0038 ..> c0006 : run() calls check()
    c0038 ..> c0011 : _watch() calls update()
    c0038 ..> c0020 : _read_issues() calls list_issues()
    c0038 ..> c0024 : 2 relationships (see list)
    c0038 ..> c0030 : type in __init__
    c0038 ..> c0036 : 2 relationships (see list)
    c0038 ..> c0038 : 3 relationships (see list)
    c0038 ..> c0043 : 2 relationships (see list)
    c0038 ..> c0046 : 2 relationships (see list)
    c0038 ..> c0047 : type in __init__
    c0039 ..> c0002 : build_watcher() constructs AgentShellTerminal
    c0039 ..> c0004 : build_watcher() calls validate_guidance()
    c0039 ..> c0006 : 6 relationships (see list)
    c0039 ..> c0007 : build_initialiser() constructs GitRepositories
    c0039 ..> c0008 : build_watcher() constructs GitWorktrees
    c0039 ..> c0012 : build_initialiser() constructs TomlConfigurationStore
    c0039 ..> c0018 : build_watcher() calls role_environment()
    c0039 ..> c0019 : build_watcher() constructs ForgetfulPlanning
    c0039 ..> c0020 : 3 relationships (see list)
    c0039 ..> c0024 : type in build_watcher
    c0039 ..> c0027 : 2 relationships (see list)
    c0039 ..> c0036 : build_watcher() constructs ScaffoldIssue
    c0039 ..> c0038 : 2 relationships (see list)
    c0039 ..> c0042 : build_watcher() constructs FactoryError
    c0040 ..> c0006 : 7 relationships (see list)
    c0040 ..> c0007 : select_repositories() calls discover()
    c0040 ..> c0011 : _prompt_workers() calls update()
    c0040 ..> c0013 : _select_model() calls quote()
    c0040 ..> c0014 : 4 relationships (see list)
    c0040 ..> c0024 : 4 relationships (see list)
    c0040 ..> c0025 : 6 relationships (see list)
    c0040 ..> c0027 : 10 relationships (see list)
    c0040 ..> c0038 : _watch_locked() calls run()
    c0040 ..> c0039 : 2 relationships (see list)
    c0040 ..> c0040 : 30 relationships (see list)
    c0040 ..> c0041 : _watch_locked() calls load_configuration()
    c0040 ..> c0042 : 16 relationships (see list)
    c0041 ..> c0012 : 2 relationships (see list)
    c0041 ..> c0024 : type in load_configuration
    c0041 ..> c0042 : load_configuration() constructs FactoryError
    c0043 --> c0046 : field source
    c0045 --> c0046 : field work_source
    c0047 ..> c0043 : type in list_issues
    c0047 ..> c0044 : 2 relationships (see list)
    c0047 ..> c0046 : 4 relationships (see list)
```

## Source index

- c0000: `src/forgetful_factory/adapters/agentshell/controller.py` —
  `src/forgetful_factory/adapters/agentshell/controller.py`:1
- c0001: `src/forgetful_factory/adapters/agentshell/model_catalog.py` —
  `src/forgetful_factory/adapters/agentshell/model_catalog.py`:1
- c0002: `AgentShellTerminal` — `src/forgetful_factory/adapters/agentshell/terminal.py`:12
- c0003: `src/forgetful_factory/adapters/command.py` — `src/forgetful_factory/adapters/command.py`:1
- c0004: `CoordinatorProfiles` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:61
- c0005: `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py` —
  `src/forgetful_factory/adapters/filesystem/coordinator_profiles.py`:1
- c0006: `ForemanProfile` — `src/forgetful_factory/adapters/filesystem/foreman_profile.py`:48
- c0007: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:7
- c0008: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:21
- c0009: `src/forgetful_factory/adapters/filesystem/git_worktrees.py` —
  `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:1
- c0010: `src/forgetful_factory/adapters/filesystem/resource_files.py` —
  `src/forgetful_factory/adapters/filesystem/resource_files.py`:1
- c0011: `SkillRegistration` — `src/forgetful_factory/adapters/filesystem/skill_registration.py`:15
- c0012: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:22
- c0013: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0014: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0015: `WorkerProfiles` — `src/forgetful_factory/adapters/filesystem/worker_profiles.py`:21
- c0016: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0017: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:52
- c0018: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0019: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:8
- c0020: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0021: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:52
- c0022: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0023: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0024: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:80
- c0025: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0026: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0027: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0028: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0029: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:7
- c0030: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0031: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0032: `Planning` — `src/forgetful_factory/application/ports/planning.py`:4
- c0033: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0034: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0035: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:4
- c0036: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:31
- c0037: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0038: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:12
- c0039: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0040: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0041: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0042: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0043: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0044: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0045: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0046: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0047: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `control() calls serve()`
- c0000 ..> c0000: `interact() calls ready()`
- c0000 ..> c0000: `main() calls control()`
- c0000 ..> c0000: `serve() calls interact()`
- c0000 ..> c0002: `control() calls close()`
- c0000 ..> c0002: `control() calls wait()`
- c0000 ..> c0002: `serve() calls close()`
- c0000 ..> c0002: `serve() calls wait()`
- c0000 ..> c0019: `control() calls create_task()`
- c0000 ..> c0019: `main() calls create_task()`
- c0000 ..> c0019: `serve() calls create_task()`
- c0001 ..> c0006: `main() calls list_models()`
- c0002 ..> c0002: `send() calls _read()`
- c0002 ..> c0002: `send() calls _write()`
- c0002 ..> c0002: `start() calls _read()`
- c0002 ..> c0002: `start() calls _write()`
- c0002 ..> c0002: `wait() calls _read()`
- c0002 ..> c0011: `_read() calls read()`
- c0002 ..> c0030: `close() calls close()`
- c0002 ..> c0042: `_read() constructs FactoryError`
- c0002 ..> c0042: `_write() constructs FactoryError`
- c0002 ..> c0042: `close() constructs FactoryError`
- c0002 ..> c0042: `start() constructs FactoryError`
- c0003 ..> c0038: `run_command() calls run()`
- c0003 ..> c0042: `run_command() constructs FactoryError`
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
- c0004 ..> c0005: `register_local_skills() calls _read_selection()`
- c0004 ..> c0005: `selection() calls _selection_conflict()`
- c0004 ..> c0006: `prepare() calls prepare()`
- c0004 ..> c0010: `prepare() calls write_json()`
- c0004 ..> c0010: `prepare() calls write_new()`
- c0004 ..> c0010: `register_local_skills() calls check_skill_file()`
- c0004 ..> c0011: `register_local_skills() calls update()`
- c0004 ..> c0011: `register_local_skills() constructs SkillRegistration`
- c0004 ..> c0015: `__init__() constructs WorkerProfiles`
- c0004 ..> c0015: `_worker_role() calls resources()`
- c0004 ..> c0015: `selection() calls selection()`
- c0004 ..> c0024: `type in _role`
- c0004 ..> c0024: `type in _worker_role`
- c0004 ..> c0024: `type in prepare`
- c0004 ..> c0024: `type in register_local_skills`
- c0004 ..> c0024: `type in selection`
- c0004 ..> c0024: `type in validate_guidance`
- c0004 ..> c0042: `prepare() constructs FactoryError`
- c0004 ..> c0042: `selection() constructs FactoryError`
- c0004 ..> c0042: `validate_depth() constructs FactoryError`
- c0004 ..> c0042: `validate_guidance() constructs FactoryError`
- c0005 ..> c0005: `_read_selection() calls _selection_conflict()`
- c0005 ..> c0010: `_read_selection() calls check_real_path()`
- c0005 ..> c0042: `_selection_conflict() constructs FactoryError`
- c0005 ..> c0042: `type in _selection_conflict`
- c0006 ..> c0004: `_selection() calls selection()`
- c0006 ..> c0004: `_selection() constructs CoordinatorProfiles`
- c0006 ..> c0004: `prepare_roles() calls register_local_skills()`
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
- c0006 ..> c0006: `prepare_roles() calls list_models()`
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
- c0006 ..> c0010: `prepare_roles() calls check_real_path()`
- c0006 ..> c0010: `record_completion() calls replace_generated_json()`
- c0006 ..> c0010: `validate_completion() calls read_generated_json()`
- c0006 ..> c0011: `_install_resources() calls read()`
- c0006 ..> c0011: `begin_setup() calls recover()`
- c0006 ..> c0011: `begin_setup() constructs SkillRegistration`
- c0006 ..> c0013: `require_pi_home() calls quote()`
- c0006 ..> c0016: `uses_browser_login() calls uses_browser_login()`
- c0006 ..> c0017: `check() calls check()`
- c0006 ..> c0017: `check() constructs AgentForgetfulConnection`
- c0006 ..> c0017: `create_project() calls create_project()`
- c0006 ..> c0017: `create_project() constructs AgentForgetfulConnection`
- c0006 ..> c0017: `login() calls login()`
- c0006 ..> c0017: `login() constructs AgentForgetfulConnection`
- c0006 ..> c0017: `projects() calls projects()`
- c0006 ..> c0017: `projects() constructs AgentForgetfulConnection`
- c0006 ..> c0018: `list_models() calls role_environment()`
- c0006 ..> c0021: `install() calls install()`
- c0006 ..> c0021: `install() constructs HostDependencies`
- c0006 ..> c0021: `installation() calls description()`
- c0006 ..> c0021: `installation() constructs HostDependencies`
- c0006 ..> c0021: `missing_executables() calls pi_ready()`
- c0006 ..> c0021: `missing_executables() constructs HostDependencies`
- c0006 ..> c0022: `missing_executables() calls executable_path()`
- c0006 ..> c0022: `missing_executables() calls runtime_ready()`
- c0006 ..> c0022: `require_pi_home() calls executable_path()`
- c0006 ..> c0023: `list_models() calls run_owned()`
- c0006 ..> c0024: `type in _selection`
- c0006 ..> c0024: `type in record_completion`
- c0006 ..> c0024: `type in validate_completion`
- c0006 ..> c0024: `type in validate_worker_models`
- c0006 ..> c0025: `type in check`
- c0006 ..> c0025: `type in create_project`
- c0006 ..> c0025: `type in list_models`
- c0006 ..> c0025: `type in login`
- c0006 ..> c0025: `type in missing_executables`
- c0006 ..> c0025: `type in prepare`
- c0006 ..> c0025: `type in projects`
- c0006 ..> c0025: `type in uses_browser_login`
- c0006 ..> c0025: `type in validate_setup`
- c0006 ..> c0042: `_install_resources() constructs FactoryError`
- c0006 ..> c0042: `_read_guidance() constructs FactoryError`
- c0006 ..> c0042: `choose_pi_home() constructs FactoryError`
- c0006 ..> c0042: `launch_resources() constructs FactoryError`
- c0006 ..> c0042: `list_models() constructs FactoryError`
- c0006 ..> c0042: `pi_home() constructs FactoryError`
- c0006 ..> c0042: `prepare_roles() constructs FactoryError`
- c0006 ..> c0042: `require_pi_home() constructs FactoryError`
- c0006 ..> c0042: `validate_bundled_resources() constructs FactoryError`
- c0006 ..> c0042: `validate_completion() constructs FactoryError`
- c0006 ..> c0042: `validate_guidance() constructs FactoryError`
- c0006 ..> c0042: `validate_setup() constructs FactoryError`
- c0006 ..> c0042: `validate_worker_models() constructs FactoryError`
- c0007 ..> c0003: `origin() calls run_command()`
- c0007 ..> c0042: `origin() constructs FactoryError`
- c0008 ..> c0003: `_repository_entries() calls run_command()`
- c0008 ..> c0003: `ensure() calls run_command()`
- c0008 ..> c0008: `ensure() calls _repository_entries()`
- c0008 ..> c0008: `verify_removed() calls _repository_entries()`
- c0008 ..> c0009: `_repository_entries() calls _worktree_entries()`
- c0008 ..> c0042: `_repository_entries() constructs FactoryError`
- c0008 ..> c0042: `ensure() constructs FactoryError`
- c0008 ..> c0042: `verify_removed() constructs FactoryError`
- c0010 ..> c0002: `_generated_parent() calls close()`
- c0010 ..> c0010: `_generated_parent() calls check_real_path()`
- c0010 ..> c0010: `check_skill_file() calls check_real_path()`
- c0010 ..> c0010: `read_generated_json() calls _generated_parent()`
- c0010 ..> c0010: `remove_generated() calls _generated_parent()`
- c0010 ..> c0010: `replace_generated_json() calls _generated_parent()`
- c0010 ..> c0010: `write_json() calls write_new()`
- c0010 ..> c0010: `write_new() calls check_real_path()`
- c0010 ..> c0012: `read_generated_json() calls load()`
- c0010 ..> c0042: `_generated_parent() constructs FactoryError`
- c0010 ..> c0042: `check_real_path() constructs FactoryError`
- c0010 ..> c0042: `check_skill_file() constructs FactoryError`
- c0010 ..> c0042: `read_generated_json() constructs FactoryError`
- c0010 ..> c0042: `write_new() constructs FactoryError`
- c0011 ..> c0010: `_finish() calls check_real_path()`
- c0011 ..> c0010: `_finish() calls check_skill_file()`
- c0011 ..> c0010: `_finish() calls replace_generated_json()`
- c0011 ..> c0010: `_parent() calls read_generated_json()`
- c0011 ..> c0010: `_resources() calls read_generated_json()`
- c0011 ..> c0010: `read() calls check_real_path()`
- c0011 ..> c0010: `read() calls read_generated_json()`
- c0011 ..> c0010: `recover() calls check_real_path()`
- c0011 ..> c0010: `update() calls replace_generated_json()`
- c0011 ..> c0011: `_finish() calls _absolute()`
- c0011 ..> c0011: `_finish() calls _error()`
- c0011 ..> c0011: `_finish() calls _parent()`
- c0011 ..> c0011: `_finish() calls _resources()`
- c0011 ..> c0011: `_finish() calls read()`
- c0011 ..> c0011: `_parent() calls _error()`
- c0011 ..> c0011: `_resources() calls _error()`
- c0011 ..> c0011: `_resources() calls _strings()`
- c0011 ..> c0011: `read() calls _absolute()`
- c0011 ..> c0011: `read() calls _error()`
- c0011 ..> c0011: `read() calls _owned()`
- c0011 ..> c0011: `read() calls _strings()`
- c0011 ..> c0011: `recover() calls _error()`
- c0011 ..> c0011: `recover() calls _finish()`
- c0011 ..> c0011: `recover() calls _resources()`
- c0011 ..> c0011: `recover() calls read()`
- c0011 ..> c0011: `recover() calls update()`
- c0011 ..> c0011: `update() calls _absolute()`
- c0011 ..> c0011: `update() calls _error()`
- c0011 ..> c0011: `update() calls _finish()`
- c0011 ..> c0011: `update() calls _parent()`
- c0011 ..> c0011: `update() calls _resources()`
- c0011 ..> c0011: `update() calls read()`
- c0011 ..> c0042: `_error() constructs FactoryError`
- c0011 ..> c0042: `type in _error`
- c0012 ..> c0002: `load() calls close()`
- c0012 ..> c0002: `save() calls close()`
- c0012 ..> c0013: `save() calls quote()`
- c0012 ..> c0024: `type in load`
- c0012 ..> c0024: `type in save`
- c0012 ..> c0026: `load() calls from_mapping()`
- c0012 ..> c0028: `load() calls load()`
- c0012 ..> c0042: `load() constructs FactoryError`
- c0012 ..> c0042: `save() constructs FactoryError`
- c0014 ..> c0002: `_hold_directory() calls close()`
- c0014 ..> c0014: `hold() calls _hold_directory()`
- c0014 ..> c0042: `_hold_directory() constructs FactoryError`
- c0015 ..> c0010: `_role_selection() calls check_real_path()`
- c0015 ..> c0010: `prepare() calls write_json()`
- c0015 ..> c0010: `prepare() calls write_new()`
- c0015 ..> c0010: `resources() calls check_real_path()`
- c0015 ..> c0015: `_role_selection() calls _skill_digest()`
- c0015 ..> c0015: `_role_selection() calls resources()`
- c0015 ..> c0015: `_validate_skill_sources() calls _skill_digest()`
- c0015 ..> c0015: `_validate_skill_sources() calls skills()`
- c0015 ..> c0015: `prepare() calls _validate_skill_sources()`
- c0015 ..> c0015: `prepare() calls skills()`
- c0015 ..> c0015: `resources() calls skills()`
- c0015 ..> c0015: `selection() calls _role_selection()`
- c0015 ..> c0022: `_role_selection() calls executable_path()`
- c0015 ..> c0024: `type in _role_selection`
- c0015 ..> c0024: `type in _validate_skill_sources`
- c0015 ..> c0024: `type in prepare`
- c0015 ..> c0024: `type in resources`
- c0015 ..> c0024: `type in selection`
- c0015 ..> c0024: `type in skills`
- c0015 ..> c0042: `_skill_digest() constructs FactoryError`
- c0015 ..> c0042: `selection() constructs FactoryError`
- c0016 ..> c0011: `uses_browser_login() calls read()`
- c0016 ..> c0025: `type in uses_browser_login`
- c0017 ..> c0017: `call() calls command()`
- c0017 ..> c0017: `check() calls call()`
- c0017 ..> c0017: `check() calls command()`
- c0017 ..> c0017: `command() calls _environment()`
- c0017 ..> c0017: `create_project() calls call()`
- c0017 ..> c0017: `login() calls _environment()`
- c0017 ..> c0017: `projects() calls command()`
- c0017 ..> c0018: `_environment() calls role_environment()`
- c0017 ..> c0018: `check() calls _catalog_tools()`
- c0017 ..> c0023: `command() calls run_owned()`
- c0017 ..> c0023: `login() calls run_owned()`
- c0017 ..> c0025: `type in _environment`
- c0017 ..> c0025: `type in call`
- c0017 ..> c0025: `type in check`
- c0017 ..> c0025: `type in command`
- c0017 ..> c0025: `type in create_project`
- c0017 ..> c0025: `type in login`
- c0017 ..> c0025: `type in projects`
- c0017 ..> c0042: `check() constructs FactoryError`
- c0017 ..> c0042: `command() constructs FactoryError`
- c0017 ..> c0042: `create_project() constructs FactoryError`
- c0017 ..> c0042: `login() constructs FactoryError`
- c0017 ..> c0042: `projects() constructs FactoryError`
- c0018 ..> c0011: `role_environment() calls update()`
- c0018 ..> c0022: `role_environment() calls executable_path()`
- c0018 ..> c0025: `type in role_environment`
- c0019 ..> c0006: `check() calls check()`
- c0019 ..> c0017: `__init__() constructs AgentForgetfulConnection`
- c0019 ..> c0017: `_call() calls call()`
- c0019 ..> c0019: `create_plan() calls _call()`
- c0019 ..> c0019: `create_task() calls _call()`
- c0019 ..> c0019: `get_plan() calls _call()`
- c0019 ..> c0019: `plans() calls _call()`
- c0019 ..> c0019: `plans() calls _rows()`
- c0019 ..> c0019: `tasks() calls _call()`
- c0019 ..> c0019: `tasks() calls _rows()`
- c0019 ..> c0019: `update_plan() calls _call()`
- c0019 ..> c0019: `update_task() calls _call()`
- c0019 ..> c0025: `type in __init__`
- c0019 ..> c0042: `_rows() constructs FactoryError`
- c0020 ..> c0003: `_api() calls run_command()`
- c0020 ..> c0020: `check_access() calls _api()`
- c0020 ..> c0020: `create_label() calls _api()`
- c0020 ..> c0020: `list_issues() calls _api()`
- c0020 ..> c0020: `list_issues() calls _validate_issue()`
- c0020 ..> c0020: `list_labels() calls _api()`
- c0020 ..> c0042: `_api() constructs FactoryError`
- c0020 ..> c0042: `_validate_issue() constructs FactoryError`
- c0020 ..> c0042: `check_access() constructs FactoryError`
- c0020 ..> c0042: `create_label() constructs FactoryError`
- c0020 ..> c0042: `list_issues() constructs FactoryError`
- c0020 ..> c0042: `list_labels() constructs FactoryError`
- c0020 ..> c0042: `source_from_remote() constructs FactoryError`
- c0020 ..> c0043: `list_issues() constructs Issue`
- c0020 ..> c0043: `type in list_issues`
- c0020 ..> c0044: `list_labels() constructs Label`
- c0020 ..> c0044: `type in create_label`
- c0020 ..> c0044: `type in list_labels`
- c0020 ..> c0046: `source_from_remote() constructs WorkSource`
- c0020 ..> c0046: `type in _api`
- c0020 ..> c0046: `type in _validate_issue`
- c0020 ..> c0046: `type in check_access`
- c0020 ..> c0046: `type in create_label`
- c0020 ..> c0046: `type in list_issues`
- c0020 ..> c0046: `type in list_labels`
- c0020 ..> c0046: `type in source_from_remote`
- c0021 ..> c0010: `install() calls write_new()`
- c0021 ..> c0011: `install() calls read()`
- c0021 ..> c0021: `_check_uv() calls _environment()`
- c0021 ..> c0021: `_forgetful_python() calls _check_uv()`
- c0021 ..> c0021: `_forgetful_python() calls _environment()`
- c0021 ..> c0021: `_install_role_runtime() calls _check_uv()`
- c0021 ..> c0021: `_install_role_runtime() calls _run()`
- c0021 ..> c0021: `_install_tmux() calls _run()`
- c0021 ..> c0021: `_run() calls _environment()`
- c0021 ..> c0021: `description() calls _forgetful_python()`
- c0021 ..> c0021: `description() calls _ubuntu_tmux()`
- c0021 ..> c0021: `install() calls _forgetful_python()`
- c0021 ..> c0021: `install() calls _install_role_runtime()`
- c0021 ..> c0021: `install() calls _install_tmux()`
- c0021 ..> c0021: `install() calls _run()`
- c0021 ..> c0021: `install() calls _ubuntu_tmux()`
- c0021 ..> c0021: `pi_ready() calls _environment()`
- c0021 ..> c0022: `_install_role_runtime() calls sync_fingerprint()`
- c0021 ..> c0022: `install() calls sync_fingerprint()`
- c0021 ..> c0022: `pi_ready() calls sync_fingerprint()`
- c0021 ..> c0023: `_check_uv() calls run_owned()`
- c0021 ..> c0023: `_forgetful_python() calls run_owned()`
- c0021 ..> c0023: `_run() calls run_owned()`
- c0021 ..> c0023: `pi_ready() calls run_owned()`
- c0021 ..> c0042: `_check_uv() constructs FactoryError`
- c0021 ..> c0042: `_forgetful_python() constructs FactoryError`
- c0021 ..> c0042: `_install_role_runtime() constructs FactoryError`
- c0021 ..> c0042: `_install_tmux() constructs FactoryError`
- c0021 ..> c0042: `_run() constructs FactoryError`
- c0021 ..> c0042: `install() constructs FactoryError`
- c0022 ..> c0022: `runtime_ready() calls sync_fingerprint()`
- c0022 ..> c0023: `runtime_ready() calls run_owned()`
- c0023 ..> c0042: `run_owned() constructs FactoryError`
- c0024 --> c0025: `field forgetful`
- c0024 --> c0045: `field repository`
- c0025 ..> c0026: `_validate_server() calls loopback_host()`
- c0025 ..> c0026: `_validate_server() calls nonblank()`
- c0025 ..> c0042: `_validate_server() constructs FactoryError`
- c0026 ..> c0024: `from_mapping() constructs FactoryConfiguration`
- c0026 ..> c0024: `type in from_mapping`
- c0026 ..> c0024: `type in validate`
- c0026 ..> c0024: `type in validate_workers`
- c0026 ..> c0025: `connection_from_mapping() constructs ForgetfulConnection`
- c0026 ..> c0025: `type in connection_from_mapping`
- c0026 ..> c0025: `validate() calls _validate_server()`
- c0026 ..> c0026: `connection_from_mapping() calls validate()`
- c0026 ..> c0026: `from_mapping() calls connection_from_mapping()`
- c0026 ..> c0026: `from_mapping() calls skill_paths()`
- c0026 ..> c0026: `from_mapping() calls validate()`
- c0026 ..> c0026: `skill_paths() calls nonblank()`
- c0026 ..> c0026: `unique_labels() calls nonblank()`
- c0026 ..> c0026: `validate() calls nonblank()`
- c0026 ..> c0026: `validate() calls validate_role_app()`
- c0026 ..> c0026: `validate() calls validate_workers()`
- c0026 ..> c0026: `validate_workers() calls nonblank()`
- c0026 ..> c0026: `validate_workers() calls validate_role_app()`
- c0026 ..> c0042: `connection_from_mapping() constructs FactoryError`
- c0026 ..> c0042: `from_mapping() constructs FactoryError`
- c0026 ..> c0042: `nonblank() constructs FactoryError`
- c0026 ..> c0042: `skill_paths() constructs FactoryError`
- c0026 ..> c0042: `validate() constructs FactoryError`
- c0026 ..> c0042: `validate_role_app() constructs FactoryError`
- c0026 ..> c0042: `validate_workers() constructs FactoryError`
- c0026 ..> c0045: `from_mapping() constructs RepositoryReference`
- c0026 ..> c0046: `from_mapping() constructs WorkSource`
- c0027 ..> c0004: `prepare_foreman() calls prepare()`
- c0027 ..> c0006: `check_foreman() calls check()`
- c0027 ..> c0006: `check_foreman() calls login()`
- c0027 ..> c0006: `prepare_foreman() calls install()`
- c0027 ..> c0006: `prepare_foreman() calls installation()`
- c0027 ..> c0006: `prepare_foreman() calls missing_executables()`
- c0027 ..> c0007: `_preflight() calls origin()`
- c0027 ..> c0007: `discover() calls discover()`
- c0027 ..> c0007: `inspect() calls origin()`
- c0027 ..> c0012: `initialise() calls save()`
- c0027 ..> c0012: `load_existing() calls load()`
- c0027 ..> c0020: `_ensure_label() calls create_label()`
- c0027 ..> c0020: `_preflight() calls check_access()`
- c0027 ..> c0020: `_preflight() calls list_labels()`
- c0027 ..> c0020: `_preflight() calls source_from_remote()`
- c0027 ..> c0020: `inspect() calls source_from_remote()`
- c0027 ..> c0024: `configure() constructs FactoryConfiguration`
- c0027 ..> c0024: `type in _preflight`
- c0027 ..> c0024: `type in check_foreman`
- c0027 ..> c0024: `type in configure`
- c0027 ..> c0024: `type in initialise`
- c0027 ..> c0024: `type in load_existing`
- c0027 ..> c0025: `_preflight() calls validate()`
- c0027 ..> c0025: `type in prepare_foreman`
- c0027 ..> c0026: `configure() calls unique_labels()`
- c0027 ..> c0026: `load_existing() calls unique_labels()`
- c0027 ..> c0027: `configure() calls inspect()`
- c0027 ..> c0027: `initialise() calls _ensure_label()`
- c0027 ..> c0027: `initialise() calls _preflight()`
- c0027 ..> c0028: `type in __init__`
- c0027 ..> c0029: `type in __init__`
- c0027 ..> c0031: `type in __init__`
- c0027 ..> c0034: `type in __init__`
- c0027 ..> c0042: `_preflight() constructs FactoryError`
- c0027 ..> c0042: `initialise() constructs FactoryError`
- c0027 ..> c0042: `inspect() constructs FactoryError`
- c0027 ..> c0042: `load_existing() constructs FactoryError`
- c0027 ..> c0042: `prepare_foreman() constructs FactoryError`
- c0027 ..> c0044: `_ensure_label() constructs Label`
- c0027 ..> c0044: `type in _preflight`
- c0027 ..> c0045: `inspect() constructs RepositoryReference`
- c0027 ..> c0045: `type in inspect`
- c0027 ..> c0046: `type in _ensure_label`
- c0027 ..> c0046: `type in _preflight`
- c0027 ..> c0047: `type in __init__`
- c0028 ..> c0024: `type in load`
- c0028 ..> c0024: `type in save`
- c0029 ..> c0024: `type in prepare_roles`
- c0029 ..> c0024: `type in record_completion`
- c0029 ..> c0025: `type in check`
- c0029 ..> c0025: `type in create_project`
- c0029 ..> c0025: `type in list_models`
- c0029 ..> c0025: `type in login`
- c0029 ..> c0025: `type in missing_executables`
- c0029 ..> c0025: `type in prepare`
- c0029 ..> c0025: `type in projects`
- c0029 ..> c0025: `type in uses_browser_login`
- c0034 ..> c0046: `type in source_from_remote`
- c0036 ..> c0006: `check() calls check()`
- c0036 ..> c0008: `_ensure_mapping() calls ensure()`
- c0036 ..> c0008: `_ensure_mapping() calls verify_removed()`
- c0036 ..> c0019: `_issue_plan() calls create_plan()`
- c0036 ..> c0019: `_issue_plan() calls get_plan()`
- c0036 ..> c0019: `_issue_plan() calls plans()`
- c0036 ..> c0019: `_ownership() calls tasks()`
- c0036 ..> c0019: `prepare() calls create_task()`
- c0036 ..> c0019: `prepare() calls update_plan()`
- c0036 ..> c0019: `unfinished() calls get_plan()`
- c0036 ..> c0019: `unfinished() calls plans()`
- c0036 ..> c0024: `type in __init__`
- c0036 ..> c0032: `type in __init__`
- c0036 ..> c0035: `type in __init__`
- c0036 ..> c0036: `_ensure_worktrees() calls _ensure_mapping()`
- c0036 ..> c0036: `prepare() calls _context()`
- c0036 ..> c0036: `prepare() calls _ensure_worktrees()`
- c0036 ..> c0036: `prepare() calls _issue_plan()`
- c0036 ..> c0036: `prepare() calls _ownership()`
- c0036 ..> c0036: `unfinished() calls _context()`
- c0036 ..> c0036: `unfinished() calls _is_unfinished_factory_plan()`
- c0036 ..> c0037: `_ensure_mapping() calls _cleanup_state()`
- c0036 ..> c0042: `_context() constructs FactoryError`
- c0036 ..> c0042: `_ensure_mapping() constructs FactoryError`
- c0036 ..> c0042: `_ensure_worktrees() constructs FactoryError`
- c0036 ..> c0042: `_issue_plan() constructs FactoryError`
- c0036 ..> c0042: `_ownership() constructs FactoryError`
- c0036 ..> c0042: `prepare() constructs FactoryError`
- c0036 ..> c0042: `unfinished() constructs FactoryError`
- c0036 ..> c0043: `type in _issue_plan`
- c0036 ..> c0043: `type in prepare`
- c0036 ..> c0043: `type in unfinished`
- c0036 ..> c0043: `unfinished() constructs Issue`
- c0036 ..> c0046: `unfinished() constructs WorkSource`
- c0037 ..> c0042: `_cleanup_state() constructs FactoryError`
- c0038 ..> c0002: `_notify_issues() calls send()`
- c0038 ..> c0002: `_watch() calls close()`
- c0038 ..> c0002: `_watch() calls start()`
- c0038 ..> c0002: `_watch() calls wait()`
- c0038 ..> c0002: `run() calls startup_hint()`
- c0038 ..> c0004: `_notify_issues() calls prepare()`
- c0038 ..> c0006: `run() calls check()`
- c0038 ..> c0011: `_watch() calls update()`
- c0038 ..> c0020: `_read_issues() calls list_issues()`
- c0038 ..> c0024: `type in _watch`
- c0038 ..> c0024: `type in run`
- c0038 ..> c0030: `type in __init__`
- c0038 ..> c0036: `_watch() calls unfinished()`
- c0038 ..> c0036: `type in __init__`
- c0038 ..> c0038: `_watch() calls _notify_issues()`
- c0038 ..> c0038: `_watch() calls _read_issues()`
- c0038 ..> c0038: `run() calls _watch()`
- c0038 ..> c0043: `type in _notify_issues`
- c0038 ..> c0043: `type in _read_issues`
- c0038 ..> c0046: `_watch() constructs WorkSource`
- c0038 ..> c0046: `type in _read_issues`
- c0038 ..> c0047: `type in __init__`
- c0039 ..> c0002: `build_watcher() constructs AgentShellTerminal`
- c0039 ..> c0004: `build_watcher() calls validate_guidance()`
- c0039 ..> c0006: `build_initialiser() constructs ForemanProfile`
- c0039 ..> c0006: `build_watcher() calls launch_resources()`
- c0039 ..> c0006: `build_watcher() calls pi_home()`
- c0039 ..> c0006: `build_watcher() calls validate_completion()`
- c0039 ..> c0006: `build_watcher() calls validate_setup()`
- c0039 ..> c0006: `build_watcher() constructs ForemanProfile`
- c0039 ..> c0007: `build_initialiser() constructs GitRepositories`
- c0039 ..> c0008: `build_watcher() constructs GitWorktrees`
- c0039 ..> c0012: `build_initialiser() constructs TomlConfigurationStore`
- c0039 ..> c0018: `build_watcher() calls role_environment()`
- c0039 ..> c0019: `build_watcher() constructs ForgetfulPlanning`
- c0039 ..> c0020: `build_initialiser() constructs GitHubWorkTracking`
- c0039 ..> c0020: `build_watcher() calls source_from_remote()`
- c0039 ..> c0020: `build_watcher() constructs GitHubWorkTracking`
- c0039 ..> c0024: `type in build_watcher`
- c0039 ..> c0027: `build_initialiser() constructs InitialiseFactory`
- c0039 ..> c0027: `type in build_initialiser`
- c0039 ..> c0036: `build_watcher() constructs ScaffoldIssue`
- c0039 ..> c0038: `build_watcher() constructs WatchFactory`
- c0039 ..> c0038: `type in build_watcher`
- c0039 ..> c0042: `build_watcher() constructs FactoryError`
- c0040 ..> c0006: `_complete_setup() calls record_completion()`
- c0040 ..> c0006: `_complete_setup() calls uses_browser_login()`
- c0040 ..> c0006: `_initialise_locked() calls begin_setup()`
- c0040 ..> c0006: `_initialise_locked() calls choose_pi_home()`
- c0040 ..> c0006: `_select_model() calls list_models()`
- c0040 ..> c0006: `_select_project() calls create_project()`
- c0040 ..> c0006: `_select_project() calls projects()`
- c0040 ..> c0007: `select_repositories() calls discover()`
- c0040 ..> c0011: `_prompt_workers() calls update()`
- c0040 ..> c0013: `_select_model() calls quote()`
- c0040 ..> c0014: `_initialise() calls hold()`
- c0040 ..> c0014: `_initialise() constructs WorkspaceWatchLease`
- c0040 ..> c0014: `_watch() calls hold()`
- c0040 ..> c0014: `_watch() constructs WorkspaceWatchLease`
- c0040 ..> c0024: `type in _complete_setup`
- c0040 ..> c0024: `type in _configure_new_factory`
- c0040 ..> c0024: `type in _owner_configuration`
- c0040 ..> c0024: `type in _worker_configuration`
- c0040 ..> c0025: `_connection() calls validate()`
- c0040 ..> c0025: `_connection() constructs ForgetfulConnection`
- c0040 ..> c0025: `type in _check_existing_connection`
- c0040 ..> c0025: `type in _configure_new_factory`
- c0040 ..> c0025: `type in _connection`
- c0040 ..> c0025: `type in _select_project`
- c0040 ..> c0027: `_complete_setup() calls check_foreman()`
- c0040 ..> c0027: `_configure_new_factory() calls configure()`
- c0040 ..> c0027: `_configure_new_factory() calls inspect()`
- c0040 ..> c0027: `_initialise_locked() calls initialise()`
- c0040 ..> c0027: `_initialise_locked() calls load_existing()`
- c0040 ..> c0027: `_prepare_foreman() calls prepare_foreman()`
- c0040 ..> c0027: `type in _complete_setup`
- c0040 ..> c0027: `type in _configure_new_factory`
- c0040 ..> c0027: `type in _select_project`
- c0040 ..> c0027: `type in select_repositories`
- c0040 ..> c0038: `_watch_locked() calls run()`
- c0040 ..> c0039: `_initialise_locked() calls build_initialiser()`
- c0040 ..> c0039: `_watch_locked() calls build_watcher()`
- c0040 ..> c0040: `_configure_new_factory() calls _prepare_foreman()`
- c0040 ..> c0040: `_configure_new_factory() calls _select_model()`
- c0040 ..> c0040: `_configure_new_factory() calls _select_numbered()`
- c0040 ..> c0040: `_configure_new_factory() calls select_repositories()`
- c0040 ..> c0040: `_connection() calls _check_existing_connection()`
- c0040 ..> c0040: `_initialise() calls _initialise_locked()`
- c0040 ..> c0040: `_initialise_locked() calls _complete_setup()`
- c0040 ..> c0040: `_initialise_locked() calls _configure_new_factory()`
- c0040 ..> c0040: `_initialise_locked() calls _confirm_pi_home()`
- c0040 ..> c0040: `_initialise_locked() calls _connection()`
- c0040 ..> c0040: `_initialise_locked() calls _owner_configuration()`
- c0040 ..> c0040: `_initialise_locked() calls _research_configuration()`
- c0040 ..> c0040: `_initialise_locked() calls _worker_configuration()`
- c0040 ..> c0040: `_print_models() calls _safe_diagnostic()`
- c0040 ..> c0040: `_prompt_worker() calls _select_numbered()`
- c0040 ..> c0040: `_prompt_workers() calls _prompt_worker()`
- c0040 ..> c0040: `_select_model() calls _print_models()`
- c0040 ..> c0040: `_select_model() calls _select_numbered()`
- c0040 ..> c0040: `_select_numbered() calls _safe_diagnostic()`
- c0040 ..> c0040: `_select_project() calls _listed_project_id()`
- c0040 ..> c0040: `_select_project() calls _safe_diagnostic()`
- c0040 ..> c0040: `_watch() calls _watch_locked()`
- c0040 ..> c0040: `_watch_locked() calls _choose_existing()`
- c0040 ..> c0040: `_watch_locked() calls _safe_diagnostic()`
- c0040 ..> c0040: `_worker_configuration() calls _prompt_workers()`
- c0040 ..> c0040: `_worker_configuration() calls _worker_arguments()`
- c0040 ..> c0040: `main() calls _initialise()`
- c0040 ..> c0040: `main() calls _parse_arguments()`
- c0040 ..> c0040: `main() calls _safe_diagnostic()`
- c0040 ..> c0040: `main() calls _watch()`
- c0040 ..> c0041: `_watch_locked() calls load_configuration()`
- c0040 ..> c0042: `_check_existing_connection() constructs FactoryError`
- c0040 ..> c0042: `_choose_existing() constructs FactoryError`
- c0040 ..> c0042: `_configure_new_factory() constructs FactoryError`
- c0040 ..> c0042: `_install_missing() constructs FactoryError`
- c0040 ..> c0042: `_listed_project_id() constructs FactoryError`
- c0040 ..> c0042: `_owner_configuration() constructs FactoryError`
- c0040 ..> c0042: `_prompt_worker() constructs FactoryError`
- c0040 ..> c0042: `_prompt_workers() constructs FactoryError`
- c0040 ..> c0042: `_research_configuration() constructs FactoryError`
- c0040 ..> c0042: `_select_model() constructs FactoryError`
- c0040 ..> c0042: `_select_numbered() constructs FactoryError`
- c0040 ..> c0042: `_select_project() constructs FactoryError`
- c0040 ..> c0042: `_watch_locked() constructs FactoryError`
- c0040 ..> c0042: `_worker_configuration() constructs FactoryError`
- c0040 ..> c0042: `main() constructs FactoryError`
- c0040 ..> c0042: `select_repositories() constructs FactoryError`
- c0041 ..> c0012: `load_configuration() calls load()`
- c0041 ..> c0012: `load_configuration() constructs TomlConfigurationStore`
- c0041 ..> c0024: `type in load_configuration`
- c0041 ..> c0042: `load_configuration() constructs FactoryError`
- c0043 --> c0046: `field source`
- c0045 --> c0046: `field work_source`
- c0047 ..> c0043: `type in list_issues`
- c0047 ..> c0044: `type in create_label`
- c0047 ..> c0044: `type in list_labels`
- c0047 ..> c0046: `type in check_access`
- c0047 ..> c0046: `type in create_label`
- c0047 ..> c0046: `type in list_issues`
- c0047 ..> c0046: `type in list_labels`

## Type key

- Type1: `dict[str, str] | None`
- Type2: `dict | None`
- Type3: `str | None`
- Type4: `subprocess.Popen | None`
- Type5: `dict[tuple[str, Path], list[str]]`
- Type6: `Path | None`
- Type7: `tuple[Path, list[dict]]`
- Type8: `list | None`
- Type9: `dict[str, list[str]]`
- Type10: `FactoryConfiguration | None`
- Type11: `dict[str, str]`
- Type12: `tuple[Label, ...]`
- Type13: `tuple[Issue, ...]`
- Type14: `tuple[str, ...]`
- Type15: `tuple[Path, ...]`
- Type16: `float | None`
- Type17: `tuple[RepositoryReference, ...]`
- Type18: `ForgetfulConnection | None`
- Type19: `int | None`
- Type20: `Callable[[list[str]], None]`
- Type21: `Callable[[str, str], bool]`
- Type22: `list[Path] | None`
- Type23: `list[str] | None`
- Type24: `dict[str, RepositoryReference]`
- Type25: `dict[WorkSource, tuple[Label, ...]]`
- Type26: `Callable[[], FactoryConfiguration | None]`
- Type27: `Callable[[], bool]`
- Type28: `Callable[[str], None]`
- Type29: `tuple[Issue, ...] | None`
- Type30: `list[str] | tuple[str, ...]`
- Type31: `str | Path`

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
- Signature7: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, scaffold:
  ScaffoldIssue) unknown`
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
