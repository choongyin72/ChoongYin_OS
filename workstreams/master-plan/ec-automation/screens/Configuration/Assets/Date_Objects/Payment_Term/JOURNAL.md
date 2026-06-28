# JOURNAL - feature/payment-term-iud (CD.0023 Payment Term)

## Built
- Full IUD automation for Payment Term (OV, date-effective): T3, RF suite (4 TCs clean->insert->update
  ->delete, in-suite DB asserts), Playwright flow, 2 recon scripts, evidence, SOW, README, CHECKLIST.
- 3rd of 5 Date Objects screens. Built to the 19-item IUD deliverable standard.

## Done well
- DB-first recon caught that Payment Term has extra columns (FIN_CODE, DAY_VALUE, CALCULATION_CODE)
  vs the term screens; live DOM recon then confirmed the **shifted field rows** (Method R7, number R8,
  optional Calculation dd R9). Remapped the clone's ids accordingly -- did NOT blind-clone R6/R7.
- Realistic test data: 'Fixed number of Days' + Day Value 30 ("30 days") matching existing rows.
- T3 thin (T2 `manage_object` + shared `Select EC Dropdown Option`); zero shared-file edits. Full I-U-D.

## Done wrong / corrected
- None at live-run time. The risk (wrong row indices from the exemplar) was pre-empted by recon.

## To improve
- 2 screens left are Calendar (CD.0024) + Calendar Collection (CD.0105) -- likely NOT the term/method
  shape; both may carry a child member grid. Recon each fully before cloning.

## Blockers -> resolution
- None.

## Decisions
- Kept the generic clone variable name `*_OFFSET` for the R:8 cell (semantics = DAY_VALUE; documented
  in SOW + a suite comment) rather than churn the shared-shape naming.
- **Stacked on CD.0108 (PR #142)** so the registry/scorecard appends layer cleanly.

## Evidence
- Live RF 4/4 PASS; Playwright ALL PASS (evidence/results.json).
- DB: TC02 `Code Should Be Present In View ov_payment_term`; TC04 `Code Should Be Absent In View`;
  independent re-read AUTOTEST_PT in OV_PAYMENT_TERM = 0 rows.
