import re
import sys
import argparse
import subprocess
import os

def extract_subtitle(video_path, output_srt, language_code):
    try:
        # Use ffprobe to find the first subtitle stream of the specified language
        probe_command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 's',
            '-show_entries', 'stream=index:stream_tags=language',
            '-of', 'csv=p=0'
        ]
        probe_result = subprocess.run(probe_command + [video_path], text=True, capture_output=True, check=True)
        # Parse the output to find the first stream with the desired language
        first_stream_index = None
        for line in probe_result.stdout.splitlines():
            index, lang = line.split(',')  # Assuming the format is "index,language"
            if lang.strip() == language_code:
                first_stream_index = int(index)  # Convert index to an integer
                final_language = first_stream_index - 2
                break


        if first_stream_index is not None:
            # Extract only the first matching subtitle stream
            extract_command = [
                'ffmpeg',
                '-i', video_path,
                '-map', f'0:s:{final_language}',
                '-c:s', 'srt',
                '-f', 'srt',
                output_srt
            ]
            subprocess.run(extract_command, check=True)
            print(f"Extracted subtitles from stream index {first_stream_index} with language {language_code}.")
        else:
            print("No matching subtitle streams found for the specified language.")
    except subprocess.CalledProcessError as e:
        print("Failed to extract subtitles:", str(e))



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

def add_new_subtitle(interim_output_path, subtitle_path, final_output_path, language_code):
    try:
        command = [
            'ffmpeg',
            '-i', interim_output_path,
            '-i', subtitle_path,
            '-map', '0',
            '-map', '1:0',
            '-c', 'copy',
            '-metadata:s:s:0', f'language={language_code}',
            final_output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to add new subtitle:", e)

def clean_up_files(*files_to_remove):
    for file_path in files_to_remove:
        os.remove(file_path)
        print(f"Removed temporary file: {file_path}")

def process_video(input_video, input_srt, language_code, file_root):
    output_video = f"{file_root}_fixed.mkv"
    output_ass = "temp_output.ass"
    interim_video = "no_subtitles.mkv"

    if input_srt:
        srt_to_ass(input_srt, output_ass)
    else:
        extracted_srt = "extracted.srt"
        extract_subtitle(input_video, extracted_srt, language_code)
        srt_to_ass(extracted_srt, output_ass)
        clean_up_files(extracted_srt)

    remove_existing_subtitles(input_video, interim_video)
    add_new_subtitle(interim_video, output_ass, output_video, language_code)
    clean_up_files(output_ass, interim_video)

    print(f"Processed {input_video}, final output saved as: {output_video}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process video and subtitle files.")
    parser.add_argument("input", help="Input video file or directory for batch processing.")
    parser.add_argument("-s", "--subtitle", help="Input subtitle file (SRT).", default="")
    parser.add_argument("-l", "--language", help="Subtitle language code (default 'fre').", default="fre")
    parser.add_argument("-b", "--batch", action="store_true", help="Batch process all MKV files in the specified directory")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    if args.batch:
        if not os.path.isdir(args.input):
            print("Specified input is not a directory. Please provide a directory when using the --batch option.")
            sys.exit(1)
        for filename in os.listdir(args.input):
            if filename.lower().endswith(".mkv"):
                input_video = os.path.join(args.input, filename)
                file_root = os.path.splitext(input_video)[0]
                process_video(input_video, args.subtitle, args.language, file_root)
    else:
        if not os.path.isfile(args.input):
            print("Specified input is not a file. Please provide a valid video file.")
            sys.exit(1)
        input_video = args.input
        file_extension = os.path.splitext(input_video)[1].lower()
        file_root = os.path.splitext(input_video)[0]
        if file_extension != ".mkv":
            print("Only MKV files are supported without batch processing.")
            sys.exit(1)
        process_video(input_video, args.subtitle, args.language, file_root)
