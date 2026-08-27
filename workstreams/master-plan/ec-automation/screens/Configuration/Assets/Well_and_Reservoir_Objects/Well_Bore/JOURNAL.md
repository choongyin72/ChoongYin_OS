# JOURNAL — Well Bore (CO.0054) OV-GM + mandatory-popup IUD

_Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well Bore. View `OV_WELL_BORE`._

## 2026-07-31 (original build)
- **Branch:** `feature/well-bore-iud`. Group A #2 (well-hierarchy set).
- **Recon facts (all executed, nothing assumed):**
  - nav = PER-FIELD groups `nav:form:G:1..G:4:R:1:C:0` = PU / Area / Facility Class 1 /
    'Well & Well Hookup'; a 5th group G:5 ('Well') is scan-flagged mandatory but returned **ZERO
    options under every scope tried** (AS1 first-available AND P1 with a real well) -> unusable
    filter, skipped. Grid loads on 4 levels - verified by listing the real bore `P1 W008 WB001`.
  - G:4 needs a **REAL well**: the first-available option is `P1 Graph 001` (a graph object, no
    bores -> grid showed 'No records found'). Used `P1 W008 OP`.
  - DB: OV_WELL_BORE = 158 rows (bores named per well, e.g. P1 W008 WB001); base WEBO_BORE.
- **Mandatory 'Well' POPUP (pin R:7):** first driver run failed with the generic engine's
  "empty source list" error. Popup recon showed the list grid is **`Objects:form:T_data`** (a THIRD
  popup-grid variant after PopupList and manage_object_nav_nav) - already populated on open, 40 rows.
  Screen-local picker selects the **nav-scope well by value** (the popup's first row is the graph
  object - deliberately not picked).
- One robocop FAIL (LEN08 line 302/300 chars in the popup JS) -> shortened, re-ran; live 4/4 both runs.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 8/8. Self-clean 0 residual.

## Built (2026-08-27 — PR #564, Area-pattern conversion)
- Converted the RF suite from the old 4-TC/suite-login/generated-code/inline-DB-verify build to
  the full Area-pattern structure: 5 TCs (added TC04 Find), per-TC `Login To EC Application`/
  `Logout From EC Application` on one browser opened once in Suite Setup, fixed test code
  `AUTOTEST_WB` (was a timestamped code), properties-file-driven insert/update/verify via 4 new
  `testdata/well_bore_*.properties` files, explicit grid-filter wiring (`Find/Clear Well Bore Row
  By Filter`), zero inline DB-verify calls in the suite itself (DB check now lives only inside the
  shared T2 `Verify Object Removed`).
- New dedicated credential pair `WELL_BORE_EC_USER`/`WELL_BORE_EC_PASS` (additive-only addition to
  `resources/credentials.py`).
- **Bespoke screen-local T3 navigator keyword** `Apply Well Bore Navigator From Properties` added
  to `well_bore_page.resource` — Well Bore was the **first screen in the Area-pattern conversion
  program whose navigator did not fit the shared T2 `Apply Navigator From Properties` keyword's
  supported same-row/increasing-column shape**. Confirmed by BOTH a live read-only DOM recon
  (G:1..G:5 each report their own `dd_input` — genuinely PER-FIELD groups, not a cascade) AND by
  re-reading the pre-existing proven driver `py/well_bore_iud.py` before writing any new code —
  both sources agreed the navigator is per-field. The bespoke keyword was modeled on
  `well_page.resource`'s own prior "Apply Well Navigator" precedent and built in parallel with,
  then reconciled against, Well Bore Interval's own bespoke navigator keyword (PR #563, same
  batch) — the two screens share the identical real shape and needed the identical kind of fix.
  It reads the navigator properties file in file order and fills `nav:form:G:<n>:R:1:C:0` for
  n = 1..4 via the existing shared T1 `Set Navigator Filter`/`Apply Navigator` primitives
  (`resources/navigator.resource`), clicking GO exactly once. `resources/manage_object.resource`
  itself was NOT touched by this conversion.
