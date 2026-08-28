# JOURNAL - Calendar IUD (CD.0024)

_Screen: Configuration > Assets > Date Objects > Calendar. Custom-URL OV, date-effective. View
`OV_CALENDAR`._
_This JOURNAL covers two builds -- the original build (stacked on CD.0023, PR #143) and the
PR #451 Bank-pattern conversion (Batch 6, FINAL screen of the 23-screen conversion pool) -- plus
this backfill pass (Batch 8, 2026-08-28) that brought the docs up to date with the current
automation, per `docs/lean-deliverable-backfill-workorder.md`._

## Built
- **Original build (PR #143-stacked):** full IUD automation for Calendar (OV, date-effective):
  T3, RF suite (4 TCs clean->insert->update->delete, in-suite DB asserts), Playwright flow, recon
  script, evidence, SOW, README, CHECKLIST. 4th of 5 Date Objects screens.
- **PR #451 (2026-08-23, Batch 6 conversion, final of 23):** rebuilt the T3
  (`calendar_page.resource`) and suite (`calendar_iud.robot`) to the label-driven,
  properties-file-driven, T2-consolidated Bank pattern; added
  `testdata/calendar_{insert,update,form_verify,grid_verify}.properties`, dedicated
  `CALENDAR_EC_USER`/`CALENDAR_EC_PASS` credentials, and explicit grid-filter wiring
  (`Find/Clear Calendar Row By Filter`) from day one. Added the missing TC04 Find (prior suite
  had only 4 TCs).
- **This backfill (Batch 8, 2026-08-28):** no automation changes -- added/updated SOW, README,
  JOURNAL (this file), CHECKLIST.md, a new evidence subfolder, and the KB selector map, to bring
  the doc bundle up to date with PR #451's current state.

## Done well
- **Original build:** DB-first + DOM recon confirmed Calendar is the SIMPLEST of the 5: plain
  Bank-family OV with only Code/Name/Start-Date mandatory; the 7 weekday indicator cells
  (R:6-R:12) are optional checkboxes. Checked for a child member grid (`daytimes`/`versions`
  sub-tabs) -- confirmed those are the standard OV objectdates/versions tabs, not a holiday
  child grid. T3 thin; zero shared-file edits; full I-U-D.
- **PR #451:** did not carry the registry's older 2026-06-28 description or a sibling screen's
  shape forward unverified -- a live field-inventory scan (both the New Object and
  updateAttributes forms) confirmed the screen-prefixed "Calendar Code"/"Calendar Name" labels
  (matching Royalty Owner/State's precedent, not the generic "Code"/"Name" Bank/Object List use)
  and reconfirmed the mandatory set via a live `{mandatory:true}` CSS scan. Grid-filter wiring
  included from the start (owner standing instruction) rather than retrofitted later. Zero
  shared-file edits (`resources/manage_object.resource`'s Refresh fallback already handled this
  screen's no-GO shape).
- **This backfill:** re-ran the existing suite (dryrun + live headless) exactly once, first
  attempt, no retry needed -- matches the "don't re-verify from scratch, just capture evidence"
  scope of this task.

## Done wrong / lessons
- **Original build (the real lesson of this screen):** assumed Calendar's list grid was
  `manage_object_nav_nav:form:T_data` (like the 3 term screens before it). Live run: TC02 Insert
  FAILED at `Row Should Exist`. Diagnosis (not retry): the insert had actually persisted (3
  AUTOTEST rows in `ov_calendar` + base `CALENDAR`), so it was a UI-read failure, not an insert
  failure. A grid dump showed `manage_object_nav_nav:form:T_data` ABSENT and no GO button --
  Calendar is a custom-URL OV (grid `nav:form:T_data`, no navigator GO, reload via toolbar
  Refresh; cf. Account / Regulatory Permits). Fixed the table id; T2 Save And Refresh List
  auto-falls back to Refresh Screen when no GO. Re-run = 4/4. Cleaned the 3 residual rows
  (End=Start via UI) before re-running -- self-clean restored. Lesson: a screen's grid id / GO
  presence is recon ground-truth, not an assumption from siblings. Also: clone substitution
  missed "Doc Date Term" in the Playwright TEST_NAME -> fixed to "AUTOTEST Calendar".
- **PR #451:** none disclosed in the PR body beyond confirming ground truth live rather than
  trusting the registry's prior (pre-Bank-pattern) description (no flake, no wrong
  classification, no shared-file regression reported).
- **This backfill:** none -- live run passed 5/5 first attempt; hygiene PASS; no automation
  touched.

## To improve
- Original-build era note (retained): the next screen, Calendar Collection (CD.0105), might
  genuinely have a child member grid given the "collection" name -- recon fully before deciding
  plain-OV vs PC (it turned out to be plain OV too, per Calendar Collection's own JOURNAL).

## Blockers -> resolution
- None at either build, and none during this backfill's re-run/re-check.

## Decisions
- Left the weekday checkboxes at default (optional) -- minimal valid insert. Holds unchanged
  across both builds.
- **PR #451:** dedicated per-screen credential pair (additive only, owner standing decision
  2026-08-22); explicit grid-filter wiring from day one rather than a follow-up pass.
- **This backfill:** kept the original Playwright bundle/investigation/evidence artifacts as
  historical record rather than deleting them; added a clearly-dated new evidence subfolder
  instead of overwriting, per items 4/5's permanent waiver (Universal Screen Engine supersedes
  hand-written Playwright drivers going forward, so no new one was built).

## Evidence
- **Original build:** live RF 4/4 PASS; Playwright ALL PASS (`evidence/results.json`).
- **PR #451:** live `EC_HEADLESS=true` run 5/5 PASS (TC01 Verify Clean State, TC02 Insert, TC03
  Update, TC04 Find, TC05 Delete). Fresh-connection DB assertion
  (`SELECT COUNT(*) FROM ov_calendar WHERE code = 'AUTOTEST_CALENDAR'`) = 0 before and after.
  `output.xml` grep on `Find Calendar Row By Filter` = 5 hits. Robocop on the 2 changed files = 9
  issues (4 VAR02 + 5 DOC02), matching the established baseline. Full-tree `robot --dryrun` =
  750/750 (baseline going in was 749/749).
- **This backfill (2026-08-28):** dryrun 5/5 PASS (`_dryrun/output.xml`); live headless 5/5 PASS,
  first attempt, no retry (`_live/output.xml`, 364KB, 24 screenshots). Independent
  fresh-connection self-clean re-check: `SELECT COUNT(*) FROM OV_CALENDAR WHERE CODE =
  'AUTOTEST_CALENDAR'` = 0; `SELECT COUNT(*) FROM OV_CALENDAR` = 6 (unchanged, matches the SOW's
  original recon count). `output.xml` grep on `Find Calendar Row By Filter` = 15 hits (this
  suite's own filter usage across TC02-TC05). Robocop re-run on the T3+suite = 9 issues (same
  parity as PR #451's own stated baseline). Full-tree `robot --dryrun` = 883/883 (repo has grown
  since PR #451's 750/750 baseline; no regression). Hygiene `py scripts/check_bundle_hygiene.py`
  = PASS. Screenshots + `output.xml` saved to `evidence/rf_backfill_2026-08-28/` (see
  `RESULTS.md` there).
