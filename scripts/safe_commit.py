#!/usr/bin/env python3
"""Mechanical enforcement of the git rules I broke by relying on attention (2026-07-31, then
2026-08-16 - Issue #385 item 1).

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

 4. HYGIENE GATE, MECHANIZED (Issue #385 item 1). If ANY staged path ends in `.py`, this script RUNS
    `scripts/check_bundle_hygiene.py` itself and aborts (unstages, exits 1) on a non-zero exit - never a
    prose reminder to "remember to run hygiene". Origin: PR #382's own note said the #357 R16 slip "was a
    habit gap... the habit itself has no code fix" - true only until the habit is wired into tooling.

 5. ENGINE CANARY GATE, MECHANIZED (Issue #385 item 1). If any staged path is
    `workstreams/master-plan/ec-automation/py/engine.py` or `.../universal_classifier.py`, this script
    RUNS `py/engine_canary.py` itself (headless) and aborts on a non-zero exit or non-"ALL PASS" output -
    a change to the shared engine cannot be committed without a fresh, real regression proof, not a
    remembered "I ran it earlier".

 6. SCOPE/FILES-TOUCHED REGENERATED ON EVERY PUSH, MECHANIZED (Issue #424). A PR body's "Scope / Files
    touched" list is written by hand once, at PR-creation time, and prose does not survive a branch that
    keeps growing - PR #423 started as 1 commit/1 file and merged at 5 commits/16 files with a body that
    still described commit 1. With --push, after a successful push this script prints the CURRENT
    full-branch file list (diffed against `merge-base origin/master HEAD`) as a ready-to-paste "## Scope /
    Files touched" block, loudly flags any file NEW since the previous push to this branch (comparing
    against the branch's previous origin ref, captured before this push), and - if an open PR already
    exists for this branch (via `gh pr view`) - diffs the emitted list against the PR body's own file
    list and warns (never aborts) on any mismatch. This is a print-only reporting gate, not a commit
    blocker: the fix isn't code correctness, it's making sure the human reading the PR isn't fed a stale
    summary of what actually shipped.

Prints the staged set BEFORE committing - the check that catches a mistake must precede the irreversible
step, not follow it (I caught the add -u accident with `git show --stat` afterwards).
"""
import argparse
import json
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


def diff_name_status(base, head):
    """Lines of `git diff --name-status base...head`, empty list if the ref pair is bad."""
    r = git("diff", "--name-status", "%s...%s" % (base, head), check=False)
    return [l for l in (r.stdout or "").splitlines() if l.strip()]


def paths_from_name_status(lines):
    """Extract the touched file path from each name-status line (renames/copies: use the NEW path)."""
    paths = set()
    for l in lines:
        parts = l.split("\t")
        if len(parts) >= 2:
            paths.add(parts[-1])
    return paths


