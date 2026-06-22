"""
EC Screen Help Deep-Dive — unattended daily learning runner.
Launched by Windows Task Scheduler; invokes Claude CLI non-interactively to do ONE bounded learning batch
on the feature/ec-screen-deepdive branch, then stops. Self-driven, safe, logged.
"""
import subprocess, sys
from datetime import datetime
from pathlib import Path

LOG_FILE   = Path(r'C:\Projects\ChoongYin_OS\tools\deep-dive-scheduler\session_log.txt')
CLAUDE_CMD = r'C:\Users\choong-yin.lee\AppData\Roaming\npm\claude.cmd'
PROJECT    = r'C:\Projects\ChoongYin_OS'

PROMPT = r"""You are running as an UNATTENDED, scheduled EC-screen deep-dive LEARNING session (no human is watching).
Be safe, bounded, and honest. Do exactly this, then stop:

0. SAFETY: run `git rev-parse --abbrev-ref HEAD`. You must end up on branch `feature/ec-screen-deepdive`.
   If `git checkout feature/ec-screen-deepdive` fails because of UNRELATED uncommitted files (a parallel
   session's work), append one line explaining that to tools/deep-dive-scheduler/session_log.txt and STOP.
   NEVER stash, discard, commit, or touch files that are not part of DeepDiveLearnings/ec-screens/. Never touch master.

1. Read DeepDiveLearnings/ec-screens/MASTER-PLAN.md and CHECKLIST.md to reload the program + see what is done.

2. First backfill up to 3 existing [~] partials: open each screen and resolve its real backing class/view
   (OV_/TV_/DV_) + screen type, complete its note, mark [x]. Then pick the next ~8 unfinished [ ] screens from
   the current priority module (PO first, then the MASTER-PLAN priority order).

3. Per screen (depth = Help + DB + light recon):
   - In-session Help: open the screen via the search box, then evaluate openOnlineHelp() and read the help page
     (description, screen code, business-function path). Direct help.jsf?screenId=... is Forbidden - in-session only.
   - DB: resolve the class via class_cnfg (CLASS_TYPE, TIME_SCOPE_CODE, DB_OBJECT_NAME) -> OV_/TV_/DV_ view + type.
     Sandbox DB: oracledb thin, dsn localhost:1521/ORCL, user ECKERNEL_EC / energy. Web: env defaults
     (EC_URL https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/, EC_USER sysadmin, EC_PASS sysadmin).
   - Write notes/<BF_CODE>.md. Mark [x] only when Help + DB view are real; else [~]. NEVER guess a table name.
   - READ-ONLY on the live EC (recon + Help only) - never Save/mutate any screen.

4. Cap this run at ~10 screens, then STOP (do not run away). ASCII-only in notes/scripts.

5. Commit on feature/ec-screen-deepdive with message `learn(ec-screens): <BF_CODEs> (<n>/1457)` and
   `git push origin feature/ec-screen-deepdive`. Append ONE progress line (date, screens done, running total)
   to tools/deep-dive-scheduler/session_log.txt.

If you hit a blocker you cannot resolve in ~2 tries, LOG it to the session_log and STOP gracefully. Do not churn."""

def log(msg):
    line = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def main():
    log('EC-screen learn: starting unattended batch')
    try:
        r = subprocess.run(
            [CLAUDE_CMD, '--print', '--dangerously-skip-permissions', PROMPT],
            cwd=PROJECT, timeout=7200)
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
