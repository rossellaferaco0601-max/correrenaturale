"""Motore grafico: una «Tela» descrive una slide con forme, testi e immagini.
La stessa tela viene scritta due volte: PNG (Pillow) e PPTX modificabile (python-pptx).
Tutte le misure sono in pixel della slide (1080 di larghezza)."""
from __future__ import annotations

import io
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RISORSE = Path(__file__).resolve().parent.parent / "assets"

VERDE = "#49762E"
AZZURRO = "#B8D7EA"
CREMA = "#F4F1E5"
NERO = "#000000"
BIANCO = "#FFFFFF"

PESI = {"Regular": "Blinker-Regular.ttf", "SemiBold": "Blinker-SemiBold.ttf", "Bold": "Blinker-Bold.ttf",
        "Black": "Blinker-Black.ttf"}
# nome del font dentro il PPTX: (famiglia, grassetto)
PESI_PPTX = {"Regular": ("Blinker", False), "SemiBold": ("Blinker SemiBold", False), "Bold": ("Blinker", True),
             "Black": ("Blinker Black", False)}
SCALA = 2  # il PNG si disegna al doppio e si riduce: bordi puliti
_font_cache: dict = {}


def font(peso: str, dim: float) -> ImageFont.FreeTypeFont:
    k = (peso, round(dim * 2) / 2)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(str(RISORSE / "fonts" / PESI[peso]), k[1])
    return _font_cache[k]


