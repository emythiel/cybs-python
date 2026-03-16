$taskName = "Clippy"
$servicePath = Split-Path $MyInvocation.MyCommand.Path -Parent
$clipboardScript = Join-Path $servicePath "clipboard_logger.ps1"

# Check if task exists
$clippyService = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

try {
    # Check if Task exists
    if (!$clippyService) {
        # Define the action
        $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$clipboardScript`""
        # Define the trigger (at user logon)
        $trigger = New-ScheduledTaskTrigger -AtLogOn
        # Settings (disable AC requirement)
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

        # Create the task
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest
        # Run the task (create task doesn't auto start)
        Start-ScheduledTask -TaskName $taskName
    } else {
        # Stop task and remove
        Stop-ScheduledTask -TaskName $taskName
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
} catch {
    Read-Host "WAT"
}
