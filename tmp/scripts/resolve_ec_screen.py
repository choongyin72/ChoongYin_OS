"""resolve_ec_screen.py — INPUT = an EC screen name only; derive its IUD metadata from EC config tables.
Usage:  SCREEN="contract area" py tmp/scripts/resolve_ec_screen.py
Derives: class_name, screen type (OV vs TV), date-effective?, base/version table, verify view, delete
method — so the IUD spec template needs only the screen name. SELECT only (read-only)."""
import os
import json
import oracledb
from pathlib import Path

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
SCREEN = os.environ.get("SCREEN", "contract area").strip().lower()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


def family_hint(screen, ctype, is_ov):
    """Read the curated family index (ec_screen_registry.json) and suggest which golden exemplar to CLONE:
    if the screen is already a known member -> name its family + exemplar; else list candidate families for
    this CLASS_TYPE (the live scan's discriminator picks the exact one). Pure read; degrades quietly if absent."""
    jp = os.environ.get("EC_REGISTRY_JSON") or str(
        Path(__file__).resolve().parents[2] / "workstreams" / "master-plan" / "ec-automation" / "docs" / "ec_screen_registry.json")
    try:
        fams = json.load(open(jp, encoding="utf-8"))["families"]
    except Exception as e:
        print(f"  (registry JSON not read: {str(e)[:55]} - sibling hint skipped)"); return
    s = screen.strip().lower()
    for f in fams:
        if any(m.strip().lower() == s for m in f.get("members", [])):
            print(f"""
  >>> REGISTRY MATCH: '{screen}' is family {f['key']} ({f['label']}).
      CLONE the golden exemplar -> {f['golden_exemplar']}  ({f['page_object']}; T2 {f['t2']})
      Delete: {f['delete']}""")
            return
    want = "OBJECT" if is_ov else "TABLE"
    cands = [f for f in fams if f.get("class_type") in (want, None)]
    print(f"\n  >>> REGISTRY: '{screen}' not yet covered. Candidate families for CLASS_TYPE={ctype} "
          f"(the live scan's discriminator picks the exact one):")
    for f in cands:
        print(f"      [{f['key']:16s}] clone {f['golden_exemplar']:18s} ({f['page_object']})")
        print(f"          when: {f['discriminator']}")


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
    family_hint(SCREEN, ctype, is_ov)
cur.close()
print("\nDONE (read-only). Still need LIVE recon: toolbar New/Delete state, navigator + yellow-mandatory fields, DOM ids.")
