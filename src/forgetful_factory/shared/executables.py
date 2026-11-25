import os
from pathlib import Path


def executable_path(workspace: Path) -> str:
    """PATH with the tools Factory installs for this workspace (Pi, Forgetful) first."""
    runtime = workspace / '.factory/runtime'
    return os.pathsep.join((str(runtime / 'pi/node_modules/.bin'),
                            str(runtime / 'forgetful/bin'), os.environ.get('PATH', '')))
