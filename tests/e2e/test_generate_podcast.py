from os import getcwd, mkdir
from shutil import copy

from typer.testing import CliRunner

from yaml2rss.entrypoint.cli.main import cli

runner = CliRunner()


class TestGeneratePodcast:
    def test_generate_podcast(self, tmpdir):
        repo_root_path: str = getcwd()

        with runner.isolated_filesystem():
            copy(repo_root_path + "/examples/podcast.yaml", "podcast.yaml")
            mkdir("images")
            open("images/logo.jpg", "a").close()
            mkdir("recordings")
            copy(
                repo_root_path + "/examples/sample-3s.mp3",
                "recordings/first_episode.mp3",
            )
            copy(
                repo_root_path + "/examples/sample-3s.mp3",
                "recordings/second_episode.mp3",
            )

            result = runner.invoke(
                cli, ["generate", "podcast", "podcast.yaml", "podcast.xml"]
            )
            assert result.exit_code == 0

            with open("podcast.xml", "r") as file:
                assert "Some podcast" in file.read()
