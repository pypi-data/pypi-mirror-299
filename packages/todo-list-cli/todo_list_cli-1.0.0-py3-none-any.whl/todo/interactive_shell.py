import typer
from .task_manager import add_task, remove_task, check_task, uncheck_task, list_tasks


def interactive_shell():
    """Enter an interactive mode"""
    typer.echo(
        "Welcome to the todo CLI! Type commands (add, remove, check, uncheck, list) or 'exit' to quit."
    )

    commands = {
        "add": add_task,
        "check": check_task,
        "uncheck": uncheck_task,
        "remove": remove_task,
        "list": list_tasks,
        "ls": list_tasks,
    }

    while True:
        try:
            command = input("> ").strip()
            if command == "exit":
                typer.echo("Exiting...")
                break

            cmd, *args = command.split(maxsplit=1)
            if cmd in commands:
                if args:
                    commands[cmd](*args)
                else:
                    commands[cmd]()
            else:
                typer.echo(f"Unknown command: {cmd}")
        except (KeyboardInterrupt, EOFError):
            typer.echo("\nExiting...")
            break
        except TypeError:
            typer.echo(f"Incorrect usage of command: {cmd}")
