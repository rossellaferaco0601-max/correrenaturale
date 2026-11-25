// Export «a livelli» per CapCut (Ross 25/11: «da oggi in poi restituiscimi i reel così: video pulito + ogni grafica su fondo trasparente,
// ogni cosa deve essere editabile; alla fine decido io se va bene o se portarlo in CapCut»).
// Per un reel scrive in out/<serie>/livelli/<ID>/:
//   lista.sh            → i comandi di render (uno per livello; da far girare nella coda unica, un render alla volta)
//   MONTAGGIO.txt       → dove mettere ogni file sulla linea del tempo di CapCut (inizio, durata, cosa è)
//   sottotitoli.srt     → i sottotitoli come testo modificabile (stesse pagine di 2-3 parole del reel)
// I livelli: 00_video.mp4 (video pulito con l'audio e i movimenti di camera, nessuna scritta), una .mov ProRes 4444 con trasparenza per
// ogni grafica, sottotitoli.mov (stile del brand, trasparente), cta.mov (pannello finale con il suono del clic), eventuali apertura,
// banner e intestazione. Ogni .mov contiene SOLO il tratto in cui il livello è a schermo: va messo all'inizio indicato in MONTAGGIO.txt.
// Uso: npx tsx scripts/cn_layers.ts G3-mani [G4-casa …]   poi: bash out/ytcn26/livelli/G3-mani/lista.sh
import { mkdirSync, writeFileSync, readFileSync, existsSync } from "node:fs";
import { REELS } from "../src/cn/reels51";
import { layout, remapWords, resolveStart, tailFrames } from "../src/cn/timeline";
import { paginate } from "../src/cn/Captions";

