#!/usr/bin/env python

import argparse
import os
import sys
from typing import List

import ffmpeg


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
    in_file = ffmpeg.input(track_filename)


def concat_music_files(files: List[str]):
    """Takes a list of filenames and concats all music files into a single file"""
    ffmpeg.concat()
    pass

def main():
    args = get_args()
    dir = args.dirname
    if not os.path.isdir(dir):
        errprint("Error: The given path is not a directory")
        sys.exit(1)

    files = os.listdir(dir)
    if len(files) == 0:
        errprint("Error: The given path has no files")
        sys.exit(1)


if __name__ == "__main__":
    main()
