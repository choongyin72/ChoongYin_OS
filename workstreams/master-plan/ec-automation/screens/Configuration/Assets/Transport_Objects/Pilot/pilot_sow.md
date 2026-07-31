# SOW - Pilot IUD (Configuration > Assets > Transport_Objects)

- **Screen:** Pilot   **BF:** CO.2079   **View:** `OV_PILOT` (8 rows, DB-verified)   **Base:** `PILOT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`) - navigator-GATED:
  3-level cascade (Production Unit -> Area -> Facility Class 1) first-available + GO.
- **Mandatory:** Pilot Code / Pilot Name / Start Date. Op Production Unit set first-available for
  grid visibility (standard OV-GM parent-matching).
- Start Date 2000-01-01. DELETE = End Date = Start Date. Unique `AUTOTEST_PL_<timestamp>` per run;
  self-cleaning; the existing 8 pilots untouched.
- Registry-first check confirmed Pilot was genuinely unbuilt (an earlier substring-based audit had
  wrongly reported it as covered - the exact-match audit and a `grep -c "^| Pilot |"` = 0 corrected that).
- Built by the proven OV-GM generator `tmp/gen_ovgm.py`; 8/8 driver and 5/5 gates on the FIRST run.

## Known risks
- None screen-specific: this is the plain gated-navigator family with no extra mandatory fields.