- The mandatory 'Well' POPUP is handled by a screen-local `Insert Well Bore Record And Save`
  keyword (mirrors Chemical Stream's own "From Connection" popup exception), reusing the
  pre-existing proven `Pick Well Popup` picker UNCHANGED — it picks the same value as the
  navigator's G:4 fill (`P1 W008 OP`, field-reuse rule).

## Done well
- Live 5/5 PASS (2026-08-27); full-tree `robot --dryrun tests/` 881/881 PASS; robocop parity with
  Area's own baseline (7 issues both, same VAR02/DOC02 shape); DB self-clean confirmed via a fresh
  connection — `SELECT COUNT(*) FROM OV_WELL_BORE WHERE CODE LIKE 'AUTOTEST%'` -> 0.
- 14 filter-keyword hits confirmed in the live `output.xml` at the time of PR #564 (re-confirmed
  as 19 hits on this backfill's own separate live run below — the count differs because the two
  runs are independent executions, not a discrepancy in the mechanism).
- Fixed code `AUTOTEST_WB` confirmed FREE in `OV_WELL_BORE` before use via a fresh independent
  `oracledb` connection.

## Done wrong / lessons
- Popup list-grid ids now number THREE variants across the well hierarchy (PopupList /
  manage_object_nav_nav / Objects) — always recon the popup frame; "empty source list" from the
  generic helper usually means wrong grid id, not a genuinely empty list.
- A scan's "first available" nav option can be a WRONG-TYPE object (graph vs well) that yields an
  empty grid — check what the option actually IS, not just that one exists.

## Blockers -> resolution
- **Original build (2026-07-31):** one robocop FAIL (LEN08, line 302/300 chars in the popup JS) —
  shortened the line, re-ran; live 4/4 both runs. No hard blockers; self-resolved within the
  2-strike cap.
- **PR #564 conversion (2026-08-27) — genuine mid-task collision, disclosed honestly:** during the
  same session's multi-PR push (Well, Well Bore Interval, Well Bore all converted together), a
  second/duplicate agent dispatch independently worked the same registry-row updates in the same
  worktree concurrently. This produced a transient duplicate "keep-both" row for both Well Bore
  and Well Bore Interval in `docs/ec_screen_registry.md` once the PRs merged. Resolution: the two
  independently-built bespoke navigator keywords were compared line-by-line and found to MATCH
  (same approach, same proven values) — no corruption resulted, so no automation rework was
  needed. The duplicate registry rows themselves were caught and removed the same day in commit
  `c35b909b` ("fix(batch-merge): drop 2 stale keep-both registry rows (Well Bore, Well Bore
  Interval)"). Root cause disclosed in that commit message: the hygiene hard-gate only confirmed
  registry rows existed (R38), it did not police duplicate rows — the by-key dedup check that
  would have caught this was informational only, not a hard gate, and ran AFTER the 3-PR push had
  already gone out. Fix applied then: the by-key check now joins hygiene in the hard-gate chain
  before any push (third occurrence of this gate-ordering class, per that commit's own message).

## Decisions
- Bespoke, screen-local T3 navigator keyword instead of extending the shared T2 keyword or forking
  `resources/manage_object.resource` — keeps the one genuinely different navigator shape isolated
  to the one screen (plus Well Bore Interval's identical case) rather than adding a conditional
  branch to shared code every other Area-pattern screen also depends on.
- Playwright + RF stay two engines; the Playwright driver (`py/well_bore_iud.py`) and its
  `investigation/` recon scripts are UNCHANGED by both the 2026-08-27 conversion and this
  2026-08-28 documentation backfill — per the owner's 2026-08-27 decision, the Universal Screen
  Engine is the go-forward replacement for hand-written Playwright drivers, so no new Playwright
  work was done or is expected here.
- Code lives in `ec-automation`; `ec-ui-knowledge/` is MD-only.

## Evidence
- Original build (2026-07-31): Playwright `evidence/wb_0[1-5]_*.png` + `wb_insert_ui_FAIL.png` +
  `results.json` (8/8 Playwright, 4/4 RF at that time).
- PR #564 conversion (2026-08-27): live RF 5/5, full-tree dryrun 881/881, DB self-clean — cited in
  the registry row and PR #564's body; no new evidence files were captured in-bundle at that time
  (lean-waiver era).
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — `log.html`/`output.xml`/
  `report.html` from a fresh live headless run (5/5 PASS, first attempt), `robocop_output.txt`
  (7 issues, parity with Area), and `summary.md` (DB self-clean + filter-hit-count re-verification).
