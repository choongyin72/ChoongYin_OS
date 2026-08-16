# External Location (CO.0227) - read-only recon COMPLETE. Resume point.

All facts below are executed-command output. No sandbox writes.

| fact | value |
|---|---|
| BF | `CO.0227` (step-0 hit in ov-non-bank-targets.md:24) |
| view | `OV_EXTERNAL_LOCATION` |
| class | `EXTERNAL_LOCATION`, CLASS_TYPE=OBJECT -> OV |
| treeview | `Configuration > Assets > Facility Objects > External Location` |
| URL | custom: `/com.ec.prod.co.screens/external_location` |
| grid | `manageObject:form:T_data` - **15 rows after GO with NO filters set** |
| toolbar | insert enabled, delete enabled |

## Navigator - per-field, ALL OPTIONAL (this is the important bit)
```
nav:form:G:0:R:0:C:0  Date
nav:form:G:1:R:0:C:0  Ext Loc Code    (text filter, optional)
nav:form:G:2:R:0:C:0  Ext Loc Name    (text filter, optional)
nav:form:G:3:R:0:C:0  Type            (dropdown filter, optional)
```
These are **search filters, not a scope cascade**. The grid loads on GO with none of them set.

## The doc was WRONG again
`ov-non-bank-targets.md:127` lists this as **OV-GM / manageObject:form:T_data / "needs capability"** from the
2026-07-27 batch guess. The grid id happens to be right, but it is NOT a groupmodel cascade screen - there is
no mandatory nav scope at all. My own UNVERIFIED warning on that row was justified.

## Why it is not buildable with the generator as it stands
`gen_ovgm.py`'s driver does:
```
pu = ec.apply_ovgm_navigator(page)
assert pu, "navigator cascade returned no top-parent PU"
```
`apply_ovgm_navigator` looks for `nav:form:G:0:R:1:C:1..N:dd_input`. None exist here, so it breaks out of the
loop immediately, clicks GO (which is exactly the right gesture) and returns `None` - then the assert kills
the run. The RF T3 has the same shape via `Apply OV-GM Navigator First Available`.

## Remaining work (one task, one PR)
Add a **GO-only** navigator mode to `gen_ovgm.py`, in both layers:
 - driver: click GO, do not require a top-parent (`pu = None` is legitimate);
 - T3: `Apply Navigator` with no dropdown selection;
 - packager/validator: this screen's family is closest to `gatedpf` (per-field nav groups + GO), but its
   grid is `manageObject:form:T_data`, so check the vocabulary tables accept that combination before
   recording rows - do not bend the wording to fit.
Then: generate -> verify_screen live -> package -> no-loss diff -> PR.
Insert-form fields are still UNKNOWN: the scan captured none because it never clicked GO (no mandatory
dropdown to fill), so the New-Object form was never reached. Get them from a scan AFTER GO.
