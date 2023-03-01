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

PATH_REGEX = re.compile("[^A-Za-z0-9 ]+")


@dataclass
class Language:
    """Dataclass for all values in 'languages.json'. Structure should remain like this because of linter support."""

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
    endText: str


def load_json() -> list[Language]:
    """Load the JSON file and return a list containing Translation dataclass instances"""

    with open("languages.json") as translations:
        data = json.load(translations)

    to_return = []

    for language in data:
        indexed = data[language]

        to_return.append(
            Language(
                indexed["localName"],
                indexed["code"],
                indexed["number"],
                **indexed["translations"],
            )
        )

    return to_return


def cls() -> None:
    """Clear the command line by making a system call for the Windows cls command"""

    subprocess.call("cls", shell=True)


def parse_input(
    max_length: int,
    inp_text: Optional[str] = None,
    not_int: Optional[str] = "The given value isn't an integer, please try again.",
    out_range: Optional[str] = "The given value is out of range, please try again.",
) -> int:
    """Parse inputs
    This is essentially a 'builtins.input' function with fail-safe checks so that the program doesn't crash if the user
    say, inputs a non-decimal character when a decimal character is expected.
    Args:
        max_length: used for validation of stdin to see if it's within the range of 1 and said arg
        inp_text: input text for the stdin validation, defaults to >>
        not_int: text for when stdin input is not an integer
        out_range: text for when stdin input is out of range
    The inp_text, not_int and out_range arguments exist to simplify the usage of this function. They're here to allow
    for different languages to be used in place of default English responses.
    Returns:
        an integer as result from stdin input function
    """

    while True:
        while not (chosen := input(inp_text or colored(">> ", "red"))).isdecimal():  # type: ignore
            print(not_int)

        # Do not write as 'not chosen'.
        # I have no idea why mypy fails here
        chosen = int(chosen)  # type: ignore
        if 1 <= chosen <= max_length or chosen == 0:  # type: ignore
            break

        print(out_range)

    return int(chosen)


def parse_path(language: Language) -> str:
    """Parse path and check its validity
    This function uses 'os.access' to check the path for read and write permissions as well as ensure it's a directory
    by appending '/' or '\\' to the end of the path granted, if not present.
    """

    while not os.access(
        path := input(language.pathInput + colored(" >> ", "red")), os.W_OK
    ) and os.access(path, os.R_OK):
        print(language.badPath)

    if path[-1] not in ("/", "\\"):
        path += "\\"

    return path


def parse_songs(language: Language) -> list[tuple[str, str]]:
    """Parse songs
    Prompt the user for songs until they say "stop". This noun is not translated to native languages because it is
    commonly borrowed from English and used colloquinally. Searching for song is done using the 'extended.search_songs'
    function and then the song(s) are parsed using the 'extended.parse_input' function.
    """

    to_download = []

    while True:
        cls()
        print(language.whichSongDefault)

        query = input(language.enterSong + colored(" >> ", "red"))

        if query.lower() == "stop":
            break

        results = VideosSearch(query, limit=20).result()

        for c, i in enumerate(results["result"]):
            print(f"{colored(f'{c + 1}', 'green')}. | {i['duration']} {i['title']}")

        if not len(results["result"]):  # empty list case
            print(language.noSongsFound)
            time.sleep(2)
            continue

        parsed_input = results["result"][
            choice := parse_input(
                len(results["result"]),
                language.whichSong + colored(" >> ", "red"),
                language.badInt,
                language.outOfRange,
            )
            - 1
        ]

        if choice == -1:  # Means user chose 0 to search again
            continue

        to_download.append((parsed_input["link"], parsed_input["title"]))  # type: ignore

    return to_download


def parse_filename(fl: str) -> str:
    """Remove any characters with regex that may not be valid in a filename (i.e. allow only alphabetical chars)"""

    return PATH_REGEX.sub("", fl)