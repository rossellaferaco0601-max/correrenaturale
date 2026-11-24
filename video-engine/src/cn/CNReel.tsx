import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig, interpolate, useCurrentFrame, Easing } from "remotion";
import { loadFont } from "@remotion/google-fonts/Blinker";
import { useMemo } from "react";
import type { CNReelProps, Element } from "./types";
import { FPS, TAIL_FRAMES, H } from "./types";
import { layout, remapWords, resolveStart, resolveCues, secToFrames, tailFrames } from "./timeline";
import { Captions } from "./Captions";
import { Hook } from "./Hook";
import { ElementView } from "./Elements";
import { Text3D, Wave, Sphere3D, Gauge3D, ECG, Steps, Bars } from "./Elements3D";
import { CTA } from "./CTA";
import { Stairs, SplitCard, splitCamera, SPLIT_CARD_H, Metronome, Road3D, Graph, Toggles } from "./Elements2";
import { Clip, Compare, Step, Airflow, Filter, Beats, Ring, Duo, Slam, Orbit, Drill, slamImpact, slamShake, orbitCam } from "./Elements5";
import { Pair, Lifebar, Fulltext, Slides } from "./Elements6";
import { Flow, Renew, Versus, Grid4, Plan, Lights, Cycle, Beat } from "./Elements7";
import { TopWord, Counter, BigPointer, Wall, Side, SIDE, sideK } from "./Elements8";
import { Fog, Layers, HangTag, Gust, Rings, Duel, Gem, WinHeader, Kin, Dose, Ticks, Takeaway, Banner, Ambient, Intro } from "./Elements10";
import { Loop, Drain, Progress, Scale2, Stamp, Chips, Switches, Pressure, Journey, Receipt, Bill, Quad, Rise } from "./Elements9";
import { Title, Mouth, Runner, Lungs, Horizon, Chat, BigStrike, Stack, Guide, Question, NameTag } from "./Elements4";

loadFont("normal", { weights: ["600", "700", "800", "900"], subsets: ["latin"] });

/** elementi che occupano tutto il fotogramma: fuori dallo spostamento/scala della zona grafiche */
// fuori dalla zona grafiche (non si spostano né si rimpiccioliscono con gfxShift/gfxScale): schede a tutto schermo e, nei selfie, le parole
// sopra la testa, il richiamo alla CTA, il muro di parole e il pannello laterale
const FULLSCREEN = new Set<Element["kind"]>(["orbit", "drill", "guide", "pair", "lifebar", "fulltext", "slides", "renew", "versus", "plan", "topword", "pointer", "wall", "side", "bill", "takeaway", "ambient"]);

