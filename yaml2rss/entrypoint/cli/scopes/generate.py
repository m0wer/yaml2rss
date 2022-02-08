"""Render scope."""
from typer import Typer

from yaml2rss.service.service import generate_podcast

cli = Typer()


@cli.command()
def podcast(config_path: str, output_path: str) -> None:
    """Generate podcast feed from YAML.

    Arguments:
        conf_path: Path to the YAML file with the feed data.
        output_path: Path where the result should be written to.
    """
    generate_podcast(config_path=config_path, output_path=output_path)
