"""Selezione: quali testimonianze si possono usare oggi (regole fisse) e quali proporre a Claude (punteggio).
Qui stanno anche il registro degli utilizzi (regola dei 90 giorni) e la rotazione dei modelli grafici."""
from __future__ import annotations

import csv
import hashlib
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from .dati import Testimonianza, leggi_data
from .modelli import MODELLI

GIORNI = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]
CAMPI_REGISTRO = ["data", "id", "nome", "formato", "modello", "leva_o_taglio", "storia", "cartella"]


class Registro:
    """Registro locale degli utilizzi (dati/registro_utilizzi.csv). Il foglio Google non viene mai toccato."""

    def __init__(self, percorso: Path):
        self.percorso, self.righe = percorso, []
        if percorso.exists():
            with open(percorso, newline="", encoding="utf-8-sig") as f:
                self.righe = [r for r in csv.DictReader(f) if r.get("id")]

    def ultimo_uso(self, id_: str, escluso: date | None = None) -> date | None:
        """Ultimo utilizzo registrato, senza contare il giorno che si sta (ri)generando."""
        d = [leggi_data(r["data"]) for r in self.righe if r["id"] == id_]
        d = [x for x in d if x and x != escluso]
        return max(d) if d else None

    def consegne(self, prima_di: date) -> list[tuple[date, str, str]]:
        """(data, formato, modello) delle consegne precedenti, dalla più recente."""
        viste = {}
        for r in self.righe:
            d = leggi_data(r["data"])
            if d and d < prima_di:
                viste[d] = (d, r["formato"], r["modello"])
        return sorted(viste.values(), reverse=True)

    def registra(self, giorno: date, usate: list[Testimonianza], formato, modello, leva, storia, cartella):
        self.righe = [r for r in self.righe if r["data"] != giorno.isoformat()]  # rifare un giorno non conta doppio
        for t in usate:
            self.righe.append(dict(data=giorno.isoformat(), id=t.id, nome=t.nome, formato=formato, modello=modello,
                                   leva_o_taglio=leva, storia=storia, cartella=str(cartella)))
        self.percorso.parent.mkdir(parents=True, exist_ok=True)
        with open(self.percorso, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=CAMPI_REGISTRO)
            w.writeheader()
            w.writerows(self.righe)


# ── regole fisse ─────────────────────────────────────────────────────────────
def motivo_esclusione(t: Testimonianza, oggi: date, registro: Registro, config: dict) -> str | None:
    """None se la testimonianza si può usare oggi, altrimenti il motivo dell'esclusione."""
    sel = config["selezione"]
    if t.stato.strip().lower() != sel["stato_valido"].lower():
        return "stato diverso da Catalogato"
    if t.minorenne:
        return "minorenne"
    if t.consenso_negato:
        return "consenso negato"
    if any(u in sel["escludi_uso_consigliato"] for u in t.uso) or t.momento in sel["escludi_momento_funnel"]:
        return "uso interno"
    if len(t.testo_pulito) < sel["testo_minimo_caratteri"]:
        return "testo troppo breve per citarlo"
    limite = oggi - timedelta(days=sel["giorni_senza_riuso"])
    usi = [d for d in (registro.ultimo_uso(t.id, escluso=oggi), t.ultimo_utilizzo) if d and d < oggi]
    if usi and max(usi) > limite:
        return f"già usata negli ultimi {sel['giorni_senza_riuso']} giorni"
    return None


# ── punteggio ────────────────────────────────────────────────────────────────
def punti_leva(t: Testimonianza, leva: dict) -> int:
    p = 0
    p += any(o in t.obiezioni for o in leva.get("obiezione", []))
    p += any(x in t.profilo for x in leva.get("profilo", []))
    p += t.momento in leva.get("momento", [])
    p += any(t.tipo.lower().startswith(x.lower()) for x in leva.get("tipo_inizia_con", []))
    p += bool(leva.get("obiezione_qualsiasi") and t.obiezioni)
    if leva.get("richiede_risultato") and not t.risultato:
        p = 0
    return int(p)


def _nel_periodo(oggi: date, da: str, a: str, anticipo: int) -> int:
    for anno in (oggi.year, oggi.year + 1):
        inizio = date(anno, int(da[:2]), int(da[3:]))
        fine = date(anno, int(a[:2]), int(a[3:]))
        if inizio <= oggi <= fine:
            return 3
        if inizio - timedelta(days=anticipo) <= oggi < inizio:
            return 2
    return 0


def punti_stagione(t: Testimonianza, oggi: date, config: dict) -> int:
    st = config["stagioni"].get(t.stagione)
    return _nel_periodo(oggi, st["da"], st["a"], config["stagioni"].get("anticipo_giorni", 30)) if isinstance(st, dict) else 0


