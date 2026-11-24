"""Controlli automatici sul contenuto scritto da Claude, PRIMA di generare le grafiche.
Gli errori bloccano la consegna (si riprova, poi ERRORE.txt); gli avvisi finiscono in scheda.md."""
from __future__ import annotations

import re
import unicodedata

from .dati import RE_EMAIL, RE_TEL, RE_URL, Testimonianza
from .modelli import MODELLI
from .scrittura import FACOLTATIVI, LIMITI, NUMERO, ORDINE, SPAZIO, leggi_sticker

# parole che non compaiono mai (regola sulla salute: niente «guarisce», «cura», «risolve»)
RE_VIETATE = re.compile(r"\bguari\w*|\bguarig\w*|\bcur(?:a|are|ato|ata|ati|ate|ano|erà|ò|arsi)\b|\brisolv\w*|\brisolt\w*|"
                        r"\brisoluzion\w*|\bgarant\w*|\bgaranzi\w*", re.I)
RE_MARCHIO = re.compile(r"running school|mentorship|\btutor\b|\bsetter\b|\bchatter\b|\bCTE\b|\bRS\b|\bFS\b", re.I)
RE_PROMESSA = re.compile(r"\b(?:guarirai|starai meglio|tornerai a|riuscirai|ti passer\w+|sparir\w+|anche tu puoi|puoi farcela|"
                         r"succeder\w+ anche a te|funziona anche)\b", re.I)
RE_INVITO = re.compile(r"\b(?:commenta|scrivimi|scrivici|scrivi in dm|in dm|link in bio|clicca)\b", re.I)
RE_EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF️‍]")
RE_VIRGOLETTATO = re.compile(r"[«“\"]([^«»“”\"]{12,})[»”\"]")
RE_NUMERO = re.compile(r"\d+(?:[.,:']\d+)*")


def normalizza(s: str) -> str:
    return " ".join(parole(s))


def parole(s: str) -> list[str]:
    """Solo le parole, minuscole e senza accenti: il confronto ignora punteggiatura, maiuscole, emoji e a capo."""
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)


def _trova(ago: list[str], pagliaio: list[str], da: int) -> int:
    n = len(ago)
    for i in range(da, len(pagliaio) - n + 1):
        if pagliaio[i:i + n] == ago:
            return i + n
    return -1


def citazione_fedele(citazione: str, originale: str) -> bool:
    """Vero se la citazione è fatta solo di pezzi dell'originale, nello stesso ordine (i tagli si segnano con «…»)."""
    orig = parole(originale)
    pezzi = [parole(p) for p in re.split(r"\[\s*(?:…|\.\.\.)\s*\]|…|\.{3,}", citazione or "")]
    pezzi = [p for p in pezzi if p]
    if not pezzi or sum(len(p) for p in pezzi) < 3:
        return False
    pos = 0
    for p in pezzi:
        pos = _trova(p, orig, pos)
        if pos < 0:
            return False
    return True


def _testi(con: dict, caption=True) -> list[tuple[str, str]]:
    out = []
    for i, el in enumerate(con.get("elementi", []), 1):
        for campo in ("etichetta", "titolo", "testo", "prima", "dopo"):
            if el.get(campo):
                out.append((f"elemento {i} · {campo}", el[campo]))
        for c in el.get("citazioni") or []:
            out.append((f"elemento {i} · citazione", c.get("testo", "")))
    out.append(("cta", " ".join(str(v) for v in (con.get("cta") or {}).values())))
    if caption:
        out.append(("caption", con.get("caption", "")))
    return out


def rifinisci(con: dict) -> dict:
    """Pulizia formale prima dei controlli: spazi, emoji (il font del brand non le ha), virgolette doppie."""
    def pul(s):
        return re.sub(r"[ \t]+", " ", RE_EMOJI.sub("", str(s or ""))).strip()

    for el in con.get("elementi", []):
        el["ruolo"] = pul(el.get("ruolo")).lower().replace("à", "a")
        for campo in ("etichetta", "titolo", "testo", "prima", "dopo"):
            el[campo] = pul(el.get(campo))
        el["citazioni"] = [dict(id=str(c.get("id", "")).strip(), testo=pul(c.get("testo")).strip("«»“”\" "))
                           for c in (el.get("citazioni") or []) if pul(c.get("testo"))]
        if con.get("modello") != "C-primadopo":
            el["prima"] = el["dopo"] = ""
    con["ids"] = [str(i).strip() for i in con.get("ids", [])]
    con["caption"] = pul(con.get("caption")).replace(" \n", "\n")
    cta = con.setdefault("cta", {})
    cta["parola"] = pul(cta.get("parola")).upper()
    cta["tipo"] = pul(cta.get("tipo")).lower() or "dm"
    cta["sticker"] = pul(cta.get("sticker"))
    return con


