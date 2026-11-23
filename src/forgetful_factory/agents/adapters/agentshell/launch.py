"""Files and modules started by path or module name. Import rules cannot see these links."""
from pathlib import Path

CONTROLLER = Path(__file__).resolve().with_name('controller.py')
MODEL_CATALOG = Path(__file__).resolve().with_name('model_catalog.py')
OWNER_MODULE = 'forgetful_factory.agents.adapters.agentshell.owner'
TMUX_HOST = Path(__file__).resolve().with_name('tmux_host.py')