def mescola(c1: str, c2: str, q: float) -> str:
    """Colore pieno ottenuto mescolando c1 con c2 (q = quota di c2). Evita le trasparenze nel PPTX."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * q):02X}" for x, y in zip(a, b))


def _pezzi(txt: str, colore: str, enfasi: str | None):
    """«una *parola* forte» → [(testo, colore), ...]"""
    out = []
    for i, p in enumerate(re.split(r"\*(.+?)\*", txt)):
        if p:
            out.append((p, enfasi if (i % 2 and enfasi) else colore))
    return out


class Tela:
    def __init__(self, w: int, h: int, sfondo: str = BIANCO):
        self.w, self.h, self.sfondo, self.el = w, h, sfondo, []

    def vuota(self) -> "Tela":
        return Tela(self.w, self.h, self.sfondo)

    # ── forme ────────────────────────────────────────────────────────────
    def rett(self, x, y, w, h, colore, raggio=0, bordo=None, spessore=0):
        self.el.append(dict(t="rett", x=x, y=y, w=w, h=h, colore=colore, raggio=raggio, bordo=bordo, spessore=spessore))

    def cerchio(self, x, y, d, colore, bordo=None, spessore=0):
        self.el.append(dict(t="cerchio", x=x, y=y, w=d, h=d, colore=colore, bordo=bordo, spessore=spessore))

    def freccia(self, x, y, w, h, verso, colore):
        """verso: giu | dx"""
        self.el.append(dict(t="freccia", x=x, y=y, w=w, h=h, verso=verso, colore=colore))

    def immagine(self, percorso, x, y, w, h=None, raggio=0, copri=True):
        """copri=True: ritaglia per riempire il riquadro (foto). False: mantiene le proporzioni (loghi)."""
        if h is None:
            with Image.open(percorso) as im:
                h = round(w * im.height / im.width)
        self.el.append(dict(t="img", src=str(percorso), x=x, y=y, w=w, h=h, raggio=raggio, copri=copri))
        return h

    # ── testo ────────────────────────────────────────────────────────────
    def misura(self, w, txt, dim, peso="Regular", inter=1.16, traccia=0, maiuscolo=False):
        return self._righe(w, txt, dim, peso, "#000000", None, inter, traccia, maiuscolo)[1]

    def _righe(self, w, txt, dim, peso, colore, enfasi, inter, traccia, maiuscolo):
        f = font(peso, dim)
        if maiuscolo:
            txt = txt.upper()
        righe = []
        for par in str(txt).split("\n"):
            parole = []  # (parola, colore)
            for pezzo, col in _pezzi(par, colore, enfasi):
                for i, wd in enumerate(re.split(r"(\s+)", pezzo)):
                    if wd and not wd.isspace():
                        parole.append([wd, col, False])
                    elif wd and parole:
                        parole[-1][2] = True  # spazio dopo
            # i pezzi adiacenti senza spazio restano attaccati (es. *parola*,)
            riga, larg = [], 0.0
            i = 0
            while i < len(parole):
                gruppo = [parole[i]]
                while not gruppo[-1][2] and i + 1 < len(parole):
                    i += 1
                    gruppo.append(parole[i])
                i += 1
                lg = sum(self._lung(f, g[0], traccia) for g in gruppo)
                sp = self._lung(f, " ", traccia) if riga else 0
                if riga and larg + sp + lg > w:
                    righe.append(riga)
                    riga, larg, sp = [], 0.0, 0
                if sp:
                    riga.append((" ", riga[-1][1]))
                riga += [(g[0], g[1]) for g in gruppo]
                larg += sp + lg
            righe.append(riga)
        return righe, round(len(righe) * dim * inter)

    @staticmethod
    def _lung(f, s, traccia):
        return f.getlength(s) + traccia * len(s)

    def testo(self, x, y, w, txt, dim, colore, peso="Regular", enfasi=None, allinea="sx", inter=1.16, traccia=0,
              maiuscolo=False) -> int:
        """Aggiunge un blocco di testo e restituisce la sua altezza. *parola* = colore d'enfasi."""
        txt = str(txt or "").strip()
        if not txt:
            return 0
        righe, h = self._righe(w, txt, dim, peso, colore, enfasi, inter, traccia, maiuscolo)
        self.el.append(dict(t="testo", x=x, y=y, w=w, h=h, txt=txt.upper() if maiuscolo else txt, righe=righe, dim=dim,
                            colore=colore, enfasi=enfasi, peso=peso, allinea=allinea, inter=inter, traccia=traccia))
        return h

    def pillola(self, x, y, txt, dim, sfondo, colore, peso="Bold", pad=(30, 14), traccia=2, maiuscolo=True, centro=False):
        """Etichetta arrotondata. Con centro=True x è il centro. Restituisce (larghezza, altezza)."""
        s = txt.upper() if maiuscolo else txt
        lw = self._lung(font(peso, dim), s, traccia)
        w, h = round(lw + pad[0] * 2), round(dim * 1.16 + pad[1] * 2)
        if centro:
            x = round(x - w / 2)
        self.rett(x, y, w, h, sfondo, raggio=h // 2)
        self.testo(x, y + pad[1], w, txt, dim, colore, peso=peso, allinea="centro", traccia=traccia, maiuscolo=maiuscolo)
        return w, h


def adatta(tela: Tela, disegna, alto: int, basso: int, centra=False, scale=None) -> int:
    """Esegue disegna(tela, s, y0) riducendo la scala s finché il contenuto sta fra `alto` e `basso`."""
    scale = scale or [1.3, 1.22, 1.15, 1.08, 1, .95, .9, .85, .8, .75, .7, .65, .6, .55, .5, .45]
    s, h = scale[-1], 0
    for s in scale:
        h = disegna(tela.vuota(), s, 0)
        if h <= basso - alto:
            break
    y0 = alto + (max(0, basso - alto - h) // 2 if centra else 0)
    return disegna(tela, s, y0)


# ── PNG ──────────────────────────────────────────────────────────────────────
def _prepara_img(e, k=1):
    w, h = round(e["w"] * k), round(e["h"] * k)
    im = Image.open(e["src"]).convert("RGBA")
    if e["copri"]:
        r = max(w / im.width, h / im.height)
        im = im.resize((max(w, round(im.width * r)), max(h, round(im.height * r))), Image.LANCZOS)
        sx, su = (im.width - w) // 2, (im.height - h) // 2
        im = im.crop((sx, su, sx + w, su + h))
    else:
        im = im.resize((w, h), Image.LANCZOS)
    if e["raggio"]:
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), round(e["raggio"] * k), fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (w, h), 0), m))
    return im


