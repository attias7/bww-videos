#!/bin/bash
# Usage: bww_captions.sh input.mp4 outprefix
# Makes a 1-fps overview sheet and timestamped caption-band strips (every 0.5 s) to read the script + timing.
# Captions are assumed ~67% down the frame; if the sheet shows them elsewhere (e.g. at the top), re-run the strip
# command by hand with a different crop y (top captions in 720x1280 are around y=265, h=90).
IN="$1"; OUT="$2"
H=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$IN")
W=$(ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 "$IN")
Y=$(python3 -c "print(int($H*0.672))"); CH=$(python3 -c "print(int($H*0.075))")
ffmpeg -v error -y -i "$IN" -vf "fps=2,crop=$W:$CH:0:$Y,scale=540:-1,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{pts\:hms}':x=2:y=2:fontsize=14:fontcolor=yellow,tile=2x32" "${OUT}%d.jpg"
ffmpeg -v error -y -i "$IN" -vf "fps=1,scale=200:-1,tile=10x8" -frames:v 1 "${OUT}_sheet.jpg"
ls "${OUT}"*
