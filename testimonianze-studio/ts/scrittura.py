"""Scrittura: prepara le istruzioni per Claude Code in modalità headless (claude -p) e ne legge la risposta.
Claude lavora senza strumenti: riceve solo il testo qui sotto e restituisce un JSON. Usa l'accesso dell'abbonamento
(le variabili delle chiavi API vengono tolte dall'ambiente del comando)."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import date

from .dati import Testimonianza
from .modelli import MODELLI

ORDINE = {"carosello": ["hook", "problema", "difficolta", "soluzione", "risultato", "sintesi", "cta"],
          "stories": ["identificazione", "difficolta", "soluzione", "risultato", "cta"]}
FACOLTATIVI = {"sintesi"}
NUMERO = {"carosello": (6, 9), "stories": (4, 6)}
LIMITI = {"carosello": dict(titolo=95, testo=300, citazione=240, prima=110, dopo=110, etichetta=26),
          "stories": dict(titolo=90, testo=200, citazione=200, prima=110, dopo=110, etichetta=26)}
# caratteri totali per slide/storia (titolo + testo + citazioni): oltre, il testo diventa troppo piccolo da leggere
SPAZIO = {"carosello": 400, "stories": 300}

SISTEMA = ("Sei il copywriter di Correre Naturale. Scrivi in italiano. Rispondi con un solo oggetto JSON valido, "
           "senza testo prima o dopo e senza blocchi di codice.")


def leggi_sticker(s: str, config: dict) -> dict:
    """«Sondaggio "Ti rivedi?" + DM DOLORI» → tipo, domanda, parola. Il «link RS» diventa invito in DM."""
    s = s or ""
    basso = s.lower()
    tipo = "sondaggio" if basso.startswith("sondaggio") else "slider" if basso.startswith("slider") else \
        "domanda" if basso.startswith("box domande") else "dm"
    dom = re.search(r"[\"“«](.+?)[\"”»]", s)
    par = re.search(r"\bDM\s+([A-ZÀ-Ü]{3,})", s)
    return dict(tipo=tipo, domanda=dom.group(1).strip() if dom else "", parola=par.group(1) if par else config["cta"]["parola_predefinita"])


def _hook_pulito(t: Testimonianza) -> str:
    h = re.sub(r"^[^:]{2,40}:\s*", "", t.hook) if t.nome and t.hook.lower().startswith(t.nome.lower()) else t.hook
    for p in t.vietati:
        h = re.sub(rf"(?<![\wÀ-ÿ]){re.escape(p)}(?![\wÀ-ÿ])", "", h, flags=re.I)
    return re.sub(r"\s+", " ", h).strip()


def scheda_candidato(t: Testimonianza, config: dict) -> dict:
    """Quello che Claude vede di una testimonianza: niente cognomi, email, link, telefoni."""
    from .controlli import normalizza
    cit = t.citazione if t.citazione and normalizza(t.citazione) in normalizza(t.testo_pulito) else ""
    return dict(id=t.id, nome=t.firma or "(anonimo: non scrivere nessun nome)", forza=t.forza, tipo=t.tipo, evento=t.evento,
                risultato=t.risultato, obiezioni=t.obiezioni, angolo=t.angolo, profilo=t.profilo,
                tema_salute=t.salute, hook_suggerito=_hook_pulito(t), citazione_suggerita=cit,
                sticker=leggi_sticker(t.sticker, config), in_stagione=bool(t.extra.get("stagione")),
                evento_vicino=t.extra.get("evento") or "", testo=t.testo_pulito[:3500])


def istruzioni(oggi: date, piano: dict, rosa: list[Testimonianza], modelli: list[str], config: dict) -> str:
    formato = piano["formato"]
    lim, (nmin, nmax) = LIMITI[formato], NUMERO[formato]
    parole = config["cta"]["parole_carosello"]
    if formato == "carosello":
        compito = (f"un CAROSELLO Instagram (1080×1350), da {nmin} a {nmax} slide, taglio «{piano['taglio']}»: "
                   f"{config['tagli'][piano['taglio']]}")
        struttura = (f"""- «elementi» = le slide, in quest'ordine di ruoli: hook → problema → difficolta → soluzione → risultato → (sintesi, facoltativa) → cta. Un ruolo può occupare più slide di fila.
