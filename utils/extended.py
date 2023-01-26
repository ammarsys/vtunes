"""Module with support functions for the main CLI"""

import json
import os
import time
import subprocess
import re

from dataclasses import dataclass
from typing import Optional

from youtubesearchpython import VideosSearch  # type: ignore
from terminalcolorpy import colored  # type: ignore


PATH_REGEX = re.compile("[a-zA-Z][a-zA-Z ]+")


@dataclass
class Translation:
    """Dataclass for all values in translation json. Structure should remain like this because of linter support."""

    localName: str
    code: str
    number: int

    pathInput: str
    badPath: str
    enterSong: str
    whichSong: str
    badInt: str
    outOfRange: str
    whichSongDefault: str
    noSongsFound: str
    songDown: str


def load_json() -> list[Translation]:
    """Load the JSON file and return a list containing Translation dataclasses"""

    with open("utils/translations.json") as translations:
        data = json.load(translations)

    to_return = []

    for language in data:
        indexed = data[language]

        to_return.append(
            Translation(
                indexed["localName"],
                indexed["code"],
                indexed["number"],
                **indexed["translations"],
            )
        )

    return to_return


def cls() -> None:
    """Clear the command line"""

    subprocess.call("cls", shell=True)


def parse_input(
    max_length: int,
    inp_text: Optional[str] = None,
    not_int: Optional[str] = None,
    out_range: Optional[str] = None,
) -> int:
    """
    Parse inputs

    Validate inputs for the following conditions,
        - whether given input is an integer
        - whether given input is in / out of range
    """

    while True:
        while not (chosen := input(inp_text or colored(">> ", "red"))).isdecimal():
            print(not_int or "The given value isn't an integer, please try again.")

        # Do not write as 'not chosen'.
        chosen = int(chosen)
        if 1 <= chosen <= max_length or chosen == 0:
            break

        print(out_range or "The given value is out of range, please try again.")

    return int(chosen)


def parse_path(language: Translation) -> str:
    """Parse path and check its validity"""

    while not os.access(
        path := input(language.pathInput + colored(" >> ", "red")), os.W_OK
    ):
        print(language.badPath)

    if path[-1] not in ("/", "\\"):
        path += "\\"

    print(path)
    return path


def parse_songs(language: Translation) -> list[tuple[str, str]]:
    """
    Parse songs,

    Not much to say here, most of the stuff is cosmetic. Basically, handle & validate user input until they choose to
    stop. With the given input(s), search for songs and return them.
    """

    to_download = []

    while True:
        cls()
        print(language.whichSongDefault)

        query = input(language.enterSong + colored(" >> ", "red"))

        if query.lower() == "stop":
            break

        results = VideosSearch(query, limit=15).result()

        for c, i in enumerate(results["result"]):
            print(f"{colored(f'{c + 1}', 'green')}. | {i['duration']} {i['title']}")

        if not len(results["result"]):
            print(language.noSongsFound)
            time.sleep(2)
            continue

        parsed_input = parse_input(
                15,
                language.whichSong + colored(" >> ", "red"),
                language.badInt,
                language.outOfRange,
            ) - 1

        if parsed_input == -1:
            continue

        result_value = results["result"][parsed_input]
        to_download.append((result_value["link"], result_value["title"]))  # type: ignore

    return to_download


def parse_filename(fl: str) -> str:
    """Remove any characters that may not be valid in a filename (allow only alphabetical chars)."""

    return PATH_REGEX.sub("", fl)
