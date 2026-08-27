# MMS Lease — IUD automation bundle

EC screen: **Configuration > Assets > Commercial Objects > MMS Lease**. Manage Object (OV),
plain — no mandatory navigator scope. DB view `OV_MMS_LEASE`. DELETE = **End Date = Start
Date** (zero-length window) — EC true delete (row removed from `OV_MMS_LEASE`).

The primary, currently maintained automation is the **RF suite** (Bank pattern, PR #437,
merged 2026-08-23). The legacy Playwright driver in this folder predates that conversion
and is kept as historical reference only — see `mms_lease_sow.md` Section 5.

## Run — RF suite (primary)

```bash
cd workstreams/master-plan/ec-automation

# dryrun
robot --dryrun tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot

# live headless run
EC_HEADLESS=true robot tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot
```

## DB self-clean check (fresh connection, before AND after a live run)

```python
import oracledb
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_MMS_LEASE WHERE CODE = 'AUTOTEST_MMS_LEASE'")
print(cur.fetchone()[0])   # expect 0 both before and after a full TC01-TC05 run
```

## Run — legacy Playwright reference (historical, not maintained)

```bash
py -X utf8 playwright/ec_iud_mms_lease.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_mms_lease.py   # watchable
```

## Folder

- `pageobjects/.../mms_lease_page.resource` + `tests/.../mms_lease_iud.robot` (outside this
  folder, treeview-mirrored) — the real, maintained RF T3/suite.
- `mms_lease_sow.md` — statement of work / spec.
- `JOURNAL.md` — work journal (built / lessons / blockers / decisions / evidence).
- `evidence/` — `rf_bank_pattern_2026-08-28/` (current RF dryrun + live run artifacts);
  older `mms_lease_0*.png` + `mms_lease_results.json` are from the original 2026-06-12
  Playwright-only build.
- `playwright/ec_iud_mms_lease.py` — legacy Playwright driver (waived going forward, kept
  for reference; superseded by the Universal Screen Engine).
- `investigation/` — recon scripts used to learn the screen (predates the Bank-pattern
  conversion).
- `CHECKLIST.md` — `docs/IUD-DELIVERABLE-CHECKLIST.md` ticked with evidence.

## Equivalent RF suite

`tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot` (T3:
`pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource`).
