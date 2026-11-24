"""Consegna: grafiche PNG, PPTX modificabile, caption.txt, scheda.md, ERRORE.txt e notifica sul PC."""
from __future__ import annotations

import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from . import grafica, modelli
from .dati import Testimonianza
from .scrittura import leggi_sticker

NOMI_GIORNI = {"lunedi": "lunedì", "martedi": "martedì", "mercoledi": "mercoledì", "giovedi": "giovedì",
               "venerdi": "venerdì", "sabato": "sabato", "domenica": "domenica"}
NOMI_STICKER = {"sondaggio": "Sondaggio", "slider": "Slider con emoji", "domanda": "Box domande", "dm": "nessuno sticker (invito in DM)"}


def _svuota(cartella: Path):
    cartella.mkdir(parents=True, exist_ok=True)
    for f in cartella.iterdir():
        if f.suffix.lower() in (".png", ".pptx") or f.name in ("caption.txt", "scheda.md", "ERRORE.txt"):
            f.unlink()


def _foto(giorno: date, config: dict):
    if not config.get("grafica", {}).get("usa_foto", True):
        return None
    foto = sorted((grafica.RISORSE / "foto").glob("*.jpg")) + sorted((grafica.RISORSE / "foto").glob("*.png"))
    return foto[giorno.toordinal() % len(foto)] if foto else None


def scrivi(cartella: Path, giorno: date, piano: dict, con: dict, usate: list[Testimonianza], sel: dict, avvisi: list[str],
           config: dict) -> list[Path]:
    _svuota(cartella)
    formato = piano["formato"]
    per_id = {t.id: t for t in usate}
    for el in con["elementi"]:
        for c in el.get("citazioni") or []:
            c["firma"] = per_id[c["id"]].firma
    tele = modelli.disegna(con["modello"], con, {"foto": _foto(giorno, config)})
    prefisso = "carosello" if formato == "carosello" else "storia"
    file = grafica.salva(tele, cartella, prefisso, pptx=("carosello.pptx" if formato == "carosello" else "stories.pptx"))
    (cartella / "caption.txt").write_text(_caption(con, formato), encoding="utf-8")
    (cartella / "scheda.md").write_text(_scheda(giorno, piano, con, usate, sel, avvisi, len(tele)), encoding="utf-8")
    return file


def _cta_riga(con: dict, formato: str) -> str:
    cta = con["cta"]
    if formato == "carosello":
        return f"Commenta {cta['parola']} (parola chiave in ultima slide e in caption)."
    st = NOMI_STICKER.get(cta.get("tipo"), cta.get("tipo", ""))
    dom = f" «{cta['sticker']}»" if cta.get("sticker") else ""
    return f"Ultima storia: sticker {st}{dom}, da aggiungere su Instagram nello spazio vuoto. Invito in DM con la parola {cta['parola']}."


def _caption(con: dict, formato: str) -> str:
    return f"{con['caption'].strip()}\n\n----------\nCTA: {_cta_riga(con, formato)}\n"


