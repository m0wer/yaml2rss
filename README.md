# yaml2rss

[![Actions Status](
https://github.com/m0wer/yaml2rss/workflows/main.yml/badge.svg
)](https://github.com/m0wer/yaml2rss/actions)
[![pre-commit](
https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
)](https://github.com/pre-commit/pre-commit)

## Installation

Run `pip install .`.

## Usage

### Generate podcast feed

1. Copy and modify `examples/podcast.yaml`.
1. From the root path of your podcast project (where the `recordings/`
  directory is), run:
  ```bash
  yaml2rss generate podcast podcast.yaml podcast.xml
  ```

#### Example build script

This scripts converts the audio files to the same format, normalizes the
volume and creates a zip file with all the recordings:

```bash
#!/bin/sh

set -e

parallel "ffmpeg -i {1} {1.}.mp3 && rm {1}" ::: recordings/*.ogg || true
mp3gain -r -k -a -c recordings/*.mp3
yaml2rss generate podcast podcast.yaml podcast.xml
zip -r recordings.zip recordings/*.mp3
```

## Development

Run `make install` to install all development dependencies.

## Documentation

You can access the online version at <https://m0wer.github.io/yaml2rss/>.

Alternatively, after `make install`, to render the documentation run:

```bash
pip install -r requirements.txt
mkdocs serve
```

You can now access the docs at <http://localhost:8000>.
