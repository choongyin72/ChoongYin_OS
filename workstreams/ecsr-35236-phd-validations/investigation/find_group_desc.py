"""READ-ONLY: find the display description of the tank PHD check group (V_PHD_TANK_DIP)
and which groups the 8 ECSR-35236 rules belong to, so the Validation Overview tree row
can be located by label. plutodev, read-only."""
import oracledb
con = oracledb.connect(user="ECKERNEL_EC", password="energy",
                       dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
cur = con.cursor()

# groups for each of the 8 rules
names = ("PHD_TANK_DIP_GRS_MASS_VAL1","PHD_TANK_DIP_STD_DENSITY_VAL1","PHD_STRM_ANALYSIS_DENSITY_VAL1",
         "PHD_STRM_ANALYSIS_GCV_VAL1","PHD_PWEL_STATUS_NODATA_BHTEMP","PHD_PWEL_STATUS_NODATA_WHTEMP",
         "PHD_PWEL_STATUS_NODATA_BHPRESS","PHD_PWEL_STATUS_NODATA_WHPRESS")
inlist = ",".join(f"'{n}'" for n in names)
cur.execute(f"""SELECT r.check_name, cc.check_group
                FROM ctrl_check_rules r JOIN ctrl_check_combination cc ON cc.check_id=r.check_id
                WHERE r.check_name IN ({inlist}) ORDER BY r.check_name""")
print("rule -> check_group:")
groups = set()
for nm, g in cur:
    print(f"   {nm} -> {g}"); groups.add(g)

# try to resolve a display description for each group code
print("\ngroup code -> description (search candidate group tables):")
for g in sorted(groups):
    found = False
    for tbl, gcol, dcol in [("CTRL_CHECK_GROUP","CHECK_GROUP","DESCRIPTION"),
                             ("CTRL_CHECK_GROUP","GROUP_NAME","DESCRIPTION"),
                             ("TV_CTRL_CHECK_GROUP","CHECK_GROUP","DESCRIPTION")]:
        try:
            cur.execute(f"SELECT {dcol} FROM {tbl} WHERE {gcol}=:g", [g])
            r = cur.fetchall()
            if r:
                print(f"   {g} -> {[x[0] for x in r]}  (via {tbl}.{dcol})"); found=True; break
        except Exception:
            pass
    if not found:
        print(f"   {g} -> (no description table matched; tree may show the code)")
con.close()
