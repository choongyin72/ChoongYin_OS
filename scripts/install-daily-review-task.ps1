# install-daily-review-task.ps1
# One-time setup: registers daily-review.ps1 in Windows Task Scheduler to run twice daily.
# Fires at 06:00 AWST and 14:00 AWST (machine must be set to AWST / Perth timezone).
# Run once as Administrator. Re-run to update an existing registration (-Force overwrites in place).

$scriptPath = "$PSScriptRoot\daily-review.ps1"
$action     = New-ScheduledTaskAction `
    -Execute  "powershell.exe" `
    -Argument "-NonInteractive -ExecutionPolicy Bypass -File `"$scriptPath`""

# Two daily triggers: 06:00 AWST (morning) and 14:00 AWST (afternoon)
$trigger06 = New-ScheduledTaskTrigger -Daily -At "06:00"
$trigger14 = New-ScheduledTaskTrigger -Daily -At "14:00"
# -StartWhenAvailable: run ASAP if machine was off at trigger time
# MultipleInstances IgnoreNew: skip the new instance if a prior run is still in progress
$settings  = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit  (New-TimeSpan -Minutes 60) `
    -StartWhenAvailable `
    -MultipleInstances   IgnoreNew `
    -WakeToRun:$false

Register-ScheduledTask `
    -TaskName "ClaudeOS-DailyReview" `
    -Action   $action `
    -Trigger  @($trigger06, $trigger14) `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task registered: ClaudeOS-DailyReview (runs at 06:00 and 14:00 AWST)"
Write-Host "Log output: $PSScriptRoot\daily-review.log"
