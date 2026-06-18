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

# Feed the prompt to claude via stdin. Two gotchas under Task Scheduler (both fixed here):
#   1. PowerShell resolves `claude` to claude.ps1, which is BLOCKED by the execution policy
#      ("running scripts is disabled on this system").
#   2. The .cmd shim's `< file` stdin redirect does NOT deliver input to claude.exe — the original
#      failure: "Input must be provided either through stdin or as a prompt argument when using --print".
# Fix: call claude.exe DIRECTLY (bypasses the blocked .ps1) and pipe the prompt natively — a real
# PowerShell pipe DOES deliver stdin to the .exe (verified). Resolve the exe relative to the .cmd shim.
$claudeExe = Join-Path (Split-Path (Get-Command claude.cmd).Source) 'node_modules\@anthropic-ai\claude-code\bin\claude.exe'
if (-not (Test-Path $claudeExe)) {
    Write-Log "ERROR: claude.exe not found at $claudeExe — aborting."
    exit 1
}

$prompt | & $claudeExe --dangerously-skip-permissions --print 2>&1 |
    Tee-Object -FilePath $LogFile -Append

Write-Log "=== Daily review finished ==="
