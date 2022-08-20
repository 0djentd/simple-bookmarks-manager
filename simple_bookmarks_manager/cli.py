import os
import json

from typing import Optional, List

import rich
import click
import appdirs
import pyperclip

from pydantic import BaseModel

from simple_bookmarks_manager import __version__


_HELP_TEXT = """
Simple bookmarks manager.
"""

_DATA_DIR = appdirs.user_data_dir(
    appname="simple_bookmarks_manager", version=__version__)

_DEFAULT_BOOKMARKS_FILE = os.path.join(_DATA_DIR, "bookmarks")


class Config(BaseModel):
    bookmarks: str
    debug: bool = False


class Bookmark(BaseModel):
    url: str
    title: Optional[str] = None

    @property
    def line(self) -> str:
        return json.dumps(self.dict())


@click.group(help=_HELP_TEXT)
@click.option("--bookmarks", type=str,
              default=_DEFAULT_BOOKMARKS_FILE, help="Path to bookmarks file")
@click.option("--debug", type=bool, default=False)
@click.pass_context
def commands(context, *args, **kwargs):
    context.obj = Config(**kwargs)


def _read_bookmarks(context) -> List:
    config = context.obj
    result = []
    with open(config.bookmarks, "r", encoding="utf-8") as file:
        for line in file:
            result.append(Bookmark(url=line))
    return result


def _check_if_already_in_bookmarks(context, url) -> Optional[Bookmark]:
    for x in _read_bookmarks(context):
        if x.url == url:
            return x
    return None


def _add_to_bookmarks(context, url) -> None:
    config = context.obj
    if _check_if_already_in_bookmarks(context, url):
        return
    with open(config.bookmarks, "a", encoding="utf-8") as file:
        file.write(Bookmark(url=url).line)
    return


@commands.command("add")
@click.argument("urls", nargs=-1)
@click.pass_context
def add_bookmarks(context, urls, *args, **kwargs):
    for url in urls:
        _add_to_bookmarks(context, url)
    return


@commands.command("add-from-clipboard")
@click.pass_context
def add_bookmark_from_clipboard(context, *args, **kwargs):
    url = pyperclip.copy()
    _add_to_bookmarks(context, url)
    return


def main():
    commands()


if __name__ == "__main__":
    main()
