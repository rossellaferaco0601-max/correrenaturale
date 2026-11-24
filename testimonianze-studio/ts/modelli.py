"""Modelli grafici dedicati alle testimonianze: 4 per i caroselli (1080×1350) e 4 per le stories (1080×1920).
Ogni modello riceve il contenuto già controllato e restituisce una lista di Tele.

Regola «testo mai sopra i volti»: nei modelli foto e testo occupano sempre zone separate della slide;
le foto usate sono solo quelle in assets/foto (nessun volto riconoscibile)."""
from __future__ import annotations

from .grafica import (AZZURRO, BIANCO, CREMA, NERO, RISORSE, VERDE, Tela, adatta, font, mescola)

CW, CH = 1080, 1350  # carosello 4:5
SW, SH = 1080, 1920  # storia 9:16
S_ALTO, S_BASSO = 280, 1470  # zona sicura delle stories (sopra e sotto c'è l'interfaccia di Instagram)
M = 84
LOGO = RISORSE / "logo"

ETICHETTE = {"problema": "Il problema", "difficolta": "La difficoltà", "soluzione": "Il metodo",
             "risultato": "Il risultato", "sintesi": "In breve", "cta": "E tu?"}

MODELLI = {
    "C-virgolette": dict(formato="carosello", nome="Virgolette", famiglia="virgolette",
                         richiede="La citazione è protagonista: almeno 2 elementi con una citazione; un elemento può avere solo la citazione (titolo e testo vuoti)."),
    "C-primadopo": dict(formato="carosello", nome="Prima / Dopo", famiglia="primadopo",
                        richiede="Esattamente un elemento (ruolo «risultato» o «soluzione») con i campi «prima» e «dopo» compilati (max 110 caratteri l'uno, fatti presi dalla testimonianza) e titolo/testo vuoti."),
    "C-percorso": dict(formato="carosello", nome="Il percorso", famiglia="percorso",
                       richiede="Ogni elemento è una tappa in ordine di tempo: titoli brevi che fanno avanzare la storia."),
    "C-voci": dict(formato="carosello", nome="Voci a confronto", famiglia="voci", solo_unita=True,
                   richiede="Solo per storia unita: ogni allievo ha almeno una citazione; un elemento può affiancare 2-3 citazioni brevi (max 150 caratteri l'una) di allievi diversi."),
    "S-messaggio": dict(formato="stories", nome="Messaggio", famiglia="messaggio",
                        richiede="Le citazioni compaiono come messaggi ricevuti; il campo «testo» è la risposta/commento di Correre Naturale (max 160 caratteri)."),
    "S-virgolette": dict(formato="stories", nome="Virgolette", famiglia="virgolette",
                         richiede="Una citazione grande per storia nelle storie centrali (max 180 caratteri)."),
    "S-tappe": dict(formato="stories", nome="Tappe", famiglia="percorso",
                    richiede="Ogni storia è una tappa in ordine di tempo, titoli brevi."),
    "S-voci": dict(formato="stories", nome="Voci a confronto", famiglia="voci", solo_unita=True,
                   richiede="Solo per storia unita: nelle storie centrali 1-2 citazioni brevi di allievi diversi (max 150 caratteri l'una)."),
    "C-schermo": dict(formato="carosello", nome="Schermata del messaggio", famiglia="schermo",
                      richiede="Le citazioni compaiono come schermate di messaggio. Il primo elemento (copertina) ha UNA citazione breve (max 150 caratteri) in cui l'allievo dice il problema; almeno altri 3 elementi hanno una citazione."),
    "S-schermo": dict(formato="stories", nome="Schermata del messaggio", famiglia="schermo",
                      richiede="Le citazioni compaiono come schermate di messaggio. La prima storia ha UNA citazione breve (max 140 caratteri) in cui l'allievo dice il problema; ogni storia centrale ha una citazione."),
}


# ── pezzi comuni ─────────────────────────────────────────────────────────────
def _virgolette(t: Tela, x, y, alt, colore):
    """Virgolette grandi: (x, y) è l'angolo in alto a sinistra del segno, alt la sua altezza."""
    l, tp, r, b = font("Black", 100).getbbox("“")
    dim = alt / (b - tp) * 100
    asc, desc = font("Black", dim).getmetrics()
    t.testo(round(x - l * dim / 100), round(y - tp * dim / 100 - (dim - asc - desc) / 2), round(dim), "“", dim, colore,
            peso="Black", inter=1)


def _piede_c(t: Tela, i, n, scuro, colore=None):
    """Piè di pagina del carosello: pittogramma, profilo e numero di slide."""
    col = colore or (BIANCO if scuro else NERO)
    t.immagine(LOGO / ("pittogramma-bianco.png" if scuro else "pittogramma-verde.png"), M, CH - 104, 34, copri=False)
    t.testo(M + 52, CH - 92, 400, "@correrenaturale", 28, col, peso="SemiBold")
    t.testo(CW - M - 200, CH - 92, 200, f"{i:02d} / {n:02d}", 28, col, peso="SemiBold", allinea="dx")


def _piede_s(t: Tela, scuro, colore=None, x=M):
    col = colore or (BIANCO if scuro else NERO)
    t.immagine(LOGO / ("pittogramma-bianco.png" if scuro else "pittogramma-verde.png"), x, S_BASSO + 22, 34, copri=False)
    t.testo(x + 52, S_BASSO + 34, 400, "@correrenaturale", 28, col, peso="SemiBold")


def _etichetta(el):
    return (el.get("etichetta") or ETICHETTE.get(el["ruolo"], "")).strip()


def _firma(c):
    return "— " + (c.get("firma") or "dai messaggi dei nostri allievi")


