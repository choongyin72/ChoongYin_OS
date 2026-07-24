# Screen: <Screen Name>

**Status:** Draft / Verified
**Last verified:** YYYY-MM-DD
**Verified against EC version/environment:** e.g. plutodev, ecaas_clp_hongkong, v.X.X

---

## Navigation

- URL / path: `...`
- Menu path (if applicable): `Navigator > ... > ...`
- Any prerequisite state (logged in as role X, specific tab open, etc.)

---

## Key elements

| Purpose | Selector | Notes |
|---|---|---|
| Search/filter input | `#...` or `[name=...]` | exact-match only |
| Record row (list view) | `...` | pattern for matching a row by text |
| Edit/Open button | `#...` | |
| Field: <name> | `#...` | type, required?, validation quirks |
| Field: <name> | `#...` | |
| Save button | `#...` | |
| Secondary confirm dialog (if any) | `#...` | some screens require this, some don't |
| Delete button | `#...` | |
| Success confirmation | selector or text pattern | how to detect save succeeded |
| Error/validation message | selector or text pattern | how to detect failure |

---

## Save / Update / Delete sequence (this screen specifically)

1. ...
2. ...
3. ...

Note any deviation from the generic sequence in `EC_UI_SOP.md` Section 2.

---

## Known quirks

- e.g. "Save button stays disabled until dropdown X is touched, even if a valid default is pre-selected."
- e.g. "This screen shows a secondary confirm modal only when deleting, not when saving."
- e.g. "Table refresh after save takes ~2s longer than `${WAIT_TIMEOUT}` default; add explicit wait."

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | Initial discovery | First automation of this screen |
| | | |
