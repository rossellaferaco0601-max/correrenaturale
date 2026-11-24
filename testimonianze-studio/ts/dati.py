"""Dati: scarico del foglio con il service account (sola lettura), lettura del CSV, pulizia dei dati personali."""
from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote

COLONNE = ["ID", "Data", "Ora", "Allievo", "Coach", "Percorso", "Tipo", "Evento / Contesto", "Risultato",
           "Angolo narrativo", "Citazione chiave", "Uso consigliato", "Allegati", "Risposte thread", "Reazioni",
           "Link Slack", "Testo completo", "Stato", "Note", "Obiezione che smonta", "Profilo allievo", "Momento funnel",
           "Stagione / aggancio", "Formato story", "Hook prima slide", "Sticker / CTA", "Forza (1-5)", "Consenso",
           "Da oscurare", "Ultimo utilizzo", "N. utilizzi"]
AMBITO = "https://www.googleapis.com/auth/spreadsheets.readonly"


# ── scarico ──────────────────────────────────────────────────────────────────
def scrivi_csv(valori: list[list], percorso: Path) -> int:
    """Scrive le righe del foglio in un CSV. Le righe arrivano «monche» (Google taglia le celle vuote in coda)."""
    if not valori or [str(c).strip() for c in valori[0][:3]] != COLONNE[:3]:
        raise ValueError("Il foglio non ha l'intestazione attesa (ID, Data, Ora…): controlla il nome della scheda.")
    n = len(valori[0])
    percorso.parent.mkdir(parents=True, exist_ok=True)
    tmp = percorso.with_suffix(".tmp")
    with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        for r in valori:
            w.writerow([str(c) for c in r] + [""] * (n - len(r)))
    os.replace(tmp, percorso)
    return len(valori) - 1


def scarica(config: dict, radice: Path, destinazione: Path) -> int:
    """Scarica la scheda «Archivio» con il service account. Solo lettura: il foglio non viene mai modificato."""
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account

    fg = config["foglio"]
    chiave = radice / fg["chiave_service_account"]
    if not chiave.exists():
        raise FileNotFoundError(f"Manca la chiave del service account: {chiave}")
    cred = service_account.Credentials.from_service_account_file(str(chiave), scopes=[AMBITO])
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{fg['id']}/values/{quote(fg['scheda'], safe='')}"
    r = AuthorizedSession(cred).get(url, params={"valueRenderOption": "FORMATTED_VALUE"}, timeout=60)
    if r.status_code == 403:
        raise PermissionError("Il service account non può leggere il foglio: condividilo con la sua email come Visualizzatore "
                              "e controlla che la «Google Sheets API» sia abilitata nel progetto.")
    r.raise_for_status()
    return scrivi_csv(r.json().get("values", []), destinazione)


# ── lettura ──────────────────────────────────────────────────────────────────
def leggi_data(s: str, id_riga: str = "") -> date | None:
    """Le date del foglio sono in due formati: AAAA-MM-GG e GG/MM/AAAA. In mancanza, la data si ricava dall'ID."""
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    if id_riga.isdigit() and len(id_riga) == 10:
        return datetime.fromtimestamp(int(id_riga), tz=timezone.utc).date()
    return None


def dividi(s: str) -> list[str]:
    """Celle con più valori separati da virgola. Le virgole dentro le parentesi non separano."""
    out, buf, liv = [], "", 0
    for ch in s or "":
        liv += ch == "("
        liv -= ch == ")"
        if ch == "," and liv <= 0:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    return [v.strip() for v in out + [buf] if v.strip()]


PARTICELLE = {"de", "di", "da", "del", "della", "dello", "dei", "degli", "lo", "la", "le", "li", "van", "von", "d", "dal", "dalla"}
RE_NOME = re.compile(r"^[A-Za-zÀ-ÿ'’.\- ]{3,40}$")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_URL = re.compile(r"(?:https?://|www\.)\S+")
RE_TEL = re.compile(r"(?<![\d:.,])(?:\+\d{1,3}[\s.-]?)?(?:\d[\s.-]?){9,12}(?![\d:])")
RE_EMOJI_SLACK = re.compile(r":[a-z0-9_+\-]{2,40}:")
RE_MENZIONE = re.compile(r"<@[^>]+>|(?<!\w)@[\wÀ-ÿ.]+")
RE_SALUTE = re.compile(r"\b(?:neuropat|diabet|tumor|cancro\b|sclerosi|cronic|chemio|infarto|cardiopat|fibromialg|parkinson|"
                       r"autoimmun|oncolog|leucemi|ictus\b|asma\b|artrite reumatoide|depression|patologi|malatti)", re.I)


