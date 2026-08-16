import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
# freetext message type object codes
cur.execute("SELECT OBJECT_ID,OBJECT_CODE FROM MESSAGE_DEFINITION WHERE UPPER(OBJECT_CODE) LIKE '%FREE%' OR UPPER(OBJECT_CODE) LIKE '%MHM13%'")
mt=cur.fetchall()
print("freetext/MHM13 message types:", mt)
# version table for MESSAGE_DEFINITION
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'MESSAGE_DEFINITION%' ORDER BY 1")
print("MD tables:", [r[0] for r in cur.fetchall()])
# columns of the version table
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='MESSAGE_DEFINITION_VERSION' ORDER BY column_id")
vc=[r[0] for r in cur.fetchall()]
print("MD_VERSION cols:", ", ".join(vc))
if mt:
    ids=[m[0] for m in mt]
    inl=",".join(f"':i{n}'".replace("'","") and f":i{n}" for n in range(len(ids)))
    binds={f"i{n}":v for n,v in enumerate(ids)}
    # pick likely FA + name columns
    namecol = "NAME" if "NAME" in vc else ("DESCRIPTION" if "DESCRIPTION" in vc else vc[1])
    facol = next((c for c in vc if "FUNCTIONAL_AREA" in c), None)
    cols = ",".join([c for c in ["OBJECT_ID",namecol,facol,"DIRECTION","FORMAT_CODE"] if c and c in vc] )
    cur.execute(f"SELECT {cols} FROM MESSAGE_DEFINITION_VERSION WHERE OBJECT_ID IN ({inl})", binds)
    print("\nMD_VERSION rows:")
    cn=[d[0] for d in cur.description]
    print(" | ".join(cn))
    for r in cur.fetchall():
        print(" | ".join("" if v is None else str(v)[:40] for v in r))
con.close();print("DONE")
