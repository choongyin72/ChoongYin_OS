#!/usr/bin/env python3
"""Mechanical enforcement of the three git rules I broke on 2026-07-31 by relying on attention.

  py scripts/safe_commit.py --msg-file tmp/msg.txt --paths <p1> <p2> ... [--push <branch>]

WHAT IT ENFORCES (each as an exit code, not a reminder):

 1. EXPLICIT PATHS ONLY. Stages exactly the paths given (deletions included - `git add <deleted path>`
    records a removal). Then it compares the STAGED set against the requested set and ABORTS on any
    extra. Origin: I used `git add -u <dir>`, which swept two unrelated floating files (Pilot/JOURNAL.md,
    Contract_Area_Setup/evidence/results.json) into a commit, breaking "stage only this session's files
    by explicit path".

 2. NO HAND-TYPED RULE CLAIMS. Refuses a message that asserts R8/synced-before-push in prose. The R8 line
    is APPENDED by this script from the sync it actually ran. Origin: three PR bodies claimed
    "R8 (synced before push)" while `grep -c "fetch\\|merge"` over the push scripts returned 0.

 3. SYNC BEFORE PUSH, ALWAYS. With --push it runs `git fetch origin master` + `git merge origin/master`
    and only then pushes, recording the real output in the commit trailer.

Prints the staged set BEFORE committing - the check that catches a mistake must precede the irreversible
step, not follow it (I caught the add -u accident with `git show --stat` afterwards).
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANNED = ["r8 (synced", "synced before push", "rules applied: r8"]
# A line that DESCRIBES or ADMITS the bad claim is not the bad claim - this guard blocked the very commit
# that confessed the fabricated R8 claim. Same fix as check_row_vocab.py's META_LINE_MARKERS.
DESCRIBING = ["claimed", "claim was", "false", "unearned", "fabricat", "origin:", "was wrong",
              "grep -c", "returned 0", "bodies said", "deliberately excluded", "correctly blocked",
              "refuses a message", "hand-types", "appended by this script"]


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


def git(*args, check=True):
    r = subprocess.run(("git",) + args, cwd=str(ROOT), capture_output=True, text=True)
    if check and r.returncode != 0:
        print(a("FAIL: git %s\n%s" % (" ".join(args), (r.stderr or "").strip()[:400])))
        sys.exit(1)
    return r


def expand(paths):
    """A directory argument legitimately covers everything under it; anything else must be named."""
    out = set()
    for p in paths:
        f = ROOT / p
        if f.is_dir():
            for sub in f.rglob("*"):
                if sub.is_file():
                    out.add(sub.relative_to(ROOT).as_posix())
        else:
            out.add(Path(p).as_posix())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--msg-file", required=True)
    ap.add_argument("--paths", nargs="+", required=True)
    ap.add_argument("--push", default="")
    ap.add_argument("--allow-deleted-dir", nargs="*", default=[],
                    help="dirs deleted wholesale (cannot be globbed - they are gone)")
    args = ap.parse_args()

    msg_path = ROOT / args.msg_file
    msg = msg_path.read_text(encoding="utf-8")
    hit = []
    for n, line in enumerate(msg.splitlines(), 1):
        low = line.lower()
        if any(d in low for d in DESCRIBING):        # describing/admitting, not asserting
            continue
        if any(b in low for b in BANNED):
            hit.append("line %d: %s" % (n, line.strip()[:90]))
    if hit:
        print(a("ABORT: the message ASSERTS a rule claim in prose:"))
        for h in hit:
            print(a("   %s" % h))
        print(a("       The R8/sync line is APPENDED BY THIS SCRIPT from the sync it actually runs.\n"
                "       Remove the typed claim. (Origin: 3 PR bodies claimed R8 with 0 fetch/merge calls.)"))
        return 1

    # ---- 1. stage exactly what was asked for ----------------------------------------------------
    git("add", "--", *args.paths)
    staged = {l.strip() for l in git("diff", "--cached", "--name-only").stdout.splitlines() if l.strip()}
    requested = expand(args.paths)
    for d in args.allow_deleted_dir:
        requested |= {s for s in staged if s.startswith(Path(d).as_posix().rstrip("/") + "/")}
    # a staged DELETION of a file under a requested dir cannot be globbed (the file is gone) - allow it
    for p in args.paths:
        pref = Path(p).as_posix().rstrip("/") + "/"
        requested |= {s for s in staged if s.startswith(pref)}

    extra = sorted(staged - requested)
    print(a("staged %d file(s); requested %d path(s)" % (len(staged), len(args.paths))))
    for s in sorted(staged):
        print(a("   + %s" % s))
    if extra:
        print(a("\nABORT: %d file(s) staged that you did NOT pass explicitly:" % len(extra)))
        for e in extra:
            print(a("   ! %s" % e))
        print(a("       Unstage them or name them. (Origin: `git add -u` swept 2 unrelated floating files.)"))
        git("reset", "-q")
        return 1
    if not staged:
        print("ABORT: nothing staged")
        return 1

    # ---- 3. sync FIRST when we intend to push, so the trailer states a fact -----------------------
    trailer = ""
    if args.push:
        git("fetch", "origin", "master")
        m = git("merge", "origin/master", "--no-edit")
        merge_txt = (m.stdout or "").strip().splitlines()[0] if (m.stdout or "").strip() else "(no output)"
        behind = git("rev-list", "--count", "HEAD..origin/master").stdout.strip()
        sha = git("rev-parse", "--short", "origin/master").stdout.strip()
        trailer = ("\n\nR8 (AUTO-GENERATED by scripts/safe_commit.py - this line exists because the command "
                   "ran):\n  git fetch origin master; git merge origin/master -> %s\n"
                   "  origin/master=%s; commits behind after merge=%s\n" % (merge_txt, sha, behind))
        print(a("sync: %s (behind=%s)" % (merge_txt, behind)))

    full = ROOT / "tmp" / "_safe_commit_msg.txt"
    full.write_text(msg.rstrip("\n") + trailer, encoding="utf-8")
    git("commit", "-q", "-F", str(full))
    print(a("committed: %s" % git("log", "--oneline", "-1").stdout.strip()))

    if args.push:
        git("push", "origin", args.push)
        print(a("pushed %s" % args.push))
    return 0


if __name__ == "__main__":
    sys.exit(main())
