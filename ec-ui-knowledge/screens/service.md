# Screen: Service

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective) — navigator-GATED.
- **BF_CODE:** CO.2103 — **Treeview:** Configuration > Assets > Service_Objects > Service
- **DB view:** `OV_SERVICE` (key `CODE`; also `NAME`, `OBJECT_START_DATE`, `OBJECT_END_DATE`,
  `CONTRACT_CODE`, `TRANSPORT_SYSTEM_CODE`)
- **Last verified:** 2026-08-27 · EC 14.2.4 · local sandbox · RF suite structurally converted to the
  Area pattern (PR #552, merged 2026-08-26); this backfill (2026-08-27) transcribed the selectors
  below from `service_page.resource`'s own Variables section, re-ran the suite live for evidence, and
  did **not** modify any automation file.

## Selectors `[from service_page.resource Variables section, transcribed 2026-08-27]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Grid filter input | `manageObject:form:T:sfilter0_ft_filter` (Code column) |
| Navigator dropdown (Business Unit, MANDATORY) | `nav:form:G:0:R:1:C:1:dd` — value `TS3 BU1` |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/service_navigator.properties` |
| Grid-filter | `Find/Clear Service Row By Filter` → shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Service Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — same row-packing rationale as Bank's/Area's own `_DEL_ENDDATE` constants: Start Date sits at `C:1`, End Date label at `C:2`, End Date input at `C:3`) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Business Unit dropdown (`TS3 BU1`) + GO. Contract
  Area/Contract are further nav columns VISIBLE on the screen but are OPTIONAL filters — confirmed
  live 2026-08-26: GO with only Business Unit set already loads the grid.
- **Insert form (`objectForm`):** Service Code*, Service Name*, Start Date* (mandatory) plus
  dropdowns Service Template, Service Type, Service Status (all `__FIRST__`), and two fields that
  are BOUND to the navigator's Business Unit scope, not free-choice: **Contract = `TS3 GTA Shipper A`**,
  **Transport System = `TS3 Transport System`** — these must match the Business Unit picked in the
  navigator (`TS3 BU1`) or the inserted row will not be visible/consistent under that nav scope. Values
  confirmed live by the pre-existing driver (shipped 2026-08-01, live 8/8) and unchanged by the
  PR #552 structural conversion.
- **Update form (`updateAttributes`):** Service Name only — Service Code is read-only.
- Field labels are **screen-prefixed**: "Service Code" / "Service Name" (NOT the generic "Code"/"Name"
  Bank/Object List use) — every shared T2 call passes `code_label=Service Code` accordingly.

## Quirks
- **OV-GM grid stays empty until the navigator is filled + GO'd** — same defining characteristic as
  Area/the whole OV-GM family.
- **Contract/Transport System are navigator-scope-bound, not independent dropdowns** — picking a
  Contract/Transport System that doesn't belong to the navigator's Business Unit is expected to
  produce an inconsistent/invisible row (not tested as a negative case here; the mandatory-field set
  above is the only combination proven live).
- **Intermittent navigator-dropdown-panel click-intercept flake (found during this 2026-08-27
  backfill's evidence capture, NOT introduced by this backfill):** the Business Unit navigator's
  PrimeFaces autocomplete panel (`nav:form:G:0:R:1:C:1:dd_panel`) occasionally does not finish
  hiding/fading before the suite's next step clicks the grid filter input
  (`manageObject:form:T:sfilter0_ft_filter`), producing a Playwright
  `TimeoutError: locator.click: Timeout 30000ms exceeded ... subtree intercepts pointer events`.
  Reproduced across 8 live attempts in this backfill session (2026-08-27), landing on a DIFFERENT TC
  each time (TC01, TC02, TC03, or TC04) — never the same TC twice in a row, and never present in
  `--dryrun` (structure-only, no browser). When it fires, the underlying DB operation for that TC's
  own step is unaffected (confirmed via `libraries.DbVerify.fetch_object("OV_SERVICE", ...)` each
  time) — this is a click-timing race on the grid-filter step, not a data-integrity or logic defect.
  Best clean result obtained after 8 attempts: 4/5 (only TC01 hit the flake). See
  `screens/Configuration/Assets/Service_Objects/Service/JOURNAL.md` for the full attempt log. Treat
  as a known, disclosed environment characteristic of the shared `Apply Navigator From Properties` →
  grid-filter sequence — not fixed by this backfill (backfill is documentation/evidence only, no
  automation file was touched).
- **Fixed test code `AUTOTEST_SERVICE`** (not a generated/unique code) — every run must complete TC05
  so the code is free for the next run.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `pageobjects/Configuration/Assets/Service_Objects/service_page.resource` (T2
  `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `tests/Configuration/Assets/Service_Objects/service_iud.robot` (5 TCs: Clean State/Insert/Update/
  Find/Delete, per-TC Login/Logout, fixed code `AUTOTEST_SERVICE`). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Service_Objects/service_iud.robot`.
- **Playwright (pre-existing, kept unchanged per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` —
  Universal Screen Engine replaces this role going forward):** driver `py/service_iud.py` (shared
  engine `ec_object_iud.py`).
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `screens/Configuration/Assets/Service_Objects/Service/`.
