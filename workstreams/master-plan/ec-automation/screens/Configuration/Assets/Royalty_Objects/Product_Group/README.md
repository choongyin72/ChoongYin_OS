# Product Group - IUD bundle

Configuration > Assets > Royalty Objects > **Product Group** (RC.0053).
Manage-Object (OV) screen, Bank family. DELETE = End Date = Start Date (true delete in `ov_product_group`).

## Contents
- `product_group_sow.md` - Statement of Work (recon + design + acceptance criteria).
- `playwright/ec_iud_product_group.py` - freestyle Playwright IUD walkthrough (screenshots per step).
- `evidence/` - screenshots from a live run.

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).

## Run
```bash
# RF (the proof) - headed live run from the ec-automation root:
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot

# Playwright walkthrough (demo / screenshots):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Product_Group/playwright/ec_iud_product_group.py
```

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `AUTOTEST_PG_*` only; self-cleaning.
