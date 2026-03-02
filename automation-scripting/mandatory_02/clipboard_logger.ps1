# Clipboard Logger
# Checks clipboard, and compares with stored variable
# If different, log clipboard and change stored variable to content

$currentClipboard = Get-Clipboard

$scriptPath = Split-Path $MyInvocation.MyCommand.Path -Parent
$clipboardFile = Join-Path -Path "$scriptPath" -ChildPath "clipboard.txt"
$logFile = Join-Path -Path "$scriptPath" -ChildPath "clipboard.log"

Write-Host "Script path: $scriptPath"
Write-Host "clipboard file: $clipboardFile"

if (!(Test-Path "$clipboardFile")) {
    New-Item -Path "$scriptPath" -Name "clipboard.txt"
    Write-Host "clipboard file not found, creating file"
} else {
    Write-Host "clipboard already exists, just continuing"
}

$fileClipboard = Get-Content -Path "$clipboardFile"
Write-Host "clipboard.txt content: $fileClipboard"

if ($currentClipboard -ne $fileClipboard) {
    # Log the change
    $timestamp = Get-Date
    Add-Content -Path "$logFile" -Value "$timestamp | $currentClipboard"
    # Save new clipboard content
    Set-Content -Path "$clipboardFile" -Value "$currentClipboard"
} else {
    Write-Host "Nice"
}
