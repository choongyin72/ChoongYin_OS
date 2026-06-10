-- =============================================================================
-- Issue_1052: TEST-ONLY fake MOL% data patch  (verifies well sum rule 1157)
-- Author : Choong-Yin Lee  |  Date: 2026-06-10
--
-- *** TEST DATA ONLY — NOT a production change. ALWAYS run the ROLLBACK after. ***
--
-- Why : real well analyses have NO COMP_MOL_PCT populated (all sum to 0), so the well
--       MOL% sum rule (DAILY_SAMPLING_WELL_GAS_COMPONENT_COMP_MOL_PCT_V1, CHECK_ID 1157)
--       cannot be positively exercised on real data. This injects a valid mole-% profile
--       into ONE well analysis so the rule can be proven to PASS (and, by scaling, to FIRE).
--
-- Target : WELL SCA_01, ANALYSIS_NO = 2592, DAYTIME 2026-06-01 (an OPEN period).
--          10 components; COMP_WT_PCT already sums to 100, COMP_MOL_PCT originally NULL
--          (verified 2026-06-10). Setting MOL% = WT% gives sum(MOL%) = 100 -> rule PASSES.
--
-- LIMITS : Works ONLY in an OPEN month. ECDP_MONTH_LOCK rejects locked periods
--          (e.g. 2025-12-01 raised ORA-20112). Pick an open-month analysis if 2592 closes.
--
-- To force a FIRE instead of PASS (out-of-range), change the SET expression to e.g.
--   SET COMP_MOL_PCT = COMP_WT_PCT * 0.90   (sum 90, below 0.98 -> FIRES)
--   SET COMP_MOL_PCT = COMP_WT_PCT * 1.10   (sum 110, above 1.02 -> FIRES)
-- =============================================================================

BEGIN
    UPDATE TV_WELL_GAS_COMPONENT
       SET COMP_MOL_PCT = COMP_WT_PCT        -- valid profile: sum(MOL%) = 100
     WHERE ANALYSIS_NO = 2592;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: expect SUM_MOL_PCT ~ 100 across the 10 components.
-- =============================================================================
SELECT ANALYSIS_NO,
       COUNT(*)                              AS COMPONENTS,
       ROUND(SUM(NVL(COMP_MOL_PCT,0)),2)     AS SUM_MOL_PCT
  FROM TV_WELL_GAS_COMPONENT
 WHERE ANALYSIS_NO = 2592
 GROUP BY ANALYSIS_NO;
-- Expected: SUM_MOL_PCT = 100  (-> isComponentSumOutOfTolerance returns 'NO' = PASS)
