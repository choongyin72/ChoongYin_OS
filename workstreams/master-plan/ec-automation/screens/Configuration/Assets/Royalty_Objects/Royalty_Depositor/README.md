# Royalty Depositor - IUD bundle

Configuration > Assets > Royalty Objects > **Royalty Depositor** (RC.0052).
Manage-Object (OV) screen, Bank family. DELETE = End Date = Start Date (true delete in `ov_royalty_depositor`).

## Contents
- `royalty_depositor_sow.md` - Statement of Work (recon + design + acceptance criteria).
- `playwright/ec_iud_royalty_depositor.py` - freestyle Playwright IUD walkthrough (screenshots per step).
- `evidence/` - screenshots from a live run.

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).

## Run
```bash
# RF (the proof) - headed live run from the ec-automation root:
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot

# Playwright walkthrough (demo / screenshots):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Royalty_Depositor/playwright/ec_iud_royalty_depositor.py
```

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `AUTOTEST_RD_*` only; self-cleaning.
