"""resolve_ec_screen.py — INPUT = an EC screen name only; derive its IUD metadata from EC config tables.
Usage:  SCREEN="contract area" py tmp/scripts/resolve_ec_screen.py
Derives: class_name, screen type (OV vs TV), date-effective?, base/version table, verify view, delete
method — so the IUD spec template needs only the screen name. SELECT only (read-only)."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
SCREEN = os.environ.get("SCREEN", "contract area").strip().lower()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


# [1] screen label -> class_name(s). Multiple can match; pick the real screen class (skip ROWSORT/TEST/autosave variants).
cands = [r[0] for r in q("""SELECT t.class_name FROM class_property_cnfg t
                            WHERE t.property_code='LABEL' AND lower(t.property_value)=:s""", SCREEN)]
real = [c for c in cands if not any(x in c for x in ("_ROWSORT", "_TEST", "AUTOSAVE"))]
print(f"SCREEN = '{SCREEN}'  |  class_property_cnfg LABEL -> {cands}  |  chosen: {real}")

for cn in real:
    rows = q("""SELECT class_type, time_scope_code, db_object_type, db_object_name, db_object_attribute, app_space_cntx
                FROM class_cnfg WHERE class_name=:c""", cn)
    if not rows:
        print(f"  {cn}: no class_cnfg row"); continue
    ctype, tscope, dotype, dname, dattr, ctx = rows[0]
    is_ov = ctype == 'OBJECT'
    date_eff = tscope == 'VERSIONED'
    # verify view: OV_<class> for OV objects (convention); base table for TV
    view = f"OV_{cn}" if is_ov else dname
    view_ok = bool(q("SELECT 1 FROM all_views WHERE owner='ECKERNEL_EC' AND view_name=:v", view))
    print(f"""
  CLASS_NAME            = {cn}
  CLASS_TYPE           = {ctype}        -> screen type: {'OV / Manage-Object' if is_ov else 'TV / Table-class'}
  TIME_SCOPE_CODE      = {tscope}      -> date-effective: {'YES -> DELETE = End Date = Start Date' if date_eff else 'NO  -> DELETE = physical row removal'}
  DB base table        = {dname}
  DB version table     = {dattr or '(none)'}
  verify view          = {view} {'(exists)' if view_ok else '(NOT found as view - use base table / confirm)'}
  app space            = {ctx}
  => Spec sec.1: type={'OV' if is_ov else 'TV'}, date-effective={'yes' if date_eff else 'no'}, base={dname}, view={view}""")
cur.close()
print("\nDONE (read-only). Still need LIVE recon: toolbar New/Delete state, navigator + yellow-mandatory fields, DOM ids.")
