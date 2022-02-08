"""Package setup module."""

__requires__ = ["pip < 22"]
from setuptools import find_packages, setup

setup(
    name="yaml2rss",
    version="0.1.0",
    description="Generate a RSS podcast feed from YAML.",
    author="m0wer",
    author_email="m0wer@autistici.org",
    license="GPLv3",
    long_description=open("README.md").read(),
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "email-validator",
        "Jinja2",
        "librosa",
        "python-magic",
        "pydantic",
        "pyyaml",
        "typer",
    ],
    entry_points="""
        [console_scripts]
        yaml2rss=yaml2rss.entrypoint.cli.main:cli
    """,
    package_data={"yaml2rss": ["templates/*.j2"]},
)
