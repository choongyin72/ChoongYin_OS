# IUD Deliverable Checklist - Document Received Term (CD.0108)

Per canonical `docs/IUD-DELIVERABLE-CHECKLIST.md` (19 items, all hard gates). Each ticked with evidence.

## A. Bundle artifacts
- [x] **1. `document_received_term_sow.md`** -- classification (OV date-eff), form layout, test data, dev story, lessons.
- [x] **2. `README.md`** -- bundle overview + exact run commands.
- [x] **3. `JOURNAL.md`** -- built / done-well / done-wrong / improve / blockers / decisions / evidence.
- [x] **4. `playwright/ec_iud_document_received_term.py`** -- env-var creds, ASCII-clean, full I-U-D flow.
- [x] **5. `investigation/`** -- `recon_new_object_form.py` + `recon_method_dropdown.py` (read-only).
- [x] **6. `evidence/`** -- 11 step screenshots + `results.json` (Playwright run = ALL PASS).
- [x] **7. `CHECKLIST.md`** -- this file.

## B. RF files
- [x] **8. T3 page object** -- `pageobjects/Configuration/Assets/Date_Objects/document_received_term_page.resource` (locators in Variables; docstring matches).
- [x] **9. Suite** -- `tests/Configuration/Assets/Date_Objects/document_received_term_iud.robot` (clean -> insert -> update -> delete -> cleanup).

## C. Verification gates
- [x] **10. robocop clean** -- `No issues found.` on T3 + suite.
- [x] **11. `--dryrun` N/N PASS** -- 4 tests, 4 passed.
- [x] **12. LIVE headed run N/N PASS** -- `EC_HEADLESS=false` -> 4 tests, 4 passed (`/c/tmp/drt_live`).
- [x] **13. DB ground-truth** -- in-suite: TC02 `Code Should Be Present In View ov_doc_received_term <code>`; TC04 `Code Should Be Absent In View ov_doc_received_term <code>`.
- [x] **14. FULL I-U-D scope** -- TC02 Insert + TC03 Update (Name) + TC04 Delete (End=Start), all present.
- [x] **15. Self-clean confirmed** -- independent DB re-read: `AUTOTEST_DRT%` in `OV_DOC_RECEIVED_TERM` = 0 rows; existing rows untouched.
- [x] **16. Hygiene PASS** -- `py scripts/check_bundle_hygiene.py` -> RESULT: PASS (R16 env creds, R20 ASCII).

## D. Delivery
- [x] **17. Registry row** appended to `docs/ec_screen_registry.md` (append-only).
- [x] **18. Scorecard row** appended to `docs/automation-scorecard.md` (append-only).
- [x] **19. PR** with the R9 6-field body; R8 sync first; never self-merge.

**All 19 green.**
