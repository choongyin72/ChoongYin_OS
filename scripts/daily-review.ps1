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

# Pipe prompt via stdin so special characters (backticks, $, quotes) are safe
$prompt | claude --dangerously-skip-permissions --print 2>&1 | Tee-Object -FilePath $LogFile -Append

Write-Log "=== Daily review finished ==="