def _carta_citazione(t: Tela, s, x, y, w, c, sfondo, col, col_firma, dim=42, banda=None, bordo=None, raggio=34,
                     peso="SemiBold"):
    """Scheda con una citazione e la firma. Restituisce l'altezza."""
    pad = round(40 * s)
    rientro = 22 if banda else 0
    tw = w - pad * 2 - rientro
    q = "«" + c["testo"] + "»"
    h1 = t.misura(tw, q, dim * s, peso, 1.3)
    hf = round(32 * s * 1.2)
    H = pad * 2 + h1 + round(18 * s) + hf
    t.rett(x, y, w, H, sfondo, raggio=raggio, bordo=bordo, spessore=3 if bordo else 0)
    if banda:
        t.rett(x + 22, y + pad, 8, H - pad * 2, banda, raggio=4)
    t.testo(x + pad + rientro, y + pad, tw, q, dim * s, col, peso=peso, inter=1.3)
    t.testo(x + pad + rientro, y + pad + h1 + round(18 * s), tw, _firma(c), 32 * s, col_firma, peso="Bold")
    return H


def _avatar(t: Tela, x, y, d, c, sfondo=VERDE, col=BIANCO, bordo=None):
    """Cerchio con l'iniziale del nome (o le virgolette se la testimonianza è anonima)."""
    if bordo:
        t.cerchio(x - 6, y - 6, d + 12, bordo)
    t.cerchio(x, y, d, sfondo)
    lettera = (c.get("firma") or "").strip()[:1].upper()
    if lettera:
        dim = d * .56
        t.testo(x, round(y + (d - dim * 1.16) / 2), d, lettera, dim, col, peso="Black", allinea="centro")
    else:
        _virgolette(t, x + d * .3, y + d * .36, d * .28, col)


def _parola(t: Tela, y, parola, sfondo, col, dim=112, centro=CW // 2):
    return t.pillola(centro, y, parola, dim, sfondo, col, peso="Black", pad=(64, 22), traccia=6, centro=True)[1]


def _cta_storia(t: Tela, el, cta, fg, enf, pill_bg, pill_fg, zona, x=M, w=SW - 2 * M, alto=S_ALTO + 40, allinea="sx"):
    """Ultima storia: domanda, spazio pulito per lo sticker di Instagram, invito in DM con la parola chiave."""
    con_sticker = cta.get("tipo") in ("sondaggio", "domanda", "slider")

    def dis(tt, s, y):
        y += tt.testo(x, y, w, el.get("titolo", ""), 84 * s, fg, peso="Black", enfasi=enf, inter=1.06, allinea=allinea) + round(40 * s)
        if con_sticker:
            hz = round(400 * s)
            tt.rett(x, y, w, hz, zona, raggio=44)
            y += hz + round(48 * s)
        if el.get("testo"):
            y += tt.testo(x, y, w, el["testo"], 46 * s, fg, peso="SemiBold", inter=1.25, allinea=allinea) + round(36 * s)
        if cta.get("parola"):
            cx = x + w // 2 if allinea == "centro" else None
            if cx:
                y += _parola(tt, y, cta["parola"], pill_bg, pill_fg, dim=104 * s, centro=cx)
            else:
                y += tt.pillola(x, y, cta["parola"], 104 * s, pill_bg, pill_fg, peso="Black", pad=(60, 20), traccia=6)[1]
        return y

    adatta(t, dis, alto, S_BASSO - 30, centra=True)


# ═════════════════════════════ CAROSELLI ════════════════════════════════════
def c_virgolette(con, ctx):
    els, n, out = con["elementi"], len(con["elementi"]), []
    for i, el in enumerate(els, 1):
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        if ruolo == "hook":
            t = Tela(CW, CH, CREMA)
            _virgolette(t, M, 110, 190, VERDE)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 104 * s, NERO, peso="Black", enfasi=VERDE, inter=1.04) + round(36 * s)
                if el.get("testo"):
                    tt.rett(M, y, 120, 8, VERDE, raggio=4)
                    y += round(44 * s)
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 46 * s, NERO, inter=1.3)
                return y

            adatta(t, dis, 380, 1090, centra=True)
            t.pillola(M, 1120, "Scorri  →", 30, VERDE, BIANCO, maiuscolo=True, traccia=3)
            _piede_c(t, i, n, False)
        elif ruolo == "cta":
            t = Tela(CW, CH, NERO)
            _virgolette(t, M, 110, 120, VERDE)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 80 * s, BIANCO, peso="Black", enfasi=AZZURRO, inter=1.08) + round(34 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, CREMA, inter=1.3) + round(50 * s)
                y += tt.pillola(M, y, con["cta"]["parola"], 112 * s, VERDE, BIANCO, peso="Black", pad=(64, 22), traccia=6)[1]
                return y

            adatta(t, dis, 290, 1170, centra=True)
            _piede_c(t, i, n, True)
        elif cit and not el.get("testo") and not el.get("titolo"):
            t = Tela(CW, CH, VERDE)
            _virgolette(t, M, 130, 170, AZZURRO)
            if _etichetta(el):
                t.testo(CW - M - 500, 150, 500, _etichetta(el), 30, CREMA, peso="SemiBold", traccia=3, maiuscolo=True, allinea="dx")

            def dis(tt, s, y, c=cit[0]):
                y += tt.testo(M, y, CW - 2 * M, c["testo"], 70 * s, BIANCO, peso="Bold", inter=1.2) + round(44 * s)
                tt.rett(M, y, 90, 6, AZZURRO, raggio=3)
                y += round(30 * s)
                y += tt.testo(M, y, CW - 2 * M, _firma(c), 38 * s, CREMA, peso="SemiBold")
                return y

            adatta(t, dis, 380, 1170, centra=True)
            _piede_c(t, i, n, True)
        else:
            t = Tela(CW, CH, CREMA)
            _virgolette(t, M, 104, 56, VERDE)
            t.testo(M + 110, 112, 700, _etichetta(el), 30, VERDE, peso="Bold", traccia=3, maiuscolo=True)

            def dis(tt, s, y, el=el, cit=cit):
                if el.get("titolo"):
                    y += tt.testo(M, y, CW - 2 * M, el["titolo"], 74 * s, NERO, peso="Bold", enfasi=VERDE, inter=1.1) + round(30 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, NERO, inter=1.32) + round(44 * s)
                for c in cit:
                    y += _carta_citazione(tt, s, M, y, CW - 2 * M, c, VERDE, BIANCO, CREMA) + round(24 * s)
                return y

            adatta(t, dis, 250, 1190, centra=True)
            _piede_c(t, i, n, False)
        out.append(t)
    return out


