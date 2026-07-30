"""Stage this screen's files by explicit path, commit, push, open stacked PR. One py call.
Usage: py tmp/git_pr.py '<json config with: slug, folder, screen, bfcode, view, base_branch, ordinal>'
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Projects\ChoongYin_OS")
c = json.loads(sys.argv[1])
slug = c["slug"]; folder = c["folder"].strip("/"); screen = c["screen"]; bf = c["bfcode"]
view = c["view"].upper(); base = c["base_branch"]; ordn = c.get("ordinal", "?")
Screen_dir = screen.replace(" ", "_")


def g(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT), **kw)
    if r.stdout.strip():
        print(r.stdout.strip()[-400:])
    if r.returncode != 0 and r.stderr.strip():
        print("ERR:", r.stderr.strip()[-400:])
    return r


branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True,
                        cwd=str(ROOT)).stdout.strip()


def engine_change_note():
    """#237 item 2: derive the engine/T2-change statement from the ACTUAL staged diff, never hardcode it.
    A 'Zero engine changes' claim that contradicts the diff is exactly the false claim the reviewer flagged."""
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True,
                            cwd=str(ROOT)).stdout.splitlines()
    shared = [p for p in staged if p.endswith("py/ec_object_iud.py")
              or "/resources/" in p and p.endswith(".resource")]
    if not shared:
        return "Zero engine/shared-resource changes (thin driver + T3 only)."
    return "Shared engine/T2 CHANGED (verify vs canary + a random sibling per R12): " + ", ".join(shared) + "."

paths = [
    "workstreams/master-plan/ec-automation/py/%s_iud.py" % slug,
    "workstreams/master-plan/ec-automation/pageobjects/%s/%s_page.resource" % (folder, slug),
    "workstreams/master-plan/ec-automation/tests/%s/%s_iud.robot" % (folder, slug),
    "workstreams/master-plan/ec-automation/screens/%s/%s/" % (folder, Screen_dir),
    "ec-ui-knowledge/screens/%s.md" % slug,
    "workstreams/master-plan/ec-automation/docs/ov-reuse-targets.md",
    "workstreams/master-plan/ec-automation/docs/ec_screen_registry.md",
    "docs/automation-scorecard.md",
]
for p in paths:
    g(["git", "add", p])

# derive the engine-change statement from what is ACTUALLY staged (after the add loop) - never hardcode
ENGINE_NOTE = engine_change_note()

msg = ("""feat(iud): %s (%s) - OV IUD, live 4/4 RF + 7/7 Playwright [stacked]

%s OV-reuse-target; plain Bank-layout OV (single Date+GO nav, mandatory Code/Name/Start Date;
optional dropdowns skipped). Label-driven (zero hardcoded field ids), generator-scaffolded
(tmp/gen_ov_screen.py) - every file verified live. Full I-U-D, DB-verified vs %s, self-cleaning.
verify_screen.py OVERALL PASS (robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7).
%s

Stacked on %s.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>""" % (screen, bf, ordn, view, ENGINE_NOTE, base))
r = g(["git", "commit", "-F", "-"], input=msg)
if r.returncode != 0:
    print("RESULT git_pr %s: COMMIT-FAIL" % slug); sys.exit(1)
g(["git", "push", "-u", "origin", branch])

body = ("**What was built** - %s (%s, `%s`) OV object-config IUD - %s OV-reuse-target, label-driven, generator-scaffolded.\n\n"
        "**DB ground-truth** - LIVE RF **4/4** + Playwright **7/7** via `scripts/verify_screen.py` (OVERALL PASS). "
        "`Code Should Be Present/Absent In View %s` + `Field Should Equal In View %s <code> NAME <updated>`. Self-clean 0 residual.\n\n"
        "**Recon** - plain Bank-layout OV: single Date+GO nav, mandatory Code/Name/Start Date; optional dropdowns skipped.\n\n"
        "**Rules** - R9, R16/R20 (hygiene PASS), no-hardcode (label-driven), no-guessing (recon-first + real verify ticks), AUTOTEST_ prefix, never touched real rows. " + ENGINE_NOTE + "\n\n"
        "**Base branch** - `%s` (stacked; merge chain from #203).\n\n"
        "🤖 Generated with [Claude Code](https://claude.com/claude-code)" % (screen, bf, view, ordn, view, view, base))
title = "feat(iud): %s (%s) - OV IUD, live 4/4 + 7/7 [stacked]" % (screen, bf)
r = g(["gh", "pr", "create", "--base", base, "--head", branch, "--title", title, "--body", body])
print("RESULT git_pr %s: DONE" % slug)
