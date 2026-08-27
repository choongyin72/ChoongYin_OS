# IUD Task - Deliverable Checklist - Price Rate

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 3) - Price Rate's RF suite was
already converted to the Area pattern and merged via PR #534 (2026-08-26); this checklist
documents the retroactive documentation/evidence bundle added 2026-08-27, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/price_rate.md` already existed (2026-08-02, stale -
      described a multi-level nav cascade) - refreshed this backfill to match PR #534's real
      single-dropdown navigator shape, transcribed from the page object's own Variables/
      Documentation, not re-scanned live.
- [x] **0b.** `grep -ril "price_rate" workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens,testdata}` -> found existing impl at
      `pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource`,
      `tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot`, `py/price_rate_iud.py`,
      and a pre-existing `screens/.../Price_Rate/` bundle (sow.md/README/evidence/investigation
      from the original 2026-08-02 build) - REUSED/EXTENDED, no parallel copy built.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (PR #534 needed only the
      `Apply Navigator From Properties` keyword, already added 2026-08-26 for the batch) - not
      modified by this backfill either.

## A. Bundle artifacts - `screens/Configuration/Assets/Sales_Objects/Price_Rate/`
- [x] **1. `price_rate_sow.md`** - updated (not replaced): classification/nav/grid/cell shape
      corrected (single Business Unit dropdown, not a cascade) and a "Dev story" section added
      with the real PR #534 conversion narrative.
- [x] **2. `README.md`** - updated with exact RF commands (dryrun/live headless/live headed) and
      the `OV_PRICE_RATE` DB self-clean query pattern; clarified RF is the maintained test,
      Playwright is the preserved original reference.
- [x] **3. `JOURNAL.md`** - created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #534's real body, plus this backfill's own honestly-disclosed environment flake.
- [ ] **4. `playwright/ec_iud_<slug>.py`** - N/A, pre-existing/untouched. Playwright bundle waived,
      owner decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). The pre-existing
      `py/price_rate_iud.py` from 2026-08-02 was left untouched - not rebuilt, not re-verified.
- [ ] **5. `investigation/`** - N/A, pre-existing/untouched. Playwright bundle waived, owner
      decision 2026-08-27. The pre-existing `investigation/recon.py` from 2026-08-02 was left
      untouched.
- [x] **6. `evidence/`** - pre-existing screenshots (`prt_0[1-5]_*.png`, `results.json`,
      2026-08-02) kept unchanged; NEW `evidence/backfill_2026-08-27/` added with a fresh dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml` + a screenshot per TC step) of the
      ALREADY-PROVEN Area-pattern suite.
- [x] **7. `CHECKLIST.md`** - this file.

## B. RF files - treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource` - already exists
      (PR #534), unmodified by this backfill; reviewed only for the KB map refresh.
- [x] **9. Suite** `tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot` - already
      exists (PR #534), unmodified by this backfill; TC01 clean -> TC02 insert -> TC03 update ->
      TC04 find -> TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-27)
- [x] **10. robocop clean (parity with Area)** - `py -m robocop check
      pageobjects/.../price_rate_page.resource tests/.../price_rate_iud.robot` (2026-08-27, this
      session) -> **7 issues, 5x `DOC02` (missing test-case documentation, TC01-TC05) + 2x
      `VAR02`**. Cross-checked `py -m robocop check pageobjects/.../area_page.resource
      tests/.../area_iud.robot` (the Area-pattern role model) -> **also 7 issues, same VAR02/DOC02
      pattern**. Price Rate's robocop output is at parity with Area's own established baseline,
      not a new/worse defect - no fix applied, per this task's explicit "do not modify the RF
      automation" scope.
- [x] **11. `--dryrun` N/N PASS** - `py -m robot --dryrun --outputdir
      evidence/backfill_2026-08-27/dryrun tests/Configuration/Assets/Sales_Objects/
      price_rate_iud.robot` -> **5 tests, 5 passed, 0 failed** (2026-08-27, this session; log/
      report/output archived in `evidence/backfill_2026-08-27/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** - `EC_HEADLESS=true py -m robot --outputdir
      evidence/backfill_2026-08-27/live tests/Configuration/Assets/Sales_Objects/
      price_rate_iud.robot` -> **5 tests, 5 passed, 0 failed** (TC01-TC05 all PASS, 2026-08-27,
      this session; archived in `evidence/backfill_2026-08-27/live/` with a screenshot per TC
      step). A real environment flake (stray `chrome-headless-shell.exe`/`node.exe` processes,
      cross-checked as environment-wide via the Area suite failing identically) caused earlier
      attempts to fail before this clean run - disclosed in full in `JOURNAL.md`, not
      smoothed over; resolved by process cleanup, no code change.
- [x] **13. DB ground-truth** - fresh oracledb connection, 2026-08-27, this session (both
      pre-run and post-run): `SELECT COUNT(*) FROM OV_PRICE_RATE WHERE CODE =
      'AUTOTEST_PRICE_RATE'` -> `0`; `SELECT CODE FROM OV_PRICE_RATE WHERE CODE LIKE
      'AUTOTEST%'` -> no rows. Confirms the suite's own TC02/TC03/TC05 insert/update/delete cycle
      against `OV_PRICE_RATE` completed cleanly.
- [x] **14. FULL I-U-D scope** - TC02 Insert + TC03 Update + TC05 Delete all present and PASS
      (see item 12); TC04 Find also present (Area-pattern's 5th TC).
- [x] **15. Self-clean confirmed** - independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_PRICE_RATE` / `AUTOTEST%` rows in `OV_PRICE_RATE` after the live run.
- [x] **16. Hygiene PASS** - `py scripts/check_bundle_hygiene.py` (run from repo root,
      2026-08-27, this session) -> `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure
      ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families`
      (one unrelated WARN about a Contract Area `investigation/` selector-string false positive,
      not related to Price Rate).

## D. Delivery
- [x] **17. Registry row** - already present, MODIFIED IN PLACE by PR #534 (not this backfill);
      confirmed live: `docs/ec_screen_registry.md` line 332, "Price Rate ... CONVERTED
      2026-08-26 to the Area-pattern RF STRUCTURE". This backfill does not touch the registry row
      again (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** - pre-existing from the original build / PR #534
      (`docs/automation-scorecard.md` line 226); not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** - this backfill's own PR (branch `docs/price-rate-backfill-artifacts`), 6-field
      body, base = master, sync-before-push done, never self-merge. (Ticked once the PR is raised
      - see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/price_rate.md` - REFRESHED 2026-08-27 (a
      stale 2026-08-02 version existed, describing a multi-level nav cascade that PR #534's real
      page-object Documentation shows is actually a single dropdown, C:1 only) - transcribed from
      `price_rate_page.resource`'s own Variables/Documentation section, not re-scanned live, per
      the backfill work order's instruction to transcribe, not re-discover.
- [x] **21. Reuse clause** - Step 0 found the screen ALREADY implemented (PR #534); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map refresh
      (#20), plus the SOW/README/CHECKLIST updates this retroactive-backfill scope additionally
      requires.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) - this is not a backfill gap, it is the current
  standing rule for Bank-/Area-pattern work.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill - they already exist
  from PR #534 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 12's first live re-run attempt hit a real, disclosed environment flake (stray browser/node
  processes from this session's earlier work, cross-checked as environment-wide, not a Price Rate
  defect) before a clean 5/5 PASS was captured - see `JOURNAL.md` for the full, undisguised
  account.
