---
name: project-cta-con-guida
description: "Alcuni reel chiudono con «commenta e ti mando la guida» invece del coaching: variante della CTA, guide ancora da preparare"
metadata:
  node_type: memory
  type: project
  modified: 2026-11-22
---

Ross, 21/11/2026 (serie G, YTCN 26): «dimmi se a qualcuno di questi possiamo attaccare una guida, cioè devono commentare per avere una guida
di approfondimento… la CTA deve essere adeguata, cioè scarica la guida».

**Why:** una guida da scaricare è una leva di contatto più leggera del coaching: chi commenta lascia il contatto in cambio di qualcosa di
pratico (interpretazione mia). Ha senso sui reel «da salvare» (pratici, a elenco, a esercizi), non su tutti.

**How to apply:**
- Nel motore: `cta: { word, title, sub: "Scarica gratis la guida", offer: [righe del titolo della guida], dm: "Ti mando la guida" }`
  (`CTA.tsx`); la didascalia chiude con «Commenta PAROLA e ti mando gratis la guida «…»» e NON nomina il coaching.
- Serie G, proposta mia montata il 21/11 (Ross non ha ancora confermato quali): STRATI → «Come vestirsi per correre al freddo» (G2);
  CIRCUITO → «Riscaldamento in casa in 5 minuti» (G4, G5, G6, G7, G8). Gli altri sei restano sul coaching.
- Le guide NON esistono ancora: vanno scritte (solo con le parole e i numeri di Daniele) prima di pubblicare quei reel. Se Ross cambia
  idea su un reel, tornare alla CTA del coaching è un solo render.
- Nelle schede la riga diventa «CTA PAROLA (guida «titolo»)».

**22/11/2026:** la guida del circuito esiste: «Come scaldarsi quando fa freddo», 17 pagine verticali (1080×1350), tutto YTCN 26 per
iscritto con i fotogrammi del video (Ross: «devi riportare tutte le info del video originale… dobbiamo dare qualcosa in più rispetto a
ciò che c'è nel reel»). Sorgente `video-engine/work/ytcn26/guida/build.py` (+ `export.js` per PDF e controllo dell'impaginazione), PDF in
`video-editing/consegne/ytcn26/`. È la guida del reel G13 (quattro fasce orizzontali, banner «Scarica la guida gratuita · Commenta
CIRCUITO»). Nei reel G4-G8 la CTA nomina ancora «Riscaldamento in casa in 5 minuti»: se Ross conferma che portano a questa guida, va
aggiornato il titolo nella CTA e nelle didascalie (un render per reel). Regola per le guide: solo parole e numeri del video, nessun
consiglio tecnico aggiunto; immagini = fotogrammi dell'originale.

**24/11/2026:** Ross: «tutte le CTA hanno parole troppo diverse, mettine una tipo freddo uguale per tutte». Nella serie G la parola è
FREDDO per tutti i reel (coaching e guida). La guida scritta è una sola, «Come scaldarsi quando fa freddo» (17 pagine, copre anche
strati, mani e testa, respiro e squat): G2, G4 e G13 rimandano a quella. Nei reel dei singoli esercizi (G5-G8) Ross non vuole CTA.
G4 ha in più un banner fisso per tutto il reel («Commenta FREDDO · ricevi il circuito completo»).
