# Meter — RF automation bundle

Screen: Configuration > Assets > Dispatching Objects > Meter (`OV_METER`). OV-GM (BU-gated) +
generic popup, full Area pattern (PR #554, merged 2026-08-26). See `meter_sow.md` for
classification/shape and `JOURNAL.md` for the build history, including the wrong-then-corrected
Area-pattern-fit classification.

This bundle is a documentation/evidence backfill (2026-08-27) — the RF automation it documents
already exists and is not modified here.

## Files
- `pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource` — T3 page object.
- `tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot` — 5-TC suite.
- `testdata/meter_navigator.properties`, `meter_insert.properties`, `meter_update.properties`,
  `meter_form_verify.properties`, `meter_grid_verify.properties`.
- `docs/meter_popup_notes.md` — the Delivery Point popup gesture recon/recipe.

## Run commands

All commands run from `workstreams/master-plan/ec-automation/`.

Dryrun (syntax/keyword check only, no browser):
```bash
robot --dryrun --outputdir results/meter_dryrun tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot
```

Live headless run:
```bash
EC_HEADLESS=true robot --outputdir results/meter_live tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot
```

Live headed run (visible browser, for manual observation):
```bash
EC_HEADLESS=false robot --outputdir results/meter_live_headed tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot
```

## DB self-clean check (`OV_METER`)

Run against a **fresh** connection (not reused from the test run's own session) before AND after
a live run — must return 0 both times:
```sql
SELECT COUNT(*) FROM OV_METER WHERE CODE LIKE 'AUTOTEST_METER%';
```

## Known quirk (see `docs/meter_popup_notes.md` for full detail)
The Delivery Point Name field is a generic EC object popup (`pin`/`pinB`), not a dropdown — its
close callback resets the form's save-dirty state, so the insert properties file's field order
(Start Date → Delivery Point Name → Meter Code → Meter Name → Meter Type) is load-bearing. Do not
reorder it.
