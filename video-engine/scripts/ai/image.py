#!/usr/bin/env python3
"""Immagini generate QUI, gratis (SD-Turbo di Stability AI, sul processore, modello scaricato da Hugging Face in ~/.cache/huggingface).
Buone per materiali e atmosfere (ghiaccio, brina, nebbia, fiato, texture, sfondi, oggetti); NON per persone realistiche né per Daniele.
Uso: work/venv_img/bin/python scripts/ai/image.py "descrizione in inglese" uscita.png [larghezza altezza] [seme]
(512x512 ~20-40 s a immagine su questa macchina; lati multipli di 64)."""
import sys, time, torch
from diffusers import AutoPipelineForText2Image
prompt, out = sys.argv[1], sys.argv[2]
W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (512, 512)
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 7
torch.set_num_threads(4)
t = time.time()
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32)
img = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0, width=W, height=H, generator=torch.Generator().manual_seed(seed)).images[0]
img.save(out); print(out, f"{W}x{H}", f"{time.time() - t:.0f} s")
