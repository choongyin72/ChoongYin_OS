"""RC.0054 Product Group Setup - READ-ONLY DB deep-dive (local sandbox localhost:1521/ORCL).
Understand the 3 sub-entities (Product Group Setup / Cost / Stream Calc Category), their backing
views/tables + columns, the parent (Product Group), and pick a safe test target. No writes."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()


def q(title, sql, args=None):
    print(f"\n=== {title} ===")
    try:
        cur.execute(sql, args or [])
        rows = cur.fetchall()
        for r in rows[:30]:
            print("   ", r)
        if len(rows) > 30:
            print(f"   ... (+{len(rows)-30} more)")
    except Exception as e:
        print("   ERR", str(e)[:110])


# 1. resolve the screen via class metadata
q("class_property_cnfg LABEL ~ 'Product Group Setup'/'Product Group Cost'",
  """SELECT label, class_name FROM class_property_cnfg
     WHERE UPPER(label) IN ('PRODUCT GROUP SETUP','PRODUCT GROUP COST','STREAM CALCULATION CATEGORY')""")

# 2. all PRODUCT_GROUP* + STREAM_CALC* tables/views
q("tables/views LIKE %PRODUCT_GROUP%",
  """SELECT object_name, object_type FROM all_objects
     WHERE owner='ECKERNEL_EC' AND object_type IN ('TABLE','VIEW')
       AND object_name LIKE '%PRODUCT_GROUP%' ORDER BY object_type, object_name""")
q("tables/views LIKE %STRM_CALC% / %STREAM_CALC% / %CALC_CATEG%",
  """SELECT object_name, object_type FROM all_objects
     WHERE owner='ECKERNEL_EC' AND object_type IN ('TABLE','VIEW')
       AND (object_name LIKE '%STRM_CALC%' OR object_name LIKE '%STREAM_CALC%' OR object_name LIKE '%CALC_CATEG%')
     ORDER BY object_type, object_name""")

# 3. columns of the likely detail views (try DV_ first, then base)
for v in ("DV_PRODUCT_GROUP_SETUP", "DV_PRODUCT_GROUP_COST", "PRODUCT_GROUP_SETUP", "PRODUCT_GROUP_COST"):
    q(f"{v} columns",
      "SELECT column_name, data_type FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id",
      [v])

# 4. parent list + the selected group's details
q("OV_PRODUCT_GROUP (parent groups, first 30)",
  "SELECT code, name, TO_CHAR(object_start_date,'YYYY-MM-DD') FROM ov_product_group ORDER BY code")
q("DV_PRODUCT_GROUP_SETUP rows for TIETO_BLEND (the selected group)",
  "SELECT * FROM dv_product_group_setup WHERE object_code='TIETO_BLEND'")
q("row counts per group (which groups are smallest / candidate test targets)",
  """SELECT object_code, COUNT(*) n FROM dv_product_group_setup GROUP BY object_code ORDER BY n""")
c.close()
