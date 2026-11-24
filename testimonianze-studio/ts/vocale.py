"""Slide «Vocale»: un MP4 con l'audio ORIGINALE dell'allievo, l'onda che avanza e le parole che compaiono.
In un carosello Instagram una slide può essere un video: è l'unico modo per avere un audio che si sente.
Servono ffmpeg nel PATH e, per le parole a tempo, faster-whisper (facoltativo: senza, esce solo l'onda)."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from .grafica import AZZURRO, BIANCO, CREMA, NERO, VERDE, Tela, a_png, font, mescola
from .modelli import CH, CW, M, S_ALTO, S_BASSO, SH, SW, _piede_c, _piede_s

FPS = 30
DURATA_MAX = 60.0   # limite di una slide video nei caroselli e di una storia
N_BARRE = 46


def _ffmpeg_pcm(audio: Path, hz=16000):
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(audio), "-t", str(DURATA_MAX), "-ac", "1", "-ar", str(hz),
                        "-f", "f32le", "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f"ffmpeg non riesce a leggere l'audio {audio.name}: {r.stderr.decode(errors='replace')[:200]}")
    return np.frombuffer(r.stdout, dtype=np.float32)


def analizza(audio: Path) -> dict:
    """Durata e altezza delle barre dell'onda, ricavate dal volume reale dell'audio."""
    import numpy as np
    x = _ffmpeg_pcm(audio)
    durata = len(x) / 16000
    pezzi = np.array_split(np.abs(x), N_BARRE)
    liv = np.array([float(np.sqrt(np.mean(p ** 2))) if len(p) else 0 for p in pezzi])
    liv = liv / (liv.max() or 1)
    return dict(durata=durata, barre=[round(float(.12 + .88 * v ** .7), 3) for v in liv], pcm=x)


def trascrivi(pcm, modello="small") -> list[dict]:
    """Parole con i tempi (faster-whisper). Vanno rilette: una trascrizione può sbagliare una parola."""
    from faster_whisper import WhisperModel
    m = WhisperModel(modello, device="cpu", compute_type="int8")
    segmenti, _ = m.transcribe(pcm, language="it", word_timestamps=True, vad_filter=False)
    return [dict(t0=round(w.start, 2), t1=round(w.end, 2), testo=w.word.strip()) for s in segmenti for w in (s.words or []) if w.word.strip()]


def _frasi(parole: list[dict], larg: int, dim: int, righe=2) -> list[list[dict]]:
    """Raggruppa le parole in blocchi che stanno in `righe` righe: a schermo c'è un blocco per volta."""
    f, spazio = font("Bold", dim), font("Bold", dim).getlength(" ")
    blocchi, att, riga, nrighe = [], [], 0.0, 1
    for p in parole:
        lw = f.getlength(p["testo"])
        if att and riga + spazio + lw > larg:
            nrighe, riga = nrighe + 1, 0.0
        chiude = att and (nrighe > righe or p["t0"] - att[-1]["t1"] > 1.2)
        if chiude:
            blocchi.append(att)
            att, riga, nrighe = [], 0.0, 1
        riga += (spazio if att and riga else 0) + lw
        att.append(p)
        if p["testo"][-1:] in ".!?" and len(att) >= 2:
            blocchi.append(att)
            att, riga, nrighe = [], 0.0, 1
    return blocchi + ([att] if att else [])


