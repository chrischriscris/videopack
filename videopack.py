#!/usr/bin/env python

import argparse
import os
import sys
from typing import List
import tempfile
import time

import ffmpeg

MUSIC_FILE_EXTENSIONS = [".flac", ".mp3", ".m4a"]


def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="videopack",
        description="concatenates all video files in a directory and converts it into a full video",
    )

    parser.add_argument("dirname")
    parser.add_argument("-c", "--cover")
    parser.add_argument("-d", "--disable-cover", action="store_true")

    return parser.parse_args()


def trim_silence(track_filename: str):
    """Trims the silences out of the beginning and the end of the provided track"""
    stream = ffmpeg.input(track_filename)
    stream = ffmpeg.filter(
        stream,
        "silenceremove",
        start_periods=1,
        start_duration=1,
        start_threshold="-60dB",
        detection="peak",
    )
    stream = ffmpeg.filter(stream, "aformat", "dblp")
    stream = ffmpeg.filter(stream, "areverse")

    # Does the same to the reversed file
    stream = ffmpeg.filter(
        stream,
        "silenceremove",
        start_periods=1,
        start_duration=1,
        start_threshold="-60dB",
        detection="peak",
    )
    stream = ffmpeg.filter(stream, "aformat", "dblp")
    stream = ffmpeg.filter(stream, "areverse")

    stream.output("output.flac").run()


def concat_music_files(files: List[str]):
    """Takes a list of filenames and concats all music files into a single file"""
    inputs = [ffmpeg.input(f) for f in files]
    ffmpeg.concat(*inputs, a=1).output("output.flac").run()
    # with tempfile.NamedTemporaryFile() as tmp:
    #     for path in files:
    #         tmp.write(str.encode(f"file '{path}'\n"))
    #     tmp.seek(0)

    #     print(tmp.read())
    #     ffmpeg.input(tmp.name, format='concat', safe=0).output("output.flac", c='copy').run()




def listdir_absolute(directory: str) -> List[str]:
    dirs = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            dirs.append(os.path.abspath(os.path.join(dirpath, f)))

    return dirs


def is_music_file(filename: str) -> bool:
    for extension in MUSIC_FILE_EXTENSIONS:
        if filename.endswith(extension):
            return True

    return False


def main():
    args = get_args()
    dir = args.dirname
    if not os.path.isdir(dir):
        errprint("Error: The given path is not a directory")
        sys.exit(1)

    files = listdir_absolute(dir)
    if len(files) == 0:
        errprint("Error: The given path has no files")
        sys.exit(1)

    music_files = list(sorted(filter(is_music_file, files)))

    # TODO: Check if there are music files
    concat_music_files(music_files)


if __name__ == "__main__":
    main()
