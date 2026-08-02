# JOURNAL - Division Order (RC.0058) OV-GM IUD

## 2026-08-02
- **Branch:** `feature/build-division-order-iud`. Previously parked as "misclassified - genuinely TV
  not OV-GM, needs the TV generator." That classification was WRONG (corrected in a separate
  investigate-only pass earlier the same day - see the park record's "RE-SCOPED" note): the screen's
  LABEL matches 3 classes (`BEARER`, `DIVISION_ORDER`, `DIVISION_ORDER_SHARE`); the original
  investigation only checked the first one listed. `DIVISION_ORDER` itself is `CLASS_TYPE=OBJECT`,
  `TIME_SCOPE_CODE=VERSIONED` (a normal OV-GM screen), base=`CONTRACT` - the SAME base table as
  Royalty Contract, discriminated only by `CLASS_NAME`.
- **Recon:** navigator = Date (optional, G:0) + mandatory Business Unit dropdown (G:1) + optional
  2nd dropdown (G:2) - same shape as Royalty Contract. Real populated scope resolved via the 2
  existing `OV_DIVISION_ORDER` rows: both scoped under Contract Area `US_LOUISIANA_NORTH`
  ("Louisiana North"), owned by Business Unit `ROYALTY_US` ("Royalty USA") - matches the treeview
  path (`EC Revenue > Royalty > Royalty USA > Division Order`) exactly. Both effective from
  `2003-01-01`.
- **Built** (generator `tmp/gen_ovgm.py`, `nav_value="Royalty USA"`,
  `extra_dropdowns=[["Contract Template","__FIRST__"],["Contract Area","Louisiana North"]]`,
  `start_date="2003-01-01"`): label-driven T3; thin driver `py/division_order_iud.py`.
- **2 known-pattern fixes applied on the first pass** (both already seen on sibling screens this
  session, so fixed immediately rather than re-discovered from scratch):
  1. Nav-dropdown id: the generator's default template assumed Date+dropdown share one navigator
     group, but this screen has them in SEPARATE groups (`G:0`=Date, `G:1`=Business Unit) - same gap
     as Property/Royalty Contract. Corrected to `nav:form:G:1:R:1:C:0:dd`.
  2. End Date: not flagged mandatory on the live scan, but Save genuinely rejects without it -
     same as Royalty Contract/Contract. Added `INSERT_END_DATE = "2099-12-31"`, matching precedent.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright driver 8/8. DB residual 0.

## Lessons
- Both fixes needed here were ALREADY-KNOWN patterns from Property/Royalty Contract/Contract - this
  screen built cleanly on the second driver run because the recon step correctly anticipated them
  from the sibling screens' history, rather than treating each new screen as a blank slate.
- Confirms the earlier investigate-only finding was correct and actionable: once the TV
  misclassification was corrected, this screen needed zero new capability - just the two already-
  cataloged OV-GM quirks.
