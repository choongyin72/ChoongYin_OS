-- =====================================================================================================
-- TEARDOWN via the OV_ object VIEWS (view-class-level delete) of the CLAUDE_WELL_TEST interface config.
-- Alternative to delete_CLAUDE_WELL_TEST_interface.sql (which deletes the base IMP_* tables directly).
--
-- WHY a DELETE and not "End Date = Start Date":
--   These classes (IMP_SOURCE_INTERFACE / _MAPPING / _PATH / IMP_TARGET_MAPPING) are TIME_SCOPE_CODE = INVARIANT
--   (NOT date-effective / NOT VERSIONED). The End-Date = Start-Date "logical delete" only works for VERSIONED
--   objects (e.g. Bank); for INVARIANT objects the OV view does NOT filter on END_DATE, so setting
--   end_date = start_date leaves the row fully visible. The correct view-level removal is a DELETE through the
--   OV view - its INSTEAD-OF-DELETE trigger performs the physical delete and cleans up the object registry.
--   (Verified on the sandbox 2026-06-21: OV-DELETE -> OV + base rows all 0; End=Start -> rows still present.)
--
-- Child-first (FK-safe): PATHS -> TARGET MAPPINGS -> SOURCE MAPPINGS -> INTERFACE. FK by business CODE.
-- Re-runnable (no-op if absent). One declare..begin..end; - NO COMMIT in the file (caller / Flyway commits).
-- =====================================================================================================
declare
  v_code constant varchar2(30) := 'CLAUDE_WELL_TEST';
begin

  -- 1) SOURCE MAPPING COMMANDS (paths)
  DELETE FROM OV_IMP_SOURCE_PATH    WHERE imp_source_interface_code = v_code;

  -- 2) TARGET MAPPINGS  (omit this block if only the 3 source-side views are wanted)
  DELETE FROM OV_IMP_TARGET_MAPPING WHERE imp_source_interface_code = v_code;

  -- 3) SOURCE MAPPINGS
  DELETE FROM OV_IMP_SOURCE_MAPPING WHERE imp_source_interface_code = v_code;

  -- 4) INTERFACE
  DELETE FROM OV_IMP_SOURCE_INTERFACE WHERE code = v_code;

end;
/
