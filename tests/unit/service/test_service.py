from yaml2rss.service.service import generate_podcast


class TestService:
    def test_render_template(self, tmpdir):
        image_file = tmpdir.join("logo.jpg")
        image_file.write("")
        config_path = "config.yaml"
        config_yaml_file = tmpdir.join(config_path)
        config_yaml_file.write(
            f"""---

            title: Some podcast
            description: >
              Podcast about random things.
            link: https://domain.tld/
            image_path: {tmpdir}/logo.jpg
            #image_title:
            feed_path: podcast.xml
            author: Someone
            email: someone@domain.tld
            copyright: Someone 2022
            language: en
            files_root_path: {tmpdir}/
            #files_root_url:

            seasons: []
            """
        )
        output_path = "output.xml"
        output_file = tmpdir.join(output_path)

        generate_podcast(config_path=config_yaml_file, output_path=output_file)
        assert len(output_file.read()) > 0
        assert "Some podcast" in output_file.read()
