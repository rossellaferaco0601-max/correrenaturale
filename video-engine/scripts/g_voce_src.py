#!/usr/bin/env python3
"""Sola voce per un intero sorgente (Ross 24/11, serie G: «togli la musica da tutti i video»): la musica di sottofondo sta dentro
l'audio del video di partenza, quindi la si toglie una volta sola dal sorgente (voce = audio − musica isolata, cn_music_stem.py)
e i master costruiti dopo escono già senza musica. L'originale resta accanto come *_conmusica.mp4.
Uso: python3 scripts/g_voce_src.py public/ytcn26/ytcn26_src.mp4"""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cn_music_stem import stem

src = sys.argv[1]; orig = src.replace(".mp4", "_conmusica.mp4"); tmp = src.replace(".mp4", "_voce.wav")
if not os.path.exists(orig): os.rename(src, orig)
a = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", orig, "-vn", "-ac", "2", "-ar", "44100", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).T.copy()
voce = np.empty_like(a); B = 44100 * 60
for i in range(0, a.shape[1], B):
    lo, hi = max(0, i - 44100), min(a.shape[1], i + B + 44100)          # un secondo di margine per lato: niente giunte udibili
    m = stem(a[:, lo:hi]); voce[:, i:i + B] = (a[:, lo:hi] - m)[:, i - lo:i - lo + min(B, a.shape[1] - i)]
    print(f"{min(i + B, a.shape[1]) / 44100:.0f} s", flush=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", "48000", tmp], input=np.ascontiguousarray(voce.T).tobytes(), check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", orig, "-i", tmp, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", src], check=True)
db = lambda v: 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-9); w = 4410
ea = np.array([db(a.mean(0)[i:i + w]) for i in range(0, a.shape[1] - w, w)]); ev = np.array([db(voce.mean(0)[i:i + w]) for i in range(0, a.shape[1] - w, w)])
q = np.argsort(ea)[:int(len(ea) * 0.1)]
print(f"parlato {np.median(ea):.1f} → {np.median(ev):.1f} dB · pause {np.mean(ea[q]):.1f} → {np.mean(ev[q]):.1f} dB")
