import os, oracledb
con = oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS","energy"),
    dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"), tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='COMPANY_CONTACT_VERSION' ORDER BY column_id")
print("CCV cols:", ", ".join(r[0] for r in cur.fetchall()))
print("\n=== distribution -> contact -> delivery address ===")
cur.execute("""
 SELECT dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, dsc.FORMAT_CODE, dsc.EDI_ADDRESS_CODE,
        cc.OBJECT_CODE, ccv.DELIVERY_ADDRESS, ccv.DELIVERY_ADDRESS_2, ccv.ADDRESS
 FROM DISTRIBUTION_SET_CONTACT dsc
 JOIN COMPANY_CONTACT cc ON cc.OBJECT_ID = dsc.COMPANY_CONTACT_ID
 LEFT JOIN COMPANY_CONTACT_VERSION ccv ON ccv.OBJECT_ID = cc.OBJECT_ID
 ORDER BY dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE""")
cols=[d[0] for d in cur.description]
for r in cur.fetchall():
    print("  "+" | ".join(f"{cols[i]}={'' if v is None else str(v)[:46]}" for i,v in enumerate(r)))
con.close(); print("DONE")