def _punti_freccia(e, k=1.0):
    x, y, w, h = (e[c] * k for c in "xywh")
    if e["verso"] == "giu":
        return [(x + w * .3, y), (x + w * .7, y), (x + w * .7, y + h * .5), (x + w, y + h * .5), (x + w / 2, y + h),
                (x, y + h * .5), (x + w * .3, y + h * .5)]
    return [(x, y + h * .3), (x + w * .5, y + h * .3), (x + w * .5, y), (x + w, y + h / 2), (x + w * .5, y + h),
            (x + w * .5, y + h * .7), (x, y + h * .7)]


def a_png(tela: Tela) -> Image.Image:
    k = SCALA
    im = Image.new("RGB", (tela.w * k, tela.h * k), tela.sfondo)
    d = ImageDraw.Draw(im)
    for e in tela.el:
        x, y, w, h = (round(e[c] * k) for c in "xywh")
        if e["t"] == "rett":
            kw = dict(fill=e["colore"], outline=e["bordo"], width=round(e["spessore"] * k))
            if e["raggio"]:
                d.rounded_rectangle((x, y, x + w - 1, y + h - 1), round(min(e["raggio"], e["w"] / 2, e["h"] / 2) * k), **kw)
            else:
                d.rectangle((x, y, x + w - 1, y + h - 1), **kw)
        elif e["t"] == "cerchio":
            d.ellipse((x, y, x + w - 1, y + h - 1), fill=e["colore"], outline=e["bordo"], width=round(e["spessore"] * k))
        elif e["t"] == "freccia":
            d.polygon(_punti_freccia(e, k), fill=e["colore"])
        elif e["t"] == "img":
            pic = _prepara_img(e, k)
            im.paste(pic, (x, y), pic)
        elif e["t"] == "testo":
            f = font(e["peso"], e["dim"] * k)
            asc, desc = f.getmetrics()
            lh = e["dim"] * e["inter"] * k
            tr = e["traccia"] * k
            for i, riga in enumerate(e["righe"]):
                lung = sum(f.getlength(s) + tr * len(s) for s, _ in riga) - (tr if riga else 0)
                cx = x + {"sx": 0, "centro": (w - lung) / 2, "dx": w - lung}[e["allinea"]]
                cy = y + i * lh + (lh - asc - desc) / 2
                for s, col in riga:
                    if tr:
                        for ch in s:
                            d.text((cx, cy), ch, font=f, fill=col)
                            cx += f.getlength(ch) + tr
                    else:
                        d.text((cx, cy), s, font=f, fill=col)
                        cx += f.getlength(s)
    return im.resize((tela.w, tela.h), Image.LANCZOS)


