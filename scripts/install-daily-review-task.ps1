# install-daily-review-task.ps1
# One-time setup: registers daily-review.ps1 in Windows Task Scheduler to run at 06:00 AWST.
# Run once as Administrator.

$scriptPath = "$PSScriptRoot\daily-review.ps1"
# -WindowStyle Hidden: run with no visible PowerShell window (claude --print works silently, so the
# window would otherwise just sit blank for the whole run and look hung). Keeps InteractiveToken logon
# (so git/gh network access still works without storing a password).
$action     = New-ScheduledTaskAction `
    -Execute  "powershell.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

# 06:00 daily (machine must be set to AWST / Perth timezone)
$trigger  = New-ScheduledTaskTrigger -Daily -At "06:00"
# -StartWhenAvailable: run ASAP if the machine was off at the scheduled trigger time
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit  (New-TimeSpan -Minutes 60) `
    -StartWhenAvailable `
    -WakeToRun:$false

Register-ScheduledTask `
    -TaskName "ClaudeOS-DailyReview" `
    -Action   $action `
    -Trigger  $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task registered: ClaudeOS-DailyReview (runs daily at 06:00 AWST)"
Write-Host "Log output: $PSScriptRoot\daily-review.log"
