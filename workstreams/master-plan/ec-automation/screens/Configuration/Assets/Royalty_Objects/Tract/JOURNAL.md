# JOURNAL - Tract (RC.0056) OV-GM IUD

_Screen: Configuration > Assets > Royalty Objects > Tract (OV-GM groupmodel, Unit-Agreement-gated).
View `OV_TRACT`. This JOURNAL was backfilled 2026-08-28 under the retired-lean-waiver work order
(`docs/lean-deliverable-backfill-workorder.md`, Batch 4; Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) - the bundle's SOW/README/evidence predated the JOURNAL rule;
PR #555 (the Area-pattern conversion) is the source of the "Built" and "Done well/wrong" content
below, pulled from its real PR body, not invented._

## Built

### Original build (2026-06-26)
- 5th Royalty Objects screen, 1st OV-GM (gated) screen in the folder. RF-only from the start (no
  Playwright bundle), following the Transport System OV-GM exemplar precedent.
- Recon confirmed: OV-GM, grid `manageObject:form:T_data` (lazy redraw), navigator gated by Unit
  Agreement dropdown + GO, insert mandatory Code/Name/Start Date/Unit Agreement dd, delete via
  `objectdates` End Date = Start Date.
- Live 4/4 against the then-current sandbox web app; per-run timestamped test code
  `AUTOTEST_TR_<run>`.

### Area-pattern conversion (PR #555, merged 2026-08-26) - the real, most important story
- **PR #555's OWN FIRST COMMIT WRONGLY DECLINED the conversion.** It reasoned that Tract's
  navigator spans two separate DOM groups (`nav:form:G:0` Date, `nav:form:G:1` Unit Agreement) and
  concluded this didn't fit Area's single-group cascade shape - superficially resembling the
  disqualifying "per-field navigator groups" case documented in
  `docs/navigator-screens-not-matching-area.md`. That wrong conclusion was logged to that doc as a
  live disqualifying entry.
