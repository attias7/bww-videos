#!/usr/bin/env python3
"""Make the first frames of a video the finished hook card, so TikTok / Instagram use it as the default cover.

Usage: python3 add_cover.py video.mp4 <cover_at_seconds> [hold_seconds=0.2]
Grabs the frame at cover_at (hook fully on screen) and shows it for the first hold_seconds, in place of the
dark/empty opening frames. Length and audio sync stay exactly the same. Rewrites the file in place.
"""
import os, subprocess, sys, tempfile

def add_cover(path, cover_at, hold=0.2):
    tmp = tempfile.mkdtemp(); png = os.path.join(tmp, "cover.png"); out = os.path.join(tmp, "out.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{cover_at:.2f}", "-i", path, "-frames:v", "1", png], check=True)
    br = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate",
                         "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    vb = f"{int(br) // 1000}k" if br.isdigit() else "4M"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-loop", "1", "-i", png, "-filter_complex",
                    f"[1:v][0:v]scale2ref[c][v];[v][c]overlay=enable='lt(t,{hold})':shortest=1[o]",
                    "-map", "[o]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-b:v", vb,
                    "-maxrate", vb, "-bufsize", vb, "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out],
                   check=True)
    os.replace(out, path)

if __name__ == "__main__":
    add_cover(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 0.2)
    print("cover set", sys.argv[1])
