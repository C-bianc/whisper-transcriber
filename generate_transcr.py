#!/usr/bin/env python
# ~* coding: utf-8 *~
# ===============================================================================
#
#           FILE: generate_transcr.py
#         AUTHOR: Bianca Ciobanica
#          EMAIL: bianca.ciobanica@student.uclouvain.be
#
#           BUGS:
#        VERSION: 3.11.4
#        CREATED: 25-03-2024
#
# ===============================================================================
# DESCRIPTION: This program transcribes MP3 audio files into text using the
#               Whisper model. By default, it provides segmented transcriptions
#               without punctuation.
#               Options:
#                --with-punct: Retain punctuation in the transcription.
#                --continued-text: Combine the transcription into a continuous
#                                   block.
#                -dir: Process all MP3 files in a directory.
#              Output is saved as a .txt file with the same name as the audio file.
#               if -save parameter is given else it prints on the console
#
#   DEPENDENCIES: whisper
#
#          USAGE: python generate_transcr.py
# ===============================================================================
import os
import whisper
import re
import argparse
import functools

# ensure that whisper.torch.load always loads with weights_only=True
whisper.torch.load = functools.partial(whisper.torch.load, weights_only=True)
model = whisper.load_model("medium")


def get_segments(transcription, with_punct=False, continued_text=False):
    if continued_text:
        full_text = transcription["text"].strip()
        if not with_punct:
            full_text = re.sub(r"[^\w\s\-\']", "", full_text)
        return full_text.lower()
    else:
        text_segments = []
        for segment in transcription["segments"]:
            text = segment["text"].strip()
            if text:
                if not with_punct:
                    text = re.sub(r"[^\w\s\-\']", "", text)  # remove punctuation
                text = text.lower()
                text_segments.append(text)
        return "\n".join(text_segments)


def get_rl_path(filename):
    wd = os.getcwd()
    return os.path.join(wd, f"{os.path.splitext(filename)[0]}.txt")


def transcribe_single_file(input_file, with_punct=False, continued_text=False, saving=False):
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return

    # create txt file
    txt_file_path = get_rl_path(input_file)

    transcr = model.transcribe(input_file)

    # get segments with or without punctuation, as per options
    transcr_segments = get_segments(transcr, with_punct=with_punct, continued_text=continued_text)

    if saving:
        with open(txt_file_path, "w") as output_file:
            output_file.write(transcr_segments)

        print(f"Saved transcription for {input_file}.")

    else:
        print(transcr_segments)


def transcribe_directory(directory, with_punct=False, continued_text=False):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)

            transcr = model.transcribe(file_path)

            # get segments with or without punctuation, as per options
            transcr_segments = get_segments(transcr, with_punct=with_punct, continued_text=continued_text)

            # create txt file
            txt_file_path = get_rl_path(file_path)

            # write to txt
            with open(txt_file_path, "w") as output_file:
                output_file.write(transcr_segments)

            print(f"Saved transcription for {filename}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio files and save the transcriptions as text files.")
    parser.add_argument(
        "input",
        help="Path to the audio file or directory containing MP3 files to transcribe.",
    )
    parser.add_argument(
        "-dir",
        action="store_true",
        help="Flag to specify that the provided input is a directory.",
    )
    parser.add_argument(
        "-save", action="store_true", help="Flag to specify that the transcription should be saved into a .txt file"
    )
    parser.add_argument(
        "--with-punct",
        action="store_true",
        help="Keep punctuation in the transcription.",
    )
    parser.add_argument(
        "--continued-text",
        action="store_true",
        help="Provide transcription as a single continuous text instead of segmented.",
    )

    args = parser.parse_args()

    with_punct = args.with_punct
    continued_text = args.continued_text

    if args.dir:
        transcribe_directory(args.input, with_punct=with_punct, continued_text=continued_text)
    else:
        transcribe_single_file(args.input, with_punct=with_punct, continued_text=continued_text)
