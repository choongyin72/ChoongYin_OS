# JOURNAL — Carrier IUD

_Screen: Configuration > Assets > Cargo Objects > Carrier (OV, date-effective, plain Bank family).
View `OV_CARRIER`. This JOURNAL was backfilled 2026-08-28 (PR #477's Bank-pattern conversion
predated the JOURNAL restoration — Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`, owner
decision 2026-08-27) per `docs/lean-deliverable-backfill-workorder.md` Batch 11. Content below is
pulled from PR #477's real body/commits, not invented._

## Built (PR #477, Batch 11, merged 2026-08-23)
- Rebuilt `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource` from the older
  hardcoded-field-id (`Fill New Object Form`) pattern to the label-driven, properties-file-driven,
  T2-consolidated Bank pattern, matching `bank_page.resource`/`berth_page.resource`/
  `port_page.resource` exactly.
- Rebuilt `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` with per-TC login/logout and
  a fixed test code `AUTOTEST_CARRIER` (replacing the old generated-unique
  `AUTOTEST_CARR_<timestamp>` code).
- New properties files: `testdata/carrier_{insert,update,form_verify,grid_verify}.properties`.
- Additive: `resources/credentials.py` gained `CARRIER_EC_USER`/`CARRIER_EC_PASS` (Carrier gets its
  own dedicated credential pair, standing decision owner 2026-08-22).
- Registry/scorecard rows MODIFIED (not appended) — this superseded the 2026-06-19 build's rows in
  `docs/automation-scorecard.md` and `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`.
- Batch-11 rows appended to `docs/grid-filter-standardization-checklist.md` and
  `docs/bank-pattern-conversion-checklist.md` under their pre-merged headers.

## Done well
- Live RF (`EC_HEADLESS=true`): **5/5 PASS** (TC01 clean-state, TC02 insert, TC03 update, TC04
  find, TC05 delete) — first try, no OV-GM lazy-redraw false-fail (plain OV, no gating).
- `robot --dryrun` on the full `tests/` tree: **772/772 pass** — the conversion did not regress
  any other screen's suite.
- Explicit grid-filter wiring confirmed live: `Find Carrier Row By Filter` fired **14x**
  (grep-counted on `output.xml`), `Clear Carrier Row Filter` fired **5x**.
- DB self-clean confirmed via an independent fresh `oracledb` connection re-read: 0 residual
  `AUTOTEST_CARRIER` rows in `OV_CARRIER`, checked AFTER the live run.
- No shared T1 (`common.resource`)/T2 (`manage_object.resource`) files were touched — the
  conversion reused the shared engine rather than forking it.
- Robocop parity check: Carrier's 9 issues (5x DOC02 missing-test-doc + 1x VAR02) matched the
  already-merged `port_iud.robot` baseline (also exit 1, 9 issues) exactly in kind and count — not
  a regression introduced by this conversion.

## Done wrong / lessons
- The original 2026-06-19 build's `AUTOTEST_CARR_<YYYYMMDDHHMMSS>` generated-unique test code was
  replaced with the fixed `AUTOTEST_CARRIER` to match Bank/Berth/Port's convention — this is a
  deliberate convention change, not a bug fix, but it means the two builds are NOT drop-in
  identical on test-code strategy; anyone re-running the pre-conversion Playwright bundle
  (`playwright/ec_iud_carrier.py`, left unchanged) will still see the old timestamped codes, while
  the RF suite now always uses `AUTOTEST_CARRIER`. Documented here so the two never get confused as
  interchangeable.
- The mandatory "Unit" reference dropdown is filled `__FIRST__` (throwaway value) but MUST stay
  excluded from `@{CARRIER_FORM_LABELS}` — including it would hit the known
  `__FIRST__`-fails-round-trip-verify gotcha (first documented on Batch 2's VAT Code screen). This
  is called out three times in the code/docs (page object Documentation, insert properties file
  comment, registry row) specifically so a future edit doesn't accidentally add it to the compare
  list.

## Blockers → resolution
- The Batch 11 task brief flagged Carrier's navigator as "unclear at survey time" (gated vs. not).
  Rather than re-running a fresh live DOM scan (which the owner's 2026-08-17 standing rule treats
  as a last resort, not a default), the conversion checked this repo's own prior evidence first:
  the original `carrier_sow.md` section 2 recon (one optional date + GO, no mandatory dropdown)
  and the already-proven Playwright driver's own field comments — both agreed the screen is NOT
  gated. That documented fact was trusted and used directly; no redundant live scan was performed.
  No blocker occurred in practice (the fact held up).

## Decisions
- Playwright bundle (`playwright/ec_iud_carrier.py`) and its `investigation/` recon scripts were
  left UNCHANGED by the conversion — per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`, new
  Playwright work is waived in favor of the Universal Screen Engine (`py/engine.py`); rebuilding a
  hand-written Playwright driver for an already-converted screen would be redundant work.
  Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.
- Kept the class/view/family classification from the original 2026-06-19 SOW (section 1) unchanged
  — the conversion is an RF-layer rebuild, not a re-classification.

## Evidence
- Original build (2026-06-19): `evidence/` (9 screenshots + `ec_iud_carrier_result.json`),
  Playwright ALL PASS.
- PR #477 conversion (2026-08-23): live RF 5/5 PASS cited in the PR body (not re-captured as
  screenshots at conversion time — RF suite does not have a screenshot-per-step flag beyond what
  `common.resource`'s `Capture Step` already produces into `results/carrier_live/`).
- This backfill (2026-08-28): `evidence/rf-live-2026-08-28/` — fresh live RF re-run, 5/5 PASS,
  `output.xml`/`log.html`/`report.html` + 24 step screenshots; independent DB self-clean re-read
  (0 residual `AUTOTEST_CARRIER` rows).
