import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
ids={'SCA':'45A9A31E13C84198E0630100007F1329','PNI':'45A9A31E13B04198E0630100007F1329'}
for code,oid in ids.items():
    print(f"\n=== {code} (eqpm {oid}) ===")
    try:
        cur.execute("select ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id(:1, DATE '2026-06-01','<=')) from dual",[oid])
        strm = cur.fetchone()[0]
        print("  capacity stream reference code (zwp_strm_ref_capacity):", strm)
        if strm:
            cur.execute("select ecdp_objects.GetObjIDFromCode('STREAM', :1) from dual",[strm])
            sid = cur.fetchone()[0]; print("  stream object id:", sid)
            cur.execute("select ecbp_stream_fluid.findGrsStdMass(:1, DATE '2026-06-01') from dual",[sid])
            print("  findGrsStdMass(stream, 2026-06-01):", cur.fetchone()[0])
        else:
            print("  -> NO capacity stream reference configured => falls back to forecast (GetPlannedVolumes)")
    except Exception as e:
        print("  ERR:", str(e)[:120])
c.close(); print("\nDONE")
