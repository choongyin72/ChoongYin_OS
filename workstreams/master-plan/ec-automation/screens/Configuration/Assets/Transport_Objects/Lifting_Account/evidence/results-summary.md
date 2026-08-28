# Evidence — backfill task's own live confirmation run (2026-08-28)

This is evidence capture of the already-proven, already-merged suite (per
`docs/lean-deliverable-backfill-workorder.md` item 4) — not a fresh verification cycle, and no
automation files were modified to produce it. The `la_0*.png`/`results.json` files alongside this
one are the ORIGINAL 2026-07-30 build's Playwright evidence (8/8), kept as historical record.

## robocop
```
robocop check pageobjects/Configuration/Assets/Transport_Objects/lifting_account_page.resource tests/Configuration/Assets/Transport_Objects/lifting_account_iud.robot
```
Result: **7 issues** (all DOC02 — missing `[Documentation]` on test cases), confirmed **exact
parity** with Area's own baseline (`pageobjects/Configuration/Assets/Basic_Objects/
area_page.resource` + `tests/Configuration/Assets/Basic_Objects/area_iud.robot` — also 7 issues,
same rule) — not a new issue category introduced by this screen.

## Dryrun
```
robot --dryrun --outputdir Workplaces/lifting-account-backfill/dryrun tests/Configuration/Assets/Transport_Objects/lifting_account_iud.robot
```
Result: **5 tests, 5 passed, 0 failed.**

## Live headless run
```
EC_HEADLESS=true robot --outputdir Workplaces/lifting-account-backfill/live tests/Configuration/Assets/Transport_Objects/lifting_account_iud.robot
```
Result: **5 tests, 5 passed, 0 failed** — first attempt, no retry needed.
- TC01 Verify Clean State — PASS
- TC02 Insert Lifting Account Data — PASS
- TC03 Update Lifting Account Data — PASS
- TC04 Find Lifting Account Data — PASS
- TC05 Delete Lifting Account Data — PASS

Artifacts kept in this folder: `output.xml`, `log.html`, `report.html`.

## DB self-clean (fresh independent oracledb connection, AFTER the live run)
```sql
SELECT COUNT(*) FROM OV_LIFTING_ACCOUNT WHERE CODE LIKE 'AUTOTEST%';
```
Result: **0** — no residual `AUTOTEST%` rows in `OV_LIFTING_ACCOUNT`.

## Scope of this run
This confirms the suite is still green post-merge (PR #562, merge commit `6a8c328`). It does not
re-derive or re-verify the navigator/regression analysis itself — that ground truth comes from
PR #562's own body and review-comment history (see `JOURNAL.md`).
