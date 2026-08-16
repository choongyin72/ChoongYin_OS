"""Path 1 (user-approved): create a guaranteed-non-deliverable distribution for the N-notify live send.
Additive clone of the working FRMW free-text TO contact (FRMW_MHM_RECEIVER_1) -> autotest@example.invalid,
+ AUTOTEST_FREETEXT_INVALID distribution. Transactional: insert -> verify -> COMMIT only if verify passes.
Idempotent: bails if AUTOTEST_FREETEXT_INVALID already exists. Reversible (see rollback in the .sql)."""
import os
import uuid
import oracledb

con = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = con.cursor()

DIST = "AUTOTEST_FREETEXT_INVALID"
CONTACT_CODE = "AUTOTEST_INVALID_RCV"
SAFE_ADDR = "autotest@example.invalid"


def guid():
    return uuid.uuid4().hex.upper()  # 32-char hex, matches EC OBJECT_ID/REC_ID format


# 0) idempotency guard
cur.execute("SELECT COUNT(*) FROM DISTRIBUTION_SET WHERE DISTRIBUTION_SET_CODE=:d", {"d": DIST})
if cur.fetchone()[0]:
    print(f"ALREADY EXISTS: {DIST} — nothing to do.")
    con.close()
    raise SystemExit(0)

# 1) source contact (the working FRMW free-text TO receiver) — show its effective window
cur.execute(
    "SELECT OBJECT_ID, START_DATE, END_DATE FROM COMPANY_CONTACT WHERE OBJECT_CODE='FRMW_MHM_RECEIVER_1'"
)
src_oid, src_start, src_end = cur.fetchone()
print(f"source FRMW_MHM_RECEIVER_1: OBJECT_ID={src_oid} START={src_start} END={src_end}")

new_oid = guid()

# 2) clone COMPANY_CONTACT (change OBJECT_ID, OBJECT_CODE, CREATED_BY, REC_ID only)
cur.execute(
    """
    INSERT INTO COMPANY_CONTACT (OBJECT_ID, OBJECT_CODE, CLASS_NAME, COMPANY_ID, START_DATE,
           END_DATE, CONTACT_GROUP_ID, RECORD_STATUS, CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
    SELECT :oid, :code, CLASS_NAME, COMPANY_ID, START_DATE, END_DATE, CONTACT_GROUP_ID,
           RECORD_STATUS, 'AUTOTEST', SYSDATE, REV_NO, :rec
    FROM COMPANY_CONTACT WHERE OBJECT_ID=:src
    """,
    {"oid": new_oid, "code": CONTACT_CODE, "rec": guid(), "src": src_oid},
)

# 3) clone COMPANY_CONTACT_VERSION (change OBJECT_ID, NAME, DELIVERY_ADDRESS, CREATED_BY, REC_ID only)
cur.execute(
    """
    INSERT INTO COMPANY_CONTACT_VERSION (OBJECT_ID, DAYTIME, END_DATE, NAME, DELIVERY_METHOD,
           DELIVERY_ADDRESS, FUNCTIONAL_AREA_ID, RECORD_STATUS, CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
    SELECT :oid, DAYTIME, END_DATE, :name, DELIVERY_METHOD, :addr, FUNCTIONAL_AREA_ID,
           RECORD_STATUS, 'AUTOTEST', SYSDATE, REV_NO, :rec
    FROM COMPANY_CONTACT_VERSION WHERE OBJECT_ID=:src
    """,
    {"oid": new_oid, "name": "AUTOTEST invalid receiver", "addr": SAFE_ADDR, "rec": guid(), "src": src_oid},
)

# 4) new distribution set (clone functional area from FRMW)
cur.execute(
    """
    INSERT INTO DISTRIBUTION_SET (DISTRIBUTION_SET_CODE, NAME, FUNCTIONAL_AREA_ID, RECORD_STATUS,
           CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
    SELECT :dist, 'AUTOTEST Freetext (non-deliverable)', FUNCTIONAL_AREA_ID, RECORD_STATUS,
           'AUTOTEST', SYSDATE, 0, :rec
    FROM DISTRIBUTION_SET WHERE DISTRIBUTION_SET_CODE='FRMW_DISTR_SET_FREE_TEXT'
    """,
    {"dist": DIST, "rec": guid()},
)

# 5) link contact -> distribution as TO (FORMAT TEXT, mirrors FRMW free-text TO)
cur.execute(
    """
    INSERT INTO DISTRIBUTION_SET_CONTACT (DISTRIBUTION_SET_CODE, COMPANY_CONTACT_ID, RECIPIENT_TYPE,
           FORMAT_CODE, RECORD_STATUS, CREATED_BY, CREATED_DATE, REV_NO, REC_ID)
    VALUES (:dist, :oid, 'TO', 'TEXT', 'P', 'AUTOTEST', SYSDATE, 0, :rec)
    """,
    {"dist": DIST, "oid": new_oid, "rec": guid()},
)

# 6) VERIFY before commit
cur.execute(
    """
    SELECT dsc.DISTRIBUTION_SET_CODE, dsc.RECIPIENT_TYPE, ccv.DELIVERY_ADDRESS, cc.OBJECT_CODE
    FROM DISTRIBUTION_SET_CONTACT dsc
    JOIN COMPANY_CONTACT cc ON cc.OBJECT_ID = dsc.COMPANY_CONTACT_ID
    JOIN COMPANY_CONTACT_VERSION ccv ON ccv.OBJECT_ID = cc.OBJECT_ID
    WHERE dsc.DISTRIBUTION_SET_CODE=:d
    """,
    {"d": DIST},
)
rows = cur.fetchall()
print("VERIFY rows:", rows)
ok = len(rows) == 1 and rows[0][2] == SAFE_ADDR and rows[0][1] == "TO"
if ok:
    con.commit()
    print(f"COMMITTED. {DIST} -> {SAFE_ADDR} (contact {CONTACT_CODE}, OBJECT_ID={new_oid})")
else:
    con.rollback()
    print("VERIFY FAILED -> ROLLED BACK, no changes.")
con.close()
print("DONE")