- Slide 1 (hook): aggancia sul PROBLEMA in cui il lettore si riconosce. Se «hook_suggerito» c'è, usalo come base. Nessun invito all'azione qui.
- Slide 2: secondo gancio, fa venire voglia di continuare.
- Slide di sviluppo: un'idea per slide, 25-55 parole.
- Ultima slide (cta): una sola azione, commentare la parola chiave. «cta.parola» è una fra {', '.join(parole)} e deve comparire in maiuscolo nel «testo» dell'ultima slide. Al centro dell'offerta c'è il coaching personalizzato.
- «cta.tipo» = "dm"; «cta.sticker» = "".
- «caption»: didascalia del post, 600-1100 caratteri. Parte dal problema, completa il carosello senza ripeterlo, chiude con la stessa CTA e la parola chiave, poi 3-5 hashtag.""")
    else:
        compito = (f"un set di STORIES Instagram (1080×1920), da {nmin} a {nmax} storie (mai più di 6), leva «{piano['leva']}»: "
                   f"{config['leve'][piano['leva']]['descrizione']}")
        struttura = (f"""- «elementi» = le storie, in quest'ordine di ruoli: identificazione → difficolta → soluzione → risultato → cta. Le storie centrali possono essere 2-4; niente riempitivi.
- Storia 1 (identificazione): il problema, detto in modo che la persona si riconosca. Nessun invito all'azione qui.
- Ogni storia si legge in pochi secondi: frasi corte.
- Ultima storia (cta): usa lo «sticker» della testimonianza principale. «cta.tipo» = il suo tipo (sondaggio, slider, domanda, dm); «cta.sticker» = la sua domanda; «cta.parola» = la sua parola (oppure una fra {', '.join(parole)}). Il «titolo» dell'ultima storia è la domanda; il «testo» invita a scrivere in DM e finisce con i due punti (la parola compare sotto, grande).
- «caption»: 1-2 frasi di accompagnamento per chi pubblica (max 300 caratteri), con la CTA.""")
    mod = "\n".join(f"  {k + 1}. {m} («{MODELLI[m]['nome']}») — {MODELLI[m]['richiede']}" for k, m in enumerate(modelli))
    rosa_json = json.dumps([scheda_candidato(t, config) for t in rosa], ensure_ascii=False, indent=1)
    return f"""Oggi è {oggi.strftime('%d/%m/%Y')} ({piano['giorno']}). Devi scrivere {compito}

Il contenuto si costruisce SOLO sulle testimonianze degli allievi elencate in fondo (candidati).

# 1. Scegli le testimonianze
- STORIA SINGOLA (una testimonianza): quando il suo «testo» ha abbastanza dettagli (problema chiaro, cosa è cambiato, risultato concreto). È la scelta normale.
- STORIA UNITA (2-4 testimonianze): solo se nessuna basta da sola; devono condividere almeno una «obiezione» (o lo stesso «angolo»): es. dolori e infortuni, troppo vecchio, parto da zero, tempi fermi.
- Preferisci, nell'ordine: «evento_vicino», «in_stagione», forza più alta, testo più ricco. I candidati sono già in ordine di preferenza.

# 2. Storytelling (obbligatorio)
Problema → Difficoltà → Soluzione (il metodo e il coaching di Correre Naturale) → Risultato → CTA. Si parte sempre dal problema, mai dalla CTA.
{struttura}

# 3. Regole che non si possono violare
- Le CITAZIONI stanno solo nel campo «citazioni» e sono fedeli all'originale: copia le parole esatte dal «testo» del candidato. Puoi accorciare tagliando l'inizio, la fine o un pezzo in mezzo (segna il taglio con «…»), ma non cambiare, aggiungere o riordinare parole, e non correggere. Non mettere le virgolette: le aggiunge la grafica.
- Fuori dal campo «citazioni» non mettere frasi tra virgolette attribuite agli allievi.
- Tutto il racconto intorno lo scrivi tu, ma ogni FATTO (tempi, distanze, età, durate, gare, numeri) deve essere scritto nei campi del candidato. Non inventare niente. Se un dettaglio manca, resta sul generale.
- Usa il «nome» del candidato così com'è (è già quello consentito). Mai cognomi, email, telefoni, link, nomi di altre persone citate nei messaggi. Se il nome è «(anonimo…)» non scrivere nessun nome: «un nostro allievo», «un'allieva».
- SALUTE: se «tema_salute» è vero (neuropatia, diabete, malattie croniche…) raccontala solo come esperienza personale di quella persona, mai come promessa o risultato atteso per chi legge.
- In tutto il contenuto, citazioni comprese, non usare mai: guarisce/guarito/guarigione, cura/curare (in senso medico), risolve/risolto/risoluzione, garantito/garanzia.
- Non nominare la «Running School», la «Mentorship», né «tutor», «setter», «chatter», né sigle interne (CTE, RS, FS).
- Tono Correre Naturale: caldo, concreto, mai esagerato. Dai del tu. Nessuna colpa al lettore, niente frasi motivazionali vuote, niente superlativi, niente emoji, niente punti esclamativi a raffica.
- Nei titoli puoi evidenziare UNA parola o breve espressione con gli asterischi: *così*.

