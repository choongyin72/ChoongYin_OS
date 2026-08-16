#!/usr/bin/env python3
"""READ-ONLY DB recon for Service (CO.2103) - which form values belong to the NAVIGATOR's scope?

Message Group's lesson: an OV-GM row that is saved outside the navigator's scope persists but never lists
in the grid. Service's navigator gates on BUSINESS UNIT (first-available 'EC LNG Norway'), while the form's
mandatory `Contract` dropdown offers 88 options ordered alphabetically - the first ('Albritton 15H-1
Division Order') is unlikely to belong to that BU. Rather than run a live insert and guess at a failure,
ask the DB which contracts/transport systems actually sit under which BU, and how existing SERVICE rows
are linked.
"""
import oracledb


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()


def show(title, sql, args=None, limit=12):
    print(a("\n--- %s ---" % title))
    try:
        cur.execute(sql, args or {})
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print(a("   cols: %s  (%d row(s))" % (cols, len(rows))))
        for r in rows[:limit]:
            print(a("   %s" % (r,)))
    except Exception as e:
        print(a("   ERR %s" % repr(e)[:160]))


show("existing SERVICE rows (what a real row looks like)",
     "select * from ov_service where rownum <= 3")

show("OV_SERVICE column names",
     "select column_name from all_tab_columns where table_name = 'OV_SERVICE' order by column_id",
     limit=40)

show("how many SERVICE rows exist at all", "select count(*) from ov_service")

con.commit()
cur.close()
con.close()
