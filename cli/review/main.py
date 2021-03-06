import click
import frontmatter
import requests
import os
from datetime import date
from cli.service.search import Search
from cli.service.tm import Tm
from cli.picture.main import Im
from cli.service.wiki import WikiSearch
from PyInquirer import prompt


class Review:
    """Will handle the Review part"""

    def __init__(self, tmdb_key, api_key, template, project):
        self.tmdb_key = tmdb_key
        self.api_key = api_key
        self.template = template
        self.project = project

    def _imdb_search(self):
        a = Search(self.api_key, self.template)
        return a.data()

    def _movie_certificate(self, language):
        if language.lower() == "korean":
            choices = ["G-General", "PG_12-Age 12+", "PG_15-Age 15+", "R_18-Age 18+"]
        elif language.lower() == "hindi" or language.lower() == "nepali":
            choices = [
                "U-Unrestricted",
                "UA-Unrestricted with Caution",
                "A-Adults",
                "S-Restricted to special classes",
            ]
        else:
            choices = [
                "G-General Audiences",
                "PG-Parental Guidance Suggested",
                "PG_13-Parents Strongly Cautioned",
                "R-Restricted" "NC_17–Adults Only",
            ]
        movie_certi = [
            {
                "type": "list",
                "name": "mC",
                "message": "Identify the movie Certificate",
                "choices": choices,
                "filter": lambda val: val.split("-")[0].replace("_", "-"),
            }
        ]
        result = prompt(movie_certi)
        self.template["movie"]["rating"] = result["mC"]

    def _download_image(self, image_url, image_aspect_change):
        img_data = requests.get(image_url).content
        movie_name = self.template["movie_name"]
        with open(
            os.path.join(self.project, "assets", "images", f"{movie_name}.jpg"), "wb",
        ) as handler:
            handler.write(img_data)
        if image_aspect_change:
            image_convert = Im(
                os.path.join(self.project, "assets", "images", f"{movie_name}.jpg")
            )
            image_convert.format_image()

    def _create_review(self, trailer):
        review_date = date.today().strftime("%Y-%m-%d")
        name = self.template["movie_name"]
        self.template["date"] = date.today()
        nl = "\n"
        if trailer:
            trailer_part = f'{{% youtube "{trailer}" %}}'
            body = f"nothing {nl}{trailer_part}"
        else:
            body = "nothing"
        post = frontmatter.Post(body, **self.template)
        with open(
            os.path.join(self.project, "_posts", review_date + "-" + name + ".md"), "w"
        ) as f:
            f.write(frontmatter.dumps(post))
        click.echo(
            click.style(f"The page for review {name} has been created", fg="green")
        )

    def create(self):
        movie = self.template["movie_name"]
        click.echo(click.style(f"Looking through imdb for movie {movie}", fg="green"))
        self.template, imdb_id = self._imdb_search()
        click.echo(click.style(f"Now time to lo0k into tmdb for {movie}", fg="green"))
        tmdb = Tm(self.template, imdb_id)
        self.template, trailer = tmdb.get_info()
        rated = False
        if "rating" in self.template["movie"]:
            rated = True
        if "genre" in self.template["movie"]:
            self.template["tags"].extend(self.template["movie"]["genre"])

        if not rated:
            self._movie_certificate(self.template["language"])
        click.echo(
            click.style(f"Now time to lo0k into wikipedia for {movie}", fg="green")
        )
        w = WikiSearch(self.template)
        self.template = w.wiki_search()
        image_aspect_change = False
        if self.template["image"] != "change":
            name = self.template["movie_name"]
            if "tmdb" not in self.template["image"]:
                click.echo(
                    click.style(
                        f"The image {name}.jpg might need to be converted to 2:3 aspect ratio",
                        fg="red",
                    )
                )
                image_aspect_change = True
            self._download_image(self.template["image"], image_aspect_change)
            self.template["image"] = os.path.join("/assets/images", f"{name}.jpg")

        self._create_review(trailer)
