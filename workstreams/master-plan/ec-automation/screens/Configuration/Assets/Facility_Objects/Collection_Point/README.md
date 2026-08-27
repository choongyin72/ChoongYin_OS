# Collection Point — EC Object IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > Collection Point (BF CO.0205).
OV-GM (groupmodel manage-object, grid `manageObject:form:T_data`), navigator-GATED (genuine
3-level Production Unit -> Area -> Operator Route SAME-ROW cascade + GO), date-effective.

Converted to the full **Area pattern** via PR #541 (2026-08-26): 5 TCs (Verify Clean State /
Insert / Update / Find / Delete), per-TC login/logout, fixed test code
`AUTOTEST_COLLECTION_POINT`, navigator fill delegated to the shared T2
`Apply Navigator From Properties` keyword, properties-file-driven insert/update/verify, explicit
grid-filter wiring, zero inline DB-verify calls (the TC05 DB check lives solely inside the shared
T2 `Verify Object Removed`).

This bundle documents the RF automation only — see `collection_point_sow.md` (spec/classification)
and `JOURNAL.md` (what actually happened, including the original 2026-08-01 build and the
2026-08-26 Area-pattern conversion). The Playwright driver `py/collection_point_iud.py` still
exists (untouched by PR #541) but a hand-written Playwright bundle is no longer required for
Area-pattern work — the Universal Screen Engine covers that role going forward.

## Files
- T3 page object: `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource`
- Suite: `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot` (5 TCs)
- Test data: `testdata/collection_point_{navigator,insert,update,form_verify,grid_verify}.properties`
- Credentials: `COLLECTION_POINT_EC_USER` / `COLLECTION_POINT_EC_PASS` in `resources/credentials.py`

## Run — dryrun
```bash
# from workstreams/master-plan/ec-automation/
robot --dryrun --outputdir results/_collection_point_dryrun tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot
```

## Run — live (headless)
```bash
EC_HEADLESS=true robot --outputdir results/_collection_point_live tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot
```

## Run — live (headed, visible browser)
```bash
robot --outputdir results/_collection_point_live tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot
```

> If a live run hangs or the browser context dies unexpectedly, check for stray
> `chrome-headless-shell.exe` processes left over from a prior run (`tasklist | grep -i chrome` on
> Windows) and kill them before retrying — this was a real, repeated cause of flakes in this
> session, not a defect in this suite (see JOURNAL.md).

## DB self-clean check (fresh connection, after any live run)
```sql
SELECT * FROM OV_COLLECTION_POINT WHERE CODE = 'AUTOTEST_COLLECTION_POINT';
-- expect 0 rows once TC05 (Delete) has completed
```
Or via `libraries/DbVerify.py`'s connection pattern (`ECKERNEL_EC` / `localhost:1521/ORCL`,
env-overridable via `EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`).

## robocop
```bash
py -m robocop check pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot
```
Expect 7 issues (VAR02 x2 + DOC02 x5) — this is the exact parity baseline shared with
Area/Facility Class 1's own reference-pattern files, not a regression to fix.

## Hygiene
```bash
py scripts/check_bundle_hygiene.py
```
(run from the repo root `C:/Projects/ChoongYin_OS`) — expect `RESULT: PASS` for R16 (no
hardcoded creds) / R20 (ASCII) / CHECKLIST-vs-VERIFY-REPORT consistency.
