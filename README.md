# SRT Beautify

This project provides an automated solution for converting SRT subtitle files into ASS format with a specified style, and for merging them with MKV/MP4 video files. Processing can be done via a Python command-line script or a user-friendly graphical interface (GUI) based on Tkinter.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Command Line Script](#command-line-script)
   - [Options](#options)
   - [Graphical Interface](#graphical-interface)

## Features

- **SRT to ASS Conversion**: Converts SRT subtitle files into the ASS format with a predefined style.
- **Subtitle Merging**: Adds the modified ASS subtitle track to MKV/MP4 video files, removing existing subtitle tracks.
- **Multiple File Support**: Processes multiple video files simultaneously when using the graphical interface.
- **Automatic Subtitle Extraction**: For MKV files, automatically extracts existing subtitles before conversion and merging.

## Prerequisites

- Python 3.6 or higher
- FFmpeg installed and accessible from your system's PATH
- Python libraries: `tkinter` for the GUI, `subprocess` for executing system commands

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ImSakushi/srt-beautify.git
   cd srt-beautify
   ```

2. **Install FFmpeg**:
   - **Windows**: Download and install from [FFmpeg.org](https://ffmpeg.org/download.html), and add the `bin` folder to your PATH environment variable.
   - **Linux**: Run `sudo apt-get install ffmpeg` (for Debian-based distributions).
   - **macOS**: Install using Homebrew by running:
     ```bash
     brew install ffmpeg
     ```
     If you don't have Homebrew installed, first install it from [brew.sh](https://brew.sh/) then run the above command.

3. **Ensure Python is installed**:
   - Check with `python --version` or `python3 --version`.

## Usage

### Command Line Script

- To process a video with a specific SRT file:
  ```bash
  python srt_ass.py path/to/video.mkv -s path/to/subtitle.srt -l eng
  ```

- To process an MKV video by extracting the subtitles:
  ```bash
  python srt_ass.py path/to/video.mkv -l fra
  ```

- To batch process a whole folder of MKV video by extracting the subtitles:
  ```bash
  python srt_ass.py -b path/to/folder -l spa
  ```
### Options
```text
-l, --language                                   Destination language
-s, --subtitle                                   For using custom .srt file
-s, --subtitle                                   For using custom .srt file
-b, --batch                                      To use a whole folder instead of a single file
{fre, ang, spa, ger, ita, por, rus, jpn, kor, chi, ara}
```


### Graphical Interface

- Launch the graphical interface:
  ```bash
  python gui.py
  ```

- Follow the on-screen instructions to select videos and the SRT file, then click "Process Videos" to start processing.