def c_primadopo(con, ctx):
    els, n, out = con["elementi"], len(con["elementi"]), []
    dopo_da = next((k for k, e in enumerate(els) if e["ruolo"] in ("soluzione", "risultato") or e.get("dopo")), n - 1)

    def banda(t, i, fg, punto):
        """PRIMA ────●──── DOPO: il punto avanza a ogni slide."""
        t.testo(M, 96, 160, "PRIMA", 30, fg, peso="Bold", traccia=4)
        t.testo(CW - M - 160, 96, 160, "DOPO", 30, fg, peso="Bold", traccia=4, allinea="dx")
        x0, x1 = M + 150, CW - M - 140
        t.rett(x0, 110, x1 - x0, 6, mescola(t.sfondo, fg, .35), raggio=3)
        px = x0 + (x1 - x0 - 34) * (i - 1) / max(1, n - 1)
        t.cerchio(round(px), 96, 34, punto)

    for i, el in enumerate(els, 1):
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        dopo = i - 1 >= dopo_da
        if el.get("prima") and el.get("dopo"):
            t = Tela(CW, CH, NERO)
            t.rett(0, CH // 2, CW, CH - CH // 2, VERDE)
            for testo, y0, pill_bg, pill_fg, nome in ((el["prima"], 0, CREMA, NERO, "Prima"), (el["dopo"], CH // 2, CREMA, VERDE, "Dopo")):
                def dis(tt, s, y, testo=testo, pill_bg=pill_bg, pill_fg=pill_fg, nome=nome):
                    y += tt.pillola(M, y, nome, 32 * s, pill_bg, pill_fg, traccia=4)[1] + round(34 * s)
                    y += tt.testo(M, y, CW - 2 * M, testo, 66 * s, BIANCO, peso="Bold", inter=1.14)
                    return y
                adatta(t, dis, y0 + 110, y0 + CH // 2 - (90 if y0 == 0 else 150), centra=True)
            t.cerchio(CW // 2 - 60, CH // 2 - 60, 120, BIANCO)
            t.freccia(CW // 2 - 26, CH // 2 - 32, 52, 64, "giu", VERDE)
            _piede_c(t, i, n, True)
        elif ruolo == "hook":
            t = Tela(CW, CH, NERO)
            banda(t, i, BIANCO, VERDE)
            t.rett(0, 990, CW, CH - 990, VERDE)

            def dis(tt, s, y, el=el):
                return y + tt.testo(M, y, CW - 2 * M, el["titolo"], 104 * s, BIANCO, peso="Black", enfasi=AZZURRO, inter=1.04)

            adatta(t, dis, 230, 930, centra=True)

            def dis2(tt, s, y, el=el):
                return y + tt.testo(M, y, CW - 2 * M, el.get("testo") or "Scorri: ti racconto com'è andata.", 44 * s, BIANCO, peso="SemiBold", inter=1.28)

            adatta(t, dis2, 1030, 1210, centra=True)
            _piede_c(t, i, n, True)
        elif ruolo == "cta":
            t = Tela(CW, CH, VERDE)
            banda(t, i, BIANCO, AZZURRO)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 80 * s, BIANCO, peso="Black", enfasi=AZZURRO, inter=1.08) + round(34 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, CREMA, inter=1.3) + round(50 * s)
                y += tt.pillola(M, y, con["cta"]["parola"], 112 * s, CREMA, VERDE, peso="Black", pad=(64, 22), traccia=6)[1]
                return y

            adatta(t, dis, 230, 1170, centra=True)
            _piede_c(t, i, n, True)
        else:
            bg, fg, acc = (VERDE, BIANCO, AZZURRO) if dopo else (NERO, BIANCO, VERDE)
            t = Tela(CW, CH, bg)
            banda(t, i, BIANCO, AZZURRO if dopo else VERDE)

            def dis(tt, s, y, el=el, cit=cit, fg=fg, acc=acc, dopo=dopo):
                y += tt.pillola(M, y, _etichetta(el), 28 * s, CREMA if dopo else VERDE, VERDE if dopo else BIANCO, traccia=3)[1] + round(36 * s)
                if el.get("titolo"):
                    y += tt.testo(M, y, CW - 2 * M, el["titolo"], 74 * s, fg, peso="Bold", enfasi=AZZURRO if dopo else None, inter=1.1) + round(30 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, CREMA, inter=1.32) + round(44 * s)
                for c in cit:
                    y += _carta_citazione(tt, s, M, y, CW - 2 * M, c, None, BIANCO, AZZURRO if dopo else CREMA, bordo=AZZURRO if dopo else mescola(NERO, BIANCO, .4)) + round(24 * s)
                return y

            adatta(t, dis, 220, 1190, centra=True)
            _piede_c(t, i, n, True)
        out.append(t)
    return out


def c_percorso(con, ctx):
    els, n, out = con["elementi"], len(con["elementi"]), []
    LY = 236  # altezza della linea del percorso: uguale su tutte le slide, così scorrendo è continua
    tenue = mescola(CREMA, VERDE, .35)
    for i, el in enumerate(els, 1):
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        t = Tela(CW, CH, CREMA)
        ultima = ruolo == "cta"
        t.rett(0, LY - 4, 150 if ultima else CW, 8, VERDE)
        for k in range(1, 10):
            x = k * 108
            if x > 230 and not ultima:
                t.rett(x - 2, LY + 14, 4, 18, tenue)
        if ultima:
            t.cerchio(150 - 66, LY - 66, 132, CREMA, bordo=VERDE, spessore=8)
            t.cerchio(150 - 42, LY - 42, 84, VERDE)
        else:
            t.cerchio(150 - 56, LY - 56, 112, VERDE)
            t.testo(150 - 56, LY - 35, 112, str(i), 60, BIANCO, peso="Black", allinea="centro")
        nome = "Partenza" if ruolo == "hook" else "Arrivo" if ultima else f"Tappa {i} · {_etichetta(el)}"
        t.testo(236, LY - 70, 760, nome, 30, VERDE, peso="Bold", traccia=3, maiuscolo=True)
        if ruolo == "hook":
            foto = ctx.get("foto")
            basso = 800 if foto else 1190

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 92 * s, NERO, peso="Black", enfasi=VERDE, inter=1.05) + round(28 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, NERO, inter=1.3)
                return y

            adatta(t, dis, 340, basso, centra=not foto)
            if foto:
                t.immagine(foto, M, 840, CW - 2 * M, 350, raggio=36)
        elif ultima:
            def dis(tt, s, y, el=el):
                return y + tt.testo(M, y, CW - 2 * M, el["titolo"], 80 * s, NERO, peso="Black", enfasi=VERDE, inter=1.08)

            adatta(t, dis, 350, 700, centra=True)
            t.rett(M, 740, CW - 2 * M, 450, VERDE, raggio=44)

            def dis2(tt, s, y, el=el):
                if el.get("testo"):
                    y += tt.testo(M + 50, y, CW - 2 * M - 100, el["testo"], 42 * s, BIANCO, peso="SemiBold", inter=1.28) + round(34 * s)
                y += tt.pillola(M + 50, y, con["cta"]["parola"], 100 * s, CREMA, VERDE, peso="Black", pad=(56, 18), traccia=6)[1]
                return y

            adatta(t, dis2, 780, 1150, centra=True)
        else:
            def dis(tt, s, y, el=el, cit=cit):
                if el.get("titolo"):
                    y += tt.testo(M, y, CW - 2 * M, el["titolo"], 74 * s, NERO, peso="Bold", enfasi=VERDE, inter=1.1) + round(30 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, NERO, inter=1.32) + round(44 * s)
                for c in cit:
                    y += _carta_citazione(tt, s, M, y, CW - 2 * M, c, BIANCO, NERO, VERDE, banda=AZZURRO) + round(24 * s)
                return y

            adatta(t, dis, 350, 1190, centra=True)
        _piede_c(t, i, n, False)
        out.append(t)
    return out


def _voci_uniche(con):
    viste, out = set(), []
    for el in con["elementi"]:
        for c in el.get("citazioni") or []:
            if c["id"] not in viste:
                viste.add(c["id"])
                out.append(c)
    return out


def _carta_voce(t: Tela, s, x, y, w, c, grande=True):
    """Scheda bianca con iniziale, nome e citazione."""
    pad = round((44 if grande else 34) * s)
    d = round((104 if grande else 80) * s)
    dim = (46 if grande else 38) * s
    tw = w - pad * 2
    q = "«" + c["testo"] + "»"
    hq = t.misura(tw, q, dim, "Regular", 1.32)
    H = pad * 2 + d + round(28 * s) + hq
    t.rett(x, y, w, H, BIANCO, raggio=40)
    _avatar(t, x + pad, y + pad, d, c)
    nome = c.get("firma") or "Dai nostri messaggi"
    t.testo(x + pad + d + round(26 * s), round(y + pad + d / 2 - (40 if grande else 34) * s * .58), tw - d - 30, nome,
            (40 if grande else 34) * s, NERO, peso="Bold")
    t.testo(x + pad, y + pad + d + round(28 * s), tw, q, dim, NERO, inter=1.32)
    return H


def c_voci(con, ctx):
    els, n, out = con["elementi"], len(con["elementi"]), []
    voci = _voci_uniche(con)
    for i, el in enumerate(els, 1):
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        if ruolo == "hook":
            t = Tela(CW, CH, AZZURRO)
            t.pillola(M, 130, f"{len(voci)} voci a confronto", 30, BIANCO, VERDE, traccia=3)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 98 * s, NERO, peso="Black", enfasi=VERDE, inter=1.05) + round(34 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, NERO, inter=1.3)
                return y

            adatta(t, dis, 250, 930, centra=True)
            for k, c in enumerate(voci[:4]):
                _avatar(t, M + k * 118, 980, 150, c, bordo=AZZURRO)
            nomi = ", ".join(c.get("firma") or "…" for c in voci[:4])
            t.testo(M, 1152, CW - 2 * M, nomi, 34, NERO, peso="SemiBold")
            _piede_c(t, i, n, False)
        elif ruolo == "cta":
            t = Tela(CW, CH, VERDE)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 80 * s, BIANCO, peso="Black", enfasi=AZZURRO, inter=1.08) + round(34 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, CREMA, inter=1.3) + round(50 * s)
                y += tt.pillola(M, y, con["cta"]["parola"], 112 * s, BIANCO, VERDE, peso="Black", pad=(64, 22), traccia=6)[1]
                return y

            adatta(t, dis, 150, 1170, centra=True)
            _piede_c(t, i, n, True)
        else:
            t = Tela(CW, CH, AZZURRO)
            t.pillola(M, 110, _etichetta(el), 28, VERDE, BIANCO, traccia=3)

            def dis(tt, s, y, el=el, cit=cit):
                if el.get("titolo"):
                    y += tt.testo(M, y, CW - 2 * M, el["titolo"], 66 * s, NERO, peso="Bold", enfasi=VERDE, inter=1.1) + round(32 * s)
                for c in cit:
                    y += _carta_voce(tt, s, M - 14, y, CW - 2 * M + 28, c, grande=len(cit) == 1) + round(24 * s)
                if el.get("testo"):
                    y += round(12 * s)
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 42 * s, NERO, inter=1.32)
                return y

            adatta(t, dis, 215, 1200, centra=True)
            _piede_c(t, i, n, False)
        out.append(t)
    return out


# ═════════════════════════════ STORIES ══════════════════════════════════════
def _fumetto(t: Tela, s, x, y, w, testo, sfondo, col, dim=46, peso="Regular", lato="sx", nome=None, col_nome=VERDE):
    """Nuvoletta di messaggio in stile brand (non imita nessuna app). Restituisce l'altezza."""
    pad, r = round(38 * s), 44
    hn = 0
    if nome:
        hn = t.testo(x + 8, y, w, nome, 32 * s, col_nome, peso="Bold") + round(12 * s)
    ht = t.misura(w - pad * 2, testo, dim * s, peso, 1.3)
    H = ht + pad * 2
    t.rett(x, y + hn, w, H, sfondo, raggio=r)
    t.rett(x if lato == "sx" else x + w - r, y + hn + H - r, r, r, sfondo)  # un angolo vivo: la «coda» del messaggio
    t.testo(x + pad, y + hn + pad, w - pad * 2, testo, dim * s, col, peso=peso, inter=1.3)
    return hn + H


def s_messaggio(con, ctx):
    els, out = con["elementi"], []
    W = SW - 2 * M
    for el in els:
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        t = Tela(SW, SH, CREMA)
        if ruolo == "cta":
            _cta_storia(t, el, con["cta"], NERO, VERDE, VERDE, BIANCO, BIANCO)
        else:
            def dis(tt, s, y, el=el, cit=cit, ruolo=ruolo):
                if _etichetta(el) and ruolo != "identificazione":
                    y += tt.testo(M, y, W, _etichetta(el), 30 * s, VERDE, peso="Bold", traccia=3, maiuscolo=True) + round(22 * s)
                if el.get("titolo"):
                    grande = ruolo == "identificazione"
                    y += tt.testo(M, y, W, el["titolo"], (92 if grande else 66) * s, NERO, peso="Black" if grande else "Bold",
                                  enfasi=VERDE, inter=1.07) + round(48 * s)
                for c in cit:
                    y += _fumetto(tt, s, M, y, W - 120, "«" + c["testo"] + "»", BIANCO, NERO, nome=c.get("firma") or "Un messaggio ricevuto") + round(34 * s)
                if el.get("testo"):
                    y += _fumetto(tt, s, M + 120, y, W - 120, el["testo"], VERDE, BIANCO, peso="SemiBold", lato="dx",
                                  nome="Correre Naturale" if cit else None, dim=44)
                return y

            adatta(t, dis, S_ALTO, S_BASSO - 30, centra=True)
        _piede_s(t, False)
        out.append(t)
    return out


def s_virgolette(con, ctx):
    els, out = con["elementi"], []
    W = SW - 2 * M
    for el in els:
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        if ruolo == "cta":
            t = Tela(SW, SH, NERO)
            _cta_storia(t, el, con["cta"], BIANCO, AZZURRO, VERDE, BIANCO, mescola(NERO, BIANCO, .12))
            _piede_s(t, True)
        elif ruolo == "identificazione":
            t = Tela(SW, SH, VERDE)
            _virgolette(t, M, S_ALTO, 150, AZZURRO)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, W, el["titolo"], 100 * s, BIANCO, peso="Black", enfasi=AZZURRO, inter=1.05) + round(40 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, W, el["testo"], 48 * s, CREMA, inter=1.3)
                return y

            adatta(t, dis, S_ALTO + 210, S_BASSO - 30, centra=True)
            _piede_s(t, True)
        else:
            scuro = ruolo == "risultato"
            bg, fg, acc = (VERDE, BIANCO, AZZURRO) if scuro else (CREMA, NERO, VERDE)
            t = Tela(SW, SH, bg)
            _virgolette(t, M, S_ALTO, 110, acc)
            t.testo(SW - M - 560, S_ALTO + 30, 560, _etichetta(el), 30, CREMA if scuro else VERDE, peso="Bold", traccia=3, maiuscolo=True, allinea="dx")

            def dis(tt, s, y, el=el, cit=cit, fg=fg, acc=acc, scuro=scuro):
                for c in cit[:1]:
                    y += tt.testo(M, y, W, c["testo"], 66 * s, fg, peso="Bold", inter=1.2) + round(30 * s)
                    y += tt.testo(M, y, W, _firma(c), 36 * s, CREMA if scuro else VERDE, peso="Bold") + round(56 * s)
                    tt.rett(M, y - round(28 * s), W, 4, mescola(tt.sfondo, fg, .25))
                    y += round(16 * s)
                if el.get("titolo"):
                    y += tt.testo(M, y, W, el["titolo"], (60 if cit else 84) * s, fg, peso="Bold", enfasi=acc, inter=1.1) + round(24 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, W, el["testo"], 44 * s, CREMA if scuro else NERO, inter=1.32)
                return y

            adatta(t, dis, S_ALTO + 170, S_BASSO - 30, centra=True)
            _piede_s(t, scuro)
        out.append(t)
    return out


