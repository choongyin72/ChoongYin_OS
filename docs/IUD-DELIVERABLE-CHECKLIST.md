# IUD Task — Deliverable Checklist (definition of done)

**Single source of truth for what an EC Object IUD task must deliver.** Both sides use this:
- **Worker:** copy this list into the screen bundle as `CHECKLIST.md`, tick every item with evidence, and raise the PR **only when all items are green**.
- **Reviewer:** verify the PR against this list. **ALL 19 items are HARD GATES** — any missing or failing item ⇒ **MUST-FIX: do NOT approve/merge, leave the PR open, post a note-back listing the exact gaps** (template below), re-review next run.

_Locked 2026-06-28 (owner): all items are hard gates — no NICE-TO-HAVE exceptions._
_Updated 2026-07-25: added Step 0 (check-existing gate) + items 20–21 (KB MD map, reuse clause) after the
Bank Account gap — a screen had passing tests but was missing its KB map + JOURNAL, so "Done" was declared
too shallow. Count is now 21 hard gates._

---

## Step 0. CHECK-EXISTING-FIRST GATE (before building anything — not optional)
- [ ] **0a.** Read `ec-ui-knowledge/screens/<screen>.md` if it exists (use its selectors; don't re-scan).
- [ ] **0b.** `grep -ril "<screen-slug>" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → **found ⇒ REUSE/EXTEND, never build a parallel copy** (the Bank 3rd-stack mistake). State "existing impl: `<path>` / none" in the plan.
- [ ] **0c.** Prefer the shared engine over new code: `py/ec_object_iud.py` (OV IUD) + `libraries/DbVerify.py` (single DB-verify). A new OV screen = a thin driver (copy `py/bank_iud.py`, swap config), not new plumbing.

## A. Bundle artifacts — `screens/<menu path>/<Screen>/`
- [ ] **1. `<screen>_sow.md`** — SOW: classification (type/pattern), nav/grid/cells, test data, dev story, lessons.
- [ ] **2. `README.md`** — bundle overview + exact run commands.
- [ ] **3. `JOURNAL.md`** — per-branch work journal (built / done-wrong / done-well / improve / blockers→resolution / decisions / evidence).
- [ ] **4. `playwright/ec_iud_<slug>.py`** — standalone Playwright reference flow (env-var creds, ASCII-clean).
- [ ] **5. `investigation/`** — the read-only recon + pre-flight scripts (resolve, scan, DB pre-checks).
- [ ] **6. `evidence/`** — step screenshots + `results.json` from a real run.
- [ ] **7. `CHECKLIST.md`** — this list, copied into the bundle, all items ticked with evidence.

## B. RF files — treeview-mirrored (reuse T1/T2; no shared-file edits unless justified + canaried)
- [ ] **8. T3 page object** `pageobjects/<menu path>/<screen>_page.resource` (locators in Variables; docstring matches Variables — R7).
- [ ] **9. Suite** `tests/<menu path>/<screen>_iud.robot` — TC structure clean → insert → update → delete → cleanup.

## C. Verification gates (record the evidence in CHECKLIST + the PR body)
> **These ticks are NOT hand-typed.** Run `py scripts/verify_screen.py --name … --t3 … --suite … --driver … --out <bundle>/VERIFY-REPORT.md`
> — it RUNS robocop + hygiene + dryrun + live suite + driver and emits the ticks from real exit codes. It must print
> `OVERALL: PASS` before the PR. Ticking a gate the verifier did not pass = hard violation (CLAUDE.md 'NO GUESSING').
- [ ] **10. robocop clean** (the new T3 + suite).
- [ ] **11. `--dryrun` N/N PASS** (suite).
- [ ] **12. LIVE headed run N/N PASS** — the proof (`EC_HEADLESS=false`).
- [ ] **13. DB ground-truth** — the **exact DbVerify assertion** cited, and each op verified at DB level (insert/update/delete).
- [ ] **14. FULL I-U-D scope** — Insert **+ Update +** Delete all present (not I/D only — the RC.0050 lesson).
- [ ] **15. Self-clean confirmed** — independent DB re-read = 0 residual; any pre-existing rows verified intact.
- [ ] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (R16 env-creds, R20 ASCII in `playwright/*.py` + `investigation/*.py`).

## D. Delivery
- [ ] **17. Registry row** appended to `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (append-only, R23).
- [ ] **18. Scorecard row** appended to `docs/automation-scorecard.md` (append-only, R23).
- [ ] **19. PR** with the R9 6-field body (What / Files / DB ground-truth evidence / Self-clean / Rules applied / Base branch); R8 sync first; **never self-merge**.

## E. Knowledge base (added 2026-07-25 — MD-only, tool-agnostic)
- [ ] **20. KB selector map** `ec-ui-knowledge/screens/<screen>.md` — nav path, DB view, grid id, insert/update/delete
      selectors, mandatory-yellow fields, quirks, last-verified date + EC version/env. Serves BOTH Playwright & RF
      (it's the single selector reference; code files cite it). `ec-ui-knowledge/` holds MD only — no code.
- [ ] **21. Reuse clause.** If Step 0 finds the screen ALREADY implemented, a "reuse run" is NOT done at green
      tests alone — it must still produce/refresh the deliverables that document it: **#3 JOURNAL**, **#6 evidence**,
      and **#20 KB map**. "Done" = tests + KB MD + JOURNAL + evidence, never just passing tests.

---

## Reviewer gate (how to enforce)
1. Open the bundle's `CHECKLIST.md` + diff; verify each of the 19 against the artifacts/evidence in the PR.
2. Spot-check the substance (not just the tick): item 12 has a real N/N; item 13's DbVerify assertion is real; item 16 reproduces PASS; items 17/18 are 0-deletion appends (R23).
3. **Any gap ⇒ MUST-FIX, do not merge, post the note-back** (below). Re-review next run after the worker pushes fixes to the same branch.

### Note-back template (reviewer → worker)
> ⛔ **IUD deliverable-checklist gate — MUST-FIX (PR not approved).**
> Missing/failing items vs `docs/IUD-DELIVERABLE-CHECKLIST.md`:
> - [ ] **#N** — `<item>` — `<what's missing / which evidence>`
> - [ ] **#M** — `<item>` — `<...>`
> Complete these, tick them in the bundle `CHECKLIST.md`, and push to this branch. Re-review next run. No code change needed for doc-only gaps.
