#!/usr/bin/env python3
"""Fasce del reel G13 («4 esercizi», schermo a fasce orizzontali): ritaglia dal sorgente di YTCN 26 le quattro fasce 1080x368, mute,
lunghe 30 secondi (900 fotogrammi), montando per ogni esercizio le inquadrature dell'originale che stanno in una fascia orizzontale.
Ogni pezzo: (inizio nel sorgente, fotogrammi a 30 fps, y del ritaglio 1920x654). Il jumping jack ha solo 14 s di girato: la sequenza
passa due volte; nella sua ripresa stretta a mano (374,75-385,7) la camera scende sulle gambe e risale, quindi il ritaglio la segue.
Uso: python3 scripts/g13_bands.py     → public/ytcn26/quad/b1.mp4 … b4.mp4"""
import subprocess

SRC, OUT = "public/ytcn26/ytcn26_src.mp4", "public/ytcn26/quad"
W, H, CH = 1080, 368, 654
# ritaglio che segue la camera nella ripresa stretta del jumping jack (t = secondi dall'inizio del pezzo)
JJ_Y = "if(lt(t,1.5),20+310*t/1.5,if(lt(t,3.85),330,if(lt(t,6.1),330-220*(t-3.85)/2.25,110)))"
BANDS = {
    "b1": [(246.5, 397, 420), (259.85, 238, 250), (267.9, 102, 420), (240.45, 163, 200)],              # mountain climber
    "b2": [(276.0, 603, 420), (296.2, 204, 260), (311.6, 93, 420)],                                   # ponte per i glutei
    "b3": [(352.62, 186, 400), (329.0, 141, 400), (334.6, 360, 360), (366.3, 81, 400), (359.0, 132, 360)],   # affondi
    "b4": [(371.5, 96, 70), (374.78, 327, JJ_Y), (371.5, 96, 70), (374.78, 327, JJ_Y), (371.5, 54, 70)],   # jumping jack (due passaggi)
}
for name, pieces in BANDS.items():
    cmd, fc = ["ffmpeg", "-loglevel", "error", "-y"], ""
    for i, (ss, n, y) in enumerate(pieces):
        cmd += ["-ss", f"{ss:.3f}", "-t", f"{n / 30 + 0.4:.3f}", "-i", SRC]
        yy = f"'{y}'" if isinstance(y, str) else y
        fc += f"[{i}:v]crop=1920:{CH}:0:{yy},scale={W}:{H}:flags=lanczos,fps=30,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}];"
    fc += "".join(f"[v{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=1[v]"
    cmd += ["-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30", f"{OUT}/{name}.mp4"]
    subprocess.run(cmd, check=True)
    n = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", f"{OUT}/{name}.mp4"], capture_output=True, text=True).stdout.strip()
    print(name, n, "fotogrammi", "(attesi", sum(p[1] for p in pieces), ")")
