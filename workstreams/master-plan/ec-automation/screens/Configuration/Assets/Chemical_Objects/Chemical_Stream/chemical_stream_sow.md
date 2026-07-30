# SOW - Chemical Stream IUD (Configuration > Assets > Chemical_Objects)

- **Screen:** Chemical Stream   **BF:** CO.0258   **View:** `OV_CHEM_STREAM`   **Base:** `CHEM_STREAM`
- **Type:** OV-GM (grid `manageObject:form:T_data`) with a **mandatory Pick-from-EC-Object POPUP**
  (From Connection). Navigator = SPECIFIC P1 values (P1 Production Unit -> P1 Area -> P1 Facility 1):
  the popup source is EMPTY under the first-available AS1 scope (the original park reason; owner
  screenshot 2026-07-30 proved the P1 scope populates it with CHEM_TANK entries P1 CT001..CT014).
- **The popup is NOT the standard object_popup** (recon-verified): `stream_node_ref_popup` has its
  own inner navigator (inherits the outer P1 scope), an **Object Type dd** (`nav:form:G:4`, EMPTY on
  open -> select `CHEM_TANK`), an **inner GO** (`button:form:B`), and its list grid id is
  **`manage_object_nav_nav:form:T_data`** (NOT `PopupList:form:T_data`). Hence screen-LOCAL popup
  handlers in both the driver and the T3 - the generic engine `pick_popup` / T1
  `Pick First EC Object Popup` do not fit (they wait for PopupList and drive no inner steps).
- **Insert extras:** Chemical Stream Type (mandatory dd, first-available = 'Pump Stream');
  From Connection = first CHEM_TANK row under the P1 scope. Form order quirk: Start Date is R:0
  (BEFORE Code/Name) - the T3 fills it first.
- **Start Date = 2020-01-01.** DELETE = End Date = Start Date. Unique `AUTOTEST_CHS_<timestamp>`
  per run; self-cleaning.

## Known risks
- Nav scope + popup source are DATA-dependent (P1 chem tanks); if removed/renamed, re-derive a scope.
- Popup internals (grid id / Object Type dd position) are per-popup-type facts - if EC changes the
  stream_node_ref_popup layout, re-recon with tmp/recon_chs_popup2.py (kept in investigation/).
