"""READ-ONLY: resolve the real email/delivery addresses behind each distribution's contacts, so we can
pick (or confirm we must create) a SAFE non-deliverable distribution for the N-notify live send.
NO writes."""
import os
import oracledb

con = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = con.cursor()

# COMPANY_CONTACT columns (find the email/address-bearing columns)
cur.execute(
    "SELECT column_name FROM all_tab_columns WHERE table_name='COMPANY_CONTACT' ORDER BY column_id"
)
cc_cols = [r[0] for r in cur.fetchall()]
print("COMPANY_CONTACT cols:", ", ".join(cc_cols))

# Per-distribution contact -> contact details (email-ish columns)
print("\n=== distribution -> contact -> address ===")
cur.execute(
    """
    SELECT dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, dsc.COMPANY_CONTACT_ID,
           cc.*
    FROM DISTRIBUTION_SET_CONTACT dsc
    LEFT JOIN COMPANY_CONTACT cc ON cc.COMPANY_CONTACT_ID = dsc.COMPANY_CONTACT_ID
    ORDER BY dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE
    """
)
cols = [d[0] for d in cur.description]
# print only the interesting subset per row
keep = {"DISTRIBUTION_SET_CODE", "RECIPIENT_TYPE", "COMPANY_CONTACT_ID", "NAME",
        "CONTACT_NAME", "EMAIL", "EMAIL_ADDRESS", "E_MAIL", "DELIVERY_ADDRESS",
        "FIRST_NAME", "LAST_NAME", "COMPANY_ID"}
idx = {c: i for i, c in enumerate(cols)}
for r in cur.fetchall():
    parts = []
    for c in cols:
        v = r[idx[c]]
        if v is not None and (c in keep or "MAIL" in c or "EMAIL" in c or "ADDRESS" in c):
            parts.append(f"{c}={str(v)[:46]}")
    print(" | ".join(parts))

# Also dump full COMPANY_CONTACT rows for the contacts referenced, to see ALL columns with values
print("\n=== full COMPANY_CONTACT rows for referenced contacts ===")
cur.execute(
    """
    SELECT cc.* FROM COMPANY_CONTACT cc
    WHERE cc.COMPANY_CONTACT_ID IN (SELECT COMPANY_CONTACT_ID FROM DISTRIBUTION_SET_CONTACT)
    """
)
cols = [d[0] for d in cur.description]
for r in cur.fetchall():
    nonnull = [f"{cols[i]}={str(v)[:40]}" for i, v in enumerate(r) if v is not None]
    print(" ; ".join(nonnull))
    print("-")

con.close()
print("DONE")
