# Payment Term IUD bundle (CD.0023)

Configuration > Assets > Date Objects > Payment Term. Manage-Object (OV, date-effective)
screen. Full Insert / Update / Delete, DB-verified and self-cleaning.

## Files
- `payment_term_sow.md` -- SOW (classification, form layout, test data, dev story).
- `CHECKLIST.md` -- the 19-item IUD deliverable checklist, ticked with evidence.
- `JOURNAL.md` -- per-branch work journal.
- `playwright/ec_iud_payment_term.py` -- freestyle reference flow (screenshots + results.json).
- `investigation/` -- read-only DOM recon (New-Object form fields + METHOD dropdown labels).
- `evidence/` -- 11 step screenshots + results.json from a real run.

## Run commands
RF suite (the DB-verified, self-cleaning proof) -- from `workstreams/master-plan/ec-automation/`:
```
# headed (the proof)
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Date_Objects/payment_term_iud.robot
# dryrun
robot --dryrun tests/Configuration/Assets/Date_Objects/payment_term_iud.robot
```

Playwright reference flow (generates evidence/) -- from repo root:
```
EC_HEADED=1 EC_CODE=AUTOTEST_PT_PW01 py workstreams/master-plan/ec-automation/screens/Configuration/Assets/Date_Objects/Payment_Term/playwright/ec_iud_payment_term.py
```

Read-only recon (never saves):
```
SCREEN="Payment Term" py tmp/scripts/scan_ec_screen.py
py workstreams/.../Payment_Term/investigation/recon_new_object_form.py
py workstreams/.../Payment_Term/investigation/recon_method_dropdown.py
```

## Credentials
Read from env (`EC_USER`/`EC_PASS`, default `sysadmin`/`sysadmin`). Never hardcoded (R16).

## DB ground truth
`OV_DOC_DATE_TERM` (`Code Should Be Present/Absent In View`). DELETE = End Date = Start Date
removes the object from the OV view (verified). Base `DOC_DATE_TERM` retains expired rows by design.
