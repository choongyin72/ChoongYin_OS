import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
T1='45A9A31E13984198E0630100007F1329'   # PLU_LNG_TRAIN1 deferment eqpm
def one(t,sql,args=None):
    try:
        cur.execute(sql,args or {}); r=cur.fetchone(); print(f"{t}: {r[0] if r else '(no row)'}")
    except Exception as e: print(f"{t}: ERR {str(e)[:110]}")

print("=== LNG Train 1 capacity trace (June 2026) ===")
one("deferment phase", "select ec_zwp_equipment.zwp_defer_phase(ec_eqpm_version.rec_id(:1,DATE '2026-06-01','<=')) from dual",[T1])
one("fcty_class_1_id", "select ec_eqpm_version.def_fcty_class_1_id(:1,DATE '2026-06-01','<=') from dual",[T1])
one("getCapacity('EQPM',T1,01-Jun)", "select zwp_p_defer_custom.getCapacity('EQPM',:1,DATE '2026-06-01') from dual",[T1])
one("zwp_strm_ref_capacity (techmax stream code)", "select ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id(:1,DATE '2026-06-01','<=')) from dual",[T1])
# techmax path used by the RAU calc for LNG trains: findGrsStdMass(stream, TRUNC(MM)..LAST_DAY)
cur.execute("select ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id(:1,DATE '2026-06-01','<=')) from dual",[T1])
strm=cur.fetchone()[0]
print("  techmax stream code:", strm)
if strm:
    cur.execute("select ecdp_objects.GetObjIDFromCode('STREAM',:1) from dual",[strm]); sid=cur.fetchone()[0]
    one("  findGrsStdMass(stream, month range)","select ecbp_stream_fluid.findGrsStdMass(:1, TRUNC(DATE '2026-06-01','MM'), LAST_DAY(TRUNC(DATE '2026-06-01','MM'))) from dual",[sid])
one("getGroupForecastId(fcty1,CAPACITY)", """select zwp_p_defer_custom.getGroupForecastId(ec_eqpm_version.def_fcty_class_1_id(:1,DATE '2026-06-01','<='),DATE '2026-06-01','CAPACITY') from dual""",[T1])
# summary capacity for Train1 June
one("TV_ZWP_DEF_DAY_SUMMARY sum(CAPACITY) June", """select round(sum(s.CAPACITY),2) from TV_ZWP_DEF_DAY_SUMMARY s
   join ov_eqpm e on e.OBJECT_ID=s.ASSET_ID and e.eqpm_type='DEFERMENT'
   where e.DEF_FCTY_1_CODE='PLU_LNG_TRAIN1' and s.DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')""")
c.close(); print("\nDONE")