const FPS = 30;
const tc = (f: number) => { const s = f / FPS, m = Math.floor(s / 60); return `${m}:${(s - m * 60).toFixed(2).padStart(5, "0")}`; };
const srtT = (f: number) => { const ms = Math.round((f / FPS) * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")},${String(ms % 1000).padStart(3, "0")}`; };
const slug = (t: string) => t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 28);
const NAMES: Record<string, string> = { fog: "titolo", gem: "pannello", kin: "parole", slam: "schianto", takeaway: "scheda-finale", ambient: "bordi", dose: "durate", ticks: "riepilogo", chips: "pillole", bigstrike: "frase-barrata", layers: "strati", hangtag: "cartellino", gust: "vento", rings: "anelli", duel: "sudore-gelo" };
const PRORES = "--codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png";

for (const id of process.argv.slice(2)) {
  const r = REELS.find((x) => x.id === id);
  if (!r) { console.error("reel non trovato:", id); continue; }
  const p = r.props, tailF = tailFrames(p.tailSeconds);
  const { items, total } = layout(p.segments, p.blendFrames, tailF);
  const words = remapWords(p.words, items, p.wordFix, p.wordOffset);
  const introF = p.intro ? Math.round(p.intro.seconds * FPS) : 0;
  const ctaF = Math.round(p.ctaSeconds * FPS);
  const lead = p.ctaLead !== undefined ? Math.round(p.ctaLead * FPS) : -1;
  const xfade = lead >= 0 ? tailF + lead : Math.max(9, tailF - Math.round((p.tailHold ?? 0) * FPS));
  const END = introF + total + ctaF - 1;   // ultimo fotogramma del reel
  const Y = p.master.split("/")[0], dir = `out/${Y}/livelli/${id}`;
  mkdirSync(dir, { recursive: true });
  type Row = { file: string; a: number; b: number; what: string; layer: string | number; video?: boolean };
  const rows: Row[] = [];
  rows.push({ file: "00_video.mp4", a: introF, b: introF + total - 1, what: "video pulito con l'audio (niente scritte); movimenti di camera già dentro", layer: "video", video: true });
  if (p.intro) rows.push({ file: "01_apertura.mov", a: 0, b: introF + 9, what: `apertura a tutto schermo: «${p.intro.lines.join(" ")}» (il video parte sotto)`, layer: "intro" });
  if (p.banner) rows.push({ file: "02_banner.mov", a: introF, b: introF + total - 1, what: `banner fisso «${p.banner.text[0]} ${p.banner.word} ${p.banner.text[1]}»`, layer: "banner" });
  if (p.winHeader) rows.push({ file: "03_intestazione.mov", a: introF, b: introF + total - 1, what: `intestazione dell'esercizio «${p.winHeader.title.replace("|", " ")}» (compare quando non c'è un pannello)`, layer: "header" });
  p.elements.forEach((el, i) => {
    const s = resolveStart(el, words), durF = Math.round(el.dur * FPS);
    const a = introF + Math.max(0, s), b = el.kind === "takeaway" ? introF + total - 1 : Math.min(introF + total - 1, introF + s + durF + 1);
    const txt = "lines" in el && Array.isArray(el.lines) ? el.lines.join(" ") : "words" in el && Array.isArray(el.words) ? el.words.join(" ") : "text" in el ? String(el.text) : "phases" in el && Array.isArray(el.phases) ? (el.phases as unknown[]).map((ph) => (Array.isArray(ph) ? ph : (ph as { lines: string[] }).lines).join(" ")).join(" / ") : "items" in el && Array.isArray(el.items) ? el.items.join(", ") : el.kind === "ambient" ? (el.mood === "frost" ? "gelo sui bordi" : "calore sui bordi") : "";
    const nm = `${String(10 + i).padStart(2, "0")}_${NAMES[el.kind] ?? el.kind}_${slug(txt.split(" / ")[0])}.mov`;
    rows.push({ file: nm, a, b, what: `${NAMES[el.kind] ?? el.kind}: ${txt}`, layer: i });
  });
  rows.push({ file: "80_sottotitoli.mov", a: introF, b: introF + total - 1, what: "sottotitoli nello stile del brand (in lime la parola detta). In alternativa importa sottotitoli.srt come testo", layer: "caps" });
  if (ctaF > 0) rows.push({ file: "90_cta.mov", a: introF + total - xfade, b: END, what: `pannello finale «Commenta ${p.cta.word}» (con il suono del clic)`, layer: "cta" });

  // comandi di render (uno alla volta). Il video pulito esce già con l'audio alla loudness dei reel (-13 LUFS come cn_finish.sh)
  const cmds = [`#!/usr/bin/env bash`, `# livelli di ${id}: generato da scripts/cn_layers.ts`, `set -e; cd "$(dirname "$0")/../../../.."`];
  for (const row of rows) {
    const out = `${dir}/${row.file}`, props = JSON.stringify({ layer: row.layer });
    if (row.video) {
      cmds.push(`[ -f ${out} ] || { npx remotion render ${id} ${dir}/_video_raw.mp4 --props='${props}' --frames=${row.a}-${row.b} --codec=h264 --crf=16 --log=error && ffmpeg -loglevel error -y -i ${dir}/_video_raw.mp4 -af "loudnorm=I=-13:TP=-1.5:LRA=11,aresample=48000" -c:v copy -c:a aac -b:a 256k -movflags +faststart ${out} && rm -f ${dir}/_video_raw.mp4; }`);
    } else {
      // ProRes 4444 di Remotion pesa ~5 MB al secondo anche dove è tutto trasparente: si ricomprime (qscale 13, metà peso, trasparenza intatta)
      cmds.push(`[ -f ${out} ] || { npx remotion render ${id} ${dir}/_tmp.mov --props='${props}' --frames=${row.a}-${row.b} ${PRORES} --log=error && ffmpeg -loglevel error -y -i ${dir}/_tmp.mov -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le -qscale:v 13 -vendor apl0 -c:a copy ${out} && rm -f ${dir}/_tmp.mov; }`);
    }
    cmds.push(`echo "fatto ${row.file}"`);
  }
  writeFileSync(`${dir}/lista.sh`, cmds.join("\n") + "\n", { mode: 0o755 });

  // sottotitoli come testo: stesse pagine del reel, nel tempo del reel (dopo l'eventuale apertura)
  const pages = paginate(words).filter((pg) => pg.start >= Math.round((p.capFrom ?? 0) * FPS) && pg.start < total);
  writeFileSync(`${dir}/sottotitoli.srt`, pages.map((pg, i) => `${i + 1}\n${srtT(introF + pg.start)} --> ${srtT(introF + Math.min(pg.end, total - 4))}\n${pg.words.map((w) => w.text.trim()).join(" ").toUpperCase()}\n`).join("\n"));

  const lines = [
    `${id} · ${r.title}`,
    `Reel di ${tc(END + 1)} (1080×1920, 30 fps). Livelli dal basso verso l'alto: prima il video, poi le grafiche, poi sottotitoli e CTA.`,
    `In CapCut: importa 00_video.mp4 sulla traccia principale; ogni altro file va su una traccia sovrapposta (Overlay), all'INIZIO indicato qui sotto,`,
    `a schermo intero (1080×1920, senza ridimensionare: la posizione è già quella giusta). Le .mov hanno lo sfondo trasparente: si possono spostare,`,
    `accorciare, ingrandire o cancellare una per una. I sottotitoli ci sono due volte: 80_sottotitoli.mov (stile del brand) oppure sottotitoli.srt`,
    `(Testo › Sottotitoli › Importa file: testo modificabile). Usane solo uno.`,
    ``,
    `INIZIO     DURATA   FILE`,
    ...rows.map((row) => `${tc(row.a).padStart(8)}  ${((row.b - row.a + 1) / FPS).toFixed(2).padStart(6)} s  ${row.file}\n                    ${row.what}`),
  ];
  if (p.zooms?.length) lines.push("", "Movimenti di camera già dentro il video pulito (avvicinamenti lenti): " + p.zooms.map((z) => `${tc(introF + z.at * FPS)} per ${z.dur} s`).join(", ") + ".");
  writeFileSync(`${dir}/MONTAGGIO.txt`, lines.join("\n") + "\n");
  if (existsSync(`out/${Y}/consegna/${id}_didascalia.txt`)) writeFileSync(`${dir}/didascalia.txt`, readFileSync(`out/${Y}/consegna/${id}_didascalia.txt`));
  console.log(`${id}: ${rows.length} livelli → ${dir}`);
}
