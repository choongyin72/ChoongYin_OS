# install-daily-review-task.ps1
# One-time setup: registers daily-review.ps1 in Windows Task Scheduler to run every hour.
# Run once as Administrator. Re-run to update an existing registration (-Force overwrites in place).

$scriptPath = "$PSScriptRoot\daily-review.ps1"
# -WindowStyle Hidden: run with no visible PowerShell window (claude --print works silently, so the
# window would otherwise just sit blank for the whole run and look hung). Keeps InteractiveToken logon
# (so git/gh network access still works without storing a password).
$action     = New-ScheduledTaskAction `
    -Execute  "powershell.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

# Hourly repetition starting from now (machine timezone must be AWST / Perth)
$trigger  = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Hours 1)
# -StartWhenAvailable: run ASAP if machine was off at trigger time
# MultipleInstances IgnoreNew: skip the new instance if a prior run is still in progress
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit    (New-TimeSpan -Minutes 55) `
    -StartWhenAvailable `
    -MultipleInstances     IgnoreNew `
    -WakeToRun:$false

Register-ScheduledTask `
    -TaskName "ClaudeOS-DailyReview" `
    -Action   $action `
    -Trigger  $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task registered: ClaudeOS-DailyReview (runs every hour)"
Write-Host "Log output: $PSScriptRoot\daily-review.log"