const AnyElement: React.FC<{ el: Element; start: number }> = ({ el, start }) => {
  switch (el.kind) {
    case "text3d": return <Text3D el={el} start={start} />;
    case "wave": return <Wave el={el} start={start} />;
    case "sphere3d": return <Sphere3D el={el} start={start} />;
    case "gauge3d": return <Gauge3D el={el} start={start} />;
    case "ecg": return <ECG el={el} start={start} />;
    case "steps": return <Steps el={el} start={start} />;
    case "bars": return <Bars el={el} start={start} />;
    case "stairs": return <Stairs el={el} start={start} />;
    case "split": return <SplitCard el={el} start={start} />;
    case "metronome": return <Metronome el={el} start={start} />;
    case "road3d": return <Road3D el={el} start={start} />;
    case "graph": return <Graph el={el} start={start} />;
    case "toggles": return <Toggles el={el} start={start} />;
    case "title": return <Title el={el} start={start} />;
    case "mouth": return <Mouth el={el} start={start} />;
    case "runner": return <Runner el={el} start={start} />;
    case "lungs": return <Lungs el={el} start={start} />;
    case "horizon": return <Horizon el={el} start={start} />;
    case "chat": return <Chat el={el} start={start} />;
    case "bigstrike": return <BigStrike el={el} start={start} />;
    case "stack": return <Stack el={el} start={start} />;
    case "guide": return <Guide el={el} start={start} />;
    case "question": return <Question el={el} start={start} />;
    case "pair": return <Pair el={el} start={start} />;
    case "lifebar": return <Lifebar el={el} start={start} />;
    case "fulltext": return <Fulltext el={el} start={start} />;
    case "slides": return <Slides el={el} start={start} />;
    case "flow": return <Flow el={el} start={start} />;
    case "renew": return <Renew el={el} start={start} />;
    case "versus": return <Versus el={el} start={start} />;
    case "grid4": return <Grid4 el={el} start={start} />;
    case "plan": return <Plan el={el} start={start} />;
    case "lights": return <Lights el={el} start={start} />;
    case "pointer": return <BigPointer el={el} start={start} />;
    case "topword": return <TopWord el={el} start={start} />;
    case "counter": return <Counter el={el} start={start} />;
    case "wall": return <Wall el={el} start={start} />;
    case "side": return <Side el={el} start={start} />;
    case "cycle": return <Cycle el={el} start={start} />;
    case "beat": return <Beat el={el} start={start} />;
    case "clip": return <Clip el={el} start={start} />;
    case "compare": return <Compare el={el} start={start} />;
    case "step": return <Step el={el} start={start} />;
    case "airflow": return <Airflow el={el} start={start} />;
    case "filter": return <Filter el={el} start={start} />;
    case "beats": return <Beats el={el} start={start} />;
    case "ring": return <Ring el={el} start={start} />;
    case "duo": return <Duo el={el} start={start} />;
    case "slam": return <Slam el={el} start={start} />;
    case "orbit": return <Orbit el={el} start={start} />;
    case "drill": return <Drill el={el} start={start} />;
    case "nametag": return <NameTag el={el} start={start} />;
    case "loop": return <Loop el={el} start={start} />;
    case "drain": return <Drain el={el} start={start} />;
    case "progress": return <Progress el={el} start={start} />;
    case "scale2": return <Scale2 el={el} start={start} />;
    case "stamp": return <Stamp el={el} start={start} />;
    case "chips": return <Chips el={el} start={start} />;
    case "switches": return <Switches el={el} start={start} />;
    case "pressure": return <Pressure el={el} start={start} />;
    case "journey": return <Journey el={el} start={start} />;
    case "receipt": return <Receipt el={el} start={start} />;
    case "bill": return <Bill el={el} start={start} />;
    case "quad": return <Quad el={el} start={start} />;
    case "rise": return <Rise el={el} start={start} />;
    case "fog": return <Fog el={el} start={start} />;
    case "gem": return <Gem el={el} start={start} />;
    case "kin": return <Kin el={el} start={start} />;
    case "takeaway": return <Takeaway el={el} start={start} />;
    case "ambient": return <Ambient el={el} start={start} />;
    case "dose": return <Dose el={el} start={start} />;
    case "ticks": return <Ticks el={el} start={start} />;
    case "layers": return <Layers el={el} start={start} />;
    case "hangtag": return <HangTag el={el} start={start} />;
    case "gust": return <Gust el={el} start={start} />;
    case "rings": return <Rings el={el} start={start} />;
    case "duel": return <Duel el={el} start={start} />;
    default: return <ElementView el={el} start={start} />;
  }
};

