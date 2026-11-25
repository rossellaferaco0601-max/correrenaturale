---
name: feedback-consegna-a-livelli
description: "Da 25/11 ogni reel si consegna anche a livelli editabili per CapCut: video pulito + ogni grafica su fondo trasparente + SRT + foglio dei tempi"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-25
---

Ross, 25/11/2026: «Video pulito + livello grafiche separato su fondo trasparente. Da oggi in poi puoi restituirmi i reel così? Così non
spreco credito di utilizzo per cose che posso cambiare a mano, ogni cosa deve essere editabile. E alla fine decido io se va bene oppure se
portarlo in CapCut».

**Why:** le correzioni piccole (testi, tempi, posizioni) costano un giro di render e credito; Ross preferisce farle a mano in CapCut.

**How to apply:** a ogni consegna, oltre al reel finito, la cartella `out/<serie>/livelli/<ID>/` fatta con `npx tsx scripts/cn_layers.ts ID`
e `lista.sh` (video pulito H.264 con audio, una .mov ProRes 4444 trasparente per ogni grafica, sottotitoli .mov + .srt, CTA, MONTAGGIO.txt
con gli inizi). Quando Ross chiede una correzione piccola, ricordarle che può farla nel livello; rifare render solo per ciò che non si fa a
mano. Primo test su G3 (25/11): da confermare che CapCut (computer) legga la trasparenza delle .mov ProRes 4444.
