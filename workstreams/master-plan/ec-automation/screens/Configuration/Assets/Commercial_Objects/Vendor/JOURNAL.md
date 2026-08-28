# JOURNAL — Vendor IUD

_Screen: Configuration > Assets > Commercial Objects > Vendor (OV, date-effective, plain Bank
pattern, no navigator). View `OV_VENDOR`. This JOURNAL was backfilled 2026-08-28 (owner
decision 2026-08-27 retired the 2026-08-23/26 lean waiver — Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`); content below is pulled from the real conversion PR
#439 body/commit (merged 2026-08-23, Batch 4 of the Bank-pattern conversion project), not
invented after the fact._

## Built (PR #439, 2026-08-23)
- Converted `pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource` (T3)
  from the older hardcoded-field-id pattern to the label-driven, properties-file-driven,
  T2-consolidated "Bank pattern", reusing shared `resources/manage_object.resource` keywords.
- Rebuilt `tests/Configuration/Assets/Commercial_Objects/vendor_iud.robot` — 5 TCs
  (clean-state / insert / update / find / delete), per-TC login/logout on one shared browser.
- New testdata files: `vendor_insert.properties`, `vendor_update.properties`,
  `vendor_form_verify.properties`, `vendor_grid_verify.properties`.
- Explicit grid-filter keyword `Find/Clear Vendor Row By Filter` wired in from day one
  (delegates to T2's `Find/Clear Object Row By Filter`) — matches the owner's 2026-08-22
  instruction that all screens should "utilise same filter feature" as Account.
- Additive `VENDOR_EC_USER`/`VENDOR_EC_PASS` in `resources/credentials.py`.
- Registry row (`docs/ec_screen_registry.md`) + scorecard row (`docs/automation-scorecard.md`)
  + the grid-filter-standardization checklist (25/25) + bank-pattern-conversion checklist,
  all updated in the same PR.
- **This backfill pass (2026-08-28):** added `vendor_sow.md` v2.0 section, this JOURNAL,
  `CHECKLIST.md`, a fresh evidence capture under `evidence/rf_backfill_2026-08-28/`, and the
  KB selector map `ec-ui-knowledge/screens/vendor.md`. No automation file touched.

## Done well
- Live recon before writing config — the mandatory field set (Code, Name, Start Date, ERP
  Vendor Code, Official Name, Vendor Group dropdown) was confirmed live on BOTH `objectForm`
  and `updateAttributes` via throwaway RF recon scripts (deleted before commit), not
  extrapolated from a similar-looking screen (Customer).
- Vendor Group's real first dropdown option (`Contract Owner Vendor`) was read back live and
  used as a literal string for the TC02 round-trip form-compare, rather than the `__FIRST__`
  sentinel — avoiding the VAT Code gotcha from Batch 2 (`__FIRST__` never resolves to literal
  text for a comparison assertion).
- Grid columns (Code/Name/Start Date/End Date) were confirmed from an existing row's raw cell
  text, not assumed to match Bank's convention blind.
- Full I-U-D scope present (not I/D-only) — TC03 Update exercises Name + Description.
- Live 5/5 pass, DB self-clean confirmed via a fresh (not reused) oracledb connection: 0
  residual `AUTOTEST_VEND` rows in `OV_VENDOR` both before TC01 and after TC05.
- No shared `resources/manage_object.resource` or `resources/common.resource` edits — the
  screen-specific behavior stayed entirely in the T3 page object.
- robocop after conversion: 7 issues (2 VAR02 + 5 DOC02) — fewer than the then-established
  9-issue baseline for the batch, no new issue classes introduced.

## Done wrong / lessons
- No live-run defect or flake was disclosed in PR #439's body for this screen — the
  conversion went through with mandatory-field recon done up front, avoiding the
  extrapolation mistake the owner had flagged on other screens in this same program
  (assuming a "similar-looking" screen's navigator/field shape instead of checking live).
- This backfill pass itself found no discrepancy on re-run: dryrun 5/5, live 5/5, robocop 7
  issues (same count as PR #439 cited), hygiene PASS, DB self-clean 0 residual — the original
  "done" claim from 2026-08-23 holds up against a fresh 2026-08-28 verification.

## Blockers → resolution
- None disclosed in PR #439 for this screen specifically (it shared a batch PR with State
  Lease/Cost Object Mapping/DOA Credit Limit/Product Description; no Vendor-specific blocker
  called out in the "Rules applied" section).
- This backfill pass hit no live-run or tooling blocker: the live suite passed on the first
  attempt (no retry needed per the process rule).

## Decisions
- Fixed test code `AUTOTEST_VEND` (not a per-run timestamped code) is used, matching Bank's/
  Customer's own convention — each run must complete TC05 (delete) so the code is free for
  the next run; EC never lets a deleted code be reused otherwise.
- Playwright driver + `investigation/` recon scripts are permanently waived for this
  Bank-pattern screen (owner decision 2026-08-27, Section H) — the pre-existing, older
  Playwright bundle in this folder predates PR #439's conversion and is left untouched as
  historical reference, not refreshed or extended.
- SOW/README/JOURNAL/evidence/CHECKLIST/KB are the six artifacts restored by this backfill;
  nothing else in the bundle needed regenerating since the underlying automation was already
  correct and merged.

## Evidence
- Original PR #439 (merged 2026-08-23): live 5/5, DB self-clean 0 residual, filter-fired 5x
  in output.xml, robocop 7 issues, full `tests/` dryrun 740/740.
- This backfill (2026-08-28): dryrun 5/5 PASS, live 5/5 PASS (first attempt, no retry), grid-
  filter fired 5x (`grep -c 'name="Find Vendor Row By Filter"' output.xml`), DB self-clean 0
  residual `AUTOTEST_VEND` rows in `OV_VENDOR` via a fresh connection, robocop 7 issues (2
  VAR02 + 5 DOC02, same as original), repo-wide hygiene PASS. Artifacts:
  `evidence/rf_backfill_2026-08-28/output.xml`, `log.html`, `results-summary.txt`.