def s_tappe(con, ctx):
    els, n, out = con["elementi"], len(con["elementi"]), []
    LX, MY = 122, 400  # la linea verticale sta nello stesso punto in ogni storia
    X0 = 226
    W = SW - X0 - M
    for i, el in enumerate(els, 1):
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        t = Tela(SW, SH, CREMA)
        ultima = ruolo == "cta"
        t.rett(LX - 4, 0, 8, MY if ultima else SH, VERDE)
        if ultima:
            t.cerchio(LX - 62, MY - 62, 124, CREMA, bordo=VERDE, spessore=8)
            t.cerchio(LX - 40, MY - 40, 80, VERDE)
        else:
            t.cerchio(LX - 54, MY - 54, 108, VERDE)
            t.testo(LX - 54, MY - 34, 108, str(i), 58, BIANCO, peso="Black", allinea="centro")
        nome = "Partenza" if i == 1 else "Arrivo" if ultima else f"Tappa {i} · {_etichetta(el)}"
        t.testo(X0, MY - 20, W, nome, 30, VERDE, peso="Bold", traccia=3, maiuscolo=True)
        if ultima:
            _cta_storia(t, el, con["cta"], NERO, VERDE, VERDE, BIANCO, BIANCO, x=X0, w=W, alto=MY + 90)
        else:
            foto = ctx.get("foto") if i == 1 else None
            basso = S_BASSO - 30 - (440 if foto else 0)

            def dis(tt, s, y, el=el, cit=cit, i=i):
                if el.get("titolo"):
                    y += tt.testo(X0, y, W, el["titolo"], (84 if i == 1 else 68) * s, NERO, peso="Black" if i == 1 else "Bold", enfasi=VERDE, inter=1.08) + round(30 * s)
                if el.get("testo"):
                    y += tt.testo(X0, y, W, el["testo"], 44 * s, NERO, inter=1.32) + round(40 * s)
                for c in cit:
                    y += _carta_citazione(tt, s, X0, y, W, c, BIANCO, NERO, VERDE, banda=AZZURRO, dim=42) + round(24 * s)
                return y

            adatta(t, dis, MY + 100, basso, centra=not foto)
            if foto:
                t.immagine(foto, X0, S_BASSO - 30 - 400, W, 400, raggio=36)
        _piede_s(t, False, x=X0)
        out.append(t)
    return out


