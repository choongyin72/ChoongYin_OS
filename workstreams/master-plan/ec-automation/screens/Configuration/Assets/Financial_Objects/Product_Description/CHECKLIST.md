# IUD Task — Deliverable Checklist — Product Description

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PR #441, merged 2026-08-23). No RF file
(`product_description_page.resource`, `product_description_iud.robot`,
`testdata/product_description_*.properties`) was modified to produce this checklist. Items 4/5
(Playwright driver + investigation/) stay permanently waived per Section H — the pre-existing
Playwright bundle from the screen's original 2026-06-11 build is kept in this bundle unchanged,
not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/product_description.md` did not exist before this
      backfill — created in this PR, transcribed from `product_description_page.resource`'s own
      Variables section, not re-scanned live.
- [x] **0b.** `grep -ril product_description workstreams/master-plan/ec-automation/{py,pageobjects,
      tests,screens}` → existing impl found:
      `pageobjects/Configuration/Assets/Financial_Objects/product_description_page.resource`,
      `tests/Configuration/Assets/Financial_Objects/product_description_iud.robot`,
      `playwright/ec_iud_product_description.py`,
      `screens/Configuration/Assets/Financial_Objects/Product_Description/` (SOW/README/
      evidence/investigation/playwright pre-existed from the 2026-06-11 build). REUSED/EXTENDED —
      no parallel copy built, and confirmed distinct from "Product" (CO.0007, class PRODUCT) and
      "Product Group" (RC.0053) via the registry row + PR #441's own body.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Find/Clear Object Row By Filter`) + `libraries/
      DbVerify.py` for this backfill's own evidence-capture DB reads. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Financial_Objects/Product_Description/`
- [x] **1. `product_description_sow.md`** — updated with a Section 0 addendum documenting the
      2026-08-23 Bank-pattern conversion (nav/grid/cell shape, test data, dev story pulled from
      PR #441's body), layered on top of the original 2026-06-11 build's own Sections 1-6.
- [x] **2. `README.md`** — rewritten with the bundle overview + exact run commands (dryrun/live/
      DB self-clean pattern) for the RF suite, alongside the pre-existing Playwright commands;
      disambiguated from Product/Product Group.
- [x] **3. `JOURNAL.md`** — created: PR #441's Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence sections, pulled from the PR body + this session's
      own live-run evidence; the original 2026-06-11 entry is included unchanged above it.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27
      (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing
      `playwright/ec_iud_product_description.py` from the 2026-06-11 build is kept unchanged, not
      rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing
      `investigation/financial_objects_recon.py` from the 2026-06-11 build is kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html`,
      per-TC step screenshots (`TC01..TC05_*.png`) from a live 5/5 RF run (2026-08-28), alongside
      the pre-existing 2026-06-11 Playwright evidence (`product_description_0[1-8]_*.png`,
      `product_description_results.json`, unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Financial_Objects/product_description_page.resource` —
      pre-existing, merged in PR #441 (Bank-pattern conversion), not touched by this backfill.
- [x] **9. Suite**
      `tests/Configuration/Assets/Financial_Objects/product_description_iud.robot` —
      pre-existing, merged in PR #441, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../
      product_description_page.resource tests/.../product_description_iud.robot` (this session,
      2026-08-28) → **9 issues** (4 VAR02 + 5 DOC02) — exact parity with PR #441's own cited
      count. No drift, no new issue category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/
      Financial_Objects/product_description_iud.robot` (this session) → **5/5 PASS**.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Financial_Objects/Product_Description/evidence
      tests/.../product_description_iud.robot` (this session) → **5/5 PASS** clean, first
      attempt (no flake, no retry needed).
- [x] **13. DB ground-truth** — `libraries.DbVerify.fetch_object("OV_PRODUCT_NODE_ITEM",
      "AUTOTEST_PD")` → `None` (absent), confirmed via a fresh oracledb connection BOTH before
      AND after the live run in this session.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Clean State, TC04 Find) — confirmed by reading `product_description_iud.robot`'s
      5 test cases and by this session's live 5/5 run.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_PD` rows in `OV_PRODUCT_NODE_ITEM` after the clean run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families` (167 bundles + 272 recon
      scripts scanned; the one WARN reported belongs to Contract Area's `investigation/`,
      unrelated to this screen).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Product Description's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (line 60) already
      exists and already documents the PR #441 conversion (edited in place at merge time of that
      PR, not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Product Description row already reflects the merged
      conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/product_description.md` — created in this
      backfill: nav path, DB view, grid id, insert/update/delete selectors (transcribed from
      `product_description_page.resource`'s Variables section), mandatory-yellow fields, quirks
      (screen-prefixed Code label, 3 mandatory reference dropdowns), last-verified date
      2026-08-23/28.
- [x] **21. Reuse clause.** Step 0 found Product Description's RF automation ALREADY implemented
      and merged — this backfill produces exactly the deliverables the reuse clause requires: #3
      JOURNAL, #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
