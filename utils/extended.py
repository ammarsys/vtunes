"""Module with support functions for the main CLI"""

import json
import os
import time
import subprocess
import re

from dataclasses import dataclass
from typing import Optional

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


def search_songs(query: str) -> list[list[str]]:
    """Search for songs using yt-dlp and chunk them into a 2d list

    Since yt-dlp returns results in format TITLE, DURATION, URL we need to chunk the results into a 2d list (a list
    containing more lists). The lists inside the said 2d list are as expected in format of TITLE, DURATION, URL.
    """

    out = subprocess.check_output(
        f'yt-dlp "ytsearch15:{query}" -O title -O duration_string -O url --flat-playlist',
        encoding="cp1252",
    ).split("\n")
    chunked = []

    for i in range(3, len(out) + 1, 3):
        chunked.append((out[i - 3 : i]))

    return chunked


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

        results = search_songs(query)

        for c, result in enumerate(results):
            print(f"{colored(f'{c + 1}', 'green')}. | {result[1]} {result[0]}")

        if not results:  # empty list case
            print(language.noSongsFound)
            time.sleep(2)
            continue

        parsed_input = (
            parse_input(
                len(results),
                language.whichSong + colored(" >> ", "red"),
                language.badInt,
                language.outOfRange,
            )
            - 1  # Remove 1 because indexing in Python starts from 0
        )

        if parsed_input == -1:
            continue

        to_download.append(
            (results[parsed_input][2], results[parsed_input][0])
        )  # first is url second is title

    return to_download


def parse_filename(fl: str) -> str:
    """Remove any characters with regex that may not be valid in a filename (i.e. allow only alphabetical chars)"""

    return PATH_REGEX.sub("", fl)