def _tempo(s: float) -> str:
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def crea(audio: Path, uscita: Path, formato: str = "carosello", titolo: str = "", firma: str = "", indice: tuple[int, int] | None = None,
         parole: list[dict] | None = None, con_parole: bool = True) -> dict:
    """Scrive l'MP4 (e il fotogramma di copertina .png accanto). Restituisce durata, parole e percorsi."""
    W, H = (CW, CH) if formato == "carosello" else (SW, SH)
    dati = analizza(audio)
    durata = min(dati["durata"], DURATA_MAX)
    if parole is None and con_parole:
        try:
            parole = trascrivi(dati["pcm"])
        except ImportError:
            parole = []
    parole = parole or []

    # ── parte fissa: sfondo, titolo, scheda del lettore ─────────────────
    t = Tela(W, H, VERDE)
    dim_tit = 76 if formato == "carosello" else 84
    dim_cap = 64 if formato == "carosello" else 70
    zona = (110, CH - 130) if formato == "carosello" else (S_ALTO, S_BASSO - 20)
    h_tit = t.misura(W - 2 * M, titolo, dim_tit, "Black", 1.07) + 50 if titolo else 0
    totale = 100 + h_tit + 300 + 70 + int(dim_cap * 1.2 * 2)      # etichetta, titolo, lettore, due righe di parole
    alto = zona[0] + max(0, (zona[1] - zona[0] - totale) // 2)
    t.pillola(M, alto, "Messaggio vocale · audio originale", 28, CREMA, VERDE, traccia=3)
    y = alto + 100
    if titolo:
        y += t.testo(M, y, W - 2 * M, titolo, dim_tit, BIANCO, peso="Black", enfasi=AZZURRO, inter=1.07) + 50
    cx, cy, cw, ch = M, y, W - 2 * M, 300
    t.rett(cx, cy, cw, ch, BIANCO, raggio=48)
    D = 150  # cerchio play
    px, py = cx + 44, cy + (ch - D) // 2
    t.cerchio(px, py, D, VERDE)
    bx0, bx1 = px + D + 44, cx + cw - 50
    t.testo(bx0, cy + 40, bx1 - bx0, firma or "Dai messaggi dei nostri allievi", 38, NERO, peso="Bold")
    if formato == "carosello":
        _piede_c(t, indice[0], indice[1], True) if indice else None
    else:
        _piede_s(t, True)
    base = a_png(t).convert("RGB")

    by0, bh = cy + 110, 110          # zona dell'onda
    passo = (bx1 - bx0) / N_BARRE
    bw = max(6, int(passo * .56))
    spento = mescola(BIANCO, VERDE, .28)
    cap_y = cy + ch + 70
    blocchi = _frasi(parole, W - 2 * M, dim_cap)
    f_cap, f_time, f_inv = font("Bold", dim_cap), font("SemiBold", 28), font("Bold", 34)

    def fotogramma(sec: float, copertina=False) -> Image.Image:
        im = base.copy()
        d = ImageDraw.Draw(im)
        q = 0 if copertina else min(1.0, sec / durata)
        for i, v in enumerate(dati["barre"]):
            h = int(bh * v)
            x = int(bx0 + i * passo)
            acceso = (i + .5) / N_BARRE <= q
            d.rounded_rectangle((x, by0 + (bh - h) // 2, x + bw, by0 + (bh + h) // 2), bw // 2, fill=VERDE if acceso else spento)
        d.text((bx0, cy + ch - 62), f"{_tempo(0 if copertina else sec)} / {_tempo(durata)}", font=f_time, fill=mescola(NERO, BIANCO, .4))
        ccx, ccy = px + D // 2, py + D // 2
        if copertina or sec < .5:   # triangolo «play»
            d.polygon([(ccx - 22, ccy - 36), (ccx - 22, ccy + 36), (ccx + 40, ccy)], fill=BIANCO)
        else:                       # in riproduzione: due barre
            d.rounded_rectangle((ccx - 30, ccy - 34, ccx - 8, ccy + 34), 6, fill=BIANCO)
            d.rounded_rectangle((ccx + 8, ccy - 34, ccx + 30, ccy + 34), 6, fill=BIANCO)
        if copertina or not blocchi:
            d.text((M, cap_y), "Alza il volume e ascolta", font=f_inv, fill=CREMA)
            return im
        att = next((b for b in blocchi if b[0]["t0"] - .15 <= sec <= b[-1]["t1"] + .6), None)
        if att is None:
            att = next((b for b in reversed(blocchi) if b[-1]["t1"] <= sec), None) if sec < blocchi[-1][-1]["t1"] + 2 else None
        if att:
            x, yy, sp = M, cap_y, f_cap.getlength(" ")
            for p in att:
                lw = f_cap.getlength(p["testo"])
                if x > M and x + lw > W - M:
                    x, yy = M, yy + int(dim_cap * 1.2)
                col = AZZURRO if p["t0"] <= sec <= p["t1"] + .08 else (BIANCO if p["t0"] <= sec else mescola(VERDE, BIANCO, .45))
                d.text((x, yy), p["testo"], font=f_cap, fill=col)
                x += lw + sp
        return im

    uscita.parent.mkdir(parents=True, exist_ok=True)
    copertina = uscita.with_suffix(".png")
    fotogramma(0, copertina=True).save(copertina, optimize=True)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-t", f"{durata:.2f}", "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
           "-movflags", "+faststart", "-shortest", str(uscita)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for n in range(int(durata * FPS) + 1):
            p.stdin.write(fotogramma(n / FPS).tobytes())
        p.stdin.close()
    except BrokenPipeError:
        pass
    err = p.stderr.read().decode(errors="replace")
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg non ha creato il video: {err[:300]}")
    uscita.with_suffix(".parole.json").write_text(json.dumps(parole, ensure_ascii=False, indent=1), encoding="utf-8")
    return dict(video=uscita, copertina=copertina, durata=durata, parole=parole, testo=" ".join(w["testo"] for w in parole))
