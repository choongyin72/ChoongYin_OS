# JOURNAL — County IUD

_Screen: Configuration > Assets > Basic Objects > County (OV, manage-object, no navigator). View `OV_COUNTY`._
_This JOURNAL was backfilled 2026-08-28 (owner decision 2026-08-27 retired the lean waiver introduced
2026-08-23/26 — Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`). Content below is pulled from the real
PR #429 and PR #489 bodies and commit messages, not invented after the fact._

## Built
- **2026-06-11** — original build: hardcoded-field-id Playwright (`playwright/ec_iud_county.py`) + RF pair
  (`county_page.resource` T3, `county_iud.robot`), part of the Basic Objects section (12 screens).
- **2026-08-23, PR #429** ("feat(ec-automation): County IUD suite - Bank-pattern conversion (batch-2)") —
  rewrote `county_page.resource` (T3) and `county_iud.robot` (5-TC suite) from the old hardcoded-field-id
  pattern to the label-driven, properties-file-driven, T2-consolidated **Bank pattern**, alongside
  Country/Regulatory Permits/Currency/VAT Code in parallel isolated worker clones
  (`tmp/batch2_shared_findings.md`). Added 4 new properties files (`county_insert.properties`,
  `county_update.properties`, `county_form_verify.properties`, `county_grid_verify.properties`) and
  additive `COUNTY_EC_USER`/`COUNTY_EC_PASS` credentials. Explicit grid-filter wiring
  (`Find/Clear County Row By Filter`) included from the start, not deferred.
- **2026-08-24, PR #489** ("fix(ec-automation): align County suite to Bank's exact pure-screen-verify
  pattern") — removed two inline DB-verify keywords (`County Should Exist In DB`,
  `County Should Be Updated In DB`) from `county_iud.robot` that `bank_iud.robot` deliberately does not
  have. Targeted alignment fix, not a rebuild — only the suite file changed, no T2/T3/testdata edits.

## Done well
- **Recon-before-build (PR #429):** live-confirmed before writing any code — navigator shape (plain
  Date filter + GO, no mandatory dropdown), screen-prefixed field labels ("County Code"/"County Name",
  not generic "Code"/"Name" — same as State/Region), `OV_COUNTY` view columns via `all_views`/
  `all_tab_columns`, `AUTOTEST_COUNTY` free in `OV_COUNTY` (0 rows) before building, and the
  `objectdates` Delete field id via a live insert+delete probe round-trip before hardcoding it into T3.
- **IUD-fill-only-needed-fields honored:** only County Code/County Name (mandatory) + Start Date +
  Description filled; non-mandatory Master System Code/Name (read-only display), API Code, and the
  State dropdown deliberately left unset.
- **Full I-U-D DB-verified** against `OV_COUNTY` at the time of PR #429: insert (`Code Should Be Present
  In View`), update (`Field Should Equal In View` on NAME/DESCRIPTION), delete (`Verify Object Removed` /
  `Code Should Be Absent In View`) — plus an independent fresh-connection re-read confirming 0 residual
  `AUTOTEST%` rows.
- **Owner-driven consistency fix caught cleanly (PR #489):** when the owner asked why County's suite
  differed from Bank's, the fix was found by directly diffing the two files against `bank_iud.robot`'s
  own documented 2026-08-18 decision ("PURE SCREEN verification... no DB check at all here"), not by
  guessing — the deviation was real, not stylistic.

## Done wrong / lessons
- **PR #429 shipped with an extra DB-verify pattern that Bank had already deliberately dropped.**
  County's original conversion kept two inline `DbVerify` calls (`County Should Exist In DB`,
  `County Should Be Updated In DB`) directly in the `.robot` suite. This was a real deviation from the
  pure-screen-verify convention `bank_iud.robot` already followed (owner decision 2026-08-18) — it went
  unnoticed until the owner explicitly asked why the two suites looked different, at which point PR #489
  fixed it. Lesson: when converting a screen "to the Bank pattern," diff the resulting suite against
  `bank_iud.robot` itself, not just against the shared T2 keywords, to catch style deviations like this
  before merge, not after.
- **Lean-waiver-era gap (this backfill's own reason for existing):** PR #429/#489 were both built and
  merged (2026-08-23/24) before Section G's 2026-08-23 lean-RF-only waiver (and its later retirement in
  Section H, 2026-08-27) — but because County had a *pre-existing* bundle from 2026-06-11 that predated
  the lean rule entirely, no JOURNAL/CHECKLIST update happened at either conversion PR, leaving the SOW/
  README stale (still describing the old hardcoded-field-id shape). This backfill (2026-08-28) is what
  closes that gap.

## Blockers -> resolution
- No hard blockers on either PR #429 or PR #489. PR #429's only pre-build risk (screen-prefixed labels
  breaking the generic `code_label` default used by other screens) was resolved by recon confirming the
  label live and threading `code_label=County Code` through every T2 call before any test ran.

## Decisions
- Keep the original 2026-06-11 Playwright bundle (`playwright/ec_iud_county.py`, `investigation/`) as
  historical reference only — per owner decision 2026-08-27 (Section H), the Playwright driver role is
  now superseded by the Universal Screen Engine; no new Playwright work was done or is planned for this
  screen.
- RF suite (`county_page.resource` + `county_iud.robot`) is the sole maintained automation going forward.
- Fixed test code `AUTOTEST_COUNTY` (not a per-run generated code) — matches the Account/Bank
  convention, requires TC05 (delete) to complete every run so the code stays reusable.

## Evidence
- PR #429: live run 5/5 pass (TC01-05); dryrun 730/730 pass (full tree at that time); robocop 7 issues,
  all VAR02/DOC02 (same classes as Bank/State baseline); fresh-connection DB re-read = 0 residual
  `AUTOTEST%` rows in `OV_COUNTY`; grid-filter wiring confirmed 5 hits in output.xml.
- PR #489: dryrun 792/792 pass (full tree at that time); live run 5/5 pass; fresh-connection DB re-read =
  0 residual `AUTOTEST%` rows.
- This backfill (2026-08-28): see `evidence/` for the re-run captured for this PR — `results.txt`
  (summary + exit code) and `output.xml`/`log.html` if under the 2MB size guidance, otherwise a truncated
  summary in their place.