def s_voci(con, ctx):
    els, out = con["elementi"], []
    voci = _voci_uniche(con)
    W = SW - 2 * M
    for el in els:
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        if ruolo == "cta":
            t = Tela(SW, SH, VERDE)
            _cta_storia(t, el, con["cta"], BIANCO, AZZURRO, BIANCO, VERDE, mescola(VERDE, BIANCO, .14))
            _piede_s(t, True)
        else:
            t = Tela(SW, SH, AZZURRO)

            def dis(tt, s, y, el=el, cit=cit, ruolo=ruolo):
                ident = ruolo == "identificazione"
                lab = f"{len(voci)} voci a confronto" if ident else _etichetta(el)
                if lab:
                    y += tt.pillola(M, y, lab, 28 * s, BIANCO if ident else VERDE, VERDE if ident else BIANCO, traccia=3)[1] + round(34 * s)
                if el.get("titolo"):
                    y += tt.testo(M, y, W, el["titolo"], (94 if ident else 64) * s, NERO, peso="Black" if ident else "Bold", enfasi=VERDE, inter=1.07) + round(40 * s)
                if ident and voci:
                    d = round(140 * s)
                    for k, c in enumerate(voci[:4]):
                        _avatar(tt, M + k * round(110 * s), y, d, c, bordo=AZZURRO)
                    y += d + round(40 * s)
                for c in cit:
                    y += _carta_voce(tt, s, M - 14, y, W + 28, c, grande=len(cit) == 1) + round(26 * s)
                if el.get("testo"):
                    y += round(10 * s)
                    y += tt.testo(M, y, W, el["testo"], 46 * s, NERO, peso="SemiBold" if ident else "Regular", inter=1.3)
                return y

            adatta(t, dis, S_ALTO, S_BASSO - 30, centra=True)
            _piede_s(t, False)
        out.append(t)
    return out


