#!/usr/bin/env python3
"""Original lo-fi beat + cut whooshes for the reel. Writes $OUT (length and cut points from timing.json in cwd)."""
import numpy as np, wave

import json, os
TM = json.load(open("timing.json")) if os.path.exists("timing.json") else {"total": 32.0, "cuts": [3.2, 6.8, 10.8, 14.0, 16.6, 21.2, 24.6, 26.8, 29.6], "flip": 9.0}
SR, DUR, BPM = 44100, TM["total"], 88
FL = TM["flip"]
n = int(SR * DUR)
t = np.arange(n) / SR
beat = 60 / BPM
out = np.zeros(n)
rng = np.random.default_rng(3)

def add(sig, start):
    i = int(start * SR)
    if i >= n: return
    j = min(n, i + len(sig))
    out[i:j] += sig[: j - i]

def kick():
    d = 0.35; tt = np.arange(int(SR * d)) / SR
    f = 110 * np.exp(-tt * 18) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.9

def snare():
    d = 0.25; tt = np.arange(int(SR * d)) / SR
    nz = rng.normal(0, 1, len(tt))
    nz = np.convolve(nz, np.ones(4) / 4, "same")
    return (nz * 0.35 + np.sin(2 * np.pi * 190 * tt) * 0.25) * np.exp(-tt * 18)

def hat():
    d = 0.06; tt = np.arange(int(SR * d)) / SR
    nz = rng.normal(0, 1, len(tt)); nz = nz - np.convolve(nz, np.ones(8) / 8, "same")
    return nz * np.exp(-tt * 70) * 0.12

def note_hz(m): return 440 * 2 ** ((m - 69) / 12)

def chord(ms, d):
    tt = np.arange(int(SR * d)) / SR
    s = np.zeros_like(tt)
    for m in ms:
        f = note_hz(m)
        s += np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 0.3)
    env = np.minimum(1, tt / 0.08) * np.exp(-tt * 0.6)
    # soft wobble
    return s * env * (1 + 0.02 * np.sin(2 * np.pi * 0.7 * tt)) * 0.07

# Fmaj7 - Em7 - Dm7 - Cmaj7 (lo-fi-ish)
prog = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
bar = beat * 4
k = 0
tpos = 0.0
while tpos < DUR:
    add(chord(prog[k % 4], bar + 0.5), tpos)
    add(np.sin(2 * np.pi * note_hz(prog[k % 4][0] - 12) * np.arange(int(SR * bar)) / SR)
        * np.exp(-np.arange(int(SR * bar)) / SR * 1.5) * 0.12, tpos)
    for b in range(4):
        bt = tpos + b * beat
        if b in (0, 2): add(kick(), bt)
        if b == 2 and k % 2 == 1: add(kick() * 0.6, bt + beat * 0.5)
        if b in (1, 3): add(snare(), bt + 0.015)
        for h in range(2):
            add(hat() * (1 if h == 0 else 0.6), bt + h * beat / 2 + (0.02 if h else 0))
    tpos += bar; k += 1

# vinyl crackle
crk = np.zeros(n); idx = rng.integers(0, n, 1400); crk[idx] = rng.normal(0, 0.15, len(idx))
out += np.convolve(crk, np.ones(3) / 3, "same") + rng.normal(0, 0.004, n)

# low-pass-ish smoothing for lo-fi warmth
out = np.convolve(out, np.ones(5) / 5, "same")

# duck + drop out one beat at "So I flipped it" (9.0s)
env = np.ones(n)
a, b = int((FL - 0.25) * SR), int((FL + 0.05) * SR)
env[a:b] = np.linspace(1, 0.05, b - a)
env[b:int((FL + 0.45) * SR)] = 0.05
c = int((FL + 0.45) * SR); env[c:c + int(0.15 * SR)] = np.linspace(0.05, 1, int(0.15 * SR))
out *= env

# whooshes on cuts
cuts = TM["cuts"]
for ct in cuts:
    d = 0.35; tt = np.arange(int(SR * d)) / SR
    nz = rng.normal(0, 1, len(tt))
    nz = np.convolve(nz, np.ones(12) / 12, "same")
    w = nz * np.sin(np.pi * tt / d) ** 2 * 0.35
    add(w, ct - 0.2)
# impact hit on flip
tt = np.arange(int(SR * 0.6)) / SR
add(np.sin(2 * np.pi * np.cumsum(70 * np.exp(-tt * 6) + 35) / SR) * np.exp(-tt * 5) * 0.9, FL)

# fade in/out, normalize
fi = int(0.3 * SR); out[:fi] *= np.linspace(0, 1, fi)
fo = int(1.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)
out = out / np.max(np.abs(out)) * 0.8
st = np.stack([out, np.roll(out, 90) * 0.97], 1)
with wave.open(os.environ.get("OUT", "music.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
