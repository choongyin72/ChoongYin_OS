# SOW - Contract Inventory (Configuration > Assets > Contract_Objects)

- **Screen:** Contract Inventory   **BF:** CO.2054   **View:** `OV_CONTRACT_INVENTORY`   **Base:** `CONTRACT_INVENTORY`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- **Pattern:** Area pattern (converted PR #556, 2026-08-26). Not Bank-shaped — this screen keeps its own
  genuine mandatory navigator, unlike Area/Bank's no-navigator or single-value cases; the conversion is a
  **structural** upgrade (5-TC/per-TC-login/pure-screen-verify/properties-driven/explicit-filter-wiring),
  not a reclassification of the screen itself.

## Navigator shape (live-verified, 2026-08-26, not re-derived from the pre-existing registry note)
Single group (`G:0`), single row (`R:1`), increasing-column shape, same as Area/Facility Class 1:
- `C:1` **Business Unit** — genuinely mandatory-yellow (`rgb(252, 249, 192)`) **and** empty until filled.
  This is the ONLY column that gates the grid load.
- `C:2` **Contract Area** — stays white/optional even after `C:1` is filled (confirmed live via a
  mandatory-yellow DOM recheck after filling `C:1` — filling Business Unit does NOT turn Contract Area
  yellow). Kept filled anyway in the navigator properties file, for behavioral parity with the
  already-proven prior driver scope (not because it is required).
- `C:3` **Contract** — likewise optional, not filled by this suite.

This corrected the pre-existing registry note ("Business Unit -> Contract Area cascade"), which read as
a genuine 2-level mandatory cascade but was not re-verified live before this conversion — the live DOM
check found only 1 of the 2 columns actually gates the grid.

Navigator fill delegates to the shared T2 `Apply Navigator From Properties`
(`resources/manage_object.resource`), driven by `testdata/contract_inventory_navigator.properties`, with
**zero shared-file changes** required (the same-row/increasing-column shape was already supported).

## Grid / cell shape
- Grid: `manageObject:form:T_data`, loads only after navigator + GO.
- Columns confirmed live (`manageObject:form:T_head` scan): Contract Inventory Code / Contract Inventory
  Name / Start Date / End Date — same 4-column shape as Area/Facility Class 1.
- `objectForm` labels confirmed live, screen-prefixed: **Contract Inventory Code**, **Contract Inventory
  Name** (mandatory), **Start Date** (mandatory, date-only, lives in `objectdates`, not `objectForm`),
  plus a "Contract name" dropdown fixed to `TS5 Shipper C` (carried over unchanged from the pre-conversion
  driver, `py/contract_inventory_iud.py`). No "Business Unit"/"Contract Area" field exists on `objectForm`,
  so there is no navigator/form field-reuse conflict.
- Delete: `objectdates` End Date = Start Date (true delete in `OV_CONTRACT_INVENTORY`). The delete-End-Date
  field id is hardcoded (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`) — same documented rationale
  as Area's own del-enddate constant (Start Date/End Date share a packed row the label scan cannot resolve
  safely).

## Test data
Fixed test code `AUTOTEST_CONTRACT_INVENTORY` (not a generated/timestamped code) — confirmed absent from
`OV_CONTRACT_INVENTORY` via a fresh `oracledb` connection both before and after the 2026-08-26 live run.
Every run must complete TC05 (delete) so the code stays free for the next run.

## Dev story (from PR #556, 2026-08-26)
Contract Inventory already had a working OV-GM IUD build from PR #314 (2026-08-02, 4 TCs, live 4/4 +
Playwright 8/8, `verify_screen.py` OVERALL PASS). PR #556 converted the RF suite's *structure* only, per
the 2026-08-26 owner standing rule that any EC screen whose navigator matches Area's layout must follow
Area's full pattern: added TC04 Find (4 -> 5 TCs), moved to per-TC Login/Logout, switched the generated
test code to the fixed `AUTOTEST_CONTRACT_INVENTORY`, moved insert/update/verify to properties-file-driven
T2 calls, added explicit `Find/Clear Contract Inventory Row By Filter` grid-filter wiring into
Update/Find/Verify-Found/Delete (26 `Find Object Row By Filter` hits in `output.xml`), and removed the
screen-local `Contract Inventory Should/Should Not Exist In DB` inline DB-verify wrappers in favor of
pure-screen verification (DB checks now live solely inside the shared T2 `Verify Object Removed`). The
real gotcha in that PR was the navigator-mandatory recon itself: the pre-existing registry note implied a
genuine 2-level cascade, and a shallower rebuild could have carried that assumption forward unverified.
The live mandatory-yellow DOM check caught that only Business Unit is actually mandatory — exactly the
kind of fact this project's "verify, don't assume" rule exists to catch. The Playwright driver
`py/contract_inventory_iud.py` was left untouched — RF-only structural conversion.

**Note on this backfill task's own brief:** the dispatch instructions for this backfill described a
"detached-HEAD collision-recovery" story for this screen. That story was NOT found in PR #556's body,
its commit message, or its branch reflog (checked all three) — see `JOURNAL.md` "Blockers -> resolution"
for what was actually verified instead: a real, disclosed `credentials.py` multi-pair carry-over flagged
by the reviewer at merge (same shared-checkout hazard class, but a credentials-file collision, not a git
branch/HEAD collision).

## Deliverables
- Driver (untouched): `py/contract_inventory_iud.py`
- T3: `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource`
- Suite: `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot`
- Testdata: `testdata/contract_inventory_{navigator,insert,update,form_verify,grid_verify}.properties`
- This SOW, `README.md`, `JOURNAL.md`, `evidence/`, `CHECKLIST.md` (this backfill, 2026-08-28)
