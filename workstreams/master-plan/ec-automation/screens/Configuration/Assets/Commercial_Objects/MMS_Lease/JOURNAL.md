# JOURNAL — MMS Lease IUD

_Screen: Configuration > Assets > Commercial Objects > MMS Lease (OV, manage-object, no
mandatory nav scope). View `OV_MMS_LEASE`. This JOURNAL was backfilled 2026-08-28 (owner
decision 2026-08-27, Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`, retiring the
2026-08-23/26 lean waiver) — the bundle predated this rule; content below is sourced from
PR #437's real body and commit history, not invented._

## Built

- **Original build (2026-06-12):** standalone Playwright driver
  (`playwright/ec_iud_mms_lease.py`, thin config over the shared `iud_engine.py`) +
  `investigation/` recon scripts, using the older hardcoded-field-id pattern.
- **Bank-pattern conversion (PR #437, merged 2026-08-23, Batch 3 of 5 parallel screens —
  Customer, Field Group, Licence, MMS Lease, Operator Lease):** rebuilt the RF T3
  (`pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource`) and suite
  (`tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot`) to the label-driven,
  properties-file-driven, T2-consolidated pattern used by `bank_page.resource` — added
  explicit grid-filter wiring (`Find MMS Lease Row By Filter` / `Clear MMS Lease Row
  Filter`) from the start, 4 new `testdata/mms_lease_*.properties` files, and an additive
  `MMS_LEASE_EC_USER`/`MMS_LEASE_EC_PASS` credential pair.
- **This backfill (2026-08-28):** SOW/README/JOURNAL/evidence/CHECKLIST/KB-map added around
  the already-merged RF automation. No RF/pageobject files touched.

## Done well

- Live recon-first: navigator scope (no mandatory GO), field labels ("MMS Lease
  Code"/"MMS Lease Name" — screen-prefixed, unlike Field Group's generic "Code"/"Name"),
  and mandatory-field sets in both `objectForm` (3: Code/Name/Start Date) and
  `updateAttributes` (2: Code/Name) were all confirmed via a real insert+select+delete+
  DB-verify cycle on a throwaway record before any config was written.
- IUD-fill-only-needed-fields: Description/Operator confirmed optional and deliberately
  omitted from the properties files.
- Grid-filter wiring included from day one (per the batch's shared ground rules), not
  deferred to a later pass.
- Full I-U-D DB-verified against `OV_MMS_LEASE`: live RF 5/5 PASS (re-confirmed by this
  backfill's own live re-run, 2026-08-28), full `tests/` dryrun 735/735 PASS at the time of
  PR #437, self-clean 0 residual `AUTOTEST_MMS_LEASE` rows via an independent fresh
  connection (both before and after the run, re-verified by this backfill).
- No shared T1/T2 file changes; `credentials.py` change was additive-only (appended after
  the last existing pair).

## Done wrong / lessons

- This screen (and its Batch 3 siblings) were originally delivered under the 2026-08-23
  lean-waiver rule (Section G of the checklist) — SOW/JOURNAL/evidence/CHECKLIST/KB-map
  were skipped at the time, which is exactly what this 2026-08-28 backfill restores. Not a
  defect in the automation itself, but a process gap the owner later closed.
- robocop reports 9 issues on the T3+suite (4 VAR02 + 5 DOC02) — identical in kind and
  count to the Bank/Country baseline, re-confirmed by this backfill's own robocop run
  (2026-08-28). Treated as an accepted, stable characteristic of this pattern family rather
  than something to chase to zero (matches the reviewer's prior acceptance of the same
  count on Bank/Country/other Batch-3 siblings).

## Blockers -> resolution

- No blockers hit during the original PR #437 build per its body (mandatory dropdowns/
  navigator scope were resolved via live recon before config was written, not via
  trial-and-error).
- This backfill's own dryrun + live re-run hit no failures on the first attempt (no retry
  needed).

## Decisions

- RF is the primary, maintained automation going forward; the legacy Playwright driver +
  its `investigation/` recon scripts are kept in the bundle as historical reference only —
  per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` that role is now permanently waived
  in favour of the Universal Screen Engine (`py/engine.py`), so no new Playwright work was
  done here.
- Fixed test code `AUTOTEST_MMS_LEASE` (not a per-run generated code) — confirmed free in
  `OV_MMS_LEASE` before being wired in; every run must complete TC05 (delete) so the code
  stays free for the next run.
- `ec-ui-knowledge/` stays MD-only; the new `mms_lease.md` KB map (added by this backfill)
  transcribes the T3's own Variables-section selectors rather than re-deriving them.

## Evidence

- Original build (2026-06-12): `evidence/mms_lease_0[1-8]_*.png` (8 screenshots) +
  `evidence/mms_lease_results.json` (Playwright reference run).
- PR #437 (2026-08-23): live RF 5/5 PASS, full `tests/` dryrun 735/735 PASS, DB self-clean
  0 residual (cited in the PR body; not re-captured as files at the time — that gap is what
  this backfill's evidence folder now covers).
- This backfill (2026-08-28): `evidence/rf_bank_pattern_2026-08-28/` — dryrun 5/5 PASS
  (`dryrun_output.xml`), live headless run 5/5 PASS (`output.xml`, `log.html`,
  `report.html`), robocop 9 issues (matches baseline), hygiene PASS, DB self-clean
  reconfirmed via fresh connection (0 before, 0 after). See
  `evidence/rf_bank_pattern_2026-08-28/results_summary.md` for exact commands and output.
