# Issue_1052 — PHD Tag Validation Status Summary Table
_Generated: 2026-06-03 | Option B | Source: Oracle DB (read-only) + WSPLU_EC_AsBuilt09_Validations_v1.0.xlsx_

---

## Summary Table (4 Tags — One Per Category)

| Validation Status | EC Class | Attribute | Object Name | Object Code | Component | PHD Tag ID | From Unit | To Unit | Last Transfer | Check Rule ID | Class Validation Name |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Both Check Rule + Class Validation | PWEL_DAY_STATUS | ON_STREAM_HRS | PL-PYA 02 | PLA-02 | - | PRP.22KQI002075.TOTALIZER.PV | NULL | HRS | 26-MAY-2026 | 1016, 1031, 1059 | PWEL_DAY_STATUS.ON_STREAM_HRS |
| Check Rule Validation ONLY | STRM_DAY_STREAM_MEAS_GAS | GRS_MASS_GAS | HP Fuel Gas to 1KT1410 | FUEL_GAS_HP_TO_1KT1410 | - | PGP.114FT058_TOTS.PREV_DAY_MASS.PV | TONNES | KG | 26-MAY-2026 | 1039, 1042, 1058 | NONE |
| Class Validation ONLY (illustration) | PWEL_DAY_STATUS | ON_STREAM_HRS | PL-PYA 02 | PLA-02 | - | PRP.22KQI002075.TOTALIZER.PV | NULL | HRS | 26-MAY-2026 | NONE | PWEL_DAY_STATUS.ON_STREAM_HRS |
| Neither | STRM_COMP_ANALYSIS | MOL_PCT | 1C1401 to E1405A/B | 1C1401_TO_E1405AB | C1 | PGP.114QI201_FWA.DACA.PV | NULL | NULL | 26-MAY-2026 | NONE | NONE |

> **Note on Class Validation ONLY row:** No PHD tag in DB has class validation without a check rule (0 tags exist in this category). The row above uses the same tag as BOTH for illustration purposes — showing what the class validation configuration looks like in isolation.

---

## Class Validation Detail — PWEL_DAY_STATUS.ON_STREAM_HRS

| Field | Value | Description |
|-------|-------|-------------|
| Class | PWEL_DAY_STATUS | Daily Production Well Status |
| Attribute | ON_STREAM_HRS | On Stream Hours |
| ERR_MANDATORY_IND | Y | Field is mandatory — cannot be empty |
| ERR_MIN | 0 | Must be >= 0 hours |
| ERR_MAX | 24 | Must be <= 24 hours |
| WARN_MIN | NULL | No warning minimum set |
| WARN_MAX | NULL | No warning maximum set |
| Location in EC | Admin → Maintain Class → PWEL_DAY_STATUS → Attributes → ON_STREAM_HRS → Validation section |
| DB Table | TV_CLASS_ATTR_VALIDATION |

---

## Check Rule Detail

### BOTH + Class Validation Only tag (PWEL_DAY_STATUS.ON_STREAM_HRS)
| Check Rule ID | Check Rule Name | Severity | Description |
|---|---|---|---|
| 1016 | Fcty pwel on stream hrs | ERROR | On stream hours must be >= 0 |
| 1031 | PHD_PWEL_STATUS_SHUT_IN | ERROR | On stream hours must be 0 if well status is SHUT IN |
| 1059 | MISSING_DATA_PWEL_DAY_STATUS_VAL_ON_STRM_HRS | ERROR | All PHD input values are mandatory |

### Check Rule Only tag (STRM_DAY_STREAM_MEAS_GAS.GRS_MASS_GAS)
| Check Rule ID | Check Rule Name | Severity | Description |
|---|---|---|---|
| 1039 | PHD_STREAM_GAS_MEAS_VAL1 | ERROR | All measured values must be >= 0 |
| 1042 | PHD_STREAM_GAS_FROZEN_VALUE_V1 | WARNING | Stream has same Grs Mass as previous day (frozen value) |
| 1058 | MISSING_DATA_STRM_DAY_STREAM_MEAS_GAS_VAL_GRS_MASS | ERROR | All PHD input values are mandatory |

---

## What Class Validation Means in Issue_1052

Class Validation and Check Rule Validation are two **distinct** validation mechanisms in ECaaS:

| | Check Rule Validation | Class Validation |
|---|---|---|
| **Configured in** | TV_CTRL_CHECK_RULES | TV_CLASS_ATTR_VALIDATION |
| **Scope** | Whole class (all records of that class) | One specific attribute within a class |
| **When fires** | On-demand or scheduled validation run | On every screen save/entry |
| **What it catches** | Business rules (frozen, variance, sum, mandatory) | Data integrity (null, out of range, mandatory) |
| **Visible in** | Validation Overview screen (CO.0203) | Red underline on field in EC screen |
| **For PHD data** | Detects patterns over time | Rejects bad incoming values immediately |
| **Location in EC UI** | Admin → Maintain Check Rules | Admin → Maintain Class → Attributes → Validation |

### The Gap (131 NEITHER tags)
These tags have NO protection of either type:
- PHD imports bad/out-of-range data → not caught on screen (no class validation)
- Bad data accumulates → not detected by scheduled validation run (no check rules)
- Users see wrong values in reports and allocations with no warning

### Important Note — EC 14.1.5.1 Bug (ECPD-166168)
Woodside Pluto is on EC 14.1.5.1. This version has a known bug:
> When re-running validation (check rules) for a parent group, the child group logs are NOT updated.
> Fixed in EC 14.1.7 (December 2025).

**Impact:** The Validation Overview screen (CO.0203) may show stale/incorrect results for child group check rules. Verify check rule coverage via direct DB query rather than the UI screen.

---
_Source: Oracle DB TV_CLASS_ATTR_VALIDATION, TV_CTRL_CHECK_RULES | WSPLU_EC_AsBuilt09_Validations_v1.0.xlsx_
_EC Version: 14.1.5.1 | Generated: 2026-06-03_
