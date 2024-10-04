import typer
from .task_manager import add_task, remove_task, check_task, uncheck_task, list_tasks


def interactive_shell():
    """Enter an interactive mode"""
    typer.echo(
        "Welcome to the todo CLI! Type commands (add, remove, check, uncheck, list) or 'exit' to quit."
    )

    commands_with_flags = {"check": check_task, "uncheck": uncheck_task}
    commands_without_flags = {
        "add": add_task,
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

            cmd, *args = command.split()

            if cmd in commands_with_flags:
                all_flag = "--all" in args
                task_name = None if all_flag else " ".join(args)
                commands_with_flags[cmd](identifier=task_name, all_tasks=all_flag)

            elif cmd in commands_without_flags:
                if args:
                    commands_without_flags[cmd](" ".join(args))
                else:
                    commands_without_flags[cmd]()

            else:
                typer.echo(f"Unknown command: {cmd}")

        except (KeyboardInterrupt, EOFError):
            typer.echo("\nExiting...")
            break
        except TypeError:
            typer.echo(f"Incorrect usage of command: {cmd}")
