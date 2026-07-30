# OV IUD sweep - PARKED screens (not plain Bank-layout; revisit later)

Rule: BUILD only plain Bank-layout OV (manage_object_nav, single Date+GO nav, mandatory =
Code/Name/Start Date only, NO mandatory dropdowns). Park anything else with the reason.

| Screen | BF | View | Reason parked | Recon detail |
|---|---|---|---|---|
| Storage Flow | CO.2091 | OV_STORAGE_FLOW | mandatory dropdowns | R4 Flow Direction (dd, mand) + R5 Storage (dd, mand); folder Tank and Storage Objects; grid empty on default GO though DB has 23 rows |

## Chemical Stream (CO.0258) - PARKED 2026-07-30 (verified reason)
- OV-GM, view OV_CHEM_STREAM. Mandatory field **From Connection** is a nav-scoped Pick-from-EC-Object popup.
- Under the automation navigator scope (first-available PU = 'AS1 EC Exploration Norway'), the popup source
  grid `PopupList:form:T_data` never renders = **empty source list** (that PU has no connectable objects).
- Ground truth: py/chemical_stream_iud.py driver ABORTED at insert_ui - "popup opened but grid never appeared
  (empty source list - check the navigator scope is set first)". nav_pu captured OK; only the popup fails.
- ROOT CAUSE: mandatory nav-scoped popup needs a DATA-BEARING scope (a PU with existing connections), not the
  sparse first-available test PU. Generic first-available IUD cannot satisfy it without seeding data.
- RESUME when: a data-bearing PU scope is chosen for the cascade (or a connection is seeded), then the popup
  source lists. Same pattern likely affects Chemical Stream Hookup (CO.0260) + other *Connection popup screens.
