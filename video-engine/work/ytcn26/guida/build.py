#!/usr/bin/env python3
"""Guida «Come scaldarsi quando fa freddo» (Ross 22/11): tutto il contenuto di YTCN 26 messo per iscritto, con i fotogrammi del video.
Solo parole e numeri di Daniele (trascrizione in video-editing/consegne/trascrizioni/YTCN26_trascrizione.md): niente consigli tecnici aggiunti.
Scrive guida.html (pagine 1080x1350, stile del marchio). Il PDF e i fogli di controllo li fa export.js.
Uso: python3 work/ytcn26/guida/build.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = "Come scaldarsi quando fa freddo"
pages = []


def foot():
    return f'<div class="foot"><span><b>Correre Naturale®</b> · {TITLE}</span><span>{len(pages) + 1}</span></div>'


def page(inner, cls=""):
    pages.append(f'<section class="page {cls}">{inner}{foot() if "cover" not in cls else ""}</section>')


def sec(img, kicker, title, body, pos="center 5%", h=400):
    page(f'<div class="top" style="height:{h}px;background-image:url(img/{img}.jpg);background-position:{pos}"></div><div class="pad"><span class="kicker">{kicker}</span><h2>{title}</h2>{body}</div>')


def ul(items):
    return '<ul class="pts">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def box(title, text, cls="box"):
    return f'<div class="{cls}">{f"<h4>{title}</h4>" if title else ""}<p>{text}</p></div>'


def ex(n, name, rows, quote, h=420):
    r = "".join(f'<div class="row"><div class="l">{a}</div><div class="r">{b}</div></div>' for a, b in rows)
    page(f'<div class="duo" style="height:{h}px"><div style="background-image:url(img/e{n}a.jpg)"></div><div style="background-image:url(img/e{n}b.jpg)"></div><span class="n">{n}</span></div>'
         f'<div class="pad ex"><span class="kicker">Il circuito · esercizio {n} di 4</span><h2>{name}</h2><div class="rows">{r}</div><div class="quote">{quote}</div></div>')


# 1 · copertina
page('<div class="photo"></div><div class="shade"></div><div class="txt"><span class="kicker">Guida gratuita</span>'
     '<h1>Come scaldarsi<br><span>quando fa freddo</span></h1>'
     '<div class="sub">Il circuito da fare in casa in 5 minuti e i quattro consigli di Daniele Vecchioni per correre bene d\'inverno: vestirsi, scaldarsi, respirare, recuperare.</div></div>'
     '<img class="logo" src="img/logo-cn-orizzontale-bianco.png">', "cover")

# 2 · introduzione e indice
sec("s_intro", "Prima di cominciare", "Correre al freddo,<br>senza soffrirlo",
    "<p>Correre al freddo è una delle sfide più grandi per molti corridori. Eppure si può uscire a correre senza congelarsi, e godersi davvero l'allenamento anche d'inverno.</p>"
    "<p><b>Non si tratta solo di coprirsi di più:</b> esistono piccoli accorgimenti che fanno una differenza enorme, e trasformano le corse invernali da una lotta contro il freddo in un'esperienza unica e rinvigorente.</p>"
    '<div class="index"><div><i>1</i>Come vestirsi</div><div><i>2</i>Il miglior riscaldamento, con il circuito da fare in casa</div><div><i>3</i>Come respirare quando fa freddo</div><div><i>4</i>Defaticamento e stretching dopo la corsa</div></div>', h=328)

# 3 · consiglio 1: l'errore dei troppi strati
sec("s_vestirsi", "Consiglio 1 · Come vestirsi", "L'errore più comune:<br>troppi strati",
    "<p>Quando si parla di correre al freddo, la prima cosa a cui pensiamo è coprirci bene. Ma troppo spesso ci vestiamo in modo eccessivo, pensando che più strati significhino più calore e più comfort. È uno degli errori più comuni, e può trasformare la corsa in <b>un incubo di sudore e disagio</b>.</p>"
    "<p>Il segreto sta nel capire come funziona il corpo quando corriamo al freddo. All'inizio ci sembra di congelare, e la tentazione di indossare un maglione o una giacca pesante è molto forte. Ma dopo i primi <b>5-10 minuti</b> il corpo inizia a riscaldarsi naturalmente.</p>"
    + box("Parti con una leggera sensazione di freddo", "Quel piccolo brivido iniziale è il segnale che ti sei vestito nel modo giusto e che sarai comodo durante la corsa. Se quel brivido vuoi evitarlo, la soluzione è nel consiglio 2."), h=372)

# 4 · i tre strati
sec("s_strati", "Consiglio 1 · Come vestirsi", "La scelta<br>dei giusti strati",
    '<div class="steps">'
    '<div><i>1</i><div><h4>Base termica traspirante</h4><p>È essenziale. Aiuta a mantenere il calore del corpo senza bloccare il sudore, e previene quella sensazione di umido freddo. Deve essere tecnica, specifica per la corsa o per gli sport di endurance.</p></div></div>'
    '<div><i>2</i><div><h4>Secondo strato, leggero e isolante</h4><p>Per esempio un gilet antivento: trattiene il calore ma permette al corpo di traspirare.</p></div></div>'
    '<div><i>3</i><div><h4>Strato esterno antivento e idrorepellente</h4><p>Per le giornate davvero fredde, o fredde e molto ventose: è ideale per proteggere senza appesantire.</p></div></div>'
    "</div>"
    + box("", "Ogni strato ha uno scopo specifico e funziona in sinergia con gli altri, per tenerti al caldo senza surriscaldarti. Così correre al freddo può diventare addirittura piacevole, senza quella lotta tra sudore e gelo.", "box dark"), h=330)

# 5 · mani e testa
sec("s_mani", "Consiglio 1 · Come vestirsi", "Copri mani<br>e testa",
    "<p>È la cosa forse più importante da sapere su come vestirsi per correre al freddo.</p>"
    "<p>Le estremità sono <b>i punti più critici da riscaldare</b> per il nostro corpo, e quelli da cui dissipiamo più calore.</p>"
    '<div class="two"><div><h4>Hai ancora una folta chioma?</h4><p>Ti basta coprire le orecchie e la fronte.</p></div><div><h4>Per tutti gli altri</h4><p>Meglio prediligere un cappello.</p></div></div>'
    + box("E le mani?", "Guanti: insieme a cappello o fascia sono l'ultima cosa da mettere prima di uscire, come vedrai tra poco.", "box dark"), h=384)

# 6 · consiglio 2: il miglior riscaldamento
sec("s_riscaldamento", "Consiglio 2 · Il riscaldamento", "Il miglior riscaldamento<br>per correre al freddo",
    "<p>Se c'è una cosa che può trasformare la tua esperienza di corsa al freddo è un buon riscaldamento. E non parliamo di qualche saltello prima di partire.</p>"
    "<p>Specialmente quando le temperature si abbassano, il corpo ha bisogno di <b>una preparazione mirata</b>: per evitare infortuni e per garantire una corsa fluida e piacevole.</p>"
    + box("Il trucco per uscire senza sentire freddo", "Inizia il riscaldamento in un ambiente chiuso: in casa, o in un'area riparata. Bastano <b>5 minuti</b> di movimenti ed esercizi mirati per riscaldare il corpo dall'interno, aumentare la circolazione e prepararlo al meglio."))

# 7 · il circuito in un colpo d'occhio
cards = "".join(f'<div class="card"><div class="im" style="background-image:url(img/e{n}b.jpg)"><div class="n">{n}</div></div><div class="b"><h3>{name}</h3><div class="w">{w}</div><span class="pill">{t}</span></div></div>' for n, name, w, t in [
    (1, "Mountain climber", "Postura, addominali, parte superiore, flessori dell'anca, piedi.", "20 s · 30 s · 1 min"),
    (2, "Ponte per i glutei", "Estensione delle anche e del bacino. Dinamico o statico.", "30 s · 1 min"),
    (3, "Affondi", "Coordinati e gentili: tutto il corpo, soprattutto la parte inferiore.", "Non oltre 1 min"),
    (4, "Jumping jack", "Alzano la temperatura corporea e scaldano i tendini.", "30 s · 1 min")])
page('<div class="pad first"><span class="kicker">Consiglio 2 · Il circuito</span><h2>4 esercizi,<br>in casa, già vestito</h2>'
     "<p class=\"lead\">È uno dei circuiti preferiti di Daniele. Si fa dopo essersi vestiti: restano da mettere solo l'antivento (se serve), i guanti e il cappello o la fascia. Ci si mette a terra e si comincia.</p>"
     f'<div class="grid">{cards}</div>'
     '<div class="note">Lo scopo <b>non è affaticarsi</b>: è solo scaldarsi.</div></div>')

# 8-11 · le quattro schede
ex(1, "Mountain climber", [
    ("Perché", "Scalda molto bene: basta questo per alzare il calore interno."),
    ("Cosa lavora", "Postura, addominali e parte superiore del corpo. In più i flessori dell'anca, e si attivano anche i piedi."),
    ("Quanto", "20 secondi, 30 secondi o un minuto.")], "«Ottimo esercizio: si lavora tutto e ci scalda per bene.»", h=560)
ex(2, "Ponte per i glutei", [
    ("Quando", "Subito dopo il mountain climber: ci si gira e si fa il ponte."),
    ("Cosa lavora", "La postura: si va in estensione con le anche e con il bacino. Intanto si recupera dal mountain climber, ma il corpo continua a lavorare."),
    ("Per chi", "Soprattutto per chi va a correre dopo essere stato seduto o appena sveglio: cioè da posizioni di flessione, o dopo che il corpo è stato fermo e immobile."),
    ("Quanto", "Dinamico oppure statico, 30 secondi o un minuto.")], "«È un esercizio che a me piace moltissimo.»")
ex(3, "Affondi", [
    ("Come", "Ci si alza e si fa qualche affondo, sempre in maniera coordinata e gentile."),
    ("Attenzione", "Non devi rischiare di farti male: stai riscaldando il corpo dall'interno, attivando la muscolatura e facendo capire al corpo che tra poco gli chiederai un po' di performance."),
    ("Cosa lavora", "Tutto il corpo, soprattutto la parte inferiore. Alzano la temperatura interna, ancora di più dopo i primi due esercizi."),
    ("Quanto", "Organizzati come preferisci, ma non superare il minuto.")], "«Lo scopo non è affaticarsi, è solo scaldarsi.»")
ex(4, "Jumping jack", [
    ("Quando", "Finiti gli affondi, per chiudere il circuito."),
    ("Perché", "Alzano la temperatura corporea e scaldano anche i tendini."),
    ("Quanto", "30 secondi o un minuto: vedi tu."),
    ("Alla fine", "Sei già quasi sudato: sei pronto a uscire.")], "«E voilà: io sto già quasi sudando, sono pronto.»", h=540)

# 12 · prima di uscire
sec("s_uscire", "Consiglio 2 · Prima di uscire", "Cosa metti<br>per ultimo",
    "<p>Finito il circuito sei caldo e pronto. Adesso completa l'abbigliamento in base al freddo che c'è fuori.</p>"
    '<div class="two tall"><div><h4>Molto, molto freddo</h4><p>Giacca antivento, guanti, cappello e fascia.</p></div><div><h4>Freddo, ma non estremo</h4><p>Puoi uscire anche così: solamente con guanti e fascia.</p></div></div>'
    + box("", "Ricorda la regola del consiglio 1: meglio un leggero brivido alla partenza che un incubo di sudore durante la corsa.", "box dark"))

# 13 · appena fuori
sec("s_corsa", "Consiglio 2 · Appena fuori", "La corsa<br>di riscaldamento",
    "<p>Una volta uscito, aggiungi un breve periodo di camminata o una corsa molto leggera: una corsa a <b>un'intensità molto bassa</b>, che può essere anche alla stessa velocità della camminata.</p>"
    + ul(["Prepara tendini, articolazioni e muscoli all'allenamento.", "Fa capire al tuo sistema nervoso che stai iniziando ad allenarti.",
          "Ti permette di sfruttare la tua energia in modo più efficiente: entri nella parte più intensa già attivo e pronto, senza sprecare energia per scaldarti nei primi chilometri."])
    + box("Ricapitolando", "Riscaldati bene prima di uscire e fai nei primi minuti un riscaldamento graduale. Così, anche se fuori fa molto freddo, sarai pronto e carico invece di dover lottare per riscaldarti strada facendo."), h=356)

# 14 · consiglio 3: respirare dal naso
sec("s_respiro", "Consiglio 3 · La respirazione", "Come respirare<br>quando fa freddo",
    "<p>Correre al freddo non mette alla prova solo tendini, muscoli e articolazioni, ma anche la capacità di respirare in modo confortevole e fluido. Se ti è capitato di sentire un fastidio nei polmoni, o la sensazione di <b>aria tagliente</b>, non sei solo: è un aspetto che scoraggia molti corridori.</p>"
    + box("Il primo consiglio: impara a respirare dal naso", "Respirare dal naso aiuta a riscaldare e umidificare l'aria prima che arrivi ai polmoni, e riduce l'impatto dell'aria fredda sul sistema respiratorio. È il modo naturale per riscaldare l'aria, filtrarla e proteggere le vie respiratorie.")
    + "<p>Con il giusto approccio, quella sensazione di disagio diventa una respirazione controllata e piacevole.</p>")

# 15 · niente affanno
sec("s_affanno", "Consiglio 3 · La respirazione", "Solo dal naso,<br>senza affanno",
    "<p>Respirare solo dal naso quando si corre può risultare difficile, soprattutto se non si è abituati. Ma respirare esclusivamente dal naso può fare davvero una grande differenza.</p>"
    + ul(["Mantieni la respirazione controllata e regolare.", "Non farti prendere dalla fretta nei primi minuti della corsa, quando il corpo si sta ancora adattando.",
          "Parti sempre a un'intensità bassa e costante.", "Stai attento a non andare in affanno fin da subito."])
    + box("", "Respirare bene non rende solo più confortevole la corsa al freddo: ti dà una sensazione di padronanza e sicurezza, e trasforma quella che poteva sembrare una sfida insormontabile in un'esperienza gratificante.", "box dark"))

# 16 · consiglio 4: dopo la corsa
sec("s_squat", "Consiglio 4 · Dopo la corsa", "Defaticamento:<br>lo squat naturale",
    "<p>Per il defaticamento e lo stretching dopo una corsa al freddo, concentrati su esercizi semplici ma potenti. E il movimento post corsa più potente per l'essere umano, secondo Daniele, è <b>lo squat naturale</b>.</p>"
    + ul(["Fallo in un ambiente chiuso, o almeno riparato, soprattutto quando le temperature sono molto basse.", "Bastano 3-4 minuti di squat naturale.",
          "Questo piccolo rituale migliora il recupero e fa la manutenzione necessaria a prevenire quei fastidiosi indolenzimenti che affliggono molti corridori."])
    + box("", "Dedicare anche pochi minuti al recupero è un investimento che ti ripagherà alla grande nella qualità delle tue corse e nella salute del tuo corpo."))

# 17 · riepilogo e invito
page('<div class="pad first"><span class="kicker">In breve</span><h2>La tua corsa<br>al freddo, passo passo</h2>'
     '<div class="check">'
     "<div><i>1</i><div><h4>Vestiti</h4><p>Strati giusti, mani e testa coperte. Meglio un leggero brivido alla partenza.</p></div></div>"
     "<div><i>2</i><div><h4>Scaldati in casa</h4><p>5 minuti, già vestito: mountain climber, ponte per i glutei, affondi, jumping jack.</p></div></div>"
     "<div><i>3</i><div><h4>Appena fuori</h4><p>Camminata o corsa molto leggera: riscaldamento graduale.</p></div></div>"
     "<div><i>4</i><div><h4>Mentre corri</h4><p>Respira dal naso, intensità bassa e costante, niente affanno.</p></div></div>"
     "<div><i>5</i><div><h4>Al rientro</h4><p>3-4 minuti di squat naturale, al chiuso.</p></div></div>"
     "</div>"
     '<div class="cta"><h4>Vuoi essere seguito passo passo?</h4><p>Scrivici su Instagram, <b>@correrenaturale</b>: ti mandiamo tutte le info sul coaching personalizzato di Correre Naturale®.</p></div></div>')

CSS = """
@font-face { font-family: Blinker; font-weight: 400; src: url(Blinker-Regular.ttf); }
@font-face { font-family: Blinker; font-weight: 600; src: url(Blinker-SemiBold.ttf); }
@font-face { font-family: Blinker; font-weight: 800; src: url(Blinker-ExtraBold.ttf); }
@font-face { font-family: Blinker; font-weight: 900; src: url(Blinker-Black.ttf); }
:root { --green: #49762E; --deep: #1C3D15; --lime: #95FF00; --cream: #F4F1E5; --ink: #0B0F0A; }
* { box-sizing: border-box; margin: 0; padding: 0; }
@page { size: 1080px 1350px; margin: 0; }
body { font-family: Blinker, sans-serif; color: var(--ink); background: #777; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 1080px; height: 1350px; position: relative; overflow: hidden; background: var(--cream); page-break-after: always; break-after: page; }
.kicker { display: inline-block; background: var(--lime); color: var(--ink); font-weight: 900; font-size: 27px; letter-spacing: 2.5px; padding: 7px 20px 9px; border-radius: 10px; text-transform: uppercase; }
.foot { position: absolute; left: 70px; right: 70px; bottom: 34px; display: flex; justify-content: space-between; font-weight: 600; font-size: 23px; color: rgba(11,15,10,0.5); }
.foot b { color: var(--green); font-weight: 900; }
h2 { font-weight: 900; font-size: 76px; line-height: 0.98; text-transform: uppercase; margin: 16px 0 22px; }
h4 { font-weight: 900; font-size: 34px; line-height: 1.08; text-transform: uppercase; }
p { font-weight: 400; font-size: 33px; line-height: 1.27; margin-bottom: 16px; }
p b, li b { font-weight: 800; }
.top { height: 400px; background-size: cover; }
.pad { padding: 34px 70px 0; }
.pad.first { padding-top: 62px; }
.box { margin-top: 10px; background: #fff; border-left: 12px solid var(--lime); border-radius: 0 22px 22px 0; padding: 22px 28px 12px; box-shadow: 0 5px 16px rgba(11,15,10,0.08); margin-bottom: 18px; }
.box h4 { color: var(--green); margin-bottom: 10px; }
.box.dark { background: var(--deep); border-left: 0; border-radius: 22px; padding: 24px 30px 10px; }
.box.dark p { color: var(--cream); } .box.dark h4 { color: var(--lime); } .box.dark b { color: var(--lime); }
.pts { list-style: none; margin: 4px 0 14px; }
.pts li { position: relative; padding-left: 44px; font-size: 32px; line-height: 1.25; margin-bottom: 13px; }
.pts li::before { content: ""; position: absolute; left: 4px; top: 11px; width: 20px; height: 20px; border-radius: 10px; background: var(--lime); box-shadow: 0 0 0 4px var(--deep); }
.index { margin-top: 12px; display: grid; gap: 12px; }
.index div { background: #fff; border-radius: 18px; padding: 15px 22px; font-weight: 800; font-size: 32px; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 12px rgba(11,15,10,0.07); }
i { font-style: normal; flex-shrink: 0; width: 58px; height: 58px; border-radius: 29px; background: var(--lime); font-weight: 900; font-size: 38px; display: flex; align-items: center; justify-content: center; }
.steps > div, .check > div { display: flex; gap: 22px; align-items: flex-start; margin-bottom: 16px; }
.steps p, .check p { margin: 6px 0 0; font-size: 31px; }
.check > div { background: #fff; border-radius: 20px; padding: 16px 22px; margin-bottom: 13px; box-shadow: 0 4px 12px rgba(11,15,10,0.07); }
.check p { font-size: 29px; line-height: 1.22; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 8px 0 20px; }
.two > div { background: #fff; border-radius: 22px; padding: 22px 24px 10px; border-top: 10px solid var(--lime); box-shadow: 0 5px 16px rgba(11,15,10,0.08); }
.two h4 { color: var(--green); margin-bottom: 8px; } .two p { font-size: 31px; }
/* copertina */
.cover { background: var(--ink); color: #fff; }
.cover .photo { position: absolute; inset: 0; background: url(img/s_cover.jpg) 46% 0 / auto 78% no-repeat var(--ink); }
.cover .shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(11,15,10,0) 30%, rgba(20,44,15,0.9) 55%, rgba(11,15,10,1) 74%); }
.cover .txt { position: absolute; left: 70px; right: 70px; bottom: 170px; }
.cover h1 { font-weight: 900; font-size: 118px; line-height: 0.96; text-transform: uppercase; margin: 24px 0 22px; }
.cover h1 span { color: var(--lime); }
.cover .sub { font-weight: 600; font-size: 36px; line-height: 1.22; color: var(--cream); }
.cover .logo { position: absolute; left: 70px; bottom: 52px; height: 78px; }
/* circuito */
.lead { font-size: 30px; margin-bottom: 4px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px; }
.card { background: #fff; border-radius: 26px; overflow: hidden; box-shadow: 0 6px 18px rgba(11,15,10,0.10); }
.card .im { height: 178px; background-size: cover; background-position: center 60%; position: relative; }
.card .n, .duo .n { position: absolute; left: 14px; top: 14px; width: 64px; height: 64px; border-radius: 32px; background: var(--lime); font-weight: 900; font-size: 44px; display: flex; align-items: center; justify-content: center; }
.card .b { padding: 12px 20px 16px; }
.card h3 { font-weight: 900; font-size: 37px; line-height: 1; text-transform: uppercase; }
.card .w { font-size: 25px; line-height: 1.2; margin-top: 6px; color: rgba(11,15,10,0.78); min-height: 60px; }
.pill { display: inline-block; margin-top: 8px; background: var(--deep); color: var(--lime); font-weight: 800; font-size: 25px; padding: 5px 15px 7px; border-radius: 10px; }
.note { margin-top: 20px; background: var(--deep); color: var(--cream); border-radius: 22px; padding: 18px 28px; font-size: 31px; }
.note b { color: var(--lime); font-weight: 800; }
/* scheda esercizio */
.duo { height: 420px; display: grid; grid-template-columns: 1fr 1fr; gap: 6px; background: var(--deep); position: relative; }
.duo > div { background-size: cover; background-position: center; }
.duo .n { left: 50%; top: auto; bottom: -46px; margin-left: -57px; width: 114px; height: 114px; border-radius: 57px; font-size: 80px; box-shadow: 0 0 0 9px var(--cream); }
.ex { padding-top: 66px; text-align: left; }
.rows { display: grid; gap: 15px; }
.row { display: grid; grid-template-columns: 215px 1fr; gap: 22px; }
.row .l { font-weight: 900; font-size: 28px; text-transform: uppercase; color: var(--green); padding-top: 5px; letter-spacing: 1px; }
.row .r { font-size: 32px; line-height: 1.25; }
.quote { margin-top: 22px; border-left: 10px solid var(--lime); padding: 4px 0 4px 22px; font-weight: 600; font-style: italic; font-size: 31px; line-height: 1.25; color: rgba(11,15,10,0.8); }
.cta { margin-top: 18px; background: var(--deep); border-radius: 24px; padding: 24px 30px 10px; }
.cta h4 { color: var(--lime); font-size: 38px; margin-bottom: 10px; } .cta p { color: var(--cream); font-size: 31px; } .cta b { color: var(--lime); }
"""
html = f'<!doctype html>\n<html lang="it"><head><meta charset="utf-8"><title>{TITLE} · Correre Naturale®</title><style>{CSS}</style></head><body>\n' + "\n".join(pages) + "\n</body></html>\n"
open(os.path.join(HERE, "guida.html"), "w").write(html)
print(len(pages), "pagine")
