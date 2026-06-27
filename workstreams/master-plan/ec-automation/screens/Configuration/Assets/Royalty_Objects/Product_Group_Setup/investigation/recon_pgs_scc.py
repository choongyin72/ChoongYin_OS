"""RC.0054 follow-up READ-ONLY recon: find the 'Stream Calculation Category' backing (first
search missed it) + confirm Product Group Cost scoping (group-only or group+product)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()


def q(title, sql, args=None):
    print(f"\n=== {title} ===")
    try:
        cur.execute(sql, args or [])
        rows = cur.fetchall()
        for r in rows[:40]:
            print("   ", r)
        if not rows:
            print("   (none)")
    except Exception as e:
        print("   ERR", str(e)[:110])


# broaden the hunt for the stream calc category entity
q("any TABLE/VIEW with CALC + (CAT or CATEG)",
  """SELECT object_name, object_type FROM all_objects WHERE owner='ECKERNEL_EC'
     AND object_type IN ('TABLE','VIEW') AND object_name LIKE '%CALC%'
     AND (object_name LIKE '%CAT%') ORDER BY object_type, object_name""")
q("any TABLE/VIEW with STRM or STREAM + CALC",
  """SELECT object_name, object_type FROM all_objects WHERE owner='ECKERNEL_EC'
     AND object_type IN ('TABLE','VIEW') AND (object_name LIKE '%STRM%' OR object_name LIKE '%STREAM%')
     AND object_name LIKE '%CALC%' ORDER BY object_type, object_name""")
q("columns named like %CALC%CAT% anywhere (which table holds the category)",
  """SELECT table_name, column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
     AND (column_name LIKE '%CALC%CAT%' OR column_name LIKE '%CALCULATION_CAT%' OR column_name LIKE '%STRM_CALC%')
     AND table_name NOT LIKE '%_JN' ORDER BY table_name""")
q("PRODUCT_GROUP* tables again incl any child not seen (full list any name with PROD_GRP/PG)",
  """SELECT object_name, object_type FROM all_objects WHERE owner='ECKERNEL_EC'
     AND object_type IN ('TABLE','VIEW') AND (object_name LIKE '%PROD_GRP%' OR object_name LIKE '%PG_%')
     ORDER BY object_name""")

# Product Group Cost scoping: is PRODUCT_CODE populated (per-product) or null (group-level)?
q("DV_PRODUCT_GROUP_COST rows for TIETO_BLEND (cost type, product, columns)",
  """SELECT object_code, product_code, cost_type, cost_column, price_column, sum_value_cost_ind, sort_order
     FROM dv_product_group_cost WHERE object_code='TIETO_BLEND' ORDER BY sort_order""")
q("DV_PRODUCT_GROUP_COST distinct PRODUCT_CODE null vs set (scoping)",
  """SELECT CASE WHEN product_code IS NULL THEN 'NULL (group-level)' ELSE 'SET (per-product)' END scope,
            COUNT(*) n FROM dv_product_group_cost GROUP BY CASE WHEN product_code IS NULL THEN 'NULL (group-level)' ELSE 'SET (per-product)' END""")

# member pool for the SETUP grid: products + are any products NOT yet in a chosen test group?
q("OV_PRODUCT count + a few codes (member pool for Setup grid)",
  """SELECT code, name FROM ov_product WHERE ROWNUM<=12 ORDER BY code""")
q("products already in TIETO_BLEND (so I can pick one NOT in it)",
  """SELECT product_code FROM dv_product_group_setup WHERE object_code='TIETO_BLEND'""")
c.close()
