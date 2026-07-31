# JOURNAL - Well Bore (CO.0054) OV-GM + mandatory-popup IUD

## 2026-07-31
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

## Lessons
- Popup list-grid ids now number THREE variants (PopupList / manage_object_nav_nav / Objects) -
  always recon the popup frame; "empty source list" from the generic helper usually means wrong grid id.
- A scan's "first available" nav option can be a WRONG-TYPE object (graph vs well) that yields an
  empty grid - check what the option actually IS, not just that one exists.
