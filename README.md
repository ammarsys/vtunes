<div align="center">
<h1>vtunes</h1>
<h6><i>CLI YouTube MP3 downloader</i></h6>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Alt Text](https://s4.gifyu.com/images/v2adc85054de801bf8.gif)
</div>
<hr>

# Overview

This is a minimalistic CLI tool to download songs from YouTube. I built this to be used for car songs, hence the name
`vtunes` - vehicle tunes. The module includes translations for several languages.

# Installation & Usage

> The required Python version is 3.9+

### Windows

You can run the `binariesInstall.ps1` by right-clicking it and selecting **Run with powershell** if you want to download
ffmpeg and yt-dlp automatically.

```
git clone https://github.com/novusys/vtunes
cd vtunes
py -m pip install -r requirements.txt
vtunes
```

### Linux

I have not fully tested this CLI on linux. [Open an issue](https://github.com/ammarsys/vtunes/issues) if you encounter problems.
```
sudo apt update && sudo apt upgrade
git clone https://github.com/novusys/vtunes
cd vtunes
python -m pip install -r requirements.txt
sudo apt install ffmpeg
sudo apt install yt-dlp
python vtunes.py
```

and voilla! That's it, follow the messages in terminal for help with usage.

# Contributing

Contributions are welcomed and encouraged. Feel free to add your own language in `languages.json`.
For code contributions, please ensure the following:

- Good programming practices
- Black formatting
- Typed code
- Tests added to `tests/`
- New tests (if aplicable)

As far as current issues go, the codebase can use some cleanup, entire test coverage & Linux testers.