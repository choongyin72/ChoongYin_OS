import oracledb
conn=oracledb.connect(user='ECKERNEL_EC',password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud',1521,service_name='plutodev'),tcp_connect_timeout=25)
cur=conn.cursor()

# 1) raw system attribute values (what the function reads), as-of each test date
for d in ('2026-08-31','2025-12-01','2026-06-10'):
    cur.execute("""SELECT
        ec_ctrl_system_attribute.attribute_value(TO_DATE(:d,'YYYY-MM-DD'),'ZWP_STRM_SUM_COMP_LOWER','<='),
        ec_ctrl_system_attribute.attribute_value(TO_DATE(:d,'YYYY-MM-DD'),'ZWP_STRM_SUM_COMP_UPPER','<=')
      FROM dual""", d=d)
    lo,up=cur.fetchone()
    print(f"  ZWP_STRM_SUM_COMP as-of {d}:  _LOWER={lo}  _UPPER={up}")

def block(label, event_view, comp_class, col, day):
    # effective limits EXACTLY as the FIXED function computes (source lines 215-224, recompiled 2026-06-10 20:57):
    #   upper = NVL(attribute_value(_UPPER), 1.02) ; lower = NVL(attribute_value(_LOWER), 0.98)
    cur.execute(f"""
      SELECT a.ANALYSIS_NO, o.CODE, o.NAME,
        (SELECT ROUND(SUM(NVL(c.{col},0)),2) FROM {comp_class} c WHERE c.ANALYSIS_NO=a.ANALYSIS_NO) sum_wt,
        ZWP_P_VALIDATION.isComponentSumOutOfTolerance('{comp_class}',a.ANALYSIS_NO,'{col}',a.DAYTIME) is_out,
        NVL(ec_ctrl_system_attribute.attribute_value(a.DAYTIME,'ZWP_STRM_SUM_COMP_LOWER','<='),0.98) eff_lower,
        NVL(ec_ctrl_system_attribute.attribute_value(a.DAYTIME,'ZWP_STRM_SUM_COMP_UPPER','<='),1.02) eff_upper
      FROM {event_view} a JOIN TV_OBJECTS o ON o.OBJECT_ID=a.OBJECT_ID
      WHERE a.DAYTIME=TO_DATE('{day}','YYYY-MM-DD') AND a.ANALYSIS_NO IS NOT NULL
      ORDER BY a.ANALYSIS_NO""")
    print(f"\n{label}  (DAYTIME={day})")
    print(f"  {'ANA':>5}|{'code':12}|{'name':24}|{'sumWT':>6}|{'val':>5}|{'ret':>3}|{'lower':>5}|{'upper':>5}| why / verdict")
    print("  "+"-"*112)
    for ana,code,name,s,out,lo,up in cur.fetchall():
        val=round((s or 0)/100,4)
        why=[]
        if val<lo: why.append(f"val<{lo}")
        if val>up: why.append(f"val>{up}")
        why=' & '.join(why) if why else f"{lo}<=val<={up}"
        verdict='FIRES ERROR' if out=='YES' else 'PASS'
        print(f"  {ana:>5}|{str(code)[:12]:12}|{str(name)[:24]:24}|{str(s):>6}|{val:>5}|{out:>3}|{lo:>5}|{up:>5}| {why} -> {verdict}")

print("\n--- SYSTEM ATTRIBUTE TOLERANCE (raw) ---")
block("RULE 1077 | Stream Gas Component Analysis","RV_STRM_GAS_ANALYSIS","TV_STRM_GAS_COMPONENT","COMP_WT_PCT","2026-08-31")
block("RULE 1083 | Well Gas Component Analysis","RV_WELL_GAS_ANALYSIS","TV_WELL_GAS_COMPONENT","COMP_WT_PCT","2025-12-01")
cur.close();conn.close()
print("\ndone (read-only)")
