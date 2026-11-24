# Guida: il «lettore» del foglio (service account Google)

Serve una volta sola, circa 10 minuti. Un service account è un utente-robot di Google con una sua email: tu condividi il foglio con quella email come **Visualizzatore** e il programma legge il foglio a nome suo. Il foglio resta privato: niente link «chiunque abbia il link».

1. Apri https://console.cloud.google.com ed entra con il tuo account Google. Accetta i termini se li chiede.
2. In alto clicca il selettore dei progetti → **Nuovo progetto** → nome `Testimonianze Studio` → **Crea**. Poi selezionalo.
3. Nella barra di ricerca in alto scrivi `Google Sheets API`, aprila e clicca **Abilita**. È l'unico servizio che serve.
4. Menu ☰ → **IAM e amministrazione** → **Account di servizio** → **Crea account di servizio**. Nome: `lettore-testimonianze`. Clicca **Crea e continua**, poi **Fine** senza assegnare ruoli: non gli serve nessun permesso sul progetto.
5. Nell'elenco compare una email tipo `lettore-testimonianze@…iam.gserviceaccount.com`. **Copiala.**
6. Clicca su quell'account → scheda **Chiavi** → **Aggiungi chiave** → **Crea nuova chiave** → **JSON** → **Crea**. Si scarica un file `.json`: è la «password» del robot. Non mandarlo a nessuno, non incollarlo in chat, non caricarlo su GitHub.
7. Apri il foglio «Archivio Testimonianze – Correre Naturale» → **Condividi** → incolla l'email del punto 5 → ruolo **Visualizzatore** → togli la spunta «Invia notifica» → **Condividi**. «Accesso generale» resta su **Con restrizioni**.
8. Rinomina il file scaricato in `service-account.json` e mettilo in `Documenti\Testimonianze Studio\dati\`.

## Se qualcosa non va
- **Al punto 7 Google rifiuta la condivisione**: il foglio appartiene a un'organizzazione che blocca gli utenti esterni. Serve che il proprietario del foglio (o l'amministratore) autorizzi quella email.
- **Al punto 6 la creazione della chiave è bloccata**: succede con gli account aziendali. Usa un account Google personale per i punti 1–6.
- **ERRORE.txt dice «Il service account non può leggere il foglio»**: controlla i punti 3 e 7.

## Cosa può fare il robot
Solo leggere quel foglio. Il programma chiede a Google il permesso `spreadsheets.readonly`: non può modificare il foglio né vedere altri file del tuo Drive. Per togliergli l'accesso basta rimuovere la sua email da «Condividi».
