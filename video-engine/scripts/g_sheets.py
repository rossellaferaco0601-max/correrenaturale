#!/usr/bin/env python3
"""Fogli di controllo della serie G (regole del 24/11):
  inquadrature  → un fotogramma a metà di OGNI inquadratura del master (il volto deve stare al centro, niente spalle o viso fuori dal bordo)
  finale        → tutti i fotogrammi dell'ultimo secondo e mezzo prima che la CTA copra tutto (niente parlato muto, niente stacco, niente fermo)
Uso: python3 scripts/g_sheets.py inquadrature public/ytcn26/masters/G2-strati.mp4 out/chk/x.jpg
     python3 scripts/g_sheets.py finale out/ytcn26/consegna/G2-strati_v3.mp4 out/chk/y.jpg [secondi di CTA=8]"""
import json, subprocess, sys, os, tempfile
mode, src, out = sys.argv[1:4]
tmp = tempfile.mkdtemp()
if mode == "inquadrature":
    pz = json.load(open(src.replace(".mp4", "_pezzi.json"))); n = len(pz)
    for i, p in enumerate(pz):
        t = (p["master"][0] + p["master"][1]) / 2
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"scale=216:384,drawtext=text='{p['master'][0]:.1f}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6", f"{tmp}/{i:03d}.jpg"], check=True)
    cols = min(n, 10); rows = (n + cols - 1) // cols
else:
    cta = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0
    D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    a = D - cta - 1.5
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-t", "1.9", "-i", src, "-vf", "fps=30,scale=162:288", f"{tmp}/%03d.jpg"], check=True)
    n = len(os.listdir(tmp)); cols = 19; rows = (n + cols - 1) // cols
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-pattern_type", "glob", "-i", f"{tmp}/*.jpg", "-vf", f"tile={cols}x{rows}", "-frames:v", "1", out], check=True)
print(out, n, "fotogrammi")
