# ECPR Drafts — PHD Validation Gaps (Issue_1052)
_Drafted: 2026-06-02 | Status: DRAFT — pending your review before raising in JIRA_

> ⚠️ **CORRECTION (2026-06-11): ECPR-D / ECPR-E / ECPR-F check-rule specifics are UNCONFIRMED INFERENCES, not requirements.**
> The validation details below for **AVG_GAS_RATE** (≥0 / %diff), **AVG_CHOKE_SIZE** (0–100%), and **ZWT_OILINWAT** (≥0) are **NOT specified in As-Built 09 or As-Built 05** — they were my own guesses by analogy. As-Built 05 calls AVG_CHOKE_SIZE simply "Choke Position" (no "%", so no 0–100 basis); AVG_GAS_RATE is undocumented; ZWT_OILINWAT is not mentioned in either As-Built. **Do NOT treat these as defined tasks.** Woodside/Grant must define *if* and *what* validation each needs before any build.

---

## ECPR-DRAFT-A: Add Check Rules for STRM_COMP_ANALYSIS Gas Composition Tags
**Priority:** High
**Reporter:** Choong-Yin Lee
**Related:** Issue_1052

**Summary:**
Add class validation and check rules for STRM_COMP_ANALYSIS (MOL_PCT, WT_PCT) to align with V_DAILY_SAMPLING_VALIDATION specified in As-Built 09.

**Description:**
As-Built 09 specifies V_DAILY_SAMPLING_VALIDATION for gas composition data, covering STRM_GAS_COMPONENT.COMP_WT_PCT (check rules 1075–1086). However, 112 PHD tags since Dec 2025 are mapped to STRM_COMP_ANALYSIS.MOL_PCT and WT_PCT — a different class. Zero check rules exist for STRM_COMP_ANALYSIS in the DB.

Impact: Bad gas composition data (out of range, frozen, sum ≠ 98–102%) will silently pass through. This feeds GCV calculations, heating value reports, and allocation — corrupting downstream outputs without any warning.

**Actions required:**
1. Add check rules for STRM_COMP_ANALYSIS.WT_PCT: min/max range (0–100), sum check (98–102%), mandatory, frozen value
2. Add check rules for STRM_COMP_ANALYSIS.MOL_PCT: same rules
3. Update As-Built 09 to reflect STRM_COMP_ANALYSIS (or clarify if STRM_GAS_COMPONENT is the intended target)
4. Confirm ZWP_PostPHDImport normalisation still fires after PHD import

---

## ECPR-DRAFT-B: Investigate STRM_ANALYSIS Double-Write and Add Validation
**Priority:** High
**Reporter:** Choong-Yin Lee
**Related:** Issue_1052

**Summary:**
Investigate potential double-write conflict between ZWP_PostPHDImport schedule and new PHD direct import for STRM_ANALYSIS.DENSITY and GCV. Add validation.

**Description:**
As-Built 05 (page 23) states: "GCV and Density calculated by ZWP_PostPHDImport as a temporary solution until those values are included in PHD."
15 PHD tags now directly import DENSITY and GCV into STRM_ANALYSIS. The ZWP_PostPHDImport schedule still appears to be active. Both may be writing to the same fields — risk of overwrite conflict. Additionally no validation (class or check rule) exists for these attributes.

**Actions required:**
1. Confirm if ZWP_PostPHDImport still calculates DENSITY/GCV or has been disabled
2. If both active: disable schedule calculation for streams now covered by PHD direct import
3. Add check rules for STRM_ANALYSIS.DENSITY (>= 0, frozen value, % diff)
4. Add check rules for STRM_ANALYSIS.GCV (>= 0, frozen value, % diff)
5. Update As-Built 05 to reflect direct PHD import replacing schedule

---

## ECPR-DRAFT-C: Add Check Rules for TANK_DAY_DIP_STATUS
**Priority:** Medium
**Reporter:** Choong-Yin Lee
**Related:** Issue_1052

