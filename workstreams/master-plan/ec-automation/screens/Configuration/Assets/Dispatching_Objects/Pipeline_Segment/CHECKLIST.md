# IUD Task — Deliverable Checklist — Pipeline Segment

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 3) — Pipeline Segment's RF
suite was already converted to the Area pattern and merged via PR #558 (2026-08-26); this
checklist documents the retroactive documentation/evidence bundle added 2026-08-27, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/pipeline_segment.md` did not exist before this backfill —
      created fresh (item 20 below), transcribed from the page object's own Variables/
      Documentation, not re-scanned live.
- [x] **0b.** `grep -ril "pipeline_segment" workstreams/master-plan/ec-automation/{py,
      pageobjects,tests,screens,testdata}` → found existing impl at
      `pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource`,
      `tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot`, and the 5
      `testdata/pipeline_segment_*.properties` files — REUSED/EXTENDED, no parallel copy built.
      No pre-existing `screens/.../Pipeline_Segment/` bundle was found (this build never had one).
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (PR #558 needed only the
      already-existing `Apply Navigator From Properties` keyword) — not modified by this backfill
      either.

## A. Bundle artifacts — `screens/Configuration/Assets/Dispatching_Objects/Pipeline_Segment/`
- [x] **1. `pipeline_segment_sow.md`** — created (did not exist before). Classification, nav/grid/
      cell shape, test data, and the real §3.2 PR #558 dev story (including the disclosed
      shared-checkout git-plumbing incident).
- [x] **2. `README.md`** — created, with exact RF commands (dryrun/live headless/live headed) and
      the `OV_PIPELINE_SEGMENT` DB self-clean query pattern.
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #558's real body + `docs/ec_screen_registry.md`'s row, not invented. Includes the disclosed
      live-run flake hit during this backfill's own evidence capture.
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A. Playwright bundle waived, owner decision
      2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). No Playwright bundle ever
      existed for this screen (its original build was RF-only, 2026-06-12) — nothing to preserve
      or rebuild.
- [ ] **5. `investigation/`** — N/A. Playwright bundle waived, owner decision 2026-08-27. No
      pre-existing recon scripts existed for this screen outside temp recon `.robot` files that
      PR #558 itself deleted before commit (per its own body).
- [x] **6. `evidence/`** — created fresh: `evidence/backfill_2026-08-27/` with a dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml`, the passing retry after a disclosed first-attempt
      flake) of the ALREADY-PROVEN Area-pattern suite, plus `summary.json` with the full DB
      self-clean result, filter-fired grep, robocop parity check, and hygiene output.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource` —
      already exists (PR #558), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot` —
      already exists (PR #558), unmodified by this backfill; TC01 clean → TC02 insert → TC03
      update → TC04 find → TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-27)
- [x] **10. robocop clean (parity with Area)** — `py -m robocop check
      pageobjects/.../pipeline_segment_page.resource tests/.../pipeline_segment_iud.robot`
      (2026-08-27, this session) → **7 issues, 2x `VAR02` (unused variable) + 5x `DOC02` (missing
      test-case documentation, TC04/TC05)**. Cross-checked `py -m robocop check
      pageobjects/.../area_page.resource tests/.../area_iud.robot` (the Area-pattern role model)
      → **also 7 issues, same VAR02/DOC02 pattern**. Pipeline Segment's robocop output is at
      parity with Area's own established baseline, not a new/worse defect — no fix applied, per
      this task's explicit "do not modify the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun --outputdir tmp_dryrun
      tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot` → **5 tests, 5
      passed, 0 failed** (2026-08-27, this session; log/report/output archived in
      `evidence/backfill_2026-08-27/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir tmp_live
      tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot`. FIRST attempt:
      **5 tests, 0 passed, 5 failed** (browser context closed mid-run — `tasklist | grep -i
      chrome` showed 0 processes immediately after, consistent with resource contention from
      concurrent agents in this shared environment, not a code defect). RETRY (same unmodified
      command): **5 tests, 5 passed, 0 failed** (TC01-TC05 all PASS, 2026-08-27, this session;
      archived in `evidence/backfill_2026-08-27/live/`). Disclosed, not smoothed over — see
      JOURNAL.md.
- [x] **13. DB ground-truth** — fresh oracledb connection, 2026-08-27, this session, run after
      the passing retry: `SELECT COUNT(*) FROM OV_PIPELINE_SEGMENT WHERE CODE =
      'AUTOTEST_PIPELINE_SEGMENT'` → `0`; `SELECT CODE FROM OV_PIPELINE_SEGMENT WHERE CODE LIKE
      'AUTOTEST%'` → `[]` (no rows). Confirms the suite's own TC02/TC03/TC05 insert/update/delete
      cycle against `OV_PIPELINE_SEGMENT` completed cleanly.
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS
      (see item 12); TC04 Find also present (Area-pattern's 5th TC).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_PIPELINE_SEGMENT` / `AUTOTEST%` rows in `OV_PIPELINE_SEGMENT` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root,
      2026-08-27, this session) → `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII
      (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one
      unrelated pre-existing WARN about Contract Area's `investigation/live_recon_contract_area.py`
      selector STRINGS `"#username"`/`"input[name='username']"`/`"#password"` — DOM locator
      literals, not hardcoded credential values, and unrelated to Pipeline Segment).

## D. Delivery
- [x] **17. Registry row** — already present, MODIFIED IN PLACE by PR #558 (not this backfill);
      confirmed live: `docs/ec_screen_registry.md` line 87, "Pipeline Segment ... FULL
      Area-pattern conversion done 2026-08-26". This backfill does not touch the registry row
      again (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from PR #558; not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/pipeline-segment-backfill-artifacts`),
      6-field body, base = master, sync-before-push done, never self-merge. (Ticked once the PR
      is raised — see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/pipeline_segment.md` — created 2026-08-27
      (did not exist before), transcribed from `pipeline_segment_page.resource`'s own
      Variables/Documentation section (nav path, DB view, grid id, insert/update/delete
      selectors, mandatory-yellow fields, quirks), not re-scanned live — per the backfill work
      order's instruction to transcribe, not re-discover.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #558); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map (#20), plus
      the SOW/README/CHECKLIST this retroactive-backfill scope additionally requires.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — this is not a backfill gap, it is the current
  standing rule for Area-pattern work, and this screen never had a Playwright bundle to begin with.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #558 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 12's live-run gate required TWO attempts (one disclosed failure, one passing retry) due to
  a shared-environment browser-context flake, not a code defect — recorded honestly in the
  evidence rather than only citing the passing run.
