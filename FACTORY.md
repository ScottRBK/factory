# Factory 
This repo documents the inner workings of a software factory.

## Inspiration

Inspired by [jovaneyck/software-factory-demo](https://github.com/jovaneyck/software-factory-demo/tree/main/.agents)

## Components 

|Component|Role|
|---------|----|
|Factory.sh|Script that will be responsible for monitoring configured github repositories, creating plans and passing info to the foreman|

```mermaid
---
config:
    theme: dark
---
    sequenceDiagram
    
    participant gh as Github
    participant script as Watcher
    participant forgetful
    participant host as Host Enivronment
    participant e2e as End to End test environment
    actor foreman as Foreman Agent
    actor fo as Feature Owner
    actor ia as Implementation Agent 
    actor ra as Review Agent

    script ->> gh: polls for issues
    activate script
    gh -->> script: new issue
    script ->> forgetful: creates plan scaffold
    script ->> host: creates worktree 
    script ->> foreman: send prompt with worktree and forgetful info
    deactivate script

    foreman ->> fo: send prompt with issue information, scaffolded plan info in worktree
    activate fo
    fo ->> forgetful: generate proper plan 
    fo ->> ia: prompt one or more implementation agents to fetch tasks in forgetful 

    activate ia 
    ia ->> host: implements changes
    ia ->> forgetful: updates tasks 
    ia ->> fo: report task completion
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
    fo ->> forgetful: update plan
    fo ->> ra: prompt agent to review pr
    activate ra 
    ra ->> host: review changes
    ra ->> fo: provide feedback
    deactivate ra
    alt issues found
        fo ->> ia: ask to fix the issues
        ia ->> host: implement fixes 
        ia ->> fo: reoport issues fixed
        ia ->> gh: invokes ci (same loop as before)
    end
    fo ->> foreman: advise that the pr is ready for merge
    gh ->> e2e: deploy new version of main     
    deactivate fo
```

## Configuration

The intention behind this repo is that it can be placed inside that of another repo and drive the
development of that repo using the software factory life-cylce.

You can configure a factory using the factory.toml file which allows the configuration of the following:

|Configuration|Type|Example|Description|
|-------------|-----|------|----------|
|repositories|list|["git@github.com:ScottRBK/forgetful.gi", "git@github.com:ScottRBK/agentshell.gi"]|List of repositories that are monitored by the factory, can support multiple if required|
|number_one|string|"openai-codex/gpt-6.1-sol"|set the provider and model information for the number one agent|



