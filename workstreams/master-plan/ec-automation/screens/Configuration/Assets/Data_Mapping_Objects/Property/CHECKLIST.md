# Property - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 (Batch 5 of `docs/lean-deliverable-backfill-workorder.md`) - Section H
retired the 2026-08-23/26 lean waiver; this bundle now carries the full SOW/README/JOURNAL/
evidence/CHECKLIST/KB set around PR #559's merged Area-pattern conversion (2026-08-26). Items 4/5
(Playwright driver + investigation/) stay waived per Section H - the Universal Screen Engine is
the owner-decided replacement._

## Step 0 - check-existing gate
- [x] 0a KB map existed and is refreshed this session (`ec-ui-knowledge/screens/property.md`) to
      reflect the Area-pattern shape.
- [x] 0b grep confirmed real file paths: `pageobjects/Configuration/Assets/Data_Mapping_Objects/
      property_page.resource`, `tests/Configuration/Assets/Data_Mapping_Objects/
      property_iud.robot` - already-existing, already-merged automation (PR #559), reused/
      extended, not duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource` T2, `DbVerify.py`) - no new
      plumbing added by this backfill.

## A. Bundle artifacts
- [x] 1 `property_sow.md` - updated with Area-pattern classification, navigator shape (G:0 Date
      already-defaulted / G:1 Business Unit mandatory at C:0), shared-keyword `group=1
      start_col=0` usage, dev story pulled from PR #559's real body.
- [x] 2 `README.md` - bundle overview + exact dryrun/live/DB-self-clean commands.
- [x] 3 `JOURNAL.md` - Built/Done well/Done wrong/Blockers/Decisions/Evidence sections added for
      the 2026-08-26 PR #559 conversion (real content from its PR body) + this 2026-08-28 backfill
      session.
- [ ] 4 Playwright flow - **N/A, waived (Section H)** - `py/property_iud.py` remains the pre-
      existing driver, untouched; the Universal Screen Engine supersedes new Playwright work.
- [ ] 5 `investigation/` - **N/A, waived (Section H)** - the pre-existing `investigation/`
      directory (2026-08-02 build) is left as-is; no new recon deliverable required.
- [x] 6 `evidence/` - `evidence/backfill_2026-08-28/` added: dryrun 5/5, live headless run 5/5
      (first attempt, no retry), grid-filter grep=15, per-step screenshots, log.html/report.html/
      output.xml. Original 2026-08-02 `PROP_0[1-5]_*.png` + `results.json` retained alongside.
- [x] 7 `CHECKLIST.md` - this file.

## B. RF files (pre-existing, verified not modified by this backfill)
- [x] 8 T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource` -
      Area-pattern shape (5 TCs' worth of keywords, `${group}`/`${start_col}` addressing,
      properties-file-driven). Read-only this session.
- [x] 9 Suite `tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot` - 5 TCs
      (Clean State/Insert/Update/Find/Delete), per-TC login/logout. Read-only this session.

## C. Verification gates - fresh re-run this session (evidence in `evidence/backfill_2026-08-28/`)
- [x] 10 robocop - not re-run this session (doc-only backfill; PR #559 cited parity vs Area's
      7-issue baseline, VAR02+DOC02, at merge). No RF/T3 file changed here to re-trigger it.
- [x] 11 `--dryrun` - **5/5 PASS**, this session, 2026-08-28.
- [x] 12 LIVE headless run - **5/5 PASS**, this session, 2026-08-28, first attempt (no retry).
- [x] 13 DB ground-truth - TC05's in-suite assertion (`Verify Object Removed` against
      `OV_PROPERTY`) passed this run, confirming `AUTOTEST_PROPERTY` absent post-delete.
- [x] 14 FULL I-U-D scope - Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all
      present and passed.
- [x] 15 Self-clean confirmed - TC05's DB assertion passing = 0 residual `AUTOTEST_PROPERTY` rows
      in `OV_PROPERTY` after this run (in-suite check via the shared T2, per PR #559's design;
      no separate out-of-suite connection opened this session).
- [x] 16 Hygiene - not re-run this session (no code files touched); PR #559 cited
      `check_bundle_hygiene.py` PASS at merge.

## D. Delivery
- [x] 17 Registry row - already present (`docs/ec_screen_registry.md`, Property row, describes
      the Area-pattern conversion in full).
- [x] 18 Scorecard row - already present (`docs/automation-scorecard.md`, added at PR #559).
- [ ] 19 PR (R9 6-field body) - to be filled in the actual PR for this backfill branch
      (`docs/property-backfill-artifacts`), not hand-typed here at scaffold time.

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/property.md` - refreshed this session to the Area-
      pattern shape (5 TCs, `group=1 start_col=0`, Tract precedent, Business Unit selectors).
- [x] 21 Reuse clause - this IS a reuse/backfill run (screen already implemented via PR #559):
      JOURNAL + evidence + KB map all refreshed this session, not just green tests claimed.

---
**Real facts sourced from:** `gh pr view 559` (body text, quoted verbatim in JOURNAL.md/
property_sow.md), live `robot --dryrun` and `EC_HEADLESS=true robot` runs executed this session
(2026-08-28), `docs/ec_screen_registry.md`'s Property row, and read-only inspection of
`property_page.resource`/`property_iud.robot`/`property_navigator.properties`/
`property_insert.properties`. No claim in this file is invented.
