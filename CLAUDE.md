# Correre Naturale® — reel e video

Repository dedicata solo a Correre Naturale® (Daniele Vecchioni, @correrenaturale). ValeFitCoach e Ciak Studio hanno repository proprie (`valefitcoach`, `ciakstudioAI`): non mescolarli.

| Cartella | Contenuto | Leggi prima |
|---|---|---|
| `video-editing/` | Regole, contesto, brand, guide, consegne, memoria | `LEGGIMI.md`, skill `cliente-correre-naturale`, `REGOLE-MONTAGGIO.md`, `CONTESTO.md` |
| `video-engine/` | Motore grafico (Remotion) | `video-engine/README.md` |

# Motore grafico video/reel (`video-engine/`)

Claude è usato come motore grafico per montare video e reel. Il progetto Remotion vive in `video-engine/` (motore `CNReel` in `src/cn`, motore ReelStudio `RSReel` in `src/rs`); le composizioni specifiche di un cliente stanno in `video-engine/src/<cliente>/` (es. `src/cn/` per Correre Naturale) e i file di lavoro in `video-engine/work/`.

## Strumenti
- Node 22 / npm / TypeScript, Python 3.13, FFmpeg 6, Git, Blender 4 (headless, Cycles CPU).
- Remotion 4 (+ transitions, captions, lottie, three, shapes, paths, noise, motion-blur, media-utils, gif), React 19, Three.js + react-three/fiber/drei, GSAP, lottie-web, SDK ElevenLabs.
- Whisper: `faster-whisper` (Python) via `video-engine/scripts/transcribe.py`.
- Chromium di sistema per il render: `/opt/pw-browsers/chromium` (impostato in `video-engine/remotion.config.ts`, override con `REMOTION_BROWSER`).

## Skill disponibili (`.claude/skills/`)
- Remotion ufficiali: `remotion-best-practices`, `remotion-create`, `remotion-markup`, `remotion-render`, `remotion-studio`, `remotion-captions`, `remotion-multimedia`, `remotion-interactivity`, `remotion-maps`, `remotion-saas`, `remotion-docs`, `remotion-upgrade`, `remotion-license`.
- Personalizzate: `kinetic-typography`, `motion-graphics`, `cinematic-animation`, `video-editing`, `compositing`, `audio-sync`, `subtitle-animation`, `broll-editing`, `web-animation-stack`, `cliente-correre-naturale`.
- `effects` (Vibha, 51 effetti con tracciamento del volto, Python/mediapipe): venv già pronto in `.claude/skills/effects/.venv` (font sostituiti con Blinker). Nel motore CN si usano via `props.fx` + `scripts/cn_fx.ts`; quali effetti vanno bene e quali no è scritto in `video-editing/REGOLE-MONTAGGIO.md` (8/11). Le regole del cliente vincono sugli effetti (niente emoji, volto libero).
- Dal PC di Ross (8/11), 34 skill generiche di montaggio e motion: editing reel (`reels-editor`, `video-edit`, `talking-head-editing-skill`, `claude-video-reel-editor`, `edit-video`, `ffmpeg-skill`, `beat-sync-editing`), motion graphics (`motion-doctrine`, `motion-graphics`, `motion-art-direction`, `motion-background`, `motion-broll`, `logo-animation`, `animation-principles`, `color-motion`, `shot-composition`, `cut-the-curve`, `cinematic-camera`, `article-highlights`, `sound-effects`, `media-use`, `style-motion`, `style-sampling`), Remotion extra (`remotion-motion-graphics`, `remotion-overlays`, `remotion-video`), HyperFrames (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `remotion-to-hyperframes`, `reverse-any-video`, `captions-overlay`, `seam-craft`), `after-effects`. Le regole del cliente (`video-editing/`) vincono sempre su queste skill.
- HyperFrames (`npm hyperframes` in `video-engine`): render HTML→video alternativo a Remotion per grafiche da pagina web.

