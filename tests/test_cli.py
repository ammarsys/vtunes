"""CLI test functions"""

import io
import os
import sys

from utils import (
    parse_path,
    Language,
    parse_filename,
    load_json,
    parse_input,
    parse_songs,
)


class _TestStdin:
    """Programically replace the stdin

    This class implements a 'readline' function just like the 'sys.stdin' does. However, with this class you can specify
    the values you want to be fed into the said function. In other words, you are programically feeding input into
    'builtins.input', no user interaction required. Useful for testing.

    Sadly, a drawback to this method is that mypy will not shut up about it, so you must use 'type: ignore' everywhere.
    """

    def __init__(self, test_values: list[str]) -> None:
        self.old_stdin = sys.stdin

        self.test_cases = iter([io.StringIO(value) for value in test_values])

    def readline(self):
        try:
            return next(self.test_cases).readline()
        except StopIteration:
            # Clean up
            self.readline = self.old_stdin.readline

            return self.readline()


def test_parse_path(english_language: Language) -> None:
    sys.stdin = _TestStdin(["./"])  # type: ignore

    assert parse_path(english_language) == "./"


def test_parse_filename() -> None:
    assert parse_filename("Despacito [VIDEO] !!!!") == "Despacito VIDEO "


def test_load_json() -> None:
    """Change the current working directory to the root directory because 'load_json' uses relative paths"""
    old = os.getcwd()
    os.chdir("..")

    assert isinstance(load_json(), list)

    os.chdir(old)


def test_parse_input() -> None:
    sys.stdin = _TestStdin(["not an integer", "99", "2"])  # type: ignore

    assert parse_input(3) == 2


def test_parse_songs(english_language) -> None:
    sys.stdin = _TestStdin(  # type: ignore
        [
            "despacito",
            "22",
            "not an integer",
            "-1",
            "0",
            "despacito",
            "1",
            "not stop",
            "0",
            "stop",
        ]
    )  # type: ignore

    assert isinstance(parse_songs(english_language), list)
