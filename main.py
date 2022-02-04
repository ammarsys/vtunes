from youtubesearchpython import VideosSearch
import subprocess
import threading

subprocess.call("", shell=True)
subprocess.call("cls", shell=True)

videos_to_download = []
path_to_download = (
    input(
        "\u001b[36m[CONFIG]\033[0m Upisi PATH gdje ce pjesme biti instalirane, ENTER za default (G:/) >> "
    )
    or "G:/"
)

text_default = lambda: print(
    "\033[95m[INFO]\033[0m Upisi STOP za prestanak, za odabir pjesma njihov redni broj"
)
clear = lambda: subprocess.call("cls", shell=True) or None

text_default()

while True:
    prompt = input("\u001b[34m[PROMPT]\033[0m Ukucaj ime pjesme >> ").strip()

    if prompt.lower() == "stop":
        clear()
        break

    results = VideosSearch(prompt, limit=15).result()
    
    for c, i in enumerate(results["result"]):
        print(f"\033[92m[{c+1}. | VIDEO]\033[0m {i['duration']} {i['title']}")

    result_value = results["result"][
        int(input("\u001b[34m[PROMPT]\033[0m Koja pjesma? >> ")) - 1
    ]
    videos_to_download.append((result_value["link"], result_value["title"]))

    clear()
    text_default()

for c, (link, title) in enumerate(videos_to_download):
    print(
        f'\033[95m[INFO {c}/{len(videos_to_download)}]\033[0m Skidanje "{title}" ...',
        end="\r",
    )

    subprocess.run(
        f'yt-dlp --extract-audio --audio-format mp3 --quiet -o "{path_to_download}{title}.mp3" {link}'
    )

    print("\033[95m[INFO]\033[0m Skinuta pjesma!" + " " * 100, end="\r")
    
input()
