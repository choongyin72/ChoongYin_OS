# Tract - IUD bundle

Configuration > Assets > Royalty Objects > **Tract** (RC.0056).
**OV-GM (gated)** Manage-Object screen - the grid loads only after a **Unit Agreement** is
picked in the navigator + GO. Same family as Transport System (gated by Unit Agreement instead
of Business Unit). DELETE = End Date = Start Date (true delete in `ov_tract`).

## Contents
- `tract_sow.md` - Statement of Work (recon + OV-GM design + acceptance criteria).
- `evidence/` - RF step screenshots from the live run.
- **RF-only** (no Playwright walkthrough) - follows the OV-GM exemplar precedent (Transport System);
  the live + DB-verified RF suite is the proof.

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).

## Run
```bash
# RF (the proof) - headed live run from the ec-automation root:
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/tract_iud.robot
```

Navigator: Unit Agreement = `Unit Agreement 1` (has data); insert parent dd must match.
Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `AUTOTEST_TR_*` only; self-cleaning.