# ═══════════════ SCHERMATA DEL MESSAGGIO (ricostruita dal testo) ════════════
# Le parole sono quelle esatte dell'allievo, ma l'immagine è composta qui in stile brand: non è lo screenshot originale
# e non imita nessuna app. Il titolo di copertina dice il problema; sotto spunta il messaggio di chi l'ha vissuto.
TEMI_SCHERMO = [
    dict(cop=NERO, tit=BIANCO, enf=AZZURRO, pill=(VERDE, BIANCO), cta=NERO, cta_enf=AZZURRO, cta_pill=(VERDE, BIANCO)),
    dict(cop=VERDE, tit=BIANCO, enf=AZZURRO, pill=(CREMA, VERDE), cta=VERDE, cta_enf=AZZURRO, cta_pill=(CREMA, VERDE)),
    dict(cop=CREMA, tit=NERO, enf=VERDE, pill=(VERDE, BIANCO), cta=VERDE, cta_enf=AZZURRO, cta_pill=(CREMA, VERDE)),
    dict(cop=AZZURRO, tit=NERO, enf=VERDE, pill=(BIANCO, VERDE), cta=NERO, cta_enf=AZZURRO, cta_pill=(VERDE, BIANCO)),
]
ORIGINI = (("recension", "dalla sua recensione"), ("lettera", "dalla sua lettera"), ("commento", "dal suo commento"),
           ("post", "dal suo post"))


