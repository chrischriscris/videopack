# videopack

Packs a directory of songs and a cover into a full video, spitting out the timestamps in the process.

Made to facilitate the upload of full albums into YouTube.

## Commands used

- To trim the silence out of the tracks:

```bash
ffmpeg -i input.mp3 -af "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse" output.flac
```

- To concatenate the tracks:
```bash
ffmpeg -i input1.flac -i input2.flac -filter_complex [0][1]concat=a=1:n=2:v=0[s0] -map [s0] output.flac
```

- To create a video with a given cover image:

```bash
```
