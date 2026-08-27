# Service - EC Object IUD bundle

**Screen:** Configuration > Assets > Service_Objects > Service (BF CO.2103). OV-GM (grid `manageObject:form:T_data`), navigator-GATED,
date-effective. See `service_sow.md` + `VERIFY-REPORT.md` (2026-08-01 base build). Driver
`py/service_iud.py` (Playwright, pre-existing, unchanged); T3/suite under
`Configuration/Assets/Service_Objects` (converted to the Area pattern in PR #552, 2026-08-26).

## RF suite — current shape (post PR #552, 2026-08-26) — this is the deliverable to run

5-TC structure (TC01 Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete), each TC with its
own Login/Logout, a **fixed** test code `AUTOTEST_SERVICE`, properties-file-driven insert/update, and
the mandatory Business Unit navigator fill delegated to the shared T2 keyword
`Apply Navigator From Properties` (`testdata/service_navigator.properties`). See `service_sow.md`'s
"Dev story - 2026-08-26" section for the full conversion history.

### Run — from `workstreams/master-plan/ec-automation/`

```bash
# structure-only dryrun (no browser/DB)
robot --dryrun tests/Configuration/Assets/Service_Objects/service_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Service_Objects/service_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Service_Objects/service_iud.robot
```

### DB self-clean check pattern

```sql
SELECT COUNT(*) FROM OV_SERVICE WHERE CODE = 'AUTOTEST_SERVICE';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```
Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_SERVICE", "AUTOTEST_SERVICE")` — `None` = confirmed absent.

### Known flake (disclosed, not fixed by this backfill)

A navigator autocomplete-panel click-intercept timing issue was reproduced intermittently during this
backfill's evidence capture (2026-08-27) — see `JOURNAL.md` and
`ec-ui-knowledge/screens/service.md`'s Quirks section. It hits a different TC each run and never
affects DB ground truth; if it fires, re-run the suite (and re-run TC05 alone first if a residual
`AUTOTEST_SERVICE` row is left behind by an interrupted attempt).

### Files in this bundle
- `service_sow.md` — SOW: classification, nav/grid/cell shape, test data, dev story (2026-08-01 base
  build + 2026-08-26 conversion + this 2026-08-27 backfill).
- `README.md` — this file.
- `JOURNAL.md` — per-branch work journal (2026-08-01 build + this backfill's evidence-capture attempts).
- `evidence/` — `SV_0*.png`/`results.json` from the original 2026-08-01 Playwright run, PLUS
  `log.html`/`output.xml`/`report.html`/per-TC screenshots from this backfill's 2026-08-27 live RF run.
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence citations.
- `investigation/` — pre-existing recon script (`recon.py`) from the 2026-08-01 build, unchanged.

KB selector map: `ec-ui-knowledge/screens/service.md`.
