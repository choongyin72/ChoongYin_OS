-- =====================================================================================================
-- TEARDOWN: clear/remove the ECIS Excel-upload interface config CLAUDE_WELL_TEST.
-- Counterpart to create_CLAUDE_WELL_TEST_interface.sql.
--
-- * Deletes CHILD-FIRST (FK-safe): IMP_SOURCE_PATH -> IMP_TARGET_MAPPING -> IMP_SOURCE_MAPPING -> IMP_SOURCE_INTERFACE.
-- * Scoped to the CLAUDE_WELL_TEST interface BY LINKAGE (interface_id), so it removes ALL its mappings / paths /
--   targets regardless of how their OBJECT_CODE was set, and it handles duplicate interface rows (IN-subquery).
-- * PRODUCT interfaces are NOT touched (only rows linked to the CLAUDE_WELL_TEST interface, + the claudePress
--   target ec_key, are removed).
-- * One begin..end; block, NO COMMIT in the file (the caller / Flyway commits). Re-runnable (no-op if absent).
-- * Constant v_code in DECLARE.  This is the proven cleanup logic (used to clear the config 2026-06-21).
-- =====================================================================================================
declare
  v_code  constant varchar2(30) := 'CLAUDE_WELL_TEST';
begin

  -- 1) SOURCE MAPPING COMMANDS (paths) - children of the mappings
  DELETE FROM imp_source_path
   WHERE imp_source_mapping_id IN (
           SELECT object_id FROM imp_source_mapping
            WHERE imp_source_interface_id IN (SELECT object_id FROM imp_source_interface WHERE object_code = v_code));

  -- 2) TARGET MAPPINGS - children of the interface
  DELETE FROM imp_target_mapping
   WHERE imp_source_interface_id IN (SELECT object_id FROM imp_source_interface WHERE object_code = v_code)
      OR ec_key = 'claudePress';

  -- 3) SOURCE MAPPINGS - children of the interface
  DELETE FROM imp_source_mapping
   WHERE imp_source_interface_id IN (SELECT object_id FROM imp_source_interface WHERE object_code = v_code);

  -- 4) INTERFACE - the parent
  DELETE FROM imp_source_interface
   WHERE object_code = v_code;

end;
/
