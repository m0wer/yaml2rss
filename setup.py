"""Package setup module."""

from setuptools import find_packages, setup

setup(
    name="yaml2rss",
    version="0.0.0",
    description="Generate a RSS podcast feed from YAML.",
    author="m0wer",
    author_email="m0wer@autistici.org",
    license="GPLv3",
    long_description=open("README.md").read(),
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "pydantic",
        "typer",
    ],
)
