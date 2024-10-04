import sys
import typer
from interactive_shell import interactive_shell
from task_manager import (
    add_task,
    remove_task,
    check_task,
    uncheck_task,
    list_tasks,
)

app = typer.Typer()


@app.command()
def add(title: str):
    """Add a new task"""
    add_task(title)


@app.command()
def remove(identifier: str):
    """Remove a task by title or id"""
    remove_task(identifier)


@app.command()
def check(
    identifier: str = typer.Argument(None), all: bool = typer.Option(False, "--all")
):
    """Mark a task as done, or all tasks if --all is passed"""
    check_task(identifier, all_tasks=all)


@app.command()
def uncheck(
    identifier: str = typer.Argument(None), all: bool = typer.Option(False, "--all")
):
    """Unmark a task as done, or all tasks if --all is passed"""
    uncheck_task(identifier, all_tasks=all)


@app.command()
def list():
    """List all tasks"""
    list_tasks()


@app.command()
def start_shell():
    """Start the interactive mode"""
    interactive_shell()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_shell()
    else:
        app()
