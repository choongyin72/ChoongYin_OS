# IUD Task — Deliverable Checklist (definition of done)

**Single source of truth for what an EC Object IUD task must deliver.** Both sides use this:
- **Worker:** copy this list into the screen bundle as `CHECKLIST.md`, tick every item with evidence, and raise the PR **only when all items are green**.
- **Reviewer:** verify the PR against this list. **ALL 19 items are HARD GATES** — any missing or failing item ⇒ **MUST-FIX: do NOT approve/merge, leave the PR open, post a note-back listing the exact gaps** (template below), re-review next run.

_Locked 2026-06-28 (owner): all 19 are hard gates — no NICE-TO-HAVE exceptions._

---

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
