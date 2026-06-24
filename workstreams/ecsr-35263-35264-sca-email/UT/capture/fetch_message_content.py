# -*- coding: utf-8 -*-
"""
Pull the verbatim rendered subject + body (MESSAGE_OUT.MESSAGE_DRAFT) for each report's
generated outgoing message, plus the freetext subject templates. Writes content.json
for build_ut_docs.py (section 11 Preview).

Usage:  EC_DB_USER=ECKERNEL_EC EC_DB_PASS=*** EC_DB_DSN=db.plutodev...:1521/plutodev \
        py fetch_message_content.py
Credentials/DSN are read from env (never hardcoded).
"""
import os, json
import oracledb

DSN  = os.environ.get("EC_DB_DSN", "db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
USER = os.environ.get("EC_DB_USER", "ECKERNEL_EC")
PASS = os.environ.get("EC_DB_PASS", "")

con = oracledb.connect(user=USER, password=PASS, dsn=DSN, tcp_connect_timeout=25)
cur = con.cursor()
out = {}


def latest(where):
    cur.execute(f"""SELECT MESSAGE_NO, SUBJECT, MESSAGE_DRAFT FROM MESSAGE_OUT
                    WHERE {where} ORDER BY MESSAGE_NO DESC FETCH FIRST 1 ROWS ONLY""")
    r = cur.fetchone()
    if not r:
        return None
    body = r[2].read() if hasattr(r[2], "read") else (r[2] or "")
    return {"msg_no": r[0], "subject": r[1], "body": body}


out["pluto"] = latest("SUBJECT LIKE 'Burrup LNG Park Daily Production Report%' "
                       "AND SUBJECT NOT LIKE '%Scarborough%'")
out["sca"]   = latest("SUBJECT LIKE '%Daily Production Report (Scarborough)%'")

dest = os.path.join(os.path.dirname(__file__), "content.json")
open(dest, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items():
    print(k, "-> msg", v["msg_no"] if v else None, ":", (v["subject"] if v else "(none)"))
print("WROTE", dest)
con.close()
