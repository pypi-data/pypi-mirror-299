from .file_utils import load_todo_file, save_todo_file
from rich.console import Console
from rich.table import Table
import typer

console = Console()


def find_task(data, identifier):
    """Find a task by title or id"""
    for task in data:
        if task["title"] == identifier or str(task["id"]) == identifier:
            return task
    return None


def change_all_tasks(data, status):
    """Change all tasks status"""
    for task in data:
        task["done"] = status
    save_todo_file(data)


def add_task(title: str):
    """Add a new task to the todo list"""
    data = load_todo_file()

    data.append({"id": len(data) + 1, "title": title, "done": False})

    save_todo_file(data)
    typer.echo(f"Task '{title}' added!")


def remove_task(identifier: str):
    """Remove a task by title or id"""
    data = load_todo_file()

    task = find_task(data, identifier)

    if task:
        data.remove(task)
        save_todo_file(data)
        typer.echo(f"Task '{identifier}' removed!")
    else:
        typer.echo(f"No task found with title or id '{identifier}'")


def check_task(identifier: str, all_tasks: bool = False):
    """Check a task as done"""
    data = load_todo_file()

    if all_tasks:
        change_all_tasks(data, True)
        typer.echo("All tasks checked!")
        return

    task = find_task(data, identifier)

    if task:
        task["done"] = True
        save_todo_file(data)
        typer.echo(f"Task '{identifier}' checked!")
    else:
        typer.echo(f"No task found with title or id '{identifier}'")


def uncheck_task(identifier: str, all_tasks: bool = False):
    """Uncheck a task"""
    data = load_todo_file()

    if all_tasks:
        change_all_tasks(data, False)
        typer.echo("All tasks unchecked!")
        return

    task = find_task(data, identifier)

    if task:
        task["done"] = False
        save_todo_file(data)
        typer.echo(f"Task '{identifier}' unchecked!")
    else:
        typer.echo(f"No task found with title or id '{identifier}'")


def list_tasks():
    """List all tasks with enhanced UI"""
    data = load_todo_file()

    if data:
        table = Table(title="Todo List", show_header=True, header_style="bold magenta")

        table.add_column("ID", style="dim", width=6)
        table.add_column("Title", style="bold", min_width=20)
        table.add_column("Status", style="bold", justify="center")

        for task in data:
            done_status = "[green]✔ Done" if task["done"] else "[red]✘ Not Done"
            table.add_row(str(task["id"]), task["title"], done_status)

        console.print(table)
    else:
        console.print("[bold yellow]No tasks found![/bold yellow]")
