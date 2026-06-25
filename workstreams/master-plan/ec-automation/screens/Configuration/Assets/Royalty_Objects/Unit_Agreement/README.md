# Unit Agreement - IUD bundle

Configuration > Assets > Royalty Objects > **Unit Agreement** (RC.0055).
Manage-Object (OV) screen, Bank family. DELETE = End Date = Start Date (true delete in `ov_unit_agr`).

## Contents
- `unit_agreement_sow.md` - Statement of Work (recon + design + acceptance criteria).
- `playwright/ec_iud_unit_agreement.py` - freestyle Playwright IUD walkthrough (screenshots per step).
- `evidence/` - screenshots from a live run.

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).

## Run
```bash
# RF (the proof) - headed live run from the ec-automation root:
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot

# Playwright walkthrough (demo / screenshots):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Unit_Agreement/playwright/ec_iud_unit_agreement.py
```

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `AUTOTEST_UA_*` only; self-cleaning.
