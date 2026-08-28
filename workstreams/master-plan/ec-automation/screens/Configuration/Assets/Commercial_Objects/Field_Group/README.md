# Field Group — IUD automation bundle

Insert / Update / Delete automation for the EC **Field Group** screen
(Configuration → Assets → Commercial Objects → Field Group). **RF is the live, maintained
suite** (Bank pattern, converted PR #434, merged 2026-08-23). A pre-existing Playwright
reference implementation is kept in this bundle unchanged (waived permanently from this
backfill per `docs/lean-deliverable-backfill-workorder.md` — the Universal Screen Engine
replaces that role).

Field Group is a plain **Manage Object (OV)** screen — **no navigator** (confirmed live
2026-08-23). DELETE = **End Date = Start Date** (zero-length window) — EC true delete (object
removed from `OV_FIELD_GROUP`).

## Run — RF suite (primary, live-maintained)
```bash
# Dryrun (syntax/resolution check only, no browser)
robot --dryrun tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot

# Live headless run
EC_HEADLESS=true robot --outputdir screens/Configuration/Assets/Commercial_Objects/Field_Group/evidence tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot

# DB self-clean check (fresh connection, run AFTER a live pass that reached TC05 Delete)
py -c "import oracledb; c=oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL'); cur=c.cursor(); cur.execute(\"SELECT CODE FROM OV_FIELD_GROUP WHERE CODE LIKE 'AUTOTEST%'\"); print(cur.fetchall())"
# Expected: []  (0 residual AUTOTEST_FIELD_GROUP rows)
```

## Run — Playwright reference (pre-existing, unmodified)
```bash
py -X utf8 playwright/ec_iud_field_group.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_field_group.py   # watchable
```

## Folder
- `pageobjects/.../field_group_page.resource` (repo-root path, not in this folder) — T3 page
  object, Bank pattern, label-driven + properties-file-driven.
- `tests/.../field_group_iud.robot` (repo-root path) — 5-TC suite (Clean State/Insert/Update/
  Find/Delete), per-TC Login/Logout, fixed code `AUTOTEST_FIELD_GROUP`.
- `testdata/field_group_{insert,update,form_verify,grid_verify}.properties` (repo-root path).
- `playwright/ec_iud_field_group.py` — thin config over the shared engine
  (`../../Basic_Objects/_shared/iud_engine.py`) — pre-existing, unmodified, permanently waived.
- `investigation/` — recon scripts used to learn the screen (pre-existing).
- `evidence/` — screenshots + results JSON from historical runs, plus
  `backfill_2026-08-28/` (this backfill's own live-run artifacts: log.html/output.xml/
  report.html, 5/5 PASS).
- `field_group_sow.md` — statement of work / spec (Sections 1-5 original 2026-06-12 build;
  Section 6 addendum = PR #434 Bank-pattern conversion + this backfill).
- `JOURNAL.md` — Built/Done well/Done wrong/Blockers/Decisions/Evidence, pulled from PR #434.
- `CHECKLIST.md` — `docs/IUD-DELIVERABLE-CHECKLIST.md` copy, ticked with real evidence.

## KB selector map
`ec-ui-knowledge/screens/field_group.md`
