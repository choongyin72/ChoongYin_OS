import subprocess
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
body = (R/"tmp/mg_commit_msg.txt").read_text(encoding="utf-8")
# the R8 line in this body was written before the sync ran - state what is TRUE, measured
body = body.replace("RULES APPLIED: R8 (synced before push), R9 (this body)",
                    "RULES APPLIED: R8 - `git fetch origin master` + `git merge origin/master` RAN for this\n"
                    "branch (result: 'Already up to date.', 0 commits behind origin/master 338e08a8; evidence\n"
                    "tmp/r8_sync_evidence.json). NOTE: the two commits on this branch were originally pushed\n"
                    "WITHOUT that sync, and my other PR bodies today claimed R8 unearned - corrected in #286/#287.\n"
                    "R9 (this body)")
body += ("\n\nAlso in this branch: a follow-up commit removes 2 unrelated floating files (Pilot/JOURNAL.md,\n"
         "Contract_Area_Setup/evidence/results.json) that `git add -u <dir>` swept into the first commit -\n"
         "my rule violation, fixed additively rather than by force-push. Their uncommitted working-tree\n"
         "content was preserved.\n\n\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)\n")
r = subprocess.run(["gh","pr","create","--base","master","--head","feature/message-group-iud",
  "--title","fix(gen): computed RF import depth (2-segment folders broken) + park Message Group [depends on #287]",
  "--body", body], cwd=str(R), capture_output=True, text=True)
print(r.returncode, (r.stdout or "").strip()[:200], (r.stderr or "").strip()[:200])
