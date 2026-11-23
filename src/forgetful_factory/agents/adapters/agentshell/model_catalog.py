"""List native Pi models through AgentShell, in the caller's consented environment."""
import asyncio
import json
import sys

from agent_shell.models.agent import AgentType
from agent_shell.shell import AgentShell


async def main() -> None:
    import os

    harness = AgentType(sys.argv[1]) if len(sys.argv) > 1 else AgentType.PI
    models = await AgentShell(harness).list_models(os.getcwd())
    print(json.dumps(models))


if __name__ == '__main__':
    asyncio.run(main())
