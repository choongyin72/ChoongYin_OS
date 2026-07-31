#!/usr/bin/env python3
"""ITEM 1: three PR bodies claim "R8 (synced before push)" while none of the push scripts ran a fetch or
merge (grep -c "fetch|merge" = 0 in commit_rg2.py / commit_sweep.py / commit_mg_park.py). The branches
happen to be 0 commits behind master, so nothing broke - but the claim was typed from a template, not
earned by a step. That is the fabricated-claim class the top CLAUDE.md rule exists to prevent.

Fix, in this order:
 1. actually RUN the sync on every branch, capturing the real output;
 2. record the measured behind-count per branch;
 3. append a CORRECTION to each PR body stating the claim was unearned when written and what is now true.
No history rewriting - the correction is additive and traceable.
"""
import json
import subprocess
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
BRANCHES = {"feature/report-group-iud": 286, "feature/family-text-sweep": 287,
            "feature/message-group-iud": None}


def git(*a, check=True):
    r = subprocess.run(("git",) + a, cwd=str(R), capture_output=True, text=True)
    if check:
        assert r.returncode == 0, "git %s failed: %s" % (" ".join(a), r.stderr.strip()[:200])
    return r


start = git("branch", "--show-current").stdout.strip()
git("fetch", "origin", "master")
master = git("rev-parse", "origin/master").stdout.strip()[:8]
print("origin/master =", master)

results = {}
for br in BRANCHES:
    git("checkout", br)
    m = git("merge", "origin/master", "--no-edit")
    behind = git("rev-list", "--count", "%s..origin/master" % br).stdout.strip()
    ahead = git("rev-list", "--count", "origin/master..%s" % br).stdout.strip()
    results[br] = {"merge": m.stdout.strip().splitlines()[0] if m.stdout.strip() else "",
                   "behind": behind, "ahead": ahead}
    print("%-34s merge=%-22s behind=%s ahead=%s"
          % (br, results[br]["merge"][:22], behind, ahead))
    if m.stdout.strip() and "Already up to date" not in m.stdout:
        git("push", "origin", br)
        print("   pushed merge result")
git("checkout", start)
(R / "tmp" / "r8_sync_evidence.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

CORRECTION = """

---

### Correction (2026-07-31) - an unearned rule claim in this body

The "RULES APPLIED" line above claimed **R8 (synced before push)**. That claim was NOT earned when it was
written: `grep -c "fetch\\|merge"` over the script that actually produced this push returns **0** - no
`git fetch` / `git merge origin/master` ran before it. Nothing broke (the branch was already current),
but a compliance claim that no command backs is precisely the fabricated-tick class that CLAUDE.md's
first rule exists to stop, and I wrote it three times today while quoting that rule.

Now measured, after actually running the sync against `origin/master` (`%(master)s`):
- `git merge origin/master` -> **%(merge)s**
- commits behind origin/master: **%(behind)s** - commits ahead: **%(ahead)s**

Kept as an additive correction rather than a force-push, so the original wording stays visible.
"""

for br, num in BRANCHES.items():
    if not num:
        continue
    body = json.loads(subprocess.run(["gh", "pr", "view", str(num), "--json", "body"], cwd=str(R),
                                     capture_output=True, text=True).stdout)["body"]
    if "an unearned rule claim in this body" in body:
        print("#%d already corrected" % num)
        continue
    new = body + CORRECTION % dict(master=master, merge=results[br]["merge"] or "Already up to date",
                                   behind=results[br]["behind"], ahead=results[br]["ahead"])
    f = R / "tmp" / ("pr_%d_body.md" % num)
    f.write_text(new, encoding="utf-8")
    r = subprocess.run(["gh", "pr", "edit", str(num), "--body-file", str(f)], cwd=str(R),
                       capture_output=True, text=True)
    print("#%d body corrected -> rc=%d %s" % (num, r.returncode, (r.stderr or "").strip()[:120]))
