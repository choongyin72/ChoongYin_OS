# SOW - Contract Capacity IUD (Configuration > Assets > Contract_Objects)

- **Screen:** Contract Capacity   **BF:** CO.2044   **View:** `OV_CONTRACT_CAPACITY`   **Base:** `CONTRACT_CAPACITY`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED,
  date-effective. Converted to the **Area pattern** (2026-08-26, PR #535): 5-TC structure,
  per-TC login/logout, pure-screen verification, properties-file-driven fill, explicit grid-filter
  wiring. Still OV-GM, not reclassified as plain Bank-shaped — the Business Unit + GO navigator
  step is real and required, carried forward unchanged from the original 2026-08-01 build.
- **Navigator shape:** single Business Unit dropdown (`nav:form:G:0:R:1:C:1:dd`) + GO — NOT a
  multi-level cascade. Value = `TS5 BU`, the SAME value the pre-existing Playwright driver
  (`py/contract_capacity_iud.py`, shipped 2026-08-01, live 8/8) already proved live — a real
  cross-check carried forward, not re-derived. Fill now delegates to the shared T2
  `Apply Navigator From Properties`, driven by `testdata/contract_capacity_navigator.properties`.
- **Grid id:** `manageObject:form:T_data` (empty until the navigator + GO completes).
- **Mandatory fields (Insert, `objectForm`):** Contract Capacity Code, Contract Capacity Name,
  Start Date, plus reference dropdowns Contract Name (=`TS5 Shipper B Firm`) and Location Name
  (=`TS5 Domestic Gas Storage`) — both PROVEN live by the pre-existing driver, both must resolve
  under the same Business Unit scope as the navigator or the inserted row is invisible in the
  filtered grid (OV-GM constraint).
- **Update (`updateAttributes`):** Contract Capacity Code read-only (guard); Contract Capacity
  Name is the only field exercised.
- **Delete (`objectdates`):** End Date = Start Date (zero-length window) → true delete, row leaves
  `OV_CONTRACT_CAPACITY`. Selector `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` is
  hardcoded (not label-driven) — documented rationale: the row packs Start Date (C:1) + End Date
  (C:3) with the End Date label at C:2, a shape the one-field-per-row label scan can't resolve.
- **Test data:** fixed test code `AUTOTEST_CONTRACT_CAPACITY` (confirmed free via a fresh
  oracledb query against `OV_CONTRACT_CAPACITY` before wiring it in — 0/0 before and after every
  run), not a generated/timestamped code (the original 2026-08-01 build used
  `AUTOTEST_CC<timestamp>`; the Area-pattern conversion fixed it, matching every other converted
  screen's convention).
- **Dev story (from PR #535, real narrative, not invented):** Contract Capacity's RF automation
  was originally built 2026-08-01 as a 4-TC suite with a single suite-level login, hardcoded
  field-id inline DB-verify wrappers (`Insert/Update Contract Capacity Record`,
  `Contract Capacity Should/Should Not Exist In DB`), and a timestamped test code. On 2026-08-26,
  under the owner's standing rule that any navigator-section screen matching Area's layout
  follows Area's full pattern, it was converted to 5 TCs (added TC04 Find), per-TC login/logout,
  properties-file-driven insert/update via the shared T2 `Insert/Update Object From Properties`,
  explicit `Find/Clear Contract Capacity Row By Filter` grid-filter wiring into
  Update/Find/Verify-Found/Delete (15 `Find Object Row By Filter` hits confirmed in output.xml),
  and PURE SCREEN verification only (zero inline DB-verify calls remain in
  `contract_capacity_iud.robot`, confirmed via grep). Live 5/5, full-tree dryrun 850/850, robocop
  7 issues (exact parity with Area's own reference-pattern baseline). No shared T1/T2 file changes
  in that round. The Playwright driver `py/contract_capacity_iud.py` was left UNTOUCHED — RF
  structural conversion only.
- **This backfill task (2026-08-28, Batch 4):** adds the documentation/evidence bundle that
  Section G's now-retired lean waiver had skipped around this already-converted, already-working
  automation — SOW/README/JOURNAL/evidence/CHECKLIST/KB map. No automation file touched.
- **Deliverables:** T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource`,
  suite `tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot`, testdata
  `contract_capacity_{navigator,insert,update,form_verify,grid_verify}.properties`, this SOW,
  `README.md`, `JOURNAL.md`, `evidence/`, `CHECKLIST.md`. Playwright driver
  `py/contract_capacity_iud.py` (historical, pre-existing, untouched) and `investigation/recon.py`
  (pre-existing) remain in the bundle from the original 2026-08-01 build; no new Playwright/
  investigation artifacts are produced by this backfill (owner decision 2026-08-27 — Universal
  Screen Engine replaces that role going forward).
