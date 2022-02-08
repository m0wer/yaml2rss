from jinja2 import Template

from yaml2rss.domain.template import render


class TestTemplate:
    def test_render(self):
        title = "test"

        result = render(
            template=Template("Example {{ title }}."),
            template_config=dict(
                title=title,
                description="Podcast about random things.",
                link="https://domain.tld/",
                image_path="images/logo.jpg",
                feed_path="podcast.xml",
                author="Someone",
                email="someone@domain.tld",
                seasons=[],
            ),
        )

        assert result == f"Example {title}."
