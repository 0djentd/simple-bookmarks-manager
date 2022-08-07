import os

from dataclasses import dataclass

import rich
import click
import appdirs

from simple_bookmarks_manager import __version__


_HELP_TEXT = """
Simple bookmarks manager.
"""

_DATA_DIR = appdirs.user_data_dir(
        appname="simple_bookmarks_manager", version=__version__)

_DEFAULT_BOOKMARKS_FILE = os.path.join(_DATA_DIR, "bookmarks")


@dataclass
class Config:
    bookmarks: str
    debug: bool = False


@click.group(help=_HELP_TEXT)
@click.option("--bookmarks", type=str,
              default=_DEFAULT_BOOKMARKS_FILE, help="Path to bookmarks file")
@click.option("--debug", type=bool, default=False)
@click.pass_context
def commands(context, *args, **kwargs):
    context.obj = Config(**kwargs)


@commands.command("add")
@click.argument("URL", nargs="+")
@click.pass_context
def add_bookmarks(context, *args, **kwargs):
    for url in args:
        print(url)


def main():
    commands()


if __name__ == "__main__":
    main()