# ── PPTX ─────────────────────────────────────────────────────────────────────
def a_pptx(tele: list[Tela], percorso: Path) -> None:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
    from pptx.util import Emu, Pt

    E = 9525  # EMU per pixel
    rgb = lambda c: RGBColor.from_string(c.lstrip("#").upper())
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(tele[0].w * E), Emu(tele[0].h * E)
    vuoto = prs.slide_layouts[6]

    def forma(sl, tipo, e):
        sh = sl.shapes.add_shape(tipo, Emu(round(e["x"] * E)), Emu(round(e["y"] * E)), Emu(round(e["w"] * E)), Emu(round(e["h"] * E)))
        sh.shadow.inherit = False
        if e.get("colore"):
            sh.fill.solid()
            sh.fill.fore_color.rgb = rgb(e["colore"])
        else:
            sh.fill.background()
        if e.get("bordo") and e.get("spessore"):
            sh.line.color.rgb = rgb(e["bordo"])
            sh.line.width = Pt(e["spessore"] * .75)
        else:
            sh.line.fill.background()
        return sh

    for tela in tele:
        sl = prs.slides.add_slide(vuoto)
        bg = sl.background.fill
        bg.solid()
        bg.fore_color.rgb = rgb(tela.sfondo)
        for e in tela.el:
            if e["t"] == "rett":
                if e["raggio"]:
                    sh = forma(sl, MSO_SHAPE.ROUNDED_RECTANGLE, e)
                    sh.adjustments[0] = min(.5, e["raggio"] / max(1, min(e["w"], e["h"])))
                else:
                    forma(sl, MSO_SHAPE.RECTANGLE, e)
            elif e["t"] == "cerchio":
                forma(sl, MSO_SHAPE.OVAL, e)
            elif e["t"] == "freccia":
                forma(sl, MSO_SHAPE.DOWN_ARROW if e["verso"] == "giu" else MSO_SHAPE.RIGHT_ARROW, e)
            elif e["t"] == "img":
                buf = io.BytesIO()
                _prepara_img(e, 2).save(buf, "PNG")
                buf.seek(0)
                sl.shapes.add_picture(buf, Emu(round(e["x"] * E)), Emu(round(e["y"] * E)), Emu(round(e["w"] * E)), Emu(round(e["h"] * E)))
            elif e["t"] == "testo":
                # qualche pixel in più di larghezza: PowerPoint e Canva vanno a capo un filo prima di Pillow
                agg = round(e["dim"] * .25)
                dx = {"sx": 0, "centro": -agg / 2, "dx": -agg}[e["allinea"]]
                tb = sl.shapes.add_textbox(Emu(round((e["x"] + dx) * E)), Emu(round(e["y"] * E)), Emu(round((e["w"] + agg) * E)), Emu(round(e["h"] * E)))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = MSO_AUTO_SIZE.NONE
                tf.vertical_anchor = MSO_ANCHOR.TOP
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                fam, grassetto = PESI_PPTX[e["peso"]]
                for i, par in enumerate(e["txt"].split("\n")):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.alignment = {"sx": PP_ALIGN.LEFT, "centro": PP_ALIGN.CENTER, "dx": PP_ALIGN.RIGHT}[e["allinea"]]
                    p.line_spacing = Pt(round(e["dim"] * e["inter"] * .75, 1))
                    for pezzo, col in _pezzi(par, e["colore"], e["enfasi"]):
                        r = p.add_run()
                        r.text = pezzo
                        r.font.name, r.font.bold, r.font.size = fam, grassetto, Pt(round(e["dim"] * .75, 1))
                        r.font.color.rgb = rgb(col)
                        if e["traccia"]:
                            r._r.get_or_add_rPr().set("spc", str(round(e["traccia"] * 75)))
    percorso.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(percorso))


def salva(tele: list[Tela], cartella: Path, prefisso: str, pptx: str | None = None) -> list[Path]:
    cartella.mkdir(parents=True, exist_ok=True)
    out = []
    for i, t in enumerate(tele, 1):
        p = cartella / f"{prefisso}-{i:02d}.png"
        a_png(t).save(p, optimize=True)
        out.append(p)
    if pptx:
        a_pptx(tele, cartella / pptx)
    return out


def foglio_contatti(tele: list[Tela], percorso: Path, alt=640, colonne=None, margine=16, sfondo="#D9D9D9") -> None:
    """Tutte le slide affiancate in un'unica immagine: serve per le anteprime e i controlli."""
    imgs = [a_png(t) for t in tele]
    imgs = [im.resize((round(im.width * alt / im.height), alt), Image.LANCZOS) for im in imgs]
    colonne = colonne or len(imgs)
    righe = (len(imgs) + colonne - 1) // colonne
    lw = imgs[0].width
    foglio = Image.new("RGB", (margine + colonne * (lw + margine), margine + righe * (alt + margine)), sfondo)
    for i, im in enumerate(imgs):
        foglio.paste(im, (margine + (i % colonne) * (lw + margine), margine + (i // colonne) * (alt + margine)))
    percorso.parent.mkdir(parents=True, exist_ok=True)
    foglio.save(percorso, quality=88)
