import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { BRAND } from "./types";

/* G13 · «4 esercizi per scaldarti in casa» (Ross 22/11): reel veloce con lo schermo diviso in QUATTRO FASCE ORIZZONTALI a tutta larghezza,
   una sotto l'altra, i quattro esercizi del circuito insieme e muti; in fondo il banner «scarica la guida». Niente sottotitoli (non c'è
   parlato) e niente pannello CTA: la CTA è il banner.
   Fasce 1080x322 già ritagliate con ffmpeg (public/ytcn26/quad/b1…b4.mp4): i due esercizi a terra stanno interi nella fascia; affondi e
   jumping jack sono in piedi e in una fascia orizzontale non ci stanno interi, quindi usano le inquadrature strette dell'originale
   (gambe che affondano; campo largo, piedi e mezzo busto del jumping jack). Banner dentro la zona sicura (bordo basso a 1496 px, destra libera). */

const FONT = "Blinker, sans-serif";
const INK = "#0B0F0A";
const BH = 322;
export const QUAD_FRAMES = 240;
const BANDS: { src: string; n: string; name: string[]; side: "left" | "right"; top: number }[] = [
  { src: "ytcn26/quad/b1.mp4", n: "1", name: ["Mountain", "climber"], side: "right", top: 232 },   // sotto i 220 px dell'interfaccia in alto
  { src: "ytcn26/quad/b2.mp4", n: "2", name: ["Ponte per", "i glutei"], side: "right", top: 18 },
  { src: "ytcn26/quad/b3.mp4", n: "3", name: ["Affondi"], side: "left", top: 18 },                 // a destra, da qui in giù, ci sono i comandi di Instagram
  { src: "ytcn26/quad/b4.mp4", n: "4", name: ["Jumping", "jack"], side: "left", top: 18 },
];
export type QuadProps = { title: string[]; kicker: string; guide: string[]; word: string };

export const Quad4: React.FC<QuadProps> = ({ title, kicker, guide, word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = (d: number, cfg = { damping: 14, stiffness: 170, mass: 0.7 }) => spring({ frame: frame - d, fps, config: cfg });
  // titolo d'apertura: sta al centro per un secondo e mezzo, poi esce verso l'alto
  const tin = sp(2), tout = interpolate(frame, [46, 56], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ban = sp(16), pulse = 1 + 0.045 * Math.max(0, Math.sin(((frame - 60) / fps) * Math.PI * 1.1)) * (frame > 60 ? 1 : 0);
  return (
    <AbsoluteFill style={{ background: BRAND.green, fontFamily: FONT }}>
      {BANDS.map((b, i) => {
        const k = sp(3 + i * 4), lab = sp(30 + i * 5), right = b.side === "right";
        return (
          <div key={i} style={{ position: "absolute", left: 0, top: i * BH, width: 1080, height: BH, overflow: "hidden", opacity: Math.min(1, k * 1.5), transform: `translateX(${(1 - k) * (i % 2 ? 90 : -90)}px)` }}>
            <OffthreadVideo src={staticFile(b.src)} muted style={{ width: 1080, height: BH, objectFit: "cover" }} />
            {/* etichetta: numero nel cerchio lime e nome dell'esercizio, dal lato libero dell'inquadratura */}
            <div style={{ position: "absolute", [b.side]: 20, top: b.top, display: "flex", flexDirection: right ? "row-reverse" : "row", alignItems: "center", gap: 12, opacity: Math.min(1, lab * 1.5), transform: `translateX(${(1 - lab) * (right ? 30 : -30)}px)` }}>
              <div style={{ width: 66, height: 66, borderRadius: 33, background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 46, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{b.n}</div>
              <div style={{ background: "rgba(11,15,10,0.88)", color: BRAND.white, fontWeight: 900, fontSize: 38, lineHeight: 1.02, padding: "8px 16px 11px", borderRadius: 12, textTransform: "uppercase", textAlign: right ? "right" : "left" }}>
                {b.name.map((l, j) => <div key={j} style={{ whiteSpace: "nowrap" }}>{l}</div>)}
              </div>
            </div>
          </div>
        );
      })}
      {/* righe di separazione tra le fasce */}
      {[1, 2, 3, 4].map((i) => <div key={i} style={{ position: "absolute", left: 0, top: i * BH - 3, width: 1080, height: 6, background: BRAND.green }} />)}
      {/* titolo d'apertura */}
      {frame < 58 ? (
        <AbsoluteFill style={{ background: `rgba(11,15,10,${0.55 * tin * (1 - tout)})` }}>
          <div style={{ position: "absolute", left: 0, width: 1080, top: 470 - tout * 220, textAlign: "center", opacity: Math.min(1, tin * 1.5) * (1 - tout), transform: `scale(${0.8 + 0.2 * tin})` }}>
            <div style={{ display: "inline-block", background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 40, letterSpacing: 3, textTransform: "uppercase", padding: "8px 26px", borderRadius: 12, marginBottom: 22 }}>{kicker}</div>
            {title.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: i === 0 ? 150 : 84, lineHeight: 1.0, textTransform: "uppercase", color: i === 0 ? BRAND.lime : BRAND.white, textShadow: "0 6px 0 rgba(11,15,10,0.85), 0 10px 26px rgba(0,0,0,0.7)", whiteSpace: "nowrap" }}>{l}</div>)}
          </div>
        </AbsoluteFill>
      ) : null}
      {/* banner della guida: sale dal basso e resta; la parola da commentare pulsa */}
      <div style={{ position: "absolute", left: 50, width: 900, top: 1300 + (1 - ban) * 260, height: 196, borderRadius: 32, background: BRAND.cream, border: `6px solid ${BRAND.lime}`, boxShadow: "0 10px 30px rgba(0,0,0,0.35)", display: "flex", alignItems: "center", gap: 24, padding: "0 26px", boxSizing: "border-box", opacity: Math.min(1, ban * 1.4) }}>
        <svg width={108} height={132} viewBox="0 0 108 132" style={{ flexShrink: 0 }}>
          <rect x={4} y={4} width={100} height={124} rx={12} fill={BRAND.green} />
          <rect x={20} y={24} width={68} height={12} rx={6} fill={BRAND.lime} />
          <rect x={20} y={48} width={68} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <rect x={20} y={64} width={52} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <rect x={20} y={80} width={60} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <path d={`M54 ${96 + 4 * Math.sin(frame / 5)} l0 18 m-9 -9 l9 9 l9 -9`} fill="none" stroke={BRAND.lime} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <div>
          {guide.map((l, i) => <div key={i} style={{ fontWeight: i === 0 ? 900 : 700, fontSize: i === 0 ? 46 : 37, lineHeight: 1.08, color: INK, whiteSpace: "nowrap", textTransform: i === 0 ? "uppercase" : "none" }}>{l}</div>)}
          <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 8 }}>
            <div style={{ fontWeight: 800, fontSize: 44, color: INK }}>Commenta</div>
            <div style={{ background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 58, lineHeight: 1, padding: "5px 22px 9px", borderRadius: 14, transform: `scale(${pulse})`, boxShadow: `0 0 0 4px ${INK}` }}>{word}</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
