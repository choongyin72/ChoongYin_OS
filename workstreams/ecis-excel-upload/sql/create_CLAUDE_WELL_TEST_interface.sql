-- =====================================================================================================
-- ECIS Excel-upload interface config: CLAUDE_WELL_TEST  (sandbox demo)
-- Mirrors the Woodside Pluto 050_Interfaces pattern (e.g. V1.0.35.0050.0020__ZWP_INTERIM_DATA_UPLOAD.sql).
--
-- * UPDATE-INSERT (idempotent / re-runnable): each object UPDATEs if present, else INSERTs. Never duplicates.
-- * REV_TEXT = 'ECPR-XXXX' on every INSERT/UPDATE  <-- REPLACE 'ECPR-XXXX' with the real change ticket.
-- * FK resolved by business key (no hardcoded GUIDs): ec_functional_area.object_id_by_uk('ECIS'); the
--   object_id / rec_id are left for EC to auto-generate on insert.
-- * DEPENDENCY ORDER (parent -> child, because of the FK chain + the object_id captured for children):
--     1. IMP_SOURCE_INTERFACE
--     2. (per column) IMP_SOURCE_MAPPING  -> then its IMP_SOURCE_PATH rows
--     3. IMP_TARGET_MAPPING
--   Maps Excel sheet 'Data' (Well | Date | Pressure) -> PWEL_DAY_STATUS.AVG_BH_PRESS keyed by well + date.
--
-- For COPSDEV delivery this becomes a versioned Flyway file under Pluto_Config/.../050_Interfaces/
-- (V<ver>.0050.<nnnn>__CLAUDE_WELL_TEST.sql); never hand-config COPSDEV.
-- =====================================================================================================
declare
  lv_interface_id  varchar2(32);
  lv_map_id        varchar2(32);
  v_rev   constant varchar2(30) := 'ECPR-XXXX';
  v_sd    constant date         := to_date('01-01-1900','dd-mm-yyyy');
