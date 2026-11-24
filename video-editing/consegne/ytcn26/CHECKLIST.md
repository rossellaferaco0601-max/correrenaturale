# Checklist di consegna · YTCN 26, serie G (revisione del 24/11/2026)

File in `video-engine/out/ytcn26/consegna/`: per ogni reel `ID_vN.mp4` (1080×1920, 30 fps), `ID_copertina.jpg` (copertina nel formato unico), `ID_didascalia.txt`, `ID_vN_anteprima.mp4`. Tutti senza musica di sottofondo (tolta dal sorgente), con Daniele al centro dell'inquadratura e, nei reel con CTA, il pannello che sale sull'ultima parola.

| Reel | Durata totale | Rappresentazioni ed effetti | Parola da commentare |
|---|---|---|---|
| G1-brivido v2 | 59,2 s | titolo a colpo, schianto su «attenzione», corridore 3D con gli strati che si accumulano fino al surriscaldamento, gelo sui bordi, corridore infreddolito → in corsa → caldo, scheda finale «da ricordare» | FREDDO |
| G2-strati v3 | 64,5 s | titolo che si condensa, i tre capi che si indossano uno sull'altro, cartellino che dondola, raffica di vento, anelli della sinergia, sudore contro gelo | FREDDO (guida) |
| G3-mani v2 | 29,7 s | titolo spinto dal vento, corridore 3D che perde calore da mani e testa, poi guanti e fascia, poi cappello; gelo sui bordi | FREDDO |
| G4-casa v3 | 50,0 s | banner fisso «Commenta FREDDO e ricevi il circuito completo», schianto su «un buon riscaldamento», frase barrata, parole che tremano dal freddo con il gelo sui bordi, corridore 3D che fa i jumping jack in casa, calore | FREDDO (guida) |
| G5-climber v2 | 29,7 s | video a finestra con i bordi sfumati, intestazione dell'esercizio, zone del corpo che si accendono, anelli delle durate | senza CTA |
| G6-ponte v3 | 44,8 s | parte da «il ponte per i glutei»; video a finestra, estensione delle anche, seduto/appena sveglio, modalità e durate | senza CTA |
| G7-affondi v3 | 51,0 s | video a finestra, affondi coordinati, temperatura che sale, tempo massimo, scheda finale «Lo scopo? Solo scaldarsi» | senza CTA |
| G8-jack v3 | 34,1 s | video a finestra, jumping jack, tendini, giacca, guanti e fascia | senza CTA |
| G9-graduale v2 | 69,7 s | apertura a tutto schermo «Quando corriamo al freddo…», corridore 3D al passo con l'intensità bassa, poi in corsa leggera con la batteria piena, riepilogo con le spunte | FREDDO |
| G10-naso v2 | 60,1 s | titolo che si condensa, pillole e parole grandi, testa 3D di profilo con l'aria che entra (gelida dalla bocca; dal naso si scalda, si umidifica, viene filtrata), gelo sui bordi | FREDDO |
| G11-respiro v2 | 51,5 s | corridore 3D in corsa leggera con l'onda del respiro (regolare verde, affanno rossa), parole che entrano dai lati | FREDDO |
| G12-squat v2 | 51,9 s | titolo a colpo, corridore 3D che scende nello squat naturale profondo e ci resta, parole grandi sui pochi minuti | FREDDO |
| G13-quattro v5 | 30,0 s | reel a fasce muto (non toccato nella revisione: «G13 va bene, lascialo stare») | CIRCUITO (guida) |

Controlli fatti su ogni reel prima della consegna:
- master: stacchi al fotogramma giusto (`f_cutcheck.py`), nessun lampo di un fotogramma (`f_flash.py`), volto libero su grafiche e sottotitoli (`f_facecheck.ts`, reel nel bosco);
- grafiche: nessuna sovrapposizione e tempi di lettura (`validate-reels.ts`), ~100 px di aria sopra i sottotitoli (`f_place.ts`), fogli di controllo guardati (`cn_stills.ts`);
- file finale: loudness intorno a -14 LUFS, nessun fotogramma nero, nessun lampo, ritrascrizione uguale al parlato, ultimo secondo e mezzo guardato fotogramma per fotogramma;
- finali: la CTA sale 0,4 s prima della fine del parlato e copre sull'ultima sillaba (foglio `g_sheets.py finale` guardato per ogni reel); G1 e G7 chiudono con la scheda «da ricordare» perché il sorgente cambia inquadratura negli ultimi secondi; G11 e G12 hanno l'ultimo stacco reso morbido (`f_match.py`);
- inquadrature: foglio `g_sheets.py inquadrature` guardato per ogni master (volto al centro), pause dell'audio a circa −50 dB (niente musica).

Da sapere prima di pubblicare: la guida è una sola, «Come scaldarsi quando fa freddo» (in questa cartella); con la parola unica FREDDO i reel G2 e G4 promettono la guida e gli altri le info sul coaching: l'automazione dei messaggi deve tenerne conto (oppure si decide che FREDDO manda sempre la guida).
