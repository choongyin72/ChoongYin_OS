# Screen: Chemical Transport Tank

- **Type:** OV (EC Object Configuration, date-effective) - plain Bank-family (`manage_object_nav`,
  full Bank-pattern conversion); no navigator, no mandatory dropdowns.
- **BF_CODE:** CO.0257 - **Treeview:** Configuration > Assets > Chemical_Objects > Chemical
  Transport Tank _(DB treeview JSON)_. **NOT** "Chemical Tank" (a separate Area-pattern OV-GM
  navigator screen — do not confuse the two similarly-named screens).
- **DB view:** `OV_CHEM_TRANS_TANK` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 (this backfill re-run) - EC 14.2.4 - local sandbox - live RF 5/5,
  dryrun 5/5. Automation itself was rebuilt 2026-08-23 (PR #461, Batch 8 Bank-pattern conversion).

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Chemical Transport Tank` -> `label.tv-link` "Chemical Transport Tank" |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data` (needs GO to load; no default rows on open) |
| Grid filter | shared T2 `Find Object Row By Filter` / `Clear Object Row Filter`, wrapped as `Find Chemical Transport Tank Row By Filter` / `Clear Chemical Transport Tank Row Filter` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete End Date field id | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (framework-invariant, shared with Bank/State/Berth) |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL, no hardcoded ids)
**Transport Tank Code*** - **Transport Tank Name*** - **Start Date*** (date) - End Date - optional
dropdowns (skipped, none mandatory). (`*` = mandatory-and-yellow-when-empty)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Transport Tank Code` (read-only) - **`Transport Tank Name`** (only field updated). Delete:
**`End Date`** = Start Date -> row leaves `OV_CHEM_TRANS_TANK`.

## Test data / codes
- Fixed test code `AUTOTEST_CTT` (not generated-unique — matches Bank/Berth convention). Name:
  `AUTOTEST Chemical Transport Tank` / `... UPDATED`. Start/End = `2000-01-01`.
- Properties files: `testdata/chemical_transport_tank_insert.properties`, `_update.properties`,
  `_form_verify.properties`, `_grid_verify.properties`.

## Automation (code in ec-automation)
- **Playwright:** `py/chemical_transport_tank_iud.py` -> 7/7 (update Name). Unchanged by the Batch 8
  RF conversion; permanently waived from further Playwright work (Universal Screen Engine replaces
  that role going forward).
- **RF:** T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_transport_tank_page.resource`
  (label-driven, properties-file-driven, explicit grid-filter wiring, rebuilt PR #461/2026-08-23) +
  suite `tests/Configuration/Assets/Chemical_Objects/chemical_transport_tank_iud.robot` (5-TC:
  clean-state/insert/update/find/delete) -> live 5/5.
- Dedicated credentials: `CHEMICAL_TRANSPORT_TANK_EC_USER`/`CHEMICAL_TRANSPORT_TANK_EC_PASS`
  (`resources/credentials.py`).

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
- Fixed test code `AUTOTEST_CTT` must be freed by TC05 (delete) every run - EC never lets a DELETED
  code be reused, but only if the run actually completes its own cleanup.
- Bundle docs (SOW/README/JOURNAL/CHECKLIST/this file) went stale for ~5 weeks after the 2026-08-23
  RF rebuild until the 2026-08-28 backfill caught up — a real instance of the risk the
  lean-deliverable backfill work order exists to close, not a hypothetical.