def origine(tipo: str) -> str:
    return next((v for k, v in ORIGINI if (tipo or "").lower().startswith(k)), "dal suo messaggio")


def _schermo(t: Tela, s, x, y, w, cit: list, dim=40, pannello=BIANCO, bolla=CREMA):
    """Finestra di messaggio: intestazione con iniziale e nome, poi una nuvoletta per citazione. Restituisce l'altezza."""
    c0 = cit[0]
    pad, d = round(34 * s), round(72 * s)
    testa = pad + d + round(26 * s)
    tw = w - pad * 2 - round(28 * s) * 2
    alt = [t.misura(tw, c["testo"], dim * s, "Regular", 1.3) + round(28 * s) * 2 for c in cit]
    H = testa + sum(alt) + round(16 * s) * (len(cit) - 1) + pad
    t.rett(x, y, w, H, pannello, raggio=44)
    _avatar(t, x + pad, y + pad, d, c0)
    t.testo(x + pad + d + round(22 * s), y + pad + round(2 * s), w - pad * 2 - d - 30, c0.get("firma") or "Un nostro allievo", 34 * s, NERO, peso="Bold")
    t.testo(x + pad + d + round(22 * s), y + pad + round(42 * s), w - pad * 2 - d - 30, c0.get("origine") or "dal suo messaggio", 25 * s, mescola(NERO, BIANCO, .45))
    yy = y + testa
    for c, h in zip(cit, alt):
        t.rett(x + pad, yy, w - pad * 2, h, bolla, raggio=30)
        t.rett(x + pad, yy + h - 30, 30, 30, bolla)   # angolo vivo: la «coda» del messaggio
        t.testo(x + pad + round(28 * s), yy + round(28 * s), tw, c["testo"], dim * s, NERO, inter=1.3)
        yy += h + round(16 * s)
    return H


def _gruppi(cit: list) -> list[list]:
    """Citazioni consecutive della stessa persona stanno nella stessa finestra."""
    out = []
    for c in cit:
        if out and out[-1][0]["id"] == c["id"]:
            out[-1].append(c)
        else:
            out.append([c])
    return out


def _tema_schermo(con, ctx):
    k = ctx.get("tema")
    if k is None:
        k = sum(ord(ch) for ch in "".join(con.get("ids") or ["x"]))
    return TEMI_SCHERMO[k % len(TEMI_SCHERMO)]


def c_schermo(con, ctx):
    els, n, out = con["elementi"], len(con["elementi"]), []
    T = _tema_schermo(con, ctx)
    for i, el in enumerate(els, 1):
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        if ruolo == "hook":
            t = Tela(CW, CH, T["cop"])
            scuro = T["cop"] in (NERO, VERDE)
            t.pillola(M, 100, _etichetta(el) or "Ti succede?", 28, *T["pill"], traccia=3)

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 96 * s, T["tit"], peso="Black", enfasi=T["enf"], inter=1.05)
                if el.get("testo"):
                    y += round(26 * s) + tt.testo(M, y + round(26 * s), CW - 2 * M, el["testo"], 42 * s, T["tit"], inter=1.28)
                return y

            y = adatta(t, dis, 196, 720 if cit else 1150, scale=[1.4, 1.3, 1.2, 1.1, 1, .93, .86, .8, .74, .68, .62, .56, .5])
            if cit:
                # la schermata spunta dal fondo della copertina: il resto del messaggio è nelle slide dopo
                # la schermata sta tutta sotto il titolo, intera: si riduce finché entra
                for ss in (1.25, 1.15, 1.05, .96, .88, .8, .72):
                    hs = _schermo(t.vuota(), ss, 0, 0, CW - 2 * M + 40, cit[:1], dim=42)
                    if y + 50 + hs <= CH - 150:
                        break
                _schermo(t, ss, M - 20, max(y + 50, CH - 150 - hs), CW - 2 * M + 40, cit[:1], dim=42)
            _piede_c(t, i, n, scuro)
        elif ruolo == "cta":
            t = Tela(CW, CH, T["cta"])

            def dis(tt, s, y, el=el):
                y += tt.testo(M, y, CW - 2 * M, el["titolo"], 80 * s, BIANCO, peso="Black", enfasi=T["cta_enf"], inter=1.08) + round(34 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, CREMA, inter=1.3) + round(50 * s)
                y += tt.pillola(M, y, con["cta"]["parola"], 112 * s, *T["cta_pill"], peso="Black", pad=(64, 22), traccia=6)[1]
                return y

            adatta(t, dis, 150, 1170, centra=True)
            _piede_c(t, i, n, True)
        elif cit and not el.get("titolo") and not el.get("testo"):
            t = Tela(CW, CH, VERDE)
            t.pillola(M, 100, _etichetta(el), 28, CREMA, VERDE, traccia=3)

            def dis(tt, s, y, cit=cit):
                for g in _gruppi(cit):
                    y += _schermo(tt, s, M - 20, y, CW - 2 * M + 40, g, dim=50) + round(26 * s)
                return y

            adatta(t, dis, 200, 1190, centra=True)
            _piede_c(t, i, n, True)
        else:
            t = Tela(CW, CH, CREMA)
            t.pillola(M, 100, _etichetta(el), 28, VERDE, BIANCO, traccia=3)

            def dis(tt, s, y, el=el, cit=cit):
                if el.get("titolo"):
                    y += tt.testo(M, y, CW - 2 * M, el["titolo"], 72 * s, NERO, peso="Bold", enfasi=VERDE, inter=1.1) + round(28 * s)
                if el.get("testo"):
                    y += tt.testo(M, y, CW - 2 * M, el["testo"], 44 * s, NERO, inter=1.32) + round(40 * s)
                for g in _gruppi(cit):
                    y += _schermo(tt, s, M - 20, y, CW - 2 * M + 40, g, dim=42) + round(24 * s)
                return y

            adatta(t, dis, 200, 1195, centra=True)
            _piede_c(t, i, n, False)
        out.append(t)
    return out