## Comandi
```bash
cd video-engine
npm run dev                                   # Remotion Studio (preview)
npx remotion render R1-fiatone out/a.mp4      # render di un reel CN
npx remotion still R1-fiatone out/f.png --frame=75
scripts/cn_finish.sh R1-fiatone v7            # render + loudness + copertina + didascalia + ritrascrizione
scripts/cn_queue.sh v7 R2-naso R3-bocca       # coda: master (se manca) → effetti skill (cn_fx) → finitura, un reel alla volta
npx tsx scripts/cn_fx.ts R1-fiatone --still   # fotogrammi di controllo degli effetti della skill `effects` sul master
python3 scripts/cn_align.py public/x/src.mp4 src/cn/words.json src/cn/words.json   # tempi reali di ogni parola (allineamento fonetico): da fare prima di agganciare grafiche e tagli
python3 scripts/cn_master_shots.py work/L3.json    # master verticale da un video GIÀ montato (longevità): un ritaglio per inquadratura, riprese di copertura, schede da coprire
npx tsx scripts/validate-reels.ts             # sovrapposizioni e ancore di hook/elementi/effetti
npx tsx scripts/cn_stills.ts C1-runner C2-namibia@12.5,30   # fogli di controllo PRIMA del render: un fotogramma per ogni grafica (ID@secondi = solo quei momenti)
npx tsx scripts/cn_covers.ts R1-fiatone       # copertina nel formato unico (fotogramma `cover.frame`; candidati con scripts/cn_smile.py), file con lo stesso nome del reel
python3 scripts/cn_voce.py L5-bugia v3 v4      # solo la voce: toglie la musica di sottofondo che sta dentro il sorgente (Oscar 14/11: la musica la mettono loro su Edits)
../.claude/skills/effects/.venv/bin/python scripts/cn_master_lock.py work/daniela.json vecchio_master.mp4   # riprese a mano: inquadratura agganciata al volto e stacchi netti (niente dissolvenze in movimento)
python3 scripts/cn_cta_music.py L5-bugia v2 v3  # musica anche sotto la CTA quando la musica è dentro il sorgente (toglie la voce dal seguito con scripts/cn_music_stem.py, modello ONNX in work/models/uvr)
python3 scripts/cn_long_words.py work/x_long.json work/c3502.wav out/x_new.json   # versione lunga: ritrascrizione pezzo per pezzo (da LEGGERE prima del master: voci fuori campo); poi scripts/cn_words_merge.py per i sottotitoli
SUB_BOX="&H38000000" python3 scripts/cn_stories.py work/storie_t/tagli.json out/testimonianze/stories   # spezzoni per le stories (solo sottotitoli); parole nel tempo del master: npx tsx scripts/cn_words_master.ts ID
python3 scripts/cn_facecheck_elements.py R2-naso public/ytcn51/masters/R2-naso_mento.json   # volto libero grafica per grafica (dopo cn_facecheck.py)
../.claude/skills/effects/.venv/bin/python scripts/cn_facecheck.py public/x/master.mp4 0.44   # il volto non si copre MAI: mento sotto il bordo grafiche
scripts/rs_render.sh progetto.json ytcn51/ytcn51_src.mp4 out/x.mp4   # render di un project.json ReelStudio
python3 scripts/transcribe.py public/clip.mp4 --lang it --out src/captions/clip.json
scripts/ffmpeg-presets.sh                     # elenco preset FFmpeg
blender -b -P scripts/blender_render.py -- "TITOLO" out/title.png
python3 scripts/gemini.py models|testo|analizza|immagine|video   # Gemini (chiave: secret di rete dell'ambiente)
npx tsx scripts/f_cfg.ts F1-normale && python3 scripts/cn_master_shots.py work/ytcn22/F1-normale.json   # serie F (YTCN 22, sorgente Full HD a tre camere): master per inquadratura; poi python3 scripts/f_cutcheck.py master.mp4
python3 scripts/f_match.py F1-normale 199.2   # stacco fluido prima della CTA: avvicinamento lento + dissolvenza breve verso l'inquadratura che inizia a quel tempo del sorgente
npx tsx scripts/f_map.ts F2-ciclista          # mappa di lavoro: inquadrature, mento e parole (dove si possono mettere le grafiche); npx tsx scripts/f_facecheck.ts = volto libero su grafiche e sottotitoli
scripts/f_queue.sh F2-ciclista:v1 F3-fastidi:v1   # coda render della serie F; finitura con OUT=out/ytcn22 WK=work/ytcn22 WMODEL=large-v3-turbo scripts/cn_finish.sh ID v1
scripts/f_queue.sh G2-strati:v1                  # serie G (YTCN 26, «Correre al freddo»): stessi script della serie F (scripts/f_series.ts), cartelle ytcn26; finitura con OUT=out/ytcn26 WK=work/ytcn26
npx tsx work/ytcn26/gem_preview.tsx GemLayers out/chk/gem '{"stage":2,"cue":0.4,"fx":[1.4,2.6]}' 0.3,1,2   # pagine di controllo di un'illustrazione scritta da Gemini (src/cn/gem)
python3 scripts/g13_bands.py && npx remotion render G13-quattro out/ytcn26/G13_raw.mp4   # reel «a fasce» (quattro esercizi + fascia banner, 30 s, muto); guida in PDF: python3 work/ytcn26/guida/build.py && node work/ytcn26/guida/export.js out/ytcn26/guida
```

## Clienti
Contesto e regole di montaggio stanno in `video-editing/`. Per Correre Naturale usa la skill `cliente-correre-naturale` prima di qualsiasi montaggio. Ogni nuova regola di montaggio va in `video-editing/REGOLE-MONTAGGIO.md`.

## Regole
- Le sorgenti (video/audio/immagini) vanno in `video-engine/public/` e si caricano con `staticFile()`.
- Ogni animazione è funzione pura di `useCurrentFrame()`; niente timer o CSS transition nel render.
- Controlla uno still prima di un render completo. Output in `video-engine/out/` (ignorato da git).
- Le chiavi API (ElevenLabs, Runway) vanno nei secret dell'ambiente, mai nel repo.

`video-engine/reelstudio/` contiene il codice e i progetti di ReelStudio (la dashboard sul PC di Ross); nel cloud gira come composizione `RSReel` (asset in `video-engine/public/rs/`). Schema project.json e catalogo effetti: `video-engine/reelstudio/CLAUDE.md`. Mai committare `impostazioni.json` (chiavi API).

Connettori Claude attivi sull'account: Canva, Fathom, Google Calendar, Google Drive, Google Sheets, Windsor.ai.
