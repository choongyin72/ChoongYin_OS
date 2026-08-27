# IUD Task — Deliverable Checklist — Sub Area

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`) — Sub Area's RF suite was already
converted to the Area pattern and merged via PR #538 (2026-08-26); this checklist documents the
retroactive documentation/evidence bundle added 2026-08-27, plus a fresh dryrun+live
evidence-capture re-run of the already-proven suite. **No automation code was rebuilt, modified,
or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/sub_area.md` did not exist before this backfill — created
      fresh (item 20 below), transcribed from the page object's own Variables/Documentation, not
      re-scanned live.
- [x] **0b.** `grep -ril "sub_area" workstreams/master-plan/ec-automation/{pageobjects,tests,screens,testdata}`
      → found existing impl at `pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource`,
      `tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot`, and a pre-existing
      `screens/.../Sub_Area/` bundle (sow.md/README/evidence/investigation/playwright from the
      original 2026-06-11 build) — REUSED/EXTENDED, no parallel copy built.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (PR #538 confirmed no gap
      found for Sub Area's cascade) — not modified by this backfill either.

## A. Bundle artifacts — `screens/Configuration/Assets/Basic_Objects/Sub_Area/`
- [x] **1. `sub_area_sow.md`** — updated (not replaced): §2 classification/nav/grid/cell shape was
      already correct and left as-is; §3.2 added with the real PR #538 dev story; §4/§5 updated
      with the Area-pattern 5-TC results and this backfill's re-run.
- [x] **2. `README.md`** — updated with exact RF commands (dryrun/live headless/live headed) and
      the `OV_SUB_AREA` DB self-clean query pattern; clarified RF is the maintained test, Playwright
      is the preserved original reference.
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #538's real body (see JOURNAL.md's own citations).
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A. Playwright bundle waived, owner decision
      2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). The pre-existing
      `playwright/ec_iud_sub_area.py` from 2026-06-11 was left untouched — not rebuilt, not
      re-verified.
- [ ] **5. `investigation/`** — N/A. Playwright bundle waived, owner decision 2026-08-27. The
      pre-existing `investigation/` recon scripts from 2026-06-11 were left untouched.
- [x] **6. `evidence/`** — pre-existing screenshots (`sub_area_0[1-8]_*.png`,
      `sub_area_results.json`, 2026-06-11) kept unchanged; NEW `evidence/backfill_2026-08-27/`
      added with a fresh dryrun (`dryrun/log.html`+`report.html`+`output.xml`) and live headless
      run (`live/log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN Area-pattern suite,
      plus `summary.json` with the DB self-clean result and hygiene output.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource`
      — already exists (PR #538), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot` — already exists
      (PR #538), unmodified by this backfill; TC01 clean → TC02 insert → TC03 update → TC04 find →
      TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-27)
- [x] **10. robocop clean (parity with Area)** — `py -m robocop check
      pageobjects/.../sub_area_page.resource tests/.../sub_area_iud.robot` (2026-08-27, this
      session) → **7 issues, all `DOC02` "Missing documentation" on TC01-TC05 test cases**.
      Cross-checked `py -m robocop check tests/.../area_iud.robot` (the Area-pattern role model) →
      **also 7 issues, same `DOC02` pattern on its own TC01-TC05**. Sub Area's robocop output is at
      parity with Area's own established baseline, not a new/worse defect — no fix applied, per
      this task's explicit "do not modify the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun --outputdir tmp_dryrun
      tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot` → **5 tests, 5 passed, 0
      failed** (2026-08-27, this session; log/report/output archived in
      `evidence/backfill_2026-08-27/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir tmp_live
      tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot` → **5 tests, 5 passed, 0
      failed** (TC01-TC05 all PASS, 2026-08-27, this session; archived in
      `evidence/backfill_2026-08-27/live/`).
- [x] **13. DB ground-truth** — fresh oracledb connection, 2026-08-27, this session:
      `SELECT COUNT(*) FROM OV_SUB_AREA WHERE CODE = 'AUTOTEST_SUB_AREA'` → `0`;
      `SELECT CODE FROM OV_SUB_AREA WHERE CODE LIKE 'AUTOTEST%'` → `[]` (no rows). Confirms the
      suite's own TC02/TC03/TC05 insert/update/delete cycle against `OV_SUB_AREA` completed
      cleanly (the suite's `Verify Object Removed` T2 keyword does the per-op DB assertion inside
      TC05; this is the independent post-run re-check).
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS (see
      item 12); TC04 Find also present (Area-pattern's 5th TC).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_SUB_AREA` / `AUTOTEST%` rows in `OV_SUB_AREA` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-27,
      this session) → `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated WARN
      about a different screen's `investigation/` script, not Sub Area).

## D. Delivery
- [x] **17. Registry row** — already present, MODIFIED IN PLACE by PR #538 (not this backfill);
      confirmed live: `docs/ec_screen_registry.md` line 51, "Sub Area ... converted to the
      Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (2026-08-26 ...)". This backfill
      does not touch the registry row again (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from the original build / PR #538; not duplicated by
      this backfill (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/sub-area-backfill-artifacts`), 6-field body,
      base = master, sync-before-push done, never self-merge. (Ticked once the PR is raised — see
      PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/sub_area.md` — created 2026-08-27 (did not
      exist before), transcribed from `sub_area_page.resource`'s own Variables/Documentation
      section (nav path, DB view, grid id, insert/update/delete selectors, mandatory-yellow
      fields, quirks), not re-scanned live — per the backfill work order's instruction to
      transcribe, not re-discover.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #538); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map (#20), plus
      the SOW/README/CHECKLIST updates the work order additionally requires for this
      retroactive-backfill scope.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — this is not a backfill gap, it is the current
  standing rule for Bank-/Area-pattern work.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #538 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
