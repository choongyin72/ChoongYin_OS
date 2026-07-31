# SOW - Create Calculation IUD (Configuration > Assets > Calculation_Objects)

- **Screen:** Create Calculation   **BF:** CO.1042   **View:** `OV_CALCULATION`   **Base:** `CALCULATION`
- **Type:** context-gated TV-STYLE dual grid (header `calculation:form:T_data` + companions
  `calculation_version:form` / `static_param:form`). Navigator = Date + ONE mandatory
  **Calculation Context** dd (first-available; 14 contexts) + GO.
- **INSERT** = toolbar Insert 'Public Calculations' -> BLANK INLINE ROW (dynamic index - EC drops it
  mid-grid) -> cells C0 Code / C1 Name / C2 Start Date (real keystrokes + Tab) + **C4 Calculation
  Period / C5 Calculation Type dds** (mandatory-YELLOW on the blank row only - they render as plain
  text on saved rows; values 'Day'/'Equations' from the sibling rows, scan-existing-row technique).
  A save without C4/C5 is SILENTLY rejected (staged row survives GO + an UNSAVED CHANGES dialog).
- **UPDATE** = select the calc row -> edit the VERSIONS grid's Calculation Name
  (`calculation_version:form:T:0:C0_in`) - the AUTHORITATIVE name source; the header C1 only
  mirrors it (editing C1 does not persist - proven).
- **DELETE** = select the row -> the purpose-built **DELETE CALCULATION** button (+ YES confirm) -
  physically removes calc + version (DB-verified). NOT End=Start.
- **Scope: calc HEADER IUD only** - equations/variables/mappings are the calc-lab program's scope
  (branch feature/ec-calc-lab). Never touch the existing EC_GRS_TO_NET_* calcs.
- Start Date 2020-01-01; unique `AUTOTEST_CC_<timestamp>` per run; self-cleaning.

## Known risks
- Row indices are DYNAMIC (insert lands mid-grid; order changes after save) - all row access is by
  C0-value scan, never a fixed index.
- Row checks must read INPUT VALUES via JS - TV cells are inputs, invisible to text-based row scans.
