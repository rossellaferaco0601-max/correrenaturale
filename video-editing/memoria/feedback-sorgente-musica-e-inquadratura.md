---
name: feedback-sorgente-musica-e-inquadratura
description: "Prima di montare da un sorgente: togliere la musica che ha dentro e controllare che il ritaglio verticale tenga Daniele al centro"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-24
---

Ross, 24/11/2026 (serie G, 13 reel): «IMPORTANTE: togli la musica da tutti i video»; «l'inquadratura di Daniele è tagliata e non capisco
perché, la spalla a sinistra è tagliata»; su G4 «Daniele viene tagliato e addirittura anche il volto finisce fuori inquadratura»; su G9
«ha degli scatti» e «le inquadrature frontali sono tagliate».

**Why:** due errori miei a monte, ripetuti su tutta la serie. 1) Il sorgente («YTCN26 NO SCRITTE») aveva una musica bassa dentro
l'audio e non l'avevo tolta, anche se dal 14/11 la regola è che nei reel non si consegna musica. 2) Nella mappa delle inquadrature la
posizione del volto era il centro ma veniva letta come bordo sinistro: ogni ritaglio era spostato di mezzo volto, Daniele stava a
sinistra e nei primi piani di tre quarti usciva dal bordo; a ogni stacco il salto di posizione dava l'effetto «scatti».

**How to apply:**
- Su ogni sorgente nuovo: misurare il livello delle pause (se non scende sotto circa −50 dB c'è musica o rumore) e togliere la musica
  UNA volta dal sorgente (`python3 scripts/g_voce_src.py sorgente.mp4`), così tutti i master nascono senza.
- Dopo ogni master: `python3 scripts/g_sheets.py inquadrature master.mp4 out.jpg` e si GUARDA il foglio: volto al centro in ogni
  inquadratura, spalle tagliate in modo uguale ai due lati, mai il viso contro il bordo. Non basta il controllo del mento.
- Parola da commentare: una sola per tutta la serie (qui FREDDO), non una per reel («tutte le CTA hanno parole troppo diverse»).
