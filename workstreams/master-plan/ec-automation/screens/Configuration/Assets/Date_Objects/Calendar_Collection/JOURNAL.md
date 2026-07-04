# JOURNAL - feature/calendar-collection-iud (CD.0105 Calendar Collection)

## Built
- Full IUD automation for Calendar Collection (OV, date-effective, custom-URL): T3, RF suite (4 TCs
  clean->insert->update->delete, in-suite DB asserts), Playwright flow, recon, evidence, SOW, README, CHECKLIST.
- 5th/last of 5 Date Objects screens. Built to the 19-item IUD deliverable standard.

## Done well
- Recon FIRST (the Calendar lesson): confirmed grid `nav:form:T_data` + no GO (custom-URL OV) and the
  simplest form (Code/Name/Start Date only) BEFORE cloning -> zero surprises, clean clone of the Calendar
  bundle (the proven custom-URL exemplar).
- Confirmed the "collection" does NOT make this a parent-child screen at the object level: the member
  calendars are a separate child grid; the object IUD is plain Code/Name/Start Date.
- T3 thin; zero shared-file edits; full I-U-D.

## Done wrong / corrected
- Clone left the lowercase test tag as `calendar` -> fixed to `calendar-collection`. (Same short-token
  clone-sub gap noted on Calendar; minor.)

## To improve
- A clone helper that takes a token map (incl. short label + tag variants) would remove these tag/name
  sub-misses across sibling clones. Worth a small generator if more Date-Objects-like batches come.

## Blockers -> resolution
- None.

## Decisions
- Object-level IUD only (member-calendar child grid out of scope -- it is not the object's identity).
  Stacked on CD.0024 (PR #144). Completes Date Objects 5/5.

## Evidence
- Live RF 4/4 PASS; Playwright ALL PASS (evidence/results.json).
- DB: TC02 `Code Should Be Present In View ov_calendar_collection`; TC04 `Code Should Be Absent In View`;
  independent re-read AUTOTEST_CC in OV_CALENDAR_COLLECTION = 0 rows.
