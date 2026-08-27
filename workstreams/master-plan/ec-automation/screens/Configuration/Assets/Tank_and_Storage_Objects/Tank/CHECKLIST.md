# IUD Task — Deliverable Checklist — Tank

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 3) — Tank's RF suite was
already built brand-new to the Area pattern and merged via PR #553 (2026-08-26); this checklist
documents the retroactive documentation/evidence bundle added 2026-08-27, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.** Since Tank never had a `screens/` bundle before
(lean new-screen build), items 1/2/3/6/7/20 are all FIRST-TIME creations, not refreshes.

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/tank.md` did not exist before this backfill — created
      fresh (item 20 below), transcribed from `tank_page.resource`'s own Variables/Documentation
      section, not re-scanned live.
- [x] **0b.** `grep -ril "tank_page.resource"` (excluding Chemical Tank) ->
      `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/tank_page.resource`,
      `tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot` — REUSED/EXTENDED, no
      parallel copy built. A pre-existing `screens/.../Tank/investigation/` folder (from PR #553)
      was found and left untouched; no `sow.md`/`README.md`/`JOURNAL.md`/`CHECKLIST.md`/
      `evidence/` existed there before this backfill.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (the `Apply Navigator
      From Properties` keyword already existed from the Area/Well batch) — not modified by this
      backfill.

## A. Bundle artifacts — `screens/Configuration/Assets/Tank_and_Storage_Objects/Tank/`
- [x] **1. `tank_sow.md`** — created (did not exist before): classification, nav/grid/cell shape
      (transcribed from `tank_page.resource` + the registry row), test data, real PR #553
      new-build dev story (not a conversion story — no prior automation existed to convert from).
- [x] **2. `README.md`** — created with exact RF commands (dryrun/live headless/live headed) and
      the `OV_TANK` DB self-clean query pattern; states plainly the RF suite is the ONLY test for
      this screen (no historical Playwright reference exists, unlike converted siblings).
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #553's real body, not invented. Discloses the real stray-process flake hit during this
      backfill's own live-run evidence capture (see JOURNAL.md "Done wrong / lessons").
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A. Playwright bundle waived permanently, owner
      decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). Tank never had one —
      it was built as a lean RF-only new-screen suite from the start; there is nothing to preserve
      or leave untouched here, unlike a converted screen with a historical driver.
- [ ] **5. `investigation/`** — N/A (waived per Section H) as a NEW deliverable of this backfill,
      but note: a pre-existing `investigation/{recon.py,dbcheck_selfclean.py}` folder from PR #553
      already exists at this path and was left completely untouched by this backfill (used
      read-only, e.g. running `dbcheck_selfclean.py` to verify self-clean, never edited).
- [x] **6. `evidence/`** — created fresh: `evidence/backfill_2026-08-27/` with a dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN Area-pattern suite, plus
      `summary.json` with the full flake timeline, DB self-clean result, and hygiene output. No
      original-build `evidence/` folder existed to preserve (lean new-screen build never produced
      one).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/tank_page.resource` — already
      exists (PR #553), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot` — already
      exists (PR #553), unmodified by this backfill; TC01 clean -> TC02 insert -> TC03 update ->
      TC04 find -> TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-27)
- [x] **10. robocop clean (parity with Area)** — `py -m robocop check
      pageobjects/.../tank_page.resource tests/.../tank_iud.robot` (2026-08-27, this session) ->
      **7 issues, 2x `VAR02` (unused variable) + 5x `DOC02` (missing test-case documentation,
      TC01-TC05)**. Cross-checked `py -m robocop check pageobjects/.../area_page.resource
      tests/.../area_iud.robot` (the Area-pattern role model) -> **also 7 issues, same VAR02/DOC02
      pattern**. Tank's robocop output is at parity with Area's own established baseline, not a
      new/worse defect — no fix applied, per this task's explicit "do not modify the RF
      automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun --outputdir tmp_dryrun
      tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot` -> **5 tests, 5 passed,
      0 failed** (2026-08-27, this session; log/report/output archived in
      `evidence/backfill_2026-08-27/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir tmp_live
      tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot` -> **5 tests, 5 passed,
      0 failed** (TC01-TC05 all PASS, 2026-08-27, this session; archived in
      `evidence/backfill_2026-08-27/live/`). Reached after clearing a real stray-process flake
      (4 prior attempts this session failed on process/connection errors caused by
      `chrome-headless-shell.exe`/`node.exe`/`robot.exe` processes left behind by earlier failed
      attempts — see JOURNAL.md; not a Tank suite defect).
- [x] **13. DB ground-truth** — fresh oracledb connection (`investigation/dbcheck_selfclean.py`),
      2026-08-27, this session: `SELECT CODE, NAME FROM OV_TANK WHERE UPPER(CODE) LIKE
      'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%'` -> `1 residual row` (from an earlier partial
      crashed attempt) before cleanup, `0` after running TC05 alone to clean it, and `0` again
      after the final clean 5/5 live run. Confirms the suite's own TC02/TC03/TC05 insert/update/
      delete cycle against `OV_TANK` completed cleanly.
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS
      (see item 12); TC04 Find also present (Area-pattern's 5th TC).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_TANK` / `AUTOTEST%` rows in `OV_TANK` after the final live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root,
      2026-08-27, this session) -> `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about `Contract_Area/investigation/live_recon_contract_area.py`'s selector
      STRINGS, not related to Tank).

## D. Delivery
- [x] **17. Registry row** — already present, added by PR #553 (not this backfill); confirmed
      live: `docs/ec_screen_registry.md` line 357, "Tank ... OV-GM manage-object, live 5/5
      DB-verified ... Area-pattern new-screen build, 2026-08-26". This backfill does not touch the
      registry row again (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from PR #553; not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/tank-backfill-artifacts`), 6-field body,
      base = master, sync-before-push done, never self-merge. (Ticked once the PR is raised — see
      PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/tank.md` — created 2026-08-27 (did not
      exist before), transcribed from `tank_page.resource`'s own Variables/Documentation section
      (nav path, DB view, grid id, insert/update/delete selectors, mandatory-yellow fields,
      quirks), not re-scanned live — per the backfill work order's instruction to transcribe, not
      re-discover. Explicitly disambiguated from Chemical Tank's own KB entry.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #553); this backfill
      produced the deliverables that document it: SOW (#1), README (#2), JOURNAL (#3), evidence
      (#6), CHECKLIST (#7), KB map (#20) — the full first-time bundle this lean new-screen build
      never produced.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). For Tank specifically this is not "waived
  re-verification of an existing driver" (as for converted screens) — it is "never built, and
  correctly not built now," since Tank was a lean new-screen build from day one. The pre-existing
  `investigation/` recon scripts from PR #553 were left untouched (used read-only).
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #553 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
