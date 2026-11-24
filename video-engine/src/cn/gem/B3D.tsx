import React from "react";
import { Img, staticFile } from "remotion";

/* Rappresentazioni 3D (Ross 24/11: «l'omino dell'animazione è orribile, crea animazioni più realistiche, anche in 3D»).
   Il corridore è un corpo umano 3D vestito da corsa, reso in Blender (scripts/b3d/render.py) a fasi: ogni fase è un ciclo di N fotogrammi
   che si chiude su se stesso (public/ytcn26/b3d/<set>/<fase>_NNN.png, fondo trasparente). Qui le fasi si agganciano alle parole (`cues`)
   e passano una nell'altra in dissolvenza; dietro c'è un fondale verde chiaro (la figura è vestita di scuro come Daniele) e sopra gli
   effetti leggeri del momento (fiato che si condensa, sudore, calore, aria nel naso…). Stessa firma dei disegni della cartella:
   { t, uid, cues } su una tela 300x300. Un'azione diversa per reel: strati, mani e testa, jumping jack in casa, passo, naso, squat. */

const N = 40;
type Fx = "cold" | "hot" | "warm" | null;
type Over = React.FC<{ t: number; k: number; tp: number }>;   // t = tempo dell'elemento, k = ingresso della fase (0..1), tp = secondi dall'inizio della fase
type Phase = { name: string; fx?: Fx; over?: Over; once?: boolean };
type Set = { dir: string; phases: Phase[]; /** inizio (secondi) di ogni fase a partire dalle parole-aggancio; la fase 0 parte da 0; negativo = mai */ sched: (c: number[]) => number[]; back?: React.ReactNode };
const HALO: Record<string, string> = { cold: "rgba(150,210,255,0.6)", hot: "rgba(255,90,50,0.65)", warm: "rgba(255,170,60,0.6)" };
const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
const src = (dir: string, name: string, f: number) => staticFile(`ytcn26/b3d/${dir}/${name}_${String(f).padStart(3, "0")}.png`);
const LIME = "#95FF00", ICE = "#BFE3FF", HOT = "#FF6B4A", WARM = "#FFA43A";

/* ---------- effetti leggeri sopra il render ---------- */
/** sbuffi di fiato che si condensa, dalla bocca in (x, y) verso `dir` (1 = destra, -1 = sinistra) */
const Breath: React.FC<{ x: number; y: number; t: number; k: number; dir?: number; rate?: number }> = ({ x, y, t, k, dir = 1, rate = 0.55 }) => (
  <>{[0, 1, 2].map((i) => { const p = (t * rate + i / 3) % 1; return <div key={i} style={{ position: "absolute", left: x + dir * p * 46 - (dir < 0 ? 26 + p * 44 : 0), top: y - p * 34, width: 26 + p * 44, height: 20 + p * 34, borderRadius: "50%", background: "rgba(240,249,255,0.9)", filter: `blur(${5 + p * 8}px)`, opacity: k * Math.sin(Math.PI * p) * 0.85 }} />; })}</>
);
/** onde di calore che salgono da un punto */
const Waves: React.FC<{ pts: [number, number][]; t: number; k: number; color?: string; rise?: number }> = ({ pts, t, k, color = HOT, rise = 46 }) => (
  <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0, opacity: k }}>
    {pts.map(([x, y], i) => { const p = (t * 0.75 + i * 0.37) % 1, yy = y - p * rise; return <path key={i} d={`M${x} ${yy} q ${i % 2 ? 9 : -9} -8 0 -16 q ${i % 2 ? -9 : 9} -8 0 -16`} fill="none" stroke={color} strokeWidth={5.5} strokeLinecap="round" opacity={Math.sin(Math.PI * p)} />; })}
  </svg>
);
/** alone che pulsa su un punto del corpo (calore che esce) */
const Spot: React.FC<{ x: number; y: number; r: number; t: number; k: number; color?: string }> = ({ x, y, r, t, k, color = "rgba(255,90,40,0.85)" }) => (
  <div style={{ position: "absolute", left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: "50%", background: `radial-gradient(closest-side, ${color}, rgba(255,90,40,0))`, opacity: k * (0.7 + 0.3 * Math.sin(t * 5)), transform: `scale(${1 + 0.12 * Math.sin(t * 5)})` }} />
);
const Sweat: Over = ({ t, k }) => (
  <>
    {[0, 1, 2, 3].map((i) => { const p = (t * 0.9 + i * 0.27) % 1, x = [108, 178, 100, 186][i]; return <div key={i} style={{ position: "absolute", left: x, top: 40 + p * 70, width: 12, height: 18, borderRadius: "50% 50% 50% 50% / 62% 62% 38% 38%", background: "#9BD8FF", boxShadow: "inset -2px -2px 0 rgba(255,255,255,0.7)", opacity: k * clamp01(p * 6) * clamp01((1 - p) * 4) }} />; })}
    <Waves pts={[[120, 26], [150, 20], [180, 26]]} t={t} k={k} rise={22} />
  </>
);

