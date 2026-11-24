"""Testimonianze Studio — flusso quotidiano.

    python esegui.py                      il contenuto di oggi
    python esegui.py --data 2026-11-26    il contenuto di un altro giorno (prova)
    python esegui.py --pianificato        come lo lancia l'Utilità di pianificazione (salta se è già fatto)
    python esegui.py --senza-scarico      usa il testimonianze.csv già presente
    python esegui.py --anteprime          rigenera le anteprime dei modelli (testi di esempio)
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import date, datetime
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))

from ts import consegna, controlli, dati, grafica, modelli, scrittura, selezione  # noqa: E402


class Fermo(Exception):
    """Errore previsto: finisce in ERRORE.txt con una spiegazione leggibile."""


def log(radice: Path, msg: str):
    riga = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(riga)
    (radice / "dati").mkdir(parents=True, exist_ok=True)
    with open(radice / "dati" / "log.txt", "a", encoding="utf-8") as f:
        f.write(riga + "\n")


def anteprime(cartella: Path):
    from ts import esempi
    foto = sorted((grafica.RISORSE / "foto").glob("*.jpg"))[2]
    for m, d in modelli.MODELLI.items():
        tele = modelli.disegna(m, esempi.per_modello(m), {"foto": foto})
        grafica.foglio_contatti(tele, cartella / f"{m}.jpg", alt=620 if m[0] == "C" else 700)
        grafica.a_pptx(tele, cartella / f"{m}.pptx")
        print("anteprima", m, d["nome"], len(tele))


def esegui(giorno: date, radice: Path, config: dict, scarica: bool, csv_esterno: Path | None) -> Path:
    cartella = radice / config["cartella_consegne"] / giorno.isoformat()
    piano = selezione.piano_del_giorno(giorno, config)
    quale = piano.get("leva") or piano.get("taglio")
    log(radice, f"Avvio per {giorno} ({piano['giorno']}): {piano['formato']} · {quale}")

    # 1. dati
    csv = csv_esterno or radice / "dati" / "testimonianze.csv"
    if scarica and not csv_esterno:
        try:
            n = dati.scarica(config, radice, csv)
            log(radice, f"Foglio scaricato: {n} righe")
        except Exception as e:
            raise Fermo("FOGLIO NON SCARICATO", f"{e}\n\nIl contenuto di oggi non è stato generato: senza i dati aggiornati "
                        "(stato, consenso) non si pubblica niente. Controlla la connessione, la chiave in dati/service-account.json "
                        "e che il foglio sia condiviso con l'email del service account.")
    if not csv.exists():
        raise Fermo("FOGLIO NON SCARICATO", f"Non trovo {csv}.")
    tutte = dati.carica(csv)

    # 2. scelta
    registro = selezione.Registro(radice / "dati" / "registro_utilizzi.csv")
    sel = selezione.candidati(tutte, giorno, piano, registro, config)
    if not sel["rosa"]:
        raise Fermo("NESSUNA TESTIMONIANZA VALIDA", "Nessuna riga supera le regole di oggi.\nEscluse: "
                    + "; ".join(f"{k}: {v}" for k, v in sel["esclusi"].items()))
    rosa = {t.id: t for t in sel["rosa"]}
    ordine = selezione.ordine_modelli(piano["formato"], giorno, registro)
    log(radice, f"Candidati: {len(rosa)} (validi {sel['validi']}) · modelli in ordine: {', '.join(ordine)}")

    # 3. scrittura + controlli
    base = scrittura.istruzioni(giorno, piano, sel["rosa"], ordine, config)
    errori, con, avvisi = [], None, []
    for tentativo in range(1, config["claude"].get("tentativi", 2) + 2):
        try:
            con = controlli.rifinisci(scrittura.chiedi_a_claude(base + (scrittura.correzione(errori) if errori else ""), config))
        except Exception as e:
            errori = [f"Risposta non utilizzabile: {e}"]
            log(radice, f"Tentativo {tentativo}: {errori[0]}")
            if isinstance(e, FileNotFoundError):
                break
            continue
        errori, avvisi = controlli.controlla(con, piano["formato"], rosa, ordine, config)
        log(radice, f"Tentativo {tentativo}: {len(errori)} errori, {len(avvisi)} avvisi")
        if not errori:
            break
    if errori or not con:
        raise Fermo("CONTENUTO NON GENERATO", "La scrittura non ha superato i controlli automatici:\n- " + "\n- ".join(errori))

    # 4. grafiche e consegna
    usate = [rosa[i] for i in con["ids"]]
    file = consegna.scrivi(cartella, giorno, piano, con, usate, sel, avvisi, config)
    (cartella / "contenuto.json").write_text(json.dumps(con, ensure_ascii=False, indent=1), encoding="utf-8")
    registro.registra(giorno, usate, piano["formato"], con["modello"], quale, con["storia"], cartella)
    log(radice, f"Consegna pronta: {len(file)} grafiche in {cartella}")
    return cartella


def main():
    ap = argparse.ArgumentParser(description="Testimonianze Studio")
    ap.add_argument("--data", help="AAAA-MM-GG (predefinito: oggi)")
    ap.add_argument("--radice", help="cartella con dati/ e Consegne/ (predefinito: questa)")
    ap.add_argument("--csv", help="usa questo CSV invece di scaricare il foglio")
    ap.add_argument("--senza-scarico", action="store_true")
    ap.add_argument("--pianificato", action="store_true")
    ap.add_argument("--anteprime", action="store_true")
    a = ap.parse_args()
    radice = Path(a.radice).resolve() if a.radice else QUI
    if a.anteprime:
        return anteprime(QUI / "anteprime")
    config = json.loads((QUI / "config.json").read_text(encoding="utf-8"))
    giorno = dati.leggi_data(a.data) if a.data else date.today()
    cartella = radice / config["cartella_consegne"] / giorno.isoformat()
    if a.pianificato:
        if datetime.now().strftime("%H:%M") < config.get("ora_esecuzione", "10:00"):
            return  # acceso prima dell'orario: ci pensa l'avvio delle 10:00
        if (cartella / "scheda.md").exists():
            return  # già consegnato oggi
    try:
        esegui(giorno, radice, config, scarica=not a.senza_scarico, csv_esterno=Path(a.csv) if a.csv else None)
        consegna.notifica("Testimonianze Studio: contenuto pronto", f"Consegna del {giorno:%d/%m} nella cartella Consegne.", cartella, QUI)
    except Fermo as e:
        p = consegna.scrivi_errore(cartella, *e.args)
        log(radice, f"ERRORE: {e.args[0]}")
        consegna.notifica("Testimonianze Studio: qualcosa è andato storto", f"{e.args[0]}. Dettagli in ERRORE.txt", cartella, QUI)
        sys.exit(1)
    except Exception:
        consegna.scrivi_errore(cartella, "ERRORE IMPREVISTO", traceback.format_exc())
        log(radice, "ERRORE IMPREVISTO (dettagli in ERRORE.txt)")
        consegna.notifica("Testimonianze Studio: qualcosa è andato storto", "Errore imprevisto. Dettagli in ERRORE.txt", cartella, QUI)
        sys.exit(1)


if __name__ == "__main__":
    main()
