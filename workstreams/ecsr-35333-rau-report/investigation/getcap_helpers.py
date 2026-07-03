import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
# SCA vs PNI: deferment phase + fcty_class_1_id (public eqpm fns)
print("=== SCA vs PNI: deferment phase + fcty1 id ===")
for code,oid in {'SCA':'45A9A31E13C84198E0630100007F1329','PNI':'45A9A31E13B04198E0630100007F1329'}.items():
    try:
        cur.execute("""select ec_zwp_equipment.zwp_defer_phase(ec_eqpm_version.rec_id(:1, DATE '2026-06-01','<=')),
                              ec_eqpm_version.def_fcty_class_1_id(:1, DATE '2026-06-01','<='),
                              ec_eqpm_version.uom(:1, DATE '2026-06-01','<=')
                       from dual""",[oid,oid,oid])
        r=cur.fetchone(); print(f"{code}: phase={r[0]} | fcty1_id={r[1]} | uom={r[2]}")
    except Exception as e: print(f"{code}: ERR {str(e)[:100]}")

def locate(fn):
    cur.execute("""select min(line) from all_source where name='ZWP_P_DEFER_CUSTOM' and type='PACKAGE BODY'
                   and lower(text) like :p""",['%function '+fn.lower()+'%'])
    return cur.fetchone()[0]
for fn,span in [('getStreamReferCapacity',55),('GetPlannedVolumes',60)]:
    st=locate(fn)
    print(f"\n=== {fn} body (from line {st}) ===")
    if st:
        cur.execute("""select line,text from all_source where name='ZWP_P_DEFER_CUSTOM' and type='PACKAGE BODY'
                       and line between :a and :b order by line""",[st, st+span])
        for ln,tx in cur.fetchall(): print("%4d| %s"%(ln,(tx or '').rstrip()))
c.close()
