# Testimonianze Studio — Correre Naturale®

Ogni giorno consegna un contenuto pronto (un set di stories o un carosello) costruito sulle testimonianze degli allievi. Solo caroselli e stories, mai reel.

```
scarica il foglio → sceglie le testimonianze → Claude scrive → controlli automatici → grafiche → consegna + notifica
```

## Cosa trovi ogni giorno
`Consegne/AAAA-MM-GG/`
- `carosello-01.png …` oppure `storia-01.png …` — le grafiche (1080×1350 o 1080×1920)
- `carosello.pptx` / `stories.pptx` — la versione modificabile, da aprire in Canva (testi, forme e foto sono elementi separati)
- `caption.txt` — caption pronta; sotto la riga di trattini c'è la CTA
- `scheda.md` — testimonianze usate (ID e nome), stato del consenso, perché sono state scelte, struttura problema → risultato, cose da fare prima di pubblicare
- `ERRORE.txt` — solo se qualcosa è andato storto (foglio non scaricato, nessuna testimonianza valida, scrittura bocciata dai controlli)

## Installazione sul PC (una volta)
1. Copia questa cartella in `Documenti\Testimonianze Studio`.
2. Crea il service account seguendo `GUIDA-SERVICE-ACCOUNT.md` e metti la chiave in `dati\service-account.json`.
3. Tasto destro su `installa.ps1` → «Esegui con PowerShell» (crea l'ambiente Python e le anteprime dei modelli).
4. Prova a mano: `.\.venv\Scripts\python.exe esegui.py`
5. Quando i modelli sono approvati: `attiva.ps1` (ogni giorno alle 10:00; se il PC è spento parte alla prima accensione). Per spegnere: `disattiva.ps1`.

Claude Code deve essere installato e avere fatto l'accesso con l'abbonamento (`claude` una volta nel terminale). Il programma non usa chiavi API: se sul PC esiste `ANTHROPIC_API_KEY`, la toglie dall'ambiente del comando.

## Comandi
```
python esegui.py                      contenuto di oggi
python esegui.py --data 2026-11-26    contenuto di un altro giorno (prova)
python esegui.py --senza-scarico      usa il testimonianze.csv già scaricato
python esegui.py --anteprime          rigenera le anteprime dei modelli (testi di esempio)
python -m unittest discover prove     prove delle regole
```
Rifare lo stesso giorno sostituisce la consegna e non «consuma» altre testimonianze.

## Regole applicate dal codice (non lasciate a Claude)
- Solo righe con Stato «Catalogato»; mai le righe con «Minorenne» nel Consenso; mai Consenso «No»; mai uso «Interno».
- Preferenza a Forza 4–5; si scende a Forza 3 solo se la leva del giorno è a corto.
- Nessun riuso prima di 90 giorni: vale il registro locale `dati/registro_utilizzi.csv` e anche la colonna «Ultimo utilizzo» del foglio.
- Consenso non confermato («Sì» assente): solo nome di battesimo e avviso in cima a `scheda.md`.
- «Da oscurare» compilato: nessun nome nel contenuto, e gli screenshot originali non si usano mai.
- Prima di arrivare a Claude il testo viene ripulito da cognomi, email, telefoni, link, menzioni.
- Citazioni: ogni citazione deve essere fatta solo di parole dell'originale, nello stesso ordine (si può tagliare, non riscrivere). Se non lo è, la risposta viene scartata.
- Salute: niente «guarisce», «cura», «risolve», «garantisce» in nessun punto; sui temi di salute niente frasi che suonano come promessa.
- Storytelling: problema → difficoltà → soluzione → risultato → CTA; il primo elemento non contiene inviti all'azione; stories max 6; caroselli 6–9 slide; parola chiave CORRO, PIANO, GUIDA o SCUOLA.
- Se la scrittura non supera i controlli si riprova (fino a 3 volte), poi `ERRORE.txt`.

## Calendario e configurazione (`config.json`)
- `calendario`: formato e leva/taglio di ogni giorno.
- `leve`: il foglio non ha una colonna con le leve; qui è scritto da quali colonne si ricava ogni leva.
- `stagioni`: i valori di «Stagione / aggancio» e il periodo in cui hanno la precedenza.
- `eventi.elenco`: gare con una data precisa; nei 21 giorni prima hanno la precedenza assoluta.
- `ora_esecuzione`, `selezione` (soglie), `cta`, `grafica.usa_foto`.

## Modelli grafici
| Carosello | Stories |
|---|---|
| `C-virgolette` Virgolette | `S-messaggio` Messaggio |
| `C-primadopo` Prima / Dopo | `S-virgolette` Virgolette |
| `C-percorso` Il percorso | `S-tappe` Tappe |
| `C-voci` Voci a confronto (solo storia unita) | `S-voci` Voci a confronto (solo storia unita) |

Rotazione: mai lo stesso modello dell'ultima uscita di quel formato, mai la stessa famiglia grafica del giorno prima.
Foto: solo quelle in `assets/foto`, sempre in una zona separata dal testo (il testo non sta mai sopra una foto).
Le anteprime in `anteprime/` usano testi di esempio inventati: servono solo a vedere l'impaginazione.

## Dove sta cosa
- `esegui.py` — il flusso; `ts/dati.py` foglio e pulizia; `ts/selezione.py` regole, punteggio, registro, rotazione; `ts/scrittura.py` istruzioni per Claude; `ts/controlli.py` controlli; `ts/grafica.py` motore PNG + PPTX; `ts/modelli.py` gli 8 modelli; `ts/consegna.py` file di consegna e notifica.
- `dati/` (mai su GitHub): `testimonianze.csv`, `service-account.json`, `registro_utilizzi.csv`, `log.txt`.

## Serie «problemi» (`serie.py`)
Fuori dal calendario quotidiano: trova i problemi più ricorrenti nelle testimonianze e crea, per ognuno, un carosello e un set di stories con **il problema nel titolo di copertina** e le **schermate dei messaggi** (modelli `C-schermo` / `S-schermo`).
```
python serie.py analisi                                   raggruppa i problemi (dati/problemi.json)
python serie.py genera --quanti 12 --salta periodo-buio   contenuti in Serie-problemi/NN-problema/
python serie.py genera --solo 3                           rifà solo il problema n. 3
python serie.py ridisegna                                 rifà solo le grafiche dopo un ritocco ai modelli
```
- Valgono le stesse regole del flusso quotidiano; in più la copertina non può contenere nomi, numeri o risultati e deve avere una citazione breve.
- Ogni testimonianza entra in un solo contenuto e viene scritta nel registro: per 90 giorni il flusso quotidiano non la riusa.
- I problemi che riguardano malattie sono esclusi dalla serie (restano utilizzabili solo come esperienza personale).
- Le schermate riportano le parole esatte dell'allievo ma sono ricomposte in stile brand: non sono gli screenshot originali.

## In prova: schermata originale e vocale (non ancora nel flusso quotidiano)
- `ts/schermate.py` + modelli `C-schermata` / `S-schermata`: la prima slide mostra lo screenshot vero del messaggio. Prima di usarlo, nomi, numeri, email e foto profilo vengono cercati (Claude Code legge l'immagine) e coperti con rettangoli «bruciati» nei pixel. La copertura va sempre ricontrollata a occhio.
- `ts/vocale.py`: slide video (MP4) con l'audio originale, l'onda che avanza e le parole a tempo. Servono ffmpeg e `pip install -r requirements-audio.txt`. Le parole trascritte si correggono nel file `.parole.json` accanto al video.
- Per entrare nel flusso servono: accesso alla cartella Drive degli allegati (service account come Visualizzatore, «Google Drive API» abilitata) e la decisione sul consenso per voce e schermate.
