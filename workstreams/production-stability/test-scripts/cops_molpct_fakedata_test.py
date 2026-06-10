import oracledb
conn=oracledb.connect(user='ECKERNEL_EC',password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud',1521,service_name='plutodev'),tcp_connect_timeout=25)
cur=conn.cursor()
ANA=2592; DAY='2026-06-01'; CLS='TV_WELL_GAS_COMPONENT'; CODE='SCA_01'

def evaluate(tag):
    cur.execute(f"SELECT ROUND(SUM(NVL(COMP_MOL_PCT,0)),2) FROM {CLS} WHERE ANALYSIS_NO=:a",a=ANA)
    s=cur.fetchone()[0]
    cur.execute(f"""SELECT ZWP_P_VALIDATION.isComponentSumOutOfTolerance('{CLS}',:a,'COMP_MOL_PCT',
                    TO_DATE(:d,'YYYY-MM-DD')) FROM dual""",a=ANA,d=DAY)
    ret=cur.fetchone()[0]; val=round((s or 0)/100,4)
    verdict='PASS' if ret=='NO' else 'FIRES ERROR'
    print(f"   {tag:24} sum(MOL%)={str(s):>7}  value={val:>6}  ret={ret:>3}  -> {verdict}")

def patch(factor):
    cur.execute(f"SELECT COMPONENT_NO,COMP_WT_PCT FROM {CLS} WHERE ANALYSIS_NO=:a",a=ANA)
    for cno,wt in cur.fetchall():
        cur.execute(f"UPDATE {CLS} SET COMP_MOL_PCT=:v WHERE ANALYSIS_NO=:a AND COMPONENT_NO=:c",
                    v=(None if wt is None else round(wt*factor,5)),a=ANA,c=cno)
    conn.commit()

cur.execute(f"SELECT COMPONENT_NO,COMP_MOL_PCT FROM {CLS} WHERE ANALYSIS_NO=:a ORDER BY COMPONENT_NO",a=ANA)
orig=cur.fetchall()
print(f"WELL {CODE} (ANALYSIS_NO={ANA}, {DAY}) — fake-data MOL% test (rule 1157)")
print("captured original MOL%:", [m for _,m in orig])
try:
    print("\n--- baseline (original data) ---");                         evaluate("baseline")
    print("\n--- PATCHED valid: MOL% = WT% (sum 100) ---");      patch(1.0);  evaluate("valid sum 100")
    print("\n--- PATCHED below: MOL% = WT% x0.90 (sum 90) ---"); patch(0.90); evaluate("below sum 90")
    print("\n--- PATCHED above: MOL% = WT% x1.10 (sum 110) ---");patch(1.10); evaluate("above sum 110")
finally:
    for cno,mol in orig:
        cur.execute(f"UPDATE {CLS} SET COMP_MOL_PCT=:v WHERE ANALYSIS_NO=:a AND COMPONENT_NO=:c",v=mol,a=ANA,c=cno)
    conn.commit()
    cur.execute(f"SELECT COMPONENT_NO,COMP_MOL_PCT FROM {CLS} WHERE ANALYSIS_NO=:a ORDER BY COMPONENT_NO",a=ANA)
    after=cur.fetchall()
    print("\n--- REVERTED ---")
    print("   MOL% after revert:", [m for _,m in after])
    print("   *** revert OK ***" if all(a==o for (_,a),(_,o) in zip(after,orig)) else "   *** REVERT MISMATCH ***")
cur.close();conn.close()
