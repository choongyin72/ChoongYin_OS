"""READ-ONLY: resolve each distribution's recipient DELIVERY_ADDRESS (email) from
COMPANY_CONTACT_VERSION, to decide if any distribution is already SAFE (non-deliverable). NO writes."""
import os
import oracledb

con = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = con.cursor()

print("=== distribution -> contact -> delivery address (COMPANY_CONTACT_VERSION) ===")
cur.execute(
    """
    SELECT dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, dsc.FORMAT_CODE,
           cc.OBJECT_CODE, ccv.DELIVERY_ADDRESS, ccv.DELIVERY_ADDRESS_2,
           ccv.ADDRESS, ccv.START_DATE, ccv.END_DATE
    FROM DISTRIBUTION_SET_CONTACT dsc
    JOIN COMPANY_CONTACT cc ON cc.OBJECT_ID = dsc.COMPANY_CONTACT_ID
    LEFT JOIN COMPANY_CONTACT_VERSION ccv ON ccv.OBJECT_ID = cc.OBJECT_ID
    ORDER BY dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, ccv.START_DATE
    """
)
cols = [d[0] for d in cur.description]
for r in cur.fetchall():
    print("  " + " | ".join(f"{cols[i]}={'' if v is None else str(v)[:42]}" for i, v in enumerate(r)))

# EDI addresses (for the B:14 / B154 edi-coded contacts)
print("\n=== DV_EDI_ADDRESS sample (edi address resolution) ===")
try:
    cur.execute("SELECT * FROM DV_EDI_ADDRESS WHERE ROWNUM<=20")
    cols = [d[0] for d in cur.description]
    for r in cur.fetchall():
        nn = [f"{cols[i]}={str(v)[:30]}" for i, v in enumerate(r) if v is not None]
        print("  " + " ; ".join(nn))
except Exception as e:
    print("  ERR:", str(e)[:160])

con.close()
print("DONE")
