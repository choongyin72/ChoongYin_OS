"""Recompute Period Actuals per gate-PASS equipment (June 2026) and compare vs stored RAU_*_ACT. Read-only."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
# gate-PASS equipment: (fcty, contract, eqpm_object_id, capacity_branch)
EQ=[('PLA Gas Export','C_PLA_GAS_EXP','45A9A31E13B84198E0630100007F1329','SUMMARY'),
    ('PLA Liquid Export','C_PLA_LIQ_EXP','45A9A31E13C04198E0630100007F1329','SUMMARY'),
    ('LNG Train 2','C_PLU_LNG_2','45A9A31E13A04198E0630100007F1329','TECHMAX'),
    ('SCA Gas Export','C_SCA_GAS_EXP','45A9A31E13C84198E0630100007F1329','SUMMARY')]
def one(sql, binds):
    cur.execute(sql, binds); r=cur.fetchone(); return r[0] if r else None
for name, ctr, oid, branch in EQ:
    print("="*78); print(f"### {name}  ({ctr})  capacity-branch={branch}")
    # capacity (month) per calc branch
    if branch=='TECHMAX':
        strm=one("select ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id(:1,DATE '2026-06-01','<=')) from dual",[oid])
        cap_raw=one("select ecbp_stream_fluid.findGrsStdMass(ecdp_objects.GetObjIDFromCode('STREAM',:1), TRUNC(DATE '2026-06-01','MM'), LAST_DAY(TRUNC(DATE '2026-06-01','MM'))) from dual",[strm])
        # unit conversion per calc: phase->from_unit, eqpm uom->to_unit
        cap=one("""select EcDp_Unit.convertValue(:1,
                     zwp_p_defer_custom.getEcCodedependency('DEFERMENT_PHASE','DEFERMENT_UNIT_TYPE',
                        ec_zwp_equipment.zwp_defer_phase(ec_eqpm_version.rec_id(:2,DATE '2026-06-01','<='))),
                     ec_eqpm_version.uom(:2,DATE '2026-06-01','<='), NULL) from dual""",[cap_raw,oid])
        print(f"  techmax stream={strm}  raw={cap_raw}  converted cap={cap}")
    else:
        cap=one("""select sum(CAPACITY) from TV_ZWP_DEF_DAY_SUMMARY
                   where ASSET_ID=:1 and DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')""",[oid])
        print(f"  summary capacity (month sum) = {cap}")
    # deferment sums (calc's exact expressions)
    def dsum(extra=""):
        return one(f"""select sum(decode(DEF_QTY,NULL,DEF_QTY_DER,DEF_QTY)) from TV_ZWP_DEF_DAY_DETAIL
                where ASSET_ID=:1 and DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01') {extra}""",[oid])
    unpl=dsum("and LOSS_CATEGORY='REAS_3_UNPL'") or 0
    plan=dsum("and LOSS_CATEGORY='REAS_3_PLAN'") or 0
    tot =dsum() or 0
    print(f"  deferments: unplanned={unpl:.2f}  planned={plan:.2f}  TOTAL={tot:.2f}")
    if cap and cap!=0:
        exp={'RELIABILITY':(cap-unpl)/cap*100,'AVAILABILITY':(cap-(unpl+plan))/cap*100,'UTILISATION':(cap-tot)/cap*100}
    else:
        exp=None; print("  -> capacity 0/NULL: calc writes NOTHING (Stage-E skip)")
    # stored
    cur.execute("""select ACCOUNT_CODE, QTY from DV_SCTR_ACC_MTH_EVENT
                   where OBJECT_CODE=:1 and DAYTIME=DATE '2026-06-01' and ACCOUNT_CODE like 'RAU%_ACT'""",[ctr])
    stored={r[0].replace('RAU_','').replace('_ACT',''):r[1] for r in cur.fetchall()}
    for m in ['RELIABILITY','AVAILABILITY','UTILISATION']:
        s=stored.get(m); e=exp[m] if exp else None
        if e is None and s is None: verdict="FAIL (never calculated - no event written)"
        elif s is None:             verdict="FAIL (missing event)"
        elif e is None:             verdict="FAIL (event exists but capacity=0??)"
        else:
            verdict = "match" if abs(e-s)<0.01 else f"MISMATCH exp={e:.4f}"
        print(f"    {m:13} stored={('%.4f'%s) if s is not None else 'None':>12}  expected={('%.4f'%e) if e is not None else '-':>12}  -> {verdict}")
c.close()
