import re
import sys
import subprocess
import os

def extract_subtitles(video_path, output_srt):
    try:
        # Commande FFmpeg pour extraire les sous-titres français, ou les premiers disponibles
        command = [
            'ffmpeg',
            '-i', video_path,
            '-map', '0:s:m:language:fre',
            '-c:s', 'srt',
            '-f', 'srt',
            output_srt
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Trying to extract any available subtitles.")
        command[4] = '0:s:0'  # Sélectionne la première piste de sous-titre disponible
        subprocess.run(command, check=True)

def srt_to_ass(srt_file_path, ass_file_path):
    header = """[Script Info]
Title: SRT converted to ASS
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
Timer: 0.0000
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Wakanim 1080p,Verdana,55.5,&H00FFFFFF,&H000000FF,&H00282828,&H00000000,-1,0,0,0,100.2,100,0,0,1,3.75,0,2,0,0,79,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def convert_time(srt_time):
        """ Convert SRT time format to ASS time format. """
        h, m, s, ms = map(int, re.split('[:,]', srt_time))
        return f"{h:01}:{m:02}:{s:02}.{int(ms/10):02}"

    def convert_tags(text):
        """ Convert HTML tags in SRT to ASS tags. """
        text = text.replace('<i>', '{\\i1}')
        text = text.replace('</i>', '{\\i0}')
        return text

    with open(srt_file_path, 'r', encoding='utf-8') as srt, open(ass_file_path, 'w', encoding='utf-8') as ass:
        ass.write(header)
        entry = []
        text = []
        for line in srt:
            if '-->' in line:
                start, end = line.split('-->')
                start = convert_time(start.strip())
                end = convert_time(end.strip())
                entry = [start, end]
            elif line.strip().isdigit():
                continue
            elif line.strip() == '':
                if entry:
                    dialogue_text = '\\N'.join(text)
                    dialogue_text = convert_tags(dialogue_text)
                    ass.write(f"Dialogue: 0,{entry[0]},{entry[1]},Wakanim 1080p,,0,0,0,,{dialogue_text}\n")
                    entry = []
                    text = []
            else:
                text.append(line.strip())

def remove_existing_subtitles(video_path, interim_output_path):
    try:
        command = [
            'ffmpeg',
            '-i', video_path,
            '-map', '0:v',
            '-map', '0:a?',
            '-c:v', 'copy',
            '-c:a', 'copy',
            interim_output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to remove existing subtitles:", e)

def add_new_subtitle(interim_output_path, subtitle_path, final_output_path):
    try:
        command = [
            'ffmpeg',
            '-i', interim_output_path,
            '-i', subtitle_path,
            '-map', '0',
            '-map', '1:0',
            '-c', 'copy',
            final_output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to add new subtitle:", e)

def clean_up_files(*files_to_remove):
    for file_path in files_to_remove:
        os.remove(file_path)
        print(f"Removed temporary file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py video_file.mkv [subtitle_file.srt]")
        sys.exit(1)

    input_video = sys.argv[1]
    file_extension = os.path.splitext(input_video)[1].lower()
    file_root = os.path.splitext(input_video)[0]
    output_video = f"{file_root}_fixed.mkv"
    output_ass = "temp_output.ass"
    interim_video = "no_subtitles.mkv"

    if len(sys.argv) == 3:
        input_srt = sys.argv[2]
        srt_to_ass(input_srt, output_ass)
    elif file_extension == ".mkv":
        extracted_srt = "extracted.srt"
        extract_subtitles(input_video, extracted_srt)
        srt_to_ass(extracted_srt, output_ass)
        clean_up_files(extracted_srt)
    else:
        print("SRT file required for MP4 input or non-MKV files.")
        sys.exit(1)

    remove_existing_subtitles(input_video, interim_video)
    add_new_subtitle(interim_video, output_ass, output_video)
    clean_up_files(output_ass, interim_video)

    print(f"Final output video saved as: {output_video}")
