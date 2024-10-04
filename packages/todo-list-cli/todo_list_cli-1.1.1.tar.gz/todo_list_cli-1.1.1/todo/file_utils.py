import json
import os

TODO_FILE = "todo.json"


def create_todo_file():
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, "w") as file:
            json.dump([], file)


def load_todo_file():
    create_todo_file()
    with open(TODO_FILE, "r") as file:
        return json.load(file)


def save_todo_file(data):
    with open(TODO_FILE, "w") as file:
        json.dump(data, file, indent=4)
