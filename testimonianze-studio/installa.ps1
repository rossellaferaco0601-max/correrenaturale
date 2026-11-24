# Testimonianze Studio — installazione sul PC (si lancia una volta). NON attiva l'automazione: per quella c'è attiva.ps1
#   Tasto destro sul file → «Esegui con PowerShell», oppure:  powershell -ExecutionPolicy Bypass -File installa.ps1
$ErrorActionPreference = "Stop"
$qui = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $qui
Write-Host "1/4  Ambiente Python (cartella .venv)..."
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { throw "Python non trovato. Installa Python 3.11 o successivo da python.org e riprova." }
if (-not (Test-Path ".venv")) { python -m venv .venv }
& ".\.venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt
Write-Host "2/4  Claude Code..."
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Warning "Comando 'claude' non trovato nel PATH: installa Claude Code e apri una volta 'claude' per accedere con l'abbonamento."
} else { Write-Host "     trovato: $((Get-Command claude).Source)" }
if ($env:ANTHROPIC_API_KEY) { Write-Warning "Sul PC esiste la variabile ANTHROPIC_API_KEY: il programma la ignora e usa solo l'abbonamento." }
Write-Host "3/4  Chiave del service account..."
New-Item -ItemType Directory -Force -Path "dati" | Out-Null
if (-not (Test-Path "dati\service-account.json")) {
    Write-Warning "Manca dati\service-account.json: segui GUIDA-SERVICE-ACCOUNT.md e copia qui il file della chiave."
} else {
    $email = (Get-Content "dati\service-account.json" -Raw | ConvertFrom-Json).client_email
    Write-Host "     trovata. Il foglio va condiviso (Visualizzatore) con: $email"
}
Write-Host "4/4  Anteprime dei modelli (cartella anteprime)..."
& ".\.venv\Scripts\python.exe" esegui.py --anteprime
Write-Host ""
Write-Host "Fatto. Prova una consegna con:   .\.venv\Scripts\python.exe esegui.py"
Write-Host "Quando sei soddisfatta, attiva l'automazione con:   powershell -ExecutionPolicy Bypass -File attiva.ps1"
