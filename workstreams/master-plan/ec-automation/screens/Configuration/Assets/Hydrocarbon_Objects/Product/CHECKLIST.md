# IUD Task — Deliverable Checklist — Product

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 12, final batch) — Product's RF
suite was already built brand-new to the Bank pattern and merged via PR #485 (2026-08-24); this
checklist documents the retroactive documentation/evidence bundle added 2026-08-28, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was rebuilt,
modified, or re-verified from scratch.** Since Product never had a `screens/` bundle before (lean
new-screen build — Phase 3, `ec-bank-pattern-new-screen` skill), items 1/2/3/6/7/20 are all
FIRST-TIME creations, not refreshes.

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/product.md` did not exist before this backfill — created
      fresh (item 20 below), transcribed from `product_page.resource`'s own Variables/
      Documentation section, not re-scanned live.
- [x] **0b.** `grep -rln "product_page.resource"` (excluding Product Description/Product Group/
      Product Price Object/Product Split Key) ->
      `pageobjects/Configuration/Assets/Hydrocarbon_Objects/product_page.resource`,
      `tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot` — REUSED/EXTENDED
      (documentation only), no parallel copy built. No pre-existing `screens/.../Product/` folder
      of any kind existed before this backfill.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (no navigator keyword
      needed — Product's navigator is a single optional Date + GO) — not modified by this backfill.

## A. Bundle artifacts — `screens/Configuration/Assets/Hydrocarbon_Objects/Product/`
- [x] **1. `product_sow.md`** — created (did not exist before): classification, nav/grid/cell
      shape (transcribed from `product_page.resource` + the registry row), test data, real PR #485
      new-build dev story (not a conversion story — no prior automation of any kind existed for
      class PRODUCT to convert from).
- [x] **2. `README.md`** — created with exact RF commands (dryrun/live headless) and the
      `OV_PRODUCT`/`PRODUCT`/`PRODUCT_VERSION` DB self-clean query pattern; states plainly the RF
      suite is the ONLY test for this screen (no Playwright bundle exists or is required).
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #485's real body, not invented. PR #485 disclosed no flake/wrong-classification/regression —
      recorded explicitly as "no gap to report" rather than smoothed over or fabricated.
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A. Playwright bundle waived permanently, owner
      decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). Product never had one —
      it was built as a lean RF-only new-screen suite from the start; there is nothing to preserve
      or leave untouched here.
- [ ] **5. `investigation/`** — N/A (waived per Section H). No pre-existing `investigation/` folder
      exists for Product at all (unlike Tank/Berth, which retained recon scripts from their own
      builds) — the original PR #485 build used `resolve_ec_screen.py`/`scan_ec_screen.py` as
      throwaway recon, not committed as a permanent deliverable.
- [x] **6. `evidence/`** — created fresh: `evidence/dryrun/` (`log.html`+`report.html`+`output.xml`)
      and `evidence/live/` (`log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN Bank-pattern
      suite, plus `summary.json` with the dryrun/live/DB-self-clean/robocop/hygiene results. All six
      files are well under the 2MB single-file guidance (largest is `live/output.xml` at ~420KB —
      screen-scoped, not full-tree). No original-build `evidence/` folder existed to preserve.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Hydrocarbon_Objects/product_page.resource` — already exists
      (PR #485), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot` — already
      exists (PR #485), unmodified by this backfill; TC01 clean-state -> TC02 insert -> TC03 update
      -> TC04 find -> TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-28)
