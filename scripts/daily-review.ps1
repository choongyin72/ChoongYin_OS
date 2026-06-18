# daily-review.ps1
# Called by Windows Task Scheduler daily at 06:00 AWST.
# Reads the review prompt from .claude/scheduled_tasks.json and pipes it to claude CLI.
# Output is appended to scripts/daily-review.log.

$RepoRoot = Split-Path $PSScriptRoot   # scripts/ -> repo root
$LogFile  = "$PSScriptRoot\daily-review.log"
$TasksFile = "$RepoRoot\.claude\scheduled_tasks.json"

function Write-Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $msg"
    $line | Tee-Object -FilePath $LogFile -Append
}

Write-Log "=== Daily review started ==="

if (-not (Test-Path $TasksFile)) {
    Write-Log "ERROR: $TasksFile not found — aborting."
    exit 1
}

# Extract the first task's prompt (index 0 = the daily review task)
$tasks  = Get-Content $TasksFile -Raw | ConvertFrom-Json
$prompt = $tasks.tasks[0].prompt

if (-not $prompt) {
    Write-Log "ERROR: No prompt found in scheduled_tasks.json — aborting."
    exit 1
}

Set-Location $RepoRoot

# Write prompt to a temp file and redirect as stdin.
# The PowerShell pipe operator does not deliver stdin reliably in non-interactive
# Task Scheduler sessions — file redirect is the safe alternative.
$tempPrompt = Join-Path $env:TEMP "claude-daily-review-prompt.txt"
[System.IO.File]::WriteAllText($tempPrompt, $prompt, (New-Object System.Text.UTF8Encoding $false))

cmd /c "claude --dangerously-skip-permissions --print < `"$tempPrompt`"" 2>&1 |
    Tee-Object -FilePath $LogFile -Append

Remove-Item $tempPrompt -ErrorAction SilentlyContinue

Write-Log "=== Daily review finished ==="