# 4. Modello grafico
Usa il primo modello di questa lista che è adatto al contenuto (i modelli «solo per storia unita» vanno usati solo con 2+ testimonianze):
{mod}

# 5. Lunghezze massime (caratteri)
titolo {lim['titolo']} · testo {lim['testo']} · ogni citazione {lim['citazione']} · prima/dopo {lim['prima']} · etichetta {lim['etichetta']}
In ogni elemento la somma di titolo + testo + citazioni non supera {SPAZIO[formato]} caratteri: se c'è una citazione, il testo intorno è breve. Conta i caratteri prima di rispondere.

# 6. Risposta
Un solo oggetto JSON con questa forma:
{{
 "storia": "singola" oppure "unita",
 "ids": ["id delle testimonianze usate"],
 "modello": "codice del modello scelto",
 "argomento": "tema in 2-4 parole",
 "motivo_scelta": "1-2 frasi: perché queste testimonianze oggi",
 "struttura": {{"problema": "...", "difficolta": "...", "soluzione": "...", "risultato": "...", "cta": "..."}},
 "elementi": [
  {{"ruolo": "...", "etichetta": "", "titolo": "...", "testo": "...", "citazioni": [{{"id": "...", "testo": "..."}}], "prima": "", "dopo": ""}}
 ],
 "cta": {{"parola": "...", "tipo": "...", "sticker": "..."}},
 "caption": "..."
}}
«struttura» riassume in una riga per voce il percorso problema → risultato (serve per la scheda interna). «etichetta» è facoltativa (se vuota la grafica mette il nome del ruolo). I campi non usati restano stringhe vuote o liste vuote.

# Candidati
{rosa_json}
"""


def correzione(errori: list[str]) -> str:
    return ("\n\n# ATTENZIONE: la tua risposta precedente è stata scartata dai controlli automatici\n"
            + "\n".join(f"- {e}" for e in errori)
            + "\nRiscrivi tutto il JSON correggendo questi punti. Per le citazioni copia le parole esatte dal testo del candidato.")


def estrai_json(testo: str) -> dict:
    testo = re.sub(r"^```(?:json)?|```$", "", testo.strip(), flags=re.M).strip()
    i, j = testo.find("{"), testo.rfind("}")
    if i < 0 or j <= i:
        raise ValueError("La risposta di Claude non contiene un JSON.")
    return json.loads(testo[i:j + 1])


def chiedi_a_claude(prompt: str, config: dict) -> dict:
    """Esegue `claude -p` senza strumenti e restituisce il JSON scritto da Claude."""
    cc = config["claude"]
    exe = shutil.which(cc.get("comando") or "claude")
    if not exe:
        raise FileNotFoundError("Comando «claude» non trovato: installa Claude Code ed esegui una volta «claude» per accedere con l'abbonamento.")
    env = dict(os.environ)
    for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):  # mai chiavi o crediti API: solo l'accesso dell'abbonamento
        env.pop(k, None)
    with tempfile.TemporaryDirectory() as tmp:  # cartella vuota: Claude non carica istruzioni o file di progetto
        with open(os.path.join(tmp, "sistema.txt"), "w", encoding="utf-8") as f:
            f.write(SISTEMA)
        cmd = [exe, "-p", "--output-format", "json", "--max-turns", "1", "--strict-mcp-config",
               "--system-prompt-file", os.path.join(tmp, "sistema.txt"), "--tools", ""]
        if cc.get("modello"):
            cmd += ["--model", cc["modello"]]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=cc.get("attesa_secondi", 600), cwd=tmp, env=env)
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError(f"Claude Code ha risposto con un errore: {(r.stderr or '').strip()[:400]}")
    try:
        busta = json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Risposta di Claude Code non leggibile: {r.stdout[:300]}")
    if isinstance(busta, list):  # alcune versioni restituiscono l'elenco degli eventi
        busta = next((b for b in reversed(busta) if isinstance(b, dict) and b.get("type") == "result"), {})
    if busta.get("is_error") or "result" not in busta:
        raise RuntimeError(f"Claude Code non ha completato la scrittura: {str(busta.get('result') or busta.get('subtype'))[:400]}")
    return estrai_json(busta["result"])
