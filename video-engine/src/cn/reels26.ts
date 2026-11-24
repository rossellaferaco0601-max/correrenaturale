// YTCN 26 · «Correre al freddo» (video del Drive «YTCN26 NO SCRITTE», 20/11/2026): serie G.
// Sorgente Full HD già montato, senza scritte: nel bosco una sola camera frontale con ingrandimenti (volto al centro, mento tra 0,37 e 0,52),
// in casa il circuito di riscaldamento (3:55-6:44, corpo intero e dettagli). Master con scripts/cn_master_shots.py (mappa in
// work/ytcn26_shots.json, stacchi fissati al fotogramma). Ogni reel è un tratto INTERO del video (regola 18/11: niente tagli inutili).
// Assetto del 18/11 per tutta la serie: sottotitoli tra 1405 e 1497 px, grafiche al 96 % con almeno ~100 px di aria sopra i sottotitoli,
// finale morbido prima della CTA. Le rappresentazioni animate (Elements10 + cartella gem/) sono inedite: una per reel.
import words26 from "./words26.json";
import type { CNReelProps } from "./types";
import type { ReelDef } from "./reels51";

const SRC = "ytcn26/ytcn26_src.mp4";
const master = (id: string) => `ytcn26/masters/${id}.mp4`;
/** Pezzi dai punti di taglio dell'audio (silenzi misurati): ogni pezzo dura un numero intero di fotogrammi. */
const cut = (...a: [number, number][]) => a.map(([f, t]) => ({ from: f, to: +(f + Math.round((t - f) * 30) / 30).toFixed(4) }));

const base = {
  src: SRC,
  words: words26 as CNReelProps["words"],
  blendFrames: 0,
  ctaSeconds: 8,
  wordOffset: -0.06, // parole allineate con cn_align.py
  wordFix: {} as Record<string, string>,
  hook: null,
  gfxShift: 150,
  gfxScale: 0.98, // bordo destro a 971 px (dentro lo 0,90)
  capShift: 40,
  // finale (Ross 24/11: «si vede che parla ma non c'è suono», «stacco troppo netto»): dopo l'ultima parola non resta NESSUN video. In questo
  // sorgente l'inquadratura cambia 2-10 centesimi dopo la fine di ogni frase, quindi niente coda dal vivo (si vedrebbe la mossa dopo), niente
  // andata e ritorno (sembrava un parlato senza audio) e niente fermo immagine: la CTA comincia a salire 0,4 s PRIMA della fine del parlato
  // (salita morbida di 12 fotogrammi) e finisce di coprire proprio sull'ultima sillaba, che si sente sopra il pannello.
  tailSeconds: 0.1,
  ctaLead: 0.4,
  tailLive: 0,
};
const KICKER = "Correre al freddo";
/** parola da commentare, UNA per tutta la serie (Ross 24/11: «tutte le CTA hanno parole troppo diverse, mettine una tipo freddo uguale per tutte») */
const PAROLA = "FREDDO";
/** circuito in casa (3:55-6:44): video «a finestra» (a tutta larghezza su fondo verde, master con `window`), grafiche nella fascia sopra la finestra */
// 24/11 (Ross su G5-G8): niente pannello CTA, bordi del video sfumati nel verde, sottotitoli più grandi e un po' più in basso,
// grafiche un po' più in alto (più aria sopra il video)
const WIN = { gfxShift: -640, winFeather: 90, capSize: 76, capShift: 96, ctaSeconds: 0, tailSeconds: 0.3, tailLive: 0.3, ctaLead: undefined };
const KICKER_W = "Riscaldamento in casa";
const CAP = (testo: string, chiusa: string) => `${testo}\n\n${chiusa}\n\n#correrenaturale #correrealfreddo #corsa #running #inverno`;
const COACH = (domanda: string, parola: string) => `${domanda} Commenta ${parola} e ti mando tutte le info sui percorsi di coaching personalizzato di Correre Naturale®.`;
const GUIDA_C = `Vuoi il circuito completo? Commenta ${PAROLA} e ti mando gratis la guida «Come scaldarsi quando fa freddo».`;
/** CTA con guida da scaricare (Ross 21/11): chi commenta riceve una guida di approfondimento invece delle info sul coaching.
 *  Due guide per la serie: come vestirsi (G2) e il circuito di riscaldamento in casa (G4 e i quattro esercizi G5-G8). */
// la guida che esiste è una sola, «Come scaldarsi quando fa freddo» (17 pagine: strati, mani e testa, circuito, corsa di riscaldamento, respiro, squat)
const GUIDA_STRATI = { word: PAROLA, title: "Vuoi vestirti giusto per correre al freddo?", sub: "Scarica gratis la guida", offer: ["Come scaldarsi", "quando fa freddo"], dm: "Ti mando la guida" };
const GUIDA_CIRCUITO = { word: PAROLA, title: "Vuoi il circuito completo?", sub: "Scarica gratis la guida", offer: ["Come scaldarsi", "quando fa freddo"], dm: "Ti mando la guida" };

