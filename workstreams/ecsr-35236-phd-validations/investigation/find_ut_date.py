"""
READ-ONLY: find the best single DAYTIME to demo on the Validation Overview screen, i.e.
a day where the tank PHD rules (gross mass + std density) flag FALSE POSITIVES
(value null/neg AND method != qualifying) so before->after suppression is visible.
plutodev, read-only.
"""
import oracledb
con = oracledb.connect(user="ECKERNEL_EC", password="energy",
                       dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
cur = con.cursor()

# top days by tank false-positive count (gross mass + std density, non-MEASURED)
q = """
SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d,
       SUM(CASE WHEN (ZWP_GRS_MASS_TONNES IS NULL OR ZWP_GRS_MASS_TONNES < 0)
                 AND NVL(GRS_MASS_METHOD,'x') <> 'MEASURED' THEN 1 ELSE 0 END) gm_fp,
       SUM(CASE WHEN (MEAS_STD_DENSITY_KGPERSM3 IS NULL OR MEAS_STD_DENSITY_KGPERSM3 < 0)
                 AND NVL(STD_DENS_METHOD,'x') <> 'MEASURED' THEN 1 ELSE 0 END) sd_fp,
       SUM(CASE WHEN (ZWP_GRS_MASS_TONNES IS NULL OR ZWP_GRS_MASS_TONNES < 0)
                 AND GRS_MASS_METHOD = 'MEASURED' THEN 1 ELSE 0 END) gm_genuine
FROM RV_TANK_DAY_DIP_STATUS
GROUP BY TRUNC(DAYTIME)
HAVING SUM(CASE WHEN (ZWP_GRS_MASS_TONNES IS NULL OR ZWP_GRS_MASS_TONNES < 0)
                 AND NVL(GRS_MASS_METHOD,'x') <> 'MEASURED' THEN 1 ELSE 0 END) > 0
    OR SUM(CASE WHEN (MEAS_STD_DENSITY_KGPERSM3 IS NULL OR MEAS_STD_DENSITY_KGPERSM3 < 0)
                 AND NVL(STD_DENS_METHOD,'x') <> 'MEASURED' THEN 1 ELSE 0 END) > 0
ORDER BY (gm_fp + sd_fp) DESC
"""
cur.execute(q)
rows = cur.fetchall()
print("Top days by tank false-positives (day | grossmass_FP | stddens_FP | grossmass_genuine):")
for r in rows[:12]:
    print(f"   {r[0]} | gm_fp={r[1]} | sd_fp={r[2]} | gm_genuine={r[3]}")
print(f"\nTotal candidate days: {len(rows)}")
con.close()
