# Screen: Target Mapping Configuration (IS.0002)

**Status:** Verified
**Last verified:** 2026-08-28
**Verified against EC version/environment:** local sandbox (this repo's default `EC_URL`), oracledb
DSN `localhost:1521/ORCL`, schema `ECKERNEL_EC`

---

## Navigation

- Menu path: `Configuration > Integration Services > Import > Target Mapping Configuration`
- DB class: `IMP_TARGET_MAPPING` (label "Import Target Mapping"), `CLASS_TYPE=OBJECT`,
  `TIME_SCOPE_CODE=INVARIANT` (no version table).
- Verify view: `OV_IMP_TARGET_MAPPING` (117 rows on this sandbox as of 2026-08-28, unchanged since
  the screen was first automated 2026-08-24 — this suite never mutates it).
- Screen-dedicated credentials: `TARGET_MAPPING_CONFIGURATION_EC_USER` / `_PASS` in
  `resources/credentials.py` (falls back to shared `EC_USER`/`EC_PASS`).

---

## Key elements

| Purpose | Selector | Notes |
|---|---|---|
| Navigator - Class filter | `StandardNavigator:form:G:0:R:1:C:0:in` | non-standard id, NOT the generic `nav:form:...` used by most OV/OV-GM screens; optional (not mandatory) |
| Navigator - Attribute filter | `StandardNavigator:form:G:0:R:1:C:1:in` | optional |
| Navigator - EC Key filter | `StandardNavigator:form:G:0:R:1:C:2:in` | optional |
| GO button | `buttongo:form:B` | non-standard id, NOT `button:form:B` / `go_button:form:B`; always required to (re)load the grid, even with no filters set |
| Grid body | `imp_target_mapping_table:form:T_data` | ~20 real rows visible on initial unfiltered load; ~117 total rows in the DB view |
| Grid cell (per column) | `input[id$=":C{n}_dd_input"]` inside each `<tr>` | columns are autocomplete-dropdown cells, NOT plain `<td>` text - read `.value` via JS, not `textContent`; the shared `table.resource` `Get Table Rows` returns blank here |
| Insert toolbar item | n/a | present in DOM but carries `ui-submenu-state-disabled` - confirmed disabled live |
| Update toolbar item | n/a | does not exist at all (DOM count = 0) |
| Delete toolbar item | n/a | present in DOM but carries `ui-submenu-state-disabled` - confirmed disabled live |

**Grid column order (0-based):** 0=Class, 1=Attribute, 2=Ec Key, 3=Class Key 1, 4=Class Key 2,
(Class Key 3-10, Condition 1-3, From/To Unit, Constant String/Number/Date follow — unused by the
existing suite).

---

## Find sequence (this screen — no Save/Update/Delete exists)

1. Launch EC, log in (`Open Target Mapping Configuration Screen` keyword), navigate to the screen.
2. (Optional) type into one or more navigator filters (Class/Attribute/EC Key) —
   `Filter Target Mapping Configuration By Class` etc.
3. Click `buttongo:form:B` (`Apply Target Mapping Configuration Navigator`) — always required,
   even with zero filters set, to (re)load the grid.
4. Read grid rows via JS (`Target Mapping Configuration Row Count` /
   `Find Target Mapping Configuration Row`), matching columns 0-4 (`Cn_dd_input.value`) against
   the expected 5 field values.
5. Cross-check the found row against the DB by its unique EC Key:
   `Code Should Be Present In View  OV_IMP_TARGET_MAPPING  <ec_key>`.

There is no Save/Update/Delete sequence for this screen — it is intentionally out of scope.

**Real pre-existing find-target row** (owner-supplied, live-verified, used by TC04):

| Field | Value |
|---|---|
| Class | `PWEL_DAY_STATUS` |
| Attribute | `AVG_LIQ_VOL` |
| EC Key | `ecValue16` |
| Class Key 1 | `Key 1` |
| Class Key 2 | `Key 2` |

---

## Known quirks

- Toolbar Insert/Delete icons render as visually enabled but are functionally disabled
  (`ui-submenu-state-disabled` class) — do not trust visual appearance alone; check the DOM class.
- There is no Update icon at all (not just disabled — absent, count=0).
- Grid cells are autocomplete-dropdown inputs (`Cn_dd_input`), not plain text — `textContent`-based
  row readers (e.g. the shared `table.resource` `Get Table Rows`) return blank; must read
  `.value` via JS instead.
- GO (`buttongo:form:B`) must be clicked even with zero navigator filters set, or the grid never
  loads (confirmed by TC01's clean-load check).
- Non-standard navigator/GO ids on this screen only — do not copy the generic
  `manage_object.resource` ids for this screen.

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-08-24 | Initial discovery + Find-only suite built | PR #488 — brand-new screen, zero prior automation; live DOM probe confirmed owner's Find-only statement |
| 2026-08-28 | KB map backfilled (this file created) | Batch 12, `docs/lean-deliverable-backfill-workorder.md` — Section H retired the lean waiver that had skipped this file originally; re-verified same facts live (robocop clean, dryrun 2/2 + tree 883/883, live 2/2, DB row count 117→117), no automation changed |
