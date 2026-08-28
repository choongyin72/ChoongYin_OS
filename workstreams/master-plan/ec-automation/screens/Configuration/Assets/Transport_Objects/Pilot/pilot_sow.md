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

---

## Addendum (2026-08-28) - Area-pattern structural conversion (PR #560, merged 2026-08-26) + backfill

_Backfilled under `docs/lean-deliverable-backfill-workorder.md` (owner decision 2026-08-27, Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`, Batch 5). The RF conversion below was already built and
merged in PR #560; this addendum documents it - no automation file was changed by this backfill._

Sections above describe the screen's original 2026-07-31 build (4 TCs, `apply_ovgm_navigator`
first-available mechanism, in-suite DB asserts). On 2026-08-26, Pilot's RF suite was converted to
the full Area-pattern STRUCTURE (PR #560), while remaining OV-GM - the genuine 3-level navigator
cascade was kept, not removed:

- 5 TCs (added **TC04 Find**, was 4), each with its own `Login To EC Application`/
  `Logout From EC Application` (Suite Setup still opens the browser once).
- Fixed test code **`AUTOTEST_PILOT`** (was a timestamp-suffixed `AUTOTEST_PL_<timestamp>`),
  confirmed FREE in `OV_PILOT` before being wired in (fresh oracledb connection).
- Navigator fill delegated to the shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`), driven by `testdata/pilot_navigator.properties`, replacing
  the pre-existing driver's own `apply_ovgm_navigator`-style inline fill.
- Live recon (2026-08-26) confirmed Pilot's navigator is a **single group, same-row 3-level
  cascade** (`nav:form:G:0:R:1:C:1/C:2/C:3` = Production Unit -> Area -> Facility Class 1, all
  MandatoryCellStyle) - the exact shape already proven on Well, FITS the Area pattern (not a
  per-field multi-group non-fit).
- Properties-file-driven Insert/Update/Verify (`testdata/pilot_{insert,update,form_verify,
  grid_verify}.properties`) via the shared T2 `Insert/Update/Verify Object *` keywords.
- Explicit `Find/Clear Pilot Row By Filter` grid-filter wiring wired into Update/Find/
  Verify-Found/Delete.
- Zero inline DB-verify calls remaining in the T3/suite - verification delegates purely to the
  shared T2 (`Verify Object Insert Exists/Form Record/Found/Removed/Does Not Exist`).

### Decision: `Op Production Unit = __FIRST__` kept as a documented EXCEPTION, not a fit violation

The insert form's **Op Production Unit** field was deliberately kept as `__FIRST__` rather than
forced to reuse the navigator's resolved Production Unit value (the general field-reuse rule
applied on other converted screens, e.g. Area's Op Production Unit = navigator PU). This is a
genuine, evidenced exception: the pre-existing `py/pilot_iud.py` driver's own code comment states
"the nav PU is not necessarily a valid Op PU option" - i.e. Op Production Unit's value domain is
INDEPENDENT of the navigator's Production Unit for this screen, proven by that driver's own
live 8/8 pass using `__FIRST__`. PR #560 kept this exception explicitly rather than blindly
applying the generic rule. This is recorded as a Decision, not a "done wrong" lesson - the
exception was correctly identified and applied, not stumbled into.

### Evidence cited in PR #560
- `AUTOTEST_PILOT` confirmed FREE in `OV_PILOT` before the build (fresh oracledb connection).
- Live headless run: **5/5 PASS** (TC01-TC05), run twice (shared tree + isolated worktree) - both 5/5.
- Fresh independent oracledb connection after the live run: 0 rows for `AUTOTEST%` in `OV_PILOT`
  (self-clean confirmed).
- `Find Object Row By Filter` fired 15x (`grep -c` on output.xml).
- Full-tree dryrun: 875/875 pass, zero collisions (isolated worktree).
- robocop parity: 7 issues (2 VAR02 + 5 DOC02), same kind/count as Area's own baseline - not a regression.
- Bundle hygiene (`py scripts/check_bundle_hygiene.py`): PASS.

### This backfill session (2026-08-28) - evidence re-capture, no automation touched
- `robot --dryrun tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` -> **5/5 PASS**.
- `EC_HEADLESS=true robot tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` -> **5/5
  PASS** on the first live run (no retry needed).
- `py -m robocop check pageobjects/.../pilot_page.resource tests/.../pilot_iud.robot` -> **7
  issues** (DOC02 missing test-case documentation) - matches PR #560's cited 7-issue baseline
  count exactly.
- `py scripts/check_bundle_hygiene.py` (repo-wide) -> PASS.
- `DbVerify.fetch_object("OV_PILOT", "AUTOTEST_PILOT")` (fresh oracledb connection, script at
  `Workplaces/pilot-backfill/db_selfclean_check.py`) -> `None` (confirmed absent) after the live run.
- `Find Pilot Row By Filter`/`Find Object Row By Filter` fired 29x in this session's output.xml
  (grep -c) - the grid-filter wiring is live and firing.
