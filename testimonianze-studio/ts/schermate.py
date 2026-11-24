"""Schermate originali dei messaggi: ricerca di nomi, numeri e volti da coprire, e copertura «bruciata» nell'immagine.
La copertura si fa sui pixel PRIMA di usare l'immagine: nel PPTX non resta nessun livello da togliere.
La ricerca usa Claude Code con la sola lettura dell'immagine (abbonamento, nessuna chiave API). Va sempre ricontrollata a occhio."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from .scrittura import estrai_json

DOMANDA = """Leggi l'immagine «{nome}» in questa cartella con lo strumento Read e guardala.
È l'allegato di una testimonianza: di solito lo screenshot di un messaggio (WhatsApp, Instagram, email, recensione).
Devo pubblicarla coprendo ogni dato che identifica una persona. Elenca TUTTE le zone da coprire:
- nomi e cognomi di persone (intestazione della chat, firma, nomi citati nel testo, nome dell'autore di un commento);
- numeri di telefono, email, nomi utente (@...), indirizzi, numeri di pettorale;
- foto profilo e volti.
NON coprire il testo del messaggio, gli orari, le date, i tempi di gara e le distanze.
Rispondi con un solo oggetto JSON, senza altro testo:
{{"tipo": "messaggio" | "foto" | "altro", "volti": true/false, "leggibile": true/false,
  "zone": [{{"cosa": "nome|telefono|email|utente|foto profilo|volto|altro", "x0": 0.0, "y0": 0.0, "x1": 0.0, "y1": 0.0}}]}}
Le coordinate sono frazioni della larghezza (x) e dell'altezza (y) dell'immagine, da 0 a 1, con l'origine in alto a sinistra.
Fai i rettangoli un po' abbondanti. «leggibile» è false se il testo del messaggio è troppo piccolo o sfocato per essere letto."""


def trova_zone(immagine: Path, config: dict) -> dict:
    cc = config["claude"]
    exe = shutil.which(cc.get("comando") or "claude")
    if not exe:
        raise FileNotFoundError("Comando «claude» non trovato.")
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    cmd = [exe, "-p", "--output-format", "json", "--max-turns", "4", "--strict-mcp-config", "--tools", "Read", "--allowedTools", "Read"]
    if cc.get("modello"):
        cmd += ["--model", cc["modello"]]
    r = subprocess.run(cmd, input=DOMANDA.format(nome=immagine.name), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=cc.get("attesa_secondi", 600), cwd=str(immagine.parent), env=env)
    busta = json.loads(r.stdout)
    if isinstance(busta, list):
        busta = next((b for b in reversed(busta) if isinstance(b, dict) and b.get("type") == "result"), {})
    if busta.get("is_error") or "result" not in busta:
        raise RuntimeError(f"Analisi dell'immagine non riuscita: {str(busta.get('result'))[:300]}")
    return estrai_json(busta["result"])


def copri(immagine: Path, uscita: Path, zone: list[dict], margine=.012, colore="#000000") -> Path:
    """Disegna un rettangolo pieno su ogni zona e salva una NUOVA immagine (l'originale non si tocca)."""
    im = Image.open(immagine).convert("RGB")
    d = ImageDraw.Draw(im)
    W, H = im.size
    for z in zone:
        x0, x1 = sorted((float(z["x0"]), float(z["x1"])))
        y0, y1 = sorted((float(z["y0"]), float(z["y1"])))
        box = (max(0, (x0 - margine) * W), max(0, (y0 - margine) * H), min(W, (x1 + margine) * W), min(H, (y1 + margine) * H))
        d.rounded_rectangle(box, radius=max(4, int(min(box[2] - box[0], box[3] - box[1]) * .25)), fill=colore)
    uscita.parent.mkdir(parents=True, exist_ok=True)
    im.save(uscita)
    return uscita