/* ---------- aria nel naso (G10): la testa è di profilo, rivolta a sinistra. Percorso: davanti al naso → cavità nasale → gola → petto ---------- */
const AIR: [number, number][] = [[20, 150], [70, 148], [108, 146], [140, 140], [168, 148], [178, 176], [182, 214], [190, 256], [200, 296]];
const MOUTH: [number, number][] = [[24, 176], [74, 172], [112, 168], [150, 172], [176, 190], [184, 222], [192, 258], [200, 296]];
const along = (pts: [number, number][], u: number): [number, number] => { const x = clamp01(u) * (pts.length - 1), i = Math.min(pts.length - 2, Math.floor(x)), f = x - i; return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f]; };
const mix = (a: number[], b: number[], f: number) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * clamp01(f))).join(",")})`;
/** mode: sharp = aria gelida dalla bocca, punte azzurre fino al petto che fa male; nose = entra dal naso ancora fredda; warm = nel naso diventa calda;
 *  humid = calda e con goccioline; filter = i granelli si fermano al naso; shield = vie respiratorie protette (contorno lime) */
const Air = (mode: "sharp" | "nose" | "warm" | "humid" | "filter" | "shield"): Over => ({ t, k }) => {
  const path = mode === "sharp" ? MOUTH : AIR, heat = mode === "sharp" || mode === "nose" ? 99 : 0.36;   // punto del percorso da cui l'aria è calda
  return (
    <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0, opacity: k }}>
      {mode === "shield" || mode === "filter" ? <polyline points={AIR.slice(2).map((p) => p.join(",")).join(" ")} fill="none" stroke={LIME} strokeWidth={mode === "shield" ? 13 : 7} strokeLinecap="round" strokeLinejoin="round" opacity={mode === "shield" ? 0.55 + 0.25 * Math.sin(t * 4) : 0.3} /> : null}
      {Array.from({ length: 9 }).map((_, i) => {
        const u = (t * 0.42 + i / 9) % 1, [x, y] = along(path, u), cold = [150, 215, 255], hot = [255, 150, 50];
        const col = mix(cold, hot, (u - heat) * 9), wob = Math.sin(t * 6 + i * 2.1) * (u < 0.3 ? 5 : 2);
        return mode === "sharp"
          ? <polygon key={i} points={`${x - 9},${y + wob} ${x},${y - 5 + wob} ${x + 9},${y + wob} ${x},${y + 5 + wob}`} fill="#DDF1FF" stroke="#7CC4FF" strokeWidth={1.5} opacity={Math.sin(Math.PI * u) * 0.95} />
          : <circle key={i} cx={x} cy={y + wob} r={u < heat ? 6.5 : 7.5} fill={col} opacity={Math.sin(Math.PI * u) * 0.95} />;
      })}
      {mode === "sharp" ? <circle cx={196} cy={270} r={26 + 6 * Math.sin(t * 7)} fill="none" stroke={HOT} strokeWidth={5} opacity={0.6 + 0.4 * Math.sin(t * 7)} /> : null}
      {mode === "humid" ? [0, 1, 2].map((i) => { const u = (t * 0.5 + i / 3) % 1, [x, y] = along(AIR, 0.38 + u * 0.3); return <path key={i} d={`M${x} ${y - 16} q -6 9 0 13 q 6 -4 0 -13`} fill="#9BD8FF" opacity={Math.sin(Math.PI * u)} />; }) : null}
      {mode === "filter" ? [0, 1, 2, 3, 4].map((i) => { const u = Math.min(1, ((t * 0.5 + i / 5) % 1) * 1.6), x = 14 + u * 84 + (u >= 1 ? Math.sin(t * 9 + i) * 2 : 0), y = 132 + i * 8; return <rect key={i} x={x} y={y} width={7} height={7} rx={1.5} fill="#3A2A1C" stroke="#F4F1E5" strokeWidth={1.2} opacity={u >= 1 ? 0.9 : 0.85} transform={`rotate(${t * 80 + i * 40} ${x + 3.5} ${y + 3.5})`} />; }) : null}
    </svg>
  );
};

/* ---------- passo e respiro (G9, G11): la figura è di tre quarti, cammina verso sinistra ---------- */
/** terreno che scorre sotto i piedi (trattini) a velocità `v` */
const Ground: React.FC<{ t: number; v: number }> = ({ t, v }) => (
  <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0 }}>
    <line x1={18} y1={268} x2={282} y2={268} stroke="rgba(11,15,10,0.55)" strokeWidth={5} strokeLinecap="round" />
    {[0, 1, 2, 3, 4].map((i) => { const x = 18 + ((i * 58 + t * v) % 264); return <line key={i} x1={x} y1={280} x2={x + 26} y2={280} stroke="rgba(244,241,229,0.75)" strokeWidth={5} strokeLinecap="round" />; })}
  </svg>
);
/** indicatore d'intensità: arco con la lancetta che resta in basso (level 0..1) */
const Dial: React.FC<{ level: number; t: number; k: number }> = ({ level, t, k }) => {
  const a = Math.PI * (1 - (level + 0.015 * Math.sin(t * 5))), cx = 236, cy = 74, r = 40;
  return (
    <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0, opacity: k }}>
      <path d={`M${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`} fill="none" stroke="rgba(11,15,10,0.8)" strokeWidth={14} strokeLinecap="round" />
      <path d={`M${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx - r * Math.cos(Math.PI * 0.34)} ${cy - r * Math.sin(Math.PI * 0.34)}`} fill="none" stroke={LIME} strokeWidth={14} strokeLinecap="round" />
      <line x1={cx} y1={cy} x2={cx + Math.cos(a) * (r - 6)} y2={cy - Math.sin(a) * (r - 6)} stroke="#F4F1E5" strokeWidth={6} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={8} fill="#F4F1E5" />
    </svg>
  );
};
/** batteria che si riempie (level 0..1) */
const Battery: React.FC<{ level: number; t: number; k: number }> = ({ level, t, k }) => (
  <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0, opacity: k }}>
    <rect x={206} y={34} width={62} height={104} rx={12} fill="rgba(11,15,10,0.85)" stroke="#F4F1E5" strokeWidth={5} />
    <rect x={224} y={22} width={26} height={12} rx={4} fill="#F4F1E5" />
    {[0, 1, 2, 3].map((i) => <rect key={i} x={214} y={112 - i * 23} width={46} height={18} rx={5} fill={LIME} opacity={clamp01(level * 4 - i) * (i === Math.floor(level * 4 - 0.01) ? 0.75 + 0.25 * Math.sin(t * 6) : 1)} />)}
  </svg>
);
/** onda del respiro regolare che scorre dal naso (x, y) */
const BreathWave: React.FC<{ t: number; k: number; calm: boolean }> = ({ t, k, calm }) => {
  const pts: string[] = []; const amp = calm ? 13 : 24, f = calm ? 0.055 : 0.13;
  for (let x = 0; x <= 150; x += 5) pts.push(`${14 + x},${58 + Math.sin(x * f - t * (calm ? 3.2 : 9)) * amp * (calm ? 1 : 0.6 + 0.4 * Math.sin(x * 0.31))}`);
  return (
    <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0, opacity: k }}>
      <rect x={8} y={22} width={166} height={72} rx={14} fill="rgba(11,15,10,0.8)" />
      <polyline points={pts.join(" ")} fill="none" stroke={calm ? LIME : HOT} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
};

/* ---------- componente ---------- */
export const makeB3D = (set: Set): React.FC<{ t: number; uid: string; cues: number[] }> => ({ t, cues }) => {
  const st = set.sched(cues);
  let idx = 0; st.forEach((s, i) => { if (i > 0 && s !== undefined && s >= 0 && t >= s) idx = i; });
  let prev = 0; for (let i = idx - 1; i > 0; i--) if (st[i] !== undefined && st[i] >= 0 && st[i] <= st[idx]) { prev = i; break; }
  const k = idx === 0 ? 1 : clamp01((t - st[idx]) / 0.3), loop = ((Math.floor(t * 30) % N) + N) % N;
  const fr = (i: number) => (set.phases[i].once ? Math.min(N - 1, Math.max(0, Math.floor((t - (i === 0 ? 0 : st[i])) * 30))) : loop);
  const A = set.phases[prev], B = set.phases[idx], tp = t - (idx === 0 ? 0 : st[idx]);
  const img: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 300, height: 300 };
  const halo = (fx: string, o: number) => <div style={{ position: "absolute", left: 20, top: 10, width: 260, height: 280, borderRadius: "50%", background: `radial-gradient(closest-side, ${HALO[fx]}, rgba(0,0,0,0))`, opacity: o }} />;
  return (
    <div style={{ position: "relative", width: 300, height: 300, borderRadius: 26, overflow: "hidden", background: "radial-gradient(circle at 50% 38%, #6BA944 0%, #49762E 55%, #2F4D1E 100%)" }}>
      {set.back}
      {A.fx && k < 1 ? halo(A.fx, 1 - k) : null}
      {B.fx ? halo(B.fx, k * (0.82 + 0.18 * Math.sin(t * 3.2))) : null}
      {k < 1 ? <Img src={src(set.dir, A.name, fr(prev))} style={img} /> : null}
      <Img src={src(set.dir, B.name, fr(idx))} style={{ ...img, opacity: k }} />
      {B.over ? <B.over t={t} k={k} tp={tp} /> : null}
    </div>
  );
};
const at = (c: number[], i: number, plus = 0) => (c[i] === undefined || c[i] < 0 ? -1 : c[i] + plus);

/* G1 · troppi strati: maglia → gilet → giacca → piumino con cappello e guanti (uno ogni 0,6 s da «più strati»), poi surriscaldato */
export const B3DOver = makeB3D({ dir: "g1", phases: [{ name: "over_0" }, { name: "over_1" }, { name: "over_2" }, { name: "over_3" }, { name: "over_4", fx: "hot", over: Sweat }], sched: (c) => [0, at(c, 0), at(c, 0, 0.6), at(c, 0, 1.2), at(c, 2)] });
/* G1 · brivido iniziale: infreddolito → corsa → corpo caldo (aggancio 0 = comincia a correre, aggancio 1 = si è scaldato) */
const coldBreath: Over = ({ t, k }) => <Breath x={158} y={50} t={t} k={k} />;
const warmWaves: Over = ({ t, k }) => <Waves pts={[[64, 150], [236, 150], [52, 200], [248, 200]]} t={t} k={k} color={WARM} />;
export const B3DWarm = makeB3D({ dir: "g1", phases: [{ name: "warm_0", fx: "cold", over: coldBreath }, { name: "warm_1" }, { name: "warm_2", fx: "warm", over: warmWaves }], sched: (c) => [0, at(c, 0), at(c, 1)] });
export const B3DWarmOk = makeB3D({ dir: "g1", phases: [{ name: "warm_2", fx: "warm", over: warmWaves }], sched: () => [0] });

/* G3 · mani e testa: a mani e testa scoperte il calore esce da lì; poi guanti e fascia, poi guanti e cappello */
const heatLoss: Over = ({ t, k }) => (
  <>
    <Spot x={92} y={96} r={40} t={t} k={k} /><Spot x={176} y={92} r={40} t={t + 0.4} k={k} /><Spot x={148} y={36} r={44} t={t + 0.8} k={k} />
    <Waves pts={[[84, 70], [104, 64], [168, 66], [188, 60], [134, 12], [162, 12]]} t={t} k={k} rise={30} />
  </>
);
export const B3DMani = makeB3D({ dir: "g3", phases: [{ name: "mani_0", fx: "cold", over: heatLoss }, { name: "mani_1" }, { name: "mani_2", fx: "warm" }], sched: (c) => [0, at(c, 0), at(c, 1)] });

/* G4 · riscaldamento in casa: dentro casa (contorno della casa dietro la figura) fermo e freddo → jumping jack → caldo */
const House = (
  <svg width={300} height={300} style={{ position: "absolute", left: 0, top: 0 }}>
    <path d="M22 132 L150 26 L278 132 M48 112 V286 H252 V112" fill="rgba(11,15,10,0.28)" stroke={LIME} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
export const B3DCasa = makeB3D({ dir: "g4", back: House, phases: [{ name: "casa_0", fx: "cold" }, { name: "casa_1" }, { name: "casa_2", fx: "warm", over: ({ t, k }) => <Waves pts={[[76, 150], [226, 150]]} t={t} k={k} color={WARM} /> }], sched: (c) => [0, at(c, 0), at(c, 1)] });

/* G9 · corsa di riscaldamento: al passo, intensità molto bassa (lancetta in basso); poi corsa leggera con la batteria piena */
export const B3DPasso = makeB3D({ dir: "g9", phases: [{ name: "passo_0", over: ({ t, k }) => <><Ground t={t} v={-70} /><Dial level={0.16} t={t} k={k} /></> }], sched: () => [0] });
export const B3DEnergia = makeB3D({ dir: "g9", phases: [
  { name: "passo_1", fx: "warm", over: ({ t, k, tp }) => <><Ground t={t} v={-150} /><Battery level={0.5 + 0.5 * clamp01(tp / 1.6)} t={t} k={k} /></> },
], sched: () => [0] });

/* G10 · respirare dal naso al freddo */
export const B3DNasoFreddo = makeB3D({ dir: "g10", phases: [{ name: "naso_0", fx: "cold", over: Air("sharp") }], sched: () => [0] });
export const B3DNaso = makeB3D({ dir: "g10", phases: [{ name: "naso_0", fx: "cold", over: Air("nose") }, { name: "naso_1", fx: "warm", over: Air("warm") }, { name: "naso_1", fx: "warm", over: Air("humid") }], sched: (c) => [0, at(c, 0), at(c, 1)] });
export const B3DNasoFiltro = makeB3D({ dir: "g10", phases: [{ name: "naso_1", fx: "warm", over: Air("warm") }, { name: "naso_1", fx: "warm", over: Air("filter") }, { name: "naso_1", fx: "warm", over: Air("shield") }], sched: (c) => [0, at(c, 0), at(c, 1)] });

/* G11 · niente affanno: corsa leggera con il respiro regolare (onda calma); l'affanno è l'onda rossa e irregolare */
export const B3DRespiro = makeB3D({ dir: "g9", phases: [
  { name: "passo_1", over: ({ t, k }) => <><Ground t={t} v={-150} /><BreathWave t={t} k={k} calm /></> },
  { name: "passo_1", over: ({ t, k }) => <><Ground t={t} v={-150} /><BreathWave t={t} k={k} calm={false} /></> },
  { name: "passo_1", fx: "warm", over: ({ t, k }) => <><Ground t={t} v={-150} /><BreathWave t={t} k={k} calm /></> },
], sched: (c) => [0, at(c, 0), at(c, 1)] });

/* G12 · squat naturale: in piedi → scende (una volta) → resta accovacciato */
export const B3DSquat = makeB3D({ dir: "g12", phases: [{ name: "squat_0" }, { name: "squat_1", once: true }, { name: "squat_2", fx: "warm" }], sched: (c) => [0, at(c, 0), at(c, 0, 1.25)] });
export const B3DSquatGiu = makeB3D({ dir: "g12", phases: [{ name: "squat_2", fx: "warm" }], sched: () => [0] });
