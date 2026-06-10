-- =============================================================================
-- Issue_1052: ROLLBACK — remove the TEST-ONLY fake MOL% data patch
-- Author : Choong-Yin Lee  |  Date: 2026-06-10
-- Purpose: restore WELL SCA_01 (ANALYSIS_NO = 2592) COMP_MOL_PCT to its ORIGINAL value
--          (NULL — verified 2026-06-10), undoing Issue1052_PHD_Sum_MolPct_FakeData_Patch.sql.
-- Safe   : Re-runnable. Scoped strictly to ANALYSIS_NO = 2592.
-- Order  : run this immediately after the fake-data test. Same OPEN-period requirement.
-- =============================================================================

BEGIN
    UPDATE TV_WELL_GAS_COMPONENT
       SET COMP_MOL_PCT = NULL               -- restore original (no MOL% data)
     WHERE ANALYSIS_NO = 2592;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- =============================================================================
-- VERIFY: expect SUM_MOL_PCT = 0 and NON_NULL = 0 (all COMP_MOL_PCT back to NULL).
-- =============================================================================
SELECT ANALYSIS_NO,
       COUNT(*)                              AS COMPONENTS,
       COUNT(COMP_MOL_PCT)                   AS NON_NULL_MOL_PCT,
       ROUND(SUM(NVL(COMP_MOL_PCT,0)),2)     AS SUM_MOL_PCT
  FROM TV_WELL_GAS_COMPONENT
 WHERE ANALYSIS_NO = 2592
 GROUP BY ANALYSIS_NO;
-- Expected: NON_NULL_MOL_PCT = 0, SUM_MOL_PCT = 0
