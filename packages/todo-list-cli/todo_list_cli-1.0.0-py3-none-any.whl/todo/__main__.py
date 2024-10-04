import sys
import typer
from todo.interactive_shell import interactive_shell
from todo.task_manager import (
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
def check(identifier: str):
    """Mark a task as done"""
    check_task(identifier)


@app.command()
def uncheck(identifier: str):
    """Mark a task as not done"""
    uncheck_task(identifier)


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
