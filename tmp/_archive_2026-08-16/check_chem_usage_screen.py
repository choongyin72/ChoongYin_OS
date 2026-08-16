#!/usr/bin/env python3
"""ITEM 9: EC_KNOWN_ISSUES.md:216 says the blocking child is removable "via the Chemical Usage Report
config screen". My earlier treeview search found no screen for CHEM_USAGE_REPORT_CONF. Settle it against
the treeview JSON + class config - read-only."""
import json
import re
import oracledb

def a(s): return str(s).encode("ascii", "replace").decode("ascii")

con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select configuration from tv_ctrl_configuration_storage where name = 'DefaultScreenTreeview'")
row = cur.fetchone()
cfg = row[0].read() if hasattr(row[0], "read") else row[0]

pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^{}]*?"screen"\s*:\s*"([^"]+)"', cfg)
print(a("treeview entries parsed: %d" % len(pairs)))
for kw in ("usage", "chemical report", "chem usage", "reporting"):
    hits = [(l, s) for l, s in pairs if kw in l.lower()]
    print(a("  label contains %-16r -> %s" % (kw, hits[:6] if hits else "NONE")))

print(a("\nany treeview label mentioning 'Chemical':"))
for l, s in sorted({(l, s) for l, s in pairs if "chemical" in l.lower()}):
    print(a("   %-42s %s" % (l, s)))

cur.execute("""select class_name, class_type from class_cnfg
               where class_name like '%USAGE%' or class_name like '%CHEM%REPORT%'""")
print(a("\nclass_cnfg rows for USAGE / CHEM*REPORT:"))
for r in cur.fetchall():
    print(a("   %-34s %s" % r))
cur.close(); con.close()