- [x] **10. robocop clean (parity with Bank)** — `robocop check
      pageobjects/.../product_page.resource tests/.../product_iud.robot` (2026-08-28, this
      session) -> **exit code 1, 12 issues: 7x `VAR02` (unused variable — `${TEST_CODE}`/
      `${END_DATE}`/`${OBJ_NAME}`/`${OBJ_DESC}`/`${OBJ_SORT_ORDER}`/`${OBJ_NAME_UPD}`/
      `${OBJ_DESC_UPD}`, kept in the suite as documented cross-reference to the testdata properties
      files, per the file's own header comments) + 5x `DOC02` (missing per-test-case
      `[Documentation]`, TC01-TC05 — suite-level `Documentation` already covers this)**.
      Cross-checked `robocop check pageobjects/.../bank_page.resource tests/.../bank_iud.robot` (the
      OV/Bank role model) on the same session -> **also exit code 1, 13 issues, same VAR02/DOC02
      pattern**. Product's 12 issues are at parity with Bank's own established baseline, not a
      new/worse defect — no fix applied, per this task's explicit "do not modify the RF automation"
      scope.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun --outputdir Workplaces/product-backfill/dryrun
      tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot` -> **5 tests, 5 passed, 0
      failed** (2026-08-28, this session; log/report/output archived in `evidence/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      Workplaces/product-backfill/live tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot`
      -> **5 tests, 5 passed, 0 failed** (TC01-TC05 all PASS, first attempt, 2026-08-28, this
      session; archived in `evidence/live/`). No timeout, no retry needed.
- [x] **13. DB ground-truth** — fresh oracledb connection (separate from the RF suite's own
      connection), 2026-08-28, this session: `SELECT (SELECT COUNT(*) FROM PRODUCT WHERE
      OBJECT_CODE='AUTOTEST_PRODUCT'), (SELECT COUNT(*) FROM OV_PRODUCT WHERE
      CODE='AUTOTEST_PRODUCT') FROM DUAL` -> `(0, 0)`. Confirms the suite's own TC02/TC03/TC05
      insert/update/delete cycle against `OV_PRODUCT` completed cleanly and left zero residual rows.
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS (see
      item 12); TC04 Find also present (5th TC, matching the original PR #485 scope).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_PRODUCT` rows in `PRODUCT`/`OV_PRODUCT` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-28,
      this session) -> `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about `Contract_Area/investigation/live_recon_contract_area.py`'s selector
      strings, not related to Product).

## D. Delivery
- [x] **17. Registry row** — already present, added by PR #485 (not this backfill); confirmed live
      at `docs/ec_screen_registry.md` (row: "Product | Configuration > Assets > Hydrocarbon Objects
      > Product (CO.0007, class PRODUCT) | OV plain manage-object, live 5/5 DB-verified, self-clean,
      full I-U-D..."). This backfill does not touch the registry row again (append-only /
      no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from PR #485; not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/product-backfill-artifacts`), 6-field body,
      base = master, sync-before-push done, never self-merge. (Ticked once the PR is raised — see
      PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/product.md` — created 2026-08-28 (did not
      exist before), transcribed from `product_page.resource`'s own Variables/Documentation section
      (nav path, DB view, grid id, insert/update/delete selectors, mandatory-yellow fields, quirks),
      not re-scanned live — per the backfill work order's instruction to transcribe, not
      re-discover. Explicitly disambiguated from Product Description/Product Group/Product Price
      Object/Product Split Key's own KB entries.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #485); this backfill
      produced the deliverables that document it: SOW (#1), README (#2), JOURNAL (#3), evidence
      (#6), CHECKLIST (#7), KB map (#20) — the full first-time bundle this lean new-screen build
      never produced.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). For Product specifically this is not "waived
  re-verification of an existing driver" (as for converted screens) — it is "never built, and
  correctly not built now," since Product was a lean new-screen build from day one with no
  Playwright bundle and no `investigation/` folder of any kind.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #485 (append-only convention, R23 — never duplicate-edit an existing row).
- Item 10 (robocop) is NOT a bare "clean" tick — it is ticked at **parity with Bank's own
  established baseline** (both exit code 1, same VAR02/DOC02 issue classes), since fixing these
  would require modifying the already-merged, already-verified RF automation — explicitly out of
  scope for this documentation-only backfill task.
