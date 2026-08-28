# Licence — IUD bundle

EC screen: **Licence** (Configuration → Assets → Commercial Objects → Licence).
**Manage Object (OV)** screen, Bank pattern (plain OV, no navigator). DELETE =
**End Date = Start Date** (zero-length window) — EC true delete (object removed from
`OV_LICENCE`).

The real, currently-maintained automation is the **RF suite** (converted to the full
Bank pattern in PR #438, 2026-08-23). The `playwright/` folder below is the original
2026-06-12 standalone Playwright reference flow — kept for history, not the primary
automation path (owner decision 2026-08-27: the Universal Screen Engine replaces new
hand-written Playwright drivers going forward; this pre-existing one is not rebuilt).

## Run the RF suite

From `workstreams/master-plan/ec-automation/`:

```bash
# Dry-run (syntax/keyword-resolution check, no browser)
robot --dryrun --outputdir results/_licence_dryrun tests/Configuration/Assets/Commercial_Objects/licence_iud.robot

# Live headless run (the real proof)
EC_HEADLESS=true robot --outputdir results/_licence_live tests/Configuration/Assets/Commercial_Objects/licence_iud.robot

# Live headed run (watchable)
EC_HEADLESS=false robot --outputdir results/_licence_live tests/Configuration/Assets/Commercial_Objects/licence_iud.robot
```

Expected: `5 tests, 5 passed, 0 failed` (TC01 Verify Clean State, TC02 Insert, TC03
Update, TC04 Find, TC05 Delete).

Confirm the grid-filter keyword actually fired (not just present in the resource file):
```bash
grep -c 'name="Find Licence Row By Filter"' results/_licence_live/output.xml   # expect 5
```

## DB self-clean check

Independent, fresh-connection query against `OV_LICENCE` (must be 0 both before and
after a run):
```python
import oracledb, os
conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_LICENCE WHERE CODE = 'AUTOTEST_LICENCE'")
print(cur.fetchone()[0])   # expect 0
```

## Original Playwright reference (2026-06-12, history only)
```bash
py -X utf8 playwright/ec_iud_licence.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_licence.py   # watchable
```

## Folder
- `pageobjects/.../Commercial_Objects/licence_page.resource` — T3 page object (label-driven, properties-file-driven, Bank pattern per PR #438)
- `tests/.../Commercial_Objects/licence_iud.robot` — RF suite (TC01-TC05)
- `testdata/licence_{insert,update,form_verify,grid_verify}.properties` — test data
- `playwright/ec_iud_licence.py` — original standalone Playwright reference (thin config over the shared `../../Basic_Objects/_shared/iud_engine.py`); kept for history, not primary
- `investigation/` — recon scripts used to learn the screen (original 2026-06-12 build)
- `evidence/` — screenshots + results JSON from the original 2026-06-12 Playwright run, plus the 2026-08-28 RF backfill re-run evidence
- `licence_sow.md` — statement of work / spec
- `JOURNAL.md` — work journal (built / done well / lessons / blockers / decisions / evidence)
- `CHECKLIST.md` — `docs/IUD-DELIVERABLE-CHECKLIST.md` copy, ticked with real evidence

## KB selector map
`ec-ui-knowledge/screens/licence.md` — nav path, DB view, grid id, insert/update/delete
selectors, mandatory fields, quirks.
