import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
def one(sql, binds):
    cur.execute(sql, binds); r=cur.fetchone(); return r[0] if r else None
for name, ctr, oid, branch in [('LNG Train 2','C_PLU_LNG_2','45A9A31E13A04198E0630100007F1329','TECHMAX'),
                               ('SCA Gas Export','C_SCA_GAS_EXP','45A9A31E13C84198E0630100007F1329','SUMMARY')]:
    print("="*78); print(f"### {name}  ({ctr})  branch={branch}")
    if branch=='TECHMAX':
        strm=one("select ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id(:o,DATE '2026-06-01','<=')) from dual",{'o':oid})
        cap_raw=one("select ecbp_stream_fluid.findGrsStdMass(ecdp_objects.GetObjIDFromCode('STREAM',:s), TRUNC(DATE '2026-06-01','MM'), LAST_DAY(TRUNC(DATE '2026-06-01','MM'))) from dual",{'s':strm})
        cap=one("""select EcDp_Unit.convertValue(:c,
                 zwp_p_defer_custom.getEcCodedependency('DEFERMENT_PHASE','DEFERMENT_UNIT_TYPE',
                    ec_zwp_equipment.zwp_defer_phase(ec_eqpm_version.rec_id(:o,DATE '2026-06-01','<='))),
                 ec_eqpm_version.uom(:o2,DATE '2026-06-01','<='), NULL) from dual""",{'c':cap_raw,'o':oid,'o2':oid})
        print(f"  techmax stream={strm}  raw(kg)={cap_raw}  converted cap={cap}")
    else:
        cap=one("select sum(CAPACITY) from TV_ZWP_DEF_DAY_SUMMARY where ASSET_ID=:o and DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')",{'o':oid})
        print(f"  summary capacity = {cap}")
    def dsum(extra=""):
        return one(f"select sum(decode(DEF_QTY,NULL,DEF_QTY_DER,DEF_QTY)) from TV_ZWP_DEF_DAY_DETAIL where ASSET_ID=:o and DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01') {extra}",{'o':oid})
    unpl=dsum("and LOSS_CATEGORY='REAS_3_UNPL'") or 0
    plan=dsum("and LOSS_CATEGORY='REAS_3_PLAN'") or 0
    tot =dsum() or 0
    print(f"  deferments: unplanned={unpl:.2f} planned={plan:.2f} TOTAL={tot:.2f}")
    exp=None
    if cap and cap!=0:
        exp={'RELIABILITY':(cap-unpl)/cap*100,'AVAILABILITY':(cap-(unpl+plan))/cap*100,'UTILISATION':(cap-tot)/cap*100}
    else:
        print("  -> capacity 0/NULL: Stage-E SKIP (nothing written)")
    cur.execute("select ACCOUNT_CODE, QTY from DV_SCTR_ACC_MTH_EVENT where OBJECT_CODE=:c and DAYTIME=DATE '2026-06-01' and ACCOUNT_CODE like 'RAU%_ACT'",{'c':ctr})
    stored={r[0].replace('RAU_','').replace('_ACT',''):r[1] for r in cur.fetchall()}
    for m in ['RELIABILITY','AVAILABILITY','UTILISATION']:
        s=stored.get(m); e=exp[m] if exp else None
        if e is None and s is None: v="NO EVENT (calc skipped)"
        elif s is None: v="MISSING event"
        else: v="match" if abs(e-s)<0.05 else f"MISMATCH expected={e:.4f}"
        print(f"    {m:13} stored={('%.4f'%s) if s is not None else 'None':>12}  expected={('%.4f'%e) if e is not None else '-':>12}  -> {v}")
c.close()
