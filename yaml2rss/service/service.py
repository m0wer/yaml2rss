"""Module to store the package services (mediators between
entrypoints and domain)."""

import yaml
from jinja2 import Template
from pydantic import FilePath

from yaml2rss.domain.template import PodcastTemplateConfig, render
from yaml2rss.service.jinja_environment import jinja_environment


def generate_podcast(config_path: FilePath, output_path: str) -> None:
    """Write the rendered podcast feed to a file.

    Arguments:
        conf_path: Path to the YAML file with the feed data.
        output_path: Path where the result should be written to.
    """
    template: Template = jinja_environment.get_template("podcast.xml.j2")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    result: str = render(
        template=template,
        template_config=PodcastTemplateConfig.parse_obj(config),
    )

    with open(output_path, "w") as file:
        file.write(result)