def controlla(con: dict, formato: str, rosa: dict[str, Testimonianza], modelli_ammessi: list[str], config: dict):
    """Restituisce (errori, avvisi)."""
    err, avv = [], []
    els = con.get("elementi") or []
    ids = con.get("ids") or []
    lim = LIMITI[formato]

    # ── testimonianze scelte ────────────────────────────────────────────
    usate = [rosa[i] for i in ids if i in rosa]
    if not ids or len(usate) != len(ids):
        return [f"«ids» deve contenere solo id presenti tra i candidati (ricevuto: {ids})."], avv
    if len(set(ids)) != len(ids) or not 1 <= len(ids) <= 4:
        err.append("Le testimonianze usate devono essere da 1 a 4, senza ripetizioni.")
    storia = con.get("storia")
    if (storia == "singola") != (len(ids) == 1) or storia not in ("singola", "unita"):
        err.append("«storia» è «singola» con una testimonianza e «unita» con 2-4.")
    if len(usate) > 1:
        comuni = set.intersection(*[set(t.obiezioni) for t in usate]) | set.intersection(*[set(a.lower() for a in t.angolo) for t in usate])
        if not comuni:
            err.append("Le testimonianze di una storia unita devono avere in comune almeno una «obiezione» o un «angolo».")

    # ── struttura ───────────────────────────────────────────────────────
    nmin, nmax = NUMERO[formato]
    if not nmin <= len(els) <= nmax:
        err.append(f"Servono da {nmin} a {nmax} {'slide' if formato == 'carosello' else 'storie'}: ne hai scritte {len(els)}.")
    ordine = ORDINE[formato]
    ruoli = [e.get("ruolo") for e in els]
    if any(r not in ordine for r in ruoli):
        err.append(f"Ruoli ammessi, in quest'ordine: {', '.join(ordine)}. Ricevuti: {', '.join(map(str, ruoli))}.")
    else:
        if ruoli != sorted(ruoli, key=ordine.index):
            err.append(f"I ruoli devono seguire l'ordine {' → '.join(ordine)}.")
        manca = [r for r in ordine if r not in ruoli and r not in FACOLTATIVI]
        if manca:
            err.append(f"Mancano i passaggi obbligatori dello storytelling: {', '.join(manca)}.")
        if ruoli and (ruoli[0] != ordine[0] or ruoli[-1] != "cta" or ruoli.count("cta") != 1 or ruoli.count(ordine[0]) != 1):
            err.append(f"Il primo elemento è «{ordine[0]}» (uno solo) e l'ultimo è «cta» (uno solo).")
    parole_cta = set(config["cta"]["parole_carosello"])
    if els:
        primo = " ".join([els[0].get("titolo", ""), els[0].get("testo", "")])
        if RE_INVITO.search(primo) or any(re.search(rf"\b{p}\b", primo) for p in parole_cta):
            err.append("Il primo elemento parte dal problema: non deve contenere inviti all'azione né la parola chiave.")
        if not els[0].get("titolo"):
            err.append("Il primo elemento deve avere un titolo.")

    # ── CTA ─────────────────────────────────────────────────────────────
    cta = con.get("cta") or {}
    ammesse = set(parole_cta)
    if formato == "stories":
        ammesse |= {leggi_sticker(t.sticker, config)["parola"] for t in usate}
    if cta.get("parola") not in ammesse:
        err.append(f"«cta.parola» deve essere una fra: {', '.join(sorted(ammesse))}.")
    elif formato == "carosello" and els and cta["parola"] not in " ".join([els[-1].get("titolo", ""), els[-1].get("testo", "")]):
        err.append(f"L'ultima slide deve contenere la parola chiave {cta['parola']} in maiuscolo.")
    if formato == "carosello" and cta.get("parola") and cta["parola"] not in con.get("caption", ""):
        err.append("La caption deve chiudere con la stessa CTA e la parola chiave.")
    if not con.get("caption"):
        err.append("Manca la caption.")
    if formato == "stories" and els and not els[-1].get("titolo"):
        err.append("L'ultima storia deve avere un titolo (la domanda o l'invito).")

    # ── modello grafico ─────────────────────────────────────────────────
    mod = con.get("modello")
    if mod not in modelli_ammessi:
        err.append(f"«modello» deve essere uno fra: {', '.join(modelli_ammessi)}.")
    elif MODELLI[mod].get("solo_unita") and len(ids) < 2:
        err.append(f"Il modello {mod} si usa solo con una storia unita (2+ testimonianze): scegli il modello successivo della lista.")
    if mod == "C-primadopo" and sum(1 for e in els if e.get("prima") and e.get("dopo")) != 1:
        err.append("Con il modello C-primadopo serve esattamente un elemento con «prima» e «dopo» compilati.")

    # ── citazioni fedeli all'originale ──────────────────────────────────
    citate = set()
    for i, el in enumerate(els, 1):
        for c in el.get("citazioni") or []:
            t = rosa.get(c.get("id"))
            if not t or t.id not in ids:
                err.append(f"Elemento {i}: la citazione ha un id che non è tra le testimonianze scelte.")
                continue
            citate.add(t.id)
            if not citazione_fedele(c["testo"], t.testo_pulito):
                err.append(f"Elemento {i}: la citazione «{c['testo'][:70]}…» non è fedele al testo originale di {t.id}: copia le parole esatte (puoi solo tagliare, segnando «…»).")
            if len(c["testo"]) > lim["citazione"] * 1.15:
                err.append(f"Elemento {i}: citazione troppo lunga ({len(c['testo'])} caratteri, massimo {lim['citazione']}).")
        if formato == "stories" and len(el.get("citazioni") or []) > 2 or len(el.get("citazioni") or []) > 3:
            err.append(f"Elemento {i}: troppe citazioni nello stesso elemento.")
        for campo in ("titolo", "testo", "prima", "dopo", "etichetta"):
            if len(el.get(campo) or "") > lim[campo] * 1.15:
                err.append(f"Elemento {i}: «{campo}» troppo lungo ({len(el[campo])} caratteri, massimo {lim[campo]}).")
        tot = len(el.get("titolo") or "") + len(el.get("testo") or "") + sum(len(c["testo"]) for c in el.get("citazioni") or [])
        if tot > SPAZIO[formato] * 1.08:
            err.append(f"Elemento {i}: troppo testo ({tot} caratteri fra titolo, testo e citazioni; massimo {SPAZIO[formato]}). Accorcia il testo o la citazione.")
        if not (el.get("titolo") or el.get("testo") or el.get("citazioni") or el.get("prima")):
            err.append(f"Elemento {i}: è vuoto.")
    for t in usate:
        if t.id not in citate:
            err.append(f"La testimonianza {t.id} è tra quelle scelte ma non ha nessuna citazione: ogni testimonianza usata va citata almeno una volta.")
    originali = [t.testo_pulito for t in usate]
    for dove, testo in _testi(con):
        if "citazione" in dove:
            continue
        for m in RE_VIRGOLETTATO.finditer(testo):
            if len(parole(m.group(1))) >= 4 and not any(citazione_fedele(m.group(1), o) for o in originali):
                err.append(f"{dove}: la frase tra virgolette «{m.group(1)[:60]}…» non è nell'originale. Fuori dal campo «citazioni» non usare frasi virgolettate.")

    # ── dati personali, salute, marchio ─────────────────────────────────
    salute = any(t.salute for t in usate)
    for dove, testo in _testi(con):
        if RE_EMAIL.search(testo) or RE_URL.search(testo) or RE_TEL.search(testo):
            err.append(f"{dove}: contiene un'email, un link o un numero di telefono.")
        for t in usate:
            for p in t.vietati:
                if re.search(rf"(?<![\wÀ-ÿ])(?:{re.escape(p.capitalize())}|{re.escape(p.upper())}|{re.escape(p)})(?![\wÀ-ÿ])", testo):
                    err.append(f"{dove}: compare «{p}», che non può comparire (cognome o dato da oscurare).")
        m = RE_VIETATE.search(testo)
        if m:
            err.append(f"{dove}: contiene «{m.group(0)}». Niente guarisce/cura/risolve/garantisce: riformula, o scegli un altro pezzo di citazione.")
        m = RE_MARCHIO.search(testo)
        if m:
            err.append(f"{dove}: contiene «{m.group(0)}», che il brand non nomina nei contenuti.")
        if salute and "citazione" not in dove:
            m = RE_PROMESSA.search(testo)
            if m:
                err.append(f"{dove}: «{m.group(0)}» suona come una promessa di risultato su un tema di salute. Racconta solo l'esperienza personale.")

    # ── avvisi (non bloccano) ───────────────────────────────────────────
    fonti = " ".join(" ".join([t.testo_pulito, t.risultato, t.evento, t.tipo, t.hook, " ".join(t.profilo)]) for t in usate)
    cifre = lambda n: re.sub(r"\D", "", n)  # 3:36:20 e 3.36.20 sono lo stesso numero
    numeri_fonte = {cifre(n) for n in RE_NUMERO.findall(fonti)}
    for dove, testo in _testi(con):
        if "citazione" in dove or "etichetta" in dove or dove == "cta":
            continue
        noti = {str(len(ids)), str(len(els)), "42", "21", "42,195", "21,097"}  # distanze di maratona e mezza
        ignoti = [n for n in RE_NUMERO.findall(testo) if cifre(n) not in numeri_fonte and n not in noti]
        if ignoti:
            avv.append(f"{dove}: i numeri {', '.join(sorted(set(ignoti)))} non compaiono nella testimonianza originale. Controllali a mano.")
    return list(dict.fromkeys(err)), avv
