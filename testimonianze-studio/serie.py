"""Testimonianze Studio — serie «problemi»: trova i problemi più ricorrenti nelle testimonianze e, per ognuno,
crea un carosello e un set di stories con il problema nel titolo di copertina e le schermate dei messaggi.

    python serie.py analisi                 legge le testimonianze valide e raggruppa i problemi (dati/problemi.json)
    python serie.py genera --quanti 10      un carosello + un set di stories per ciascuno dei primi 10 problemi
    python serie.py genera --solo 3         rifà solo il problema n. 3

Valgono tutte le regole del flusso quotidiano (consenso, minorenni, 90 giorni, citazioni fedeli, salute).
Ogni testimonianza entra in un solo contenuto della serie. Uscita in <radice>/Serie-problemi/.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))

from ts import consegna, controlli, dati, grafica, scrittura, selezione  # noqa: E402

CARTELLA = "Serie-problemi"
IN_PARALLELO = 4

ETICHETTA = """Per ogni testimonianza qui sotto dimmi QUALE PROBLEMA aveva la persona prima o durante il percorso: la difficoltà,
la paura, il blocco o la convinzione che la frenava (non il risultato). Scrivilo come lo direbbe lei, in 3-8 parole,
in minuscolo: «ho sempre dolore al ginocchio», «paura di non finire la maratona», «i miei tempi non migliorano».
- «problemi»: da 0 a 2 frasi. Lista vuota se il testo non racconta nessun problema (per esempio solo un ringraziamento o la cronaca di una gara andata bene).
- «dettaglio»: quanto il testo racconta quel problema: 0 per niente, 1 accenno, 2 chiaro, 3 raccontato con particolari.
Usa solo quello che c'è scritto: non dedurre problemi che il testo non dice.
Rispondi con un solo oggetto JSON: {"righe": [{"id": "...", "problemi": ["..."], "dettaglio": 0}]}

Testimonianze:
"""

RAGGRUPPA = """Qui sotto ci sono i problemi raccontati dagli allievi di una scuola di corsa (Correre Naturale), uno per riga: id e frase.
Raggruppali nei problemi più ricorrenti: da 12 a 16 gruppi, ognuno un problema preciso e riconoscibile da chi corre
(non categorie vaghe come «difficoltà varie»). Una riga può stare in un solo gruppo; le righe che non c'entrano con nessun gruppo si lasciano fuori.
Per ogni gruppo:
- «chiave»: 2-3 parole minuscole con trattini (es. dolori-ricorrenti);
- «titolo»: il problema detto a chi legge, in seconda persona, come titolo di copertina (max 60 caratteri, niente numeri, niente soluzione);
- «descrizione»: 1-2 frasi su come si presenta questo problema nelle testimonianze;
- «salute»: true se il gruppo riguarda una malattia o condizione medica (diabete, neuropatia, malattie croniche, tumori, problemi cardiaci…), false per dolori e infortuni da corsa;
- «righe»: gli indici (numeri interi) delle righe del gruppo.
Rispondi con un solo oggetto JSON: {"gruppi": [{"chiave": "...", "titolo": "...", "descrizione": "...", "salute": false, "righe": [0, 1]}]}

