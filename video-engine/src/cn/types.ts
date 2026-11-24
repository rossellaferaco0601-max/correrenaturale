import type { Caption } from "@remotion/captions";

export type Seg = { from: number; to: number };

/** Ogni elemento vive nella zona grafiche (y 0,47-0,74), uno alla volta. `word` aggancia l'inizio alla parola detta più vicina ad `at`. */
/** `cues`: parole dette (in ordine) a cui agganciare le parti interne della grafica (righe di un elenco, cambio di stato): diventano `onAt`
 *  (secondi dall'inizio dell'elemento), calcolati sui tempi reali delle parole. */
/** `dy`: sposta in basso (px) una grafica della zona grafiche, per i primi piani in cui il mento scende sotto il bordo normale;
 *  `hideCaps`: mentre la grafica è a schermo i sottotitoli si spengono (in basso un solo testo alla volta, Ross 12/11). */
/** `shiftAt` / `shiftDy`: da quel secondo (dall'inizio della grafica) la grafica scende di altri `shiftDy` px (cambio di inquadratura con il volto più
 *  grande); `hideCapsFrom`: da quel secondo i sottotitoli si spengono (in basso un solo testo alla volta). */
export type ElementBase = { at: number; dur: number; word?: string; cues?: string[]; onAt?: number[]; dy?: number; hideCaps?: boolean; shiftAt?: number; shiftDy?: number; hideCapsFrom?: number };

