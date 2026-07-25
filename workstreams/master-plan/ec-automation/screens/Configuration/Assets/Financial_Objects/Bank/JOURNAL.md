# JOURNAL — Bank IUD

_Screen: Configuration > Assets > Financial Objects > Bank (OV, date-effective). View `ov_bank`._
_Bank is the golden OV exemplar. This JOURNAL was backfilled 2026-07-25 (bundle predated the JOURNAL rule)._

## Built (2026-07-25 re-visit)
- **Reusable OV engine** `py/ec_object_iud.py` (generic, label-resolved fields, `read_form_record`, grid-render-aware
  `select_row`, save-toggle fallback) + thin driver `py/bank_iud.py` — the template for all OV screens.
- **Single DB-verify** `libraries/DbVerify.py` (folded in `fetch_object`/`field_equals`/`verify_row`/`code_present`).
- **KB map** `ec-ui-knowledge/screens/bank.md` + pattern SOP `EC_OBJECT_CONFIG_IUD.md`.
- Legacy standalone `playwright/ec_iud_bank.py` retired to a pointer stub -> the generic driver.
- RF (pre-existing): `bank_page.resource` (T3) + `bank_iud.robot` suite.

## Done well
- Full I-U-D DB-verified vs `ov_bank` (insert NAME, update NAME + DESCRIPTION, delete End=Start absent); self-clean 0 residual.
- Playwright 7/7, RF 4/4, both live. One engine + one DB-verify shared by both stacks after consolidation.

## Done wrong / lessons
- **Selector assumptions:** carried CLP's `span.tv-link` (14.1.x) to 14.2.4 where it's `<label>` -> 0 hits; label
  resolver used exact `getElementById(...:C:0)` but the id has a suffix -> insert failed first run. Fix: prefix match + input-driven resolve.
- **3rd parallel copy:** first relocated my new engine ALONGSIDE the existing RF + legacy Playwright instead of
  consolidating — owner caught it. Fix: consolidated to one engine + one DbVerify; added the check-existing-first gate.
- **Shallow "Done":** initially reported done on green tests without KB map/JOURNAL. Fix: 21-item checklist + reuse clause.

## Blockers -> resolution
- Empty UI reads (x3) = async grid render / stale browser, NOT wrong selectors -> `wait_for_row()` before select (now in engine).
- No hard blockers; every issue self-resolved within the 2-strike cap; no data damage.

## Decisions
- Playwright + RF stay two engines (RF can't import the py engine); they SHARE `DbVerify.py` as the one ground-truth lib.
- Code lives in `ec-automation`; `ec-ui-knowledge/` is MD-only.

## Evidence
- Playwright: `tmp/bank_iud/evidence/bank_0[1-5]_*.png` (7/7, 2026-07-25).
- RF: `results/_demo/report.html` (4/4, 2026-07-25).
