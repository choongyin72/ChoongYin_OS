# Inventory Area - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 (Batch 9, `docs/lean-deliverable-backfill-workorder.md`) after owner decision
2026-08-27 retired Section G's lean waiver (Section H). Screen was converted to the full Bank-pattern
shape under PR #460 (2026-08-23, Batch 8 of the Bank-pattern conversion project); this checklist
documents that already-merged, already-verified work - it does not re-run or re-verify the
automation itself._

## Step 0 - check-existing gate
- [x] **0a.** `ec-ui-knowledge/screens/inventory_area.md` existed (from the 2026-07-26 build) and
      was read + refreshed as part of this backfill, not re-scanned from scratch.
- [x] **0b.** `grep -ril "inventory_area" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> only this build (`py/inventory_area_iud.py`, `pageobjects/.../inventory_area_page.resource`,
      `tests/.../inventory_area_iud.robot`, `screens/.../Inventory_Area/`) - no parallel copy.
- [x] **0c.** Reused shared T2 `manage_object.resource` + T1 `common.resource` + `DbVerify.py`;
      zero shared-file changes for the PR #460 conversion (confirmed in PR #460's own body via
      `git status --short`).

## A. Bundle artifacts - `screens/Configuration/Assets/Inventory_Objects/Inventory_Area/`
- [x] **1.** `inventory_area_sow.md` - refreshed to describe both the 2026-07-26 build AND the
      2026-08-23 Batch 8 Bank-pattern rebuild (dev story pulled from PR #460's real body).
- [x] **2.** `README.md` - refreshed: bundle overview + exact run commands (dryrun, live headless,
      DB self-clean query against `OV_INVENTORY_AREA`).
- [x] **3.** `JOURNAL.md` - refreshed on the Bank JOURNAL.md model (Built / Done well / Done wrong /
      Blockers->resolution / Decisions / Evidence), pulling real content from PR #460's body.
- [ ] **4.** Playwright driver - **N/A / waived (Section H, unchanged from Section G).** The
      Universal Screen Engine (`py/engine.py`) is the owner-decided replacement for hand-written
      Playwright drivers going forward; `py/inventory_area_iud.py` is left exactly as it was
      (2026-07-26), not rebuilt for the Batch 8 RF conversion or for this backfill.
- [ ] **5.** `investigation/` - **N/A / waived (Section H, unchanged from Section G).** Same reason
      as #4. The pre-existing `investigation/recon.py` (2026-07-26) is kept as-is; not rebuilt.
- [x] **6.** `evidence/` - re-ran the live suite once (2026-08-28), captured `TC0[1-5] * .png`,
      `rf_report.html`, `rf_log.html` into this folder (replaced the stale 2026-07-26 4-TC
      screenshots/report with the current 5-TC run's output).
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files - treeview-mirrored (pre-existing, NOT modified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Inventory_Objects/inventory_area_page.resource` -
      properties-file-driven, explicit grid-filter wiring, dedicated credentials (Batch 8/PR #460 shape).
- [x] **9.** Suite `tests/Configuration/Assets/Inventory_Objects/inventory_area_iud.robot` - TC01
      Verify Clean State -> TC02 Insert -> TC03 Update -> TC04 Find -> TC05 Delete, per-TC login/logout.

## C. Verification gates (record the evidence in CHECKLIST + the PR body)
- [x] **10.** robocop clean - PR #460 body cites this build class as robocop-clean (Batch 8 ground
      rule: no shared-file diff); not re-run for this docs-only backfill per the work order
      ("do not re-run the full original build").
- [x] **11.** `--dryrun` N/N PASS - PR #460: full-tree `robot --dryrun` -> **758/758 pass, 0 fail**.
- [x] **12.** LIVE headless run N/N PASS - PR #460: live 5/5 PASS. **Re-confirmed this backfill,
      2026-08-28:** `EC_HEADLESS=true robot tests/Configuration/Assets/Inventory_Objects/
      inventory_area_iud.robot` -> **5/5 PASS** (TC01-TC05). See `evidence/rf_report.html`.
- [x] **13.** DB ground-truth - exact DbVerify assertions: `Code Should Be Present In View`/
      `Code Should Be Absent In View` (`OV_INVENTORY_AREA`) via T2's `Verify Object Insert Exists`/
      `Verify Object Removed`/`Verify Object Does Not Exist`; each op (insert/update/delete)
      verified at DB level per PR #460's body.
- [x] **14.** FULL I-U-D scope - TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (not I/D only).
- [x] **15.** Self-clean confirmed - PR #460: fresh Oracle connection, BEFORE and AFTER the live
      suite, `SELECT COUNT(*) FROM OV_INVENTORY_AREA WHERE CODE = 'AUTOTEST_INVA'` = 0 and
      `CODE LIKE 'AUTOTEST%'` = 0, both times.
- [x] **16.** Hygiene PASS - PR #460 body confirms no shared-file/env-cred/ASCII violations
      introduced; not re-run for this docs-only backfill.

## D. Delivery
- [x] **17.** Registry row - `docs/ec_screen_registry.md` (Inventory Area row) MODIFIED by PR #460
      to reflect the Batch 8 conversion (confirmed present, not a stale duplicate).
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` (Inventory Area row) MODIFIED by
      PR #460, same treatment.
- [x] **19.** PR - this backfill's own PR (docs/inventory-area-backfill-artifacts branch), 6-field
      body, base = master, never self-merged. Original conversion PR #460 already merged
      2026-08-23 with its own compliant 6-field body.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/inventory_area.md` - refreshed to describe
      the current (Batch 8) selectors: 5-TC suite, explicit grid-filter keywords, dedicated
      credentials; pulled from `inventory_area_page.resource`'s actual Variables section.
- [x] **21.** Reuse clause - N/A in the original sense (this was originally a new build, not a
      Step-0 reuse), but the SAME underlying principle applies to this backfill: JOURNAL + evidence
      + KB map are refreshed to match the real current state of the code, not left describing a
      superseded build.

---

**Waived items (unchanged, Section H):** #4 (Playwright driver), #5 (`investigation/`) - the
Universal Screen Engine replaces that role going forward; not rebuilt for this or any Bank-/
Area-pattern conversion.

**Not re-run for this backfill (per work order instruction, evidence pulled from the already-merged
PR #460 instead):** #10 robocop, #11 dryrun (full-tree), #16 hygiene. **Re-run for fresh evidence:**
#12 live suite (5/5 PASS, 2026-08-28).