**Summary:**
Add check rules and class validation for TANK_DAY_DIP_STATUS attributes (AVG_TEMP, GRS_VOL, MEAS_STD_DENSITY, ZWP_GRS_MASS) and update As-Built documents.

**Description:**
14 PHD tags mapped to TANK_DAY_DIP_STATUS since Dec 2025. This class (condensate tank dip measurements) is not in As-Built 05 or 09. Zero check rules exist in DB. All FROM_UNIT = NULL except ZWP_GRS_MASS.
Tank data feeds inventory and allocation calculations — unvalidated data risks incorrect tank volumes.

**Actions required:**
1. Add check rules: >= 0, frozen value, mandatory for GRS_VOL and ZWP_GRS_MASS
2. Add check rules for AVG_TEMP (range check) and MEAS_STD_DENSITY (>= 0)
3. Set FROM_UNIT for AVG_TEMP, GRS_VOL, MEAS_STD_DENSITY
4. Update As-Built 05 to document TANK_DAY_DIP_STATUS as a PHD interface target
5. Update As-Built 09 to include validation spec

---

## ECPR-DRAFT-D: Document and Validate AVG_GAS_RATE PHD Tags
**Priority:** Medium
**Reporter:** Choong-Yin Lee
**Related:** Issue_1052

**Summary:**
Document PWEL_DAY_STATUS.AVG_GAS_RATE in As-Built 05 and add appropriate check rules.

**Description:**
9 PHD tags mapped to PWEL_DAY_STATUS.AVG_GAS_RATE since Dec 2025. This attribute is not documented in As-Built 05 or 09. No validation exists. Purpose and unit of measure are unclear.

**Actions required:**
1. Confirm purpose and UOM with Woodside/engineering team
2. Update As-Built 05 to document AVG_GAS_RATE as PHD interface element
3. ⚠️ INFERENCE ONLY — (>= 0 / frozen / %diff) NOT specified in As-Built 05/09; attribute undocumented. Needs Woodside to define purpose + UOM + validation before any rule.
4. Update As-Built 09 with validation spec

---

## ECPR-DRAFT-E: Add Validation for AVG_CHOKE_SIZE PHD Tags
**Priority:** Low
**Reporter:** Choong-Yin Lee
**Related:** Issue_1052

**Summary:**
Add check rules for PWEL_DAY_STATUS.AVG_CHOKE_SIZE (12 tags). Attribute is specified in As-Built 05 but missing from As-Built 09 validation spec.

**Actions required:**
1. ⚠️ INFERENCE ONLY — As-Built 05 says "Choke Position" (no "%"); 0–100% is NOT specified anywhere. Woodside/Grant to define the actual validation (if any).
2. Update As-Built 09 to include validation specification

---

## ECPR-DRAFT-F: Fix ZWT_OILINWAT — Unit Conversion and Check Rules
**Priority:** Low
**Reporter:** Choong-Yin Lee
**Related:** Issue_1052

**Summary:**
Fix ZWT_OILINWAT (Oil in Water, WATER_OVERBOARD stream): set FROM_UNIT to mg/L, add check rules, update As-Built 05 with EC Target attribute name.

**Actions required:**
1. Set FROM_UNIT = 'mg/L' in V_TRANS_CONFIG for tag PRP.00AI02631XR24.DACA.PV  (FROM_UNIT confirmed still NULL; mg/L is from the tag description, needs Woodside confirmation)
2. ⚠️ INFERENCE ONLY — ZWT_OILINWAT is NOT mentioned in As-Built 05 or 09; the >= 0 check is my guess. Woodside/Grant to define the actual validation (if any).
3. Update As-Built 05 — EC Target column for "Measured Oil in Water" row is blank
4. Update As-Built 09 — add ZWT_OILINWAT to V_DAILY_PHD_VALIDATION section

---
_Review all drafts before raising. ECPRs D and F are lowest priority and may be deferred post go-live._