def emit_scope_report(branch, old_remote_sha):
    """Issue #424: after a successful push, print the CURRENT full-branch Scope/Files-touched block
    (a PR body written once at creation goes stale as the branch grows - PR #423 merged at 5 commits/
    16 files with a body still describing commit 1), flag any file NEW since the previous push to this
    branch, and - if an open PR already exists for this branch - warn (never abort) on any file the PR
    body doesn't mention. ${old_remote_sha} must be captured BEFORE this push runs (empty string if this
    branch has no prior remote ref, i.e. this is its first push)."""
    merge_base_new = git("merge-base", "origin/master", "HEAD", check=False).stdout.strip()
    if not merge_base_new:
        print(a("\n[Issue #424] skipped scope report - HEAD has no merge-base with origin/master"))
        return
    new_lines = diff_name_status(merge_base_new, "HEAD")
    new_paths = paths_from_name_status(new_lines)

    print(a("\n## Scope / Files touched (regenerated for %s - Issue #424, paste into the PR body)" % branch))
    if new_lines:
        for l in sorted(new_lines):
            print(a("   %s" % l))
    else:
        print(a("   (no diff vs origin/master?)"))

    if old_remote_sha:
        merge_base_old = git("merge-base", "origin/master", old_remote_sha, check=False).stdout.strip()
        old_paths = paths_from_name_status(diff_name_status(merge_base_old, old_remote_sha)) \
            if merge_base_old else set()
        grown = sorted(new_paths - old_paths)
        if grown:
            print(a("\n[!!] FILE LIST GREW SINCE THE LAST PUSH TO %s - the PR body is now STALE unless "
                     "you refresh its Scope/Files-touched section:" % branch))
            for g in grown:
                print(a("   + %s" % g))
    else:
        print(a("   (first push of this branch - nothing to compare growth against)"))

    # Optional stronger form: cross-check against an ALREADY-OPEN PR's own body. Best-effort - a missing
    # PR, unauthenticated gh, or a network hiccup is silently skipped, never a reason to fail the push.
    try:
        pr = subprocess.run(["gh", "pr", "view", branch, "--json", "number,url,body"],
                            cwd=str(ROOT), capture_output=True, text=True)
    except OSError:
        # gh binary not installed on this machine at all - same best-effort contract as an
        # unauthenticated gh or missing PR: skip silently, never fail the push (reviewer
        # hand-fix at merge of PR #425: subprocess.run raises FileNotFoundError for a missing
        # executable, which the returncode!=0 check below never sees).
        return
    if pr.returncode == 0 and (pr.stdout or "").strip():
        try:
            data = json.loads(pr.stdout)
        except ValueError:
            data = None
        if data:
            body = data.get("body") or ""
            missing_from_body = sorted(p for p in new_paths if p not in body)
            if missing_from_body:
                print(a("\n[!!] open PR #%s (%s) body does not mention %d touched file(s) - update the "
                         "PR description's Scope/Files-touched section:"
                         % (data.get("number"), data.get("url"), len(missing_from_body))))
                for m in missing_from_body:
                    print(a("   ? %s" % m))


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

    # ---- 2. hygiene + engine-canary gates, MECHANIZED (Issue #385 item 1) -------------------------
    if any(s.endswith(".py") for s in staged):
        print(a("\n[gate] .py file(s) staged - running scripts/check_bundle_hygiene.py ..."))
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_bundle_hygiene.py")],
                           cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(a((r.stdout or "") + (r.stderr or "")))
        if r.returncode != 0:
            print(a("ABORT: check_bundle_hygiene.py FAILED (exit=%d) - fix the reported issue(s), "
                     "then re-run. Not a prose reminder - this gate runs the tool itself." % r.returncode))
            git("reset", "-q")
            return 1

    _ENGINE_FILES = ("workstreams/master-plan/ec-automation/py/engine.py",
                      "workstreams/master-plan/ec-automation/py/universal_classifier.py")
    if any(s in _ENGINE_FILES for s in staged):
        canary = ROOT / "workstreams" / "master-plan" / "ec-automation" / "py" / "engine_canary.py"
        print(a("\n[gate] engine.py/universal_classifier.py staged - running %s (headless) ..." % canary))
        r = subprocess.run([sys.executable, "-X", "utf8", str(canary)],
                           cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**__import__("os").environ, "EC_HEADED": "0"})
        print(a((r.stdout or "") + (r.stderr or "")))
        if r.returncode != 0 or "ALL PASS" not in (r.stdout or ""):
            print(a("ABORT: engine_canary.py did not report ALL PASS (exit=%d) - a change to the shared "
                     "engine cannot be committed without a fresh, real regression proof." % r.returncode))
            git("reset", "-q")
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
        # capture the branch's PRE-push remote state before it moves, so emit_scope_report can tell
        # whether the file list grew (Issue #424) - a failed fetch just means no prior remote ref yet.
        git("fetch", "origin", args.push, check=False)
        _old_ref = git("rev-parse", "origin/%s" % args.push, check=False)
        # `git rev-parse` on a ref that doesn't exist yet ECHOES THE ARGUMENT ITSELF to stdout (not
        # empty) while the real error goes to stderr with returncode!=0 - trusting stdout truthiness
        # alone made a genuinely-first-ever push look like it had a prior remote ref (found live while
        # exercising this fix, Issue #424's own verification step catching a real bug).
        old_remote_sha = _old_ref.stdout.strip() if _old_ref.returncode == 0 else ""
        git("push", "origin", args.push)
        print(a("pushed %s" % args.push))
        emit_scope_report(args.push, old_remote_sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