Righe:
"""


def _carica(radice: Path, config: dict, oggi: date):
    tutte = dati.carica(radice / "dati" / "testimonianze.csv")
    registro = selezione.Registro(radice / "dati" / "registro_utilizzi.csv")
    validi = [t for t in tutte if selezione.motivo_esclusione(t, oggi, registro, config) is None]
    return tutte, validi, registro


def analisi(radice: Path, config: dict, oggi: date) -> dict:
    _, validi, _ = _carica(radice, config, oggi)
    lotti = [validi[i:i + 20] for i in range(0, len(validi), 20)]

    def etichetta(lotto):
        righe = [dict(id=t.id, risultato=t.risultato, testo=t.testo_pulito[:1800]) for t in lotto]
        for _ in range(3):
            try:
                r = scrittura.chiedi_a_claude(ETICHETTA + json.dumps(righe, ensure_ascii=False, indent=1), config)
                return [x for x in r.get("righe", []) if str(x.get("id")) in {t.id for t in lotto}]
            except Exception as e:
                print("  riprovo un lotto:", str(e)[:120])
        return []

    with ThreadPoolExecutor(IN_PARALLELO) as ex:
        etichette = [x for l in ex.map(etichetta, lotti) for x in l]
    print(f"Etichettate {len(etichette)} testimonianze su {len(validi)}")
    frasi = [(str(e["id"]), p, int(e.get("dettaglio") or 0)) for e in etichette for p in (e.get("problemi") or [])[:2] if p]
    elenco = "\n".join(f"{i}. {p}" for i, (_, p, _) in enumerate(frasi))
    gruppi = scrittura.chiedi_a_claude(RAGGRUPPA + elenco, config)["gruppi"]
    per_id = {t.id: t for t in validi}
    pref = config["selezione"]["forza_preferita"]
    out = []
    for g in gruppi:
        membri = {}
        for i in g.get("righe", []):
            if isinstance(i, int) and 0 <= i < len(frasi):
                tid, frase, det = frasi[i]
                if tid not in membri or det > membri[tid]["dettaglio"]:
                    membri[tid] = dict(id=tid, frase=frase, dettaglio=det)
        membri = list(membri.values())
        out.append(dict(chiave=g["chiave"], titolo=g["titolo"], descrizione=g.get("descrizione", ""), salute=bool(g.get("salute")),
                        testimonianze=len(membri), forti=sum(1 for m in membri if per_id[m["id"]].forza >= pref), membri=membri))
    out.sort(key=lambda g: (-g["testimonianze"], -g["forti"]))
    ris = dict(data=oggi.isoformat(), valide=len(validi), con_problema=len({f[0] for f in frasi}), problemi=out)
    (radice / "dati" / "problemi.json").write_text(json.dumps(ris, ensure_ascii=False, indent=1), encoding="utf-8")
    return ris


def _punti(t, m, oggi, config) -> float:
    return m["dettaglio"] * 3 + t.forza * 2 + selezione.punti_stagione(t, oggi, config) * .5 + min(len(t.testo_pulito), 1500) / 500


def assegna(problemi: list[dict], validi: list, registro, oggi: date, config: dict, quanti: int, per_rosa=4, salta=()) -> list[dict]:
    """Sceglie i problemi della serie e divide le testimonianze: nessuna entra in due contenuti."""
    per_id = {t.id: t for t in validi}
    gia = {r["id"] for r in registro.righe if CARTELLA not in r.get("cartella", "")}  # usate nelle consegne quotidiane, anche di oggi
    minima = config["selezione"]["forza_minima"]
    prese, piano = set(gia), []
    for p in problemi:
        if len(piano) >= quanti:
            break
        if p["salute"] or p["chiave"] in salta:
            continue  # i problemi di salute non diventano «titolo + soluzione»: restano esperienze personali
        liberi = [(per_id[m["id"]], m) for m in p["membri"] if m["id"] in per_id and m["id"] not in prese
                  and per_id[m["id"]].forza >= minima and m["dettaglio"] >= 1 and not per_id[m["id"]].salute]
        liberi.sort(key=lambda tm: -_punti(tm[0], tm[1], oggi, config))
        if len(liberi) < 4:
            continue
        car, sto = [t for t, _ in liberi[0::2][:per_rosa]], [t for t, _ in liberi[1::2][:per_rosa]]
        prese |= {t.id for t in car + sto}
        piano.append(dict(n=len(piano) + 1, problema=p, carosello=car, stories=sto))
    return piano


def scrivi_pezzo(radice: Path, config: dict, oggi: date, voce: dict, formato: str, registro_lock) -> dict:
    p, rosa_l = voce["problema"], voce[formato]
    rosa = {t.id: t for t in rosa_l}
    for t in rosa_l:
        t.extra = dict(leva=1, stagione=selezione.punti_stagione(t, oggi, config), evento=None, punti=0)
    modello = "C-schermo" if formato == "carosello" else "S-schermo"
    piano = dict(formato=formato, giorno=selezione.GIORNI[oggi.weekday()])
    piano.update({"taglio": "Educativo" if voce["n"] % 2 else "Pratico"} if formato == "carosello" else {"leva": "Obiezioni"})
    base = scrittura.istruzioni(oggi, piano, rosa_l, [modello], config, problema=p)
    errori, con, avvisi = [], None, []
    for _ in range(config["claude"].get("tentativi", 2) + 1):
        try:
            con = controlli.rifinisci(scrittura.chiedi_a_claude(base + (scrittura.correzione(errori) if errori else ""), config))
        except Exception as e:
            errori, con = [f"Risposta non utilizzabile: {e}"], None
            continue
        con["modello"] = con.get("modello") or modello
        errori, avvisi = controlli.controlla(con, formato, rosa, [modello], config, serie=True)
        if not errori:
            break
    cartella = radice / CARTELLA / f"{voce['n']:02d}-{p['chiave']}" / formato
    if errori or not con:
        consegna.scrivi_errore(cartella, "CONTENUTO NON GENERATO", "- " + "\n- ".join(errori))
        return dict(n=voce["n"], formato=formato, ok=False, errori=errori, cartella=cartella)
    usate = [rosa[i] for i in con["ids"]]
    sel = dict(validi=voce["validi"], forti_liberi=voce["forti"], in_leva=len(rosa_l), esclusi={}, note=[])
    file = consegna.scrivi(cartella, oggi, piano, con, usate, sel, avvisi, config, ctx={"tema": voce["n"] - 1 + (formato == "stories")})
    scheda = cartella / "scheda.md"
    scheda.write_text(f"**Serie problemi · n. {voce['n']} · «{p['titolo']}»** — problema raccontato in {p['testimonianze']} testimonianze "
                      f"({p['forti']} con Forza 4–5).\n\n" + scheda.read_text(encoding="utf-8"), encoding="utf-8")
    (cartella / "contenuto.json").write_text(json.dumps(con, ensure_ascii=False, indent=1), encoding="utf-8")
    _foglio(file, cartella.parent / f"anteprima-{formato}.jpg", 560 if formato == "carosello" else 640)
    return dict(n=voce["n"], formato=formato, ok=True, con=con, usate=usate, avvisi=avvisi, cartella=cartella, piano=piano, pezzi=len(file))


def genera(radice: Path, config: dict, oggi: date, quanti: int, solo: int | None, salta=()) -> list[dict]:
    pj = radice / "dati" / "problemi.json"
    if not pj.exists():
        analisi(radice, config, oggi)
    problemi = json.loads(pj.read_text(encoding="utf-8"))["problemi"]
    _, validi, registro = _carica(radice, config, oggi)
    forti = sum(1 for t in validi if t.forza >= config["selezione"]["forza_preferita"])
    piano = assegna(problemi, validi, registro, oggi, config, quanti, salta=salta)
    for v in piano:
        v.update(validi=len(validi), forti=forti)
    lavori = [(v, f) for v in piano for f in ("carosello", "stories") if solo in (None, v["n"])]
    with ThreadPoolExecutor(IN_PARALLELO) as ex:
        ris = list(ex.map(lambda vf: scrivi_pezzo(radice, config, oggi, vf[0], vf[1], None), lavori))
    # registro: una riga per testimonianza usata (i contenuti della serie si aggiungono, non sostituiscono la giornata)
    rifatti = {str(r["cartella"]) for r in ris}
    registro.righe = [r for r in registro.righe if r.get("cartella") not in rifatti]
    for r in ris:
        if r["ok"]:
            registro.registra(oggi, r["usate"], r["formato"], r["con"]["modello"], "Serie problemi", r["con"]["storia"], r["cartella"], aggiungi=True)
    _indice(radice, piano, ris, problemi, oggi)
    return ris


def _foglio(file: list[Path], uscita: Path, alt: int):
    from PIL import Image
    ims = [Image.open(f) for f in file]
    ims = [i.resize((round(i.width * alt / i.height), alt)) for i in ims]
    foglio = Image.new("RGB", (sum(i.width + 12 for i in ims) + 12, alt + 24), "#D9D9D9")
    x = 12
    for i in ims:
        foglio.paste(i, (x, 12))
        x += i.width + 12
    foglio.save(uscita, quality=86)


def ridisegna(radice: Path):
    """Rifà solo le grafiche (PNG, PPTX, anteprime) dai contenuto.json già scritti: serve dopo un ritocco ai modelli."""
    from ts import modelli
    for cj in sorted((radice / CARTELLA).glob("*/*/contenuto.json")):
        con = json.loads(cj.read_text(encoding="utf-8"))
        formato, n = cj.parent.name, int(cj.parent.parent.name[:2])
        tele = modelli.disegna(con["modello"], con, {"tema": n - 1 + (formato == "stories")})
        for vecchio in list(cj.parent.glob("*.png")) + list(cj.parent.glob("*.pptx")):
            vecchio.unlink()
        file = grafica.salva(tele, cj.parent, "carosello" if formato == "carosello" else "storia",
                             pptx="carosello.pptx" if formato == "carosello" else "stories.pptx")
        _foglio(file, cj.parent.parent / f"anteprima-{formato}.jpg", 560 if formato == "carosello" else 640)
        print("ridisegnato", cj.parent.parent.name, formato, len(file))


def _indice(radice: Path, piano: list[dict], ris: list[dict], problemi: list[dict], oggi: date):
    per = defaultdict(dict)
    for r in ris:
        per[r["n"]][r["formato"]] = r
    righe = [f"# Serie «problemi» · {oggi.isoformat()}", "",
             "Un carosello e un set di stories per ciascuno dei problemi più ricorrenti nelle testimonianze. In copertina c'è il problema; "
             "le schermate riportano le parole esatte degli allievi, ricomposte in stile brand (non sono gli screenshot originali).", "",
             "| N. | Problema in copertina | Testimonianze che lo raccontano | Carosello | Stories |", "|---|---|---|---|---|"]
    for v in piano:
        def cella(f):
            r = per.get(v["n"], {}).get(f)
            if not r:
                return "non rifatto"
            if not r["ok"]:
                return "NON GENERATO (vedi ERRORE.txt)"
            return f"{r['pezzi']} {'slide' if f == 'carosello' else 'storie'} · " + ", ".join(t.firma or "anonimo" for t in r["usate"])
        p = v["problema"]
        righe.append(f"| {v['n']:02d} | {p['titolo']} | {p['testimonianze']} ({p['forti']} con Forza 4–5) | {cella('carosello')} | {cella('stories')} |")
    righe += ["", "## Tutti i problemi trovati", "", "| Problema | Testimonianze | Forza 4–5 | Nota |", "|---|---|---|---|"]
    scelti = {v["problema"]["chiave"] for v in piano}
    for p in problemi:
        nota = "nella serie" if p["chiave"] in scelti else "tema di salute: escluso dalla serie" if p["salute"] else "non in serie"
        righe.append(f"| {p['titolo']} | {p['testimonianze']} | {p['forti']} | {nota} |")
    (radice / CARTELLA).mkdir(parents=True, exist_ok=True)
    (radice / CARTELLA / "INDICE.md").write_text("\n".join(righe) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Serie problemi")
    ap.add_argument("comando", choices=["analisi", "genera", "ridisegna"])
    ap.add_argument("--radice")
    ap.add_argument("--data")
    ap.add_argument("--quanti", type=int, default=10)
    ap.add_argument("--solo", type=int)
    ap.add_argument("--salta", default="", help="chiavi dei problemi da lasciare fuori, separate da virgola")
    a = ap.parse_args()
    radice = Path(a.radice).resolve() if a.radice else QUI
    config = json.loads((QUI / "config.json").read_text(encoding="utf-8"))
    oggi = dati.leggi_data(a.data) if a.data else date.today()
    if a.comando == "ridisegna":
        return ridisegna(radice)
    if a.comando == "analisi":
        r = analisi(radice, config, oggi)
        print(f"Testimonianze valide {r['valide']}, con un problema raccontato {r['con_problema']}")
        for p in r["problemi"]:
            print(f"  {p['testimonianze']:3d} ({p['forti']:2d} forti) {'[salute] ' if p['salute'] else ''}{p['titolo']}")
    else:
        for r in genera(radice, config, oggi, a.quanti, a.solo, salta=tuple(x.strip() for x in a.salta.split(",") if x.strip())):
            print(f"  {r['n']:02d} {r['formato']:9s} {'ok · ' + str(r['pezzi']) + ' grafiche · ' + ', '.join(t.id for t in r['usate']) if r['ok'] else 'NON GENERATO: ' + '; '.join(r['errori'])[:200]}")


if __name__ == "__main__":
    main()
