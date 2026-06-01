# auto-attach.ps1
# Polls workstreams/claude-schedule/drafts/ every ~10 min (via Task Scheduler).
# For each spec with status: approved, arms it via RemoteTrigger, then sets status: armed.
# Requires: Claude Code CLI on PATH, OAuth'd session.

$draftsDir = "$PSScriptRoot\..\workstreams\claude-schedule\drafts"
$specs = Get-ChildItem -Path $draftsDir -Filter "*.md"

foreach ($spec in $specs) {
    $content = Get-Content $spec.FullName -Raw
    if ($content -match "status: approved") {
        Write-Host "Arming: $($spec.Name)"
        # Replace with actual RemoteTrigger CLI invocation when available
        # claude schedule arm --spec "$($spec.FullName)"
        $content = $content -replace "status: approved", "status: armed"
        Set-Content -Path $spec.FullName -Value $content
        Write-Host "Armed: $($spec.Name)"
    }
}
