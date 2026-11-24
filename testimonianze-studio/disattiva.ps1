# Testimonianze Studio — spegne l'esecuzione automatica (non cancella niente).
Unregister-ScheduledTask -TaskName "Testimonianze Studio" -Confirm:$false
Write-Host "Automazione disattivata."
