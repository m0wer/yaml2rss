"""Module to store the template domain functions and classes."""

from datetime import datetime
from os.path import getsize
from pathlib import Path
from typing import List, Sequence

import jinja2
import magic
from librosa import get_duration
from pydantic import (
    BaseModel,
    DirectoryPath,
    EmailStr,
    FilePath,
    HttpUrl,
    ValidationError,
    root_validator,
)

mime = magic.Magic(mime=True)
SUPPORTED_AUDIO_MIME_TYPES: List[str] = ["audio/mpeg"]


class EpisodeConfig(BaseModel):
    """Episode configuration.

    Attributes:
        title: Episode title.
        description: Episode description.
        pub_date: Episode publication date.
        url: Episode URL.
        author: Episode author.
    """

    title: str
    description: str
    pub_date: datetime
    url: str
    author: str = None


class FileDetails(BaseModel):
    """File details.

    Attributes:
        file: File path.
        length: File length in bytes.
        duration: File duration in seconds.
        type: File mime type.
    """

    file: FilePath
    length: int
    duration: int
    type: str

    @root_validator(pre=True)
    @classmethod
    def validate_length(cls, values):
        """Get file length in bytes if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        if "length" not in values or values["length"] is None:
            values["length"] = getsize(values["file"])

        return values

    @root_validator(pre=True)
    @classmethod
    def validate_duration(cls, values):
        """Get file duration in seconds if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        if "duration" not in values or values["duration"] is None:
            values["duration"] = int(get_duration(filename=values["file"]))

        return values

    @root_validator(pre=True)
    @classmethod
    def validate_type(cls, values):
        """Get file mime type if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        if "type" not in values or values["type"] is None:
            values["type"] = mime.from_file(values["file"])

        if values["type"] not in SUPPORTED_AUDIO_MIME_TYPES:
            raise ValidationError()

        return values


class PodcastEpisodeConfig(EpisodeConfig):
    """Extension of episode configuration for a podcast episode.

    Arguments:
        file_details: Details of the podcast audio file.
    """

    file_details: FileDetails


class SeasonConfig(BaseModel):
    """Season configuration.

    Arguments:
        episodes: List of season episodes configuration.
    """

    episodes: Sequence[EpisodeConfig]


class PodcastSeasonConfig(SeasonConfig):
    """Pocast season configuration.

    Arguments:
        episodes: List of podcast season episodes configuration.
    """

    episodes: List[PodcastEpisodeConfig]


SeasonsConfig = Sequence[SeasonConfig]
PodcastSeasonsConfig = List[PodcastSeasonConfig]


class TemplateConfig(BaseModel):
    """Generic feed template configuration.

    Attributes:
        title: Feed title.
        description: Feed description/summary.
        link: Feed home page link (base URL).
        feed_path: Path of the feed XML file relative to `link`.
        author: Feed author.
        email: Feed author email.
        copyright: Feed copyright notice.
        language: Feed language two-letter code.
        last_build_date: Feed last build date.
        seaons: Feed seasons configuration.
    """

    title: str
    description: str
    link: HttpUrl
    feed_path: Path
    author: str
    email: EmailStr
    copyright: str = None
    language: str = "en"
    last_build_date: datetime = datetime.now()
    seasons: SeasonsConfig

    @root_validator(pre=True)
    @classmethod
    def validate_copyright(cls, values):
        """Set the copyright notice if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        if "copyright" not in values or values["copyright"] is None:
            values["copyright"] = f"Copyright {values['author']}."

        return values

    @root_validator(pre=True)
    @classmethod
    def validate_episode_author(cls, values):
        """Set the episode author to the feed author if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        for season in values["seasons"]:
            for episode in season["episodes"]:
                if "author" not in episode or episode["author"] is None:
                    episode["author"] = values["author"]

        return values


class PodcastTemplateConfig(TemplateConfig):
    """Template for podcast RSS feed.

    Arguments:
        image_path: Path to feed image relative to `link`.
        image_title: Feed image title.
        files_root_url: Base URL for the feed audio files.
        files_root_path: Path to the directory containing the audio files.
        seasons: Podcast seasons configuration.
    """

    image_path: FilePath
    image_title: str
    files_root_url: HttpUrl
    files_root_path: DirectoryPath = Path("")
    seasons: PodcastSeasonsConfig

    @root_validator(pre=True)
    @classmethod
    def validate_image_title(cls, values):
        """Set the episode author to the feed author if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        if "image_title" not in values or values["image_title"] is None:
            values["image_title"] = values["title"]

        return values

    @root_validator(pre=True)
    @classmethod
    def validate_files_root_url(cls, values):
        """Set the files root URl to `link` if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        if "files_root_url" not in values or values["files_root_url"] is None:
            values["files_root_url"] = values["link"]

        return values

    @root_validator(pre=True)
    @classmethod
    def validate_episode_file(cls, values):
        """Add the `files_root_path` to the episodes files.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        for season in values["seasons"]:
            for episode in season["episodes"]:
                file_details: dict = episode["file_details"]
                if "file" in file_details and file_details["file"] is not None:
                    episode["file_details"]["file"] = (
                        values["files_root_path"] + file_details["file"]
                    )

        return values

    @root_validator(pre=True)
    @classmethod
    def validate_episode_url(cls, values):
        """Set the episodes URL to `files_root_url` + `file` if None.

        Arguments:
            cls: Class.
            values: Instance initialization values.

        Returns:
            Values with required modifications.
        """
        for season in values["seasons"]:
            for episode in season["episodes"]:
                if "url" not in episode or episode["url"] is None:
                    episode["url"] = (
                        values["files_root_url"]
                        + episode["file_details"]["file"]
                    )

        return values


def render(template: jinja2.Template, template_config: TemplateConfig) -> str:
    """Render the template with the passed configuration.

    Arguments:
        template: Jinja template.
        template_config: Template variable values to replace.

    Returns:
        Rendered template.
    """
    return template.render(template_config)
