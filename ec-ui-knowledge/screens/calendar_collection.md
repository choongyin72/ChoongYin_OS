# Screen: Calendar Collection

- **Type:** OV (custom-URL, EC Object Configuration, date-effective) — CD.0105
- **Treeview path:** Configuration > Assets > Date Objects > Calendar Collection
- **Open via:** menu search (same mechanism as other OV screens)
- **DB view (ground truth):** `OV_CALENDAR_COLLECTION` (base `CALENDAR_COLLECTION`/`CALENDAR_COLL_VERSION`;
  key `CODE`; also `NAME`, `OBJECT_START_DATE`, `OBJECT_END_DATE`) — 7 pre-existing rows, confirmed
  unchanged at last verification.
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox (`localhost:1521/ORCL`) · live RF I-U-D
  5/5 DB-verified (re-run of the already-merged PR #449 suite, no automation changes made).
- **Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated) — mirrors
  `bank.md`/`calendar.md`'s own shape. Converted from an older hardcoded-field-id pattern in PR #449
  (2026-08-23, Batch 6, final of the 5-screen Date Objects pool).

## Custom-URL / no-GO navigation shape (distinct from plain manage-object OV)
This screen has **no navigator GO button at all** — confirmed live 2026-08-23: `manage_object_nav`
grid count=0, GO button count=0. The grid loads directly on open; refresh is via the **toolbar
Refresh** icon, which T2's `Save And Refresh List` keyword (in `resources/manage_object.resource`)
already auto-detects and falls back to for this shape — no shared-file changes were needed to
support it.

## Selectors `[from pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource Variables section]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | **`nav:form:T_data`** (custom-URL table id — NOT `manage_object_nav`, which is absent on this screen) |
| Delete field (End Date) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |
| Row filter | shared T2 `Find Object Row By Filter`/`Clear Object Row Filter` against `${CC_TABLE}` (= `nav:form:T_data`) |
| Mandatory form labels (Insert) | `Code`, `Name` — **generic labels, NOT screen-prefixed** (confirmed live via a field-label recon of every `objectForm` label; contrasts with Calendar's screen-prefixed "Calendar Code"/"Calendar Name") |
| Start Date | mandatory, Insert-only (not present in `updateAttributes`) |
| Update-only labels | Code (read-only), Name, Description, Comments |

### New-Object form (`objectForm`) — confirmed live 2026-08-23, 8 ECCell labels total
`R0 Code*` (generic), `R1 Name*` (generic), `R2 Start Date*` (date, Insert-only), `R3 End Date`
(date, optional), `R4 Description`, `R5 Comments`. **No weekday-indicator checkboxes on this EC
build** — contrary to the pre-conversion page object's stale docstring, which had implied Calendar's
7 weekday checkboxes might carry over here; a live scan corrected this before the conversion.

### Update tab (`updateAttributes`) — 4 labels confirmed live
Code (read-only), Name, Description, Comments. Start/End Date are NOT part of `updateAttributes`
(they live in the separate `objectdates` sub-form), same convention as Bank/Country.

### Delete (`objectdates`)
Row R0: End Date `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`. **EC Object delete = set
End Date = Start Date -> Save** (row leaves `OV_CALENDAR_COLLECTION`). Confirmed present in the DOM
even though there's no visible "Object Dates" sub-tab link on this screen (same convention as
Bank/Calendar/Royalty Owner).

## Mandatory / yellow fields
- **Insert:** Code, Name (both mandatory-yellow, `MandatoryCellStyle`-confirmed), Start Date
  (effective/mandatory but Insert-only).
- **Update:** none beyond Name being the only field this suite exercises; Code is read-only.
- **Delete:** End Date (must be set = Start Date for a true delete).

## Quirks
- **Custom-URL OV with NO GO button** — the defining quirk of this screen (shared with Calendar,
  CD.0024). Do not look for a navigator GO; use the toolbar Refresh fallback.
- **Member calendars** (the individual calendars belonging to a collection) live in a SEPARATE
  child grid/tab — out of scope for this object-level IUD; only Code/Name/Start Date at the
  object level are tested.
- Fixed reusable test code `AUTOTEST_CALENDAR_COLLECTION` (not a generated-unique code) — confirmed
  free via a fresh DB connection both before the PR #449 build and again at this KB map's
  last-verified re-check (2026-08-28: 0 residual rows).

## Automation (code lives in `workstreams/master-plan/ec-automation` — this file is the MD selector reference)
- **RF:** T3 `pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource` +
  suite `tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot` (T2 `manage_object`
  + `DbVerify.py`). Properties: `testdata/calendar_collection_{insert,update,form_verify,grid_verify}.properties`.
  Dedicated credentials: `CALENDAR_COLLECTION_EC_USER`/`CALENDAR_COLLECTION_EC_PASS` in
  `resources/credentials.py`. Validated live 5/5 (2026-08-28 re-run).
- **Playwright:** legacy per-screen driver `screens/Configuration/Assets/Date_Objects/Calendar_Collection/playwright/ec_iud_calendar_collection.py`
  (predates the Bank-pattern conversion; left untouched — the Universal Screen Engine is the
  owner-decided replacement for new Playwright drivers going forward, per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H).
