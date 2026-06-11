# Issue_1052 — Advanced Checks: DRAFT + Review Note
_Prepared overnight 2026‑06‑09 for review after 9am 2026‑06‑10. **Nothing deployed, nothing committed.**_

## What's drafted
- **`Issue1052_PHD_Advanced_Checks_DRAFT.sql`** (local, uncommitted) — idempotent, mirrors the verified live templates:
  - **Frozen‑value (CONCRETE, runnable once approved):** clones live rule **1026** (`ZWP_P_TOOLTIP.getValFrozenValue`). Drafted for **STRM_ANALYSIS Density + GCV** → links to `V_PHD_STREAM_ANALYSIS`.
  - **Sum 98–102% (TEMPLATE only — placeholders, intentionally NOT executed):** clones live rule **1077** (`ZWP_P_VALIDATION.isComponentSumOutOfTolerance`). Class/column left as `<<PLACEHOLDER>>` pending the Grant decision below.

## Open decisions — what I traced vs what still needs Grant/As‑Built

### 1. Tolerance bounds — ✅ RESOLVED from the DB
- The sum functions read tolerance from `CTRL_SYSTEM_ATTRIBUTE` (`ZWP_STRM_SUM_COMP` / `ZWP_WELL_SUM_COMP`, `_LOWER`/`_UPPER`), **defaulting to 0.98 / 1.02**.
- **No override row exists** → **live tolerance = 98–102%** (the defaults). Configurable later if Woodside wants a different band.

### 2. Sum check — which class/column? ⚠️ NEEDS GRANT (Finding‑1)
- DB reality: composition is in **`STRM_COMP_ANALYSIS`** — per‑component rows (`ANALYSIS_NO`, `MOL_PCT`, `WT_PCT`, e.g. C1/C2/C3/CO2…), `DATA_CLASS_NAME='STRM_COMP_ANALYSIS'`.
- Existing sum rule (1077) runs on **event‑grain `RV_STRM_GAS_ANALYSIS`** + component table **`TV_STRM_GAS_COMPONENT`** (`COMP_WT_PCT`, `COMP_MOL_PCT`).
- **Decision:** which class/grain is correct for the Issue_1052 composition sum? (As‑Built 05 says STRM_GAS_COMPONENT; DB tags landed on STRM_COMP_ANALYSIS.) This drives `P_CLASS_NAME`, `P_COLUMN_NAME`, and the rule's `TABLE_ID`.

### 3. Which attributes get the checks? ⚠️ NEEDS GRANT + As‑Built 09
- **Frozen** currently exists for: `RV_PWEL_DAY_STATUS` (×8), `STRM_DAY_STREAM_MEAS_GAS` (×3), `MEAS_OIL` (×2), `MEAS_WAT` (×1), `STRM_SUB_DAY_STATUS_GAS` (×2). **None** on STRM_ANALYSIS / STRM_COMP_ANALYSIS / TANK_DAY_DIP_STATUS → my draft adds STRM_ANALYSIS Density/GCV (candidate; confirm).
- **Sum/tolerance** exists for sampling (1077/1083) + cargo (1124); **not** for STRM_COMP_ANALYSIS yet.
- Extra context found: rich per‑component limits already configured — `ZWP_STRM_COMP_<comp>_MIN/MAX/PCT` (C1, C2, C3, C6+, CO2, IC4, IC5, N2…, each MIN=0/MAX=100/PCT=2) and `ZWP_ANALYSIS_TOLERANCE=1`. So per‑component range checks may already be covered elsewhere — worth confirming we're not duplicating.

## Data sources
- **DB (COPS DEV)** — used for everything above (tolerance, class structure, existing‑rule patterns, function logic). ✅ done.
- **Still need: As‑Built 09 (Validations) + As‑Built 05 (Interfaces)** in client SharePoint (`PHBRQuorum`) — authoritative "which attributes / which class". + **Grant** for the final call.

## Verified mechanism (reference)
Function‑binding check rule = `TV_CTRL_CHECK_RULES` (WHERE_FORMULA tests the function var) + `TV_CTRL_CHECK_RULE_VARIABLE` (a `FUNCTION` var = package name + a `CONST_STRING`) + `TV_CTRL_CHECK_RULE_FUNC_P` (param→column mapping) + `CTRL_CHECK_COMBINATION` (group link). The frozen/sum logic already lives in `ZWP_P_TOOLTIP` / `ZWP_P_VALIDATION` (functions authored by leeeecho) — so this is **wiring, not new PL/SQL**.

## Status / next
- Draft SQL ready; **frozen part runnable** once you approve; **sum part needs the class decision** filled in.
- I did **not** deploy or commit anything. On your word (after Grant), I'll finalise + deploy to COPS DEV + verify + extend the RF test.
