---
name: feedback-spazio-sottotitoli-grafiche
description: "In tutti i reel più spazio tra sottotitoli e animazioni (~100 px), scritte dentro le caselle, zone sicure di Instagram rispettate"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-22
---

Ross, 18/11/2026: «memorizza questo: in tutti i reel deve esserci più spazio tra i sottotitoli e le animazioni, te lo avevo già detto,
e vanno rispettati i layout di Instagram». Stesso giorno, su F14: «le scritte escono dalle box». Era già stato detto il 6/11 (glass box
più distanti dai sottotitoli) e il 12/11 (le grafiche non toccano mai i sottotitoli).

**Why:** con 40 px di aria grafica e sottotitolo si leggono come due testi impilati; e ciò che finisce sotto i 1500 px o nella colonna
dei comandi a destra viene coperto dall'interfaccia di Instagram.

**How to apply:** almeno ~100 px tra il bordo basso di ogni grafica e la scatola dei sottotitoli; sottotitoli con il bordo basso sopra i
1500 px; grafiche dentro x < 0,90. Nel motore CN: `capShift 40`, `gfxScale 0.96` e un `dy` per ogni grafica calcolato con
`npx tsx scripts/f_place.ts ID` (mette la grafica più in alto quando il mento lo permette; ✗ se l'aria è sotto i 90 px: accorciare la
grafica, non avvicinarla). Nelle caselle il corpo del testo si calcola sulla riga più lunga (mai testo che sborda): controllarlo sui
fotogrammi a grandezza reale. Dove il volto è grande e non c'è posto: una sola scritta in basso, sottotitoli spenti per quel tratto.

**21/11/2026 (G2, serie G):** «le animazioni sono perfette, forse le farei solo leggermente più grandi, ma sempre rispettando le regole
degli spazi». Le rappresentazioni disegnate (pannello con illustrazione + frase) piacciono: tenerle GRANDI. Come: `gfxScale 0.98` (bordo
destro a 971 px), pannelli alti 336-350 px alzati con `dy` fin dove il mento lo permette (aria sempre ~100 px), il disegno ingrandito
dentro il pannello (`ART_FIT` in `Elements10.tsx`). Le miniature dei fogli di controllo ingannano: giudicare la grandezza su un fotogramma
intero (`npx remotion still ID out.png --frame=N`).

**22/11/2026 (G13, reel a fasce):** due bocciature di fila perché lasciavo una zona verde piena sotto il banner («i video devono prendere
tutto lo schermo anche in verticale»). Le zone sicure di Instagram valgono per scritte e banner, NON per il video: il video riempie sempre
tutto il fotogramma, la grafica gli sta sopra dove c'è spazio libero nell'inquadratura. Mai fondi pieni per «fare posto» alla grafica.
