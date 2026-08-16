"""Map the BU linkage for each Dispatching screen's parent objects, so the suite can
pick a navigator BU under which its inserted row will be VISIBLE."""
import os

import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()

def q(sql, **kw):
    try:
        cur.execute(sql, **kw)
        return cur.fetchall()
    except Exception as e:
        return f"ERR {str(e)[:90]}"

print("TRANSPORT SYSTEMS:", q("SELECT code, name, business_unit_code FROM ov_transport_system"))
print("\nPIPELINES (code,name,BU?):")
print(q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_PIPELINE' AND column_name LIKE '%BUSINESS%'"))
print(q("SELECT code, name, business_unit_code FROM ov_pipeline"))
print("\nCONTRACT 'ECP Norway 3P Gas Purchase' BU:")
print(q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_CONTRACT' AND column_name LIKE '%BUSINESS%'"))
print(q("SELECT code, name, business_unit_code FROM ov_contract WHERE name LIKE 'ECP Norway%'"))
print("\nBUSINESS UNITS:", q("SELECT code, name FROM ov_business_unit"))
print("\nNOMINATION POINT BU-ish columns:",
      q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_NOMINATION_POINT' AND (column_name LIKE '%BUSINESS%' OR column_name LIKE '%CONTRACT%')"))
print("\nsample NPs of a contract:",
      q("SELECT code, contract_code FROM ov_nomination_point WHERE ROWNUM <= 5"))
print("\nTRANSPORT ZONE sample:", q("SELECT code, transport_system_code FROM ov_transport_zone WHERE ROWNUM <= 5"))
print("\nDELIVERY STREAM BU columns:",
      q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_DELIVERY_STREAM' AND column_name LIKE '%BUSINESS%'"))
conn.close()
