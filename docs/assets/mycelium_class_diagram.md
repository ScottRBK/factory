# Mermaid class diagrams

Declared types and signatures; unknown types are `unknown`. Receivers are omitted.
Fields are associations, not lifetime ownership. Calls are static heuristic estimates.
Members and connections within each view are uncapped.
Parallel arrows are summarized.
Cross-diagram relationships are retained in the complete relationship list.

Included: 68 boxes. Calls without in-scope endpoints: 0.

## Test filtering

Mode: exclude.
Saved detector version: 2.
Test paths: `tests`.
Keep paths: none.
Calls removed by test filtering: 3407. Type relationships removed: 52.

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
- `tests/test_foreman_setup_repair.py`: 31 source occurrences (test-path).
- `tests/test_init.py`: 43 source occurrences (test-path).
- `tests/test_init_launch.py`: 13 source occurrences (test-path).
- `tests/test_installer_onboarding.py`: 20 source occurrences (test-path).
- `tests/test_local_skills.py`: 21 source occurrences (test-path).
- `tests/test_managed_watcher_alerts.py`: 10 source occurrences (test-path).
- `tests/test_native_assisted_reload.py`: 2 source occurrences (test-path).
- `tests/test_native_roles.py`: 4 source occurrences (test-path).
- `tests/test_native_workers.py`: 2 source occurrences (test-path).
- `tests/test_normalized_lifecycle.py`: 8 source occurrences (test-path).
- `tests/test_owner_profiles.py`: 10 source occurrences (test-path).
- `tests/test_planning_setup.py`: 13 source occurrences (test-path).
- `tests/test_planning_watch.py`: 29 source occurrences (test-path).
- `tests/test_profile_recovery.py`: 32 source occurrences (test-path).
- `tests/test_profiles.py`: 34 source occurrences (test-path).
- `tests/test_project_onboarding.py`: 17 source occurrences (test-path).
- `tests/test_research_configuration.py`: 8 source occurrences (test-path).
- `tests/test_review_regressions.py`: 56 source occurrences (test-path).
- `tests/test_setup_completion.py`: 29 source occurrences (test-path).
- `tests/test_shared_pi.py`: 23 source occurrences (test-path).
- `tests/test_watch.py`: 52 source occurrences (test-path).
- `tests/test_watch_lock.py`: 6 source occurrences (test-path).
- `tests/test_watcher_alerts.py`: 62 source occurrences (test-path).
- `tests/test_watcher_cancellation.py`: 5 source occurrences (test-path).
- `tests/test_watcher_followup.py`: 35 source occurrences (test-path).
- `tests/test_watcher_guidance.py`: 4 source occurrences (test-path).
- `tests/test_worker_configuration.py`: 18 source occurrences (test-path).
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
    class c0014["src/forgetful_factory/adapters/filesystem/git_repositories.py"] {
        <<module>>
        -_resolve_repository(path: Path) Path
    }
    class c0015["GitWorktrees"] {
        <<class>>
        +inspect(repository: str, branch: str, path: str, remote: str) None
        -_repository_entries(repository: str, remote: str) Type7
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
        -_verify_removed(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        -_inspect(repository: str, branch: str, path: str, recorded: bool, remote: str) Type8
    }
    class c0016["src/forgetful_factory/adapters/filesystem/git_worktrees.py"] {
        <<module>>
        -_read_git(arguments: list[str]) str
        -_worktree_entries(output: str) list[dict]
    }
    class c0017["src/forgetful_factory/adapters/filesystem/resource_files.py"] {
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
    class c0018["src/forgetful_factory/adapters/filesystem/selected_skills.py"] {
        <<module>>
        +selected_skill_files(values: list[str]) list[Path]
    }
    class c0019["TomlConfigurationStore"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +path: unknown
        +load() Type9
        +save(configuration: FactoryConfiguration) None
    }
    class c0020["src/forgetful_factory/adapters/filesystem/toml_configuration.py"] {
        <<module>>
        +quote(value: str) str
    }
    class c0021["WorkspaceWatchLease"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +directory: unknown
        +hold() Iterator[None]
        -_hold_directory(directory: Path) Iterator[None]
    }
    class c0022["WorkerProfiles"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +directory: unknown
        +prepare(choices: InitialAgentChoices) None
    }
    class c0023["src/forgetful_factory/adapters/forgetful/authentication.py"] {
        <<module>>
        +uses_browser_login(connection: ForgetfulConnection) bool
    }
    class c0024["AgentForgetfulConnection"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +role: unknown
        +login(connection: ForgetfulConnection) None
        -_environment(connection: ForgetfulConnection) Type10
        +command(connection: ForgetfulConnection, arguments: list[str]) dict
        +call(connection: ForgetfulConnection, tool: str, arguments: unknown) dict
        +projects(connection: ForgetfulConnection) list[dict]
        +create_project(connection: ForgetfulConnection, name: str) int
        +check(connection: ForgetfulConnection, execution_enabled: bool) None
    }
    class c0025["src/forgetful_factory/adapters/forgetful/connection.py"] {
        <<module>>
        +role_environment(Signature4)
        -_catalog_tools(catalog: object) dict
    }
    class c0026["ForgetfulPlanning"] {
        <<class>>
        -__init__(Signature5)
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
    class c0027["src/forgetful_factory/adapters/forgetful/planning.py"] {
        <<module>>
        -_positive_id(value: object) bool
    }
    class c0028["GitHubWorkTracking"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
        -_api(source: WorkSource, suffix: str, #42;arguments: str) object
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type11
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type13) Type12
        -_validate_issue(source: WorkSource, item: dict) None
    }
    class c0029["HostDependencies"] {
        <<class>>
        -__init__(workspace: Path) unknown
        +workspace: unknown
        +runtime: unknown
        +pi_ready(pi_home: str) bool
        -_ubuntu_tmux() bool
        +description(command: str) Type3
        -_environment(extra: Type2) Type10
        -_run(args: list[str], cwd: Path, interactive: bool, extra_env: Type2) str
        -_check_uv() None
        -_forgetful_python() str
        -_install_tmux() None
        -_install_role_runtime() None
        +install(command: str) None
    }
    class c0030["src/forgetful_factory/adapters/host_dependencies.py"] {
        <<module>>
        +executable_path(workspace: Path) str
        +sync_fingerprint(inputs: Type14) str
        +runtime_ready(runtime: Path, inputs: Type14, probe: str) bool
    }
    class c0031["src/forgetful_factory/adapters/sensitive_command.py"] {
        <<module>>
        +run_owned(args: list[str], cwd: Path, env: Type10, login: bool, timeout: Type15) str
    }
    class c0032["FactoryConfiguration"] {
        <<class>>
        +watcher_label: Type13
        +foreman_agent_file: str
        +repository: Type16
        +forgetful: Type17
        +execution_enabled: bool
    }
    class c0033["ForgetfulConnection"] {
        <<class>>
        +method: str
        +instance: str
        +executable: str
        +database: Type3
        +server: Type3
        +project_id: Type18
        +validate() None
        -_validate_server() None
    }
    class c0034["src/forgetful_factory/application/configuration.py"] {
        <<module>>
        +loopback_host(host: str) bool
        +connection_from_mapping(data: object) Type17
        +nonblank(value: object, field: str) str
        +validate(configuration: FactoryConfiguration) None
        +from_mapping(data: dict) FactoryConfiguration
        +unique_labels(labels: list[str]) Type13
    }
    class c0035["InitialAgentChoices"] {
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
        +implementation_skills: Type13
        +review_skills: Type13
        +research_agent_model: Type3
        +research_agent_harness: Type3
        +research_agent_effort: Type3
        +execution_enabled: bool
    }
    class c0036["src/forgetful_factory/application/initial_agent_choices.py"] {
        <<module>>
        +validate_role_app(harness: str, role: str) None
        +validate_workers(configuration: InitialAgentChoices) None
        +skill_paths(data: dict, field: str) Type13
        +validate_initial_agents(configuration: InitialAgentChoices) None
    }
    class c0037["InitialiseFactory"] {
        <<class>>
        -__init__(Signature6)
        +tracking: unknown
        +storage: unknown
        +repositories: unknown
        +sources: unknown
        +profile: unknown
        +prepare_foreman(connection: ForgetfulConnection, install: Type19, confirm: Type20) None
        +check_foreman(config: FactoryConfiguration, login: bool) str
        +load_existing(paths: Type21, labels: Type22) Type9
        +discover(workspace: Path) list[Path]
        +inspect(paths: list[Path]) Type23
        +configure(paths: list[Path], labels: list[str], agent_file: str) FactoryConfiguration
        -_preflight(config: FactoryConfiguration) Type24
        -_ensure_label(source: WorkSource, name: str, existing: set[str]) str
        +initialise(config: FactoryConfiguration, before_writes: Type25, save: bool) list[str]
    }
    class c0038["ConfigurationStore"] {
        <<class>>
        +load() Type9
        +save(configuration: FactoryConfiguration) None
    }
    class c0039["ForemanProfile"] {
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
    class c0040["ForemanTerminal"] {
        <<class>>
        +startup_hint() str
        +start() None
        +send(message: str) None
        +wait(interval: float) None
        +close() None
    }
    class c0041["LocalRepositories"] {
        <<class>>
        +origin(path: Path) str
        +discover(workspace: Path) list[Path]
    }
    class c0042["Planning"] {
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
    class c0043["PlanningReadError"] {
        <<class>>
    }
    class c0044["WatchLease"] {
        <<class>>
        +hold() AbstractContextManager[None]
    }
    class c0045["WorkSourceResolver"] {
        <<class>>
        +source_from_remote(remote: str) WorkSource
    }
    class c0046["WorktreeProblem"] {
        <<class>>
        -__init__(code: str, diagnostic: str, path: Type3) unknown
        +code: unknown
        +paths: unknown
    }
    class c0047["WorktreeReadError"] {
        <<class>>
    }
    class c0048["Worktrees"] {
        <<class>>
        +inspect(repository: str, branch: str, path: str, remote: str) None
        +ensure(repository: str, branch: str, path: str, recorded: bool, remote: str) None
        +verify_removed(repository: str, branch: str, path: str, remote: str) None
    }
    class c0049["ScaffoldIssue"] {
        <<class>>
        -__init__(Signature7)
        +planning: unknown
        +worktrees: unknown
        +workspace: unknown
        +config: unknown
        +repositories: unknown
        +sources: unknown
        +check() None
        +check_repository(repository: RepositoryReference) None
        -_check_source(repository: RepositoryReference) None
        +prepare(issue: Issue) Type1
        -_repository(source: WorkSource) RepositoryReference
        -_initial_mappings(issue: Issue) list[dict]
        +preflight(issue: Issue) None
        -_prepare_plan(issue: Issue, plan: dict) Type1
        +lookup(issue: Issue) Type18
        -_create_plan(issue: Issue) dict
        +unfinished() list[dict]
        +recover(plan_id: int, external_ref: str, issue: Type27, task_ids: Type28) Type26
        -_snapshot(context: dict, external_ref: str) Issue
        -_is_unfinished_factory_plan(summary: dict, sources: set[str]) bool
        -_active(plan: dict) bool
        -_context(plan: dict) dict
        -_ownership(plan_id: int, external_ref: str) list[dict]
        -_ensure_worktrees(mappings: list[dict], recorded: bool) None
        -_ensure_mapping(repository: unknown, mapping: dict, recorded: bool) None
    }
    class c0050["src/forgetful_factory/application/scaffold_issue.py"] {
        <<module>>
        -_cleanup_state(mapping: dict) Type3
    }
    class c0051["BlockedWork"] {
        <<class>>
        +reference: str
        +plan_id: Type18
        +issue: Type27
        +task_ids: Type28
        +recovered: bool
        +setup_paths: Type13
        +setup_cause: Type3
    }
    class c0052["WatchFactory"] {
        <<class>>
        -__init__(Signature8)
        +tracking: unknown
        +terminal: unknown
        +scaffold: unknown
        +run(Signature9)
        -_watch(Signature10)
        -_alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) None
        -_submit(Signature11)
        -_read_issues(source: WorkSource, labels: Type13, alerts: WatcherAlerts) Type31
    }
    class c0053["IntakeProblem"] {
        <<class>>
    }
    class c0054["RepositoryProblem"] {
        <<class>>
    }
    class c0055["ScaffoldProblem"] {
        <<class>>
        -__init__(Signature12)
        +code: unknown
        +plan_id: unknown
        +plan_ids: unknown
        +task_ids: unknown
        +candidate_task_ids: unknown
        +paths: unknown
        +cause: unknown
    }
    class c0056["ScaffoldReadProblem"] {
        <<class>>
    }
    class c0057["UncertainScaffold"] {
        <<class>>
    }
    class c0058["WatcherAlerts"] {
        <<class>>
        -__init__(terminal: unknown, report_error: unknown) unknown
        +terminal: unknown
        +report_error: unknown
        +sent: Type10
        +last_diagnostic: Type10
        +clear(subject: str) None
        +send(Signature13)
        +last_diagnostic#91;subject#93;: unknown
        +sent#91;subject#93;: unknown
    }
    class c0059["src/forgetful_factory/cli/bootstrap.py"] {
        <<module>>
        +build_initialiser(workspace: Path) InitialiseFactory
        +build_watcher(Signature14)
        +prepare_foreman_launch(Signature15)
    }
    class c0060["src/forgetful_factory/cli/main.py"] {
        <<module>>
        +select_repositories(application: InitialiseFactory, workspace: Path) list[Path]
        -_parse_arguments() argparse.Namespace
        -_configure_new_factory(Signature16)
        -_check_existing_connection(Signature17)
        -_connection(Signature18)
        -_prepare_foreman(Signature19)
        -_print_models(models: list[str]) None
        -_select_numbered(label: str, choices: Type33, show_choices: bool, prompt: Type3) str
        -_select_model(Signature20)
        -_confirm_pi_home(home: str, args: argparse.Namespace) bool
        -_install_missing(commands: list[str]) None
        -_safe_diagnostic(message: str) str
        -_choose_existing(args: argparse.Namespace) bool
        -_watch(args: argparse.Namespace, workspace: Path) int
        -_foreman(args: argparse.Namespace, workspace: Path) int
        -_watch_locked(args: argparse.Namespace, workspace: Path) int
        -_listed_project_id(answer: str, projects: list[dict]) int
        -_select_project(Signature21)
        -_owner_choices(Signature22)
        -_worker_arguments(args: argparse.Namespace) dict
        -_research_choices(args: unknown, config: unknown) unknown
        -_prompt_worker(role: str, discover_models: unknown) dict
        -_prompt_workers(discover_models: unknown) dict
        -_worker_choices(Signature23)
        -_complete_setup(Signature24)
        -_initialise(args: argparse.Namespace, workspace: Path) int
        -_offer_factory_launch(args: argparse.Namespace, workspace: Path) int
        -_initialise_locked(args: argparse.Namespace, workspace: Path) Type34
        -_launch_setup_foreman(Signature25)
        +main() int
    }
    class c0061["src/forgetful_factory/configuration.py"] {
        <<module>>
        +load_configuration(workspace: Type35) FactoryConfiguration
    }
    class c0062["FactoryError"] {
        <<class>>
    }
    class c0063["Issue"] {
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
    class c0064["Label"] {
        <<class>>
        +name: str
    }
    class c0065["RepositoryReference"] {
        <<class>>
        +local_dir: str
        +remote: str
        +work_source: WorkSource
    }
    class c0066["WorkSource"] {
        <<class>>
        +provider: str
        +reference: str
    }
    class c0067["WorkTrackingService"] {
        <<class>>
        +check_access(source: WorkSource) None
        +list_labels(source: WorkSource) Type11
        +create_label(source: WorkSource, label: Label) None
        +list_issues(source: WorkSource, labels: Type13) Type12
    }
    c0000 ..> c0000 : 2 relationships (see list)
    c0000 ..> c0006 : close() calls close()
    c0000 ..> c0062 : 2 relationships (see list)
    c0001 ..> c0000 : 6 relationships (see list)
    c0001 ..> c0001 : 9 relationships (see list)
    c0001 ..> c0026 : 3 relationships (see list)
    c0002 ..> c0011 : main() calls list_models()
    c0003 ..> c0000 : 6 relationships (see list)
    c0003 ..> c0003 : 10 relationships (see list)
    c0003 ..> c0005 : run() calls read_state()
    c0003 ..> c0012 : __init__() calls runtime_directory()
    c0003 ..> c0017 : save() calls replace_generated_json()
    c0003 ..> c0020 : 2 relationships (see list)
    c0003 ..> c0026 : 2 relationships (see list)
    c0003 ..> c0062 : 6 relationships (see list)
    c0004 ..> c0003 : 2 relationships (see list)
    c0004 ..> c0026 : main() calls create_task()
    c0005 ..> c0000 : 2 relationships (see list)
    c0005 ..> c0003 : 2 relationships (see list)
    c0005 ..> c0005 : 3 relationships (see list)
    c0005 ..> c0012 : 3 relationships (see list)
    c0005 ..> c0017 : read_state() calls read_generated_json()
    c0005 ..> c0020 : request() calls quote()
    c0005 ..> c0062 : 5 relationships (see list)
    c0006 ..> c0000 : close() calls close()
    c0006 ..> c0006 : 5 relationships (see list)
    c0006 ..> c0062 : 4 relationships (see list)
    c0007 ..> c0003 : run_command() calls run()
    c0007 ..> c0062 : run_command() constructs FactoryError
    c0008 ..> c0008 : 3 relationships (see list)
    c0008 ..> c0034 : 3 relationships (see list)
    c0008 ..> c0062 : 2 relationships (see list)
    c0009 ..> c0009 : 2 relationships (see list)
    c0009 ..> c0010 : prepare() calls selected_resources()
    c0009 ..> c0011 : prepare() calls prepare()
    c0009 ..> c0017 : 3 relationships (see list)
    c0009 ..> c0022 : __init__() constructs WorkerProfiles
    c0009 ..> c0032 : 2 relationships (see list)
    c0009 ..> c0062 : 3 relationships (see list)
    c0011 ..> c0008 : selected_launch() calls foreman_launch()
    c0011 ..> c0009 : 4 relationships (see list)
    c0011 ..> c0011 : 22 relationships (see list)
    c0011 ..> c0017 : 11 relationships (see list)
    c0011 ..> c0018 : selected_launch() calls selected_skill_files()
    c0011 ..> c0020 : require_pi_home() calls quote()
    c0011 ..> c0023 : uses_browser_login() calls uses_browser_login()
    c0011 ..> c0024 : 8 relationships (see list)
    c0011 ..> c0025 : list_models() calls role_environment()
    c0011 ..> c0029 : 6 relationships (see list)
    c0011 ..> c0030 : 3 relationships (see list)
    c0011 ..> c0031 : list_models() calls run_owned()
    c0011 ..> c0032 : 4 relationships (see list)
    c0011 ..> c0033 : 9 relationships (see list)
    c0011 ..> c0062 : 14 relationships (see list)
    c0012 ..> c0017 : runtime_directory() calls check_real_path()
    c0012 ..> c0062 : runtime_directory() constructs FactoryError
    c0013 ..> c0007 : origin() calls run_command()
    c0013 ..> c0014 : origin() calls _resolve_repository()
    c0013 ..> c0062 : origin() constructs FactoryError
    c0014 ..> c0062 : _resolve_repository() constructs FactoryError
    c0015 ..> c0007 : ensure() calls run_command()
    c0015 ..> c0015 : 5 relationships (see list)
    c0015 ..> c0016 : 3 relationships (see list)
    c0015 ..> c0046 : 3 relationships (see list)
    c0015 ..> c0047 : 3 relationships (see list)
    c0015 ..> c0062 : ensure() constructs FactoryError
    c0016 ..> c0007 : _read_git() calls run_command()
    c0016 ..> c0047 : _read_git() constructs WorktreeReadError
    c0017 ..> c0000 : _generated_parent() calls close()
    c0017 ..> c0017 : 9 relationships (see list)
    c0017 ..> c0019 : read_generated_json() calls load()
    c0017 ..> c0062 : 6 relationships (see list)
    c0018 ..> c0062 : selected_skill_files() constructs FactoryError
    c0019 ..> c0000 : 2 relationships (see list)
    c0019 ..> c0020 : save() calls quote()
    c0019 ..> c0032 : 2 relationships (see list)
    c0019 ..> c0034 : load() calls from_mapping()
    c0019 ..> c0038 : load() calls load()
    c0019 ..> c0062 : 2 relationships (see list)
    c0021 ..> c0000 : _hold_directory() calls close()
    c0021 ..> c0021 : hold() calls _hold_directory()
    c0021 ..> c0062 : _hold_directory() constructs FactoryError
    c0022 ..> c0017 : 3 relationships (see list)
    c0022 ..> c0035 : type in prepare
    c0023 ..> c0005 : uses_browser_login() calls request()
    c0023 ..> c0033 : type in uses_browser_login
    c0024 ..> c0024 : 7 relationships (see list)
    c0024 ..> c0025 : 2 relationships (see list)
    c0024 ..> c0031 : 2 relationships (see list)
    c0024 ..> c0033 : 7 relationships (see list)
    c0024 ..> c0062 : 5 relationships (see list)
    c0025 ..> c0030 : role_environment() calls executable_path()
    c0025 ..> c0033 : type in role_environment
    c0026 ..> c0011 : check() calls check()
    c0026 ..> c0024 : 2 relationships (see list)
    c0026 ..> c0026 : 12 relationships (see list)
    c0026 ..> c0027 : 3 relationships (see list)
    c0026 ..> c0033 : type in __init__
    c0026 ..> c0043 : 4 relationships (see list)
    c0028 ..> c0007 : _api() calls run_command()
    c0028 ..> c0028 : 5 relationships (see list)
    c0028 ..> c0062 : 7 relationships (see list)
    c0028 ..> c0063 : 2 relationships (see list)
    c0028 ..> c0064 : 3 relationships (see list)
    c0028 ..> c0066 : 8 relationships (see list)
    c0029 ..> c0017 : install() calls write_new()
    c0029 ..> c0029 : 15 relationships (see list)
    c0029 ..> c0030 : 3 relationships (see list)
    c0029 ..> c0031 : 4 relationships (see list)
    c0029 ..> c0062 : 6 relationships (see list)
    c0030 ..> c0030 : runtime_ready() calls sync_fingerprint()
    c0030 ..> c0031 : runtime_ready() calls run_owned()
    c0031 ..> c0000 : 2 relationships (see list)
    c0031 ..> c0062 : run_owned() constructs FactoryError
    c0032 --> c0033 : field forgetful
    c0032 --> c0065 : field repository
    c0033 ..> c0034 : 2 relationships (see list)
    c0033 ..> c0062 : _validate_server() constructs FactoryError
    c0034 ..> c0032 : 3 relationships (see list)
    c0034 ..> c0033 : 3 relationships (see list)
    c0034 ..> c0034 : 5 relationships (see list)
    c0034 ..> c0062 : 4 relationships (see list)
    c0034 ..> c0065 : from_mapping() constructs RepositoryReference
    c0034 ..> c0066 : from_mapping() constructs WorkSource
    c0036 ..> c0034 : 3 relationships (see list)
    c0036 ..> c0035 : 2 relationships (see list)
    c0036 ..> c0036 : 3 relationships (see list)
    c0036 ..> c0062 : 4 relationships (see list)
    c0037 ..> c0003 : initialise() calls save()
    c0037 ..> c0009 : prepare_foreman() calls prepare()
    c0037 ..> c0011 : 5 relationships (see list)
    c0037 ..> c0013 : 3 relationships (see list)
    c0037 ..> c0019 : load_existing() calls load()
    c0037 ..> c0028 : 5 relationships (see list)
    c0037 ..> c0032 : 6 relationships (see list)
    c0037 ..> c0033 : 2 relationships (see list)
    c0037 ..> c0034 : 2 relationships (see list)
    c0037 ..> c0037 : 3 relationships (see list)
    c0037 ..> c0038 : type in __init__
    c0037 ..> c0039 : type in __init__
    c0037 ..> c0041 : type in __init__
    c0037 ..> c0045 : type in __init__
    c0037 ..> c0062 : 5 relationships (see list)
    c0037 ..> c0064 : 2 relationships (see list)
    c0037 ..> c0065 : 2 relationships (see list)
    c0037 ..> c0066 : 2 relationships (see list)
    c0037 ..> c0067 : type in __init__
    c0038 ..> c0032 : 2 relationships (see list)
    c0039 ..> c0032 : 3 relationships (see list)
    c0039 ..> c0033 : 8 relationships (see list)
    c0039 ..> c0035 : type in prepare_roles
    c0043 --|> c0062 : inherits
    c0045 ..> c0066 : type in source_from_remote
    c0046 ..> c0000 : __init__() calls __init__()
    c0046 --|> c0062 : inherits
    c0047 --|> c0062 : inherits
    c0049 ..> c0011 : check() calls check()
    c0049 ..> c0013 : check_repository() calls origin()
    c0049 ..> c0015 : 3 relationships (see list)
    c0049 ..> c0026 : 10 relationships (see list)
    c0049 ..> c0028 : _check_source() calls source_from_remote()
    c0049 ..> c0032 : type in __init__
    c0049 ..> c0041 : type in __init__
    c0049 ..> c0042 : type in __init__
    c0049 ..> c0045 : type in __init__
    c0049 ..> c0048 : type in __init__
    c0049 ..> c0049 : 25 relationships (see list)
    c0049 ..> c0050 : _ensure_mapping() calls _cleanup_state()
    c0049 ..> c0053 : preflight() constructs IntakeProblem
    c0049 ..> c0054 : 2 relationships (see list)
    c0049 ..> c0055 : 10 relationships (see list)
    c0049 ..> c0056 : 5 relationships (see list)
    c0049 ..> c0057 : 4 relationships (see list)
    c0049 ..> c0062 : _is_unfinished_factory_plan() constructs FactoryError
    c0049 ..> c0063 : 9 relationships (see list)
    c0049 ..> c0065 : 3 relationships (see list)
    c0049 ..> c0066 : 3 relationships (see list)
    c0050 ..> c0055 : _cleanup_state() constructs ScaffoldProblem
    c0051 --> c0063 : field issue
    c0052 ..> c0000 : 8 relationships (see list)
    c0052 ..> c0009 : _watch() calls prepare()
    c0052 ..> c0011 : _watch() calls check()
    c0052 ..> c0028 : _read_issues() calls list_issues()
    c0052 ..> c0032 : 2 relationships (see list)
    c0052 ..> c0040 : type in __init__
    c0052 ..> c0049 : 5 relationships (see list)
    c0052 ..> c0051 : 2 relationships (see list)
    c0052 ..> c0052 : 4 relationships (see list)
    c0052 ..> c0055 : 2 relationships (see list)
    c0052 ..> c0058 : 5 relationships (see list)
    c0052 ..> c0062 : _read_issues() constructs FactoryError
    c0052 ..> c0063 : 2 relationships (see list)
    c0052 ..> c0066 : 2 relationships (see list)
    c0052 ..> c0067 : type in __init__
    c0053 --|> c0055 : inherits
    c0054 --|> c0055 : inherits
    c0055 --|> c0062 : inherits
    c0056 --|> c0055 : inherits
    c0057 --|> c0055 : inherits
    c0058 ..> c0000 : 2 relationships (see list)
    c0058 ..> c0062 : type in send
    c0059 ..> c0006 : build_watcher() constructs AgentShellTerminal
    c0059 ..> c0011 : 5 relationships (see list)
    c0059 ..> c0013 : 2 relationships (see list)
    c0059 ..> c0015 : build_watcher() constructs GitWorktrees
    c0059 ..> c0019 : build_initialiser() constructs TomlConfigurationStore
    c0059 ..> c0025 : prepare_foreman_launch() calls role_environment()
    c0059 ..> c0026 : build_watcher() constructs ForgetfulPlanning
    c0059 ..> c0028 : 3 relationships (see list)
    c0059 ..> c0032 : 2 relationships (see list)
    c0059 ..> c0037 : 2 relationships (see list)
    c0059 ..> c0049 : build_watcher() constructs ScaffoldIssue
    c0059 ..> c0052 : 2 relationships (see list)
    c0059 ..> c0059 : build_watcher() calls prepare_foreman_launch()
    c0059 ..> c0062 : 2 relationships (see list)
    c0060 ..> c0000 : _watch_locked() constructs BorrowedForemanTerminal
    c0060 ..> c0003 : _watch_locked() calls run()
    c0060 ..> c0005 : 12 relationships (see list)
    c0060 ..> c0011 : 12 relationships (see list)
    c0060 ..> c0013 : select_repositories() calls discover()
    c0060 ..> c0015 : _configure_new_factory() calls inspect()
    c0060 ..> c0019 : _initialise_locked() calls load()
    c0060 ..> c0020 : 6 relationships (see list)
    c0060 ..> c0021 : 6 relationships (see list)
    c0060 ..> c0032 : 2 relationships (see list)
    c0060 ..> c0033 : 6 relationships (see list)
    c0060 ..> c0035 : 4 relationships (see list)
    c0060 ..> c0036 : _initialise_locked() calls validate_initial_agents()
    c0060 ..> c0037 : 10 relationships (see list)
    c0060 ..> c0059 : 4 relationships (see list)
    c0060 ..> c0060 : 34 relationships (see list)
    c0060 ..> c0061 : 3 relationships (see list)
    c0060 ..> c0062 : 17 relationships (see list)
    c0061 ..> c0019 : 2 relationships (see list)
    c0061 ..> c0032 : type in load_configuration
    c0061 ..> c0062 : load_configuration() constructs FactoryError
    c0063 --> c0066 : field source
    c0065 --> c0066 : field work_source
    c0067 ..> c0063 : type in list_issues
    c0067 ..> c0064 : 2 relationships (see list)
    c0067 ..> c0066 : 4 relationships (see list)
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
- c0013: `GitRepositories` — `src/forgetful_factory/adapters/filesystem/git_repositories.py`:15
- c0014: `src/forgetful_factory/adapters/filesystem/git_repositories.py` —
  `src/forgetful_factory/adapters/filesystem/git_repositories.py`:1
- c0015: `GitWorktrees` — `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:29
- c0016: `src/forgetful_factory/adapters/filesystem/git_worktrees.py` —
  `src/forgetful_factory/adapters/filesystem/git_worktrees.py`:1
- c0017: `src/forgetful_factory/adapters/filesystem/resource_files.py` —
  `src/forgetful_factory/adapters/filesystem/resource_files.py`:1
- c0018: `src/forgetful_factory/adapters/filesystem/selected_skills.py` —
  `src/forgetful_factory/adapters/filesystem/selected_skills.py`:1
- c0019: `TomlConfigurationStore` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:20
- c0020: `src/forgetful_factory/adapters/filesystem/toml_configuration.py` —
  `src/forgetful_factory/adapters/filesystem/toml_configuration.py`:1
- c0021: `WorkspaceWatchLease` — `src/forgetful_factory/adapters/filesystem/watch_lease.py`:10
- c0022: `WorkerProfiles` — `src/forgetful_factory/adapters/filesystem/worker_profiles.py`:15
- c0023: `src/forgetful_factory/adapters/forgetful/authentication.py` —
  `src/forgetful_factory/adapters/forgetful/authentication.py`:1
- c0024: `AgentForgetfulConnection` — `src/forgetful_factory/adapters/forgetful/connection.py`:52
- c0025: `src/forgetful_factory/adapters/forgetful/connection.py` —
  `src/forgetful_factory/adapters/forgetful/connection.py`:1
- c0026: `ForgetfulPlanning` — `src/forgetful_factory/adapters/forgetful/planning.py`:13
- c0027: `src/forgetful_factory/adapters/forgetful/planning.py` —
  `src/forgetful_factory/adapters/forgetful/planning.py`:1
- c0028: `GitHubWorkTracking` — `src/forgetful_factory/adapters/github/work_tracking.py`:8
- c0029: `HostDependencies` — `src/forgetful_factory/adapters/host_dependencies.py`:52
- c0030: `src/forgetful_factory/adapters/host_dependencies.py` —
  `src/forgetful_factory/adapters/host_dependencies.py`:1
- c0031: `src/forgetful_factory/adapters/sensitive_command.py` —
  `src/forgetful_factory/adapters/sensitive_command.py`:1
- c0032: `FactoryConfiguration` — `src/forgetful_factory/application/configuration.py`:82
- c0033: `ForgetfulConnection` — `src/forgetful_factory/application/configuration.py`:11
- c0034: `src/forgetful_factory/application/configuration.py` —
  `src/forgetful_factory/application/configuration.py`:1
- c0035: `InitialAgentChoices` — `src/forgetful_factory/application/initial_agent_choices.py`:9
- c0036: `src/forgetful_factory/application/initial_agent_choices.py` —
  `src/forgetful_factory/application/initial_agent_choices.py`:1
- c0037: `InitialiseFactory` — `src/forgetful_factory/application/initialise_factory.py`:18
- c0038: `ConfigurationStore` — `src/forgetful_factory/application/ports/configuration_store.py`:6
- c0039: `ForemanProfile` — `src/forgetful_factory/application/ports/foreman_profile.py`:8
- c0040: `ForemanTerminal` — `src/forgetful_factory/application/ports/foreman_terminal.py`:4
- c0041: `LocalRepositories` — `src/forgetful_factory/application/ports/local_repositories.py`:5
- c0042: `Planning` — `src/forgetful_factory/application/ports/planning.py`:10
- c0043: `PlanningReadError` — `src/forgetful_factory/application/ports/planning.py`:6
- c0044: `WatchLease` — `src/forgetful_factory/application/ports/watch_lease.py`:5
- c0045: `WorkSourceResolver` — `src/forgetful_factory/application/ports/work_source_resolver.py`:6
- c0046: `WorktreeProblem` — `src/forgetful_factory/application/ports/worktrees.py`:10
- c0047: `WorktreeReadError` — `src/forgetful_factory/application/ports/worktrees.py`:6
- c0048: `Worktrees` — `src/forgetful_factory/application/ports/worktrees.py`:19
- c0049: `ScaffoldIssue` — `src/forgetful_factory/application/scaffold_issue.py`:47
- c0050: `src/forgetful_factory/application/scaffold_issue.py` —
  `src/forgetful_factory/application/scaffold_issue.py`:1
- c0051: `BlockedWork` — `src/forgetful_factory/application/watch_factory.py`:22
- c0052: `WatchFactory` — `src/forgetful_factory/application/watch_factory.py`:32
- c0053: `IntakeProblem` — `src/forgetful_factory/application/watcher_problems.py`:104
- c0054: `RepositoryProblem` — `src/forgetful_factory/application/watcher_problems.py`:100
- c0055: `ScaffoldProblem` — `src/forgetful_factory/application/watcher_problems.py`:80
- c0056: `ScaffoldReadProblem` — `src/forgetful_factory/application/watcher_problems.py`:96
- c0057: `UncertainScaffold` — `src/forgetful_factory/application/watcher_problems.py`:108
- c0058: `WatcherAlerts` — `src/forgetful_factory/application/watcher_problems.py`:112
- c0059: `src/forgetful_factory/cli/bootstrap.py` — `src/forgetful_factory/cli/bootstrap.py`:1
- c0060: `src/forgetful_factory/cli/main.py` — `src/forgetful_factory/cli/main.py`:1
- c0061: `src/forgetful_factory/configuration.py` — `src/forgetful_factory/configuration.py`:1
- c0062: `FactoryError` — `src/forgetful_factory/domain/models.py`:4
- c0063: `Issue` — `src/forgetful_factory/domain/models.py`:27
- c0064: `Label` — `src/forgetful_factory/domain/models.py`:22
- c0065: `RepositoryReference` — `src/forgetful_factory/domain/models.py`:15
- c0066: `WorkSource` — `src/forgetful_factory/domain/models.py`:9
- c0067: `WorkTrackingService` — `src/forgetful_factory/domain/services/work_tracking.py`:6

## Relationships

- c0000 ..> c0000: `send() calls _request()`
- c0000 ..> c0000: `start() calls _request()`
- c0000 ..> c0006: `close() calls close()`
- c0000 ..> c0062: `_request() constructs FactoryError`
- c0000 ..> c0062: `wait() constructs FactoryError`
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
- c0001 ..> c0026: `control() calls create_task()`
- c0001 ..> c0026: `main() calls create_task()`
- c0001 ..> c0026: `serve() calls create_task()`
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
- c0003 ..> c0017: `save() calls replace_generated_json()`
- c0003 ..> c0020: `observe() calls quote()`
- c0003 ..> c0020: `run() calls quote()`
- c0003 ..> c0026: `run() calls create_task()`
- c0003 ..> c0026: `start_watcher() calls create_task()`
- c0003 ..> c0062: `control() constructs FactoryError`
- c0003 ..> c0062: `observe() constructs FactoryError`
- c0003 ..> c0062: `reap_watcher() constructs FactoryError`
- c0003 ..> c0062: `relay() constructs FactoryError`
- c0003 ..> c0062: `run() constructs FactoryError`
- c0003 ..> c0062: `start_watcher() constructs FactoryError`
- c0004 ..> c0003: `main() calls run()`
- c0004 ..> c0003: `main() constructs ForemanOwner`
- c0004 ..> c0026: `main() calls create_task()`
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
- c0005 ..> c0017: `read_state() calls read_generated_json()`
- c0005 ..> c0020: `request() calls quote()`
- c0005 ..> c0062: `_reply() constructs FactoryError`
- c0005 ..> c0062: `enter_terminal() constructs FactoryError`
- c0005 ..> c0062: `read_state() constructs FactoryError`
- c0005 ..> c0062: `request() constructs FactoryError`
- c0005 ..> c0062: `start_owner() constructs FactoryError`
- c0006 ..> c0000: `close() calls close()`
- c0006 ..> c0006: `send() calls _read()`
- c0006 ..> c0006: `send() calls _write()`
- c0006 ..> c0006: `start() calls _read()`
- c0006 ..> c0006: `start() calls _write()`
- c0006 ..> c0006: `wait() calls _read()`
- c0006 ..> c0062: `_read() constructs FactoryError`
- c0006 ..> c0062: `_write() constructs FactoryError`
- c0006 ..> c0062: `close() constructs FactoryError`
- c0006 ..> c0062: `start() constructs FactoryError`
- c0007 ..> c0003: `run_command() calls run()`
- c0007 ..> c0062: `run_command() constructs FactoryError`
- c0008 ..> c0008: `foreman_launch() calls read_definition()`
- c0008 ..> c0008: `foreman_launch() calls relative_path()`
- c0008 ..> c0008: `read_definition() calls relative_path()`
- c0008 ..> c0034: `foreman_launch() calls nonblank()`
- c0008 ..> c0034: `read_definition() calls nonblank()`
- c0008 ..> c0034: `relative_path() calls nonblank()`
- c0008 ..> c0062: `foreman_launch() constructs FactoryError`
- c0008 ..> c0062: `read_definition() constructs FactoryError`
- c0009 ..> c0009: `prepare() calls _write_agent()`
- c0009 ..> c0009: `prepare() calls validate_guidance()`
- c0009 ..> c0010: `prepare() calls selected_resources()`
- c0009 ..> c0011: `prepare() calls prepare()`
- c0009 ..> c0017: `_write_agent() calls write_definition()`
- c0009 ..> c0017: `prepare() calls check_skill_file()`
- c0009 ..> c0017: `prepare() calls write_new()`
- c0009 ..> c0022: `__init__() constructs WorkerProfiles`
- c0009 ..> c0032: `type in prepare`
- c0009 ..> c0032: `type in validate_guidance`
- c0009 ..> c0062: `prepare() constructs FactoryError`
- c0009 ..> c0062: `validate_depth() constructs FactoryError`
- c0009 ..> c0062: `validate_guidance() constructs FactoryError`
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
- c0011 ..> c0017: `_install_resources() calls write_new()`
- c0011 ..> c0017: `_protect_runtime() calls write_new()`
- c0011 ..> c0017: `begin_setup() calls remove_generated()`
- c0011 ..> c0017: `pi_home() calls read_generated_json()`
- c0011 ..> c0017: `prepare() calls write_new()`
- c0011 ..> c0017: `prepare_roles() calls check_real_path()`
- c0011 ..> c0017: `prepare_setup_guidance() calls write_new()`
- c0011 ..> c0017: `record_completion() calls replace_generated_json()`
- c0011 ..> c0017: `save_pi_choice() calls write_json()`
- c0011 ..> c0017: `validate_bundled_resources() calls check_real_path()`
- c0011 ..> c0017: `validate_completion() calls read_generated_json()`
- c0011 ..> c0018: `selected_launch() calls selected_skill_files()`
- c0011 ..> c0020: `require_pi_home() calls quote()`
- c0011 ..> c0023: `uses_browser_login() calls uses_browser_login()`
- c0011 ..> c0024: `check() calls check()`
- c0011 ..> c0024: `check() constructs AgentForgetfulConnection`
- c0011 ..> c0024: `create_project() calls create_project()`
- c0011 ..> c0024: `create_project() constructs AgentForgetfulConnection`
- c0011 ..> c0024: `login() calls login()`
- c0011 ..> c0024: `login() constructs AgentForgetfulConnection`
- c0011 ..> c0024: `projects() calls projects()`
- c0011 ..> c0024: `projects() constructs AgentForgetfulConnection`
- c0011 ..> c0025: `list_models() calls role_environment()`
- c0011 ..> c0029: `install() calls install()`
- c0011 ..> c0029: `install() constructs HostDependencies`
- c0011 ..> c0029: `installation() calls description()`
- c0011 ..> c0029: `installation() constructs HostDependencies`
- c0011 ..> c0029: `missing_executables() calls pi_ready()`
- c0011 ..> c0029: `missing_executables() constructs HostDependencies`
- c0011 ..> c0030: `missing_executables() calls executable_path()`
- c0011 ..> c0030: `missing_executables() calls runtime_ready()`
- c0011 ..> c0030: `require_pi_home() calls executable_path()`
- c0011 ..> c0031: `list_models() calls run_owned()`
- c0011 ..> c0032: `type in record_completion`
- c0011 ..> c0032: `type in selected_launch`
- c0011 ..> c0032: `type in validate_completion`
- c0011 ..> c0032: `type in validate_worker_models`
- c0011 ..> c0033: `type in check`
- c0011 ..> c0033: `type in create_project`
- c0011 ..> c0033: `type in list_models`
- c0011 ..> c0033: `type in login`
- c0011 ..> c0033: `type in missing_executables`
- c0011 ..> c0033: `type in prepare`
- c0011 ..> c0033: `type in projects`
- c0011 ..> c0033: `type in uses_browser_login`
- c0011 ..> c0033: `type in validate_setup`
- c0011 ..> c0062: `_install_resources() constructs FactoryError`
- c0011 ..> c0062: `_read_guidance() constructs FactoryError`
- c0011 ..> c0062: `choose_pi_home() constructs FactoryError`
- c0011 ..> c0062: `list_models() constructs FactoryError`
- c0011 ..> c0062: `pi_home() constructs FactoryError`
- c0011 ..> c0062: `prepare_roles() constructs FactoryError`
- c0011 ..> c0062: `prepare_setup_guidance() constructs FactoryError`
- c0011 ..> c0062: `require_pi_home() constructs FactoryError`
- c0011 ..> c0062: `selected_launch() constructs FactoryError`
- c0011 ..> c0062: `validate_bundled_resources() constructs FactoryError`
- c0011 ..> c0062: `validate_completion() constructs FactoryError`
- c0011 ..> c0062: `validate_guidance() constructs FactoryError`
- c0011 ..> c0062: `validate_setup() constructs FactoryError`
- c0011 ..> c0062: `validate_worker_models() constructs FactoryError`
- c0012 ..> c0017: `runtime_directory() calls check_real_path()`
- c0012 ..> c0062: `runtime_directory() constructs FactoryError`
- c0013 ..> c0007: `origin() calls run_command()`
- c0013 ..> c0014: `origin() calls _resolve_repository()`
- c0013 ..> c0062: `origin() constructs FactoryError`
- c0014 ..> c0062: `_resolve_repository() constructs FactoryError`
- c0015 ..> c0007: `ensure() calls run_command()`
- c0015 ..> c0015: `_inspect() calls _repository_entries()`
- c0015 ..> c0015: `_verify_removed() calls _repository_entries()`
- c0015 ..> c0015: `ensure() calls _inspect()`
- c0015 ..> c0015: `inspect() calls _inspect()`
- c0015 ..> c0015: `verify_removed() calls _verify_removed()`
- c0015 ..> c0016: `_inspect() calls _read_git()`
- c0015 ..> c0016: `_repository_entries() calls _read_git()`
- c0015 ..> c0016: `_repository_entries() calls _worktree_entries()`
- c0015 ..> c0046: `_inspect() constructs WorktreeProblem`
- c0015 ..> c0046: `_repository_entries() constructs WorktreeProblem`
- c0015 ..> c0046: `_verify_removed() constructs WorktreeProblem`
- c0015 ..> c0047: `ensure() constructs WorktreeReadError`
- c0015 ..> c0047: `inspect() constructs WorktreeReadError`
- c0015 ..> c0047: `verify_removed() constructs WorktreeReadError`
- c0015 ..> c0062: `ensure() constructs FactoryError`
- c0016 ..> c0007: `_read_git() calls run_command()`
- c0016 ..> c0047: `_read_git() constructs WorktreeReadError`
- c0017 ..> c0000: `_generated_parent() calls close()`
- c0017 ..> c0017: `_generated_parent() calls check_real_path()`
- c0017 ..> c0017: `check_skill_file() calls check_real_path()`
- c0017 ..> c0017: `read_generated_json() calls _generated_parent()`
- c0017 ..> c0017: `remove_generated() calls _generated_parent()`
- c0017 ..> c0017: `replace_generated_json() calls _generated_parent()`
- c0017 ..> c0017: `write_definition() calls read_generated_json()`
- c0017 ..> c0017: `write_definition() calls write_json()`
- c0017 ..> c0017: `write_json() calls write_new()`
- c0017 ..> c0017: `write_new() calls check_real_path()`
- c0017 ..> c0019: `read_generated_json() calls load()`
- c0017 ..> c0062: `_generated_parent() constructs FactoryError`
- c0017 ..> c0062: `check_real_path() constructs FactoryError`
- c0017 ..> c0062: `check_skill_file() constructs FactoryError`
- c0017 ..> c0062: `read_generated_json() constructs FactoryError`
- c0017 ..> c0062: `write_definition() constructs FactoryError`
- c0017 ..> c0062: `write_new() constructs FactoryError`
- c0018 ..> c0062: `selected_skill_files() constructs FactoryError`
- c0019 ..> c0000: `load() calls close()`
- c0019 ..> c0000: `save() calls close()`
- c0019 ..> c0020: `save() calls quote()`
- c0019 ..> c0032: `type in load`
- c0019 ..> c0032: `type in save`
- c0019 ..> c0034: `load() calls from_mapping()`
- c0019 ..> c0038: `load() calls load()`
- c0019 ..> c0062: `load() constructs FactoryError`
- c0019 ..> c0062: `save() constructs FactoryError`
- c0021 ..> c0000: `_hold_directory() calls close()`
- c0021 ..> c0021: `hold() calls _hold_directory()`
- c0021 ..> c0062: `_hold_directory() constructs FactoryError`
- c0022 ..> c0017: `prepare() calls check_skill_file()`
- c0022 ..> c0017: `prepare() calls write_definition()`
- c0022 ..> c0017: `prepare() calls write_new()`
- c0022 ..> c0035: `type in prepare`
- c0023 ..> c0005: `uses_browser_login() calls request()`
- c0023 ..> c0033: `type in uses_browser_login`
- c0024 ..> c0024: `call() calls command()`
- c0024 ..> c0024: `check() calls call()`
- c0024 ..> c0024: `check() calls command()`
- c0024 ..> c0024: `command() calls _environment()`
- c0024 ..> c0024: `create_project() calls call()`
- c0024 ..> c0024: `login() calls _environment()`
- c0024 ..> c0024: `projects() calls command()`
- c0024 ..> c0025: `_environment() calls role_environment()`
- c0024 ..> c0025: `check() calls _catalog_tools()`
- c0024 ..> c0031: `command() calls run_owned()`
- c0024 ..> c0031: `login() calls run_owned()`
- c0024 ..> c0033: `type in _environment`
- c0024 ..> c0033: `type in call`
- c0024 ..> c0033: `type in check`
- c0024 ..> c0033: `type in command`
- c0024 ..> c0033: `type in create_project`
- c0024 ..> c0033: `type in login`
- c0024 ..> c0033: `type in projects`
- c0024 ..> c0062: `check() constructs FactoryError`
- c0024 ..> c0062: `command() constructs FactoryError`
- c0024 ..> c0062: `create_project() constructs FactoryError`
- c0024 ..> c0062: `login() constructs FactoryError`
- c0024 ..> c0062: `projects() constructs FactoryError`
- c0025 ..> c0030: `role_environment() calls executable_path()`
- c0025 ..> c0033: `type in role_environment`
- c0026 ..> c0011: `check() calls check()`
- c0026 ..> c0024: `__init__() constructs AgentForgetfulConnection`
- c0026 ..> c0024: `_call() calls call()`
- c0026 ..> c0026: `_read() calls _call()`
- c0026 ..> c0026: `_task() calls _read()`
- c0026 ..> c0026: `create_plan() calls _call()`
- c0026 ..> c0026: `create_task() calls _call()`
- c0026 ..> c0026: `get_plan() calls _read()`
- c0026 ..> c0026: `plans() calls _read()`
- c0026 ..> c0026: `plans() calls _rows()`
- c0026 ..> c0026: `tasks() calls _read()`
- c0026 ..> c0026: `tasks() calls _rows()`
- c0026 ..> c0026: `tasks() calls _task()`
- c0026 ..> c0026: `update_plan() calls _call()`
- c0026 ..> c0026: `update_task() calls _call()`
- c0026 ..> c0027: `_rows() calls _positive_id()`
- c0026 ..> c0027: `_task() calls _positive_id()`
- c0026 ..> c0027: `get_plan() calls _positive_id()`
- c0026 ..> c0033: `type in __init__`
- c0026 ..> c0043: `_read() constructs PlanningReadError`
- c0026 ..> c0043: `_rows() constructs PlanningReadError`
- c0026 ..> c0043: `_task() constructs PlanningReadError`
- c0026 ..> c0043: `get_plan() constructs PlanningReadError`
- c0028 ..> c0007: `_api() calls run_command()`
- c0028 ..> c0028: `check_access() calls _api()`
- c0028 ..> c0028: `create_label() calls _api()`
- c0028 ..> c0028: `list_issues() calls _api()`
- c0028 ..> c0028: `list_issues() calls _validate_issue()`
- c0028 ..> c0028: `list_labels() calls _api()`
- c0028 ..> c0062: `_api() constructs FactoryError`
- c0028 ..> c0062: `_validate_issue() constructs FactoryError`
- c0028 ..> c0062: `check_access() constructs FactoryError`
- c0028 ..> c0062: `create_label() constructs FactoryError`
- c0028 ..> c0062: `list_issues() constructs FactoryError`
- c0028 ..> c0062: `list_labels() constructs FactoryError`
- c0028 ..> c0062: `source_from_remote() constructs FactoryError`
- c0028 ..> c0063: `list_issues() constructs Issue`
- c0028 ..> c0063: `type in list_issues`
- c0028 ..> c0064: `list_labels() constructs Label`
- c0028 ..> c0064: `type in create_label`
- c0028 ..> c0064: `type in list_labels`
- c0028 ..> c0066: `source_from_remote() constructs WorkSource`
- c0028 ..> c0066: `type in _api`
- c0028 ..> c0066: `type in _validate_issue`
- c0028 ..> c0066: `type in check_access`
- c0028 ..> c0066: `type in create_label`
- c0028 ..> c0066: `type in list_issues`
- c0028 ..> c0066: `type in list_labels`
- c0028 ..> c0066: `type in source_from_remote`
- c0029 ..> c0017: `install() calls write_new()`
- c0029 ..> c0029: `_check_uv() calls _environment()`
- c0029 ..> c0029: `_forgetful_python() calls _check_uv()`
- c0029 ..> c0029: `_forgetful_python() calls _environment()`
- c0029 ..> c0029: `_install_role_runtime() calls _check_uv()`
- c0029 ..> c0029: `_install_role_runtime() calls _run()`
- c0029 ..> c0029: `_install_tmux() calls _run()`
- c0029 ..> c0029: `_run() calls _environment()`
- c0029 ..> c0029: `description() calls _forgetful_python()`
- c0029 ..> c0029: `description() calls _ubuntu_tmux()`
- c0029 ..> c0029: `install() calls _forgetful_python()`
- c0029 ..> c0029: `install() calls _install_role_runtime()`
- c0029 ..> c0029: `install() calls _install_tmux()`
- c0029 ..> c0029: `install() calls _run()`
- c0029 ..> c0029: `install() calls _ubuntu_tmux()`
- c0029 ..> c0029: `pi_ready() calls _environment()`
- c0029 ..> c0030: `_install_role_runtime() calls sync_fingerprint()`
- c0029 ..> c0030: `install() calls sync_fingerprint()`
- c0029 ..> c0030: `pi_ready() calls sync_fingerprint()`
- c0029 ..> c0031: `_check_uv() calls run_owned()`
- c0029 ..> c0031: `_forgetful_python() calls run_owned()`
- c0029 ..> c0031: `_run() calls run_owned()`
- c0029 ..> c0031: `pi_ready() calls run_owned()`
- c0029 ..> c0062: `_check_uv() constructs FactoryError`
- c0029 ..> c0062: `_forgetful_python() constructs FactoryError`
- c0029 ..> c0062: `_install_role_runtime() constructs FactoryError`
- c0029 ..> c0062: `_install_tmux() constructs FactoryError`
- c0029 ..> c0062: `_run() constructs FactoryError`
- c0029 ..> c0062: `install() constructs FactoryError`
- c0030 ..> c0030: `runtime_ready() calls sync_fingerprint()`
- c0030 ..> c0031: `runtime_ready() calls run_owned()`
- c0031 ..> c0000: `run_owned() calls close()`
- c0031 ..> c0000: `run_owned() calls wait()`
- c0031 ..> c0062: `run_owned() constructs FactoryError`
- c0032 --> c0033: `field forgetful`
- c0032 --> c0065: `field repository`
- c0033 ..> c0034: `_validate_server() calls loopback_host()`
- c0033 ..> c0034: `_validate_server() calls nonblank()`
- c0033 ..> c0062: `_validate_server() constructs FactoryError`
- c0034 ..> c0032: `from_mapping() constructs FactoryConfiguration`
- c0034 ..> c0032: `type in from_mapping`
- c0034 ..> c0032: `type in validate`
- c0034 ..> c0033: `connection_from_mapping() constructs ForgetfulConnection`
- c0034 ..> c0033: `type in connection_from_mapping`
- c0034 ..> c0033: `validate() calls _validate_server()`
- c0034 ..> c0034: `connection_from_mapping() calls validate()`
- c0034 ..> c0034: `from_mapping() calls connection_from_mapping()`
- c0034 ..> c0034: `from_mapping() calls validate()`
- c0034 ..> c0034: `unique_labels() calls nonblank()`
- c0034 ..> c0034: `validate() calls nonblank()`
- c0034 ..> c0062: `connection_from_mapping() constructs FactoryError`
- c0034 ..> c0062: `from_mapping() constructs FactoryError`
- c0034 ..> c0062: `nonblank() constructs FactoryError`
- c0034 ..> c0062: `validate() constructs FactoryError`
- c0034 ..> c0065: `from_mapping() constructs RepositoryReference`
- c0034 ..> c0066: `from_mapping() constructs WorkSource`
- c0036 ..> c0034: `skill_paths() calls nonblank()`
- c0036 ..> c0034: `validate_initial_agents() calls nonblank()`
- c0036 ..> c0034: `validate_workers() calls nonblank()`
- c0036 ..> c0035: `type in validate_initial_agents`
- c0036 ..> c0035: `type in validate_workers`
- c0036 ..> c0036: `validate_initial_agents() calls validate_role_app()`
- c0036 ..> c0036: `validate_initial_agents() calls validate_workers()`
- c0036 ..> c0036: `validate_workers() calls validate_role_app()`
- c0036 ..> c0062: `skill_paths() constructs FactoryError`
- c0036 ..> c0062: `validate_initial_agents() constructs FactoryError`
- c0036 ..> c0062: `validate_role_app() constructs FactoryError`
- c0036 ..> c0062: `validate_workers() constructs FactoryError`
- c0037 ..> c0003: `initialise() calls save()`
- c0037 ..> c0009: `prepare_foreman() calls prepare()`
- c0037 ..> c0011: `check_foreman() calls check()`
- c0037 ..> c0011: `check_foreman() calls login()`
- c0037 ..> c0011: `prepare_foreman() calls install()`
- c0037 ..> c0011: `prepare_foreman() calls installation()`
- c0037 ..> c0011: `prepare_foreman() calls missing_executables()`
- c0037 ..> c0013: `_preflight() calls origin()`
- c0037 ..> c0013: `discover() calls discover()`
- c0037 ..> c0013: `inspect() calls origin()`
- c0037 ..> c0019: `load_existing() calls load()`
- c0037 ..> c0028: `_ensure_label() calls create_label()`
- c0037 ..> c0028: `_preflight() calls check_access()`
- c0037 ..> c0028: `_preflight() calls list_labels()`
- c0037 ..> c0028: `_preflight() calls source_from_remote()`
- c0037 ..> c0028: `inspect() calls source_from_remote()`
- c0037 ..> c0032: `configure() constructs FactoryConfiguration`
- c0037 ..> c0032: `type in _preflight`
- c0037 ..> c0032: `type in check_foreman`
- c0037 ..> c0032: `type in configure`
- c0037 ..> c0032: `type in initialise`
- c0037 ..> c0032: `type in load_existing`
- c0037 ..> c0033: `_preflight() calls validate()`
- c0037 ..> c0033: `type in prepare_foreman`
- c0037 ..> c0034: `configure() calls unique_labels()`
- c0037 ..> c0034: `load_existing() calls unique_labels()`
- c0037 ..> c0037: `configure() calls inspect()`
- c0037 ..> c0037: `initialise() calls _ensure_label()`
- c0037 ..> c0037: `initialise() calls _preflight()`
- c0037 ..> c0038: `type in __init__`
- c0037 ..> c0039: `type in __init__`
- c0037 ..> c0041: `type in __init__`
- c0037 ..> c0045: `type in __init__`
- c0037 ..> c0062: `_preflight() constructs FactoryError`
- c0037 ..> c0062: `initialise() constructs FactoryError`
- c0037 ..> c0062: `inspect() constructs FactoryError`
- c0037 ..> c0062: `load_existing() constructs FactoryError`
- c0037 ..> c0062: `prepare_foreman() constructs FactoryError`
- c0037 ..> c0064: `_ensure_label() constructs Label`
- c0037 ..> c0064: `type in _preflight`
- c0037 ..> c0065: `inspect() constructs RepositoryReference`
- c0037 ..> c0065: `type in inspect`
- c0037 ..> c0066: `type in _ensure_label`
- c0037 ..> c0066: `type in _preflight`
- c0037 ..> c0067: `type in __init__`
- c0038 ..> c0032: `type in load`
- c0038 ..> c0032: `type in save`
- c0039 ..> c0032: `type in prepare_roles`
- c0039 ..> c0032: `type in record_completion`
- c0039 ..> c0032: `type in selected_launch`
- c0039 ..> c0033: `type in check`
- c0039 ..> c0033: `type in create_project`
- c0039 ..> c0033: `type in list_models`
- c0039 ..> c0033: `type in login`
- c0039 ..> c0033: `type in missing_executables`
- c0039 ..> c0033: `type in prepare`
- c0039 ..> c0033: `type in projects`
- c0039 ..> c0033: `type in uses_browser_login`
- c0039 ..> c0035: `type in prepare_roles`
- c0043 --|> c0062: `inherits`
- c0045 ..> c0066: `type in source_from_remote`
- c0046 ..> c0000: `__init__() calls __init__()`
- c0046 --|> c0062: `inherits`
- c0047 --|> c0062: `inherits`
- c0049 ..> c0011: `check() calls check()`
- c0049 ..> c0013: `check_repository() calls origin()`
- c0049 ..> c0015: `_ensure_mapping() calls ensure()`
- c0049 ..> c0015: `_ensure_mapping() calls verify_removed()`
- c0049 ..> c0015: `preflight() calls inspect()`
- c0049 ..> c0026: `_create_plan() calls create_plan()`
- c0049 ..> c0026: `_create_plan() calls get_plan()`
- c0049 ..> c0026: `_create_plan() calls plans()`
- c0049 ..> c0026: `_ownership() calls tasks()`
- c0049 ..> c0026: `_prepare_plan() calls create_task()`
- c0049 ..> c0026: `_prepare_plan() calls update_plan()`
- c0049 ..> c0026: `lookup() calls plans()`
- c0049 ..> c0026: `recover() calls get_plan()`
- c0049 ..> c0026: `recover() calls plans()`
- c0049 ..> c0026: `unfinished() calls plans()`
- c0049 ..> c0028: `_check_source() calls source_from_remote()`
- c0049 ..> c0032: `type in __init__`
- c0049 ..> c0041: `type in __init__`
- c0049 ..> c0042: `type in __init__`
- c0049 ..> c0045: `type in __init__`
- c0049 ..> c0048: `type in __init__`
- c0049 ..> c0049: `_ensure_mapping() calls _check_source()`
- c0049 ..> c0049: `_ensure_worktrees() calls _ensure_mapping()`
- c0049 ..> c0049: `_initial_mappings() calls _repository()`
- c0049 ..> c0049: `_prepare_plan() calls _active()`
- c0049 ..> c0049: `_prepare_plan() calls _context()`
- c0049 ..> c0049: `_prepare_plan() calls _ensure_worktrees()`
- c0049 ..> c0049: `_prepare_plan() calls _initial_mappings()`
- c0049 ..> c0049: `_prepare_plan() calls _ownership()`
- c0049 ..> c0049: `check_repository() calls _check_source()`
- c0049 ..> c0049: `preflight() calls _initial_mappings()`
- c0049 ..> c0049: `preflight() calls _repository()`
- c0049 ..> c0049: `preflight() calls check_repository()`
- c0049 ..> c0049: `prepare() calls _create_plan()`
- c0049 ..> c0049: `prepare() calls _prepare_plan()`
- c0049 ..> c0049: `prepare() calls lookup()`
- c0049 ..> c0049: `prepare() calls preflight()`
- c0049 ..> c0049: `prepare() calls recover()`
- c0049 ..> c0049: `recover() calls _active()`
- c0049 ..> c0049: `recover() calls _context()`
- c0049 ..> c0049: `recover() calls _ensure_worktrees()`
- c0049 ..> c0049: `recover() calls _ownership()`
- c0049 ..> c0049: `recover() calls _repository()`
- c0049 ..> c0049: `recover() calls _snapshot()`
- c0049 ..> c0049: `recover() calls check_repository()`
- c0049 ..> c0049: `unfinished() calls _is_unfinished_factory_plan()`
- c0049 ..> c0050: `_ensure_mapping() calls _cleanup_state()`
- c0049 ..> c0053: `preflight() constructs IntakeProblem`
- c0049 ..> c0054: `_check_source() constructs RepositoryProblem`
- c0049 ..> c0054: `check_repository() constructs RepositoryProblem`
- c0049 ..> c0055: `_active() constructs ScaffoldProblem`
- c0049 ..> c0055: `_context() constructs ScaffoldProblem`
- c0049 ..> c0055: `_create_plan() constructs ScaffoldProblem`
- c0049 ..> c0055: `_ensure_mapping() constructs ScaffoldProblem`
- c0049 ..> c0055: `_ensure_worktrees() constructs ScaffoldProblem`
- c0049 ..> c0055: `_ownership() constructs ScaffoldProblem`
- c0049 ..> c0055: `_prepare_plan() constructs ScaffoldProblem`
- c0049 ..> c0055: `_snapshot() constructs ScaffoldProblem`
- c0049 ..> c0055: `lookup() constructs ScaffoldProblem`
- c0049 ..> c0055: `recover() constructs ScaffoldProblem`
- c0049 ..> c0056: `_create_plan() constructs ScaffoldReadProblem`
- c0049 ..> c0056: `_prepare_plan() constructs ScaffoldReadProblem`
- c0049 ..> c0056: `lookup() constructs ScaffoldReadProblem`
- c0049 ..> c0056: `prepare() constructs ScaffoldReadProblem`
- c0049 ..> c0056: `recover() constructs ScaffoldReadProblem`
- c0049 ..> c0057: `_create_plan() constructs UncertainScaffold`
- c0049 ..> c0057: `_prepare_plan() constructs UncertainScaffold`
- c0049 ..> c0057: `prepare() constructs UncertainScaffold`
- c0049 ..> c0057: `recover() constructs UncertainScaffold`
- c0049 ..> c0062: `_is_unfinished_factory_plan() constructs FactoryError`
- c0049 ..> c0063: `_snapshot() constructs Issue`
- c0049 ..> c0063: `type in _create_plan`
- c0049 ..> c0063: `type in _initial_mappings`
- c0049 ..> c0063: `type in _prepare_plan`
- c0049 ..> c0063: `type in _snapshot`
- c0049 ..> c0063: `type in lookup`
- c0049 ..> c0063: `type in preflight`
- c0049 ..> c0063: `type in prepare`
- c0049 ..> c0063: `type in recover`
- c0049 ..> c0065: `type in _check_source`
- c0049 ..> c0065: `type in _repository`
- c0049 ..> c0065: `type in check_repository`
- c0049 ..> c0066: `_check_source() constructs WorkSource`
- c0049 ..> c0066: `_snapshot() constructs WorkSource`
- c0049 ..> c0066: `type in _repository`
- c0050 ..> c0055: `_cleanup_state() constructs ScaffoldProblem`
- c0051 --> c0063: `field issue`
- c0052 ..> c0000: `_alert_plan() calls send()`
- c0052 ..> c0000: `_read_issues() calls send()`
- c0052 ..> c0000: `_submit() calls send()`
- c0052 ..> c0000: `_watch() calls close()`
- c0052 ..> c0000: `_watch() calls send()`
- c0052 ..> c0000: `_watch() calls start()`
- c0052 ..> c0000: `_watch() calls wait()`
- c0052 ..> c0000: `run() calls startup_hint()`
- c0052 ..> c0009: `_watch() calls prepare()`
- c0052 ..> c0011: `_watch() calls check()`
- c0052 ..> c0028: `_read_issues() calls list_issues()`
- c0052 ..> c0032: `type in _watch`
- c0052 ..> c0032: `type in run`
- c0052 ..> c0040: `type in __init__`
- c0052 ..> c0049: `_watch() calls check_repository()`
- c0052 ..> c0049: `_watch() calls lookup()`
- c0052 ..> c0049: `_watch() calls recover()`
- c0052 ..> c0049: `_watch() calls unfinished()`
- c0052 ..> c0049: `type in __init__`
- c0052 ..> c0051: `_watch() constructs BlockedWork`
- c0052 ..> c0051: `type in _alert_plan`
- c0052 ..> c0052: `_watch() calls _alert_plan()`
- c0052 ..> c0052: `_watch() calls _read_issues()`
- c0052 ..> c0052: `_watch() calls _submit()`
- c0052 ..> c0052: `run() calls _watch()`
- c0052 ..> c0055: `_watch() constructs ScaffoldProblem`
- c0052 ..> c0055: `type in _alert_plan`
- c0052 ..> c0058: `_read_issues() calls clear()`
- c0052 ..> c0058: `_watch() calls clear()`
- c0052 ..> c0058: `_watch() constructs WatcherAlerts`
- c0052 ..> c0058: `type in _alert_plan`
- c0052 ..> c0058: `type in _read_issues`
- c0052 ..> c0062: `_read_issues() constructs FactoryError`
- c0052 ..> c0063: `type in _read_issues`
- c0052 ..> c0063: `type in _submit`
- c0052 ..> c0066: `_watch() constructs WorkSource`
- c0052 ..> c0066: `type in _read_issues`
- c0052 ..> c0067: `type in __init__`
- c0053 --|> c0055: `inherits`
- c0054 --|> c0055: `inherits`
- c0055 --|> c0062: `inherits`
- c0056 --|> c0055: `inherits`
- c0057 --|> c0055: `inherits`
- c0058 ..> c0000: `__init__() calls __init__()`
- c0058 ..> c0000: `send() calls send()`
- c0058 ..> c0062: `type in send`
- c0059 ..> c0006: `build_watcher() constructs AgentShellTerminal`
- c0059 ..> c0011: `build_initialiser() constructs ForemanProfile`
- c0059 ..> c0011: `prepare_foreman_launch() calls pi_home()`
- c0059 ..> c0011: `prepare_foreman_launch() calls selected_launch()`
- c0059 ..> c0011: `prepare_foreman_launch() calls validate_completion()`
- c0059 ..> c0011: `prepare_foreman_launch() constructs ForemanProfile`
- c0059 ..> c0013: `build_initialiser() constructs GitRepositories`
- c0059 ..> c0013: `build_watcher() constructs GitRepositories`
- c0059 ..> c0015: `build_watcher() constructs GitWorktrees`
- c0059 ..> c0019: `build_initialiser() constructs TomlConfigurationStore`
- c0059 ..> c0025: `prepare_foreman_launch() calls role_environment()`
- c0059 ..> c0026: `build_watcher() constructs ForgetfulPlanning`
- c0059 ..> c0028: `build_initialiser() constructs GitHubWorkTracking`
- c0059 ..> c0028: `build_watcher() calls source_from_remote()`
- c0059 ..> c0028: `build_watcher() constructs GitHubWorkTracking`
- c0059 ..> c0032: `type in build_watcher`
- c0059 ..> c0032: `type in prepare_foreman_launch`
- c0059 ..> c0037: `build_initialiser() constructs InitialiseFactory`
- c0059 ..> c0037: `type in build_initialiser`
- c0059 ..> c0049: `build_watcher() constructs ScaffoldIssue`
- c0059 ..> c0052: `build_watcher() constructs WatchFactory`
- c0059 ..> c0052: `type in build_watcher`
- c0059 ..> c0059: `build_watcher() calls prepare_foreman_launch()`
- c0059 ..> c0062: `build_watcher() constructs FactoryError`
- c0059 ..> c0062: `prepare_foreman_launch() constructs FactoryError`
- c0060 ..> c0000: `_watch_locked() constructs BorrowedForemanTerminal`
- c0060 ..> c0003: `_watch_locked() calls run()`
- c0060 ..> c0005: `_foreman() calls enter_terminal()`
- c0060 ..> c0005: `_foreman() calls read_state()`
- c0060 ..> c0005: `_foreman() calls request()`
- c0060 ..> c0005: `_foreman() calls start_owner()`
- c0060 ..> c0005: `_initialise() calls enter_terminal()`
- c0060 ..> c0005: `_initialise() calls request()`
- c0060 ..> c0005: `_initialise_locked() calls read_state()`
- c0060 ..> c0005: `_launch_setup_foreman() calls start_owner()`
- c0060 ..> c0005: `_offer_factory_launch() calls read_state()`
- c0060 ..> c0005: `_watch() calls read_state()`
- c0060 ..> c0005: `_watch() calls request()`
- c0060 ..> c0005: `_watch_locked() calls read_state()`
- c0060 ..> c0011: `_complete_setup() calls record_completion()`
- c0060 ..> c0011: `_complete_setup() calls uses_browser_login()`
- c0060 ..> c0011: `_initialise_locked() calls begin_setup()`
- c0060 ..> c0011: `_initialise_locked() calls choose_pi_home()`
- c0060 ..> c0011: `_initialise_locked() calls save_pi_choice()`
- c0060 ..> c0011: `_initialise_locked() calls selected_launch()`
- c0060 ..> c0011: `_launch_setup_foreman() calls prepare_setup_guidance()`
- c0060 ..> c0011: `_select_model() calls list_models()`
- c0060 ..> c0011: `_select_project() calls create_project()`
- c0060 ..> c0011: `_select_project() calls projects()`
- c0060 ..> c0011: `_watch() calls validate_completion()`
- c0060 ..> c0011: `_watch() constructs ForemanProfile`
- c0060 ..> c0013: `select_repositories() calls discover()`
- c0060 ..> c0015: `_configure_new_factory() calls inspect()`
- c0060 ..> c0019: `_initialise_locked() calls load()`
- c0060 ..> c0020: `_initialise() calls quote()`
- c0060 ..> c0020: `_initialise_locked() calls quote()`
- c0060 ..> c0020: `_launch_setup_foreman() calls quote()`
- c0060 ..> c0020: `_select_model() calls quote()`
- c0060 ..> c0020: `_watch() calls quote()`
- c0060 ..> c0020: `_watch_locked() calls quote()`
- c0060 ..> c0021: `_foreman() calls hold()`
- c0060 ..> c0021: `_foreman() constructs WorkspaceWatchLease`
- c0060 ..> c0021: `_initialise() calls hold()`
- c0060 ..> c0021: `_initialise() constructs WorkspaceWatchLease`
- c0060 ..> c0021: `_watch() calls hold()`
- c0060 ..> c0021: `_watch() constructs WorkspaceWatchLease`
- c0060 ..> c0032: `type in _complete_setup`
- c0060 ..> c0032: `type in _configure_new_factory`
- c0060 ..> c0033: `_connection() calls validate()`
- c0060 ..> c0033: `_connection() constructs ForgetfulConnection`
- c0060 ..> c0033: `type in _check_existing_connection`
- c0060 ..> c0033: `type in _configure_new_factory`
- c0060 ..> c0033: `type in _connection`
- c0060 ..> c0033: `type in _select_project`
- c0060 ..> c0035: `_configure_new_factory() constructs InitialAgentChoices`
- c0060 ..> c0035: `type in _configure_new_factory`
- c0060 ..> c0035: `type in _owner_choices`
- c0060 ..> c0035: `type in _worker_choices`
- c0060 ..> c0036: `_initialise_locked() calls validate_initial_agents()`
- c0060 ..> c0037: `_complete_setup() calls check_foreman()`
- c0060 ..> c0037: `_configure_new_factory() calls configure()`
- c0060 ..> c0037: `_initialise_locked() calls initialise()`
- c0060 ..> c0037: `_initialise_locked() calls load_existing()`
- c0060 ..> c0037: `_launch_setup_foreman() calls check_foreman()`
- c0060 ..> c0037: `_prepare_foreman() calls prepare_foreman()`
- c0060 ..> c0037: `type in _complete_setup`
- c0060 ..> c0037: `type in _configure_new_factory`
- c0060 ..> c0037: `type in _select_project`
- c0060 ..> c0037: `type in select_repositories`
- c0060 ..> c0059: `_foreman() calls prepare_foreman_launch()`
- c0060 ..> c0059: `_initialise_locked() calls build_initialiser()`
- c0060 ..> c0059: `_launch_setup_foreman() calls prepare_foreman_launch()`
- c0060 ..> c0059: `_watch_locked() calls build_watcher()`
- c0060 ..> c0060: `_configure_new_factory() calls _prepare_foreman()`
- c0060 ..> c0060: `_configure_new_factory() calls _select_model()`
- c0060 ..> c0060: `_configure_new_factory() calls _select_numbered()`
- c0060 ..> c0060: `_configure_new_factory() calls select_repositories()`
- c0060 ..> c0060: `_connection() calls _check_existing_connection()`
- c0060 ..> c0060: `_initialise() calls _initialise_locked()`
- c0060 ..> c0060: `_initialise() calls _offer_factory_launch()`
- c0060 ..> c0060: `_initialise_locked() calls _complete_setup()`
- c0060 ..> c0060: `_initialise_locked() calls _configure_new_factory()`
- c0060 ..> c0060: `_initialise_locked() calls _confirm_pi_home()`
- c0060 ..> c0060: `_initialise_locked() calls _connection()`
- c0060 ..> c0060: `_initialise_locked() calls _launch_setup_foreman()`
- c0060 ..> c0060: `_initialise_locked() calls _owner_choices()`
- c0060 ..> c0060: `_initialise_locked() calls _research_choices()`
- c0060 ..> c0060: `_initialise_locked() calls _worker_choices()`
- c0060 ..> c0060: `_print_models() calls _safe_diagnostic()`
- c0060 ..> c0060: `_prompt_worker() calls _select_numbered()`
- c0060 ..> c0060: `_prompt_workers() calls _prompt_worker()`
- c0060 ..> c0060: `_select_model() calls _print_models()`
- c0060 ..> c0060: `_select_model() calls _select_numbered()`
- c0060 ..> c0060: `_select_numbered() calls _safe_diagnostic()`
- c0060 ..> c0060: `_select_project() calls _listed_project_id()`
- c0060 ..> c0060: `_select_project() calls _safe_diagnostic()`
- c0060 ..> c0060: `_watch() calls _watch_locked()`
- c0060 ..> c0060: `_watch_locked() calls _choose_existing()`
- c0060 ..> c0060: `_watch_locked() calls _safe_diagnostic()`
- c0060 ..> c0060: `_worker_choices() calls _prompt_workers()`
- c0060 ..> c0060: `_worker_choices() calls _select_numbered()`
- c0060 ..> c0060: `_worker_choices() calls _worker_arguments()`
- c0060 ..> c0060: `main() calls _foreman()`
- c0060 ..> c0060: `main() calls _initialise()`
- c0060 ..> c0060: `main() calls _parse_arguments()`
- c0060 ..> c0060: `main() calls _safe_diagnostic()`
- c0060 ..> c0060: `main() calls _watch()`
- c0060 ..> c0061: `_foreman() calls load_configuration()`
- c0060 ..> c0061: `_watch() calls load_configuration()`
- c0060 ..> c0061: `_watch_locked() calls load_configuration()`
- c0060 ..> c0062: `_check_existing_connection() constructs FactoryError`
- c0060 ..> c0062: `_choose_existing() constructs FactoryError`
- c0060 ..> c0062: `_configure_new_factory() constructs FactoryError`
- c0060 ..> c0062: `_foreman() constructs FactoryError`
- c0060 ..> c0062: `_initialise() constructs FactoryError`
- c0060 ..> c0062: `_initialise_locked() constructs FactoryError`
- c0060 ..> c0062: `_install_missing() constructs FactoryError`
- c0060 ..> c0062: `_listed_project_id() constructs FactoryError`
- c0060 ..> c0062: `_prompt_worker() constructs FactoryError`
- c0060 ..> c0062: `_select_model() constructs FactoryError`
- c0060 ..> c0062: `_select_numbered() constructs FactoryError`
- c0060 ..> c0062: `_select_project() constructs FactoryError`
- c0060 ..> c0062: `_watch() constructs FactoryError`
- c0060 ..> c0062: `_watch_locked() constructs FactoryError`
- c0060 ..> c0062: `_worker_choices() constructs FactoryError`
- c0060 ..> c0062: `main() constructs FactoryError`
- c0060 ..> c0062: `select_repositories() constructs FactoryError`
- c0061 ..> c0019: `load_configuration() calls load()`
- c0061 ..> c0019: `load_configuration() constructs TomlConfigurationStore`
- c0061 ..> c0032: `type in load_configuration`
- c0061 ..> c0062: `load_configuration() constructs FactoryError`
- c0063 --> c0066: `field source`
- c0065 --> c0066: `field work_source`
- c0067 ..> c0063: `type in list_issues`
- c0067 ..> c0064: `type in create_label`
- c0067 ..> c0064: `type in list_labels`
- c0067 ..> c0066: `type in check_access`
- c0067 ..> c0066: `type in create_label`
- c0067 ..> c0066: `type in list_issues`
- c0067 ..> c0066: `type in list_labels`

## Type key

- Type1: `dict | None`
- Type2: `dict[str, str] | None`
- Type3: `str | None`
- Type4: `subprocess.Popen | None`
- Type5: `dict[tuple[str, Path], list[str]]`
- Type6: `Path | None`
- Type7: `tuple[Path, list[dict]]`
- Type8: `tuple[Path, Path] | None`
- Type9: `FactoryConfiguration | None`
- Type10: `dict[str, str]`
- Type11: `tuple[Label, ...]`
- Type12: `tuple[Issue, ...]`
- Type13: `tuple[str, ...]`
- Type14: `tuple[Path, ...]`
- Type15: `float | None`
- Type16: `tuple[RepositoryReference, ...]`
- Type17: `ForgetfulConnection | None`
- Type18: `int | None`
- Type19: `Callable[[list[str]], None]`
- Type20: `Callable[[str, str], bool]`
- Type21: `list[Path] | None`
- Type22: `list[str] | None`
- Type23: `dict[str, RepositoryReference]`
- Type24: `dict[WorkSource, tuple[Label, ...]]`
- Type25: `Callable[[], FactoryConfiguration | None]`
- Type26: `tuple[Issue, dict] | None`
- Type27: `Issue | None`
- Type28: `tuple[int, ...] | None`
- Type29: `Callable[[], bool]`
- Type30: `Callable[[str], None]`
- Type31: `tuple[Issue, ...] | None`
- Type32: `tuple[FactoryConfiguration, InitialAgentChoices]`
- Type33: `list[str] | tuple[str, ...]`
- Type34: `int | dict | str`
- Type35: `str | Path`

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
  FactoryConfiguration, repositories: LocalRepositories, sources: WorkSourceResolver) unknown`
- Signature8: `-__init__(tracking: WorkTrackingService, terminal: ForemanTerminal, scaffold:
  ScaffoldIssue) unknown`
- Signature9: `+run(config: FactoryConfiguration, workspace: Path, interval: float, choose_existing:
  Callable[[], bool], report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature10: `-_watch(config: FactoryConfiguration, workspace: Path, interval: float, existing:
  bool, report: Callable[[str], None], report_error: Callable[[str], None]) None`
- Signature11: `-_submit(issue: Issue, scaffold: dict | None, seen: dict[str, str], report:
  Callable[[str], None], recovered: bool) None`
- Signature12: `-__init__(code: str, diagnostic: str, plan_id: int | None, plan_ids: tuple[int, ...]
  | None, task_ids: tuple[int, ...] | None, candidate_task_ids: tuple[int, ...] | None, paths:
  tuple[str, ...], cause: str | None) unknown`
- Signature13: `+send(subject: str, error: FactoryError, scope: str, code: str, retry: str,
  identities: unknown) None`
- Signature14: `+build_watcher(python: str, config: FactoryConfiguration, workspace: Path, terminal:
  unknown) WatchFactory`
- Signature15: `+prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, complete:
  unknown) unknown`
- Signature16: `-_configure_new_factory(application: InitialiseFactory, workspace: Path, args:
  argparse.Namespace, paths: list[Path] | None, connection: ForgetfulConnection, home: str)
  tuple[FactoryConfiguration, InitialAgentChoices]`
- Signature17: `-_check_existing_connection(args: argparse.Namespace, existing: ForgetfulConnection,
  executable: str | None) None`
- Signature18: `-_connection(args: argparse.Namespace, workspace: Path, existing:
  ForgetfulConnection | None) ForgetfulConnection`
- Signature19: `-_prepare_foreman(application: unknown, connection: unknown, args: unknown,
  prepared: unknown) unknown`
- Signature20: `-_select_model(application: unknown, connection: unknown, home: str, requested: str
  | None, owner: str | None) str`
- Signature21: `-_select_project(application: InitialiseFactory, connection: ForgetfulConnection,
  workspace: Path) int`
- Signature22: `-_owner_choices(args: argparse.Namespace, choices: InitialAgentChoices)
  InitialAgentChoices`
- Signature23: `-_worker_choices(args: argparse.Namespace, config: InitialAgentChoices,
  discover_models: unknown) InitialAgentChoices`
- Signature24: `-_complete_setup(application: InitialiseFactory, config: FactoryConfiguration,
  workspace: Path, login: bool, initial: bool) None`
- Signature25: `-_launch_setup_foreman(application: unknown, config: unknown, workspace: unknown,
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
