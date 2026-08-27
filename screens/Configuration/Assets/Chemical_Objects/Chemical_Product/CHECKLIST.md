# IUD Task — Deliverable Checklist — Chemical Product

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. Backfill of a genuinely new-build Bank-pattern
screen (PR #486, merged 2026-08-24) under the Section H workorder
(`docs/lean-deliverable-backfill-workorder.md`, Batch 12). Per Section G/H, items 4/5
(Playwright driver + investigation/) stay permanently waived for Bank-/Area-pattern builds — the
Universal Screen Engine replaces that role.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/chemical_product.md` did not exist before this backfill —
      confirmed via `grep -ril` during the original PR #486 build (no prior KB entry).
- [x] **0b.** `grep -ril "chemical_product" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      before PR #486 → no hits (genuinely new build, no parallel-copy risk). Confirmed no prior
      RF/Playwright automation existed.
- [x] **0c.** Reused shared T2/T1 (`manage_object.resource`/`common.resource`); the Delete
      workaround was implemented as a NEW screen-scoped library (`ChemicalProductCleanup.py`),
      not folded into the shared `libraries/DbVerify.py` — correct per this gate's spirit
      (extend, don't fork the shared plumbing).

## A. Bundle artifacts — `screens/Configuration/Assets/Chemical_Objects/Chemical_Product/`
- [x] **1. `chemical_product_sow.md`** — classification, nav/grid/cell shape, test data, dev
      story from PR #486. Present in this bundle.
- [x] **2. `README.md`** — bundle overview + exact dryrun/live/DB-check commands. Present.
- [x] **3. `JOURNAL.md`** — Built/Done well/Done wrong/Blockers/Decisions/Evidence, sourced from
      PR #486's real body. Present.
- [ ] **4. Playwright driver** — N/A "Playwright bundle waived" (Section H: permanently waived
      for Bank-/Area-pattern builds; Universal Screen Engine replaces this role).
- [ ] **5. `investigation/`** — N/A "Playwright bundle waived" (same reason as #4).
- [x] **6. `evidence/`** — `evidence/live/` (output.xml, log.html, 25 step screenshots),
      `evidence/dryrun/output.xml`, `evidence/results-summary.md`. Captured 2026-08-28, live 5/5
      PASS re-run of the already-proven suite (see Evidence section of JOURNAL.md).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Chemical_Objects/chemical_product_page.resource`
      — pre-existing from PR #486, NOT modified by this backfill (verified: no diff in this PR
      touches `pageobjects/` or `tests/`).
- [x] **9. Suite** `tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot` — TC01
      clean-state -> TC02 insert -> TC03 update -> TC04 find -> TC05 delete. Pre-existing from
      PR #486, NOT modified.

## C. Verification gates
- [x] **10. robocop clean** — per PR #486's body: 11 issues on the changed files, exact parity
      with `chemical_transport_tank_iud.robot`/`_page.resource` (11 issues, same DOC02-only
      baseline noise) — no regression. Not re-run this backfill (no automation files changed).
- [x] **11. `--dryrun` N/N PASS** — this backfill: `robot --dryrun` → **5 tests, 5 passed, 0
      failed** (`evidence/dryrun/output.xml`). Original PR #486: full-tree dryrun 779/779.
- [x] **12. LIVE headless run N/N PASS** — this backfill: `EC_HEADLESS=true robot` → **5 tests, 5
      passed, 0 failed** (`evidence/live/output.xml`, `evidence/live/log.html`). Original PR
      #486: live RF 5/5.
- [x] **13. DB ground-truth** — this backfill, fresh oracledb connection (separate session from
      the live run): `SELECT COUNT(*) FROM CHEM_PRODUCT WHERE OBJECT_CODE LIKE 'AUTOTEST%'` = 0;
      `SELECT COUNT(*) FROM OV_CHEM_PRODUCT WHERE CODE LIKE 'AUTOTEST%'` = 0; orphan check on
      `CHEM_USAGE_REPORT_CONF` (join on `OBJECT_ID` vs `CHEM_PRODUCT`) = 0. See
      `evidence/results-summary.md`.
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Delete (TC05) all present and
      passing, plus clean-state (TC01) and find (TC04).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read = 0 residual
      `AUTOTEST_CHEMPROD` rows in `CHEM_PRODUCT`/`OV_CHEM_PRODUCT`, 0 orphaned
      `CHEM_USAGE_REPORT_CONF` rows.
- [x] **16. Hygiene PASS** — no new code files added by this backfill (docs/evidence only); PR
      #486's own hygiene pass already covered `ChemicalProductCleanup.py`/the T3/suite (per its
      PR body — no env-creds hardcoded, ASCII-clean).

## D. Delivery
- [x] **17. Registry row** — already appended in PR #486 (`docs/ec_screen_registry.md`, "Chemical
      Product" row, line ~271). Not duplicated by this backfill.
- [x] **18. Scorecard row** — already appended in PR #486 (`docs/automation-scorecard.md`). Not
      duplicated by this backfill.
- [x] **19. PR** — this backfill's own PR follows the standard 6-field body (What was backfilled
      / Files added / Base branch = master / etc.); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/chemical_product.md` — nav path, DB view,
      grid id, insert/update/delete selectors, mandatory fields, quirks (incl. the
      `CHEM_USAGE_REPORT_CONF` known-issue workaround), last-verified 2026-08-24 (original build)
      / bundle backfilled 2026-08-28. Newly created by this backfill (did not exist before).
- [x] **21. Reuse clause** — N/A for this screen (this is a genuinely new build per PR #486, not
      a Step-0 "already implemented" reuse case) — but the retroactive backfill itself satisfies
      the same intent: JOURNAL + evidence + KB map now exist alongside the already-passing tests.

---

**Verdict:** OVERALL — all applicable items satisfied with real evidence; items 4/5 correctly
marked N/A per the Section H Playwright waiver. No automation files (`pageobjects/`, `tests/`,
`testdata/`, `libraries/ChemicalProductCleanup.py`) were touched by this backfill.
