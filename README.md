# videopack

Packs a directory of songs and a cover into a full video, spitting out the timestamps in the process.

Made to facilitate the upload of full albums into YouTube.

## Command used

- To trim the silence out of the tracks:

```bash
ffmpeg -i input.mp3 -af "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse" output.flac
```

- To concatenate the tracks:
```bash
```

- To create a video with a given cover image:

```bash
```
