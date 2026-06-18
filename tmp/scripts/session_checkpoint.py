"""Context-loss insurance: snapshot the machine-derivable session state so a resume/post-clear session can
fast-forward without losing the trail. Read-only (git/gh queries only). Prints a ready-to-paste CHECKPOINT
block for the resume log; the human/Claude fills the narrative bits (ACTIVE TASK / PENDING / BLOCKERS).
Usage:  py tmp/scripts/session_checkpoint.py   (optionally STAMP="2026-06-18 00:30 AWST")"""
import subprocess, os

def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=r"c:\Projects\ChoongYin_OS", timeout=30).stdout.strip()
    except Exception as e:
        return f"(err: {str(e)[:50]})"

branch = sh("git rev-parse --abbrev-ref HEAD")
head = sh("git rev-parse --short HEAD")
ahead = sh("git rev-list --count origin/master..HEAD 2>/dev/null") or "?"
local = sh("git rev-parse HEAD")
remote = sh(f"git rev-parse origin/{branch} 2>/dev/null")
synced = "IN SYNC" if (remote and local == remote) else "NOT pushed / diverged"
recent = sh("git log --oneline -8")
# uncommitted (exclude the noisy untracked tmp churn -> show tracked-modified + staged only)
dirty = sh("git status --porcelain --untracked-files=no")
prs = sh("gh pr list --state open --limit 30 --json number,title,headRefName -q '.[] | \"  #\\(.number) \\(.headRefName) — \\(.title)\"' 2>/dev/null") or "(gh unavailable / none)"
stamp = os.environ.get("STAMP", "(stamp manually)")

print(f"""## CHECKPOINT — {stamp}
**GIT:** branch `{branch}` @ `{head}` · {ahead} commits ahead of master · {synced}
**Recent commits:**
{recent}

**Uncommitted (tracked) — MUST be committed before /clear or token-limit:**
{dirty or "  (clean — nothing tracked-modified)"}

**Open PRs (awaiting reviewer/merge):**
{prs}

**ACTIVE TASK:** <fill: the ONE thing in flight + its exact next step>
**DONE THIS SESSION:** <fill: what's committed, with hashes/PRs>
**PENDING / NEXT:** <fill>
**BLOCKERS / OPEN Qs:** <fill>
**KEY FACTS BANKED (don't re-derive):** <fill or link [[memory]]>
""")
