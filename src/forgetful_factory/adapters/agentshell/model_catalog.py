"""List native Pi models through AgentShell, in the caller's consented environment."""
import asyncio
import json

from agent_shell.models.agent import AgentType
from agent_shell.shell import AgentShell


async def main() -> None:
    import os

    models = await AgentShell(AgentType.PI).list_models(os.getcwd())
    print(json.dumps(models))


if __name__ == '__main__':
    asyncio.run(main())
