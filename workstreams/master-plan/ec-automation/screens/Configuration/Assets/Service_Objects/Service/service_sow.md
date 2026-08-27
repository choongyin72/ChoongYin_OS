# SOW - Service IUD (Configuration > Assets > Service_Objects)

- **Screen:** Service   **BF:** CO.2103   **View:** `OV_SERVICE`   **Base:** `SERVICE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator: SINGLE Business Unit dropdown (`nav:form:G:0:R:1:C:1:dd`, value `TS3 BU1`) + GO. Contract
  Area/Contract are further nav columns visible on the screen but are OPTIONAL filters — GO with only
  Business Unit set already loads the grid (confirmed live 2026-08-26).
- Fields BY LABEL, screen-prefixed ("Service Code"/"Service Name", not generic "Code"/"Name"). Insert
  mandatory set: Service Code*, Service Name*, Start Date* + dropdowns Service Template/Service
  Type/Service Status (`__FIRST__`) + two navigator-scope-bound fields: **Contract = `TS3 GTA Shipper A`**,
  **Transport System = `TS3 Transport System`** (must match the Business Unit navigator scope).
- IUD: INSERT -> UPDATE(Service Name) -> FIND -> DELETE(End=Start). Test data — ORIGINAL 2026-08-01
  build used a generated `AUTOTEST_SV<timestamp>` code; the 2026-08-26 conversion (PR #552) switched
  to a **fixed** `AUTOTEST_SERVICE` code (confirmed absent from `OV_SERVICE` before being wired in).
  Self-clean = absent in `OV_SERVICE`.
- Deliverables: driver `py/service_iud.py` (Playwright, pre-existing, kept unchanged — waived from
  further build per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`), T3
  `pageobjects/Configuration/Assets/Service_Objects/service_page.resource`, suite
  `tests/Configuration/Assets/Service_Objects/service_iud.robot`, this SOW, `README.md`, `JOURNAL.md`,
  `evidence/`, `CHECKLIST.md`, `VERIFY-REPORT.md` (auto-generated, 2026-08-01 build only).

## Dev story - 2026-08-01 base build
Built via the reusable OV-GM engine/generator (`tmp/gen_ovgm.py`): label-driven T3, Playwright driver +
RF T3/suite, `verify_screen.py` OVERALL PASS (robocop 0, hygiene 0, dryrun 4/4, live RF 4/4 + Playwright
8/8, DB residual 0). See `JOURNAL.md`'s 2026-08-01 entry for the full account.

## Dev story - 2026-08-26 structural conversion (PR #552)
Converted from the OLD structure (bespoke inline navigator fill, 4 TCs, single suite-level login) to
Area's full pattern: shared T2 `Apply Navigator From Properties` (driven by the new
`service_navigator.properties`, value `TS3 BU1` - the same value the pre-existing proven driver
already used live), 5 TCs (added TC04 Find), per-TC login/logout, fixed test code `AUTOTEST_SERVICE`,
properties-file-driven insert/update preserving the exact pre-existing mandatory-field set, explicit
grid-filter wiring (`Find/Clear Service Row By Filter`), zero inline DB-verify calls (removed the
screen-local `Service Should/Should Not Exist In DB` wrapper keywords). No shared T1/T2 file changes -
`Apply Navigator From Properties` already existed from the Area conversion (PRs #521-523). Real PR
body cited: live 5/5 pass (after clearing one residual `AUTOTEST_SERVICE` row from an earlier
interrupted attempt, root-caused via a fresh oracledb query, not raw SQL), full-tree dryrun 850/850,
self-clean 0/0 before+after (fresh connection), grid-filter keyword firing 15 times in `output.xml`,
robocop parity with Area's own reference files (same DOC02-only categories, same count of 7).

## Dev story - 2026-08-27 documentation/evidence backfill (this file's own update)
Backfilled under `docs/lean-deliverable-backfill-workorder.md` (Batch 3) - owner decision 2026-08-27
retiring Section H's lean waiver for SOW/README/JOURNAL/evidence/CHECKLIST/KB map. No automation file
(`service_page.resource`, `service_iud.robot`, `testdata/service_*.properties`) was touched. Live
evidence-capture re-run (8 attempts total) found and disclosed a REAL, reproducible intermittent
flake - a navigator autocomplete panel occasionally intercepting the grid-filter click 30s later
(different TC each time: TC01/02/03/04, never the same TC twice) - the DB ground truth was correct on
every attempted operation regardless; best clean result was 4/5. See `JOURNAL.md` for the full attempt
log and `ec-ui-knowledge/screens/service.md`'s Quirks section for the disclosed characteristic.
