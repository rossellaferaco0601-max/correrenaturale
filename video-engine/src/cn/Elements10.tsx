import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from "remotion";
import type { Element } from "./types";
import { BRAND, PANEL_X, PANEL_W, GFX_TOP } from "./types";
import { useInOut } from "./Elements3D";
import { GemLayers } from "./gem/GemLayers";
import { GemRings } from "./gem/GemRings";
import { GemWind } from "./gem/GemWind";
import { GemNose } from "./gem/GemNose";
import { GemHeat } from "./gem/GemHeat";
import { GemHouse } from "./gem/GemHouse";
import { GemOver } from "./gem/GemOver";
import { GemWarm } from "./gem/GemWarm";
import { GemBattery } from "./gem/GemBattery";
import { GemBreath } from "./gem/GemBreath";
import { GemSquat } from "./gem/GemSquat";
import { GemClimber } from "./gem/GemClimber";
import { GemBridge } from "./gem/GemBridge";
import { GemLunge } from "./gem/GemLunge";
import { GemJack } from "./gem/GemJack";
import { GaugeArt } from "./gem/GaugeArt";
import GLYPHS from "./blinker900.json";
import { B3DOver, B3DWarm, B3DWarmOk, B3DMani, B3DCasa, B3DPasso, B3DEnergia, B3DNasoFreddo, B3DNaso, B3DNasoFiltro, B3DRespiro, B3DSquat, B3DSquatGiu } from "./gem/B3D";

/* Serie G (YTCN 26, «Correre al freddo»): RAPPRESENTAZIONI dei concetti. I disegni animati (cartella `gem/`) sono scritti da Gemini su
   indicazioni di regia e rifiniti a mano; qui stanno le scritte (≥ 60 px) e l'aggancio alle parole di Daniele (`cues`).
   `fog` = titolo che si condensa come il fiato al freddo, `layers` = i capi che si indossano uno sull'altro, `hangtag` = cartellino del capo
   che dondola, `gust` = raffica di vento sulle parole, `rings` = i tre strati che lavorano in sinergia attorno al calore,
   `duel` = due forze che si spingono (sudore contro gelo) e vengono cancellate. Ognuna usata in un solo reel. */

const FONT = "Blinker, sans-serif";
const INK = "#0B0F0A";
const CORAL = "#FF6B4A";
const ICE = "#B8D7EA";
const CREAM = "#F4F1E5";
const SHADOW = "0 6px 0 rgba(11,15,10,0.85), 0 10px 26px rgba(0,0,0,0.7)";
const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
type P<K extends Element["kind"]> = { el: Extract<Element, { kind: K }>; start: number };
const cueF = (el: Element, i: number, fps: number, def: number) => Math.round((el.onAt?.[i] ?? def) * fps);
const panel = (s: number, out: number, h: number): React.CSSProperties => ({ position: "absolute", left: PANEL_X, width: PANEL_W, top: GFX_TOP, height: h, borderRadius: 30, background: "rgba(11,15,10,0.9)", fontFamily: FONT, color: BRAND.white, opacity: out * Math.min(1, s * 1.3), transform: `translateY(${(1 - s) * 40}px)`, overflow: "hidden" });
/** corpo più grande che fa stare la scritta (maiuscola, Blinker 900) nella larghezza data */
// larghezze VERE di Blinker Black maiuscolo, in parti del corpo (misurate sul file del font: 24/11, le stime facevano sbordare «ADDOMINALI»)
const glyph = (ch: string) => (GLYPHS as Record<string, number>)[ch] ?? 0.62;
const fit = (text: string, w: number, max: number) => Math.min(max, Math.floor(w / Math.max(2.2, 1.03 * [...text.toUpperCase()].reduce((a, ch) => a + glyph(ch), 0))));

/* ---------- titolo d'apertura, un ingresso diverso per reel (`anim`): `fog` = ogni parola arriva sfocata e larga, come il fiato al freddo, e va
   a fuoco; `rise` = le parole salgono da sotto la riga; `snap` = arrivano grandi e si assestano con un colpo; `wind` = entrano spinte da sinistra;
   `type` = si scrivono lettera per lettera ---------- */
