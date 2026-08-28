# JOURNAL — Country IUD

_Screen: Configuration > Assets > Basic Objects > Country (plain OV, no navigator, date-effective).
View `OV_COUNTRY`. Bank pattern (label-driven, properties-file-driven, T2-consolidated), converted
in PR #428 (merged 2026-08-23). This JOURNAL was backfilled 2026-08-28 as part of the lean-waiver
retirement (`docs/lean-deliverable-backfill-workorder.md`, Batch 6) — the bundle predated the
JOURNAL requirement being restored for Bank/Area-pattern work. Content below is pulled from PR
#428's real body, not invented._

## Built (PR #428, 2026-08-23)
- Rebuilt `pageobjects/Configuration/Assets/Basic_Objects/country_page.resource` (fully rebuilt,
  +161/-54 lines) from the older hardcoded-field-id pattern to the label-driven,
  properties-file-driven, T2-consolidated "Bank pattern" already proven on Bank/State/Object
  List/Account/Cost Centre.
- Rebuilt `tests/Configuration/Assets/Basic_Objects/country_iud.robot` (+47/-41 lines) — 5 TCs
  (Verify Clean State / Insert / Update / Find / Delete).
- New properties files: `testdata/country_insert.properties`, `country_update.properties`,
  `country_form_verify.properties`, `country_grid_verify.properties`.
- Additive-only: `resources/credentials.py` gained `COUNTRY_EC_USER`/`COUNTRY_EC_PASS` (appended
  after the last existing pair, per the owner's 2026-08-22 per-screen-credential standing
  decision).
- Explicit grid Find/Clear Row By Filter wiring (`Find/Clear Country Row By Filter` -> shared T2)
  included **from the start**, not deferred to a later pass.
- This was Batch 2 of a 5-screen parallel conversion batch: Country / County / Regulatory
  Permits / Currency / VAT Code.
- Registry (`workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`) and scorecard
  (`docs/automation-scorecard.md`) rows updated; `grid-filter-standardization-checklist.md`
  Country row marked 15 of 15 done.

## Done well
- Full I-U-D DB-verified vs `OV_COUNTRY` (insert Country Name, update Country Name, delete
  End=Start absent); self-clean confirmed via a fresh (not reused) `oracledb` connection both
  BEFORE the run (code-freeness check) and AFTER (0 residual `AUTOTEST_COUNTRY` rows).
- Field labels ("Country Code"/"Country Name", screen-prefixed, same convention as State/Region)
  and mandatory scope were confirmed via a **live RF field-label recon script BEFORE building**
  (objectForm: 14 ECCell labels / 3 mandatory; updateAttributes: 10 ECCell labels / 2 mandatory) —
  not assumed from a sibling screen's pattern. The recon script was deleted after use (throwaway,
  per repo convention).
- Grid-filter wiring verified as actually FIRING live, not just present in source:
  `grep -o 'name="Find Country Row By Filter"' output.xml` -> 5 hits (Update/Find/Verify-Insert-
  Exists/Verify-Found/Delete call sites).
- No shared T1/T2 file (`resources/common.resource`/`resources/manage_object.resource`) touched —
  the existing `${code_label}` parameter (added on State's PR) was reused unchanged, keeping the
  conversion isolated to Country's own T3 + testdata.
- Live RF run: **5/5 PASS** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05
  Delete). `robot --dryrun` on the full `tests/` tree: 730/730 PASS at the time of the PR.
- robocop on the 2 changed RF files: 9 issues (4 VAR02 + 5 DOC02) — identical in kind/count to the
  State exemplar's own baseline; no new issue classes introduced.

## Done wrong / lessons
- Nothing disclosed in PR #428's body as a defect, flake, or wrong classification for Country
  itself — the PR reports a clean first-pass conversion. (Contrast with sibling screens in later
  batches, e.g. Company's non-reproducible TC05 grid-refresh flake, or Royalty Depositor's
  transient shared-sandbox lockout — Country's own conversion hit neither.)
- The bundle's `country_sow.md`/`README.md` were NOT updated at PR #428 merge time to reflect the
  Bank-pattern conversion — they still described the pre-conversion 2026-06-11 shape (hardcoded
  field ids, `AUTOTEST_CTRY_<timestamp>` code, Playwright-primary framing) until this 2026-08-28
  backfill corrected them. This is exactly the documentation drift the lean-waiver retirement
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) exists to catch.

## Blockers -> resolution
- None disclosed in PR #428 for Country specifically — no hard blockers, no data damage, no
  retry needed on the live run.

## Decisions
- Playwright bundle (`playwright/ec_iud_country.py`, `investigation/`) is NOT rebuilt or extended
  as part of the Bank-pattern conversion or this backfill — kept as a superseded historical
  reference only; the Universal Screen Engine is the owner-decided replacement going forward
  (Section H of the deliverable checklist).
- Fixed test code `AUTOTEST_COUNTRY` (not a per-run timestamped code) adopted to match
  Bank/State/Object List's convention — requires every run to complete TC05 (delete) so the code
  stays free for the next run.
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only (KB map added in this backfill).

## Evidence
- PR #428 (merged 2026-08-23): live RF 5/5 PASS, DB self-clean via fresh connection, filter-fired
  grep (5 hits), robocop 9 issues (baseline-matching), full-tree dryrun 730/730.
- This backfill (2026-08-28): dryrun 5/5 PASS re-confirmed; live headless re-run 5/5 PASS
  (`evidence/rf_backfill_2026-08-28/log.html`, `output.xml`, 26 per-step screenshots); filter-fired
  grep re-confirmed 5 hits; robocop re-confirmed 9 issues (same kind/count); hygiene
  (`py scripts/check_bundle_hygiene.py`) PASS; DB self-clean re-confirmed via TC05's own
  `Code Should Be Absent In View OV_COUNTRY` assertion passing live.
