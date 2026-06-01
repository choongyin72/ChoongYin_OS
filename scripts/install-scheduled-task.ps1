# install-scheduled-task.ps1
# One-time setup: registers auto-attach.ps1 in Windows Task Scheduler to run every 10 min.
# Run once as Administrator.

$scriptPath = "$PSScriptRoot\auto-attach.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NonInteractive -File \"$scriptPath\""
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 10) -Once -At (Get-Date)
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

Register-ScheduledTask -TaskName "ClaudeOS-AutoAttach" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
Write-Host "Task registered: ClaudeOS-AutoAttach (runs every 10 min)"
