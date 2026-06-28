# JOURNAL - feature/doc-date-term-iud (CD.0107 Document Date Term)

## Built
- Full IUD automation for Document Date Term (OV, date-effective): T3 page object, RF suite
  (4 TCs: clean -> insert -> update -> delete, in-suite DB asserts), Playwright reference flow,
  2 read-only recon scripts, 11-screenshot evidence set, SOW, README, CHECKLIST.
- **Pilot of the new 19-item IUD deliverable standard** (`docs/IUD-DELIVERABLE-CHECKLIST.md`, PR #140):
  first screen carrying the bundle `CHECKLIST.md` to prove the format + reviewer gate before batching
  the remaining 4 Date Objects screens.

## Done well
- DB-first recon nailed the classification (OV date-effective) before any UI work; the two extra
  mandatory inputs (METHOD dropdown + numeric OFFSET) were found by DOM recon, not guessed.
- Kept T3 thin -- reused T2 `manage_object` generics + the shared `Select EC Dropdown Option`.
  Zero shared-file edits (no R12 trigger), zero new T1/T2 keywords.
- Full I-U-D scope from the start (RC.0050 lesson applied -- not I/D only).
- Robocop clean, dryrun 4/4, live headed 4/4, hygiene PASS, independent DB residual = 0.

## Done wrong / corrected
- First recon used the singular label "Document Date Term"; the class LABEL is plural
  ("Document Date Terms"), so the label->class match returned empty. Corrected with a LIKE-based
  resolve -- class = DOC_DATE_TERM confirmed.
- Recon scripts initially had `\:` invalid-escape SyntaxWarnings in CSS-id locators; fixed by making
  those locator strings raw (`r'...'`).

## To improve
- The OFFSET-mandatory + METHOD-dropdown combo is reusable knowledge for the sibling "term" screens
  (Document Received Term, Payment Term may share the same form shape) -- check at their recon.

## Blockers -> resolution
- None. (Pre-cleanup + unique-per-run code meant clean state was always true; no flaky re-arm.)

## Decisions
- METHOD = 'Set Document Date manually' (MANUAL) + OFFSET = 0 -- simplest valid combination, no
  calendar dependency, keeps the pilot focused on the IUD mechanics + the dropdown gesture.
- Built in an isolated worktree off origin/master so the deep-dive branch's uncommitted changes are
  untouched.

## Evidence
- Live RF: 4/4 PASS (`/c/tmp/ddt_live`). Playwright: ALL PASS (evidence/results.json).
- DB: TC02 `Code Should Be Present In View ov_doc_date_term`; TC04 `Code Should Be Absent In View`;
  independent re-read AUTOTEST_DDT in OV_DOC_DATE_TERM = 0 rows.