export const Fog: React.FC<P<"fog">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const anim = el.anim ?? "fog";
  let n = 0, chars = 0;
  return (
    <div style={{ position: "absolute", left: 60, width: 960, top: GFX_TOP, fontFamily: FONT, opacity: out, display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
      {el.lines.map((line, li) => {
        const acc = line === el.accent, size = fit(line, acc ? 840 : 940, acc ? 112 : 98), first = n, c0 = chars;
        chars += line.length;
        const kp = anim === "type" ? clamp01((local - 3 - c0 / 1.4) / 5) : clamp01((local - (3 + first * 4)) / 8);
        const shown = Math.max(0, Math.min(line.length, Math.floor((local - 3) * 1.4 - c0)));
        const word: React.CSSProperties = { position: "relative", fontWeight: 900, fontSize: size, lineHeight: 1.04, textTransform: "uppercase", whiteSpace: "pre", color: acc ? INK : BRAND.white, textShadow: acc ? "none" : SHADOW };
        return (
          <div key={li} style={{ position: "relative", display: "flex", gap: size * 0.26, padding: acc ? "8px 34px 14px" : 0, overflow: anim === "rise" ? "hidden" : "visible" }}>
            {acc ? <div style={{ position: "absolute", inset: 0, borderRadius: 20, background: BRAND.lime, transform: `scaleX(${kp})`, transformOrigin: "left center" }} /> : null}
            {anim === "type" ? (
              <span style={word}>{line.slice(0, shown)}<span style={{ opacity: 0 }}>{line.slice(shown)}</span>{shown > 0 && shown < line.length ? <span style={{ position: "absolute", left: `${(shown / line.length) * 100}%`, top: "8%", width: 8, height: "84%", background: acc ? INK : BRAND.lime }} /> : null}</span>
            ) : line.split(" ").map((w, wi) => {
              const f = local - (3 + n++ * 4), k = clamp01(f / (anim === "fog" ? 11 : 8)), e = 1 - Math.pow(1 - k, 3);
              const st: React.CSSProperties = anim === "fog" ? { opacity: k, filter: `blur(${(1 - k) * 18}px)`, transform: `translateY(${(1 - k) * 16}px) scale(${1 + (1 - k) * 0.3})` }
                : anim === "rise" ? { transform: `translateY(${(1 - e) * 115}%)` }
                : anim === "snap" ? { opacity: clamp01(f / 2), transform: `scale(${1 + (1 - e) * 0.9}) rotate(${(1 - e) * (wi % 2 ? 5 : -5)}deg)` }
                : { opacity: clamp01(f / 3), transform: `translateX(${(1 - e) * -160}px) skewX(${(1 - e) * -20}deg)` };
              return <span key={wi} style={{ ...word, ...st }}>{w}</span>;
            })}
          </div>
        );
      })}
    </div>
  );
};

/* ---------- i capi uno sull'altro: a sinistra il disegno (lo strato del momento si chiude dal basso sulla parola detta, poi i suoi effetti:
   calore, sudore, vento, pioggia), a destra il nome dello strato e, sotto, la targhetta che cambia a ogni parola chiave.
   cues: [strato, targhetta 1, targhetta 2, …] ---------- */
export const Layers: React.FC<P<"layers">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, s, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const cue = cueF(el, 0, fps, 0.25), on = el.chips.map((_, i) => cueF(el, i + 1, fps, 1.4 + i * 1.3));
  let idx = -1; on.forEach((f, i) => { if (local >= f) idx = i; });
  const kb = spring({ frame: local - cue, fps, config: { damping: 11, stiffness: 220, mass: 0.6 } });
  const kc = idx >= 0 ? spring({ frame: local - on[idx], fps, config: { damping: 12, stiffness: 230, mass: 0.55 } }) : 0;
  const chip = idx >= 0 ? el.chips[idx] : "", TW = 504;
  const size = Math.min(...el.lines.map((l) => fit(l, TW, 94)));
  return (
    <div style={panel(s, out, 350)}>
      <div style={{ position: "absolute", left: 10, top: 15, width: 320, height: 320, transform: "scale(1.5)", transformOrigin: "50% 49%" }}>
        <GemLayers t={local / fps} uid={`ly${start}`} stage={el.stage} cue={cue / fps} fx={[(on[0] ?? 9999) / fps, (on[1] ?? 9999) / fps]} />
      </div>
      <div style={{ position: "absolute", left: 16, top: 14, width: 66, height: 66, borderRadius: 33, background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 46, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${local >= cue ? 0.6 + 0.4 * kb : 0})` }}>{el.stage}</div>
      <div style={{ position: "absolute", left: 344, top: 0, width: TW + 10, height: 350, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "flex-start", gap: 18 }}>
        <div style={{ opacity: local >= cue ? clamp01(kb * 1.5) : 0, transform: `translateX(${(1 - (local >= cue ? kb : 0)) * 36}px)` }}>
          {el.lines.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: size, lineHeight: 1.03, textTransform: "uppercase", whiteSpace: "nowrap" }}>{l}</div>)}
        </div>
        <div style={{ height: 92, display: "flex", alignItems: "center" }}>
          {chip ? <div style={{ background: BRAND.lime, color: INK, borderRadius: 16, padding: "10px 24px 13px", fontWeight: 900, fontSize: fit(chip, TW - 52, 78), lineHeight: 1, textTransform: "uppercase", whiteSpace: "nowrap", opacity: clamp01(kc * 1.6), transform: `scale(${0.8 + 0.2 * kc})`, transformOrigin: "left center" }}>{chip}</div> : null}
        </div>
      </div>
    </div>
  );
};

/* ---------- cartellino del capo: scende appeso al filo e dondola (pendolo smorzato); la seconda riga arriva sulla sua parola e gli dà
   un'altra spinta. cues: [cartellino, riga 2] ---------- */
export const HangTag: React.FC<P<"hangtag">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const f0 = cueF(el, 0, fps, 0.1), f1 = cueF(el, 1, fps, 1.4), t0 = Math.max(0, local - f0) / fps, t1 = Math.max(0, local - f1) / fps;
  const drop = spring({ frame: local - f0, fps, config: { damping: 13, stiffness: 150, mass: 0.7 } });
  const ang = 15 * Math.exp(-t0 * 1.4) * Math.cos(t0 * 6.2) + (local >= f1 ? 7 * Math.exp(-t1 * 2) * Math.sin(t1 * 8.5) : 0) + 1.2 * Math.sin(local / fps * 1.9);
  const W = 700, H = 286, k1 = spring({ frame: local - f1, fps, config: { damping: 12, stiffness: 230, mass: 0.55 } });
  const size = Math.min(...el.lines.map((l) => fit(l, W - 90, 94)));
  return (
    <div style={{ position: "absolute", left: (1080 - W) / 2, top: GFX_TOP + 26, width: W, height: H, fontFamily: FONT, opacity: out * clamp01((local - f0 + 1) / 3), transformOrigin: "50% -150px", transform: `translateY(${(drop - 1) * 360}px) rotate(${ang}deg)` }}>
      <svg width={W} height={200} style={{ position: "absolute", left: 0, top: -150, overflow: "visible" }}>
        <path d={`M${W / 2 - 3} 0 Q ${W / 2 - 26} 96 ${W / 2} 184`} fill="none" stroke={CREAM} strokeWidth={5} strokeLinecap="round" />
        <path d={`M${W / 2 + 3} 0 Q ${W / 2 + 26} 96 ${W / 2} 184`} fill="none" stroke={CREAM} strokeWidth={5} strokeLinecap="round" opacity={0.7} />
      </svg>
      <div style={{ position: "absolute", inset: 0, background: CREAM, borderRadius: 26, clipPath: "polygon(9% 0, 91% 0, 100% 22%, 100% 100%, 0 100%, 0 22%)", boxShadow: "0 14px 34px rgba(0,0,0,0.45)" }} />
      <div style={{ position: "absolute", left: 14, right: 14, top: 14, bottom: 14, border: `4px dashed rgba(73,118,46,0.55)`, borderRadius: 18, clipPath: "polygon(8% 0, 92% 0, 100% 21%, 100% 100%, 0 100%, 0 21%)" }} />
      <div style={{ position: "absolute", left: W / 2 - 19, top: 18, width: 38, height: 38, borderRadius: 19, background: "#49762E", boxShadow: `inset 0 0 0 9px ${CREAM}, inset 0 0 0 38px ${INK}` }} />
      <div style={{ position: "absolute", left: 0, width: W, top: 72, textAlign: "center", color: INK, fontWeight: 900, fontSize: size, lineHeight: 1.06, textTransform: "uppercase" }}>
        <div style={{ whiteSpace: "nowrap" }}>{el.lines[0]}</div>
        {el.lines[1] ? <div style={{ whiteSpace: "nowrap", color: "#35591F", opacity: local >= f1 ? clamp01(k1 * 1.6) : 0, transform: `scale(${0.8 + 0.2 * k1})` }}>{el.lines[1]}</div> : null}
      </div>
    </div>
  );
};

/* ---------- raffica: il vento attraversa la zona, le parole arrivano spinte da sinistra e restano piegate; sull'ultima parola la raffica
   si alza. cues: una per parola ---------- */
export const Gust: React.FC<P<"gust">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const on = el.words.map((_, i) => cueF(el, i, fps, 0.2 + i * 1.2)), t = local / fps, gust = on[on.length - 1] / fps;
  const strong = clamp01((t - gust) / 0.4);
  return (
    <div style={{ position: "absolute", left: PANEL_X, width: PANEL_W, top: GFX_TOP, height: 280, fontFamily: FONT, opacity: out }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 880, height: 250, transform: "scaleY(1.12)", transformOrigin: "left top", opacity: clamp01(local / 6) }}><GemWind t={t} uid={`gw${start}`} gust={gust} /></div>
      <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}>
        {el.words.map((w, i) => {
          const k = spring({ frame: local - on[i], fps, config: { damping: 13, stiffness: 170, mass: 0.7 } });
          const lean = -(7 + 5 * strong) - 2.5 * Math.sin(t * 9 + i * 1.7) * (0.4 + 0.6 * strong);
          return <div key={i} style={{ fontWeight: 900, fontSize: fit(w, 700, 142), lineHeight: 0.98, textTransform: "uppercase", whiteSpace: "nowrap", color: i === el.words.length - 1 ? ICE : BRAND.white, textShadow: SHADOW, opacity: local >= on[i] ? clamp01(k * 1.8) : 0, transform: `translateX(${(1 - k) * -220 + 3 * Math.sin(t * 13 + i) * strong}px) skewX(${lean}deg)` }}>{w}</div>;
        })}
      </div>
    </div>
  );
};

/* ---------- sinergia: a sinistra i tre strati come anelli attorno al calore del corpo (prima girano ognuno per conto suo, poi si
   agganciano; il centro diventa caldo), a destra la frase del momento. cues: [anelli, aggancio = frase 2, calore = frase 3] ---------- */
export const Rings: React.FC<P<"rings">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, s, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const f0 = cueF(el, 0, fps, 0.2), lock = cueF(el, 1, fps, 2.2), warm = cueF(el, 2, fps, 3.8), on = [0, lock, warm];
  let idx = 0; on.forEach((f, i) => { if (i < el.phases.length && local >= f) idx = i; });
  const k = spring({ frame: local - on[idx], fps, config: { damping: 13, stiffness: 210, mass: 0.6 } });
  const lines = el.phases[idx], TW = 504, size = Math.min(...lines.map((l) => fit(l, TW - 8, 100)));
  return (
    <div style={panel(s, out, 336)}>
      <div style={{ position: "absolute", left: 20, top: 18, width: 300, height: 300, transform: "scale(1.07)" }}>
        <GemRings t={local / fps} uid={`rg${start}`} on={[f0 / fps, f0 / fps + 0.3, f0 / fps + 0.6]} lock={lock / fps} warm={warm / fps} />
      </div>
      <div style={{ position: "absolute", left: 348, top: 0, width: TW, height: 336, display: "flex", flexDirection: "column", justifyContent: "center", opacity: clamp01(k * 1.6), transform: `translateX(${(1 - k) * 34}px)` }}>
        {lines.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: size, lineHeight: 1.05, textTransform: "uppercase", whiteSpace: "nowrap", color: idx === el.phases.length - 1 && i === 0 ? BRAND.lime : BRAND.white }}>{l}</div>)}
      </div>
    </div>
  );
};

/* ---------- due forze che si spingono: i due blocchi entrano dai lati, si scontrano al centro e il confine va avanti e indietro; sull'ultima
   parola una riga lime li cancella. cues: [scontro, parola sinistra, parola destra, cancellatura] ---------- */
export const Duel: React.FC<P<"duel">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const f0 = cueF(el, 0, fps, 0.1), fl = cueF(el, 1, fps, 0.6), fr = cueF(el, 2, fps, 1.4), fx = cueF(el, 3, fps, 2.2), t = Math.max(0, local - f0) / fps;
  const W = 880, H = 224, arrive = spring({ frame: local - f0, fps, config: { damping: 14, stiffness: 240, mass: 0.6 } });
  const done = clamp01((local - fx) / 7);
  const split = 0.5 + (0.085 * Math.sin(t * 5.4) + 0.03 * Math.sin(t * 13.1)) * (1 - done) * clamp01(t * 2);
  const hit = Math.exp(-Math.max(0, local - f0 - 5) / 4) * (local >= f0 + 5 ? 1 : 0), sx = W * split;
  const word = (txt: string, w: number, f: number, col: string) => <div style={{ fontWeight: 900, fontSize: fit(txt, w - 60, 124), lineHeight: 1, textTransform: "uppercase", whiteSpace: "nowrap", color: col, opacity: clamp01((local - f) / 4), transform: `scale(${1 + 0.12 * Math.exp(-Math.max(0, local - f) / 5)})` }}>{txt}</div>;
  return (
    <div style={{ position: "absolute", left: PANEL_X, width: W, top: GFX_TOP + 20, height: H, fontFamily: FONT, opacity: out * clamp01((local - f0 + 1) / 3), transform: `scale(${1 + 0.03 * hit})` }}>
      <div style={{ position: "absolute", left: (arrive - 1) * 500, top: 0, width: sx - 5, height: H, borderRadius: "30px 8px 8px 30px", background: `linear-gradient(90deg, #FFB020, ${CORAL})`, display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden", filter: `saturate(${1 - 0.6 * done})`, opacity: 1 - 0.12 * done }}>{word(el.left, W * 0.42, fl, INK)}</div>
      <div style={{ position: "absolute", left: sx + 5 + (1 - arrive) * 500, top: 0, width: W - sx - 5, height: H, borderRadius: "8px 30px 30px 8px", background: `linear-gradient(90deg, ${ICE}, #7FB2D4)`, display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden", filter: `saturate(${1 - 0.6 * done})`, opacity: 1 - 0.12 * done }}>{word(el.right, W * 0.42, fr, INK)}</div>
      <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, overflow: "visible", opacity: (1 - done) * clamp01(t * 3) }}>
        {[0, 1, 2, 3].map((i) => { const y = 26 + i * 56, j = 9 * Math.sin(t * 17 + i * 2.1); return <path key={i} d={`M${sx - 16 + j} ${y} L${sx + 12 - j} ${y + 16} L${sx - 10 + j} ${y + 30}`} fill="none" stroke={BRAND.white} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />; })}
      </svg>
      <div style={{ position: "absolute", left: -24, top: H / 2 - 6, width: W + 48, height: 12, borderRadius: 6, background: BRAND.lime, boxShadow: `0 0 0 4px ${INK}`, transform: `rotate(-7deg) scaleX(${done})`, transformOrigin: "left center" }} />
    </div>
  );
};

/* ---------- illustrazione + frase: a sinistra un disegno animato della cartella `gem/` (riceve i tempi delle parole-aggancio), a destra la
   frase del momento e, se c'è, la targhetta lime. Ogni `phases[i]` entra sull'aggancio i (oppure `on`: indice dell'aggancio, -1 = dall'inizio).
   `artCues`: quali agganci passare al disegno, nell'ordine dei suoi tempi (-1 = già avvenuto); se manca, gli stessi della grafica ---------- */
const ARTS = { nose: GemNose, heat: GemHeat, house: GemHouse, over: GemOver, warm: GemWarm, battery: GemBattery, breath: GemBreath, squat: GemSquat, climber: GemClimber, bridge: GemBridge, lunge: GemLunge, jack: GemJack, gauge: GaugeArt, over3d: B3DOver, warm3d: B3DWarm, warmok3d: B3DWarmOk, mani3d: B3DMani, casa3d: B3DCasa, passo3d: B3DPasso, energia3d: B3DEnergia, nasofreddo3d: B3DNasoFreddo, naso3d: B3DNaso, nasofiltro3d: B3DNasoFiltro, respiro3d: B3DRespiro, squat3d: B3DSquat, squatgiu3d: B3DSquatGiu };
export type GemArt = keyof typeof ARTS;
/** quanto ingrandire ogni disegno (e di quanto spostarlo) perché riempia la sua metà del pannello: le tele sono 300x300 ma il soggetto non
 *  le occupa tutte allo stesso modo (Ross 21/11: «le animazioni le farei leggermente più grandi») */
const ART_FIT = { nose: [1.14, 0, 0], heat: [1.24, 0, -12], house: [1.16, 0, -6], over: [1.5, -12, -16], warm: [1.42, 0, 0], battery: [1.36, -20, -42], breath: [1.14, 0, 0], squat: [1.12, 0, -4], climber: [1.14, 4, -34], bridge: [1.14, 4, -58], lunge: [1.24, 6, -30], jack: [1.24, 0, -22], gauge: [1.14, 0, -10], ...Object.fromEntries(["over3d", "warm3d", "warmok3d", "mani3d", "casa3d", "passo3d", "energia3d", "nasofreddo3d", "naso3d", "nasofiltro3d", "respiro3d", "squat3d", "squatgiu3d"].map((k) => [k, [1.02, 0, 0]])) } as Record<GemArt, [number, number, number]>;
export const Gem: React.FC<P<"gem">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, s, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const sec = el.onAt ?? [], at = (i: number) => { const o = el.phases[i].on ?? i; return o < 0 ? 0 : Math.round((sec[o] ?? 9999) * fps); };
  let idx = -1; el.phases.forEach((_, i) => { if (local >= at(i)) idx = i; });
  const ph = idx >= 0 ? el.phases[idx] : null, k = idx >= 0 ? spring({ frame: local - at(idx), fps, config: { damping: 13, stiffness: 210, mass: 0.6 } }) : 0;
  // finché non c'è una frase il disegno sta al centro del pannello (niente metà vuota); quando entra la prima frase scivola a sinistra
  const f0 = Math.min(...el.phases.map((_, i) => at(i))), k0 = f0 <= 0 ? 1 : spring({ frame: local - f0 + 4, fps, config: { damping: 15, stiffness: 150, mass: 0.7 } });
  const Art = ARTS[el.art], H = 336, TW = 492;   // 32 px di margine dal bordo destro del pannello
  const artCues = el.artCues ? el.artCues.map((i) => (i < 0 ? -1 : sec[i] ?? 9999)) : sec;
  const size = ph ? Math.min(...ph.lines.map((l) => fit(l, TW, ph.chip ? 90 : 100))) : 0;
  return (
    <div style={panel(s, out, H)}>
      <div style={{ position: "absolute", left: 22, top: 18, width: 300, height: 300, transform: `translate(${ART_FIT[el.art][1] + (1 - k0) * 268}px, ${ART_FIT[el.art][2]}px) scale(${ART_FIT[el.art][0]})` }}>
        <Art t={local / fps} uid={`g${start}`} cues={artCues} />
      </div>
      {ph ? (
        <div style={{ position: "absolute", left: 356, top: 0, width: TW + 4, height: H, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "flex-start", gap: 18, opacity: clamp01(k * 1.6), transform: `translateX(${(1 - k) * 34}px)` }}>
          <div>{ph.lines.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: size, lineHeight: 1.05, textTransform: "uppercase", whiteSpace: "nowrap" }}>{l}</div>)}</div>
          {ph.chip ? <div style={{ background: BRAND.lime, color: INK, borderRadius: 16, padding: "10px 24px 13px", fontWeight: 900, fontSize: fit(ph.chip, TW - 52, 78), lineHeight: 1, textTransform: "uppercase", whiteSpace: "nowrap", transform: `scale(${0.8 + 0.2 * k})`, transformOrigin: "left center" }}>{ph.chip}</div> : null}
        </div>
      ) : null}
    </div>
  );
};

