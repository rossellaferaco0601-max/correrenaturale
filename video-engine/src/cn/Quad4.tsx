import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { BRAND } from "./types";

/* G13 · «4 esercizi per scaldarti in casa» (Ross 22/11): reel veloce con lo schermo diviso in QUATTRO FASCE ORIZZONTALI a tutta larghezza
   che riempiono TUTTO lo schermo anche in altezza (4 x 480 px, nessuna zona vuota), i quattro esercizi del circuito insieme e muti;
   in basso, sopra il video, il banner «scarica la guida». Niente sottotitoli (non c'è parlato) e niente pannello CTA: la CTA è il banner.
   Fasce 1080x480 già ritagliate con ffmpeg (public/ytcn26/quad/b1…b4.mp4), tutte con il corpo intero.
   Ordine delle fasce: gli esercizi a terra stanno in alto e in basso (sopra il corpo c'è parete libera), quelli in piedi in mezzo. L'ultima
   fascia è il ponte perché il banner deve stare nella parte più bassa che Instagram lascia leggibile (fino a ~1580 px) senza coprire
   l'esercizio: lì sopra il corpo c'è solo parete. Per questo le fasce non hanno il numero (non sono nell'ordine del circuito). */

const FONT = "Blinker, sans-serif";
const INK = "#0B0F0A";
const BH = 480;
export const QUAD_FRAMES = 240;
const BANDS: { src: string; name: string[]; top: number }[] = [
  { src: "ytcn26/quad/b1.mp4", name: ["Mountain", "climber"], top: 236 },   // sotto i 220 px dell'interfaccia in alto
  { src: "ytcn26/quad/b2.mp4", name: ["Affondi"], top: 20 },
  { src: "ytcn26/quad/b3.mp4", name: ["Jumping", "jack"], top: 20 },
  { src: "ytcn26/quad/b4.mp4", name: ["Ponte per", "i glutei"], top: 16 },
];
export type QuadProps = { title: string[]; kicker: string; guide: string[]; word: string };

export const Quad4: React.FC<QuadProps> = ({ title, kicker, guide, word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = (d: number, cfg = { damping: 14, stiffness: 170, mass: 0.7 }) => spring({ frame: frame - d, fps, config: cfg });
  // titolo d'apertura: sta al centro per un secondo e mezzo, poi esce verso l'alto
  const tin = sp(2), tout = interpolate(frame, [46, 56], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ban = sp(16), pulse = 1 + 0.05 * Math.max(0, Math.sin(((frame - 60) / fps) * Math.PI * 1.1)) * (frame > 60 ? 1 : 0);
  return (
    <AbsoluteFill style={{ background: INK, fontFamily: FONT }}>
      {BANDS.map((b, i) => {
        const lab = sp(30 + i * 5);   // le fasce ci sono dal primo fotogramma (niente fotogramma nero in apertura)
        return (
          <div key={i} style={{ position: "absolute", left: 0, top: i * BH, width: 1080, height: BH, overflow: "hidden" }}>
            <OffthreadVideo src={staticFile(b.src)} muted style={{ width: 1080, height: BH, objectFit: "cover" }} />
            {/* nome dell'esercizio, in alto a sinistra (parete libera) */}
            <div style={{ position: "absolute", left: 20, top: b.top, background: "rgba(11,15,10,0.88)", borderLeft: `10px solid ${BRAND.lime}`, color: BRAND.white, fontWeight: 900, fontSize: 42, lineHeight: 1.02, padding: "8px 18px 11px 14px", borderRadius: 10, textTransform: "uppercase", opacity: Math.min(1, lab * 1.5), transform: `translateX(${(1 - lab) * -30}px)` }}>
              {b.name.map((l, j) => <div key={j} style={{ whiteSpace: "nowrap" }}>{l}</div>)}
            </div>
          </div>
        );
      })}
      {/* righe di separazione tra le fasce */}
      {[1, 2, 3].map((i) => <div key={i} style={{ position: "absolute", left: 0, top: i * BH - 3, width: 1080, height: 6, background: BRAND.lime }} />)}
      {/* titolo d'apertura */}
      {frame < 58 ? (
        <AbsoluteFill style={{ background: `rgba(11,15,10,${0.55 * tin * (1 - tout)})` }}>
          <div style={{ position: "absolute", left: 0, width: 1080, top: 640 - tout * 220, textAlign: "center", opacity: Math.min(1, tin * 1.5) * (1 - tout), transform: `scale(${0.8 + 0.2 * tin})` }}>
            <div style={{ display: "inline-block", background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 40, letterSpacing: 3, textTransform: "uppercase", padding: "8px 26px", borderRadius: 12, marginBottom: 22 }}>{kicker}</div>
            {title.map((l, i) => <div key={i} style={{ fontWeight: 900, fontSize: i === 0 ? 150 : 84, lineHeight: 1.0, textTransform: "uppercase", color: i === 0 ? BRAND.lime : BRAND.white, textShadow: "0 6px 0 rgba(11,15,10,0.85), 0 10px 26px rgba(0,0,0,0.7)", whiteSpace: "nowrap" }}>{l}</div>)}
          </div>
        </AbsoluteFill>
      ) : null}
      {/* banner della guida: sopra il video, nella parete libera dell'ultima fascia, a destra del nome dell'esercizio; la riga con la parola da
          commentare sta in alto (zona sicura), quella della guida subito sotto */}
      <div style={{ position: "absolute", left: 300, width: 650, top: 3 * BH + 12 + (1 - ban) * 200, height: 142, borderRadius: 26, background: BRAND.cream, border: `6px solid ${BRAND.lime}`, boxShadow: "0 10px 30px rgba(0,0,0,0.45)", display: "flex", alignItems: "center", gap: 18, padding: "0 20px", boxSizing: "border-box", opacity: Math.min(1, ban * 1.4) }}>
        <svg width={84} height={104} viewBox="0 0 108 132" style={{ flexShrink: 0 }}>
          <rect x={4} y={4} width={100} height={124} rx={12} fill={BRAND.green} />
          <rect x={20} y={24} width={68} height={12} rx={6} fill={BRAND.lime} />
          <rect x={20} y={48} width={68} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <rect x={20} y={64} width={52} height={8} rx={4} fill="rgba(244,241,229,0.85)" />
          <path d={`M54 ${84 + 4 * Math.sin(frame / 5)} l0 26 m-11 -11 l11 11 l11 -11`} fill="none" stroke={BRAND.lime} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ fontWeight: 800, fontSize: 44, color: INK }}>Commenta</div>
            <div style={{ background: BRAND.lime, color: INK, fontWeight: 900, fontSize: 52, lineHeight: 1, padding: "4px 18px 8px", borderRadius: 12, transform: `scale(${pulse})`, boxShadow: `0 0 0 4px ${INK}` }}>{word}</div>
          </div>
          {guide.map((l, i) => <div key={i} style={{ fontWeight: 800, fontSize: 33, lineHeight: 1.1, color: INK, whiteSpace: "nowrap", marginTop: i === 0 ? 8 : 0 }}>{l}</div>)}
        </div>
      </div>
    </AbsoluteFill>
  );
};
