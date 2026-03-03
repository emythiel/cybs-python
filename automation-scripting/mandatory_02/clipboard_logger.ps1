# Clipboard Logger
# Checks clipboard, and compares with stored variable
# If different, log clipboard and change stored variable to content

# Set script path and logfile path
$scriptPath = Split-Path $MyInvocation.MyCommand.Path -Parent
$logFile = Join-Path $scriptPath "clipboard.log"

# Check if logfile exists, create if it doesn't
if (!(Test-Path $logFile)) {
    New-Item -Path $logFile -ItemType File | Out-Null
}

# Get current clipboard content
$currentClipboard = Get-Clipboard

# Get the last line of the logfile, split at first | to ignore timestamp
$fileClipboard = ((Get-Content $logFile -Tail 1) -split '\|.',2)[1]

# Compare clipboard content with latest logfile entry
if ($currentClipboard -ne $fileClipboard) {
    # Log the change
    $timestamp = Get-Date
    Add-Content -Path $logFile -Value "$timestamp | $currentClipboard"
}
