from rich.console import Console
from rich.prompt import Prompt

__all__ = [
    "__appname__",
    "__version__",
    "console",
    "prompt"
]
__appname__ = "betterqa"
__version__ = "0.1.4"

console = Console(force_terminal=True, emoji=True,force_interactive=True)
prompt = Prompt()
