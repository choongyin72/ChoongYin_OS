# SOW - Chemical Stream Hookup IUD (Configuration > Assets > Chemical_Objects)
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-08-01 (original build); updated 2026-08-27 (backfill after PR #544 Area-pattern conversion)
**Version:** 2.0 — RF suite converted to the Area-pattern 5-TC structure via PR #544 (2026-08-26); original Playwright reference kept unchanged; live + DB-verified.

## 1. Original build (2026-08-01)
- **Screen:** Chemical Stream Hookup   **BF:** CO.0260   **View:** `OV_CHEM_STRM_HOOKUP`   **Base:** `CHEM_STRM_HOOKUP`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CSH_<timestamp>`; self-clean = absent in OV_CHEM_STRM_HOOKUP.
- Deliverables: driver `py/chemical_stream_hookup_iud.py`, T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_page.resource`,
  suite `tests/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).

## 2. Area-pattern conversion (PR #544, merged 2026-08-26)

### 2.1 Updated classification
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Chemical_Objects > Chemical Stream Hookup (CO.0260) |
| Screen type | OV-GM (manage-object, groupmodel), navigator-GATED, date-effective — unchanged classification, structural RF conversion only |
| List/grid id | `manageObject:form:T_data` |
| DB view (ground truth) | `OV_CHEM_STRM_HOOKUP` |
| Delete semantics | End Date = Start Date (true delete) |
| Navigator (mandatory 3-level same-row cascade before grid loads) | Production Unit -> Area -> Facility Class 1 + GO (`nav:form:G:0:R:1:C:1:dd` / `C:2:dd` / `C:3:dd`) |
| Navigator values (this environment, confirmed LIVE) | `AS1 EC Exploration Norway` / `AS1_Area` / `AS1_Facility_01` |
| Mandatory objectForm fields | Chemical Stream Hookup Code, Chemical Stream Hookup Name, Start Date |
| Mandatory-field pre-flight gate | `resources/mandatory_field_gate.resource` (`Assert No Empty Mandatory Field`) — kept exactly as-is, see §2.3 |
| Test data | Fixed code `AUTOTEST_CSH` (replacing the old timestamped `AUTOTEST_CSH_<timestamp>`), confirmed free in `OV_CHEM_STRM_HOOKUP` (count = 0) before the conversion run |

### 2.2 Dev story (pulled from PR #544's real body, not invented)
Converted Chemical Stream Hookup's existing RF automation from the OLD pattern (4 TCs, single
suite-level login, inline `Apply OV-GM Navigator First Available`, screen-local inline DB-verify
wrapper keywords) to Area's full pattern: 5 TCs (added TC04 Find), per-TC login/logout, fixed test
code `AUTOTEST_CSH`, properties-file-driven insert/update, explicit grid-filter wiring, and the
mandatory 3-level cascade navigator (Production Unit -> Area -> Facility Class 1) now delegates to
the shared T2 `Apply Navigator From Properties` keyword via a new
`chemical_stream_hookup_navigator.properties` whose 3 values were confirmed LIVE via a temporary
probe (not guessed, not copied from Well's own "P1 ..." scope). `resources/manage_object.resource`
itself was NOT modified. New test-data files:
`testdata/chemical_stream_hookup_{navigator,insert,update,form_verify,grid_verify}.properties`.
Verification at conversion time (PR #544 body): live run `EC_HEADLESS=true robot
.../chemical_stream_hookup_iud.robot` -> **5/5 PASS**; full-tree dryrun `robot --dryrun tests/` ->
**850/850 PASS**, zero collisions; `robocop check` on the 2 changed files -> 7 issues (VAR02 x2 +
DOC02 x5), exact parity with Area's own reference-pattern files; DB self-clean via a fresh
oracledb connection both before and after the run -> 0 rows for `AUTOTEST_CSH` / no residual
`AUTOTEST%` rows in `OV_CHEM_STRM_HOOKUP`.

### 2.3 Design decision preserved (owner instruction — do not question or change)
This screen has a standalone `mandatory_field_gate.resource` pre-flight check ("Assert No Empty
Mandatory Field before Save") that is kept exactly as-is per the task's explicit instruction. The
gate scans every visible input/select/textarea under a given `${scope_prefix}` for EC's own
mandatory-yellow background (`rgb(252, 249, 192)`) that is still empty, and FAILS the test BEFORE
the caller clicks Save/GO — naming every offending field — rather than relying only on reading
EC's post-Save error banner reactively. It is opt-in (a T3 suite imports
`resources/mandatory_field_gate.resource` explicitly) and additive-only: it does not modify
`common.resource` / `manage_object.resource` / any existing shared keyword, so every other
already-shipped screen is unaffected. Chemical Stream Hookup was the SECOND screen (after Action
Trigger) to adopt this mechanism at its original 2026-08-01 build, deliberately picked as the
CASCADE-HEAVY comparison case (PU -> Area -> Facility Class 1 + GO before the form is even open),
where a missed mandatory field costs a full cascade re-fill under a reactive-only (post-Save
banner) approach. The PR #544 conversion extracted the gate call into a new T3-local `Fill Object
Form Fields And Save With Gate` helper (to stay under the house keyword-length convention) that
inlines the gate call before Save inside Insert/Update — `mandatory_field_gate.resource` itself
was not touched by the conversion.

### 2.4 Live-probed navigator values (genuine investigative finding)
The 3 navigator values (`AS1 EC Exploration Norway` / `AS1_Area` / `AS1_Facility_01`) were
confirmed LIVE via a temporary probe (a throwaway `.robot` file, deleted after use, per PR #544's
body) that opened the navigator and read back each column's actual first-available resolved
label — not guessed, and not copied from Well's own "P1 ..." scope (a different screen's proven
value that does not apply here). These are exactly the labels the screen's PRIOR automation's
`Apply OV-GM Navigator First Available` mechanism resolved to on this sandbox; the conversion made
the same resolved values explicit and properties-file-driven instead of re-resolving them at
every run. Source: `testdata/chemical_stream_hookup_navigator.properties` (comment header) and
`docs/ec_screen_registry.md`'s Chemical Stream Hookup row (both cite PR #544 directly).

## 3. Deliverables (current, post-PR #544)
| Deliverable | Where |
|---|---|
| RF suite (maintained test, Area-pattern 5-TC) | `tests/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_iud.robot` |
| RF page object (Area-pattern) | `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_page.resource` |
| RF navigator/data files | `testdata/chemical_stream_hookup_{navigator,insert,update,form_verify,grid_verify}.properties` |
| Playwright reference (unmodified since 2026-08-01, NOT rebuilt by this backfill) | `py/chemical_stream_hookup_iud.py` |
| Recon trail (original build) | `investigation/recon.py` |
| Registry row | `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (modified in place by PR #544) |
| Conversion PR | [#544](https://github.com/choongyin72/ChoongYin_OS/pull/544) |
| Work journal | `JOURNAL.md` |
| KB selector map | `../../../../../../ec-ui-knowledge/screens/chemical_stream_hookup.md` |

This backfill (2026-08-27) does not rebuild or modify the RF automation, the Playwright driver, or
`mandatory_field_gate.resource` — it documents PR #544's already-merged conversion, updates this
SOW / `README.md` / `JOURNAL.md` / `CHECKLIST.md` / the KB map accordingly, and additionally
captured one fresh confirmation run of the existing, unmodified suite for evidence purposes
(dryrun 5/5, live headless 5/5, robocop parity, DB self-clean, hygiene — see
`evidence/2026-08-27-area-pattern-backfill/` and `JOURNAL.md`), per the evidence-capture allowance
in `docs/lean-deliverable-backfill-workorder.md` item 4.
