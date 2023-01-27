"""VTunes, a user-friendly CLI YouTube MP3 downloader"""

import subprocess

from utils import load_json, parse_input, parse_path, cls, parse_songs, parse_filename

from terminalcolorpy import colored  # type: ignore

subprocess.call("", shell=True)
cls()

translations = load_json()

print("Please select your language,")

for language in translations:
    print("{0.number}. | {0.localName} ({0.code})".format(language))

language = translations[parse_input(max_length=len(translations)) - 1]
path = parse_path(language)
cls()
songs = parse_songs(language)

for c, (link, title) in enumerate(songs):
    print(f'{c}/{len(songs)} {language.songDown} {colored(">>", "red")} "{title}"')

    subprocess.run(
        f'yt-dlp --extract-audio --audio-format mp3 --quiet -o "{path}{parse_filename(title)}.mp3" {link}'
    )

input(language.endText)