def s_schermo(con, ctx):
    els, out = con["elementi"], []
    T = _tema_schermo(con, ctx)
    W = SW - 2 * M
    for el in els:
        ruolo, cit = el["ruolo"], el.get("citazioni") or []
        if ruolo == "cta":
            t = Tela(SW, SH, T["cta"])
            _cta_storia(t, el, con["cta"], BIANCO, T["cta_enf"], *T["cta_pill"], mescola(T["cta"], BIANCO, .14))
            _piede_s(t, True)
        else:
            ident = ruolo == "identificazione"
            bg = T["cop"] if ident else CREMA
            scuro = bg in (NERO, VERDE)
            fg, enf = (T["tit"], T["enf"]) if ident else (NERO, VERDE)
            t = Tela(SW, SH, bg)

            def dis(tt, s, y, el=el, cit=cit, ident=ident, fg=fg, enf=enf):
                lab = (_etichetta(el) or "Ti succede?") if ident else _etichetta(el)
                if lab:
                    y += tt.pillola(M, y, lab, 28 * s, *(T["pill"] if ident else (VERDE, BIANCO)), traccia=3)[1] + round(36 * s)
                if el.get("titolo"):
                    y += tt.testo(M, y, W, el["titolo"], (96 if ident else 66) * s, fg, peso="Black" if ident else "Bold", enfasi=enf, inter=1.06) + round(36 * s)
                if el.get("testo") and ident:
                    y += tt.testo(M, y, W, el["testo"], 44 * s, fg, inter=1.3) + round(40 * s)
                for g in _gruppi(cit):
                    y += _schermo(tt, s, M - 20, y, W + 40, g, dim=46) + round(26 * s)
                if el.get("testo") and not ident:
                    y += round(10 * s) + tt.testo(M, y + round(10 * s), W, el["testo"], 44 * s, fg, inter=1.32)
                return y

            adatta(t, dis, S_ALTO, S_BASSO - 30, centra=True)
            _piede_s(t, scuro)
        out.append(t)
    return out


# ═══════════════ IN PROVA: schermata originale del messaggio ════════════════
# Non sono ancora nella rotazione quotidiana: servono gli allegati (cartella Drive) e la copertura di nomi e numeri.
MODELLI_IN_PROVA = {
    "C-schermata": dict(formato="carosello", nome="Schermata originale", famiglia="schermata"),
    "S-schermata": dict(formato="stories", nome="Schermata originale", famiglia="schermata"),
}


def _schermata(ctx, con):
    """Immagine (già coperta) della prima testimonianza usata."""
    return (ctx.get("schermate") or {}).get((con.get("ids") or [""])[0])


def c_schermata(con, ctx):
    """Slide 1: il messaggio vero, grande, sotto il titolo. Le altre slide seguono il modello Virgolette."""
    out = c_virgolette(con, ctx)
    img, el, n = _schermata(ctx, con), con["elementi"][0], len(con["elementi"])
    if not img:
        return out
    t = Tela(CW, CH, NERO)
    t.pillola(M, 96, "Messaggio originale", 28, VERDE, BIANCO, traccia=3)

    def dis(tt, s, y):
        return y + tt.testo(M, y, CW - 2 * M, el["titolo"], 78 * s, BIANCO, peso="Black", enfasi=VERDE, inter=1.06)

    y = adatta(t, dis, 186, 470, scale=[1, .92, .85, .78, .7, .62, .55])
    # la schermata sta SOTTO il titolo, in una zona sua: nessun testo sopra l'immagine. Esce dal bordo: invita a scorrere
    t.immagine(img, M + 40, y + 50, CW - 2 * M - 80, CH - (y + 50), raggio=36, ancora="alto")
    t.rett(0, CH - 128, CW, 128, NERO)
    _piede_c(t, 1, n, True)
    out[0] = t
    return out


def s_schermata(con, ctx):
    out = s_messaggio(con, ctx)
    img, el = _schermata(ctx, con), con["elementi"][0]
    if not img:
        return out
    t = Tela(SW, SH, NERO)
    t.pillola(M, S_ALTO, "Messaggio originale", 28, VERDE, BIANCO, traccia=3)

    def dis(tt, s, y):
        return y + tt.testo(M, y, SW - 2 * M, el["titolo"], 84 * s, BIANCO, peso="Black", enfasi=VERDE, inter=1.06)

    y = adatta(t, dis, S_ALTO + 90, S_ALTO + 400, scale=[1, .92, .85, .78, .7, .62, .55])
    t.immagine(img, M + 30, y + 50, SW - 2 * M - 60, S_BASSO - 10 - (y + 50), raggio=36, ancora="alto")
    _piede_s(t, True)
    out[0] = t
    return out


FUNZIONI = {"C-schermata": c_schermata, "S-schermata": s_schermata, "C-schermo": c_schermo, "S-schermo": s_schermo,
            "C-virgolette": c_virgolette, "C-primadopo": c_primadopo, "C-percorso": c_percorso, "C-voci": c_voci,
            "S-messaggio": s_messaggio, "S-virgolette": s_virgolette, "S-tappe": s_tappe, "S-voci": s_voci}


def disegna(modello: str, contenuto: dict, ctx: dict | None = None) -> list[Tela]:
    return FUNZIONI[modello](contenuto, ctx or {})