/* ---------- intestazione fissa dei reel «a finestra» (circuito in casa: video a tutta larghezza su fondo verde): occupa la fascia sopra la
   finestra quando non c'è una grafica; numero dell'esercizio nel cerchio lime, nome grande, riga piccola sopra ---------- */
export const WinHeader: React.FC<{ kicker: string; title: string; n?: string; show: number }> = ({ kicker, title, n, show }) => (
  <div style={{ position: "absolute", left: 70, width: 940, top: GFX_TOP + 40, fontFamily: FONT, opacity: show, transform: `translateY(${(1 - show) * 24}px)`, display: "flex", alignItems: "center", gap: 30 }}>
    {n ? <div style={{ width: 150, height: 150, borderRadius: 75, flexShrink: 0, background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 104, display: "flex", alignItems: "center", justifyContent: "center" }}>{n}</div> : null}
    <div>
      <div style={{ fontWeight: 800, fontSize: 46, letterSpacing: 3, textTransform: "uppercase", color: CREAM, opacity: 0.92 }}>{kicker}</div>
      {title.split("|").map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: fit(l, n ? 740 : 920, 112), lineHeight: 1.02, textTransform: "uppercase", color: BRAND.white, whiteSpace: "nowrap" }}>{l}</div>)}
    </div>
  </div>
);

