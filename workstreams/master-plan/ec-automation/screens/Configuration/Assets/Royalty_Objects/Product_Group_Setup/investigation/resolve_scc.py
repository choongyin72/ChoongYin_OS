"""Last targeted hunt for the Stream Calc Category backing class/table. READ-ONLY."""
import oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL").cursor()


def q(t, sql, a=None):
    print(f"\n=== {t} ===")
    try:
        rows = cur.execute(sql, a or []).fetchall()
        for r in rows[:40]: print("   ", r)
        if not rows: print("   (none)")
    except Exception as e: print("   ERR", str(e)[:90])


q("LABELs LIKE %calc%cat% or %stream%calc%",
  """SELECT class_name, property_value FROM class_property_cnfg WHERE property_code='LABEL'
     AND (lower(property_value) LIKE '%calc%cat%' OR lower(property_value) LIKE '%stream%calc%'
          OR lower(property_value) LIKE '%calculation category%')""")
q("class_cnfg class_name LIKE %STRM_CALC% / %SCC% / %CALC_CAT% / %STREAM_CALC%",
  """SELECT class_name, class_type, db_object_type, db_object_name FROM class_cnfg
     WHERE class_name LIKE '%STRM_CALC%' OR class_name LIKE '%SCC%' OR class_name LIKE '%CALC_CAT%'
        OR class_name LIKE '%STREAM_CALC%'""")
q("class_property_cnfg rows where property_value mentions 'strm_calc_cat' (component id)",
  """SELECT class_name, property_code, property_value FROM class_property_cnfg
     WHERE lower(property_value) LIKE '%strm_calc_cat%' AND ROWNUM<=20""")
q("class for label 'product group setup' partial (the middle grid class)",
  """SELECT class_name, property_value FROM class_property_cnfg WHERE property_code='LABEL'
     AND lower(property_value) LIKE 'product group setup%'""")
cur.connection.close() if hasattr(cur, 'connection') else None
