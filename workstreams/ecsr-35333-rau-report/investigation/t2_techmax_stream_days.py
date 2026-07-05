import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
for strm in ['LNG_TRAIN_2_TECHMAX','LNG_TRAIN_1_DEF_CAP']:
    cur.execute("""select count(*), min(daytime), max(daytime), round(min(grs_mass),1), round(max(grs_mass),1), round(sum(grs_mass),1)
                   from strm_day_stream s join stream o on o.object_id=s.object_id
                   where o.object_code=:s and s.daytime between DATE '2026-06-01' and DATE '2026-06-30'""",{'s':strm})
    r=cur.fetchone()
    print(f"{strm:22} June rows={r[0]}  range={r[1]}..{r[2]}  grs_mass min={r[3]} max={r[4]} SUM={r[5]}")
c.close()
