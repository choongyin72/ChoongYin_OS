import oracledb
conn=oracledb.connect(user='ECKERNEL_EC',password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud',1521,service_name='plutodev'),tcp_connect_timeout=25)
cur=conn.cursor()
COL='COMP_MOL_PCT'

def positive(label, event_view, comp_class, day):
    cur.execute(f"""
      SELECT a.ANALYSIS_NO, o.CODE, o.NAME,
        (SELECT ROUND(SUM(NVL(c.{COL},0)),2) FROM {comp_class} c WHERE c.ANALYSIS_NO=a.ANALYSIS_NO) sum_v,
        ZWP_P_VALIDATION.isComponentSumOutOfTolerance('{comp_class}',a.ANALYSIS_NO,'{COL}',a.DAYTIME) is_out,
        NVL(ec_ctrl_system_attribute.attribute_value(a.DAYTIME,'ZWP_STRM_SUM_COMP_LOWER','<='),0.98) lo,
        NVL(ec_ctrl_system_attribute.attribute_value(a.DAYTIME,'ZWP_STRM_SUM_COMP_UPPER','<='),1.02) up
      FROM {event_view} a JOIN TV_OBJECTS o ON o.OBJECT_ID=a.OBJECT_ID
      WHERE a.DAYTIME=TO_DATE('{day}','YYYY-MM-DD') AND a.ANALYSIS_NO IS NOT NULL
      ORDER BY a.ANALYSIS_NO""")
    print(f"\n{label}  (DAYTIME={day})  [COL={COL}]")
    print(f"  {'ANA':>5}|{'code':12}|{'name':22}|{'sumMOL':>7}|{'val':>5}|{'ret':>3}|{'lower':>5}|{'upper':>5}| verdict")
    print("  "+"-"*92)
    npass=nfire=0
    for ana,code,name,s,out,lo,up in cur.fetchall():
        val=round((s or 0)/100,4); verdict='FIRES ERROR' if out=='YES' else 'PASS'
        if out=='YES': nfire+=1
        else: npass+=1
        print(f"  {ana:>5}|{str(code)[:12]:12}|{str(name)[:22]:22}|{str(s):>7}|{val:>5}|{out:>3}|{lo:>5}|{up:>5}| {verdict}")
    print(f"   -> PASS={npass} FIRE={nfire}")

def negative(label, comp_class, event_view):
    rule='1156' if 'STRM' in comp_class else '1157'
    cur.execute(f"""
      SELECT * FROM (
        SELECT a.ANALYSIS_NO, o.CODE, a.DAYTIME,
          (SELECT ROUND(SUM(NVL(c.{COL},0)),2) FROM {comp_class} c WHERE c.ANALYSIS_NO=a.ANALYSIS_NO) sum_v,
          ZWP_P_VALIDATION.isComponentSumOutOfTolerance('{comp_class}',a.ANALYSIS_NO,'{COL}',a.DAYTIME) is_out
        FROM {event_view} a JOIN TV_OBJECTS o ON o.OBJECT_ID=a.OBJECT_ID
        WHERE a.ANALYSIS_NO IS NOT NULL
      ) WHERE sum_v IS NOT NULL AND sum_v NOT BETWEEN 98 AND 102 AND sum_v<>0
      FETCH FIRST 5 ROWS ONLY""")
    rows=cur.fetchall()
    print(f"\n{label} — REAL out-of-range MOL% analyses:")
    print(f"   {'Rule':>4}|{'Analysis':>8}|{'date':>10}|{'code':14}|{'sum(MOL%)':>9}|{'value':>6}|{'ret':>3}| verdict")
    print("   "+"-"*86)
    if not rows: print("   (none found)")
    for ana,code,day,s,out in rows:
        val=round((s or 0)/100,4); verdict='FIRES ERROR' if out=='YES' else 'PASS'
        side=' (below 0.98)' if val<0.98 else (' (above 1.02)' if val>1.02 else '')
        print(f"   {rule:>4}|{ana:>8}|{day:%Y-%m-%d}|{str(code)[:14]:14}|{str(s):>9}|{val:>6}|{out:>3}| {verdict}{side}")

print("===== PART A: valid MOL% sums SHOULD PASS =====")
positive("RULE 1156 | Stream Gas Component Analysis","RV_STRM_GAS_ANALYSIS","TV_STRM_GAS_COMPONENT","2026-08-31")
positive("RULE 1157 | Well Gas Component Analysis","RV_WELL_GAS_ANALYSIS","TV_WELL_GAS_COMPONENT","2025-12-01")
print("\n===== PART B: out-of-range MOL% sums SHOULD FIRE =====")
negative("RULE 1156 stream","TV_STRM_GAS_COMPONENT","RV_STRM_GAS_ANALYSIS")
negative("RULE 1157 well","TV_WELL_GAS_COMPONENT","RV_WELL_GAS_ANALYSIS")
cur.close();conn.close()
print("\ndone (read-only)")
