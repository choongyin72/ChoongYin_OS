# Navigator screens NOT matching Area's layout — parked for later

**Scope:** this doc tracks EC object screens that have a navigator section (OV-GM style) but whose
screen layout does NOT match Area's — so they are NOT auto-converted to Area's role-model pattern
(see `docs/bank-pattern-conversion-checklist.md`'s sibling rule for plain-Bank-shaped screens, and the
owner's 2026-08-26 standing directive: any navigator screen matching Area's layout MUST follow Area's
full pattern; a screen listed here is the explicit exception to that default).

**Area's layout, for reference (what "matching" means):** a manage-object OV-GM screen — mandatory
navigator (single dropdown, or a same-row/increasing-column cascade like Production Unit -> Area),
grid `manageObject:form:T_data`, New-Object popup form (`objectForm`), date-effective delete via
`objectdates` End Date = Start Date. Screens with a genuinely different shape (per-field navigator
groups instead of same-row columns, a POPUP-based child-object picker instead of a plain dropdown,
non-`manageObject:form:T_data` grid ids not already covered by the shared navigator keyword's design,
physical/non-date-effective delete, TV-style inline-editable grids, etc.) do not fit and belong here.

**How to use this doc:** when investigating any navigator-bearing screen and it turns out NOT to match
Area's layout, append a row below with the real reason (backed by live evidence, not assumption) — same
discipline as `ov-non-bank-targets.md`'s dated-note convention. Do not force a screen listed here into
Area's pattern without fresh re-verification; a screen might also be later found to fit after all
(re-verify, don't just trust an old entry) — same caution this project applies everywhere else.

## Screens

| Screen | BF_CODE | Real navigator shape | Why it doesn't match Area | Found |
|---|---|---|---|---|
| Stream - by Group Model (class STREAM, view OV_STREAM, URL `manage_object_groupmodel_nav`) | CO.0027 | Live DOM dump (`tmp/scripts/stream_group_model_nav_shape.py`, 2026-08-26): `nav:form:G:0` has FOUR mandatory dropdowns, but NOT on one row: Row R:1 holds Date(C:0)+Production Unit(C:1)->Area(C:2)->Facility Class 1(C:3) as a genuine same-row 3-level cascade (this part alone WOULD fit Area's pattern); then a wholly separate table-row R:2 carries just the label "Stream", and R:3:C:0 carries a 4th mandatory dropdown (options confirmed live: `AS1_FCTY_01_GAS_PROD`/`AS1_FCTY_01_OIL_PROD`/`AS1_FCTY_01_WAT_PROD`) that must also be filled + GO clicked before the grid (`manageObject:form:T_data`) loads. This directly contradicts this session's own pre-task "known facts" note, which assumed the 4th level was "Facility Class 2" continuing the same row at C:4 — live recon found no such C:4 field; the real 4th field is R:3:C:0, labelled "Stream", not "Facility Class 2". | The shared T2 `Apply Navigator From Properties` keyword (resources/manage_object.resource) is explicitly documented as covering ONLY the "uniform single-row, C:1..C:N cascade shape" and calls `Apply Navigator` (GO) once, immediately after filling the last column on the SAME row/`${row}` parameter. It has no mechanism for a 4th mandatory value that lives on a different table-row (R:3 vs R:1) within the same `G:0` group before GO fires. Per the ec-area-pattern-new-screen skill's Step 0 hard rule ("Does NOT fit — do not force it"), this was NOT hacked around by editing the shared keyword or by guessing a workaround; it is logged here instead. Note this is a genuinely NEW third shape — not the already-covered "single dropdown"/"same-row cascade" cases, and not the already-excluded "per-field `G:1`/`G:2`/`G:3` groups" case either (it is still one `G:0` fieldset, just spread across non-contiguous rows). Recon otherwise fully confirmed CO.0027/STREAM/OV_STREAM/`manage_object_groupmodel_nav` matches the task's other facts: OV, VERSIONED (End Date=Start Date delete), grid `manageObject:form:T_data`, mandatory `objectForm` fields Stream Code/Stream Name/Start Date/Stream Type/Alloc Period, `AUTOTEST_STREAM_GROUP_MODEL` confirmed free in `OV_STREAM` (0 rows). | 2026-08-26 |
