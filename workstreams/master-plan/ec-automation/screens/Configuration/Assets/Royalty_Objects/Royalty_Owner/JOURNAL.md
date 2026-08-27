# JOURNAL — Royalty Owner IUD

_Screen: Configuration > Assets > Royalty Objects > Royalty Owner (RC.0051). OV, date-effective.
View `OV_ROYALTY_OWNER`. This JOURNAL is backfilled 2026-08-28 (Batch 8 of
`docs/lean-deliverable-backfill-workorder.md`) — the bundle's SOW/README/playwright/evidence
predate the 2026-08-27 owner decision that restored JOURNAL/CHECKLIST/KB-map to Bank-/Area-pattern
work; this file is built from PR #447's real body/commits, not invented after the fact._

## Built (2026-08-23, PR #447 — Batch 5 Bank-pattern conversion)
- Rebuilt `royalty_owner_page.resource` (T3) from the older hardcoded-field-id/generated-code
  pattern to the label-driven, properties-file-driven, T2-consolidated "Bank pattern" (matching
  Bank/State), with **explicit grid-filter wiring included from day one** (`Find/Clear Royalty
  Owner Row By Filter`, delegating to T2 `Find Object Row By Filter`/`Clear Object Row Filter`).
- Rebuilt `royalty_owner_iud.robot` suite (5 TCs: clean-state, insert, update, find, delete) to the
  same zero-argument, friendly-narrative wrapper style as Bank/State/Object List.
- New `testdata/royalty_owner_{insert,update,form_verify,grid_verify}.properties` (properties-file
  test data, replacing inline/generated values).
- Additive-only `resources/credentials.py` change (`ROYALTY_OWNER_EC_USER`/`_PASS`) — every EC
  screen gets its own dedicated credential pair per standing decision; no shared-file edits to
  `manage_object.resource`/`common.resource`.
- Registry (`docs/ec_screen_registry.md`), scorecard (`docs/automation-scorecard.md`), and the two
  standardization checklists (`grid-filter-standardization-checklist.md`,
  `bank-pattern-conversion-checklist.md`) updated in the same PR.

## Done well
- **Recon-first, no guessing:** a live field-inventory scan of `objectForm`/`updateAttributes`
  (not an assumption carried over from Bank/State) confirmed the real mandatory trio (Royalty
  Owner Code / Royalty Owner Name / Start Date), the screen-prefixed label convention ("Royalty
  Owner Code"/"Royalty Owner Name", not the generic "Code"/"Name" Bank/Object List use — same
  pattern as State), and that Start Date is Insert-only (absent from `updateAttributes` — 28
  ECCell labels starting at Royalty Owner Code/Name/Official Name..., no Start/End Date).
- Confirmed the screen is a standard manage-object OV shape (no navigator) and explicitly NOT a
  multi-party-ownership/document structure that could have caused a scope mismatch.
- Full I-U-D DB-verified against `OV_ROYALTY_OWNER`: live 5/5 pass
  (`EC_HEADLESS=true robot tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot`).
  Fresh independent `oracledb` connection query on `OV_ROYALTY_OWNER.CODE` confirmed 0 residual
  `AUTOTEST_ROYALTY_OWNER` rows after the suite completed (TC05 delete cleaned up).
- `output.xml` grep confirmed `Find Royalty Owner Row By Filter` fired exactly 5 times — the
  explicit grid-filter wiring is real, not decorative.
- Verify-row-identity-before-write discipline: T2's `Update Object From Properties`/`Delete Object
  Via End Date` (shared, unmodified) read back Code from the selected row before writing —
  inherited for free by reusing T2 rather than re-implementing the write path.
- Full verification chain run for real: robocop (9 issues — 4 VAR02 + 5 DOC02, matching the
  established Bank-pattern baseline exactly, not a new/different count), `robot --dryrun` on the
  full `tests/` tree (745/745 pass at PR time), live 5/5, DB self-clean via fresh connection,
  output.xml filter-fired grep.
- Isolated sparse-checkout clone under `Workplaces/royalty_owner/`, own feature branch — no
  shared-file edits, no risk to other screens' T2/T1 layers.

## Done wrong / lessons
- None disclosed as a defect in PR #447's body — the conversion is described as a clean rebuild
  with no reported flake, wrong classification, or shared-file regression. (Distinct from some
  sibling screens in this same Royalty Objects family — e.g. Tract, which needed a real per-field
  mandatory/empty recheck rather than a shape-match assumption; Royalty Owner's own recon did not
  surface an equivalent gotcha.)
- Backfill-session note (2026-08-28): the original bundle's SOW/README (dated 2026-06-25, predating
  PR #447) were not updated at conversion time to reflect the Bank-pattern rebuild — they still
  described the pre-conversion mechanics. This JOURNAL + the SOW/README touch-ups in this backfill
  bring the docs back in line with what the code actually does today, per the retired-lean-waiver
  work order (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).

## Blockers -> resolution
- No hard blockers reported in PR #447. The only "gotcha" called out was a documentation risk, not
  a functional one: the screen-prefixed label convention ("Royalty Owner Code"/"Royalty Owner
  Name") had to be confirmed live rather than assumed from Bank/Object List's generic "Code"/
  "Name" labels — resolved by the live field-inventory scan before any config was written (same
  discipline as State/Calendar's later conversions).

## Decisions
- Reuse T2 `manage_object.resource` and T1 `common.resource` as-is — no shared-file edits. Royalty
  Owner gets its own dedicated credential pair (`ROYALTY_OWNER_EC_USER`/`_PASS`) per standing
  decision, added additively to `credentials.py`.
- Playwright bundle (`playwright/ec_iud_royalty_owner.py`) predates the Universal Screen Engine
  decision and was left untouched by PR #447 and by this backfill — per Section H of the
  checklist, no NEW Playwright work is required going forward, but an existing one is not deleted
  either.
- Fixed test code `AUTOTEST_ROYALTY_OWNER` (not a generated unique code), matching Bank/State/
  Object List's convention — reusable across runs as long as every run completes TC05 delete.

## Evidence
- RF live run at PR #447 time: 5/5 pass (cited in the PR body, not re-captured as files in the
  original bundle).
- RF live run captured for this backfill (2026-08-28): `evidence/2026-08-28_backfill_run/` — 5/5
  pass, `output.xml` + 8 step screenshots. See `evidence/EVIDENCE-SUMMARY.md` for the full
  breakdown and the independent re-verification (robocop parity, dryrun count, fresh-connection
  DB self-clean, filter-fired grep).
- Pre-conversion evidence (2026-06-25 build): `evidence/royalty_owner_tc01_clean.png` ..
  `royalty_owner_tc04_deleted.png` (kept, not overwritten).
