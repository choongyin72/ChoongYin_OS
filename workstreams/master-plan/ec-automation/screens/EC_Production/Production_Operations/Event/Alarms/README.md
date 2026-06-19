# Alarms — IUD automation bundle (NEW pattern: EVENT-LOG)

**Screen:** EC Production > Production Operations > Event > Alarms
**Type:** `DATA`/DAY class (`FCTY_DAY_ALARM`) — a **gated inline-grid event log**, not OV/TV master-data.
**Delete:** PHYSICAL (event rows). **No object code** — rows identified by a unique **REASON marker**.
**Status:** ✅ live **4/4 PASS**, DB-verified, self-cleaning. See [alarms_sow.md](alarms_sow.md).

## Layout
- `playwright/ec_iud_alarms.py` — freestyle proof (cascade nav → insert → reason-change update → physical delete; env creds).
- `investigation/` — read-only recon: `find_alarm_screens.py`, `recon_alarms_row.py`, `alarms_db_recon.py`, `alarms_residue.py`.
- `evidence/` — screenshots + `ec_iud_alarms_result.json`.

## Run
```bash
cd workstreams/master-plan/ec-automation
# RF suite (the proof — headed, DB-verified):
EC_HEADLESS=false py -m robot --outputdir results/alarms_live \
  tests/EC_Production/Production_Operations/Event/alarms_iud.robot
# Playwright bundle (EC_HEADED=1 to watch, EC_CODE to override the Reason marker):
EC_HEADED=1 py -X utf8 screens/EC_Production/Production_Operations/Event/Alarms/playwright/ec_iud_alarms.py
```

## Key facts
- **Gated**: PU → Area → Facility Class 1 cascade (+ Date) + GO must be applied before the grid (`alarms:form:T_data`) loads.
- Insert via toolbar **"Alarms"** → blank row → **Type of Alarm** (C2 dd, the only mandatory cell, first option) + **Reason** (C3, the `AUTOTEST_ALARM_<ts>` marker). Save → GO.
- **DB oracle**: `View Count Where DV_ALARMS REASON <marker>` (1 after insert, 0 after delete). Update = a Reason-change, also DB-verified.
- Physical delete; self-clean verified in both `DV_ALARMS` and `FCTY_DAY_ALARM`.
- Reuses T2 `table_class.resource` + T1 `navigator`/`table` + DbVerify — no shared-file changes. Credentials from env (R16).
- Sibling candidate for later: **Reported Alarms** (`SR_MD_REPORTED_ALARMS`, same base table, TABLE/EVENT).