export const REELS26: ReelDef[] = [
  {
    id: "G1-brivido",
    title: "L'errore dei troppi strati",
    cover: { frame: 1156, kicker: KICKER, lines: ["Freddo: l'errore", "dei troppi strati"], accent: "troppi strati" },
    props: {
      ...base,
      master: master("G1-brivido"),
      segments: cut([41.62, 92.7]),
      elements: [
        { kind: "fog", anim: "snap", at: 0.1, dur: 4.4, lines: ["Correre al freddo:", "l'errore più comune"], accent: "l'errore più comune" },
        // 24/11 (Ross: «non vedo nessun effetto», «l'omino è orribile»): schianto su «attenzione», corridore 3D al posto dei disegni,
        // gelo sui bordi quando «sembra di congelare», calore quando il corpo si scalda, avvicinamenti lenti nei passaggi senza grafica
        { kind: "slam", dy: -33, at: 4.6, word: "ma", dur: 3.2, cues: ["ma", "attenzione"], lead: ["Ma"], text: "Attenzione" },
        { kind: "gem", dy: -19, art: "over3d", at: 8.3, word: "eccessivo", dur: 12.9, cues: ["più", "realtà", "incubo"], phases: [{ lines: ["Più strati,", "più calore?"] }, { lines: ["L'errore", "più comune"] }, { lines: ["Un incubo", "di sudore"] }] },
        { kind: "kin", anim: "pulse", at: 21.5, word: "segreto", dur: 4.6, cues: ["segreto", "capire"], words: ["Il segreto?", "Capire il corpo"] },
        { kind: "gem", dy: -19, art: "warm3d", at: 27.9, dur: 11.9, cues: ["congelare", "5-10", "riscaldarsi"], phases: [{ lines: ["Sembra di", "congelare"] }, { lines: ["Dopo", "5-10 minuti"] }, { lines: ["Il corpo", "si scalda"] }], artCues: [1, 2] },
        { kind: "ambient", mood: "frost", at: 28.2, word: "congelare", dur: 3.4 },
        { kind: "ambient", mood: "heat", at: 38.0, word: "riscaldarsi", dur: 2.6 },
        { kind: "gem", dy: -19, art: "warm3d", at: 41.0, word: "meglio", dur: 7.45, cues: ["leggera", "brivido", "segnale"], phases: [{ lines: ["Parti con un", "leggero freddo"] }, { lines: ["Brivido", "iniziale"] }, { lines: ["Brivido", "iniziale"], chip: "Vestito giusto" }], artCues: [-1, 2] },
        // a 48,93 il sorgente cambia inquadratura (2 s prima della fine): l'ultima frase va sopra la scheda «da ricordare», che resta fino alla CTA
        { kind: "takeaway", at: 48.62, dur: 2.5, lines: ["Brivido iniziale:", "vestito giusto"], accent: "vestito giusto", art: "warmok3d" },
      ],
      zooms: [{ at: 21.4, dur: 5.2, scale: 1.07 }],
      cta: { word: PAROLA, title: "Vuoi correre bene anche d'inverno?" },
    },
    didascalia: CAP(`Quando fa freddo la prima cosa a cui pensiamo è coprirci bene. Ma troppo spesso ci vestiamo in modo eccessivo, convinti che più strati significhino più calore e più comfort: è uno degli errori più comuni, e può trasformare la corsa in un incubo di sudore e disagio.

Il segreto è capire come funziona il corpo quando corri al freddo. All'inizio sembra di congelare e la tentazione di mettere un maglione o una giacca pesante è forte, ma dopo i primi 5-10 minuti il corpo comincia a scaldarsi da solo.

Per questo è meglio partire con una leggera sensazione di freddo: quel piccolo brivido iniziale è il segnale che ti sei vestito nel modo giusto e che starai comodo per tutta la corsa.`, COACH("Vuoi correre bene anche d'inverno?", PAROLA)),
  },
  {
    id: "G2-strati",
    title: "Gli strati giusti per correre al freddo",
    cover: { frame: 130, kicker: KICKER, lines: ["Freddo:", "gli strati giusti"], accent: "strati giusti" },
    props: {
      ...base,
      master: master("G2-strati"),
      // «partiamo dalla scelta dei giusti strati … senza quella lotta tra sudore e gelo. Molto fastidiosa.» (tratto intero)
      segments: cut([100.72, 157.04]),
      elements: [
        { kind: "fog", at: 0.1, dur: 2.55, dy: -30, lines: ["Correre al freddo:", "gli strati giusti"], accent: "gli strati giusti" },
        { kind: "layers", at: 3.7, word: "una", dur: 11.6, cues: ["base", "calore", "sudore"], stage: 1, dy: -33, lines: ["Base termica", "traspirante"], chips: ["Calore dentro", "Sudore fuori"] },
        { kind: "hangtag", at: 16.5, word: "tecnica", dur: 4.3, dy: -40, cues: ["tecnica", "corsa"], lines: ["Base tecnica", "per la corsa"] },
        { kind: "layers", at: 22.1, word: "secondo", dur: 6.5, cues: ["secondo", "trattiene", "permette"], stage: 2, dy: -33, lines: ["Strato leggero", "isolante"], chips: ["Tiene caldo", "Fa traspirare"] },
        { kind: "gust", at: 30.7, word: "fredde", dur: 2.95, dy: -40, cues: ["fredde", "ventose"], words: ["Freddo", "Vento"] },
        { kind: "layers", at: 33.95, word: "esterno", dur: 5.3, cues: ["esterno", "antivento", "idrorepellente"], stage: 3, dy: -33, lines: ["Strato esterno"], chips: ["Antivento", "Idrorepellente"] },
        { kind: "rings", at: 40.7, word: "ogni", dur: 6.5, dy: -22, cues: ["ogni", "sinergia", "caldo"], phases: [["Ogni strato", "ha uno scopo"], ["In sinergia"], ["Al caldo", "senza", "surriscaldarti"]] },
        { kind: "duel", at: 53.2, word: "lotta", dur: 2.6, dy: -30, cues: ["lotta", "sudore", "gelo", "molto"], left: "Sudore", right: "Gelo" },
      ],
      cta: GUIDA_STRATI,
    },
    didascalia: `Come ci si veste per correre al freddo? Non con «più roba», ma con gli strati giusti.

Il primo è una base termica traspirante: tiene il calore del corpo senza bloccare il sudore, così eviti quella sensazione di umido freddo. Deve essere tecnica, specifica per la corsa o per gli sport di endurance. Sopra puoi aggiungere un secondo strato leggero e isolante, come un gilet antivento, che trattiene il calore ma lascia traspirare. Per le giornate davvero fredde o molto ventose serve infine uno strato esterno antivento e idrorepellente, che protegge senza appesantire.

Ogni strato ha uno scopo preciso e lavorano insieme: ti tengono al caldo senza farti surriscaldare. Così correre al freddo può diventare addirittura piacevole, senza la lotta continua tra sudore e gelo.

Vuoi la guida completa? Commenta FREDDO e ti mando gratis la guida «Come scaldarsi quando fa freddo».

#correrenaturale #correrealfreddo #corsa #running #inverno`,
  },
  {
    id: "G3-mani",
    title: "Freddo: copri mani e testa",
    cover: { frame: 302, kicker: KICKER, lines: ["Freddo: copri", "mani e testa"], accent: "mani e testa" },
    props: {
      ...base,
      master: master("G3-mani"),
      segments: cut([157.14, 178.68]),
      elements: [
        { kind: "fog", anim: "wind", at: 0.1, dur: 5.3, lines: ["Freddo: la cosa", "più importante"], accent: "più importante" },
        // 24/11: corridore 3D al posto dell'omino disegnato. A mani e testa scoperte il calore esce da lì; poi guanti e fascia, poi il cappello
        { kind: "gem", dy: -19, art: "mani3d", at: 5.9, word: "coprire", dur: 8.6, cues: ["mani", "estremità", "critici", "dissipiamo"], phases: [{ lines: ["Copri mani", "e testa"] }, { lines: ["I punti", "più critici"], on: 2 }, { lines: ["Qui perdi", "più calore"], on: 3 }], artCues: [-1, -1] },
        { kind: "ambient", mood: "frost", at: 12.4, word: "dissipiamo", dur: 2.3 },
        { kind: "gem", dy: -19, art: "mani3d", at: 16.7, word: "basta", dur: 4.3, cues: ["orecchie", "meglio"], phases: [{ lines: ["Orecchie", "e fronte"] }, { lines: ["Oppure un", "cappello"] }], artCues: [0, 1] },
      ],
      zooms: [{ at: 14.7, dur: 2.0, scale: 1.06 }],
      cta: { word: PAROLA, title: "Vuoi goderti la corsa anche al freddo?" },
    },
    didascalia: CAP(`La cosa forse più importante da sapere su come vestirsi per correre al freddo: coprire mani e testa.

Le estremità sono i punti più difficili da scaldare per il corpo e quelli da cui disperdiamo più calore. Puoi avere gli strati giusti sul busto, ma se mani e testa restano scoperte il freddo lo senti lo stesso.

Se hai ancora una folta chioma ti basta coprire orecchie e fronte con una fascia. Altrimenti meglio un cappello.`, COACH("Vuoi goderti la corsa anche al freddo?", PAROLA)),
  },
  {
    id: "G4-casa",
    title: "Il trucco per uscire senza sentire freddo",
    cover: { frame: 868, kicker: KICKER, lines: ["Freddo: scaldati", "prima di uscire"], accent: "prima di uscire" },
    props: {
      ...base,
      master: master("G4-casa"),
      segments: cut([180.52, 222.36]),
      elements: [
        { kind: "fog", anim: "rise", at: 0.1, dur: 3.1, lines: ["Il miglior riscaldamento", "per correre al freddo"], accent: "per correre al freddo" },
        // 24/11 (Ross: «né effetti né animazioni, noioso e poco dinamico»): schianto su «un buon riscaldamento», frase barrata sui saltelli,
        // gelo quando «le temperature si abbassano», corridore 3D che si scalda in casa con i jumping jack, calore «dall'interno»
        { kind: "slam", dy: -65, at: 6.9, word: "è", dur: 2.3, cues: ["un", "riscaldamento"], lead: ["Un buon"], text: "Riscaldamento" },
        { kind: "bigstrike", at: 9.6, word: "qualche", dur: 2.1, text: "Qualche saltello", big: true },
        { kind: "kin", anim: "ice", at: 13.3, word: "temperature", dur: 3.1, cues: ["temperature", "abbassano"], words: ["Temperature", "basse"] },
        { kind: "ambient", mood: "frost", at: 13.3, word: "temperature", dur: 3.1 },
        { kind: "kin", anim: "slide", at: 16.7, word: "preparazione", dur: 4.9, cues: ["preparazione", "infortuni"], words: ["Preparazione mirata", "Meno infortuni"] },
        { kind: "kin", anim: "pulse", at: 22.6, word: "trucco", dur: 2.75, cues: ["trucco"], words: ["Il trucco?"] },
        { kind: "gem", dy: -31, art: "casa3d", at: 25.7, word: "iniziare", dur: 15.5, cues: ["ambiente", "5", "dall'interno", "circolazione", "preparare"], phases: [{ lines: ["Al chiuso,", "in casa"] }, { lines: ["Bastano", "5 minuti"] }, { lines: ["Calore", "dall'interno"] }, { lines: ["Più", "circolazione"] }, { lines: ["Corpo", "pronto"] }], artCues: [1, 2] },
        { kind: "ambient", mood: "heat", at: 36.1, word: "dall'interno", dur: 2.6 },
      ],
      zooms: [{ at: 3.3, dur: 3.5, scale: 1.07 }, { at: 22.4, dur: 3.2, scale: 1.07 }],
      // banner fisso per tutto il reel (Ross 24/11): una riga sotto i sottotitoli, che per questo salgono di 22 px
      banner: { word: PAROLA, text: ["Commenta", "e ricevi il circuito completo"], y: 1522 },
      capShift: 18,
      cta: GUIDA_CIRCUITO,
    },
    didascalia: CAP(`Se c'è una cosa che può cambiare la tua esperienza di corsa al freddo è un buon riscaldamento. E non parlo di qualche saltello prima di partire: quando le temperature si abbassano il corpo ha bisogno di una preparazione mirata, per evitare infortuni e per avere una corsa fluida e piacevole.

Il trucco per uscire senza sentire freddo? Cominciare il riscaldamento in un ambiente chiuso, in casa o in un'area riparata.

Bastano 5 minuti di movimenti ed esercizi mirati per scaldare il corpo dall'interno, aumentare la circolazione e arrivare fuori già pronto.`, GUIDA_C),
  },
  {
    id: "G5-climber",
    title: "Riscaldamento in casa: mountain climber",
    cover: { frame: 240, shiftY: -0.17, kicker: KICKER_W, lines: ["Esercizio 1:", "mountain climber"], accent: "mountain climber" },
    props: {
      ...base,
      ...WIN,
      winHeader: { kicker: KICKER_W, title: "Mountain|climber", n: "1" },
      master: master("G5-climber"),
      segments: cut([240.4, 269.7]),
      elements: [
        { kind: "gem", art: "climber", at: 4.6, word: "oltre", dur: 17.2, cues: ["postura", "superiore", "flessori", "piedi", "scalda"], phases: [{ lines: ["Postura e", "addominali"] }, { lines: ["Parte", "superiore"] }, { lines: ["Flessori", "dell'anca"] }, { lines: ["Anche", "i piedi"] }, { lines: ["Scalda", "per bene"] }] },
        { kind: "dose", at: 22.5, dur: 6.3, cues: ["20", "30", "minuto"], items: ["20 sec", "30 sec", "1 min"] },
      ],
      cta: GUIDA_CIRCUITO,
    },
    didascalia: CAP(`Primo esercizio del circuito di riscaldamento da fare in casa prima di uscire a correre al freddo: il mountain climber.

Scalda molto bene e intanto fa lavorare la postura, gli addominali e la parte superiore del corpo. In più lavora sui flessori dell'anca e attiva anche i piedi: si muove tutto.

Puoi farlo per 20 secondi, 30 secondi o un minuto: basta questo per alzare il calore interno.`, GUIDA_C),
  },
  {
    id: "G6-ponte",
    title: "Riscaldamento in casa: ponte per i glutei",
    cover: { frame: 120, shiftY: -0.17, kicker: KICKER_W, lines: ["Esercizio 2:", "ponte per i glutei"], accent: "ponte per i glutei" },
    props: {
      ...base,
      ...WIN,
      winHeader: { kicker: KICKER_W, title: "Ponte|per i glutei", n: "2" },
      tailSeconds: 1.0, // l'ultima durata («un minuto») arriva a fine frase: resta a schermo un secondo (coda che continua a muoversi, il sorgente stacca subito dopo)
      tailLive: 0.05,
      master: master("G6-ponte"),
      // 24/11 (Ross): «il video deve iniziare da quando parla del ponte glutei» → da «il ponte per i glutei» (prima c'era la fine del mountain climber)
      segments: cut([275.5, 319.24]),
      elements: [
        // tempi rifatti sul nuovo inizio (275,5 s del sorgente): l'intestazione «2 · Ponte per i glutei» copre la prima frase, poi le grafiche
        { kind: "gem", art: "bridge", at: 5.5, word: "lavoriamo", dur: 14.2, cues: ["postura", "estensione", "recuperiamo"], phases: [{ lines: ["Postura"] }, { lines: ["Estensione", "delle anche"] }, { lines: ["Recuperi", "e lavori"] }], artCues: [0, 1] },
        { kind: "gem", art: "bridge", at: 23.4, dur: 12.0, cues: ["seduto", "sveglio", "flessione", "fermo"], phases: [{ lines: ["Sei stato", "seduto?"] }, { lines: ["O appena", "sveglio?"] }, { lines: ["Corpo in", "flessione"] }, { lines: ["Fermo e", "immobile"] }], artCues: [-1, -1, 0] },
        { kind: "dose", at: 36.5, dur: 8.0, cues: ["dinamico", "statico", "30", "minuto"], tags: ["Dinamico", "Statico"], items: ["30 sec", "1 min"] },
      ],
      cta: GUIDA_CIRCUITO,
    },
    didascalia: CAP(`Secondo esercizio del circuito di riscaldamento in casa: il ponte per i glutei.

Anche qui si lavora sulla postura: si va in estensione con le anche e con il bacino, e intanto si recupera dall'esercizio precedente senza fermarsi.

È prezioso soprattutto se vai a correre dopo essere stato seduto o appena sveglio, cioè dopo ore in posizioni di flessione o con il corpo fermo. Puoi farlo dinamico oppure statico, per 30 secondi o un minuto.`, GUIDA_C),
  },
  {
    id: "G7-affondi",
    title: "Riscaldamento in casa: affondi",
    cover: { frame: 270, shiftY: -0.17, kicker: KICKER_W, lines: ["Esercizio 3:", "gli affondi"], accent: "gli affondi" },
    props: {
      ...base,
      ...WIN,
      winHeader: { kicker: KICKER_W, title: "Affondi", n: "3" },
      master: master("G7-affondi"),
      segments: cut([319.4, 370.06]),
      elements: [
        { kind: "gem", art: "lunge", at: 4.4, word: "affondo", dur: 6.4, cues: ["affondo", "coordinata"], phases: [{ lines: ["Affondi"] }, { lines: ["Coordinati", "e gentili"] }], artCues: [0] },
        { kind: "gem", art: "lunge", at: 12.0, word: "non", dur: 7.6, cues: ["male", "dall'interno", "muscolatura"], phases: [{ lines: ["Senza", "farsi male"] }, { lines: ["Caldi", "dall'interno"] }, { lines: ["Muscoli", "attivi"] }], artCues: [-1, 1] },
        { kind: "gem", art: "lunge", at: 33.4, word: "fanno", dur: 10.0, cues: ["tutto", "inferiore", "temperatura"], phases: [{ lines: ["Lavora", "tutto il corpo"] }, { lines: ["Parte", "inferiore"] }, { lines: ["Sale la", "temperatura"] }], artCues: [-1, -1, 2] },
        { kind: "gem", art: "lunge", at: 46.9, word: "non", dur: 2.4, cues: ["minuto"], phases: [{ lines: ["Massimo", "un minuto"] }], artCues: [-1, -1, -1, 0] },
        // a 49,72 il sorgente passa alla posa del jumping jack (un secondo prima della fine): l'ultima frase va sopra la scheda «da ricordare»
        { kind: "takeaway", at: 49.4, dur: 1.55, lines: ["Lo scopo?", "Solo scaldarsi"], accent: "Solo scaldarsi" },   // senza disegno (24/11: niente omini)
      ],
      cta: GUIDA_CIRCUITO,
    },
    didascalia: CAP(`Terzo esercizio del circuito di riscaldamento in casa: ci si alza e si fa qualche affondo, sempre in maniera coordinata e gentile.

Qui non devi rischiare di farti male: stai scaldando il corpo dall'interno, attivando la muscolatura e facendo capire al corpo che tra poco gli chiederai un po' di performance.

Gli affondi fanno lavorare bene tutto il corpo, soprattutto la parte inferiore, e alzano la temperatura interna. Non superare il minuto: lo scopo non è affaticarsi, è solo scaldarsi.`, GUIDA_C),
  },
  {
    id: "G8-jack",
    title: "Riscaldamento in casa: jumping jack",
    cover: { frame: 45, shiftY: -0.17, kicker: KICKER_W, lines: ["Esercizio 4:", "jumping jack"], accent: "jumping jack" },
    props: {
      ...base,
      ...WIN,
      winHeader: { kicker: KICKER_W, title: "Jumping|jack", n: "4" },
      winFeatherTop: 40, // nella parte parlata la testa di Daniele arriva vicino al bordo alto: sfumatura corta, i capelli non si velano
      master: master("G8-jack"),
      segments: cut([370.36, 404.06]),
      elements: [
        { kind: "gem", art: "jack", at: 2.6, word: "jumping", dur: 17.8, cues: ["temperatura", "tendini", "30", "sudando", "pronto"], phases: [{ lines: ["Più", "temperatura"] }, { lines: ["Scalda", "i tendini"] }, { lines: ["30 secondi", "o un minuto"] }, { lines: ["Quasi", "sudato"] }, { lines: ["Pronto", "a uscire"] }], artCues: [0, 1, 3] },
        { kind: "gem", art: "jack", at: 21.6, word: "mettere", dur: 12.0, cues: ["giacca", "guanti", "cappello", "estremo", "guanti"], phases: [{ lines: ["Giacca", "antivento"] }, { lines: ["Guanti"] }, { lines: ["Cappello", "e fascia"] }, { lines: ["Freddo non", "estremo?"] }, { lines: ["Solo guanti", "e fascia"] }], artCues: [-1, -1, -1, 0, 1, 2] },
      ],
      cta: GUIDA_CIRCUITO,
    },
    didascalia: CAP(`Ultimo esercizio del circuito di riscaldamento in casa: finiti gli affondi, qualche jumping jack.

Alzano la temperatura corporea e scaldano anche i tendini. Trenta secondi o un minuto, vedi tu: alla fine sei già quasi sudato e pronto a uscire.

Se fa molto, molto freddo metti giacca antivento, guanti, cappello e fascia. Se è freddo ma non estremo puoi uscire anche così, solo con guanti e fascia.`, GUIDA_C),
  },
  {
    id: "G9-graduale",
    title: "La corsa di riscaldamento",
    cover: { frame: 1106, kicker: KICKER, lines: ["La corsa", "di riscaldamento"], accent: "di riscaldamento" },
    props: {
      ...base,
      master: master("G9-graduale"),
      segments: cut([404.14, 463.98]),
      elements: [
        // 24/11 (Ross): apertura a tutto schermo «Quando corriamo al freddo…» prima del video (campo `intro`), corridore 3D al passo con
        // l'intensità bassa e poi in corsa leggera con la batteria piena
        { kind: "kin", anim: "pulse", at: 6.4, word: "proprio", dur: 2.3, cues: ["corsa", "riscaldamento"], words: ["Corsa di", "riscaldamento"] },
        { kind: "gem", dy: -10, art: "passo3d", at: 9.1, word: "corsa", dur: 13.2, cues: ["intensità", "camminata", "tendini", "nervoso"], phases: [{ lines: ["Intensità", "molto bassa"] }, { lines: ["Al passo della", "camminata"] }, { lines: ["Tendini,", "articolazioni", "e muscoli"] }, { lines: ["Sistema", "nervoso"] }] },
        // «Ma c'è di più» cade su un primo piano (mento a 0,50): niente schianto, parole grandi appena sotto, da «più»
        { kind: "kin", anim: "pulse", dy: 20, at: 23.1, word: "più", dur: 2.3, cues: ["più"], words: ["C'è di più"] },
        { kind: "gem", dy: -11, art: "energia3d", at: 27.7, word: "permette", dur: 17.2, cues: ["energia", "attivo", "sprecare", "godersi"], phases: [{ lines: ["Energia", "più efficiente"] }, { lines: ["Già attivo", "e pronto"] }, { lines: ["Niente energia", "sprecata"] }, { lines: ["Dall'inizio", "alla fine"] }] },
        { kind: "ticks", at: 47.0, word: "riscaldati", dur: 11.8, cues: ["riscaldati", "primi", "pronto"], items: ["Prima: scaldati", "Fuori: graduale"], foot: "Pronto e carico" },
      ],
      intro: { seconds: 1.7, kicker: "La corsa di riscaldamento", lines: ["Quando corriamo", "al freddo…"], accent: "al freddo…" },
      zooms: [{ at: 0.2, dur: 6.0, scale: 1.06 }, { at: 25.3, dur: 2.3, scale: 1.06 }],
      cta: { word: PAROLA, title: "Vuoi goderti la corsa dall'inizio alla fine?" },
    },
    didascalia: CAP(`Una volta uscito, aggiungi un breve periodo di camminata o una corsa molto leggera: la corsa di riscaldamento. È una corsa a intensità molto bassa, anche alla stessa velocità della camminata, che prepara tendini, articolazioni e muscoli e fa capire al sistema nervoso che l'allenamento sta cominciando.

C'è di più: ti permette di usare la tua energia in modo più efficiente. Entri nella parte intensa dell'allenamento già attivo e pronto, invece di sprecare energia per scaldarti nei primi chilometri. Ed è questo che fa la differenza per goderti la corsa dall'inizio alla fine, anche nelle giornate più fredde.

Ricapitolando: scaldati bene prima di uscire e nei primi minuti fai un riscaldamento graduale. Anche se fuori fa molto freddo sarai pronto e carico, invece di lottare per scaldarti strada facendo.`, COACH("Vuoi goderti la corsa dall'inizio alla fine?", PAROLA)),
  },
  {
    id: "G10-naso",
    title: "Come respirare quando fa freddo",
    cover: { frame: 1456, kicker: KICKER, lines: ["Aria fredda?", "Respira dal naso"], accent: "Respira dal naso" },
    props: {
      ...base,
      master: master("G10-naso"),
      segments: cut([472.52, 524.5]),
      elements: [
        { kind: "fog", anim: "fog", at: 0.1, dur: 3.4, lines: ["Come respirare", "quando fa freddo"], accent: "quando fa freddo" },
        // 24/11 (Ross: «le animazioni sono orribili, aggiungine in 3D»): testa 3D di profilo con l'aria che entra (gelida dalla bocca, poi
        // dal naso dove si scalda, si umidifica e viene filtrata), gelo sui bordi su «aria tagliente»
        { kind: "chips", at: 4.2, word: "tendini", dur: 2.4, cues: ["tendini", "muscoli", "articolazioni"], items: ["Tendini", "Muscoli", "Articolazioni"] },
        { kind: "kin", anim: "slide", at: 6.8, word: "anche", dur: 4.1, cues: ["anche", "respirare"], words: ["Ma anche", "il respiro"] },
        { kind: "gem", dy: -19, art: "nasofreddo3d", at: 12.3, word: "sentire", dur: 6.5, cues: ["fastidio", "aria"], phases: [{ lines: ["Fastidio", "nei polmoni"] }, { lines: ["Aria", "tagliente"] }], artCues: [] },
        { kind: "ambient", mood: "frost", at: 15.4, word: "aria", dur: 3.0 },
        { kind: "kin", anim: "pulse", at: 29.4, word: "controllata", dur: 2.6, cues: ["controllata", "piacevole"], words: ["Controllata", "e piacevole"] },
        { kind: "gem", dy: -19, art: "naso3d", at: 33.2, word: "imparare", dur: 7.4, cues: ["naso", "riscaldare", "umidificare"], phases: [{ lines: ["Respira", "dal naso"] }, { lines: ["Riscalda", "l'aria"] }, { lines: ["Umidifica", "l'aria"] }], artCues: [1, 2] },
        // da 40,8 a 44,9 il sorgente è in primo piano (mento a 0,53): niente grafica, solo sottotitoli
        { kind: "gem", dy: -19, art: "nasofiltro3d", at: 45.2, word: "ebbene", dur: 6.2, cues: ["naturale", "filtrarla", "proteggere"], phases: [{ lines: ["Il modo", "naturale"] }, { lines: ["La filtra"] }, { lines: ["Protegge", "le vie", "respiratorie"] }], artCues: [1, 2] },
      ],
      zooms: [{ at: 19.0, dur: 4.0, scale: 1.07 }],
      cta: { word: PAROLA, title: "Vuoi respirare bene anche al freddo?" },
    },
    didascalia: CAP(`Correre al freddo non mette alla prova solo tendini, muscoli e articolazioni, ma anche la capacità di respirare in modo confortevole e fluido. Se ti è capitato di sentire un fastidio nei polmoni o quella sensazione di aria tagliente durante la corsa invernale, non sei solo: è una cosa che scoraggia molti corridori.

Con il giusto approccio quella sensazione di disagio può diventare una respirazione controllata e piacevole. Il primo consiglio è imparare a respirare dal naso.

Il naso riscalda e umidifica l'aria prima che arrivi ai polmoni, riducendo l'impatto dell'aria fredda sul sistema respiratorio. È il modo naturale per riscaldare l'aria, filtrarla e proteggere le vie respiratorie.`, COACH("Vuoi respirare bene anche al freddo?", PAROLA)),
  },
  {
    id: "G11-respiro",
    title: "Niente affanno: respirazione controllata",
    cover: { frame: 494, kicker: KICKER, lines: ["Naso e corsa:", "niente affanno"], accent: "niente affanno" },
    props: {
      ...base,
      master: master("G11-respiro"),
      segments: cut([524.56, 567.9]),
      elements: [
        // 24/11: corridore 3D in corsa leggera con l'onda del respiro (regolare = verde; l'affanno = rossa e irregolare)
        { kind: "gem", dy: -19, art: "respiro3d", at: 0.15, dur: 6.9, cues: ["difficile"], phases: [{ lines: ["Solo dal naso", "mentre corri"], on: -1 }, { lines: ["Solo dal naso", "mentre corri"], chip: "Difficile?", on: 0 }], artCues: [-1, -1] },
        { kind: "kin", anim: "slide", at: 10.4, word: "davvero", dur: 2.4, cues: ["grande", "differenza"], words: ["Grande", "differenza"] },
        { kind: "gem", dy: -19, art: "respiro3d", at: 13.05, dur: 16.1, cues: ["controllata", "fretta", "intensità", "costante", "affanno"], phases: [{ lines: ["Controllata", "e regolare"] }, { lines: ["Niente fretta", "all'inizio"] }, { lines: ["Intensità", "bassa"] }, { lines: ["Intensità", "costante"] }, { lines: ["Mai in", "affanno"] }], artCues: [4, -1] },
        { kind: "gem", dy: -19, art: "respiro3d", at: 34.6, word: "dà", dur: 8.2, cues: ["padronanza", "esperienza"], phases: [{ lines: ["Padronanza", "e sicurezza"] }, { lines: ["Esperienza", "gratificante"] }], artCues: [-1, 0] },
      ],
      zooms: [{ at: 7.3, dur: 3.0, scale: 1.06 }, { at: 29.3, dur: 5.1, scale: 1.07 }],
      cta: { word: PAROLA, title: "Vuoi correre senza andare in affanno?" },
    },
    didascalia: CAP(`Lo so: respirare solo dal naso mentre corri può sembrare difficile, soprattutto se non sei abituato. Ma respirare esclusivamente dal naso può fare davvero una grande differenza.

Mantieni la respirazione controllata e regolare e non farti prendere dalla fretta nei primi minuti, quando il corpo si sta ancora adattando. Parti sempre a un'intensità bassa e costante, e stai attento a non andare in affanno fin da subito.

Respirare bene non rende solo più confortevole la corsa al freddo: ti dà una sensazione di padronanza e sicurezza, e trasforma quella che sembrava una sfida insormontabile in un'esperienza gratificante.`, COACH("Vuoi correre senza andare in affanno?", PAROLA)),
  },
  {
    id: "G12-squat",
    title: "Dopo la corsa: lo squat naturale",
    cover: { frame: 950, kicker: KICKER, lines: ["Dopo la corsa:", "squat naturale"], accent: "squat naturale" },
    props: {
      ...base,
      master: master("G12-squat"),
      segments: cut([609.58, 653.28]),
      elements: [
        { kind: "fog", anim: "snap", at: 0.1, dur: 4.0, lines: ["Dopo la corsa:", "il movimento più potente"], accent: "il movimento più potente" },
        // 24/11: corridore 3D che scende nello squat naturale profondo (una volta, su «squat») e ci resta
        { kind: "gem", dy: -19, art: "squat3d", at: 4.9, word: "per", dur: 12.5, cues: ["squat", "ambiente"], phases: [{ lines: ["Il movimento", "più potente"], on: -1 }, { lines: ["Squat", "naturale"], on: 0 }, { lines: ["Al chiuso", "o al riparo"], on: 1 }] },
        { kind: "gem", dy: -19, art: "squatgiu3d", at: 20.3, word: "solo", dur: 9.5, cues: ["recupero", "manutenzione", "indolenzimenti"], phases: [{ lines: ["Migliora", "il recupero"] }, { lines: ["Fa", "manutenzione"] }, { lines: ["Meno", "indolenzimenti"] }] },
        { kind: "kin", anim: "slide", at: 31.0, word: "dedicare", dur: 2.7, cues: ["pochi", "minuti"], words: ["Pochi minuti", "al recupero"] },
        { kind: "gem", dy: -19, art: "squatgiu3d", at: 34.0, word: "bastano", dur: 9.0, cues: ["3-4", "investimento", "qualità"], phases: [{ lines: ["Bastano", "3-4 minuti"] }, { lines: ["Investimento", "che ripaga"] }, { lines: ["Qualità", "e salute"] }] },
      ],
      zooms: [{ at: 17.6, dur: 2.6, scale: 1.06 }],
      cta: { word: PAROLA, title: "Vuoi recuperare meglio dopo la corsa?" },
    },
    didascalia: CAP(`Il movimento più potente che puoi fare dopo la corsa? Per me è lo squat naturale.

Quando le temperature sono molto basse, defaticamento e stretching vanno fatti in un ambiente chiuso, o almeno riparato. Questo piccolo rituale dopo la corsa migliora il recupero e fa la manutenzione che serve a prevenire quegli indolenzimenti che affliggono tanti corridori.

Bastano 3-4 minuti di squat naturale: pochi minuti dedicati al recupero sono un investimento che ti ripaga nella qualità delle tue corse e nella salute del tuo corpo.`, COACH("Vuoi recuperare meglio dopo la corsa?", PAROLA)),
  },
];