/** Il master (già montato con FFmpeg) scorre continuo: niente seek tra i tagli, niente lampi. */
const Master: React.FC<{ src: string; total: number; fade?: number }> = ({ src, total, fade }) => {
  const frame = useCurrentFrame();
  const tail = fade ?? secToFrames(0.5);
  const volume = interpolate(frame, [total - tail, total], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <OffthreadVideo src={staticFile(src)} volume={volume} style={{ width: "100%", height: "100%" }} />;
};

export const CNReel: React.FC<CNReelProps> = (p) => {
  const { fps } = useVideoConfig();
  // con `intro` il reel si apre con una scheda a tutto schermo: il video (e tutti i suoi tempi) parte dopo quei fotogrammi
  const introF = p.intro ? Math.round(p.intro.seconds * fps) : 0;
  const frame = useCurrentFrame() - introF;
  const tailF = tailFrames(p.tailSeconds);
  const { items, total } = useMemo(() => layout(p.segments, p.blendFrames, tailF), [p.segments, p.blendFrames, tailF]);
  const words = useMemo(() => remapWords(p.words, items, p.wordFix, p.wordOffset), [p.words, items, p.wordFix, p.wordOffset]);
  const starts = useMemo(() => p.elements.map((el) => resolveStart(el, words)), [p.elements, words]);
  const ctaFrames = Math.round(p.ctaSeconds * fps);
  // la CTA parte al taglio e sale dal basso mentre il video (coda) continua sotto; con `tailHold` parte quei secondi dopo il taglio
  // (respiro dopo l'ultima parola: Ross 18/11, «stacco troppo netto prima della CTA»)
  // con `ctaLead` il pannello comincia a salire PRIMA della fine del parlato e finisce di coprire nella coda: dopo l'ultima parola non resta
  // video «muto» (Ross 24/11: «si vede che parla ma non c'è suono», «stacco troppo netto»)
  const lead = p.ctaLead !== undefined ? Math.round(p.ctaLead * fps) : -1;
  const xfade = lead >= 0 ? tailF + lead : Math.max(9, tailF - Math.round((p.tailHold ?? 0) * fps));
  const tailPush = 1;
  const videoFade = 1; // niente dissolvenza verde sul video: il pannello della CTA lo copre salendo
  // camera del titolo spezzato: il video scende sotto la scheda a tutta larghezza (la testa resta intera)
  let cam = 0;
  p.elements.forEach((el, i) => { if (el.kind === "split") cam = Math.max(cam, splitCamera(frame, starts[i], Math.round(el.dur * fps))); });
  const camShift = H * SPLIT_CARD_H * cam;
  // push-in lento durante l'hook (tutto in Remotion: niente doppia immagine al rilascio)
  const hookF = p.hook ? Math.round(p.hook.dur * fps) : 0;
  const hookZoom = p.hookZoom && hookF ? interpolate(frame, [0, hookF, hookF + 15], [1, p.hookZoom, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) }) : 1;

  // avvicinamenti lenti nei passaggi senza grafica
  let zoom = 1;
  (p.zooms ?? []).forEach((z) => { const a = Math.round(z.at * fps), b = a + Math.round(z.dur * fps); const k = interpolate(frame, [a, b - 14, b], [0, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) }); zoom = Math.max(zoom, 1 + (z.scale - 1) * k); });

  // schianto: scossa della camera sull'urto della parola
  let shake = { dx: 0, dy: 0, sc: 1 };
  p.elements.forEach((el, i) => { if (el.kind === "slam") { const sh = slamShake(frame, slamImpact({ ...el, onAt: resolveCues(el, starts[i], words) } as Extract<Element, { kind: "slam" }>, starts[i], fps)); if (sh.sc !== 1) shake = sh; } });

  // orbita: il video continua a scorrere ma arretra (ancorato in basso), su fondo brand
  let orb = 0, orbBack = 0.72;
  p.elements.forEach((el, i) => { if (el.kind === "orbit") { const z = orbitCam(el, starts[i], frame, fps); if (z > orb) { orb = z; orbBack = el.back ?? 0.72; } } });
  const orbScale = 1 - (1 - orbBack) * orb;
  // selfie: mentre una grafica occupa la fascia bassa (tutte tranne parole sopra la testa, pannello laterale e muro) niente sottotitoli
  const capHidden = p.elements.some((el, i) => {
    const l = frame - starts[i];
    if (el.hideCapsFrom !== undefined) return l >= Math.round(el.hideCapsFrom * fps) && l < Math.round(el.dur * fps) + 2;
    if (!el.hideCaps && (!p.capHideOnGfx || el.kind === "side" || el.kind === "wall" || (el.kind === "topword" && el.zone !== "strip"))) return false;
    return l >= -2 && l < Math.round(el.dur * fps) + 2;
  });
  // pannello laterale: il video si ritira a sinistra (sempre visibile) e lascia la colonna di destra a un elenco o a una mappa
  let sd = 0;
  p.elements.forEach((el, i) => { if (el.kind === "side") { const l = frame - starts[i], d = Math.round(el.dur * fps); if (l >= 0 && l < d) sd = Math.max(sd, sideK(l, d)); } });

  return (
    <AbsoluteFill style={{ background: "#2F4D1E", fontFamily: "Blinker, sans-serif" }}>
      <Sequence from={introF} durationInFrames={total} layout="none">
        {cam > 0 ? <AbsoluteFill style={{ background: "#E9E4D2", opacity: cam }} /> : null}
        {orb > 0 || sd > 0 ? <AbsoluteFill style={{ background: "linear-gradient(180deg,#1C3D15 0%,#0B0F0A 100%)" }} /> : null}
        <AbsoluteFill style={{ transform: `translate(${sd * SIDE.x}px, ${sd * SIDE.y}px) scale(${1 - (1 - SIDE.scale) * sd})`, transformOrigin: "0 0", borderRadius: sd > 0 ? 60 * sd : 0, overflow: sd > 0 ? "hidden" : "visible" }}>
        <AbsoluteFill style={{ transform: `scale(${orbScale})`, transformOrigin: "50% 100%", borderRadius: 44 * orb, overflow: "hidden", boxShadow: orb > 0 ? "0 -20px 80px rgba(0,0,0,0.6)" : "none" }}>
        <AbsoluteFill style={{ opacity: videoFade, transform: `translate(${shake.dx}px, ${camShift + shake.dy}px) scale(${hookZoom * shake.sc * tailPush * zoom})`, transformOrigin: "50% 30%" }}>
          <Master src={p.master} total={total} fade={lead >= 0 ? Math.min(tailF, 15) : undefined} />
        </AbsoluteFill>
        </AbsoluteFill>
        </AbsoluteFill>
        {/* reel a finestra: i bordi del video sfumano nel verde del fondo (niente riga netta tra video e fasce) */}
        {p.winFeather ? [0, 1].map((b) => <div key={b} style={{ position: "absolute", left: 0, width: 1080, top: b ? 1380 - p.winFeather! : 580, height: p.winFeather, background: `linear-gradient(${b ? 0 : 180}deg, #49762E 0%, rgba(73,118,46,0.75) 30%, rgba(73,118,46,0) 100%)` }} />) : null}
        {p.hook ? <Hook hook={p.hook} /> : null}
        <AbsoluteFill style={{ transform: `translateY(${p.gfxShift ?? 0}px) scale(${p.gfxScale ?? 1})`, transformOrigin: `50% ${H * 0.44}px` }}>
          {/* l'intestazione sparisce 1,3 s prima della fine del parlato e non torna per pochi fotogrammi dopo l'ultima grafica */}
          {p.winHeader ? <WinHeader {...p.winHeader} show={Math.min(...p.elements.map((el, i) => { const l = frame - starts[i], d = Math.round(el.dur * fps); return l < -8 ? Math.min(1, (-8 - l) / 6) : l > d + 2 ? Math.min(1, (l - d - 2) / 6) : 0; }), 1) * Math.min(1, Math.max(0, (total - tailF - 40 - frame) / 6))} /> : null}
          {p.elements.map((el, i) => (FULLSCREEN.has(el.kind) ? null : el.dy || el.shiftAt !== undefined ? (
            <AbsoluteFill key={i} style={{ transform: `translateY(${(el.dy ?? 0) + (el.shiftAt !== undefined && frame - starts[i] >= Math.round(el.shiftAt * fps) ? el.shiftDy ?? 0 : 0)}px)` }}><AnyElement el={{ ...el, onAt: resolveCues(el, starts[i], words) } as Element} start={starts[i]} /></AbsoluteFill>
          ) : (
            <AnyElement key={i} el={{ ...el, onAt: resolveCues(el, starts[i], words) } as Element} start={starts[i]} />
          )))}
        </AbsoluteFill>
        {/* le grafiche a tutto schermo non si spostano né si rimpiccioliscono: devono coprire tutto il fotogramma (Ross 11/11: banda in alto) */}
        {p.elements.map((el, i) => (FULLSCREEN.has(el.kind) ? (
          <AnyElement key={i} el={{ ...el, onAt: resolveCues(el, starts[i], words) } as Element} start={starts[i]} />
        ) : null))}
        {capHidden ? null : (
          <AbsoluteFill style={{ transform: `translateY(${p.capShift ?? 0}px)` }}>
            <Captions words={words} size={p.capSize} endFrame={total - 4} startFrame={Math.round((p.capFrom ?? 0) * fps)} />
          </AbsoluteFill>
        )}
        {p.banner ? <Banner {...p.banner} /> : null}
      </Sequence>
      {/* ctaSeconds: 0 = reel senza pannello finale (video «spontanei»: la chiusa la dice chi parla) */}
      {ctaFrames > 0 ? (
        <Sequence from={introF + total - xfade} durationInFrames={ctaFrames + xfade} layout="none">
          <CTA cta={p.cta} frames={ctaFrames} soft={lead >= 0} />
        </Sequence>
      ) : null}
      {p.intro ? <Intro frames={introF} kicker={p.intro.kicker} lines={p.intro.lines} accent={p.intro.accent} /> : null}
    </AbsoluteFill>
  );
};

export const reelDuration = (p: CNReelProps) => layout(p.segments, p.blendFrames, tailFrames(p.tailSeconds)).total + Math.round(p.ctaSeconds * FPS) + (p.intro ? Math.round(p.intro.seconds * FPS) : 0);
