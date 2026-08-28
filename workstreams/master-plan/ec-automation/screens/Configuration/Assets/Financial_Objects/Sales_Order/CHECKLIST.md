# IUD Task — Deliverable Checklist — Sales Order

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 7) — Sales Order's RF suite was
already converted to the Bank pattern and merged via PR #444 (2026-08-23); this checklist
documents the retroactive documentation/evidence bundle added 2026-08-28, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.** Sales Order already had a `screens/` bundle
predating the lean rule (from its original 2026-06-11 Playwright build) — items 1/2/4/5/6 (partly)
existed before this backfill and were reviewed/refreshed, not created from nothing; items 3/7/20
are first-time creations.

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/sales_order.md` did not exist before this backfill —
      created fresh (item 20 below), transcribed from `sales_order_page.resource`'s own
      Variables/Documentation section, not re-scanned live.
- [x] **0b.** `grep -ril "sales_order_page.resource"` ->
      `pageobjects/Configuration/Assets/Financial_Objects/sales_order_page.resource`,
      `tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot` — REUSED/EXTENDED, no
      parallel copy built. The pre-existing `screens/.../Sales_Order/{playwright/,investigation/,
      evidence/}` folder (from the original 2026-06-11 build) was found and left untouched.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (`Find/Clear Object Row
      By Filter`, `Insert/Update Object From Properties`, `Delete Object Via End Date` all
      pre-existing) — not modified by this backfill.

## A. Bundle artifacts — `screens/Configuration/Assets/Financial_Objects/Sales_Order/`
- [x] **1. `sales_order_sow.md`** — pre-existing (original 2026-06-11 Playwright build), reviewed
      this backfill: classification/DB view/test data already accurate, left as-is (no edit
      needed — describes the Playwright build correctly; the RF Bank-pattern conversion's own
      "what happened" narrative lives in JOURNAL.md instead, per this backfill's scope).
- [x] **2. `README.md`** — UPDATED (was Playwright-only; now documents both layers): added the
      exact RF commands (dryrun/live headless/live headed), the `OV_PRODUCT_SALES_ORDER` DB
      self-clean query pattern, and key facts pulled from PR #444. Original Playwright run
      instructions preserved in the "Folder" section.
- [x] **3. `JOURNAL.md`** — created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #444's real body, not invented.
- [x] **4. `playwright/ec_iud_sales_order.py`** — PRE-EXISTING (original 2026-06-11 build), left
      untouched. Not rebuilt or re-verified — per Section H, no NEW Playwright work is done for
      Bank-pattern conversions; a pre-existing driver from before the conversion is preserved as a
      historical reference, not deleted.
- [x] **5. `investigation/`** — PRE-EXISTING (original 2026-06-11 build), left untouched, used
      read-only.
- [x] **6. `evidence/`** — PRE-EXISTING top-level content (original Playwright screenshots +
      `results.json`) left untouched; ADDED `evidence/backfill_2026-08-28/` with a dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN RF suite, plus
      `summary.json` with the DB self-clean result, filter-fired grep, robocop parity, and hygiene
      output.
- [x] **7. `CHECKLIST.md`** — this file (created, did not exist before).

## B. RF files — treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Financial_Objects/sales_order_page.resource` — already
      exists (PR #444), unmodified by this backfill; reviewed only for the KB map.
- [x] **9. Suite** `tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot` — already
      exists (PR #444), unmodified by this backfill; TC01 clean -> TC02 insert -> TC03 update ->
      TC04 find -> TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-28)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../sales_order_page.resource
      tests/.../sales_order_iud.robot` (2026-08-28, this session) -> **7 issues, 2x `VAR02`
      (unused variable) + 5x `DOC02` (missing test-case documentation, TC01/TC03-TC05)** — same
      count/shape PR #444's own body cited ("robocop: 7 issues... at/below the 9-issue baseline").
      No fix applied, per this task's explicit "do not modify the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** — `py -m robot --dryrun --outputdir tmp_dryrun_so
      tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot` -> **5 tests, 5 passed,
      0 failed** (2026-08-28, this session; archived in `evidence/backfill_2026-08-28/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir tmp_live_so
      tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot` -> **5 tests, 5 passed,
      0 failed** (TC01-TC05 all PASS, 2026-08-28, this session, FIRST attempt, no retry needed;
      archived in `evidence/backfill_2026-08-28/live/`).
- [x] **13. DB ground-truth** — fresh oracledb connection (separate from the test run),
      2026-08-28, this session: `SELECT COUNT(*) FROM OV_PRODUCT_SALES_ORDER WHERE CODE =
      'AUTOTEST_SO'` -> **0**; `SELECT CODE, NAME FROM OV_PRODUCT_SALES_ORDER WHERE UPPER(CODE)
      LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%'` -> **no rows**. Confirms the suite's own
      TC02/TC03/TC05 insert/update/delete cycle against `OV_PRODUCT_SALES_ORDER` completed
      cleanly.
- [x] **14. FULL I-U-D scope** — TC02 Insert + TC03 Update + TC05 Delete all present and PASS (see
      item 12); TC04 Find also present.
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_SO` / `AUTOTEST%` rows in `OV_PRODUCT_SALES_ORDER` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-28,
      this session) -> `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about `Contract_Area/investigation/live_recon_contract_area.py`'s selector
      STRINGS, not related to Sales Order).

## D. Delivery
- [x] **17. Registry row** — already present, added by PR #444 (not this backfill); confirmed
      live: `docs/ec_screen_registry.md`, Sales Order row (Financial Objects section) —
      "OV ✅ rebuilt live 5/5 (2026-08-23, batch-5)... `OV_PRODUCT_SALES_ORDER`... `sales_order_
      page.resource`". This backfill does not touch the registry row again (append-only /
      no-duplicate-edit).
- [x] **18. Scorecard row** — pre-existing from PR #444; not duplicated by this backfill
      (documentation-only task, no new automation scope to score).
- [ ] **19. PR** — this backfill's own PR (branch `docs/sales-order-backfill-artifacts`), 6-field
      body, base = master, sync-before-push done, never self-merge. (Ticked once the PR is
      raised — see PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/sales_order.md` — created 2026-08-28 (did
      not exist before), transcribed from `sales_order_page.resource`'s own Variables/
      Documentation section (nav path, DB view, grid id, insert/update/delete selectors,
      mandatory-yellow fields, quirks), not re-scanned live — per the backfill work order's
      instruction to transcribe, not re-discover.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #444, plus an even
      older Playwright build); this backfill produced the deliverables that document the CURRENT
      RF automation: JOURNAL (#3), CHECKLIST (#7), KB map (#20), plus a refreshed README (#2) and
      new evidence (#6) — the full documentation bundle the lean rule had skipped.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are NOT newly built by this backfill (waived per
  Section H for NEW work), but UNLIKE a lean new-screen build (e.g. Tank), this screen already had
  a real, pre-existing Playwright driver from BEFORE the conversion/waiver rule existed. That
  driver was reviewed, confirmed still present and unmodified, and left in place as a historical
  reference — not rebuilt, not re-verified against the current RF suite's behavior, and not
  deleted.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill — they already exist
  from PR #444 and appending a second row for the same screen would violate the append-only,
  no-duplicate convention (R23).
- Item 1 (SOW) and item 6 (evidence, top-level content) are pre-existing from the ORIGINAL
  2026-06-11 build (predating even the Bank-pattern conversion), not from PR #444 — reviewed for
  accuracy against the CURRENT screen shape and left as-is since they remain accurate; new
  evidence for the current RF suite was added as a dated subfolder rather than replacing the
  original Playwright evidence.