def evento_vicino(t: Testimonianza, oggi: date, config: dict) -> str | None:
    ev = config.get("eventi", {})
    testo = " ".join([t.evento, t.tipo, t.risultato, t.testo_pulito]).lower()
    for e in ev.get("elenco", []):
        d = leggi_data(e.get("data", ""))
        if d and timedelta(days=-2) <= d - oggi <= timedelta(days=ev.get("giorni_prima", 21)) \
                and any(p.lower() in testo for p in e.get("parole", [])):
            return e["nome"]
    return None


def _caso(giorno: date, id_: str) -> float:
    """Piccola variazione stabile per giorno: a parità di punteggio non esce sempre la stessa."""
    return int(hashlib.sha256(f"{giorno}{id_}".encode()).hexdigest()[:6], 16) / 0xFFFFFF


def candidati(tutte: list[Testimonianza], oggi: date, piano: dict, registro: Registro, config: dict) -> dict:
    """Applica le regole fisse, ordina per punteggio e restituisce la rosa da proporre a Claude."""
    sel = config["selezione"]
    esclusi, validi = Counter(), []
    for t in tutte:
        m = motivo_esclusione(t, oggi, registro, config)
        if m:
            esclusi[m] += 1
        else:
            validi.append(t)
    leva = config["leve"].get(piano.get("leva", ""), None)
    note = []
    for t in validi:
        pl = punti_leva(t, leva) if leva else 1
        ps, ev = punti_stagione(t, oggi, config), evento_vicino(t, oggi, config)
        t.extra = dict(leva=pl, stagione=ps, evento=ev,
                       punti=t.forza * 2 + pl * 3 + ps + (6 if ev else 0) + (len(t.testo_pulito) >= sel["testo_storia_singola_caratteri"])
                             + .5 * bool(t.citazione) + _caso(oggi, t.id))
    ordina = lambda l: sorted(l, key=lambda t: -t.extra["punti"])
    in_leva = [t for t in validi if t.extra["leva"] > 0]
    rosa = ordina([t for t in in_leva if t.forza >= sel["forza_preferita"]])
    if len(rosa) < 4:
        altri = ordina([t for t in in_leva if sel["forza_minima"] <= t.forza < sel["forza_preferita"]])
        if altri:
            note.append(f"Poche testimonianze con Forza {sel['forza_preferita']}–5 per questa leva: aggiunte {min(len(altri), 6)} con Forza {sel['forza_minima']}.")
        rosa += altri
    if len(rosa) < 2 and leva:
        altri = ordina([t for t in validi if t not in rosa and t.forza >= sel["forza_minima"]])
        if altri:
            note.append(f"Nessuna testimonianza libera per la leva «{piano['leva']}»: uso le migliori disponibili di altre leve.")
        rosa += altri
    n = sel["candidati_per_claude"]
    testa = rosa[: max(4, n - 4)]
    # compagne di tema: stessa obiezione delle prime, per poter costruire una «storia unita»
    temi = Counter(o for t in testa[:4] for o in t.obiezioni)
    compagne = [t for t in rosa[len(testa):] + ordina([v for v in validi if v not in rosa and v.forza >= sel["forza_minima"]])
                if any(o in temi for o in t.obiezioni)]
    scelta = (testa + [c for c in compagne if c not in testa])[:n]
    if len(scelta) < min(n, len(rosa)):
        scelta += [t for t in rosa if t not in scelta][: n - len(scelta)]
    return dict(rosa=scelta, validi=len(validi), in_leva=len(in_leva), esclusi=dict(esclusi), note=note,
                forti_liberi=sum(1 for t in validi if t.forza >= sel["forza_preferita"]))


# ── calendario e rotazione dei modelli ───────────────────────────────────────
def piano_del_giorno(oggi: date, config: dict) -> dict:
    p = dict(config["calendario"][GIORNI[oggi.weekday()]])
    p["giorno"] = GIORNI[oggi.weekday()]
    return p


def ordine_modelli(formato: str, oggi: date, registro: Registro) -> list[str]:
    """Modelli del formato in ordine di preferenza: prima quelli usati meno di recente.
    Mai lo stesso modello dell'ultima uscita di quel formato, mai la stessa «famiglia» di ieri."""
    miei = [m for m, d in MODELLI.items() if d["formato"] == formato]
    passate = registro.consegne(oggi)
    ultimo_uso = {}
    for d, f, m in passate:
        ultimo_uso.setdefault(m, d)
    stesso_formato = next((m for d, f, m in passate if f == formato), None)
    ieri = next((m for d, f, m in passate if d == oggi - timedelta(days=1)), None)
    fam_ieri = MODELLI[ieri]["famiglia"] if ieri in MODELLI else None
    giro = oggi.toordinal() % len(miei)
    miei = miei[giro:] + miei[:giro]
    ordinati = sorted(miei, key=lambda m: ultimo_uso.get(m, date.min))
    buoni = [m for m in ordinati if m != stesso_formato and MODELLI[m]["famiglia"] != fam_ieri]
    return buoni or [m for m in ordinati if m != stesso_formato] or ordinati
