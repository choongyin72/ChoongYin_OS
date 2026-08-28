# Backfill evidence-capture run - Document Template (2026-08-28)

Real numbers from this backfill task's own single re-run (no rebuild of automation). Commands run
from `workstreams/master-plan/ec-automation/` unless noted.

- **Dryrun:** `robot --dryrun tests/Configuration/Assets/Revenue_Document_Objects/document_template_iud.robot`
  -> **5/5 PASS**, 0 failed. See `dryrun_output.xml`.
- **Live headless run:** `EC_HEADLESS=true robot tests/Configuration/Assets/Revenue_Document_Objects/document_template_iud.robot`
  -> **5/5 PASS on attempt 1** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05
  Delete), no retry needed. See `live_log.html` / `live_report.html` / `live_output.xml` +
  per-step screenshots (`TC0*_*.png`, auto-captured by the suite's own `Capture Step` calls).
- **Filter-fired check:** `grep -c "Find Object Row By Filter" live_output.xml` -> **15** (matches
  PR #484's own cited count exactly - no drift).
- **Robocop:** `robocop check pageobjects/.../document_template_page.resource
  tests/.../document_template_iud.robot` -> **9 issues** (4x VAR02 unused suite variable, 5x DOC02
  missing test-case documentation). Not a regression: Bank's own suite
  (`tests/Configuration/Assets/Financial_Objects/bank_iud.robot`) was checked the same way this
  session and returns **13** issues of the same two classes - Document Template's count is
  baseline noise for this pattern family, lower than the exemplar's own baseline, not new.
  See `robocop_output.txt`.
- **Hygiene:** `REPO_ROOT=<repo root> py scripts/check_bundle_hygiene.py` -> **RESULT: PASS** (no
  hardcoded creds/R16, pure ASCII/R20, no CHECKLIST/VERIFY-REPORT contradiction, doc rows match
  declared families). The run's only WARN is 2 pre-existing hardcoded-credential lines in
  **Contract Area's** `investigation/` recon script - a different screen, not touched by this task.
  See `hygiene_output.txt`.
- **DB self-clean:** fresh `oracledb` connection (`EC_DB_USER=ECKERNEL_EC`, `EC_DB_DSN=localhost:1521/ORCL`,
  same resolution as `libraries/DbVerify.py`), read-only: `SELECT CODE FROM OV_DOC_TEMPLATE WHERE
  CODE = 'AUTOTEST_DOCUMENT_TEMPLATE'` -> **0 rows** (checked AFTER the live run completed TC05).
  See `db_selfclean_check_output.txt`.

No blocker hit; no retry needed on either the dryrun or the live run.
