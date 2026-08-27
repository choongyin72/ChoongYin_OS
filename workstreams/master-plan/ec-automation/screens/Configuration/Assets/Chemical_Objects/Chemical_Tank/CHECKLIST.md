# Chemical Tank - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

**Status:** original OV-GM IUD build (2026-07-30, PR #244) + Area-pattern RF conversion
(2026-08-26, PR #549) + documentation/evidence backfill (2026-08-28, Batch 4 of
`docs/lean-deliverable-backfill-workorder.md`, per owner decision 2026-08-27 retiring the
lean waiver in Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).

## Step 0 - check-existing gate
- [x] 0a KB map existed (`ec-ui-knowledge/screens/chemical_tank.md`) — refreshed by this backfill
      for the PR #549 conversion (was stale at the 2026-07-30 pre-conversion state).
- [x] 0b grep `workstreams/master-plan/ec-automation` for `chemical_tank` -> only this build (page
      object, suite, driver, testdata, bundle) — confirmed live via grep during this backfill.
- [x] 0c reused shared engine (ec_object_iud.py) + DbVerify + shared T2 `manage_object.resource`
      (thin driver/T3, no per-screen plumbing duplicated).

## A. Bundle artifacts
- [x] 1 `chemical_tank_sow.md` — refreshed with Section 6 (PR #549 conversion + `__FIRST__` gotcha).
- [x] 2 `README.md` — refreshed with real dryrun/live/DB-self-clean commands.
- [x] 3 `JOURNAL.md` — refreshed with the 2026-08-26 (PR #549) and 2026-08-28 (this backfill) entries.
- [ ] 4 Playwright flow — **N/A per Section H of the checklist**: item 4 (Playwright driver) stays
      waived for Bank-/Area-pattern conversions; the pre-existing `py/chemical_tank_iud.py` from the
      2026-07-30 build satisfies it incidentally but is not required by this backfill.
- [ ] 5 `investigation/` — **N/A per Section H**: item 5 (investigation/ recon scripts) stays
      waived; the pre-existing `investigation/recon.py` from the 2026-07-30 build satisfies it
      incidentally but is not required by this backfill.
- [x] 6 `evidence/` — pre-existing `ct_0[1-5]_*.png` + `results.json` from 2026-07-30, plus this
      backfill's fresh live-run artifacts (see `evidence/backfill_2026-08-28/`).
- [x] 7 `CHECKLIST.md` — this file, refreshed.

## B. RF files (pre-existing, untouched by this backfill)
- [x] 8 T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_tank_page.resource`
      (rewritten to Area's 5-TC shape by PR #549; NOT modified by this backfill).
- [x] 9 Suite `tests/Configuration/Assets/Chemical_Objects/chemical_tank_iud.robot`
      (5 TCs, per-TC login/logout, post-PR #549; NOT modified by this backfill).

## C. Verification gates (real evidence citations; this backfill did not rebuild the automation)
- [x] 10 robocop parity — PR #549 body: 13 issues, identical count to Area's/Facility Class 1's own
      baseline (confirmed side-by-side robocop run per PR #549's body).
- [x] 11 `--dryrun` — PR #549 body: full-tree `robot --dryrun tests/` -> 850/850 passed, 0 failed
      (before and after PR #549's fix).
- [x] 12 LIVE run — PR #549 body: `EC_HEADLESS=true robot tests/.../chemical_tank_iud.robot` ->
      TC01-TC05 all PASS (5/5, supersedes the original 2026-07-30 4/4). This backfill's own fresh
      re-run result: see `evidence/backfill_2026-08-28/` (result cited below).
- [x] 13 DB ground-truth — `Verify Object Removed`/`Verify Object Insert Exists` (shared T2,
      `manage_object.resource`) against view `OV_CHEM_TANK`; PR #549 body: fresh `oracledb`
      connection, `SELECT CODE, NAME FROM OV_CHEM_TANK WHERE CODE LIKE 'AUTOTEST%'` -> `[]`.
- [x] 14 FULL I-U-D — Insert (TC02) + Update (TC03) + Delete (TC05) + Find (TC04) all present.
- [x] 15 Self-clean — PR #549 body: fresh-connection re-read -> 0 residual rows, before and after
      the live run.
- [x] 16 Hygiene — pre-existing driver/T3 already hygiene-clean per the 2026-07-30
      `verify_screen.py` OVERALL PASS; no new Playwright/investigation code added by PR #549 or
      this backfill to re-check.

## D. Delivery
- [x] 17 Registry row — `docs/ec_screen_registry.md` Chemical Tank row MODIFIED by PR #549 (Area
      conversion note, live RF 5/5, dryrun 850/850, self-clean, `__FIRST__` gotcha documented inline).
- [x] 18 Scorecard row — pre-existing scorecard entry from the 2026-07-30 build; not required to
      change shape by this backfill (RF suite structure change already reflected in the registry row).
- [x] 19 PR — this backfill's own PR (R9 6-field body); PR #549 already carried its own body for
      the RF conversion.

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/chemical_tank.md` — refreshed by this backfill: 5-TC/Area
      pattern, explicit navigator properties, the `__FIRST__` Op Production Unit quirk, last-verified
      date updated to 2026-08-28.
- [x] 21 Reuse clause — satisfied: JOURNAL + evidence + KB map all refreshed/produced by this
      backfill for the PR #549 conversion, not just passing tests.

_Items 4/5 marked N/A per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H (2026-08-27): the
Playwright driver + investigation/ recon scripts stay permanently waived for Bank-/Area-pattern
conversion work — the Universal Screen Engine is the owner-decided replacement going forward. This
screen happens to already have both from its original 2026-07-30 pre-Area-pattern build; that is
pre-existing/incidental, not something this backfill or PR #549 was required to produce._
