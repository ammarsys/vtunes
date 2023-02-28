"""VTunes, a user-friendly CLI YouTube MP3 downloader"""

import subprocess
import os
import platform
import sys

from utils import load_json, parse_input, parse_path, cls, parse_songs, parse_filename

from terminalcolorpy import colored  # type: ignore

subprocess.call("", shell=True)
cls()

ffmeg_path = None
try:
    subprocess.check_output("ffmpeg --version")
except FileNotFoundError:
    if os.path.exists(r"utils\ffmpeg\ffmpeg.exe"):
        ffmeg_path = os.getcwd() + r"\utils\ffmpeg\ffmpeg.exe"

    elif platform.system() == "Windows":
        print(colored("[ERROR]", "red"), "FFMPEG not found. Install it and add to your system variables or simply run 'binariesInstall.ps1'.")
        input()
        quit()

    else:
        print(colored("[ERROR]", "red"), "FFMPEG not found. Install it and add to your system variables.")
        input()
        quit()


yt_dlp_path = None
try:
    subprocess.check_output("yt-dlp --version")
except FileNotFoundError:
    if os.path.exists(r"utils\yt-dlp\yt-dlp.exe"):
        yt_dlp_path = os.getcwd() + r"\utils\yt-dlp\yt-dlp.exe"

    elif platform.system() == "Windows":
        print(colored("[ERROR]", "red"), "YT-DLP not found. Install it and add to your system variables or simply run 'binariesInstall.ps1'.")
        input()
        quit()

    else:
        print(colored("[ERROR]", "red"), "YT-DLP not found. Install it and add to your system variables.")
        input()
        quit()

if not sys.version_info >= (3, 9):
    print(colored("[ERROR]", "red") + " Outdated Python version. Please install 3.9 or above.")
    input()
    quit()


translations = load_json()

print("Please select your language,")

for language in translations:
    print("{0.number}. | {0.localName} ({0.code})".format(language))

choice = parse_input(max_length=len(translations))

# Check in case user provides 0, so it doesn't end up being -1 (last element). Automatically pick English.
# zero indicating that they can't find their language so resort to English as the 'worldwide' language.
language = translations[choice - 1 if choice else choice]
path = parse_path(language)

cls()
songs = parse_songs(language)

for c, (link, title) in enumerate(songs):
    print(
        f'{c+1}/{len(songs)} {language.songDown} {colored(">>", "red")} "{title}"'
    )

    subprocess.run(
        f'{yt_dlp_path if yt_dlp_path else "yt-dlp"} --extract-audio --console-title --audio-format mp3 --quiet -o "{path}{parse_filename(title)}.mp3" {link}' + rf' --ffmpeg-location {ffmeg_path}' if ffmeg_path else ''
    )


cls()
input(language.endText)