begin
  --------------------------------------------------------------------------------------------------- 1
  -- IMP_SOURCE_INTERFACE (parent)
  begin
    select object_id into lv_interface_id
      from imp_source_interface where object_code = 'CLAUDE_WELL_TEST';
    update imp_source_interface
       set name='Claude Well Test', type='INSERT_UPDATE', transaction_type='ROW', source_type='EXCEL',
           overwrite='FULL', ec_data_level='P', ec_valid_level='P', staging_validation_ind='N',
           functional_area_id = ec_functional_area.object_id_by_uk('ECIS'), rev_text=v_rev
     where object_id = lv_interface_id;
  exception when no_data_found then
    insert into imp_source_interface
           (object_code, start_date, name, type, transaction_type, source_type, overwrite,
            functional_area_id, ec_data_level, ec_valid_level, staging_validation_ind, rev_text)
    values ('CLAUDE_WELL_TEST', v_sd, 'Claude Well Test', 'INSERT_UPDATE', 'ROW', 'EXCEL', 'FULL',
            ec_functional_area.object_id_by_uk('ECIS'), 'P', 'P', 'N', v_rev)
    returning object_id into lv_interface_id;
  end;

  --------------------------------------------------------------------------------------------------- 2
  -- IMP_SOURCE_MAPPING + IMP_SOURCE_PATH, one block per source column

  -- (a) WELL : KEY_LIST / STRING ; cells = UPPER_LEFT Move(0,1) .. LOWER_RIGHT FindVertical("")
  begin
    select object_id into lv_map_id from imp_source_mapping
     where object_code='CLAUDE_WELL' and imp_source_interface_id=lv_interface_id;
    update imp_source_mapping set code='WELL', sort_order=10, name='Well', path_origin='Data.A1',
           type='KEY_LIST', value_type='STRING', rev_text=v_rev where object_id=lv_map_id;
  exception when no_data_found then
    insert into imp_source_mapping (object_code, start_date, code, imp_source_interface_id, sort_order,
           name, path_origin, type, value_type, rev_text)
    values ('CLAUDE_WELL', v_sd, 'WELL', lv_interface_id, 10, 'Well', 'Data.A1', 'KEY_LIST', 'STRING', v_rev)
    returning object_id into lv_map_id;
  end;
  update imp_source_path set imp_source_mapping_id=lv_map_id, sort_order=10, type='UPPER_LEFT', path='Move',
         path_param_1='0', path_param_2='1', rev_text=v_rev where object_code='CLAUDE_WELL_10';
  if sql%rowcount=0 then
    insert into imp_source_path (object_code, start_date, imp_source_mapping_id, sort_order, type, path,
           path_param_1, path_param_2, rev_text)
    values ('CLAUDE_WELL_10', v_sd, lv_map_id, 10, 'UPPER_LEFT', 'Move', '0', '1', v_rev);
  end if;
  update imp_source_path set imp_source_mapping_id=lv_map_id, sort_order=20, type='LOWER_RIGHT',
         path='FindVertical', path_param_1='""', path_param_2=null, rev_text=v_rev where object_code='CLAUDE_WELL_20';
  if sql%rowcount=0 then
    insert into imp_source_path (object_code, start_date, imp_source_mapping_id, sort_order, type, path,
           path_param_1, path_param_2, rev_text)
    values ('CLAUDE_WELL_20', v_sd, lv_map_id, 20, 'LOWER_RIGHT', 'FindVertical', '""', null, v_rev);
  end if;

  -- (b) DATE : KEY_LIST / DATE ; cells = Move(1,1) .. FindVertical("")
  begin
    select object_id into lv_map_id from imp_source_mapping
     where object_code='CLAUDE_DATE' and imp_source_interface_id=lv_interface_id;
    update imp_source_mapping set code='DATE', sort_order=20, name='Date', path_origin='Data.A1',
           type='KEY_LIST', value_type='DATE', rev_text=v_rev where object_id=lv_map_id;
  exception when no_data_found then
    insert into imp_source_mapping (object_code, start_date, code, imp_source_interface_id, sort_order,
           name, path_origin, type, value_type, rev_text)
    values ('CLAUDE_DATE', v_sd, 'DATE', lv_interface_id, 20, 'Date', 'Data.A1', 'KEY_LIST', 'DATE', v_rev)
    returning object_id into lv_map_id;
  end;
  update imp_source_path set imp_source_mapping_id=lv_map_id, sort_order=10, type='UPPER_LEFT', path='Move',
         path_param_1='1', path_param_2='1', rev_text=v_rev where object_code='CLAUDE_DATE_10';
  if sql%rowcount=0 then
    insert into imp_source_path (object_code, start_date, imp_source_mapping_id, sort_order, type, path,
           path_param_1, path_param_2, rev_text)
    values ('CLAUDE_DATE_10', v_sd, lv_map_id, 10, 'UPPER_LEFT', 'Move', '1', '1', v_rev);
  end if;
  update imp_source_path set imp_source_mapping_id=lv_map_id, sort_order=20, type='LOWER_RIGHT',
         path='FindVertical', path_param_1='""', path_param_2=null, rev_text=v_rev where object_code='CLAUDE_DATE_20';
  if sql%rowcount=0 then
    insert into imp_source_path (object_code, start_date, imp_source_mapping_id, sort_order, type, path,
           path_param_1, path_param_2, rev_text)
    values ('CLAUDE_DATE_20', v_sd, lv_map_id, 20, 'LOWER_RIGHT', 'FindVertical', '""', null, v_rev);
  end if;

  -- (c) PRESSURE : DATA / NUMBER ; EC_KEY=claudePress, KEY_1=ROWS:WELL, KEY_2=ROWS:DATE ; Move(2,1) .. FindVertical("")
  begin
    select object_id into lv_map_id from imp_source_mapping
     where object_code='CLAUDE_PRESSURE' and imp_source_interface_id=lv_interface_id;
    update imp_source_mapping set code='PRESSURE', sort_order=30, name='Pressure', path_origin='Data.A1',
           type='DATA', value_type='NUMBER', ec_key='claudePress', key_1='ROWS:WELL', key_2='ROWS:DATE',
           rev_text=v_rev where object_id=lv_map_id;
  exception when no_data_found then
    insert into imp_source_mapping (object_code, start_date, code, imp_source_interface_id, sort_order,
           name, path_origin, type, value_type, ec_key, key_1, key_2, rev_text)
    values ('CLAUDE_PRESSURE', v_sd, 'PRESSURE', lv_interface_id, 30, 'Pressure', 'Data.A1', 'DATA', 'NUMBER',
           'claudePress', 'ROWS:WELL', 'ROWS:DATE', v_rev)
    returning object_id into lv_map_id;
  end;
  update imp_source_path set imp_source_mapping_id=lv_map_id, sort_order=10, type='UPPER_LEFT', path='Move',
         path_param_1='2', path_param_2='1', rev_text=v_rev where object_code='CLAUDE_PRESSURE_10';
  if sql%rowcount=0 then
    insert into imp_source_path (object_code, start_date, imp_source_mapping_id, sort_order, type, path,
           path_param_1, path_param_2, rev_text)
    values ('CLAUDE_PRESSURE_10', v_sd, lv_map_id, 10, 'UPPER_LEFT', 'Move', '2', '1', v_rev);
  end if;
  update imp_source_path set imp_source_mapping_id=lv_map_id, sort_order=20, type='LOWER_RIGHT',
         path='FindVertical', path_param_1='""', path_param_2=null, rev_text=v_rev where object_code='CLAUDE_PRESSURE_20';
  if sql%rowcount=0 then
    insert into imp_source_path (object_code, start_date, imp_source_mapping_id, sort_order, type, path,
           path_param_1, path_param_2, rev_text)
    values ('CLAUDE_PRESSURE_20', v_sd, lv_map_id, 20, 'LOWER_RIGHT', 'FindVertical', '""', null, v_rev);
  end if;

  --------------------------------------------------------------------------------------------------- 3
  -- IMP_TARGET_MAPPING : claudePress -> PWEL_DAY_STATUS.AVG_BH_PRESS (Class Key 1=KEY_1, Key 2=KEY_2)
  update imp_target_mapping
     set attribute='AVG_BH_PRESS', class='PWEL_DAY_STATUS', class_key_1='KEY_1', class_key_2='KEY_2',
         imp_source_interface_id=lv_interface_id, rev_text=v_rev
   where object_code='CLAUDE_PRESS_TGT' and ec_key='claudePress';
  if sql%rowcount=0 then
    insert into imp_target_mapping (object_code, start_date, ec_key, imp_source_interface_id, attribute,
           class, class_key_1, class_key_2, rev_text)
    values ('CLAUDE_PRESS_TGT', v_sd, 'claudePress', lv_interface_id, 'AVG_BH_PRESS', 'PWEL_DAY_STATUS',
           'KEY_1', 'KEY_2', v_rev);
  end if;

  commit;
end;
/
