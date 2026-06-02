# Issue_1052 — PHD Tag Validation Status — Comprehensive Table
_Generated: 2026-06-02 | Source: Oracle DB (ECKERNEL_EC) | Read-only_
_Scope: All active PHD tags with LAST_TRANSFER >= 1 Dec 2025_

---

## Overall Summary

| Category | Tags | % of Total |
|----------|------|-----------|
| ✅ Both Class Validation AND Check Rule | 81 | 12% |
| 🟡 Check Rule ONLY (no Class Validation) | 449 | 68% |
| 🔵 Class Validation ONLY (no Check Rule) | 0 | 0% |
| 🔴 NEITHER Class Validation NOR Check Rule | 131 | 20% |
| **Total Active PHD Tags (since 1 Dec 2025)** | **661** | **100%** |

---

## Category 1 — Both Class Validation AND Check Rule (81 tags)
> Tags fully covered: class validation configured AND at least one check rule active.

| EC Class | Attribute | Tag Count | From Unit | Check Rule IDs | Severity |
|----------|-----------|-----------|-----------|----------------|---------|
| PWEL_DAY_STATUS | AVG_BH_PRESS | 12 | MPA | 1016–1102 (mandatory, frozen, std dev, % diff) | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_BH_TEMP | 12 | NULL | 1016–1102 | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_COND_MASS | 12 | SM3/D | 1016–1102 (NODATA_COND, frozen) | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_FLOW_MASS | 12 | SM3/D | 1016–1102 (NODATA, frozen, std dev) | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_GAS_MASS | 21 | KG | 1016–1102 | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_WATER_MASS | 12 | SM3/D | 1016–1102 | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_WH_PRESS | 12 | KPA | 1016–1102 (NODATA_WHPRESS) | ERROR/WARNING |
| PWEL_DAY_STATUS | AVG_WH_TEMP | 12 | NULL | 1016–1102 | ERROR/WARNING |

**Class attributes validated:** ON_STREAM_HRS, AVG_FLOW_MASS, AVG_COND_MASS, AVG_GAS_MASS, AVG_WATER_MASS, AVG_BH_PRESS, AVG_BH_TEMP, AVG_WH_PRESS, AVG_WH_TEMP

---

## Category 2 — Check Rule ONLY, No Class Validation (449 tags)
> Check rules fire on the class but no class attribute validation row is configured.
> Partially protected — anomaly detection works but no min/max/mandatory class-level enforcement.

| EC Class | Attribute | Tags | From Unit | Check Rule IDs | Severity | Notes |
|----------|-----------|------|-----------|----------------|---------|-------|
| PWEL_DAY_STATUS | ON_STREAM_HRS | 12 | NULL | CR 1016 (on strm hrs), 1031 (0–24 check), MISSING_DATA | ERROR | OK |
| PWEL_DAY_STATUS | AVG_CHOKE_SIZE | 12 | NULL | Generic PWEL rules only — no choke-specific range check | ERROR/WARNING | Gap: no 0–100% rule |
| PWEL_DAY_STATUS | AVG_GAS_RATE | 9 | NULL | Generic PWEL rules only | ERROR/WARNING | Not in As-Built 05/09 |
| STRM_DAY_STREAM_MEAS_GAS | GRS_MASS_GAS | 135 | KG/NULL | CR 1039–1058 (mandatory, frozen, variance, std dev) | ERROR/WARNING | OK |
| STRM_DAY_STREAM_MEAS_GAS | GRS_VOL_GAS | 112 | SM3/NULL | CR 1039–1058 | ERROR/WARNING | OK |
| STRM_DAY_STREAM_MEAS_GAS | MEAS_ENERGY | 80 | GJ/NULL | CR 1039–1058 | ERROR/WARNING | OK |
| STRM_DAY_STREAM_MEAS_ELE | POWER_CONSUMPTION | 36 | KWH/NULL | CR 1057, 1073, 1074 (mandatory, ELE checks) | ERROR | OK |
| STRM_DAY_STREAM_MEAS_OIL | GRS_MASS_OIL | 15 | KG | CR 1051–1058 (mandatory, frozen, variance) | ERROR/WARNING | OK |
| STRM_DAY_STREAM_MEAS_OIL | GRS_VOL_OIL | 9 | SM3/NULL | CR 1051–1058 | ERROR/WARNING | OK |
| STRM_DAY_STREAM_MEAS_WAT | GRS_VOL_WAT | 2 | NULL/SM3 | CR 1048 (mandatory), 1049 (frozen), 1068 (missing data) | ERROR/WARNING | OK |
| EQPM_DAY_STATUS | ON_STREAM_HRS | 2 | NULL | CR 1118/1119 (ARGU/RTO 0–24), 1137/1138 (mandatory) | ERROR | OK |

---

