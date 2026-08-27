# IUD Task — Deliverable Checklist — Cost Object Mapping

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 7) — Cost Object Mapping's RF
suite was already converted to the Bank pattern and merged via PR #442 (2026-08-23); this
checklist documents the retroactive documentation/evidence refresh added 2026-08-28, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.** Unlike a brand-new-screen backfill, this screen
already had a `screens/` bundle — but it dated from the SUPERSEDED 2026-06-11 legacy Playwright
build and had never been refreshed for the 2026-08-23 RF conversion; items 1/2 are therefore
REFRESHES of stale content, not first-time creations.

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/cost_object_mapping.md` did not exist before this
      backfill — created fresh (item 20 below), transcribed from
      `cost_object_mapping_page.resource`'s own Variables/Documentation section, not re-scanned
      live.
- [x] **0b.** `grep -ril "cost_object_mapping_page.resource"` ->
      `pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource`,
      `tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot` — REUSED as-is,
      no parallel copy built. A pre-existing `screens/.../Cost_Object_Mapping/` bundle (legacy
      2026-06-11 Playwright build: `cost_object_mapping_sow.md`, `README.md`, `playwright/`,
      `investigation/`, `evidence/*.png`+`results.json`) was found and left untouched EXCEPT for
      `cost_object_mapping_sow.md`/`README.md`, which were refreshed (not deleted) to describe the
      current RF-only implementation instead of the superseded Playwright one.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (no modification).

## A. Bundle artifacts — `screens/Configuration/Assets/Financial_Objects/Cost_Object_Mapping/`
- [x] **1. `cost_object_mapping_sow.md`** — REFRESHED (pre-existing since 2026-06-11, described
      the superseded Playwright build): classification, nav/grid/cell shape (transcribed from
      `cost_object_mapping_page.resource` + registry row line 66), current `AUTOTEST_CMAP` test
      data, real PR #442 conversion dev story pulled from its actual PR body. The prior 1.0
      content is dated and referenced, not silently erased.
- [x] **2. `README.md`** — REFRESHED (pre-existing since 2026-06-11, positioned Playwright as
      primary): now states the RF suite is the current/maintained automation, with exact RF
      commands (dryrun/live headless/live headed) and the `OV_FIN_COST_OBJECT` DB self-clean query
      pattern; the legacy Playwright bundle is explicitly labeled historical reference.
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #442's real body plus the legacy bundle's own real history, not invented. Discloses a real
      robocop rule-breakdown discrepancy found during this backfill (see JOURNAL.md "Done well").
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A for NEW production per owner decision 2026-08-27
      (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, permanent waiver). Note: this screen
      uniquely already has a legacy `playwright/ec_iud_cost_object_mapping.py` from the
      2026-06-11 pre-conversion build — left untouched as historical reference, not extended or
      re-verified by this backfill.
- [ ] **5. `investigation/`** — N/A as a NEW deliverable (waived per Section H); the pre-existing
      legacy `investigation/financial_objects_recon.py` (2026-06-11) was left completely untouched
      (not read for this backfill's own recon — this backfill relied on the current
      `cost_object_mapping_page.resource`'s own Documentation/Variables sections and PR #442's
      body instead, per the workorder's "transcribe, don't re-discover" instruction).
- [x] **6. `evidence/`** — created fresh: `evidence/backfill_2026-08-28/` with a dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml`+per-TC screenshots) of the ALREADY-PROVEN
      Bank-pattern suite, plus `summary.json` with the DB self-clean result, filter-grep count,
      and robocop/hygiene output. The pre-existing legacy `evidence/*.png`+`results.json`
      (2026-06-11) was left untouched alongside it.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource` —
      already exists (PR #442), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot` —
      already exists (PR #442), unmodified by this backfill; TC01 clean -> TC02 insert -> TC03
      update -> TC04 find -> TC05 delete/cleanup, confirmed by re-running it (not by reading
      alone).

## C. Verification gates (real re-run evidence, 2026-08-28)
- [x] **10. robocop** — `py -m robocop check pageobjects/.../cost_object_mapping_page.resource
      tests/.../cost_object_mapping_iud.robot` (2026-08-28, this session) -> **9 issues total**
      (2x `VAR02` + 2x `LEN32` + 5x `DOC02`), matching PR #442's cited total ("9 issues") but not
      its exact per-rule breakdown ("4 VAR02 + 5 DOC02") — disclosed as a likely robocop
      version/ruleset drift in JOURNAL.md, not smoothed over. No fix applied, per this task's
      explicit "do not modify the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun --outputdir
      Workplaces/cost-object-mapping-backfill/dryrun
      tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot` -> **5 tests,
      5 passed, 0 failed** (2026-08-28, this session; log/report/output archived in
      `evidence/backfill_2026-08-28/dryrun/`). One transient msys/bash crash on the very first
      attempt (unrelated to the RF suite), resolved on a single retry per the standing process
      rule.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir
      Workplaces/cost-object-mapping-backfill/live
      tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot` -> **5 tests,
      5 passed, 0 failed** (TC01-TC05 all PASS, first attempt, no retry needed; archived in
      `evidence/backfill_2026-08-28/live/`).
- [x] **13. DB ground-truth** — fresh oracledb connection (throwaway scratch script,
      `Workplaces/cost-object-mapping-backfill/dbcheck.py`, gitignored, not committed), 2026-08-28,
      this session: `SELECT COUNT(*) FROM OV_FIN_COST_OBJECT WHERE CODE = 'AUTOTEST_CMAP'` -> **0**;
      `SELECT CODE, NAME FROM OV_FIN_COST_OBJECT WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME)
      LIKE 'AUTOTEST%'` -> **no rows**; total row count **90** (matches PR #442's original cited
      baseline, unchanged).
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS
      (see item 12); TC04 Find also present (Bank-pattern's 5th TC).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_CMAP` / `AUTOTEST%` rows in `OV_FIN_COST_OBJECT` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-28,
      this session) -> `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about `Contract_Area/investigation/live_recon_contract_area.py`'s selector
      STRINGS, not related to Cost Object Mapping).

## D. Delivery
- [x] **17. Registry row** — already present, added by PR #442 (not this backfill); confirmed
      live: `docs/ec_screen_registry.md` line 66, "Cost Object Mapping ... OV manage-object, live
      5/5 (2026-08-23, Batch 4)". This backfill does not touch the registry row again
      (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from PR #442; not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/cost-object-mapping-backfill-artifacts`),
      6-field body, base = master, sync-before-push done, never self-merge. (Ticked once the PR is
      raised — see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/cost_object_mapping.md` — created
      2026-08-28 (did not exist before), transcribed from `cost_object_mapping_page.resource`'s
      own Variables/Documentation section (nav path, DB view, grid id, insert/update/delete
      selectors, mandatory-yellow fields, quirks), not re-scanned live — per the backfill work
      order's instruction to transcribe, not re-discover.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #442) with a stale
      pre-existing bundle from an even older build; this backfill refreshed the deliverables that
      document the CURRENT implementation: SOW (#1, refreshed), README (#2, refreshed), JOURNAL
      (#3, new), evidence (#6, new folder alongside the legacy one), CHECKLIST (#7, new), KB map
      (#20, new).

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A for NEW production per the
  PERMANENT waiver (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). This screen is a special case
  among the backfill batch: it already has a LEGACY Playwright driver + investigation/ folder from
  before the RF conversion existed. That legacy content was left completely untouched (neither
  re-verified nor extended) — it is historical record, not an active deliverable this backfill is
  required to maintain.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #442 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 10 (robocop) shows a real breakdown discrepancy vs. the original PR's cited numbers (total
  matches, per-rule split does not) — disclosed in JOURNAL.md rather than silently reconciled or
  ignored.
