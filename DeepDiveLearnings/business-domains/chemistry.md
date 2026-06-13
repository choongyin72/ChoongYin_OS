# EC Chemistry — domain dive 5 (2026-06-13, local sandbox) — DRAFT

Sources: menu walk (`ec_chemistry_branch.txt`, 27 nodes) · DB counts · DOC-04 §9.

## 1. Menu shape (small branch, two halves)
- **Chemicals**: Chemical Product Management · Chemical Inventory · Chemical Treatment
  — track chemical products (scale/corrosion inhibitors, methanol…), tank inventories,
  injection treatments at injection points.
- **Laboratory**: Configuration · Modelling · Sample Manager · Sample Analysis ·
  Daily Analysis And Measurements — lab sample lifecycle + analyses.

## 2. Sandbox data
CHEM_TANK_STATUS **39k** (+history 2.3k) · CHEM_INJ_POINT_STATUS 352 · CHEM_PRODUCT 105
— chemical tank statuses tracked daily (real seeded flow); injection points configured.
Lab side: PWEL_SAMPLE 25k + STRM_WATER_ANALYSIS 1.5k (counted under Production prefixes —
the lab data feeds Production quality).

## 3. Core flow
```
Chemical products defined → tanks hold inventory (CHEM_TANK_STATUS daily levels)
  └─ injection points consume product (CHEM_INJ_POINT_STATUS: rates/dosage vs target)
  └─ ChemCalc* CRON schedules (visible in Schedules grid!) recompute target/actual
     dosage + rates daily — the live calc engine for this domain
Lab: samples taken (Sample Manager) → analyses entered/imported (Sample Analysis)
  └─ component analyses (mole%/wt%) → feed Production allocation + quality validations
```

## 4. Ties to our work — STRONG
- **Issue_1052 lives here**: Stream/Well Gas Component Analysis screens = Laboratory
  "Sample Analysis"/"Daily Analysis And Measurements" area; our sum-checks (1156/1157)
  and frozen checks validate exactly this lab data.
- Chemical Objects (Assets section: 5 OV screens incl. 3 groupmodel) = master data here.
- ChemGen*/ChemCalc* schedules = ready-made examples of CRON-type schedules (vs our
  ONCE/manual ECIS ones) for scheduler learning.

## 5. Candidate business test cases
1. **Inventory balance**: tank level day N = day N-1 − injected + refills (oracle = pure
   arithmetic over CHEM_TANK_STATUS/_HISTORY).
2. **Dosage calc**: known injection target + production volume → run ChemCalc schedule →
   assert computed dosage.
3. **Sample lifecycle**: register sample → enter analysis → assert it lands in the same
   tables Issue_1052 checks validate (closing the loop with our validation work).

## 6. Open questions
- Pluto scope: chemicals module in As-Built? (offshore platforms inject inhibitors —
  plausible; confirm.)
