# SOW — Chemical Product IUD

**Screen:** Configuration > Assets > Chemical Objects > Chemical Product (BF_CODE `CO.0072`).

## Classification
- **Type:** OV (EC Object Configuration / Manage-Object), date-effective, versioned.
- **Pattern:** Bank pattern (`ec-bank-pattern-new-screen`) — plain manage-object OV, **no mandatory
  navigator cascade** (optional date nav + GO only, confirmed live via `scan_ec_screen.py`,
  2026-08-24). Distinct from the Area-pattern siblings in the same Chemical Objects group
  (Chemical Stream, Chemical Tank, Chemical Injection Point, Chemical Stream Hookup), which DO
  carry an OV-GM navigator cascade and were backfilled separately under Batches 2/4.
- **DB view:** `OV_CHEM_PRODUCT` (key `CODE`; underlying table `CHEM_PRODUCT`).
- **Grid id:** `manage_object_nav_nav:form:T_data` — same manage-object family as Bank/Berth/
  Chemical Transport Tank; reused from T2's centralized `${OV_MANAGE_OBJECT_TABLE}` constant, not
  re-hardcoded.

## Navigator / grid / cell shape
- No mandatory dropdown/cascade in the navigator — optional date nav + GO only.
- Grid: standard manage-object row list, one row per `CODE`; filterable via the shared T2
  `Find Object Row By Filter` / `Clear Object Row Filter` keywords (explicit grid-filter wiring,
  matching Bank/Berth/Chemical Transport Tank's convention).
- Insert form (`objectForm`) mandatory fields (confirmed live via `scan_ec_screen.py`,
  2026-08-24): **Chemical Product Code**, **Chemical Product Name**, **Start Date**, **Meas.
  Units** (a reference dropdown, `mand=True`, NOT a cascade — no "Dependent field" banner on a raw
  dropdown-options dump). Optional fields (Product Type, Vendor Company, Vendor Comment, Est.
  Days For Delivery, Description) are deliberately left unfilled per the "IUD fills only needed
  fields" rule.
- Update form (`updateAttributes`): Chemical Product Code is read-only; only **Chemical Product
  Name** is updated. Start Date lives only in `objectdates`, not in `updateAttributes` (same
  pattern as Bank/Berth/State/Chemical Transport Tank).
- Delete (`objectdates` tab, field id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`): End
  Date = Start Date (zero-length-window close), the standard OV true-delete convention.

## Test data used
- Fixed test code `AUTOTEST_CHEMPROD` (confirmed absent from `CHEM_PRODUCT` before wiring in,
  2026-08-24), matching Bank/Berth/Chemical Transport Tank's convention rather than a
  dynamically-generated code.
- Insert: `Chemical Product Code=AUTOTEST_CHEMPROD`, `Chemical Product Name=AUTOTEST Chemical
  Product`, `Start Date=2000-01-01`, `Meas. Units=Liter` (a literal option value from the live
  dropdown dump — Liter/M3/bbls/%/US Gallons/cm/inch/voltage — not `__FIRST__`, matching the VAT
  Code/Sales Order precedent that `__FIRST__` never resolves to literal text for a round-trip
  compare).
- Update: `Chemical Product Name=AUTOTEST Chemical Product UPDATED` (Meas. Units left unchanged).
- Dedicated per-screen credentials: `CHEMICAL_PRODUCT_EC_USER` / `CHEMICAL_PRODUCT_EC_PASS`
  (`resources/credentials.py`, standing 2026-08-22 decision — every EC screen gets its own
  credential pair).

## Dev story (from PR #486, merged 2026-08-24)
This was a genuinely new, from-scratch Bank-pattern RF IUD build — zero prior RF/Playwright
automation existed for Chemical Product before PR #486. The real gotcha was Delete: this screen
had a previously-documented EC PRODUCT DEFECT (`ec-ui-knowledge/EC_KNOWN_ISSUES.md`) where
`CHEM_PRODUCT` auto-creates a 1:1 `CHEM_USAGE_REPORT_CONF` child row on insert, and that child's
NO-ACTION FK silently blocks the standard End Date = Start Date UI delete — the web UI swallows
the resulting ORA error, Save appears to succeed, but `OBJECT_END_DATE` stays NULL. There is no UI
screen for `CHEM_USAGE_REPORT_CONF`. The fix (already prescribed in `EC_KNOWN_ISSUES.md`) was
implemented as a new screen-scoped library, `libraries/ChemicalProductCleanup.py`, which removes
the orphaned child row at DB level immediately before the normal UI End=Start Save — called from
`Delete Chemical Product Record And Save` in the T3 page object. This kept the shared
`resources/manage_object.resource` / `resources/common.resource` / `libraries/DbVerify.py`
completely untouched; the workaround lives entirely in Chemical Product's own new library file.
That previously-PARKED known issue is now UNPARKED with the fix applied (`EC_KNOWN_ISSUES.md`
status line updated in the same PR).

## Lessons
- Check `EC_KNOWN_ISSUES.md` before treating a screen's Delete step as trivial — this exact
  screen was already flagged there and the fix was already written down; it just needed applying,
  not re-discovering.
- A screen-specific DB workaround belongs in a screen-scoped library file, not a shared T1/T2
  file — keeps the blast radius contained to one screen.
