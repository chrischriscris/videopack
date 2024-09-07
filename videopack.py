#!/usr/bin/env python

from dataclasses import dataclass
import argparse
import os
import sys
import subprocess
from typing import List
import tempfile

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


def trim_silence(track_filename: str, output_filename="output.flac"):
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

    stream.output(output_filename).run()


def concat_music_files(files: List[str], output_filename: str = "output.flac"):
    """Takes a list of filenames and concats all music files into a single file"""
    inputs = [ffmpeg.input(f) for f in files]
    print(f"{files=}, {output_filename=}")
    print(ffmpeg.concat(*inputs, a=1, v=0).output(output_filename).compile())
    ffmpeg.concat(*inputs, a=1, v=0).output(output_filename).run()


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


def create_video(audio_file: str, image_file: str):
    """Creates a video out of an audio and an image file"""
    subprocess.run(
        [
            "ffmpeg",
            "-loop",
            "1",
            "-i",
            image_file,
            "-i",
            audio_file,
            "-shortest",
            "output.mp4",
        ]
    )


@dataclass
class SongData:
    path: str
    duration: float
    title: str


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

    songs: List[SongData] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for path in music_files:
            trimmed_path = f"{tmpdir}/{len(songs):03}.flac"
            trim_silence(path, trimmed_path)

            probe = ffmpeg.probe(trimmed_path)["format"]
            duration = float(probe["duration"])
            title = probe["tags", "title"]
            song = SongData(trimmed_path, duration, title)
            songs.append(song)

        with tempfile.NamedTemporaryFile(suffix=".flac") as tmpfile:
            concat_music_files([s.path for s in songs], tmpfile.name)
            create_video(tmpfile.name, f"{dir}/cover.jpg")

    print("Done!")


if __name__ == "__main__":
    main()
