from betterqa import *


def run():
    console.print(f"[bold green]hello world :smile: {__version__}[/bold green]")
    name = prompt.ask(console=console, prompt="[bold yellow]Enter your name:question:[/bold yellow]")
    console.print(name)


if __name__ == '__main__':
    run()
