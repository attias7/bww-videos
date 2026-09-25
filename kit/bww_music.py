"""Original ambient piano/pad music generator for Black & White Wisdom reels. make(path, seconds, chords, bpm, arp, kick_from)."""
import numpy as np, wave, sys
SR = 44100
rng = np.random.default_rng(7)

def note(n):  # midi -> hz
    return 440 * 2 ** ((n - 69) / 12)

def env(length, a, r):
    t = np.arange(length) / SR
    e = np.minimum(1, t / a) * np.minimum(1, (length / SR - t) / r)
    return np.clip(e, 0, 1)

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for f in freqs:
        for d in (-0.15, 0.0, 0.15):
            ff = f * 2 ** (d / 12 / 4)
            out += np.sin(2*np.pi*ff*t) + 0.3*np.sin(4*np.pi*ff*t) + 0.12*np.sin(6*np.pi*ff*t)
    return out * env(n, 0.8, 0.9) / (len(freqs) * 3)

def pluck(f, dur=2.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2*np.pi*f*t) + 0.4*np.sin(4*np.pi*f*t)*np.exp(-t*3) + 0.15*np.sin(6*np.pi*f*t)*np.exp(-t*6)
    return s * np.exp(-t * 2.2) * np.minimum(1, t / 0.004)

def kick(dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 45 + 70 * np.exp(-t * 25)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t * 7)

def reverb(x, secs=2.5, mix=0.35):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t * 3.0)
    ir[0] = 0
    L = len(x) + n
    N = 1 << (L - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return (1 - mix) * x / (np.max(np.abs(x)) + 1e-9) + mix * wet

def make(path, total, chords, bpm, arp_pattern, riser=True, kick_from=2.2):
    n = int(total * SR); mix = np.zeros(n + SR * 6)
    beat = 60 / bpm
    cd = beat * 4  # one bar per chord
    t0 = 0.0; i = 0
    while t0 < total:
        ch = chords[i % len(chords)]
        p = pad([note(m) for m in ch], cd + 0.9)
        s = int(t0 * SR); mix[s:s+len(p)] += 0.55 * p
        # bass
        bn = int((cd + 0.5) * SR); bt = np.arange(bn) / SR
        b = np.sin(2*np.pi*note(ch[0]-12)*bt) * env(bn, 0.05, 0.6)
        mix[s:s+bn] += 0.35 * b
        # arpeggio
        for k, idx in enumerate(arp_pattern):
            ts = t0 + k * beat / 2
            if ts >= total: break
            m = ch[idx % len(ch)] + 12 * (idx // len(ch)) + 12
            pl = pluck(note(m)); ss = int(ts * SR)
            mix[ss:ss+len(pl)] += 0.22 * pl
        t0 += cd; i += 1
    # heartbeat kick
    tk = kick_from
    while tk < total - 0.5:
        k = kick(); s = int(tk * SR); mix[s:s+len(k)] += 0.6 * k
        tk += beat
    if riser:
        rn = int(kick_from * SR); rt = np.arange(rn) / SR
        nz = rng.standard_normal(rn)
        nz = np.convolve(nz, np.ones(8)/8, 'same')
        mix[:rn] += 0.10 * nz * (rt / kick_from) ** 2
    mix = reverb(mix[:n + SR], 2.8, 0.4)[:n]
    fade = int(1.2 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
    mix[:int(0.05*SR)] *= np.linspace(0, 1, int(0.05*SR))
    mix = np.tanh(mix / np.max(np.abs(mix)) * 1.3) * 0.85
    st = np.stack([mix, np.roll(mix, 300)], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