export type Element = ElementBase &
  (
    | { kind: "kinetic"; words: string[]; accentIndex?: number }
    | { kind: "widget"; title: string; lines: string[] }
    | { kind: "stat"; value: string; label: string }
    | { kind: "pill"; text: string }
    | { kind: "stage"; title: string; keyword: string; steps: string[] }
    | { kind: "checklist"; items: string[]; strike?: boolean; cross?: boolean; big?: boolean }
    | { kind: "text3d"; word3d: string; sub?: string }
    | { kind: "wave"; title: string; mode: "chaos" | "calm" | "chaos-to-calm" | "calm-to-chaos" }
    | { kind: "sphere3d"; phases: { label: string; sec: number; scale: number }[] }
    | { kind: "gauge3d"; title: string; from: number; to: number; labels: string[] }
    | { kind: "ecg"; title: string; bpmFrom: number; bpmTo: number }
    | { kind: "steps"; inhale: number; exhale: number }
    | { kind: "bars"; title: string; labels: string[]; values: number[] }
    | { kind: "stairs"; title: string; steps?: number }
    | { kind: "split"; lines: string[]; accent: string }
    | { kind: "graph"; title: string; label: string; from: number; to: number; unit?: string }
    | { kind: "toggles"; title: string; items: string[] }
    | { kind: "title"; lines: string[]; accent?: string }
    | { kind: "mouth"; lines: string[] }
    | { kind: "runner"; fast: string; slow: string; bpmFrom: number; bpmTo: number }
    | { kind: "lungs"; title: string; sub?: string }
    | { kind: "horizon"; title: string; kmTo: number }
    | { kind: "chat"; sender: string; messages: string[] }
    | { kind: "bigstrike"; text: string; big?: boolean }
    | { kind: "stack"; title: string; items: string[] }
    | { kind: "guide"; mode: "ritmica" | "nasale" | "hold"; title?: string; titleSec?: number; inhale?: number; exhale?: number; hold?: number; breaths?: number }
    | { kind: "metronome"; title: string; inhale: number; exhale: number; bpm?: number }
    | { kind: "pair"; title: string; sub: string; items: [{ def: string; name: string }, { def: string; name: string }]; fadeIn?: number; fadeOut?: number }
    | { kind: "lifebar"; place: string; title: string; total: number; healthy: number; decline: string; declineSub: string; focus: string; focusNot: string; focusIs: string; fadeIn?: number; fadeOut?: number }
    | { kind: "slides"; header?: string; source?: string; fadeIn?: number; fadeOut?: number; steps: { g: number; kind: "stat" | "text" | "chip"; value?: string; label?: string; lines?: string[]; accent?: number; color?: "lime" | "coral" }[] }
    | { kind: "flow"; title: string; sub: string; inputs: [string, string]; output: string; outSub?: string }
    | { kind: "renew"; term: string; sub: string; oldLabel: string; newLabel: string; fadeIn?: number; fadeOut?: number }
    | { kind: "versus"; header: string; title: string; a: { label: string; value: string }; b: { label: string; value: string }; final: string[]; finalAccent?: number; source?: string; fadeIn?: number; fadeOut?: number }
    | { kind: "grid4"; items: string[]; foot: string }
    | { kind: "plan"; n: number; kicker: string; pre?: string; title: string[]; points: string[]; foot?: string; art: "walk" | "run" | "timer"; fadeIn?: number; fadeOut?: number }
    | { kind: "lights"; title: string; items: string[] }
    | { kind: "pointer"; text: string; accent?: string; arrow?: boolean; y?: number }
    | { kind: "cycle"; items: string[] }
    | { kind: "topword"; lines: string[]; accent?: string; anim?: "pop" | "drop"; zone?: "top" | "strip"; y?: number; max?: number }
    | { kind: "counter"; to: number; from?: number; prefix?: string; suffix?: string; decimals?: number; label: string }
    | { kind: "wall"; rows: string[]; title?: string; hold?: boolean }
    | { kind: "side"; title?: string; items?: string[]; map?: "it-na" | "na-it"; pairs?: boolean }
    | { kind: "beat"; bpm: number; label: string; tone?: "lime" | "coral" }
    | { kind: "fulltext"; lines: string[]; accentIndex?: number; fadeIn?: number; fadeOut?: number }
    | { kind: "clip"; src: string; from?: number; tag: string; text: string; posY?: number }
    | { kind: "step"; n: string; label: string; sub: string; strike: string }
    | { kind: "airflow"; lines: [string, string] }
    | { kind: "filter" }
    | { kind: "beats"; words: [string, string] }
    | { kind: "ring"; words: [string, string] }
    | { kind: "duo"; title: string; words: [string, string] }
    | { kind: "slam"; lead: string[]; text: string }
    | { kind: "orbit"; titles: string[]; headX: number; headTop: number; back?: number }
    | { kind: "compare"; sides: [{ q: string; a: string }, { q: string; a: string }] }
    | { kind: "drill"; n: number; title: string; fadeIn?: number; fadeOut?: number; steps: { label: string; sub: string; shape: "hold" | "grow" | "shrink" | "ring" | "feet" | "pulse" | "count"; color?: "lime" | "az" | "cream"; n?: number; big?: string }[] }
    | { kind: "question"; text: string; label?: string }
    | { kind: "nametag"; name: string; sub?: string }
    | { kind: "loop"; title: string; items: string[] }
    | { kind: "drain"; title: string; items: string[]; fill?: boolean }
    | { kind: "stamp"; lines: string[]; stamp: string; tone?: "lime" | "coral" }
    | { kind: "chips"; items: string[]; strike?: boolean }
    | { kind: "switches"; title: string; items: string[] }
    | { kind: "pressure"; title: string; label: string; end: string }
    | { kind: "journey"; title: string; items: string[] }
    | { kind: "progress"; title: string; label: string; after: string; zero: string }
    | { kind: "scale2"; title: string; left: string; right: string; from?: "tilted"; phase?: number }
    | { kind: "receipt"; title: string; items: string[] }
    | { kind: "bill"; title: string; items: string[]; total: string }
    | { kind: "quad"; items: string[]; foot?: string }
    | { kind: "rise"; label: string; lines: string[] }
    | { kind: "fog"; lines: string[]; accent?: string; anim?: "fog" | "rise" | "snap" | "wind" | "type" }
    | { kind: "gem"; art: "nose" | "heat" | "house" | "over" | "warm" | "battery" | "breath" | "squat" | "climber" | "bridge" | "lunge" | "jack" | "gauge" | "over3d" | "warm3d" | "warmok3d" | "mani3d" | "casa3d" | "passo3d" | "energia3d" | "nasofreddo3d" | "naso3d" | "nasofiltro3d" | "respiro3d" | "squat3d" | "squatgiu3d"; phases: { lines: string[]; chip?: string; on?: number }[]; artCues?: number[] }
    | { kind: "kin"; words: string[]; anim: "ice" | "pulse" | "slide" }
    | { kind: "ambient"; mood: "frost" | "heat" }
    | { kind: "takeaway"; lines: string[]; accent?: string; kicker?: string; art?: string }
    | { kind: "dose"; tags?: string[]; items: string[] }
    | { kind: "ticks"; items: string[]; foot?: string }
    | { kind: "layers"; stage: 1 | 2 | 3; lines: string[]; chips: string[] }
    | { kind: "hangtag"; lines: string[] }
    | { kind: "gust"; words: string[] }
    | { kind: "rings"; phases: string[][] }
    | { kind: "duel"; left: string; right: string }
    | { kind: "road3d"; title: string; fromLabel: string; toLabel: string; fromSpeed: number; toSpeed: number; unit?: string }
  );

export type Hook = { lines: string[]; keyword: string; dur: number };

/** Effetto della skill `effects` (fx.py) applicato al master prima di Remotion. `wide`: durante l'effetto il master
 *  arretra (campo largo con sfondo sfocato) per lasciare spazio sopra la testa. Le altre chiavi passano a fx.py. */
export type Fx = { fx: string; at: number; dur: number; word?: string; wide?: boolean; [k: string]: unknown };

/** `offer` = le righe dentro la targhetta lime (default: «coaching personalizzato / di Correre Naturale®»); con una GUIDA da scaricare
 *  (Ross 21/11: «devono commentare per avere una guida di approfondimento») si mettono qui il titolo della guida, in `sub` «Scarica gratis
 *  la guida» e in `dm` il testo della notifica («Ti mando la guida»). */
export type CTA = { word: string; title: string; sub?: string; offer?: string[]; dm?: string };

