import re, oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select configuration from tv_ctrl_configuration_storage where name='DefaultScreenTreeview'")
r = cur.fetchone(); cfg = r[0].read() if hasattr(r[0], "read") else r[0]
for lbl, scr in re.findall(r'"label"\s*:\s*"([^"]+)"[^{}]*?"screen"\s*:\s*"([^"]+)"', cfg):
    if lbl == "Area": print(a("Area -> %s" % scr))
cur.execute("select count(*) from ov_area")
print(a("ov_area rows: %d" % cur.fetchone()[0]))
cur.close(); con.close()