- **The owner corrected this same day.** A fresh live DOM recon found: `G:0`'s Date field already
  carries a non-empty default on load (today's date) and needs NO fill at all - it was never a
  real second mandatory group in practice. `G:1`'s Unit Agreement dropdown, confirmed live via its
  `{mandatory:true} MandatoryCellStyle` class, is the ONLY mandatory-and-empty navigator field.
  Tract's REAL navigator requirement is therefore exactly ONE mandatory dropdown - structurally
  the SAME shape as Area's own single-dropdown navigator, just living at group 1 / column 0
  instead of group 0 / column 1.
- The wrongly-added row was removed from `docs/navigator-screens-not-matching-area.md` with an
  explicit correction-log entry (not silently deleted - transparency over silent rewrite), and
  Tract was converted to the full Area pattern in the same PR (a corrected commit added on top of
  the same branch/PR number, not a new PR).
- **Shared-keyword extension:** to make the conversion possible, the shared T2 `Apply Navigator
  From Properties` keyword (`resources/manage_object.resource`) gained two new OPTIONAL,
  backward-compatible arguments: `${group}=0` and `${start_col}=1`. Defaults preserve every
  existing caller unchanged (Area/Well Hookup/Contract/Meter/etc. all still target
  `nav:form:G:0:...C:1..C:N`); Tract calls it as `group=1 start_col=0`. Proven backward-compatible
  via a full-tree dryrun (874/874 unchanged before/after the edit) plus live 5/5 regression
  canaries on 2 existing callers of the keyword's old 2-arg form (Area, Meter).
- **Field-reuse rule applied:** the navigator's Unit Agreement value
  (`testdata/tract_navigator.properties`, "Unit Agreement 1") is reused IDENTICALLY in the insert
  form's own Unit Agreement field (`testdata/tract_insert.properties`) - the same value must gate
  both the nav scope and the objectForm's own distinct Unit Agreement parent dd, or the inserted
  row is invisible under the OV-GM filter.
- Full rebuild delivered: 5 TCs (added TC04 Find), per-TC Login/Logout
  (`TRACT_EC_USER`/`TRACT_EC_PASS`), fixed test code `AUTOTEST_TRACT` (confirmed free live via a
  fresh oracledb connection, replacing the old per-run timestamped code), properties-file-driven
  insert/update/verify (`testdata/tract_{navigator,insert,update,form_verify,grid_verify}.
  properties`), explicit `Find/Clear Tract Row By Filter` wired into Update/Find/Verify-Found/
  Delete, zero inline DB-verify calls left in the `.robot` file.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place (not new rows) to record both the wrong conclusion and its correction.

### This backfill (2026-08-28, Batch 4)
- Refreshed `tract_sow.md` (dev story section, test-data table, navigator classification) and
  `README.md` (exact commands, DB self-clean query, Area-pattern facts, the wrong-then-corrected
  story) to reflect PR #555's conversion; both predated the JOURNAL rule and still described the
  original 2026-06-26 CLP-sandbox-era, per-run-timestamped-code shape.
- Added this `JOURNAL.md`, `CHECKLIST.md`, and the KB selector map
  `ec-ui-knowledge/screens/tract.md` (new - did not exist before).
- Added `evidence/backfill_2026-08-28/` (fresh dryrun + live headless re-run of the already-proven
  Area-pattern suite) - no automation code touched.

## Done well
- Full I-U-D DB-verified vs `OV_TRACT` (insert Tract Code/Name, update Tract Name, delete
  End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb connection during this
  backfill's own live re-run (`AUTOTEST_TRACT` count = 0, no `AUTOTEST%` residual rows).
- Live headless re-run this session: **5/5 PASS on the FIRST attempt** (TC01-TC05), no retry
  needed, no flake hit.
- Robocop parity re-confirmed this session: **7 issues** on the 2 changed screen files
  (`tract_page.resource` + `tract_iud.robot`), cross-checked live against
  `area_page.resource`/`area_iud.robot` (also **7 issues**, same DOC02/VAR02 kind) - genuine
  parity, not just cited from the PR body.
- Full-tree dryrun of the Tract suite alone re-confirmed: 5/5 PASS.
- Filter-fired grep re-confirmed: `grep -c "Find Object Row By Filter"` on this session's own
  live-run `output.xml` -> **15 hits**, matching the PR #555 body's own citation.
- Zero inline DB-verify calls confirmed via grep on `tract_iud.robot` (pure screen verification).
- `py scripts/check_bundle_hygiene.py` -> **RESULT: PASS** (one unrelated pre-existing WARN about
  a Contract Area `investigation/` script, not related to Tract).

## Done wrong / lessons

**This is the single most important fact about this screen's history - captured honestly, not
softened:** PR #555's own first commit wrongly classified Tract as NOT fitting the Area pattern,
based on a surface-level read of its navigator DOM shape (two separate `G:0`/`G:1` groups) that
superficially resembled the genuinely-disqualifying "per-field navigator groups" case. The mistake
was not verifying, field-by-field, whether each group was ACTUALLY mandatory-and-empty on live
load - `G:0`'s Date field was defaulted and needed no fill, so the "two mandatory groups" premise
was false from the start. This is the exact class of error `feedback_verify_each_field_not_
shape_match.md` warns against: "fit/no-fit calls need per-field live mandatory+empty checks, not
'shape resembles a known case'." The owner caught it and directed a fresh live recon, which
resolved it correctly the same day. The wrong conclusion was logged transparently (not deleted) in
`docs/navigator-screens-not-matching-area.md`'s correction log, and the registry/scorecard rows
document both the wrong turn and the correction in the same text - nothing was smoothed over.

**Field-reuse rule** was a real, deliberate design decision worth calling out clearly (not a
mistake): the Unit Agreement value used to gate the navigator scope had to be re-used, verbatim,
as the value filled into the insert form's own Unit Agreement dropdown - a screen-specific
instance of the owner's general field-reuse rule, applied correctly from the start of the
corrected build (not discovered via a failed insert).

- No other real regression or wrong turn was disclosed in PR #555's own body for the corrected
  conversion itself.
- **This backfill's own live re-run hit no flake** - 5/5 PASS on the first attempt, unlike some
  other screens in this backfill program that hit environment-wide chrome/node process pile-ups.
  Noted here for completeness, not because there was a problem to disclose.

## Blockers -> resolution
- No blockers during this backfill (documentation/evidence-only; the live re-run passed clean on
  the first attempt).
- The only real blocker in this screen's whole history was PR #555's own wrong-then-corrected
  classification (see "Done wrong / lessons" above) - resolved same-day by owner correction + live
  re-recon, not by trial-and-error.

## Decisions
- Playwright bundle stays waived permanently for this screen - it never had one (RF-only since the
  original 2026-06-26 build, per the OV-GM exemplar precedent), and owner decision 2026-08-27
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) confirms no new Playwright bundle is built for
  Area-pattern work regardless. The Universal Screen Engine is the owner-decided replacement going
  forward.
- The RF suite is the sole maintained/live test for this screen.
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build (2026-06-26): `evidence/tract_tc0[1-4]_*.png` (4 screenshots, pre-Area-pattern
  4-TC shape - no TC04 Find existed yet).
- PR #555 conversion (2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), 15 `Find
  Object Row By Filter` hits in output.xml, robocop 7 issues (parity with Area), full-tree dryrun
  875/875, DB self-clean 0/0 (fresh oracledb, before+after) - all cited in the PR body.
- This backfill (2026-08-28, `evidence/backfill_2026-08-28/`): `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless, first attempt, no retry,
  `log.html`/`report.html`/`output.xml`), a re-confirmed 15-hit filter-fired grep, a re-confirmed
  7-issue robocop parity check against Area's own baseline, a fresh-connection DB self-clean
  (`OV_TRACT`: `AUTOTEST_TRACT` count = 0, no `AUTOTEST%` residual rows), and `py
  scripts/check_bundle_hygiene.py` -> `RESULT: PASS`.
