# Issue_1052 — PHD Validation Gap Analysis
_Deep dive completed: 2026-06-02_
_Sources: WSPLU_EC_AsBuilt09_Validations_v1.0.xlsx, WSPLU_EC_AsBuilt05_Interfaces_v1.0.docx, Oracle DB_

---

## Summary
**671 total PHD tags updated since 1 Dec 2025. 163 tags (24%) have no validation coverage.**

## Gap Table

| Class | Attribute | Tags | In As-Built 05? | Validation As-Built 09? | DB Check Rules? | Risk |
|-------|-----------|------|----------------|------------------------|----------------|------|
| STRM_COMP_ANALYSIS | MOL_PCT + WT_PCT | 112 | Wrong class (spec says STRM_GAS_COMPONENT) | No — wrong class | ZERO | 🔴 HIGH |
| STRM_ANALYSIS | DENSITY + GCV | 15 | No — schedule was doing this | No | ZERO | 🔴 HIGH |
| TANK_DAY_DIP_STATUS | AVG_TEMP, GRS_VOL, MEAS_STD_DENSITY, ZWP_GRS_MASS | 14 | No | No | ZERO | 🟠 MEDIUM |
| PWEL_DAY_STATUS | AVG_GAS_RATE | 9 | No | No | ZERO | 🟠 MEDIUM |
| PWEL_DAY_STATUS | AVG_CHOKE_SIZE | 12 | Yes (interface spec only) | No | No specific | 🟡 LOW |
| STRM_DAY_STREAM_MEAS_WAT | ZWT_OILINWAT | 1 | EC Target blank | No | ZERO + NULL units | 🟡 LOW |

## Covered correctly (✅)
- PWEL_DAY_STATUS: AVG_BH_PRESS/TEMP/WH_PRESS/WH_TEMP/FLOW/GAS/WATER/COND_MASS, ON_STREAM_HRS (check rules 1016–1102)
- STRM_DAY_STREAM_MEAS_GAS: GRS_MASS, GRS_VOL, MEAS_ENERGY (check rules 1039–1058)
- STRM_DAY_STREAM_MEAS_OIL: GRS_MASS, GRS_VOL
- STRM_DAY_STREAM_MEAS_WAT: GRS_VOL_WAT (rule 1068)
- STRM_DAY_STREAM_MEAS_ELE: POWER_CONSUMPTION (rules 1057, 1073, 1074)
- EQPM_DAY_STATUS: ON_STREAM_HRS (rules 1118, 1119, 1137, 1138)

## Key Findings

### Finding 1 — STRM_COMP_ANALYSIS (112 tags) CRITICAL
As-Built 05 specifies gas composition → STRM_GAS_COMPONENT.COMP_MOL_PCT / COMP_WT_PCT.
DB has 112 tags mapped to STRM_COMP_ANALYSIS.MOL_PCT / WT_PCT — different class.
As-Built 09 V_DAILY_SAMPLING_VALIDATION covers STRM_GAS_COMPONENT check rules 1075–1086, NOT STRM_COMP_ANALYSIS.
Result: zero validation fires on gas composition import. Bad data silently corrupts GCV → allocation → reports.

### Finding 2 — STRM_ANALYSIS (15 tags) HIGH
As-Built 05 page 23 says: "GCV and Density calculated by ZWP_PostPHDImport as temporary solution until values included in PHD."
Now tags are added to import DENSITY + GCV directly from PHD — but As-Built never updated.
Risk: ZWP_PostPHDImport may still run = double-write conflict on same attribute.
No validation specified or configured.

### Finding 3 — TANK_DAY_DIP_STATUS (14 tags) MEDIUM
Condensate tank dip measurements. Not in As-Built 05 or 09.
No check rules. All FROM_UNIT = NULL (except ZWP_GRS_MASS).
Tank data feeds inventory → allocation calculations.

### Finding 4 — AVG_GAS_RATE (9 tags) MEDIUM
Completely undocumented — not in As-Built 05 or 09.
Unknown purpose. No validation.

### Finding 5 — AVG_CHOKE_SIZE (12 tags) LOW
In As-Built 05 as interface data element ("Choke Position" — NB: no "%", so a 0–100% range is NOT specified/implied).
Not in As-Built 09 = no validation spec. No specific check rule. (Any validation = TBD by Woodside/Grant.)

### Finding 6 — ZWT_OILINWAT (1 tag) LOW
EC Target BLANK in As-Built 05. Not in As-Built 09.
FROM_UNIT = NULL (description says mg/L). Zero check rules in DB.

## ECPRs Required
> ⚠️ 2026-06-11: ECPRs D/E/F (AVG_GAS_RATE, AVG_CHOKE_SIZE, ZWT_OILINWAT) carry **no validation spec in As-Built 05/09**. Any specific checks I drafted for them are inferences, not requirements — Woodside/Grant must define them first.

1. ECPR-NEW-A: Add check rules for STRM_COMP_ANALYSIS (MOL_PCT, WT_PCT)
2. ECPR-NEW-B: Investigate + fix STRM_ANALYSIS double-write + add validation
3. ECPR-NEW-C: Add check rules for TANK_DAY_DIP_STATUS + update As-Built
4. ECPR-NEW-D: Document AVG_GAS_RATE in As-Built 05 + add validation
5. ECPR-NEW-E: Add AVG_CHOKE_SIZE validation (range 0–100%)
6. ECPR-NEW-F: Fix ZWT_OILINWAT — FROM_UNIT, check rules, update As-Built 05

---
_Prepared by: Choong-Yin Lee | Verified via DB query (read-only)_
