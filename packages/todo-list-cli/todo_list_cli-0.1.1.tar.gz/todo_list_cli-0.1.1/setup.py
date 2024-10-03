from setuptools import setup, find_packages

setup(
    name="todo_list_cli",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    description="A CLI todo app built with Typer and Rich",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/renancavalcantercb/todo-list-cli",
    author="Renan Cavalcante",
    author_email="renancavalcantercb@protonmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "typer[all]",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "todo_list_cli=todo.__main__:start_shell",
        ],
    },
    python_requires=">=3.7",
)
