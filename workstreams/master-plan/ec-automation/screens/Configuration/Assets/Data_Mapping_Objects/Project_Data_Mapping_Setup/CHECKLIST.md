# IUD Task - Deliverable Checklist (Project Data Mapping Setup)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` Section F (engine-only bundle variant).
Playwright-side items are backed by a fresh live run (`AUTOTEST_PDMS_007`, 2026-08-16); RF-side
items are deliberately deferred - see note below.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** No `ec-ui-knowledge/screens/project-data-mapping-setup.md` existed before this
      bundle - not added this pass (screen already has a full-narrative home in the design doc's
      "Pilot 3" section; a KB stub would just duplicate it - see `reference_ec_screens_notes_help_corpus`
      pattern, this screen's own SOW/JOURNAL is the more complete reference).
- [x] **0b.** Existing work found (Phase 4 Pilot 3 - INSERT+DELETE proven live 2026-08-14, never
      packaged) - REUSED/EXTENDED (fresh live re-verification of the full I-U-D cycle, including
      the previously-unresolved UPDATE step), not rebuilt in parallel.
- [x] **0c.** Uses the Universal Screen Engine (`py/engine.py`) directly - no shared-file changes
      needed for the driver itself (a genuine, separate engine improvement was made during this
      pass and shipped as its own PR, not bundled here).

## A. Bundle artifacts
- [x] **1.** `project_data_mapping_setup_sow.md`.
- [x] **2.** `README.md`.
- [x] **3.** `JOURNAL.md` (includes real mistakes made + fixed during this packaging pass).
- [x] **4.** `playwright/ec_iud_project_data_mapping_setup.py` - delegates to
      `py/project_data_mapping_setup_iud.py`, independently verified live.
- [x] **5.** `investigation/` - 4 real recon scripts (real-row lookup, treeview path derivation,
      Insert mandatory-field confirmation, Target Property option check).
- [x] **6.** `evidence/` - 8 screenshots, fresh 2026-08-16 run.
- [x] **7.** This file.

## B. RF files - DEFERRED, not built
- [ ] **8.** T3 page object - **deferred.** This screen was built via the Universal Screen Engine
      (`engine.py`), not the classic T2/T3 pattern - same reasoning already applied to Financial
      Item Definition/Template (PR #379). Will revisit once RF can properly adopt the new engine
      implementation directly, rather than duplicating a hand-written T3 that would become
      redundant.
- [ ] **9.** Suite - **deferred**, same reason as #8.

## C. Verification gates
- [ ] **10.** robocop clean - N/A, no RF files exist yet (deferred, see #8/#9).
- [x] **16.** Hygiene PASS - `check_bundle_hygiene.py` exit=0 (applies to the Playwright/Python
      side, which does exist).
- [ ] **11.** `--dryrun` - N/A, no RF suite exists yet (deferred).
- [ ] **12.** LIVE RF suite - N/A, no RF suite exists yet (deferred).
- [x] **13.** DB ground-truth - live driver run + direct DB query, both confirm `AUTOTEST_PDMS_007`
      inserted/updated/deleted correctly against `OV_COST_MAPPING`.
- [x] **14.** FULL I-U-D scope - Insert + Update + Delete all proven live, via the Playwright
      driver AND independently via the `playwright/` delegator - closing the gap left open at the
      end of the original Pilot 3 session (Update had never been proven there).
- [x] **15.** Self-clean confirmed - 0 residual for `AUTOTEST_PDMS_007` after delete, confirmed
      after both the direct driver run and the delegator re-run.

## D. Delivery
- [x] **17.** Registry row appended to `docs/ec_screen_registry.md`.
- [x] **18.** Scorecard row appended to `docs/automation-scorecard.md`.
- [x] **19.** PR with R9 6-field body; R8 sync; not self-merged.

## E. Knowledge base
- [ ] **20.** Not added - see 0a rationale above (design doc's "Pilot 3" section is the complete
      reference; no separate stub needed).
- [x] **21.** Reuse clause - Step 0 found existing (unpackaged, partially-unproven) work; JOURNAL +
      fresh full-cycle evidence produced in this pass.

## Note on the RF gap (same reasoning as Financial Item Definition/Template, PR #379)
Proceed with this CHECKLIST in the standard engine-only shape, but leave items 8-9 (and the gates
that depend on them, 10-12) explicitly deferred rather than built now or faked as passing. Will
revisit once the RF layer can properly call into the Universal Screen Engine directly, instead of
duplicating a hand-written T3 for a screen the engine already drives generically.