export type CNReelProps = {
  /** master 1080x1920 già montato (scripts/cn_master.py) */
  master: string;
  /** sorgente originale (per export/metadata) */
  src: string;
  segments: Seg[];
  words: Caption[];
  /** hook in scatola sotto il mento; null se l'hook è affidato a un effetto */
  hook: Hook | null;
  elements: Element[];
  fx?: Fx[];
  cta: CTA;
  /** reel «a finestra» (video orizzontale a tutta larghezza su fondo verde, master con `window`): intestazione fissa nella fascia sopra la
   *  finestra, visibile quando non c'è una grafica. `title` può andare su due righe con «|». */
  winHeader?: { kicker: string; title: string; n?: string };
  wordFix: Record<string, string>;
  blendFrames: number;
  ctaSeconds: number;
  /** compensazione del ritardo di Whisper, in secondi (negativo = anticipa) */
  wordOffset: number;
  /** push-in lento della camera durante l'hook (es. 1.12), poi rientro morbido */
  hookZoom?: number;
  /** volto grande (interviste strette): grafiche più in basso (px) e più piccole, sottotitoli più in basso (px), per non coprire mai il volto */
  /** coda prima della CTA (s, default 0,5): fermo sull'ultimo fotogramma con leggerissimo avvicinamento; più lunga = la CTA entra più tardi e più morbida */
  tailSeconds?: number;
  /** secondi di coda in cui il sorgente continua dal vivo (default: tutta la coda). Se subito dopo il taglio il sorgente cambia inquadratura, va messo a 0: la coda tiene l'ultimo fotogramma mentre il pannello della CTA sale */
  tailLive?: number;
  /** secondi di coda che passano prima che la CTA cominci a salire (default 0: parte al taglio). Serve con una coda più lunga (`tailSeconds`)
   *  per lasciare un respiro dopo l'ultima parola; nel master la coda va fatta con `ping` (niente fermo immagine) */
  tailHold?: number;
  /** secondi iniziali senza sottotitoli (Oscar 12/11: «la parte iniziale dove c'è l'hook visivo togliamo i sottotitoli»): ripartono dalla prima pagina intera dopo questo tempo */
  capFrom?: number;
  /** la CTA comincia a salire questi secondi PRIMA della fine del parlato e finisce di coprire nella coda (Ross 24/11: prima della CTA non
   *  deve restare né un «parlato muto» né uno stacco netto). Con questo campo la salita è morbida (12 fotogrammi, accelera e rallenta). */
  ctaLead?: number;
  /** avvicinamenti lenti della camera sul video nei passaggi senza grafica (Ross 24/11: «non vedo nessun effetto», «poco dinamico»):
   *  da `at` (secondi del reel) per `dur` secondi il video arriva a `scale` e torna a 1 negli ultimi 14 fotogrammi; perno sul volto */
  zooms?: { at: number; dur: number; scale: number }[];
  /** apertura a tutto schermo PRIMA del video (Ross 24/11, G9: «metti un'introduzione tipo "quando corriamo al freddo" e poi parti con il video») */
  intro?: { seconds: number; kicker?: string; lines: string[]; accent?: string };
  /** corpo dei sottotitoli (default 64) */
  capSize?: number;
  /** reel «a finestra»: bordi alto e basso del video sfumati nel verde del fondo, in px (Ross 24/11) */
  winFeather?: number;
  /** sfumatura del solo bordo alto, se diversa (G8: quando Daniele parla in piedi la testa arriva vicino al bordo e non deve velarsi) */
  winFeatherTop?: number;
  /** banner fisso per tutto il reel (Ross 24/11, G4): invito a commentare la parola per ricevere qualcosa; sta nella fascia `y` (px) */
  banner?: { word: string; text: string[]; y: number };
  /** selfie: in basso un solo testo alla volta. Mentre è a schermo una grafica della fascia bassa i sottotitoli si spengono (Ross 12/11: «titoli sovrapposti») */
  capHideOnGfx?: boolean;
  gfxShift?: number;
  gfxScale?: number;
  capShift?: number;
};

export const BRAND = {
  green: "#49762E",
  az: "#B8D7EA",
  cream: "#F4F1E5",
  ink: "#0B0F0A",
  lime: "#95FF00",
  white: "#FFFFFF",
};

export const FPS = 30;
/** coda del master: 0,5 s di fermo immagine muto, su cui entra la CTA */
export const TAIL_FRAMES = 15;
export const W = 1080;
export const H = 1920;
/** zone (frazioni dell'altezza): volto libero sopra 0,45; grafiche; sottotitoli */
/** Zone (frazioni dell'altezza), dentro l'area sicura dei Reel: sopra 0,80 niente di importante (comandi Instagram), a destra x < 0,90. */
export const ZONE = { faceBottom: 0.42, gfxTop: 0.44, gfxBottom: 0.67, capTop: 0.69, capBottom: 0.78 };
/** pannelli delle grafiche: margini simmetrici, lontani dalla colonna dei comandi a destra */
export const PANEL_X = 100;
export const PANEL_W = 880;
export const GFX_TOP = Math.round(H * ZONE.gfxTop);
export const GFX_H = Math.round(H * (ZONE.gfxBottom - ZONE.gfxTop));
