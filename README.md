# SRT Beautify

This project provides an automated solution for converting SRT subtitle files into ASS format with a specified style, and for merging them with MKV/MP4 video files. Processing can be done via a Python command-line script or a user-friendly graphical interface (GUI) based on Tkinter.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Command Line Script](#command-line-script)
   - [Graphical Interface](#graphical-interface)

## Features {#features}

- **SRT to ASS Conversion**: Converts SRT subtitle files into the ASS format with a predefined style.
- **Subtitle Merging**: Adds the modified ASS subtitle track to MKV/MP4 video files, removing existing subtitle tracks.
- **Multiple File Support**: Processes multiple video files simultaneously when using the graphical interface.
- **Automatic Subtitle Extraction**: For MKV files, automatically extracts existing subtitles before conversion and merging.

## Prerequisites {#prerequisites}

- Python 3.6 or higher
- FFmpeg installed and accessible from your system's PATH
- Python libraries: `tkinter` for the GUI, `subprocess` for executing system commands

## Installation {#installation}

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ImSakushi/srt_beautify.git
   cd srt_beautify
   ```

2. **Install FFmpeg**:
   - **Windows**: Download and install from [FFmpeg.org](https://ffmpeg.org/download.html), and add the `bin` folder to your PATH environment variable.
   - **Linux**: Run `sudo apt-get install ffmpeg` (for Debian-based distributions).

3. **Ensure Python is installed**:
   - Check with `python --version` or `python3 --version`.

## Usage {#usage}

### Command Line Script {#command-line-script}

- To process a video with a specific SRT file:
  ```bash
  python srtass.py path/to/video.mkv path/to/subtitle.srt
  ```

- To process an MKV video by extracting the subtitles:
  ```bash
  python srtass.py path/to/video.mkv
  ```

### Graphical Interface {#graphical-interface}

- Launch the graphical interface:
  ```bash
  python gui.py
  ```

- Follow the on-screen instructions to select videos and the SRT file, then click "Process Videos" to start processing.
```

With these modifications, users can now easily navigate your README by clicking on the sections listed in the table of contents. Each link will take them directly to the corresponding section in the document.
