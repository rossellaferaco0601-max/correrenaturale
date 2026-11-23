import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { BRAND } from "./types";

/* G13 · «4 esercizi per scaldarti in casa» (Ross 22-23/11): reel veloce a FASCE ORIZZONTALI a tutta larghezza che riempiono tutto lo schermo:
   quattro fasce con i quattro esercizi del circuito (insieme, muti) e, in fondo, una QUINTA FASCIA che è il banner «scarica la guida».
   Niente sottotitoli (non c'è parlato) e niente pannello CTA: la CTA è la quinta fascia.
   Fasce video 1080x368 già ritagliate con ffmpeg (public/ytcn26/quad/b1…b4.mp4), nell'ordine del circuito, con numero e nome. I due esercizi
   a terra stanno interi nella fascia; affondi e jumping jack sono in piedi e non ci stanno, quindi usano le inquadrature strette
   dell'originale (gambe che affondano; busto, piedi e mezzo busto del jumping jack).
   Quinta fascia da 1472 a 1920 px: le due righe che contano («Commenta CIRCUITO», «e scarica la guida gratuita») stanno in alto, entro
   i ~1640 px; sotto, dove Instagram mette nome e didascalia, ci sono solo le pagine della guida come decorazione. */

const FONT = "Blinker, sans-serif";
const INK = "#0B0F0A";
const BH = 368, BAN_TOP = 4 * BH;
export const QUAD_FRAMES = 390;
const BANDS: { src: string; n: string; name: string[]; side: "left" | "right"; top: number }[] = [
  { src: "ytcn26/quad/b1.mp4", n: "1", name: ["Mountain", "climber"], side: "right", top: 236 },   // sotto i 220 px dell'interfaccia in alto
  { src: "ytcn26/quad/b2.mp4", n: "2", name: ["Ponte per", "i glutei"], side: "right", top: 18 },
  { src: "ytcn26/quad/b3.mp4", n: "3", name: ["Affondi"], side: "left", top: 18 },
  { src: "ytcn26/quad/b4.mp4", n: "4", name: ["Jumping", "jack"], side: "left", top: 18 },                // a destra, qui, ci sono i comandi di Instagram
];
const PAGES = [{ src: "ytcn26/quad/guida_07.jpg", x: 250, r: -9 }, { src: "ytcn26/quad/guida_08.jpg", x: 630, r: 9 }, { src: "ytcn26/quad/guida_01.jpg", x: 440, r: 0 }];
export type QuadProps = { title: string[]; kicker: string; guide: string[]; word: string };

