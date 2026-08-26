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

_None logged yet as of 2026-08-26 — this doc is a placeholder ready for the first entry. Append rows in
this format:_

| Screen | BF_CODE | Real navigator shape | Why it doesn't match Area | Found |
|---|---|---|---|---|