## Category 3 — Class Validation ONLY (0 tags)
> **None.** No tags have class validation without a check rule.

---

## Category 4 — NEITHER Class Validation NOR Check Rule (131 tags)
> **Highest risk. No validation of any kind. Bad data passes through silently.**

### 4A. STRM_COMP_ANALYSIS — MOL_PCT (78 tags) — CRITICAL
_Gas composition mol % — feeds GCV calculations and allocation_

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.10QY001_2B/2C/2D/2E/2F/2G/2H/2L/2N/2T.PV (10) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.114QI201–207_FWA.DACA.PV (7 — stream 1C1401_TO_E1405AB) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.44QI101–106_FWA + copies (12) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.44QI110_FWA + copy (2) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.44QI201–206_FWA + copies (24) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.44QI210_FWA + copies (4) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.44QI210C/D/E/F/G/H/I/J/K/M.PV (10) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PGP.TOT_HP_CH4_ATM_FWA_YDAY.DACA.PV (1) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | MOL_PCT | PAS.PGP_ZERO_TAG-COPY-14 to COPY-21 (8) | NULL | NO | NO |

**Validation required:** Range 0–100% (ERROR), Sum of components 98–102% (ERROR), Mandatory (ERROR), Frozen value (WARNING)

---

### 4B. STRM_COMP_ANALYSIS — WT_PCT (24 tags) — CRITICAL
_Gas composition weight % — feeds GCV and heating value calculations_

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| STRM_COMP_ANALYSIS | WT_PCT | PGP.114QI201W–207W_FWA.DACA.PV (7) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | WT_PCT | PGP.44QI201W–206W_FWA.DACA.PV (6) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | WT_PCT | PGP.44QI210W_FWA.DACA.PV (1) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | WT_PCT | PGP.56QQ211A–217A, 222A, 223A.PV (9) | NULL | NO | NO |
| STRM_COMP_ANALYSIS | WT_PCT | PAS.PGP_VT_56QQ218A_C6+ (1) | NULL | NO | NO |

**Validation required:** Range 0–100% (ERROR), Sum 98–102% (ERROR), Mandatory (ERROR), Frozen value (WARNING)

---

### 4C. STRM_ANALYSIS — DENSITY (6 tags) — HIGH
_Stream density — As-Built 05 says calculated by ZWP_PostPHDImport schedule (double-write risk)_

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| STRM_ANALYSIS | DENSITY | PGP.114FT058_FWA.PREV_DAY_SDENS.PV | NULL | NO | NO |
| STRM_ANALYSIS | DENSITY | PGP.114FT059_FWA.PREV_DAY_SDENS.PV | NULL | NO | NO |
| STRM_ANALYSIS | DENSITY | PGP.401FE001_FWA.PREV_DAY_SDENS.PV | NULL | NO | NO |
| STRM_ANALYSIS | DENSITY | PGP.402FE001_FWA.PREV_DAY_SDENS.PV | NULL | NO | NO |
| STRM_ANALYSIS | DENSITY | PGP.403FE001_FWA.PREV_DAY_SDENS.PV | NULL | NO | NO |
| STRM_ANALYSIS | DENSITY | PGP.404FE001_FWA.PREV_DAY_SDENS.PV | NULL | NO | NO |

**Validation required:** >= 0 (ERROR), Frozen value (WARNING). Investigate ZWP_PostPHDImport conflict.

---

### 4D. STRM_ANALYSIS — GCV (9 tags) — HIGH
_Gross Calorific Value — was calculated by schedule, now also from PHD_

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| STRM_ANALYSIS | GCV | PGP.114FT058_FWA.PREV_DAY_CV.PV | NULL | NO | NO |
| STRM_ANALYSIS | GCV | PGP.114FT059_FWA.PREV_DAY_CV.PV | NULL | NO | NO |
| STRM_ANALYSIS | GCV | PGP.401FE001_FWA.PREV_DAY_CV.PV | NULL | NO | NO |
| STRM_ANALYSIS | GCV | PGP.402FE001_FWA.PREV_DAY_CV.PV | NULL | NO | NO |
| STRM_ANALYSIS | GCV | PGP.403FE001_FWA.PREV_DAY_CV.PV | NULL | NO | NO |
| STRM_ANALYSIS | GCV | PGP.404FE001_FWA.PREV_DAY_CV.PV | NULL | NO | NO |
| STRM_ANALYSIS | GCV | PGP.44QI210A.PV | MJPERSM3 | NO | NO |
| STRM_ANALYSIS | GCV | PGP.44QI210A.PV-COPY-1 | MJPERSM3 | NO | NO |
| STRM_ANALYSIS | GCV | PGP.44QI210A.PV-COPY-2 | MJPERSM3 | NO | NO |

**Validation required:** >= 0 (ERROR), Frozen value (WARNING). Investigate ZWP_PostPHDImport conflict.