@dataclass
class Testimonianza:
    id: str
    riga: dict
    data: date | None
    allievo: str
    nome: str            # nome di battesimo ("" se non ricavabile)
    cognomi: list[str]
    tipo: str
    percorso: str
    evento: str
    risultato: str
    angolo: list[str]
    citazione: str
    uso: list[str]
    testo: str           # testo completo ORIGINALE
    stato: str
    obiezioni: list[str]
    profilo: list[str]
    momento: str
    stagione: str
    formato_story: str
    hook: str
    sticker: str
    forza: int
    consenso: str
    oscurare: str
    ultimo_utilizzo: date | None
    testo_pulito: str = ""
    extra: dict = field(default_factory=dict)

    # ── regole sul consenso ─────────────────────────────────────────────
    @property
    def minorenne(self) -> bool:
        return "minorenne" in self.consenso.lower()

    @property
    def consenso_negato(self) -> bool:
        return self.consenso.strip().lower() == "no"

    @property
    def consenso_confermato(self) -> bool:
        return self.consenso.strip().lower() in ("sì", "si", "sí")

    @property
    def da_oscurare(self) -> bool:
        return bool(self.oscurare.strip())

    @property
    def salute(self) -> bool:
        return (self.tipo.lower().startswith("salute") or "Ho un problema di salute" in self.obiezioni
                or "Salute" in self.profilo or bool(RE_SALUTE.search(self.testo + " " + self.risultato)))

    @property
    def firma(self) -> str:
        """Come compare il nome nel contenuto. Consenso confermato: nome e cognome. Altrimenti solo il nome
        di battesimo. Se «Da oscurare» è compilato: nessun nome."""
        if self.da_oscurare or not self.nome:
            return ""
        return self.allievo if self.consenso_confermato else self.nome

    @property
    def vietati(self) -> list[str]:
        """Parole che non devono comparire in nessun punto del contenuto."""
        v = [] if self.consenso_confermato and not self.da_oscurare else list(self.cognomi)
        if self.da_oscurare and self.nome:
            v.append(self.nome)
        return v


def _nome(allievo: str) -> tuple[str, list[str]]:
    a = re.sub(r"\s+", " ", allievo or "").strip()
    if not RE_NOME.match(a) or "(" in a:
        return "", [p for p in re.findall(r"[A-Za-zÀ-ÿ'’]{3,}", a) if p[:1].isupper()]
    parti = a.split(" ")
    if len(parti) > 4 or not all(p[:1].isupper() or p.lower() in PARTICELLE for p in parti):
        return "", [p for p in parti if len(p) >= 3 and p[:1].isupper()]
    nome = parti[0].capitalize() if parti[0].isupper() else parti[0]
    cognomi = [p for p in parti[1:] if len(p) >= 3 and p.lower() not in PARTICELLE]
    return nome, cognomi


def pulisci(testo: str, t: "Testimonianza") -> str:
    """Toglie dal testo email, telefoni, link, menzioni, codici emoji e i cognomi dell'allievo.
    Si tolgono solo pezzi: le parole che restano sono quelle originali."""
    s = testo or ""
    if t.allievo and s.lower().startswith(t.allievo.lower()):
        s = s[len(t.allievo):]
    for rx in (RE_EMAIL, RE_URL, RE_MENZIONE, RE_EMOJI_SLACK, RE_TEL):
        s = rx.sub(" ", s)
    for parola in t.vietati:
        s = re.sub(rf"(?<![\wÀ-ÿ]){re.escape(parola)}(?![\wÀ-ÿ])", " ", s, flags=re.I)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" ?\n ?", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r" +([,.;:!?])", r"\1", s)
    return s.strip(" \n-–:,")


def da_riga(r: dict) -> Testimonianza:
    g = lambda k: (r.get(k) or "").strip()
    nome, cognomi = _nome(g("Allievo"))
    try:
        forza = int(float(g("Forza (1-5)").replace(",", ".")))
    except ValueError:
        forza = 0
    t = Testimonianza(
        id=g("ID"), riga=r, data=leggi_data(g("Data"), g("ID")), allievo=re.sub(r"\s+", " ", g("Allievo")), nome=nome,
        cognomi=cognomi, tipo=g("Tipo"), percorso=g("Percorso"), evento=g("Evento / Contesto"), risultato=g("Risultato"),
        angolo=[a.strip() for a in re.split(r"\s/\s|,|;", g("Angolo narrativo")) if a.strip()], citazione=g("Citazione chiave"),
        uso=dividi(g("Uso consigliato")), testo=g("Testo completo"), stato=g("Stato"), obiezioni=dividi(g("Obiezione che smonta")),
        profilo=dividi(g("Profilo allievo")), momento=g("Momento funnel"), stagione=g("Stagione / aggancio"),
        formato_story=g("Formato story"), hook=g("Hook prima slide"), sticker=g("Sticker / CTA"), forza=forza,
        consenso=g("Consenso"), oscurare=g("Da oscurare"), ultimo_utilizzo=leggi_data(g("Ultimo utilizzo")))
    t.testo_pulito = pulisci(t.testo, t)
    return t


def carica(percorso: Path) -> list[Testimonianza]:
    with open(percorso, newline="", encoding="utf-8-sig") as f:
        righe = list(csv.DictReader(f))
    if not righe:
        raise ValueError("Il file testimonianze.csv è vuoto.")
    mancanti = [c for c in ("ID", "Stato", "Testo completo", "Consenso", "Allievo") if c not in righe[0]]
    if mancanti:
        raise ValueError(f"Nel foglio mancano le colonne: {', '.join(mancanti)}")
    return [da_riga(r) for r in righe if (r.get("ID") or "").strip()]
