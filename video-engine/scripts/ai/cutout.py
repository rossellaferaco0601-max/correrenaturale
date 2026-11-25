#!/usr/bin/env python3
"""Daniele ritagliato dallo sfondo (RobustVideoMatting, ONNX, gratuito: work/models/ai/rvm_mobilenetv3_fp32.onnx da github.com/PeterL1n).
Serve per le scritte DIETRO la persona: in Remotion si mette video → scritta → questo ritaglio sopra (stesso tempo del master).
Uso (venv della skill effects):  ../.claude/skills/effects/.venv/bin/python scripts/ai/cutout.py master.mp4 inizio_s durata_s uscita.mov
Esce una .mov ProRes 4444 con la persona su fondo trasparente, 1080x1920, 30 fps, lunga `durata_s`. CPU: ~0,3-0,5 s a fotogramma."""
import subprocess, sys, time
import numpy as np, onnxruntime as ort
src, ss, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
W, H = 1080, 1920
MODEL = __file__.replace("scripts/ai/cutout.py", "work/models/ai/rvm_mobilenetv3_fp32.onnx")
so = ort.SessionOptions(); so.log_severity_level = 3
sess = ort.InferenceSession(MODEL, so, providers=["CPUExecutionProvider"])
rd = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", src, "-vf", f"fps=30,scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le", "-qscale:v", "13", "-vendor", "apl0", out], stdin=subprocess.PIPE)
rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4; ds = np.array([0.25], np.float32); n = 0; t0 = time.time()
while True:
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    x = (img.astype(np.float32) / 255).transpose(2, 0, 1)[None]
    fgr, pha, *rec = sess.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ds})
    a = (np.clip(pha[0, 0], 0, 1) * 255).astype(np.uint8)
    wr.stdin.write(np.dstack([img, a]).tobytes()); n += 1
wr.stdin.close(); wr.wait()
print(f"{out}: {n} fotogrammi in {time.time() - t0:.0f} s ({(time.time() - t0) / max(1, n):.2f} s a fotogramma)")
