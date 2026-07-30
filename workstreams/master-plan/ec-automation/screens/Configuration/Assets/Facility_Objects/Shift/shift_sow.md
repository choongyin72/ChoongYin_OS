# SOW - Shift IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Shift   **BF:** CO.0224   **View:** `OV_SHIFT`   **Base:** `SHIFT`
- **Type:** OV-GM (grid `manageObject:form:T_data`) with a **mandatory FREE-TEXT extra:
  Start Time (HH:MI)** - the field class the OV-GM generator cannot fill (the original park
  reason). Hand-built instead; value `07:00`, format read from the EXISTING P1 S001 row
  (owner technique: scan an existing row's populated values to learn every element).
- **Navigator = SPECIFIC P1 values** (P1 Production Unit -> P1 Area -> P1 Facility 1; lists the
  4 existing P1 shifts - owner screenshot 2026-07-31). **Op Production Unit = nav PU**
  (parent-matching, from the existing row's values).
- **Start Date = 2020-01-01** (existing P1 shifts effective 2011-01-01/15).
- DELETE = End Date = Start Date. Unique `AUTOTEST_SH_<timestamp>` per run; self-cleaning.
- View confirmed by REAL lookup: OV_SHIFT contains 'P1 S001' (4 rows total).

## Known risks
- Nav scope is DATA-dependent (P1 objects); re-derive if renamed/removed.
- Start Time is free text - EC may accept malformed values silently; '07:00' matches the
  existing-data format exactly.