---

### 4E. TANK_DAY_DIP_STATUS — AVG_TEMP (5 tags) — MEDIUM
_Condensate tank temperature — not in As-Built_

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| TANK_DAY_DIP_STATUS | AVG_TEMP | PGP.34LDI005_5.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | AVG_TEMP | PGP.34LDI006_19.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | AVG_TEMP | PGP.T3301_TEMP.TEMP.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | AVG_TEMP | PGP.T3302_TEMP.TEMP.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | AVG_TEMP | PGP.T3303_TEMP.TEMP.PV | NULL | NO | NO |

---

### 4F. TANK_DAY_DIP_STATUS — GRS_VOL (5 tags) — MEDIUM
_Condensate tank gross volume — feeds inventory and allocation_

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| TANK_DAY_DIP_STATUS | GRS_VOL | PGP.T3101_TOTS.VOLUME.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | GRS_VOL | PGP.T3102_TOTS.VOLUME.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | GRS_VOL | PGP.T3301_TOTS.VOLUME.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | GRS_VOL | PGP.T3302_TOTS.VOLUME.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | GRS_VOL | PGP.T3303_TOTS.VOLUME.PV | NULL | NO | NO |

---

### 4G. TANK_DAY_DIP_STATUS — MEAS_STD_DENSITY (2 tags) — MEDIUM

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| TANK_DAY_DIP_STATUS | MEAS_STD_DENSITY | PGP.34LDI005_6.PV | NULL | NO | NO |
| TANK_DAY_DIP_STATUS | MEAS_STD_DENSITY | PGP.34LDI006_18.PV | NULL | NO | NO |

---

### 4H. TANK_DAY_DIP_STATUS — ZWP_GRS_MASS (2 tags) — MEDIUM

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR |
|----------|----------------|---------|-----------|----|----|
| TANK_DAY_DIP_STATUS | ZWP_GRS_MASS | PGP.T3101_TOTS.MASS.PV | TONNES | NO | NO |
| TANK_DAY_DIP_STATUS | ZWP_GRS_MASS | PGP.T3102_TOTS.MASS.PV | TONNES | NO | NO |

---

### 4I. STRM_DAY_STREAM_MEAS_WAT — ZWT_OILINWAT (1 tag) — LOW

| EC Class | Class Attribute | PHD Tag | From Unit | CV | CR | Notes |
|----------|----------------|---------|-----------|----|----|-------|
| STRM_DAY_STREAM_MEAS_WAT | ZWT_OILINWAT | PRP.00AI02631XR24.DACA.PV | NULL | NO | NO | EC Target blank in As-Built 05. Unit = mg/L |

---

## Prioritised Action Plan

| # | Priority | EC Class | Attribute | Tags | Validation to Add | ECPR |
|---|----------|----------|-----------|------|-------------------|------|
| 1 | CRITICAL | STRM_COMP_ANALYSIS | MOL_PCT | 78 | Range 0–100%, sum 98–102%, mandatory, frozen | Draft-A |
| 2 | CRITICAL | STRM_COMP_ANALYSIS | WT_PCT | 24 | Range 0–100%, sum 98–102%, mandatory, frozen | Draft-A |
| 3 | HIGH | STRM_ANALYSIS | GCV | 9 | >= 0, frozen + investigate ZWP_PostPHDImport conflict | Draft-B |
| 4 | HIGH | STRM_ANALYSIS | DENSITY | 6 | >= 0, frozen + investigate ZWP_PostPHDImport conflict | Draft-B |
| 5 | MEDIUM | TANK_DAY_DIP_STATUS | GRS_VOL | 5 | >= 0, mandatory, frozen | Draft-C |
| 6 | MEDIUM | TANK_DAY_DIP_STATUS | ZWP_GRS_MASS | 2 | >= 0, mandatory | Draft-C |
| 7 | MEDIUM | TANK_DAY_DIP_STATUS | AVG_TEMP | 5 | Range check, frozen | Draft-C |
| 8 | MEDIUM | TANK_DAY_DIP_STATUS | MEAS_STD_DENSITY | 2 | >= 0 | Draft-C |
| 9 | LOW | PWEL_DAY_STATUS | AVG_CHOKE_SIZE | 12 | Range 0–100% | Draft-E |
| 10 | LOW | PWEL_DAY_STATUS | AVG_GAS_RATE | 9 | Document in As-Built, confirm UOM, add rules | Draft-D |
| 11 | LOW | STRM_DAY_STREAM_MEAS_WAT | ZWT_OILINWAT | 1 | FROM_UNIT=mg/L, >= 0, frozen | Draft-F |

---
_Verified via read-only DB query on 2026-06-02_
_Total: 661 active PHD tags since 1 Dec 2025 | 131 (20%) with no validation_
