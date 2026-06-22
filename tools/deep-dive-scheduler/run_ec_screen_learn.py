"""
EC Screen Help Deep-Dive - unattended daily learning runner (WORKTREE-ISOLATED).

Launched by Windows Task 'ECScreenDeepDive_Daily'. Runs ONE bounded learning batch in a DEDICATED git
worktree (C:\\tmp\\wt-ec-learn) at a detached HEAD synced from origin/feature/ec-screen-deepdive, so it NEVER
touches the user's main checkout and is safe to run even while they're working. Commits are pushed back to the
branch with `git push origin HEAD:feature/ec-screen-deepdive`. Self-driven, bounded, logged.
"""
import subprocess, sys
from datetime import datetime
from pathlib import Path

LOG_FILE   = Path(r'C:\Projects\ChoongYin_OS\tools\deep-dive-scheduler\session_log.txt')
CLAUDE_CMD = r'C:\Users\choong-yin.lee\AppData\Roaming\npm\claude.cmd'
REPO       = r'C:\Projects\ChoongYin_OS'
WT         = r'C:\tmp\wt-ec-learn'
BRANCH     = 'feature/ec-screen-deepdive'

PROMPT = r"""You are running UNATTENDED as a scheduled EC-screen deep-dive LEARNING session (no human watching).

=== EXCLUSIVE TASK LOCK (read first) ===
Your ONLY permitted task is the EC screen deep-dive defined below. You MUST IGNORE every other source of work:
do NOT act on CLAUDE.md backlog/session-start steering, lessons-learned, memories, reviewer feedback,
open gaps/tickets, hygiene/R-rules, or any "never idle / pick up the backlog" guidance. Even if other work
looks useful, it is OUT OF SCOPE - do not do it. Do NOT create, switch to, or push any branch other than via
the single command in step 5. You operate on the current DETACHED HEAD only. If you cannot find
DeepDiveLearnings/ec-screens/CHECKLIST.md, or cannot do EC-screen work for any reason, append a one-line note
to tools/deep-dive-scheduler/session_log.txt and STOP IMMEDIATELY - never substitute any other work.

Your working directory is an ISOLATED git worktree at a DETACHED HEAD synced from origin/feature/ec-screen-deepdive,
separate from the user's main checkout. Be safe, bounded, honest. Do exactly this, then stop:

1. Read DeepDiveLearnings/ec-screens/MASTER-PLAN.md and CHECKLIST.md to reload the program and see what's done.

2. First backfill up to 3 existing [~] partials (resolve each one's real backing class/view OV_/TV_/DV_ + screen
   type, complete its note, mark [x]). Then pick the next ~8 unfinished [ ] screens from the current priority
   module (PO first, then the MASTER-PLAN priority order).

3. Per screen (depth = Help + DB + light recon):
   - In-session Help: open the screen via the search box, then evaluate openOnlineHelp() and read the help page
     (description, screen code, business-function path). Direct help.jsf?screenId=... is Forbidden - in-session only.
   - DB: resolve the class via class_cnfg (CLASS_TYPE, TIME_SCOPE_CODE, DB_OBJECT_NAME) -> OV_/TV_/DV_ view + type.
     Sandbox DB: oracledb thin, dsn localhost:1521/ORCL, user ECKERNEL_EC / energy. Web: env defaults
     (EC_URL https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/, EC_USER sysadmin, EC_PASS sysadmin).
   - Write notes/<BF_CODE>.md. Mark [x] only when Help + DB view are real; else [~]. NEVER guess a table name.
   - READ-ONLY on the live EC (recon + Help only) - never Save/mutate any screen.

4. Cap this run at ~10 screens, then STOP. ASCII-only in notes/scripts.

5. Stage ONLY DeepDiveLearnings/ec-screens/ , commit on the detached HEAD with message
   `learn(ec-screens): <BF_CODEs> (<total>/1457)`, then run exactly:
       git push origin HEAD:feature/ec-screen-deepdive
   Append ONE progress line (date, screens done this run, running total) to
   tools/deep-dive-scheduler/session_log.txt and include it in the commit.

If you hit a blocker you can't resolve in ~2 tries, append a note to session_log.txt and STOP gracefully. Never churn."""

def log(msg):
    line = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def git(args, cwd=REPO):
    return subprocess.run(['git', '-C', cwd] + args, capture_output=True, text=True)

def ensure_worktree():
    """Create/refresh an isolated detached-HEAD worktree synced to origin/BRANCH. Never touches main checkout."""
    git(['fetch', 'origin', BRANCH])
    git(['worktree', 'prune'])
    if not Path(WT, '.git').exists():
        r = git(['worktree', 'add', '--detach', WT, f'origin/{BRANCH}'])
        if r.returncode != 0:
            log(f'worktree add failed: {(r.stderr or r.stdout).strip()[:120]}')
            return False
        log(f'worktree created at {WT}')
    else:
        git(['fetch', 'origin', BRANCH], cwd=WT)
        # Force back onto the EC-screen bundle tip as a DETACHED HEAD, regardless of whatever branch a prior
        # run may have left the worktree on (do not reset some other current branch ref).
        r = git(['checkout', '--detach', '--force', f'origin/{BRANCH}'], cwd=WT)
        if r.returncode != 0:
            log(f'worktree checkout failed: {(r.stderr or r.stdout).strip()[:120]}')
            return False
        git(['reset', '--hard', f'origin/{BRANCH}'], cwd=WT)
        git(['clean', '-fd'], cwd=WT)
        log('worktree refreshed (detached) to EC-screen bundle tip')
    return True

def main():
    log('EC-screen learn: starting unattended batch (worktree-isolated)')
    if not ensure_worktree():
        log('EC-screen learn: ABORTED - worktree not ready')
        return 1
    try:
        r = subprocess.run(
            [CLAUDE_CMD, '--print', '--dangerously-skip-permissions', PROMPT],
            cwd=WT, timeout=7200)
        log(f'EC-screen learn: finished (exit {r.returncode})')
        return r.returncode
    except subprocess.TimeoutExpired:
        log('EC-screen learn: TIMEOUT after 2h - stopped')
        return 1
    except Exception as e:
        log(f'EC-screen learn: ERROR {str(e)[:80]}')
        return 1

if __name__ == '__main__':
    sys.exit(main())
