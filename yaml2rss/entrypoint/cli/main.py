"""Module to store the CLI."""

from typer import Typer

from .scopes import generate

cli = Typer()

cli.add_typer(generate.cli, name="generate")

if __name__ == "__main__":
    cli()
