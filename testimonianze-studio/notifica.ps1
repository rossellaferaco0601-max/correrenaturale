# Notifica di Windows: «contenuto pronto» oppure «qualcosa è andato storto». Clic = apre la cartella del giorno.
param([string]$Titolo = "Testimonianze Studio", [string]$Testo = "", [string]$Cartella = "")
$ErrorActionPreference = "Stop"
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$t = [System.Security.SecurityElement]::Escape($Titolo)
$b = [System.Security.SecurityElement]::Escape($Testo)
$apri = ""
if ($Cartella -and (Test-Path $Cartella)) {
    $uri = [System.Security.SecurityElement]::Escape(([System.Uri](Resolve-Path $Cartella).Path).AbsoluteUri)
    $apri = " activationType='protocol' launch='$uri'"
}
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml("<toast$apri><visual><binding template='ToastGeneric'><text>$t</text><text>$b</text></binding></visual></toast>")
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
$app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show($toast)
