# READ-ONLY: do OUR tank/stream rule names exist on ec14151? (explains why 4 NEW rules were inserted)
import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"); cur=c.cursor()
ours=['PHD_TANK_DIP_GRS_MASS_VAL1','PHD_TANK_DIP_STD_DENSITY_VAL1','PHD_STRM_ANALYSIS_DENSITY_VAL1','PHD_STRM_ANALYSIS_GCV_VAL1']
inl=",".join("'%s'"%n for n in ours)
cur.execute(f"select check_name, check_id, rev_text from ctrl_check_rules where check_name in ({inl}) order by check_name")
found=cur.fetchall()
print("OUR tank/stream rule names present on ec14151:", len(found))
for r in found: print("   ", r)
missing=set(ours)-{r[0] for r in found}
print("MISSING on ec14151:", sorted(missing) if missing else "none")
c.close()
