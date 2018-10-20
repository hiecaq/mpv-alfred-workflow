mpv-alfred-workflow
====================

Control mpv through alfred.

Installation
--------------------

You need brew-installed python3 to run this workflow. Otherwise, you have to set up the python3 path manually in the scripts.

Usage
--------------------

mpv has to be started with `--input-ipc-server` flag:

```bash
mpv --input-ipc-server=/tmp/mpvsocket
```

the socket address is default to `/tmp/mpvsocket`.

This workflow would be useful if you use mpv as a music player because you don't like any music player on Mac OS, via some command like this:

```bash
mpv --playlist <(find ~/Music | ag -v "instrumental|Drama|off vocal|オリジナルドラマ" | ag "\.(mp3|flac)$") --shuffle --loop-playlist=yes --no-audio-display --volume=30 --input-ipc-server=/tmp/mpvsocket
```
