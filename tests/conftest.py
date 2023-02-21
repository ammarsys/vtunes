"""Configuration file with fixtures for the tests"""

import pytest

from utils import Language

ENGLISH_LANGUAGE_DICT = {
    "translations": {
        "pathInput": "Enter the PATH where the songs should be installed",
        "badPath": "The PATH wasn't found or the program doesn't have sufficient permission, please try again",
        "enterSong": "Enter a songs name to search",
        "whichSong": "Choose a song (enter 0 to search again)",
        "badInt": "The given value isn't an integer, please try again",
        "outOfRange": "The given value is out of range, please try again",
        "whichSongDefault": "Enter STOP to finish song selection, to choose a song enter their corresponding number,",
        "noSongsFound": "No songs for the given query were found, please try again",
        "songDown": "Downloading song",
        "endText": "All songs downloaded. If you liked the program give us a star on GitHub https://github.com/ammarsys/vtunes",
    },
    "localName": "English",
    "code": "EN",
    "number": 1,
}


@pytest.fixture
def english_language() -> Language:
    # I have no idea why mypy is complaining here.
    return Language(  # type: ignore
        ENGLISH_LANGUAGE_DICT["localName"],  # type: ignore
        ENGLISH_LANGUAGE_DICT["code"],  # type: ignore
        ENGLISH_LANGUAGE_DICT["number"],  # type: ignore
        **ENGLISH_LANGUAGE_DICT["translations"]
    )