def _scheda(giorno: date, piano: dict, con: dict, usate: list[Testimonianza], sel: dict, avvisi: list[str], n: int) -> str:
    formato = piano["formato"]
    r = [f"# Testimonianze Studio · {giorno.isoformat()} ({NOMI_GIORNI[piano['giorno']]})", ""]
    non_conf = [t for t in usate if not t.consenso_confermato]
    if non_conf:
        r += ["> **ATTENZIONE · CONSENSO NON CONFERMATO** per " + ", ".join(f"{t.id} ({t.allievo})" for t in non_conf)
              + ". Nel contenuto compare solo il nome di battesimo (o nessun nome). Verifica il consenso prima di pubblicare.", ""]
    oscurate = [t for t in usate if t.da_oscurare]
    if oscurate:
        r += ["> **DA OSCURARE** per " + ", ".join(t.id for t in oscurate) + ": nel contenuto non compaiono nomi, cognomi né numeri di contatto, "
              "e gli screenshot originali non sono usati.", ""]
    quale = f"leva {piano['leva']}" if formato == "stories" else f"taglio {piano['taglio']}"
    r += [f"**Formato:** {formato} ({quale}) · {n} {'slide' if formato == 'carosello' else 'storie'} · modello «{modelli.MODELLI[con['modello']]['nome']}» · storia {con['storia']}",
          f"**Argomento:** {con.get('argomento', '')}", "", "## Testimonianze usate", "",
          "| ID | Nome (dal foglio) | Consenso | Forza | Nel contenuto compare come | Da oscurare | Tema salute |", "|---|---|---|---|---|---|---|"]
    for t in usate:
        r.append(f"| {t.id} | {t.allievo} | {t.consenso or 'vuoto'} | {t.forza} | {t.firma or 'anonimo'} | {'sì' if t.da_oscurare else 'no'} | {'sì' if t.salute else 'no'} |")
    r += ["", "## Perché sono state scelte", "", con.get("motivo_scelta", "").strip(), ""]
    for t in usate:
        x = t.extra
        dett = [f"Forza {t.forza}"]
        if formato == "stories":
            dett.append(f"corrispondenze con la leva: {x.get('leva', 0)}")
        if x.get("evento"):
            dett.append(f"evento vicino: {x['evento']}")
        if x.get("stagione"):
            dett.append(f"in stagione («{t.stagione}»)")
        if t.obiezioni:
            dett.append("obiezione: " + ", ".join(t.obiezioni))
        r.append(f"- {t.id}: " + "; ".join(dett) + ".")
    s = con.get("struttura", {})
    r += ["", "## Struttura", "", f"**Problema:** {s.get('problema', '')}", "", f"**Difficoltà:** {s.get('difficolta', '')}", "",
          f"**Soluzione:** {s.get('soluzione', '')}", "", f"**Risultato:** {s.get('risultato', '')}", "", f"**CTA:** {s.get('cta', '')}", "",
          "## Prima di pubblicare", "", f"- {_cta_riga(con, formato)}"]
    if any(t.salute for t in usate):
        r.append("- Tema salute: rileggi che l'esperienza sia raccontata come personale, senza promesse per chi legge.")
    r += [f"- {a}" for a in avvisi + sel.get("note", [])]
    r += ["", "## Controlli automatici superati", "",
          "Stato «Catalogato», nessun minorenne, nessun riuso negli ultimi 90 giorni, citazioni fatte solo di parole dell'originale, "
          "nessun cognome, email, telefono o link, nessuna parola vietata (guarisce, cura, risolve, garantisce), storytelling problema → CTA, parola chiave ammessa.",
          "", "## Scorta", "",
          f"Testimonianze utilizzabili oggi: {sel['validi']} (di cui {sel['forti_liberi']} con Forza 4–5"
          + (f", {sel['in_leva']} adatte alla leva di oggi" if formato == "stories" else "") + "). Escluse: "
          + ("; ".join(f"{k} {v}" for k, v in sorted(sel["esclusi"].items(), key=lambda kv: -kv[1])) or "nessuna") + ".", ""]
    return "\n".join(r)


def scrivi_errore(cartella: Path, titolo: str, dettagli: str = "") -> Path:
    cartella.mkdir(parents=True, exist_ok=True)
    p = cartella / "ERRORE.txt"
    p.write_text(f"Testimonianze Studio · {datetime.now():%Y-%m-%d %H:%M}\n\n{titolo}\n\n{dettagli}".rstrip() + "\n", encoding="utf-8")
    return p


def notifica(titolo: str, testo: str, cartella: Path, radice: Path) -> bool:
    """Notifica di Windows (clic = apre la cartella). Sugli altri sistemi scrive solo a schermo."""
    print(f"[notifica] {titolo} — {testo}")
    if sys.platform != "win32":
        return False
    try:
        r = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(radice / "notifica.ps1"),
                            "-Titolo", titolo, "-Testo", testo, "-Cartella", str(cartella)], capture_output=True, timeout=30,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return r.returncode == 0
    except Exception:
        return False
