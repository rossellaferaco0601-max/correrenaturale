#!/usr/bin/env python3
"""Mappa di profondità di un fotogramma (Depth Anything V2 small, ONNX, gratuito: work/models/ai/depth_anything_v2_small.onnx da Hugging Face).
Serve per l'effetto 3D sulle riprese (parallasse: Daniele e lo sfondo si muovono a velocità diverse, la camera «entra» nella scena) e per
sfocare solo lo sfondo. Uscita: PNG in scala di grigi a 16 bit, bianco = vicino, stessa grandezza del fotogramma.
Uso: ../.claude/skills/effects/.venv/bin/python scripts/ai/depth.py video.mp4 secondo uscita.png   (oppure un'immagine al posto del video)"""
import subprocess, sys
import numpy as np, onnxruntime as ort, cv2
src, out = sys.argv[1], sys.argv[-1]
if src.lower().endswith((".png", ".jpg", ".jpeg")): img = cv2.cvtColor(cv2.imread(src), cv2.COLOR_BGR2RGB)
else:
    t = float(sys.argv[2]); raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    img = cv2.cvtColor(cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
H, W = img.shape[:2]; S = 518
sess = ort.InferenceSession(__file__.replace("scripts/ai/depth.py", "work/models/ai/depth_anything_v2_small.onnx"), providers=["CPUExecutionProvider"])
h, w = (S, int(round(S * W / H / 14)) * 14) if H > W else (int(round(S * H / W / 14)) * 14, S)
x = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).astype(np.float32).transpose(2, 0, 1)[None]
d = sess.run(None, {sess.get_inputs()[0].name: x})[0][0]
d = cv2.resize(d, (W, H), interpolation=cv2.INTER_CUBIC); d = (d - d.min()) / (d.max() - d.min() + 1e-6)
cv2.imwrite(out, (d * 65535).astype(np.uint16)); print(out, f"{W}x{H}")
