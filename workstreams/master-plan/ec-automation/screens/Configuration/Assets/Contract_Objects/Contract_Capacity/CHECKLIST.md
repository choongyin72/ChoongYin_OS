# Contract Capacity - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 (Batch 4 of `docs/lean-deliverable-backfill-workorder.md`). Screen was
built 2026-08-01 (original 4-TC shape) then converted to the Area pattern 2026-08-26 (PR #535,
5-TC shape). Section G's lean waiver (2026-08-23/26) had skipped items 1/3/6/7/20 for that
conversion round; Section H (2026-08-27) retired that waiver. This CHECKLIST reflects the
CURRENT (5-TC, post-#535) state, ticked with real evidence — items 4/5 (Playwright driver +
investigation/) stay waived per Section H (Universal Screen Engine replaces that role)._

## Step 0 - check-existing gate
- [x] 0a KB map existed from the 2026-08-01 build; refreshed 2026-08-28 to reflect the 5-TC
      Area-pattern shape (`ec-ui-knowledge/screens/contract_capacity.md`).
- [x] 0b grep ec-automation -> `pageobjects/.../contract_capacity_page.resource` +
      `tests/.../contract_capacity_iud.robot` are the only automation files (re-confirmed via
      `grep -ril contract_capacity_page.resource` against the full tree, 2026-08-28) - REUSE/EXTEND
      confirmed, this backfill adds docs only, no parallel copy.
- [x] 0c reused shared engine (`ec_object_iud.py` historically) + `DbVerify.py` + T2
      (`manage_object.resource`) - unchanged by this backfill.

## A. Bundle artifacts
- [x] **1** `contract_capacity_sow.md` - refreshed 2026-08-28 to document the Area-pattern
      conversion (nav shape, mandatory fields, PR #535 dev story).
- [x] **2** `README.md` - refreshed with the current 5-TC run commands + DB self-clean snippet.
- [x] **3** `JOURNAL.md` - refreshed 2026-08-28: Built (2026-08-01 + 2026-08-26 conversion +
      this backfill) / Done well / Done wrong-lessons / Blockers→resolution / Decisions /
      Evidence, pulling real content from PR #535's body.
- [ ] **4** Playwright flow - **WAIVED** (Section H, 2026-08-27): `py/contract_capacity_iud.py`
      is the pre-existing 2026-08-01 driver, left UNTOUCHED by PR #535 and by this backfill; no
      new Playwright bundle built (Universal Screen Engine replaces this role going forward).
- [ ] **5** `investigation/` - **WAIVED** (Section H): pre-existing `recon.py` from the
      2026-08-01 build stays as historical reference; no new recon script produced.
- [x] **6** `evidence/` - `evidence/CC_0[1-5]_*.png` + `results.json` (2026-08-01 build) PLUS
      `evidence/backfill_2026-08-28/` (dryrun 5/5, live attempt-1 `output_attempt1_TC05fail.xml`,
      live retry `output.xml`/`log.html`/`report.html` 5/5, DB self-clean 0, `results_summary.md`).
- [x] **7** `CHECKLIST.md` - this file.

## B. RF files
- [x] **8** T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource`
      - label-driven, properties-file-driven fill (PR #535, 2026-08-26). Pre-existing, unmodified
      by this backfill.
- [x] **9** Suite `tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot` - 5 TC
      (Clean State / Insert / Update / Find / Delete), per-TC login/logout. Pre-existing,
      unmodified by this backfill.

## C. Verification gates (re-run 2026-08-28 for this backfill; original gate cited in PR #535)
- [x] **10** robocop clean - `py -m robocop check pageobjects/.../contract_capacity_page.resource
      tests/.../contract_capacity_iud.robot` → **7 issues** (VAR02 x2 + DOC02 x5), exact parity
      with PR #535's own citation ("7 issues... exact parity with Area's own reference-pattern
      baseline") - re-run 2026-08-28, same count.
- [x] **11** `--dryrun` - re-run 2026-08-28: `robot --dryrun tests/.../contract_capacity_iud.robot`
      → **5/5 pass, 0 fail**.
- [x] **12** LIVE run - re-run 2026-08-28: attempt 1 = 4/5 pass (TC05 flake, see JOURNAL); retry =
      **5/5 pass, 0 fail** (`evidence/backfill_2026-08-28/output.xml`/`log.html`/`report.html`).
- [x] **13** DB ground-truth - `Verify Object Removed`/`Verify Object Insert Exists`/
      `Verify Object Form Record` (shared T2, pure-screen + in-suite DB check on delete) against
      `OV_CONTRACT_CAPACITY`; fresh-connection re-check 2026-08-28:
      `SELECT COUNT(*) FROM OV_CONTRACT_CAPACITY WHERE CODE LIKE 'AUTOTEST%'` → `0`.
- [x] **14** FULL I-U-D - TC02 Insert, TC03 Update, TC05 Delete all present and passing (plus TC04
      Find, added in PR #535).
- [x] **15** Self-clean confirmed - 0 residual, fresh oracledb connection, 2026-08-28 (see #13).
- [x] **16** Hygiene - `py scripts/check_bundle_hygiene.py` (repo root) re-run 2026-08-28 → **PASS**
      (no hardcoded creds R16, pure ASCII R20, no CHECKLIST/VERIFY-REPORT contradiction).

## D. Delivery
- [x] **17** Registry row - `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`
      (already appended/updated by PR #535, 2026-08-26 - describes the 5-TC conversion in full).
- [x] **18** Scorecard row - `docs/automation-scorecard.md` (already updated by PR #535).
- [ ] **19** PR (R9 body) - CANNOT be ticked here: this file is written BEFORE the backfill PR
      exists. Ticked in the PR body itself, never at scaffold time (per the #235 lesson).

## E. Knowledge base
- [x] **20** KB map `ec-ui-knowledge/screens/contract_capacity.md` - refreshed 2026-08-28 to the
      current 5-TC/Area-pattern shape (was stale at the 2026-08-01/4-TC state).
- [x] **21** Reuse clause - N/A for a fresh build; APPLIES for this backfill of already-shipped
      automation - JOURNAL + evidence + KB map all refreshed with real, current content (not just
      passing tests re-cited).

_Items 10-16 for this backfill were re-run live 2026-08-28 (not hand-typed) - see JOURNAL.md
"Evidence" section and `evidence/backfill_2026-08-28/` for the raw artifacts. OV-GM specifics:
single Business Unit dropdown navigator (`TS5 BU`) + GO, PROVEN by the pre-existing Playwright
driver; dropdowns Contract Name=TS5 Shipper B Firm, Location Name=TS5 Domestic Gas Storage._
