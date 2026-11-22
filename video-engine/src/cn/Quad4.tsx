import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { BRAND } from "./types";

/* G13 · «4 esercizi per scaldarti in casa» (Ross 22/11): reel veloce a schermo diviso in quattro, i quattro esercizi del circuito insieme,
   muti, con un banner in fondo che invita a scaricare la guida. Niente sottotitoli (non c'è parlato) e niente pannello CTA: la CTA è il banner.
   Celle 540x640 già ritagliate con ffmpeg (public/ytcn26/quad/q1…q4.mp4): in alto i due esercizi a terra (il corpo sta in basso nella cella,
   sotto la zona dell'interfaccia di Instagram), in basso i due in piedi. Banner dentro la zona sicura (bordo basso a 1490 px, destra libera). */

const FONT = "Blinker, sans-serif";
const INK = "#0B0F0A";
const CW = 540, CH = 640;
export const QUAD_FRAMES = 240;
const CELLS = [
  { src: "ytcn26/quad/q1.mp4", n: "1", name: "Mountain climber" },
  { src: "ytcn26/quad/q2.mp4", n: "2", name: "Ponte glutei" },
  { src: "ytcn26/quad/q3.mp4", n: "3", name: "Affondi" },
  { src: "ytcn26/quad/q4.mp4", n: "4", name: "Jumping jack" },
];
export type QuadProps = { title: string[]; kicker: string; guide: string[]; word: string };

export const Quad4: React.FC<QuadProps> = ({ title, kicker, guide, word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = (d: number, cfg = { damping: 14, stiffness: 170, mass: 0.7 }) => spring({ frame: frame - d, fps, config: cfg });
  // titolo d'apertura: sta al centro per un secondo e mezzo, poi esce verso l'alto
  const tin = sp(2), tout = interpolate(frame, [46, 56], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ban = sp(18), pulse = 1 + 0.045 * Math.max(0, Math.sin(((frame - 60) / fps) * Math.PI * 1.1)) * (frame > 60 ? 1 : 0);
  return (
    <AbsoluteFill style={{ background: BRAND.green, fontFamily: FONT }}>
      {CELLS.map((c, i) => {
        const x = (i % 2) * CW, y = Math.floor(i / 2) * CH, k = sp(4 + i * 4), lab = sp(30 + i * 5);
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: CW, height: CH, overflow: "hidden", opacity: Math.min(1, k * 1.4), transform: `scale(${0.94 + 0.06 * k})` }}>
            <OffthreadVideo src={staticFile(c.src)} muted style={{ width: CW, height: CH, objectFit: "cover" }} />
            {/* etichetta: numero nel cerchio lime e nome dell'esercizio; nella fila alta sta sotto i 230 px (zona sicura) */}
            <div style={{ position: "absolute", left: 18, top: i < 2 ? 236 : 18, display: "flex", alignItems: "center", gap: 12, opacity: Math.min(1, lab * 1.5), transform: `translateX(${(1 - lab) * -30}px)` }}>
              <div style={{ width: 62, height: 62, borderRadius: 31, background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 42, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{c.n}</div>
              <div style={{ background: "rgba(11,15,10,0.88)", color: BRAND.white, fontWeight: 900, fontSize: 40, lineHeight: 1, padding: "10px 16px 13px", borderRadius: 12, textTransform: "uppercase", whiteSpace: "nowrap" }}>{c.name}</div>
            </div>
          </div>
        );
      })}
      {/* righe di separazione */}
      <div style={{ position: "absolute", left: CW - 4, top: 0, width: 8, height: 2 * CH, background: BRAND.green }} />
      <div style={{ position: "absolute", left: 0, top: CH - 4, width: 1080, height: 8, background: BRAND.green }} />
      {/* titolo d'apertura */}
      {frame < 58 ? (
        <AbsoluteFill style={{ background: `rgba(11,15,10,${0.5 * tin * (1 - tout)})` }}>
          <div style={{ position: "absolute", left: 0, width: 1080, top: 470 - tout * 220, textAlign: "center", opacity: Math.min(1, tin * 1.5) * (1 - tout), transform: `scale(${0.8 + 0.2 * tin})` }}>
            <div style={{ display: "inline-block", background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 40, letterSpacing: 3, textTransform: "uppercase", padding: "8px 26px", borderRadius: 12, marginBottom: 22 }}>{kicker}</div>
            {title.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: i === 0 ? 150 : 84, lineHeight: 1.0, textTransform: "uppercase", color: i === 0 ? BRAND.lime : BRAND.white, textShadow: "0 6px 0 rgba(11,15,10,0.85), 0 10px 26px rgba(0,0,0,0.7)", whiteSpace: "nowrap" }}>{l}</div>)}
          </div>
        </AbsoluteFill>
      ) : null}
      {/* banner della guida: sale dal basso e resta; la parola da commentare pulsa */}
      <div style={{ position: "absolute", left: 50, width: 900, top: 1296 + (1 - ban) * 260, height: 198, borderRadius: 32, background: BRAND.cream, border: `6px solid ${BRAND.lime}`, boxShadow: "0 10px 30px rgba(0,0,0,0.35)", display: "flex", alignItems: "center", gap: 24, padding: "0 26px", boxSizing: "border-box", opacity: Math.min(1, ban * 1.4) }}>
        <svg width={108} height={132} viewBox="0 0 108 132" style={{ flexShrink: 0 }}>
          <rect x={4} y={4} width={100} height={124} rx={12} fill={BRAND.green} />
          <rect x={20} y={24} width={68} height={12} rx={6} fill={BRAND.lime} />
          <rect x={20} y={48} width={68} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <rect x={20} y={64} width={52} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <rect x={20} y={80} width={60} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <path d={`M54 ${96 + 4 * Math.sin(frame / 5)} l0 18 m-9 -9 l9 9 l9 -9`} fill="none" stroke={BRAND.lime} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <div>
          {guide.map((l, i) => <div key={i} style={{ fontWeight: 800, fontSize: 41, lineHeight: 1.06, color: INK, whiteSpace: "nowrap" }}>{l}</div>)}
          <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 8 }}>
            <div style={{ fontWeight: 800, fontSize: 48, color: INK }}>Commenta</div>
            <div style={{ background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 62, lineHeight: 1, padding: "5px 22px 9px", borderRadius: 14, transform: `scale(${pulse})`, boxShadow: `0 0 0 4px ${INK}` }}>{word}</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
