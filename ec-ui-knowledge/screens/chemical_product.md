# Screen: Chemical Product

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object`); plain
  manage-object (optional date nav + GO only, no mandatory dropdown/cascade).
- **BF_CODE:** CO.0072 — **Treeview:** Configuration > Assets > Chemical_Objects > Chemical
  Product _(DB treeview JSON)_
- **DB view:** `OV_CHEM_PRODUCT` (key `CODE`; underlying table `CHEM_PRODUCT`; `NAME`,
  `OBJECT_START/END_DATE`).
- **Last verified:** 2026-08-24 — EC 14.2.4 — local sandbox — PR #486, live RF 5/5, full-tree
  dryrun 779/779, robocop parity with `chemical_transport_tank_iud.robot` (11 issues both), DB
  self-clean via fresh connection.

## Selectors `[from chemical_product_page.resource, 2026-08-24 scan]`
| Purpose | Selector |
|---|---|
| Grid id | `manage_object_nav_nav:form:T_data` (`${CHEM_PRODUCT_TABLE}` = shared `${OV_MANAGE_OBJECT_TABLE}` constant — same manage-object family as Bank/Berth/Chemical Transport Tank) |
| Delete field id | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date, `objectdates` tab) |
| Grid filter | `Find Object Row By Filter` / `Clear Object Row Filter` (shared T2) via screen wrappers `Find Chemical Product Row By Filter` / `Clear Chemical Product Row Filter` |

### Form labels (T3 resolves BY LABEL, `@{CHEM_PRODUCT_FORM_LABELS}`)
`Chemical Product Code` — `Chemical Product Name` — `Meas. Units`. Screen-prefixed labels (NOT
the generic "Code"/"Name" Bank/Object List use).

### Insert form (`objectForm`) — mandatory fields
**Chemical Product Code*** — **Chemical Product Name*** — **Start Date*** (date) — **Meas.
Units*** (reference dropdown, `mand=True`, NOT a cascade — confirmed by a raw dropdown-options
dump with no "Dependent field" banner; literal option value `Liter` used, not `__FIRST__`).
Optional, deliberately not filled: Product Type, Vendor Company, Vendor Comment, Est. Days For
Delivery, Description.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Chemical Product Code` (read-only) — **`Chemical Product Name`** (only field updated). Start
Date is Insert-only, not present in `updateAttributes` (same as Bank/Berth/Chemical Transport
Tank). Delete: **End Date = Start Date** (zero-length-window close) — but see Quirks below, this
alone is NOT sufficient on this screen.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_product_page.resource`
  (label-driven, properties-file-driven) + suite `tests/.../chemical_product_iud.robot` — live
  5/5 (TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete).
- **No Playwright bundle** — lean RF-only build per `ec-bank-pattern-new-screen`; items 4/5 of the
  deliverable checklist stay permanently waived (Universal Screen Engine replaces that role).
- **Screen-scoped cleanup library:** `libraries/ChemicalProductCleanup.py`
  (`remove_chem_usage_report_conf_child`) — called from `Delete Chemical Product Record And Save`
  immediately before the standard End=Start Save.
- **Gate:** live RF 5/5, full-tree dryrun 779/779, robocop parity with
  `chemical_transport_tank_iud.robot`.

## Quirks
- **Delete does NOT work via the standard End Date = Start Date Save alone** — this is a
  documented **EC PRODUCT DEFECT**, not an automation gap. `CHEM_PRODUCT` auto-creates a 1:1
  `CHEM_USAGE_REPORT_CONF` child row on insert with a NO-ACTION FK; that FK silently blocks the
  standard delete (the web UI swallows the resulting ORA-02292/ORA-20102, Save appears to
  succeed, but `OBJECT_END_DATE` stays NULL). There is **no UI screen** for
  `CHEM_USAGE_REPORT_CONF`. Fix: remove the orphaned child row at DB level FIRST (via
  `ChemicalProductCleanup.remove_chem_usage_report_conf_child`), THEN do the normal UI End=Start
  Save. See `ec-ui-knowledge/EC_KNOWN_ISSUES.md` for the original PARKED entry (now UNPARKED with
  this fix applied).
- Meas. Units dropdown literal option `Liter` confirmed live (Liter, M3, bbls, %, US Gallons, cm,
  inch, voltage) — `__FIRST__` does not resolve to literal text for a round-trip compare on this
  field (same precedent as VAT Code/Sales Order).
- Distinct from the Area-pattern Chemical_* siblings in the same treeview group (Chemical Stream,
  Chemical Tank, Chemical Injection Point, Chemical Stream Hookup) — those carry an OV-GM
  navigator cascade; Chemical Product does not.