export const Quad4: React.FC<QuadProps> = ({ title, kicker, guide, word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = (d: number, cfg = { damping: 14, stiffness: 170, mass: 0.7 }) => spring({ frame: frame - d, fps, config: cfg });
  // titolo d'apertura: sta al centro per due secondi e mezzo (Ross 23/11: «un secondo in più»), poi esce verso l'alto
  const T_OUT = 76;
  const tin = sp(2), tout = interpolate(frame, [T_OUT, T_OUT + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pulse = 1 + 0.05 * Math.max(0, Math.sin(((frame - 60) / fps) * Math.PI * 1.1)) * (frame > 60 ? 1 : 0);
  return (
    <AbsoluteFill style={{ background: BRAND.green, fontFamily: FONT }}>
      {BANDS.map((b, i) => {
        const lab = sp(T_OUT + 9 + i * 4), right = b.side === "right";   // le etichette entrano quando il titolo è uscito
        return (
          <div key={i} style={{ position: "absolute", left: 0, top: i * BH, width: 1080, height: BH, overflow: "hidden" }}>
            <OffthreadVideo src={staticFile(b.src)} muted style={{ width: 1080, height: BH, objectFit: "cover" }} />
            {/* etichetta: numero nel cerchio lime e nome dell'esercizio, dal lato libero dell'inquadratura */}
            <div style={{ position: "absolute", [b.side]: 20, top: b.top, display: "flex", flexDirection: right ? "row-reverse" : "row", alignItems: "center", gap: 12, opacity: Math.min(1, lab * 1.5), transform: `translateX(${(1 - lab) * (right ? 30 : -30)}px)` }}>
              <div style={{ width: 70, height: 70, borderRadius: 35, background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 48, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{b.n}</div>
              <div style={{ background: "rgba(11,15,10,0.88)", color: BRAND.white, fontWeight: 900, fontSize: 40, lineHeight: 1.02, padding: "8px 16px 11px", borderRadius: 12, textTransform: "uppercase", textAlign: right ? "right" : "left" }}>
                {b.name.map((l, j) => <div key={j} style={{ whiteSpace: "nowrap" }}>{l}</div>)}
              </div>
            </div>
          </div>
        );
      })}
      {/* quinta fascia: il banner della guida */}
      <div style={{ position: "absolute", left: 0, top: BAN_TOP, width: 1080, height: 1920 - BAN_TOP, background: `linear-gradient(180deg, ${BRAND.green} 0%, #1C3D15 100%)`, overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, width: 1080, top: 22, display: "flex", justifyContent: "center", alignItems: "center", gap: 18 }}>
          <div style={{ fontWeight: 800, fontSize: 64, color: BRAND.white }}>Commenta</div>
          <div style={{ background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 74, lineHeight: 1, padding: "4px 24px 10px", borderRadius: 16, transform: `scale(${pulse})` }}>{word}</div>
        </div>
        {guide.map((l, i) => <div key={i} style={{ position: "absolute", left: 0, width: 1080, top: 118 + i * 50, textAlign: "center", fontWeight: 800, fontSize: 46, color: BRAND.cream }}>{l}</div>)}
        {/* pagine della guida che spuntano dal basso (decorazione: su Instagram questa parte sta sotto nome e didascalia) */}
        {PAGES.map((pg, i) => {
          const k = sp(6 + i * 5, { damping: 13, stiffness: 120, mass: 0.8 });   // le scritte del banner ci sono dal primo fotogramma, le pagine salgono subito dopo
          return <Img key={i} src={staticFile(pg.src)} style={{ position: "absolute", left: pg.x, top: 214 + (1 - k) * 300 + (i === 2 ? -10 : 14) + 4 * Math.sin(frame / 14 + i), width: 200, borderRadius: 12, boxShadow: "0 10px 26px rgba(0,0,0,0.5)", transform: `rotate(${pg.r}deg)` }} />;
        })}
      </div>
      {/* righe di separazione tra le fasce */}
      {[1, 2, 3, 4].map((i) => <div key={i} style={{ position: "absolute", left: 0, top: i * BH - 3, width: 1080, height: 6, background: BRAND.lime }} />)}
      {/* titolo d'apertura sulle quattro fasce dei video, con il velo scuro dietro (0,72) */}
      {frame < T_OUT + 12 ? (
        <AbsoluteFill style={{ height: BAN_TOP, background: `rgba(11,15,10,${0.72 * Math.min(1, tin * 1.4) * (1 - tout)})` }}>
          <div style={{ position: "absolute", left: 0, width: 1080, top: 520 - tout * 220, textAlign: "center", opacity: Math.min(1, tin * 1.5) * (1 - tout), transform: `scale(${0.8 + 0.2 * tin})` }}>
            <div style={{ display: "inline-block", background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 40, letterSpacing: 3, textTransform: "uppercase", padding: "8px 26px", borderRadius: 12, marginBottom: 22 }}>{kicker}</div>
            {title.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: i === 0 ? 150 : 84, lineHeight: 1.0, textTransform: "uppercase", color: i === 0 ? BRAND.lime : BRAND.white, textShadow: "0 6px 0 rgba(11,15,10,0.85), 0 10px 26px rgba(0,0,0,0.7)", whiteSpace: "nowrap" }}>{l}</div>)}
          </div>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
