# Clipboard Logger
# Checks clipboard, and compares with stored variable
# If different, log clipboard and change stored variable to content
# Install (Powershell, run as admin):
# schtasks /create /sc ONLOGON /tn Clippy /tr "powershell.exe -ExecutionPolicy Bypass -File C:\PATH\TO\FILES\clipboard_logger.ps1"

# Set script path and logfile path
$scriptPath = Split-Path $MyInvocation.MyCommand.Path -Parent
$logFile = Join-Path $scriptPath "clipboard.log"

while ($true) {
    # Check if logfile exists, create if it doesn't
    # Done inside loop in case file is deleted while script is running
    if (!(Test-Path $logFile)) {
        New-Item -Path $logFile -ItemType File | Out-Null
    }

    # Get current clipboard content
    # Each new line is it's own element in an array, so we join them with a space
    # This helps with problems with new lines
    $currentClipboard = ((Get-Clipboard) -Join ' ')

    # Get last line of clipboard (if it's there)
    $lastLine = Get-Content $logFile -Tail 1 -ErrorAction SilentlyContinue
    # Split at '|' so we ignore  the initial timestamp
    $fileClipboard = if ($lastLine) { ($lastLine -split '\>',2)[1] } else { "" }

    # Compare clipboard content with latest logfile entry
    if ($currentClipboard -ne $fileClipboard) {
        # Log the change
        $timestamp = Get-Date -Format "yyyy/MM/dd-HH:mm:ss"
        Add-Content -Path $logFile -Value "$timestamp>$currentClipboard"
    }

    # Wait 5 seconds before checking again
    Start-Sleep -Seconds 5
}
