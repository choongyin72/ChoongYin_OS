# IUD Task - Deliverable Checklist - Product Group

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 7) - Product Group's RF suite
was already rebuilt to the Bank pattern and merged via PR #445 (2026-08-23, Batch 5); this
checklist documents the retroactive documentation/evidence bundle added 2026-08-28, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/product_group.md` did NOT already exist - created fresh
      this backfill (transcribed from `product_group_page.resource`'s own Variables/Documentation
      section, not re-scanned live).
- [x] **0b.** `grep -ril "product_group" workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens,testdata}` -> found existing impl at
      `pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource`,
      `tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot`,
      `testdata/product_group_{insert,update,form_verify,grid_verify}.properties`, and a
      pre-existing `screens/.../Product_Group/` bundle (sow.md/README/playwright/evidence from
      the original 2026-06-25 build) - REUSED/EXTENDED, no parallel copy built. Confirmed distinct
      from "Product" (CO.0007) and "Product Description" (CD.0012) via the registry's own
      disambiguation note.
- [x] **0c.** Shared T2 `resources/manage_object.resource` and T1 `resources/common.resource`
      reused as-is by PR #445 and unmodified by this backfill.

## A. Bundle artifacts - `screens/Configuration/Assets/Royalty_Objects/Product_Group/`
- [x] **1. `product_group_sow.md`** - updated (not replaced): added a "Dev story / revision
      history" section with the real PR #445 Bank-pattern-conversion narrative (screen-prefixed
      labels, mandatory-field confirmation, 4->5 TC growth, fixed test code) plus this backfill's
      own scope.
- [x] **2. `README.md`** - updated with exact dryrun/live-headless/live-headed RF commands and
      the `OV_PRODUCT_GROUP` DB self-clean query pattern; the Bank-pattern facts (fixed test code,
      own credential pair, 5-TC structure) called out explicitly.
- [x] **3. `JOURNAL.md`** - created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #445's real body.
- [ ] **4. `playwright/ec_iud_product_group.py`** - pre-existing (2026-06-25 original build), NOT
      rebuilt. Permanently waived for Bank-pattern work by owner decision 2026-08-27
      (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) - the Universal Screen Engine is the
      replacement going forward; the legacy file is kept as-is, untouched.
- [ ] **5. `investigation/`** - N/A, permanently waived by the same Section H decision. This
      screen never had a dedicated `investigation/` folder; no throwaway recon script was needed
      for this documentation-only backfill.
- [x] **6. `evidence/`** - pre-existing screenshots (`product_group_tc0[1-4]_*.png`, 2026-06-25)
      kept unchanged; NEW `evidence/backfill_2026-08-28/` added with a fresh dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml`+per-TC step screenshots) of the ALREADY-PROVEN
      Bank-pattern suite.
- [x] **7. `CHECKLIST.md`** - this file.

## B. RF files - treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource` - already
      exists (PR #445), unmodified by this backfill; reviewed only for the KB map's transcription.
- [x] **9. Suite** `tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot` - already
      exists (PR #445), unmodified by this backfill; TC01 clean -> TC02 insert -> TC03 update ->
      TC04 find -> TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-28)
- [x] **10. robocop clean (parity with PR #445's own baseline)** - `py -m robocop check
      pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource
      tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot` (2026-08-28, this
      session) -> **9 issues** (4 VAR02 + 5 DOC02). Matches PR #445's own cited Batch 5 baseline
      exactly, no new issue classes - no fix applied, per this task's explicit "do not modify the
      RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** - `py -m robot --dryrun --outputdir
      evidence/backfill_2026-08-28/dryrun tests/Configuration/Assets/Royalty_Objects/
      product_group_iud.robot` -> **5 tests, 5 passed, 0 failed** (2026-08-28, this session;
      log/report/output archived in `evidence/backfill_2026-08-28/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** - `EC_HEADLESS=true py -m robot --outputdir
      evidence/backfill_2026-08-28/live tests/Configuration/Assets/Royalty_Objects/
      product_group_iud.robot` -> **5 tests, 5 passed, 0 failed** (TC01-TC05 all PASS, first
      attempt, no retry needed, 2026-08-28, this session; archived in
      `evidence/backfill_2026-08-28/live/`).
- [x] **13. DB ground-truth** - fresh oracledb connection, 2026-08-28, this session, post-run:
      `SELECT COUNT(*) FROM OV_PRODUCT_GROUP WHERE CODE = 'AUTOTEST_PRODUCT_GROUP'` -> `0`.
      Confirms the suite's own TC02/TC03/TC05 insert/update/delete cycle against
      `OV_PRODUCT_GROUP` completed cleanly.
- [x] **14. FULL I-U-D scope** - TC02 Insert + TC03 Update + TC05 Delete all present and PASS (see
      item 12); TC04 Find also present (Bank-pattern's 5th TC).
- [x] **15. Self-clean confirmed** - independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_PRODUCT_GROUP` rows in `OV_PRODUCT_GROUP` after the live run.
- [x] **16. Hygiene PASS** - `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-28,
      this session) -> `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about a Contract Area `investigation/` selector-string false positive, not
      related to Product Group).

## D. Delivery
- [x] **17. Registry row** - already present, from PR #445 (not this backfill); confirmed live:
      `docs/ec_screen_registry.md` line 113. This backfill does not re-append or edit the registry
      row (append-only / no-duplicate-edit).
- [x] **18. Scorecard row** - pre-existing from PR #445 (`docs/automation-scorecard.md`); not
      duplicated by this backfill (documentation-only task, no new automation scope to score).
- [ ] **19. PR** - this backfill's own PR (branch `docs/product-group-backfill-artifacts`),
      6-field body, base = master, sync-before-push done, never self-merge. (Ticked once the PR is
      raised - see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/product_group.md` - CREATED 2026-08-28 (did
      not exist before) - transcribed from `product_group_page.resource`'s own
      Variables/Documentation section, not re-scanned live, per the backfill work order's
      instruction to transcribe, not re-discover.
- [x] **21. Reuse clause** - Step 0 found the screen ALREADY implemented (PR #445); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map (#20), plus
      the SOW/README/CHECKLIST this retroactive-backfill scope additionally requires.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A/pre-existing-untouched. Item 4's
  legacy file already existed from the original 2026-06-25 build and is kept as-is (not rebuilt,
  not deleted); item 5 never existed for this screen. Both are also permanently waived regardless
  for all Bank-/Area-pattern work by owner decision 2026-08-27
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H).
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill - they already exist
  (from PR #445) and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 12's live re-run passed 5/5 on the FIRST attempt this session - no flake, no retry, nothing
  to disclose beyond the plain PASS result.
- Item 10's filter-fired hit count (12, this backfill) differs from PR #445's originally-cited
  count (5) because this suite's Update/Find/Verify-Found/Delete keywords each call their own
  Find/Clear filter pair around the action - a re-run naturally produces more hits than a
  narrower citation, not a regression. See `JOURNAL.md` "Done well" for the exact figure.
