# SOW - Price Rate IUD (Configuration > Assets > Sales_Objects)

- **Screen:** Price Rate   **BF:** CO.3024   **View:** `OV_PRICE_RATE`   **Base:** `PRICE_RATE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator: **single Business Unit dropdown** (`nav:form:G:0:R:1:C:1:dd`, C:1 only - not a
  multi-level cascade) + GO; value **"SS2 BU"**, confirmed live via the original OLD-pattern
  driver and carried unchanged through the Area-pattern conversion. Fields resolved BY LABEL
  (screen-prefixed "Price Rate Code"/"Price Rate Name", not the generic "Code"/"Name").
- Mandatory fields (insert): Price Rate Code, Price Rate Name, Start Date, Frequency (dropdown,
  no fixed proven value in this sandbox - `__FIRST__` used, same convention as other converted
  OV-GM screens' mandatory-but-unconstrained dropdowns), Business Unit (must equal the navigator
  scope "SS2 BU" or the inserted row is invisible under the filtered grid).
- IUD: INSERT -> UPDATE(Price Rate Name) -> FIND -> DELETE(End=Start). Fixed test code
  `AUTOTEST_PRICE_RATE` (confirmed free in `OV_PRICE_RATE` before use); self-clean = absent after
  delete.
- Deliverables: T3 `pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource`,
  suite `tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot`, testdata
  `testdata/price_rate_{navigator,insert,update,form_verify,grid_verify}.properties`, this SOW,
  `README.md`, `JOURNAL.md`, `CHECKLIST.md`, `evidence/`.

## Dev story

**Original build (2026-08-02):** built via `ec-object-iud-builder` - OV-GM classification, nav
cascade confirmed via `scripts/find_populated_scope.py` (PROVEN explicit value, not
first-available), generic engine (`ec_object_iud.py`) handled the nav/appear/absent/pagination
gestures with zero screen-specific tuning. `verify_screen.py` OVERALL PASS: robocop 0, hygiene 0,
dryrun 4/4, live RF 4/4, Playwright 8/8, DB residual 0.

**Area-pattern conversion (PR #534, merged 2026-08-26):** converted the RF automation from its OLD
pattern (bespoke inline navigator dropdown fill, 4 TCs, single suite-level login, screen-local
DB-verify wrapper keywords) to Area's full pattern: 5 TCs (added TC04 Find), per-TC login/logout,
fixed test code `AUTOTEST_PRICE_RATE`, properties-file-driven insert/update/verify, explicit
grid-filter wiring (`Find/Clear Price Rate Row By Filter`), and the Business Unit navigator fill
delegated to the shared T2 `Apply Navigator From Properties` keyword (via new
`testdata/price_rate_navigator.properties`, using the same "SS2 BU" value the prior OLD-pattern
driver already proved live). Zero inline DB-verify calls remain - all verification now goes
through T2's `Verify Object Insert Exists/Form Record/Found/Removed/Does Not Exist`. Price Rate
REMAINS OV-GM; this was a structural conversion, not a reclassification as plain Bank-shaped. Real
evidence cited in PR #534: live RF 5/5, full-tree dryrun 850/850, robocop 7 issues (parity with
Area's own 7-issue baseline), DB self-clean 0/0 (fresh oracledb connection, before+after), filter
keyword fired 14x, zero inline DB-verify calls (grep-confirmed). Old Playwright driver
`py/price_rate_iud.py` left untouched (out of scope for the RF-only conversion). No real
issue/flake was disclosed in PR #534's body itself.

**This backfill (2026-08-27, Batch 3, `docs/lean-deliverable-backfill-workorder.md`):** added the
retroactive JOURNAL/CHECKLIST/KB-map artifacts the 2026-08-23/26 lean waiver had skipped, refreshed
the pre-existing (2026-08-02) SOW/README to reflect the Area-pattern conversion, and captured fresh
dryrun + live evidence of the already-proven suite (see JOURNAL.md "Blockers -> resolution" for a
real environment flake hit and resolved during this evidence capture - not a Price Rate defect).
