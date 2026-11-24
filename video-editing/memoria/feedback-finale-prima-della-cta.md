---
name: feedback-finale-prima-della-cta
description: "Prima della CTA non si deve mai vedere la mossa/inquadratura successiva di Daniele, né un fermo immagine, né uno stacco netto; l'ultima grafica esce prima"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-24
---

Ross, 17 e 18/11/2026 (serie F, YTCN 22). Prima su F1 («quello stacco strano prima della CTA, devi renderlo più fluido»), poi su F4
(«prima della CTA c'è un taglio strano, non si deve vedere la mossa successiva di Daniele, è una cosa che ti ho detto mille volte, c'è
sempre lo stesso errore») e su F7 e F11 («c'è uno stacco troppo netto prima della CTA»).

**Why:** il finale è il punto in cui chi guarda decide se leggere la CTA: un salto di posa, un fotogramma bloccato o una grafica coperta
a metà sembrano errori di montaggio. È la correzione che Ross ripete più spesso insieme al volto libero. (Interpretazione mia: «mossa
successiva» = l'inquadratura o la posa che nel video di partenza viene dopo l'ultima frase del reel, anche quando lo stacco dell'originale
cade a metà dell'ultima parola.)

**How to apply:**
- Negli ultimi ~2,5 s non deve restare uno stacco del video di partenza. Se l'ultima frase finisce dopo uno stacco dell'originale, quel
  pezzo NON si mostra: lo si copre con una grafica a tutto schermo che resta finché la CTA la copre (F4: il conto intero), oppure
  si chiude prima. La dissolvenza verso la posa successiva non basta (F4 v1 bocciato).
- Niente fermo immagine: coda che continua a muoversi (`ping` in `cn_master_shots.py`) e CTA che parte ~0,3 s dopo l'ultima parola
  (`tailSeconds 0.8`, `tailHold 0.3`).
- L'ultima grafica deve essere uscita prima che la CTA cominci a salire (F11: la frase barrata veniva coperta a metà).
- Controllo prima di consegnare: fotogrammi degli ultimi 2,5 s di OGNI reel, uno ogni 3, più la differenza tra fotogrammi della coda
  (una fila di zeri = fermo immagine).

**21/11/2026 (G2 v1, serie G):** Ross: «c'è sempre quello stacco brutto prima della CTA, prova a risolvere». Guardando il file fotogramma
per fotogramma c'era UN SOLO fotogramma dell'inquadratura successiva (un lampo a 56,30 s) proprio prima della coda: quando il pezzo
finisce a meno di un fotogramma dallo stacco successivo del sorgente, ffmpeg (`fps=30:round=down`) metteva nell'ultimo fotogramma il primo
dell'inquadratura dopo. Corretto alla radice in `scripts/cn_master_shots.py` (il limite vale anche per l'ultimo pezzo).
- Controllo obbligatorio su master e file finale di OGNI reel: `python3 scripts/f_flash.py file.mp4` (un fotogramma diverso da quello
  prima e da quello dopo = lampo). È dentro `scripts/f_all.sh`. I 15 reel della serie F, ricontrollati, erano puliti.
- Prima di dire «il finale è a posto» guardare TUTTI i fotogrammi dell'ultimo secondo e mezzo, non uno ogni 3.

**24/11/2026 (serie G, revisione di tutti i reel):** Ross su G2: «proprio prima della CTA c'è un parlato muto di Daniele, si vede che parla
ma non c'è suono»; su G4: «poco prima della CTA c'è un taglio orribile»; su G9: «lo stacco prima della CTA è troppo netto»; «controlla
sempre lo stacco prima della CTA». La coda `ping` (andata e ritorno) faceva scorrere all'indietro l'ultima frase per quasi un secondo:
la bocca si muove senza audio. Quindi anche l'andata e ritorno è bocciata, come il fermo immagine e la coda dal vivo.
- **Regola attuale: dopo l'ultima parola non resta nessun video.** La CTA comincia a salire 0,4 s PRIMA della fine del parlato e finisce
  di coprire sull'ultima sillaba, che si sente sopra il pannello (`ctaLead 0.4`, salita morbida di 12 fotogrammi, `tailSeconds 0.1`,
  `tailLive 0`). L'ultima grafica esce prima che il pannello parta.
- Controllo: `python3 scripts/g_sheets.py finale file.mp4 out.jpg` (tutti i fotogrammi dell'ultimo secondo e mezzo) su OGNI reel.
