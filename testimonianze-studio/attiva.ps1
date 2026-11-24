# Testimonianze Studio — attiva l'esecuzione automatica: ogni giorno all'ora indicata in config.json.
# Se a quell'ora il PC è spento, parte alla prima accensione (con accesso fatto). Per spegnerla: disattiva.ps1
$ErrorActionPreference = "Stop"
$qui = Split-Path -Parent $MyInvocation.MyCommand.Path
$ora = (Get-Content "$qui\config.json" -Raw -Encoding UTF8 | ConvertFrom-Json).ora_esecuzione
if (-not $ora) { $ora = "10:00" }
$python = "$qui\.venv\Scripts\pythonw.exe"
if (-not (Test-Path $python)) { throw "Prima esegui installa.ps1" }
$azione = New-ScheduledTaskAction -Execute $python -Argument "`"$qui\esegui.py`" --pianificato" -WorkingDirectory $qui
$regole = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) -MultipleInstances IgnoreNew
$ogniGiorno = New-ScheduledTaskTrigger -Daily -At $ora
$descr = "Testimonianze Studio: scarica il foglio, sceglie le testimonianze, scrive e impagina il contenuto del giorno."
try {
    # secondo avvio a ogni accesso: copre il caso «PC acceso dopo l'orario» (lo script salta se la consegna c'è già)
    $accesso = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
    Register-ScheduledTask -TaskName "Testimonianze Studio" -Action $azione -Trigger $ogniGiorno, $accesso -Settings $regole -Description $descr -Force | Out-Null
} catch {
    # senza diritti di amministratore l'avvio «all'accesso» non si può registrare: resta il recupero automatico dell'avvio mancato
    Register-ScheduledTask -TaskName "Testimonianze Studio" -Action $azione -Trigger $ogniGiorno -Settings $regole -Description $descr -Force | Out-Null
}
Write-Host "Automazione attiva: ogni giorno alle $ora. La vedi in «Utilità di pianificazione» con il nome «Testimonianze Studio»."
