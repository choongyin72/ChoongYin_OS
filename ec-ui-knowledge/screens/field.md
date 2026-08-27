# Field — EC UI selector map

**Treeview path:** Configuration > Assets > Commercial Objects > Field
**Screen type:** Manage Object (OV-GM groupmodel) — grid loads only after the mandatory
navigator is filled + GO clicked.
**DB view:** `OV_FIELD`
**Grid id:** `manageObject:form:T_data`
**Grid headers (confirmed live):** Field Code / Field Name / Start Date / End Date
**Delete semantics:** End Date = Start Date (EC true delete — row removed from `OV_FIELD`)
**Pattern:** FULL Area-pattern conversion (owner standing rule 2026-08-26 — any navigator
screen matching Area's layout follows Area's full 5-TC/per-TC-login/pure-screen-verify
structure). RF automation: `pageobjects/Configuration/Assets/Commercial_Objects/
field_page.resource` + `tests/Configuration/Assets/Commercial_Objects/field_iud.robot`.

## Navigator (mandatory before grid loads)
Single Area dropdown, same-row cascade (only one level):
```
nav:form:G:0:R:1:C:1:dd    value: "Offshore area"
```
Filled via the shared T2 keyword `Apply Navigator From Properties`
(`resources/manage_object.resource`), driven by `testdata/field_navigator.properties`.
Followed by GO.

## Insert / Update selectors
Labels are SCREEN-PREFIXED — "Field Code"/"Field Name", NOT the generic "Code"/"Name" that
Bank/Object List use (confirmed live 2026-08-26 via a fresh objectForm ECCell/mandatory-class
dump). Insert/Update are driven by the shared T2 keywords (`Insert/Update Object From
Properties`) using `code_label=Field Code`, reading `testdata/field_insert.properties` /
`field_update.properties` — no hardcoded field-id selectors remain in `field_page.resource`
for these forms (label-driven via the shared T2 layer).

Delete's End Date field IS hardcoded (deliberately, not label-driven — same shape as
`objectdates` on every other converted screen, End Date packed into the same row as Start
Date with the label at C:2):
```
${FIELD_DEL_ENDDATE}   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

## Mandatory / yellow fields (confirmed live via MandatoryCellStyle dump, 2026-08-26)
- Field Code
- Field Name
- Start Date

NOT mandatory (confirmed live): Sort Order, Description, Master System Code, Master System
Name, Commercial Entity, Parent field, Operator, Country, State, Comments, Full field name,
Non equity Indicator.

**Geo Area** is not statically mandatory but is a genuine business-rule requirement: it must
be set to the navigator's Area value (`Offshore area`) on Insert or the new row will not be
visible under the current OV-GM navigator scope. It's the groupmodel link field. Deliberately
excluded from the round-trip form-label comparison list (`@{FIELD_FORM_LABELS}` = Field
Code/Field Name only) because a resolved reference dropdown can re-render different display
text after reload — same caveat documented for Area's own Op Production Unit field.

## Quirks
- OV-GM screen, not plain Bank-shaped — the navigator step is real and required even though
  the rest of the suite structure now matches Bank/Area's pattern.
- Uses a FIXED test code `AUTOTEST_FIELD` (converted from an originally-generated
  `AUTOTEST_FLD_<timestamp>` code in the 2026-08-26 conversion) — every live run must complete
  TC05 (delete) so the code is free for the next run.
- `field_page.resource` did not originally import `libraries/PropertiesReader.py` before the
  2026-08-26 navigator-fill conversion (PR #525) — if working on a similarly "not yet
  properties-driven" screen, check for this import explicitly; its absence only surfaces as a
  full-tree dryrun failure, not an obvious static error.
- Zero inline DB-verify calls in `field_iud.robot` — all DB ground-truth checks live inside the
  shared T2 keywords (`Verify Object Removed` etc.), not screen-local code.

## Filter wiring
Grid Code-column filter via the shared T2 `Find/Clear Object Row By Filter`, wrapped in
screen-local `Find Field Row By Filter`/`Clear Field Row Filter` keywords, wired into
Update/Find/Verify-Found/Delete.

## Credentials
Dedicated pair in `resources/credentials.py`: `FIELD_EC_USER`/`FIELD_EC_PASS` (defaults to
`EC_USER`/`EC_PASS` env vars, then `sysadmin`/`sysadmin`).

## Last verified
2026-08-27 (backfill re-run: full-tree dryrun 883/883 PASS, live 5/5 PASS, DB self-clean 0
residual `AUTOTEST%` rows in `OV_FIELD`) against the local sandbox EC environment
(`localhost:1521/ORCL`, `ECKERNEL_EC`). Selectors/labels themselves last confirmed live
2026-08-26 (PR #525/#529).
