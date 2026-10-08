# Factory 
This repo documents the inner workings of a software factory.

## Inspiration

Inspired by [jovaneyck/software-factory-demo](https://github.com/jovaneyck/software-factory-demo/tree/main/.agents)

## Components 

|Component|Role|
|---------|----|
|Github|Code repository and ci/cd layer|
|Watcher|Script that will be responsible for monitoring configured github repositories, creating plans and passing info to the foreman|
|forgetful|Agentic Memory system that includes planning and tasks|
|Host Environment|This is where the agent will be operating inside, this could be a dev machine, vps or docker container - for mvp just host machine|
|End to End test environment|Isolated test environment that has changes deployed to and can be used to run end to end verification tests|
|Foreman Agent|Pi agent that is the primary interaction point for the user or the watcher script|
|Feature Owner|Sub agent that is used to own the particular feature or issue, can be any harness/model type supported by agent shell|
|Implementation Agent|Sub agent that is launched by the feature owner that is designated with implementing the changes|
|Review Agent|Sub agent that is launched by the feature owner that is designated with reviewing the changes|


```mermaid
---
config:
    theme: dark
---
    sequenceDiagram
    
    actor user as User
    participant gh as Github
    participant script as Watcher
    participant forgetful
    participant host as Host Enivronment
    participant e2e as End to End test environment
    actor foreman as Foreman Agent
    actor fo as Feature Owner
    actor ia as Implementation Agent 
    actor ra as Review Agent

    user ->> script: executes
    script ->> foreman: launches pi session
    activate foreman
    script ->> gh: polls for issues
    activate script
    user ->> gh: adds new issue to gh and tags it
    gh -->> script: new issue
    script ->> forgetful: creates plan scaffold
    script ->> host: creates worktree 
    script ->> foreman: send prompt with worktree and forgetful info

    foreman ->> fo: send prompt with issue information, scaffolded plan info in worktree
    activate fo
    fo ->> fo: invoke grill me on issue
    alt requested more feedback
        fo ->> gh: requests further feedback
        fo ->> foreman: informs foreman that more info has been requested
        foreman ->> user: informs user that further info has been requested
        user ->> gh: updates issue
        script ->> foreman: informs of changes to the issue or user can update foreman direct
        foreman ->> fo: updates with user input 
    end
    fo ->> forgetful: generate proper plan 
    fo ->> ia: prompt one or more implementation agents 
    fo ->> forgetful: record agent assigned to task

    activate ia 
    ia ->> host: implements changes
    ia ->> fo: report task completion
    fo ->> forgetful: updates tasks 
    fo ->> gh: invokes ci 
    fo ->> gh: checks for ci result
    alt ci issues
        fo ->> ia: ask for ci issues correction
        ia ->> host: corrects ci issues
        ia ->> fo: reports issues resolved
        fo ->> gh: invokes ci 
    end
    deactivate ia

    fo ->> gh: raise pr 
    fo ->> forgetful: update tasks
    fo ->> ra: prompt agent to review pr
    fo ->> forgetful: record agent assigned to task
    activate ra 
    ra ->> host: review changes
    ra ->> gh: provide feedback 
    ra ->> fo: reports feedback finished
    deactivate ra
    alt issues found
        fo ->> ia: ask to fix the issues
        ia ->> host: implement fixes 
        ia ->> fo: reoport issues fixed
        ia ->> gh: invokes ci (same loop as before)
    end

    fo ->> forgetful: update tasks mark plan as completed
    fo ->> host: document adrs in repo
    fo ->> gh: adds adrs to pr and merges the pr into main
    fo ->> host: cleans up worktrees and branch
    fo ->> foreman: reports completed
    deactivate fo

    activate gh
    gh ->> e2e: deploy new version of main     
    gh ->> e2e: executes e2e regression tests
    foreman ->> gh: monitors for e2e deployment and test progress
    deactivate gh
    alt issues during e2e
        foreman ->> gh: raises new issue
    end 
    deactivate foreman
    deactivate script
```

## Agent Setup

Beyond the below configuration each agent will utilise a predefined list of agents that each have
their own system prompt, tools (inc mcp) and skills.

|Agent|Tools|Skills|Responsibilties|
|-----|-----|------|---------------|
|Foreman|`forgetful`,`agent-shell`, `github`|`foreman`|Notified on new issues -> launches feature owners -> monitors feature owners -> communicates with user|
|Feature Owner|`forgetful`,`agent-shell`, `github`|`feature-owner`|Launched by Foreman -> uses grill me skill -> updates issues and foreman if more info needed -> builds proper plan -> launches implementation_agent_effort -> launches reviewer -> updates forgetful -> speaks to foreman|
|Implementation Agent|`bash`, `browser-tools/computer-use`, `github`|`tdd`, `{application-specific-architecture-skills}`|Launched by the feature owner -> implements changes -> commits -> fixes issues|
|Reviewer Agent|`bash`, `browser-tools/computer-use`, `github`|`{application or organisation specific coding standards}`|Launched by the feature owner -> reviews pr -> reoports back to github|

## Tools
|Tool|Description|
|----|-----------|
|`forgetful`|[forgetful](https://github.com/ScottRBK/forgetful) is an mcp agent memory layer, also supports cli|
|`agent-shell`|[pi extension](https://github.com/ScottRBK/pi-agentshell-extension) or [python libary](https://github.com/ScottRBK/agent-shell) that abstracts the invocation of cli agents|
|`browser-tools`|tools used to give an agent access to a web browse, needed for reviewing or building web based apps|
|`computer-use`|grants an agent access to use a machine, needed for reviewing or building rich clients|
|`github`|tool to access gh, can just be gh cli installed with appropriate permissions| 

## Skills
|Skill|Description|
|-----|-----------|
|`foreman`|describes the roles and responsiblities of the foreman, along with expected workflow|
|`feature-owner`|describes the roles and responsibilities of the feature owner, along with expected workflow|
|`tdd`|skill for describing test driven development approach|
|`{application-specific-architecture-skills}`|skills pertaining to how the application should be implemented, eg hexagonal architectture, rust error handling etc.|
|`{application or organisation specific coding standards}`|any skills or instrunctions relating to coding standards|
## Configuration

The intention behind this repo is that it can be placed inside that of another repo and drive the
development of that repo using the software factory life-cylce.

You can configure a factory using the factory.toml file which allows the configuration of the following:

|Configuration|Type|Example|Description|
|-------------|-----|------|----------|
|repositories|dict|[{ remote: "git@github.com:ScottRBK/forgetful.gi", local_dir: "~/gh/forgetful"}, {remote: "git@github.com:ScottRBK/agentshell.gi", local_dir: "~/ai/agentshell"}]|List of repositories that are monitored by the factory, can support multiple if required|
|watcher_label|list[string]|"factory"|list of strings indicating which labels the watcher should pick up, must be specified, accepts * as wild card for all|
|foreman_agent_model|string|"openai-codex/gpt-6.1-sol"|set the provider and model information for the foreman agent|
|foreman_agent_effort|string|"max"|thinking effort level of the foreman agent|
|feature_owner_agent_model|string|"openai-codex/gpt-6.1-sol"|set the provider and model information for the foreman agent|
|feature_owner_agent_harness|string|"codex"|agentic harness for the feature owner agent|
|feature_owner_agent_effort|string|"max"|thinking effort level of the foreman agent|
|implementation_agent_model|string|"openai-codex/gpt-6-luna"|set the provider and model information for the foreman agent|
|implementation_agent_harness|string|"codex"|agentic harness for the feature owner agent|
|implementation_agent_effort|string|"xhigh"|thinking effort level of the foreman agent|
|review_agent_model|string|"opus"|set the provider and model information for the review agent|
|review_agent_harness|string|"claude_code"|agentic harness for the review agent|
|review_agent_effort|string|"high"|thinking effort level of the review agent|




