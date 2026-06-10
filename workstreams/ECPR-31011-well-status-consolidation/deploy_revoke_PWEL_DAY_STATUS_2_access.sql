-- ============================================================================
-- ECPR-31011  Hide "Daily Production Well Status 2 (SCA)" screen
-- DEPLOY: revoke ALL role access by DELETING the access rows for the screen
--         URL object (object_id 5097 on plutodev, resolved by name below).
-- Target : plutodev (ECKERNEL_EC) — Woodside Pluto DEV
-- Rollback: rollback_restore_PWEL_DAY_STATUS_2_access.sql (restores all 18
--           rows with original levels; pre-change state also in
--           access_backup_PWEL_DAY_STATUS_2.csv)
-- Note   : DELETE goes through view TV_T_BASIS_ACCESS so the EC IUD trigger
--          handles journalling, same as Pluto_Config access scripts.
-- ============================================================================

-- pre-check: expect 18
SELECT COUNT(*) AS rows_before
FROM   tv_t_basis_access
WHERE  object_id = (SELECT object_id FROM t_basis_object
                    WHERE  object_name = '/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS_2');

-- revoke: delete every role-access row for the SCA screen object
DELETE FROM tv_t_basis_access
WHERE  object_id = (SELECT object_id FROM t_basis_object
                    WHERE  object_name = '/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS_2');

-- post-check: expect 0
SELECT COUNT(*) AS rows_after
FROM   tv_t_basis_access
WHERE  object_id = (SELECT object_id FROM t_basis_object
                    WHERE  object_name = '/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS_2');

-- sanity: screens 1 and 3 must be untouched (expect 18 and 5)
SELECT o.object_name, COUNT(a.t_basis_access_id) AS access_rows
FROM   t_basis_object o
LEFT   JOIN tv_t_basis_access a ON a.object_id = o.object_id
WHERE  o.object_name IN (
  '/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS',
  '/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS_3')
GROUP  BY o.object_name;

COMMIT;
