# JOURNAL — Choke Model IUD

_Screen: Configuration > Assets > Stream Objects > Choke Model (CO.0217, OV). View `OV_CHOKE_MODEL`._
_Branch: feature/choke-model-iud (off master). 2026-07-26._

## Built
- Playwright: `py/choke_model_iud.py` (thin driver on shared engine + DbVerify) — zero engine changes.
- RF: T3 `.../Stream_Objects/choke_model_page.resource` + suite `.../choke_model_iud.robot` (reuse T2 `manage_object` + DbVerify).
- KB map `ec-ui-knowledge/screens/choke_model.md`.

## Done well
- 4th OV-reuse-target; verify_screen.py gate → OVERALL PASS (ticks auto-generated from real runs).
- Full I-U-D DB-verified vs `OV_CHOKE_MODEL`: Playwright 7/7, RF 4/4; update covers Name + Description.
- Recon-first caught **Start Date at R4** (not R2 — Sort Order + Description precede it); RF T3 uses R4. Also caught the folder differs from Choke (Stream Objects vs Well and Reservoir Objects) — verified per screen, not assumed sibling.
- All T3 keywords documented up-front → robocop 0.

## Problems / blockers
- None. Grid needs GO (handled). Many optional dropdowns present but none mandatory → plain engine sufficed.

## Decisions
- Update = Name + Description (both real columns). Optional dropdowns (Parent/Condition/etc.) left default.

## Evidence
- `VERIFY-REPORT.md` (OVERALL PASS) · `evidence/chkm_0[1-5]_*.png` (7/7) · `evidence/rf_report.html` (4/4). 2026-07-26.
