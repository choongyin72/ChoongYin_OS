# JOURNAL - Trailer (CO.0265) plain-OV IUD

## 2026-07-31
- **Branch:** `feature/trailer-iud`. Group A #6, sibling of Truck (CO.0264).
- **Recon (executed):** empty navigator (zero nav fields, GO only), custom grid id
  `trailer_object:form:T_data`, mandatory = Code/Name/Start Date + Licence Plate No +
  Trailer Type/UOM/Transport Company dds. DB: OV_TRAILER = 0 rows (our row is the first).
- **First screen through the AUDITED plain-OV generator with zero debugging:** driver 8/8 and all 5
  verify gates PASS on the FIRST run. The 6 defects fixed during the Truck audit (GO re-query,
  UNSAVED CHANGES dialog, grid-id key, extra_texts, LEN03 split, leftover `assert pu`) all held here.
- **The new #278 vocabulary validator immediately proved its worth:** the registry row came out
  correct (the family-aware fix from PR #279 worked), but `check_row_vocab.py` FLAGGED the scorecard
  row - I had only made the REGISTRY template family-aware, not the SCORECARD one, so the scorecard
  still said "(OV-GM, CO.0265) ... OV-GM gated-navigator ... Op PU first-available" on a plain-OV
  screen. Fixed the second template too (family-aware tag + descriptor), removed the bad row,
  regenerated, re-validated: clean. Regression-checked all 5 families (ovgm/plain/custom/tv) - no
  breakage.

## Lessons
- The validator caught a defect the same class of check was created for, on its FIRST real use, in a
  place I had not thought to fix - evidence that type-correctness checks beat edit-landed checks.
- When fixing a templating defect, enumerate EVERY template that emits the same vocabulary (registry
  AND scorecard AND KB), not just the one the last bug surfaced in.
