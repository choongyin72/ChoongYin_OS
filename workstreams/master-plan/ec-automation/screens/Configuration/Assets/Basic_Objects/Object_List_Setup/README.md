# Object List Setup — Playwright IUD

Insert / Delete automation for the EC **Object List Setup** screen
(Configuration → Assets → Basic Objects → Object List Setup), implemented in
**Playwright** (Python). This is a **PARENT-CHILD setup screen** (new "PC" pattern):
the navigator picks **List Class + Object List + GO**, then the chosen list's
**items** show in an inline TV-style grid. Insert/Delete toolbar entries act on
"Object List Item". Item delete is **physical**.

## Run
```bash
# from this folder — headless (default)
py -X utf8 playwright/ec_iud_object_list_setup.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_object_list_setup.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `400` | ms slow-motion per action (headed only) |
| `EC_URL` / `EC_DB_DSN` | sandbox | override targets |

Fixed test values (user-approved 2026-06-11): List Class `FIN_ACCOUNT`,
Object List `OPEX GL Equipment Rental`, member item `6931250`. The member is only
REFERENCED (a membership row is created and physically deleted again); the account
object itself is never modified. Verification is a **count-delta** on
`OBJECT_LIST_SETUP.GENERIC_OBJECT_CODE`, so pre-existing rows in other lists never matter.

## Folder
- `playwright/ec_iud_object_list_setup.py` — dedicated implementation (item-grid flow)
- `investigation/` — recon scripts that learned the screen (item-row DOM, save-reject probe)
- `evidence/` — screenshots + results JSON from a full insert → delete run
- `object_list_setup_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Basic_Objects/object_list_setup_iud.robot`
