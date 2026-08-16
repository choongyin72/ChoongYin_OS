"""READ-ONLY: locate where contact email/delivery addresses live and resolve each distribution's
recipients. DISTRIBUTION_SET_CONTACT.COMPANY_CONTACT_ID -> COMPANY_CONTACT.OBJECT_ID. NO writes."""
import os
import oracledb

con = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = con.cursor()

# 1) which columns anywhere look like an email/delivery address?
print("=== columns that look like email/address across contact-ish tables ===")
cur.execute(
    """
    SELECT table_name, column_name FROM all_tab_columns
    WHERE owner='ECKERNEL_EC'
      AND (column_name LIKE '%EMAIL%' OR column_name LIKE '%E_MAIL%'
           OR column_name LIKE '%ADDRESS%' OR column_name LIKE '%EDI%')
      AND (table_name LIKE '%CONTACT%' OR table_name LIKE '%EDI%'
           OR table_name LIKE '%COMM%' OR table_name LIKE '%COMPANY%')
    ORDER BY table_name, column_name
    """
)
for t, c in cur.fetchall():
    print(f"  {t}.{c}")

# 2) the contacts referenced by our distributions
print("\n=== referenced contacts (OBJECT_CODE / CLASS / COMPANY) ===")
cur.execute(
    """
    SELECT dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, cc.OBJECT_CODE, cc.CLASS_NAME,
           cc.COMPANY_ID, cc.OBJECT_ID
    FROM DISTRIBUTION_SET_CONTACT dsc
    JOIN COMPANY_CONTACT cc ON cc.OBJECT_ID = dsc.COMPANY_CONTACT_ID
    ORDER BY dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE
    """
)
contact_ids = []
for r in cur.fetchall():
    print(f"  {r[0]:30} {r[1]:5} code={r[2]} class={r[3]} company={r[4]}")
    contact_ids.append(r[5])

# 3) EDI addresses for those contacts (COMPANY_CONTACT_EDI)
print("\n=== COMPANY_CONTACT_EDI cols ===")
cur.execute(
    "SELECT column_name FROM all_tab_columns WHERE table_name='COMPANY_CONTACT_EDI' ORDER BY column_id"
)
print("  ", ", ".join(r[0] for r in cur.fetchall()))

print("\n=== COMPANY_CONTACT_EDI rows for referenced contacts ===")
if contact_ids:
    binds = {f"c{i}": v for i, v in enumerate(contact_ids)}
    inlist = ",".join(f":c{i}" for i in range(len(contact_ids)))
    try:
        cur.execute(f"SELECT * FROM COMPANY_CONTACT_EDI WHERE OBJECT_ID IN ({inlist})", binds)
        cols = [d[0] for d in cur.description]
        for r in cur.fetchall():
            nn = [f"{cols[i]}={str(v)[:44]}" for i, v in enumerate(r) if v is not None]
            print("  " + " ; ".join(nn))
    except Exception as e:
        print("  ERR:", str(e)[:160])

con.close()
print("DONE")
