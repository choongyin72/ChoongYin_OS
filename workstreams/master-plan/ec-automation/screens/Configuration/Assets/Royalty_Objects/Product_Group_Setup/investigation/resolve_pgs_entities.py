"""Resolve the 3 Product Group Setup sub-entities -> class -> backing table/view, via EC config
(class_property_cnfg LABEL -> class_cnfg db_object_name). READ-ONLY."""
import oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL").cursor()

for label in ("product group setup", "product group cost", "stream calculation category"):
    print(f"\n=== LABEL '{label}' ===")
    cands = [r[0] for r in cur.execute(
        "SELECT class_name FROM class_property_cnfg WHERE property_code='LABEL' AND lower(property_value)=:s", [label]).fetchall()]
    real = [c for c in cands if not any(x in c for x in ("_ROWSORT", "_TEST", "AUTOSAVE"))]
    print("   class candidates:", cands, "| chosen:", real)
    for cn in real:
        rows = cur.execute(
            "SELECT class_type, time_scope_code, db_object_type, db_object_name, db_object_attribute FROM class_cnfg WHERE class_name=:c", [cn]).fetchall()
        for r in rows:
            print(f"   {cn}: class_type={r[0]} time_scope={r[1]} db_obj_type={r[2]} db_object_name={r[3]} attr={r[4]}")
            # the verify view convention: DV_<base> for these detail (TABLE) classes
            base = r[3]
            if base:
                for pref in ("DV_", "OV_", ""):
                    v = pref + base
                    try:
                        n = cur.execute(f"SELECT COUNT(*) FROM {v}").fetchone()[0]
                        print(f"       {v}: EXISTS, {n} rows")
                    except Exception:
                        pass
cur.connection.close() if hasattr(cur, 'connection') else None