/* ---------- parole grandi con un ingresso diverso per reel (`anim`): `ice` = arrivano azzurre e tremano dal freddo, poi si fermano bianche;
   `pulse` = colpo di scala con la riga lime che si disegna sotto; `slide` = entrano alternate da sinistra e da destra. cues: una per parola ---------- */
export const Kin: React.FC<P<"kin">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const on = el.words.map((_, i) => cueF(el, i, fps, 0.15 + i * 0.9)), t = local / fps;
  return (
    <div style={{ position: "absolute", left: 60, width: 960, top: GFX_TOP, fontFamily: FONT, opacity: out, display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
      {el.words.map((w, i) => {
        const f = local - on[i], k = spring({ frame: f, fps, config: { damping: 12, stiffness: 200, mass: 0.6 } }), size = fit(w, 900, 132), cold = clamp01(1 - f / 16);
        const st: React.CSSProperties = el.anim === "ice" ? { color: cold > 0.05 ? ICE : BRAND.white, transform: `translate(${5 * Math.sin(t * 46 + i) * cold}px, ${(1 - k) * -30}px) scale(${1.25 - 0.25 * k})`, letterSpacing: (1 - k) * 14 }
          : el.anim === "slide" ? { transform: `translateX(${(1 - k) * (i % 2 ? 420 : -420)}px)` }
          : { transform: `scale(${0.5 + 0.5 * k})` };
        return (
          <div key={i} style={{ position: "relative", opacity: f >= 0 ? clamp01(k * 2) : 0 }}>
            <div style={{ fontWeight: 900, fontSize: size, lineHeight: 1.02, textTransform: "uppercase", whiteSpace: "nowrap", color: BRAND.white, textShadow: SHADOW, ...st }}>{w}</div>
            {el.anim === "pulse" && i === el.words.length - 1 ? <div style={{ height: 14, borderRadius: 7, background: BRAND.lime, boxShadow: `0 0 0 4px ${INK}`, transform: `scaleX(${clamp01((f - 4) / 8)})`, transformOrigin: "left center", marginTop: 6 }} /> : null}
          </div>
        );
      })}
    </div>
  );
};

/* ---------- quanto farlo: (in alto, se ci sono) le modalità che si accendono sulla parola, poi un anello per ogni durata che si chiude sulla
   sua parola con il numero dentro. cues: [modalità…, durate…] ---------- */
export const Dose: React.FC<P<"dose">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, s, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const tags = el.tags ?? [], nT = tags.length, D = 196, RR = 82, C = 2 * Math.PI * RR;
  const H = (nT ? 100 : 0) + D + 44;
  return (
    <div style={panel(s, out, H)}>
      {nT ? (
        <div style={{ position: "absolute", left: 0, width: PANEL_W, top: 22, display: "flex", justifyContent: "center", gap: 22 }}>
          {tags.map((tg, i) => { const f = local - cueF(el, i, fps, 0.3 + i * 0.9), k = spring({ frame: f, fps, config: { damping: 12, stiffness: 220, mass: 0.6 } }), lit = f >= 0; return <div key={i} style={{ borderRadius: 18, padding: "8px 30px 12px", border: `5px solid ${lit ? BRAND.lime : "rgba(255,255,255,0.25)"}`, background: lit ? BRAND.lime : "transparent", color: lit ? INK : "rgba(255,255,255,0.5)", fontWeight: 900, fontSize: fit(tg, 340, 66), lineHeight: 1, textTransform: "uppercase", transform: `scale(${lit ? 0.88 + 0.12 * k : 1})` }}>{tg}</div>; })}
        </div>
      ) : null}
      <div style={{ position: "absolute", left: 0, width: PANEL_W, top: (nT ? 106 : 0) + 22, display: "flex", justifyContent: "center", gap: 46 }}>
        {el.items.map((it, i) => {
          const f = local - cueF(el, nT + i, fps, 0.4 + (nT + i) * 0.9), fill = clamp01(f / 14), k = spring({ frame: f, fps, config: { damping: 11, stiffness: 220, mass: 0.6 } });
          const [num, unit] = it.split(" ");
          return (
            <div key={i} style={{ position: "relative", width: D, height: D }}>
              <svg width={D} height={D} style={{ position: "absolute", left: 0, top: 0, transform: "rotate(-90deg)" }}>
                <circle cx={D / 2} cy={D / 2} r={RR} fill="none" stroke="rgba(255,255,255,0.16)" strokeWidth={16} />
                <circle cx={D / 2} cy={D / 2} r={RR} fill="none" stroke={BRAND.lime} strokeWidth={16} strokeLinecap="round" strokeDasharray={C} strokeDashoffset={C * (1 - fill)} />
              </svg>
              <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: f >= 0 ? 1 : 0.28, transform: `scale(${f >= 0 ? 0.8 + 0.2 * k : 1})` }}>
                <div style={{ fontWeight: 900, fontSize: 84, lineHeight: 0.95, color: BRAND.white }}>{num}</div>
                <div style={{ fontWeight: 800, fontSize: 40, lineHeight: 1, color: CREAM, textTransform: "uppercase" }}>{unit}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/* ---------- riepilogo: ogni riga arriva con la sua spunta che si disegna; alla fine (se c'è `foot`) le righe lasciano il posto alla
   conclusione su targa lime. cues: [righe…, conclusione] ---------- */
export const Ticks: React.FC<P<"ticks">> = ({ el, start }) => {
  const { fps } = useVideoConfig();
  const { local, out, visible } = useInOut(start, Math.round(el.dur * fps));
  if (!visible) return null;
  const n = el.items.length, RH = 118, fF = el.foot ? cueF(el, n, fps, 0.4 + n * 1.4) : 99999, gone = clamp01((local - fF + 4) / 5);
  const kf = spring({ frame: local - fF, fps, config: { damping: 11, stiffness: 200, mass: 0.6 } });
  const size = Math.min(...el.items.map((x) => fit(x, 730, 88)));
  return (
    <div style={{ position: "absolute", left: PANEL_X, width: PANEL_W, top: GFX_TOP, height: n * RH, fontFamily: FONT, opacity: out }}>
      {el.items.map((it, i) => {
        const f = local - cueF(el, i, fps, 0.3 + i * 1.4), k = spring({ frame: f, fps, config: { damping: 13, stiffness: 200, mass: 0.6 } }), tick = clamp01((f - 3) / 7);
        return (
          <div key={i} style={{ position: "absolute", left: 0, top: i * RH, width: PANEL_W, height: RH - 14, borderRadius: 24, background: "rgba(11,15,10,0.9)", display: "flex", alignItems: "center", gap: 24, padding: "0 26px", boxSizing: "border-box", opacity: (f >= 0 ? clamp01(k * 1.6) : 0) * (1 - gone), transform: `translateX(${(1 - k) * -60}px)` }}>
            <svg width={72} height={72} style={{ flexShrink: 0 }}><circle cx={36} cy={36} r={33} fill={BRAND.lime} /><path d="M19 37 L31 49 L54 24" fill="none" stroke={INK} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={60} strokeDashoffset={60 * (1 - tick)} /></svg>
            <div style={{ fontWeight: 900, fontSize: size, lineHeight: 1, textTransform: "uppercase", whiteSpace: "nowrap", color: BRAND.white }}>{it}</div>
          </div>
        );
      })}
      {el.foot ? (
        <div style={{ position: "absolute", left: 0, width: PANEL_W, top: (n * RH - 14) / 2 - 80, textAlign: "center", opacity: local >= fF ? clamp01(kf * 1.6) : 0, transform: `scale(${0.7 + 0.3 * kf})` }}>
          <div style={{ display: "inline-block", background: BRAND.lime, color: INK, borderRadius: 24, padding: "22px 44px 28px", fontWeight: 900, fontSize: fit(el.foot, 760, 110), lineHeight: 1, textTransform: "uppercase", whiteSpace: "nowrap" }}>{el.foot}</div>
        </div>
      ) : null}
    </div>
  );
};

/* ---------- scheda finale «da ricordare» a tutto schermo, sul verde della CTA: sale dal basso e resta finché la CTA la copre (stesso fondo:
   nessuno stacco). Serve quando il sorgente cambia inquadratura negli ultimi secondi: l'ultima frase si sente sopra la scheda, con i
   sottotitoli, e la «mossa successiva» di Daniele non si vede (regola del finale, 17-21/11). In alto il disegno del reel nel suo stato finale ---------- */
export const Takeaway: React.FC<P<"takeaway">> = ({ el, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - start;
  if (local < 0) return null;
  const up = 1 - Math.pow(1 - Math.min(1, local / 9), 3), Art = el.art ? ARTS[el.art as GemArt] : null;
  const k = (d: number) => spring({ frame: local - d, fps, config: { damping: 14, stiffness: 160, mass: 0.7 } });
  return (
    <AbsoluteFill style={{ background: BRAND.green, transform: `translateY(${(1 - up) * 100}%)`, fontFamily: FONT, color: BRAND.white }}>
      {Art ? <div style={{ position: "absolute", left: 390, top: 400, width: 300, height: 300, transform: `scale(${1.95 * (0.8 + 0.2 * k(4))})`, opacity: k(4) }}><Art t={local / fps + 20} uid={`tk${start}`} cues={[-1, -1, -1, -1, -1, -1]} /></div> : null}
      <div style={{ position: "absolute", left: 0, width: 1080, top: 830, textAlign: "center", opacity: k(8), transform: `translateY(${(1 - k(8)) * 40}px)` }}>
        <div style={{ fontWeight: 800, fontSize: 48, letterSpacing: 4, textTransform: "uppercase", color: CREAM, marginBottom: 18 }}>{el.kicker ?? "Da ricordare"}</div>
        {el.lines.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: fit(l, 940, 132), lineHeight: 1.04, textTransform: "uppercase", whiteSpace: "nowrap", color: l === el.accent ? BRAND.lime : BRAND.white }}>{l}</div>)}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- banner fisso (Ross 24/11, G4: «un banner dall'inizio alla fine del video con la CTA per ricevere il circuito completo»):
   una riga sola sotto i sottotitoli, dentro la zona sicura di Instagram (sopra i 1600 px, a sinistra della colonna dei comandi).
   La parola da commentare sta nella pillola lime, che pulsa piano; entra dopo il titolo d'apertura e resta fino alla CTA ---------- */
export const Banner: React.FC<{ word: string; text: string[]; y: number; from?: number }> = ({ word, text, y, from = 20 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = spring({ frame: frame - from, fps, config: { damping: 15, stiffness: 150, mass: 0.7 } });
  const pulse = 1 + 0.04 * Math.max(0, Math.sin(((frame - from) / fps) * Math.PI * 0.9));
  return (
    <div style={{ position: "absolute", left: 60, width: 912, top: y, height: 78, borderRadius: 39, background: "rgba(11,15,10,0.92)", border: `3px solid ${BRAND.lime}`, boxSizing: "border-box", fontFamily: FONT, display: "flex", alignItems: "center", justifyContent: "center", gap: 14, opacity: clamp01(k * 1.5), transform: `translateY(${(1 - k) * 60}px)` }}>
      <div style={{ fontWeight: 800, fontSize: 36, color: BRAND.white, whiteSpace: "nowrap" }}>{text[0]}</div>
      <div style={{ background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 44, lineHeight: 1, padding: "5px 16px 8px", borderRadius: 12, transform: `scale(${pulse})` }}>{word}</div>
      <div style={{ fontWeight: 800, fontSize: 36, color: BRAND.white, whiteSpace: "nowrap" }}>{text[1]}</div>
    </div>
  );
};

/* ---------- effetto d'ambiente sui bordi dello schermo (24/11): `frost` = il gelo sale dagli angoli (velo azzurro e cristalli che si disegnano)
   mentre Daniele dice «congelare»; `heat` = alone caldo che pulsa dal basso quando il corpo si scalda. Sta solo sui bordi: mai sul volto,
   mai sopra sottotitoli e grafiche (che restano leggibili al centro) ---------- */
export const Ambient: React.FC<P<"ambient">> = ({ el, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - start, durF = Math.round(el.dur * fps);
  if (local < 0 || local >= durF) return null;
  const k = clamp01(local / 14) * clamp01((durF - local) / 12), t = local / fps;
  if (el.mood === "heat") {
    return (
      <AbsoluteFill style={{ pointerEvents: "none", opacity: k }}>
        <AbsoluteFill style={{ boxShadow: `inset 0 -${120 + 40 * Math.sin(t * 5)}px 260px -60px rgba(255,120,30,0.85), inset 0 0 200px 30px rgba(255,150,40,0.45)` }} />
      </AbsoluteFill>
    );
  }
  // cristalli: rami che crescono dai quattro angoli (lontani dal volto, che sta al centro in alto)
  const branch = (x: number, y: number, ang: number, len: number, depth: number, key: string, grow: number): React.ReactNode[] => {
    const x2 = x + Math.cos(ang) * len * grow, y2 = y + Math.sin(ang) * len * grow;
    const out: React.ReactNode[] = [<line key={key} x1={x} y1={y} x2={x2} y2={y2} stroke="#EAF6FF" strokeWidth={2 + depth * 2.2} strokeLinecap="round" opacity={0.9} />];
    if (depth > 0 && grow > 0.35) [0.45, 0.8].forEach((f, i) => [-1, 1].forEach((sg) => out.push(...branch(x + Math.cos(ang) * len * f * grow, y + Math.sin(ang) * len * f * grow, ang + sg * 0.9, len * 0.42, depth - 1, `${key}${i}${sg}`, clamp01((grow - 0.35) * 1.6)))));
    return out;
  };
  const g = clamp01(local / 26);
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: k }}>
      <AbsoluteFill style={{ boxShadow: "inset 0 0 220px 70px rgba(150,205,245,0.8), inset 0 0 60px 10px rgba(235,246,255,0.75)" }} />
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {[[0, 0, 0.72], [1080, 0, Math.PI - 0.72], [0, 1920, -0.9], [1080, 1920, Math.PI + 0.9], [0, 760, 0.1], [1080, 880, Math.PI - 0.1]].map(([x, y, a], i) => branch(x, y, a, 250, 2, `b${i}`, g))}
      </svg>
    </AbsoluteFill>
  );
};

/* ---------- apertura a tutto schermo prima del video (G9, 24/11): dà il soggetto a un reel che parte a metà discorso («Poi, una volta uscito…»).
   Fondo verde del marchio, occhiello + frase grande; alla fine sale e scopre il video già in movimento ---------- */
export const Intro: React.FC<{ frames: number; kicker?: string; lines: string[]; accent?: string }> = ({ frames, kicker, lines, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame >= frames + 10) return null;
  const x = clamp01((frame - frames) / 10), up = x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  const k = (d: number) => spring({ frame: frame - d, fps, config: { damping: 14, stiffness: 170, mass: 0.7 } });
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${BRAND.green} 0%, #1C3D15 100%)`, transform: `translateY(${-up * 100}%)`, fontFamily: FONT, color: BRAND.white }}>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 700, textAlign: "center" }}>
        {kicker ? <div style={{ display: "inline-block", background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 46, letterSpacing: 3, textTransform: "uppercase", padding: "8px 26px 10px", borderRadius: 12, marginBottom: 30, opacity: clamp01(k(0) * 1.5), transform: `scale(${0.8 + 0.2 * k(0)})` }}>{kicker}</div> : null}
        {lines.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: fit(l, 960, 150), lineHeight: 1.03, textTransform: "uppercase", whiteSpace: "nowrap", color: l === accent ? BRAND.lime : BRAND.white, opacity: clamp01(k(3 + i * 5) * 1.5), transform: `translateY(${(1 - k(3 + i * 5)) * 50}px)` }}>{l}</div>)}
      </div>
    </AbsoluteFill>
  );
};
