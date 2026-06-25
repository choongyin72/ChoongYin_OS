# -*- coding: utf-8 -*-
"""
ECSR-35236 — read-only compare of the PHD check-rule family between COPSDEV/plutodev and ECAASTEST,
keyed by CHECK_NAME (the business code; CHECK_ID is NOT portable across envs). Also dumps the 8 target
rules' WHERE_FORMULA + their ATTRIBUTE variables. Pure recon — never writes.

Credentials are read from ENV (never hardcoded). Set before running:
  EC_DB_DSN        e.g. db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev
  EC_DB_USER       e.g. ECKERNEL_EC
  EC_DB_PASS
  ECAASTEST_DSN    e.g. test.db.non-prod.plp.wde.ecaas.cloud:1521/QDB
  ECAASTEST_USER   e.g. ECKERNEL_EC
  ECAASTEST_PASS   (keep in your shell/scratch only — NEVER commit it)
Run:  py compare_check_rules.py
"""
import os
import oracledb

ENVS = {
    "PLUTODEV":  (os.environ.get("EC_DB_DSN"),     os.environ.get("EC_DB_USER", "ECKERNEL_EC"),     os.environ.get("EC_DB_PASS")),
    "ECAASTEST": (os.environ.get("ECAASTEST_DSN"), os.environ.get("ECAASTEST_USER", "ECKERNEL_EC"), os.environ.get("ECAASTEST_PASS")),
}
TARGET_RULES = [  # the 8 rules in ECSR-35236, by CODE (CHECK_NAME) + Mel's criterion
    ("PHD_TANK_DIP_GRS_MASS_VAL1",     "GRS_MASS_METHOD = 'MEASURED'"),
    ("PHD_TANK_DIP_STD_DENSITY_VAL1",  "STD_DENS_METHOD = 'MEASURED'"),
    ("PHD_STRM_ANALYSIS_DENSITY_VAL1", "STD_DENSITY_METHOD = 'COMP_ANALYSIS'"),
    ("PHD_STRM_ANALYSIS_GCV_VAL1",     "GCV_METHOD = 'COMP_ANALYSIS'"),
    ("PHD_PWEL_STATUS_NODATA_BHTEMP",  "ON_STREAM_HRS > 0"),
    ("PHD_PWEL_STATUS_NODATA_WHTEMP",  "ON_STREAM_HRS > 0"),
    ("PHD_PWEL_STATUS_NODATA_BHPRESS", "ON_STREAM_HRS > 0"),
    ("PHD_PWEL_STATUS_NODATA_WHPRESS", "ON_STREAM_HRS > 0"),
]


def rd(v):
    return (v.read() if hasattr(v, "read") else v)


def conn(env):
    dsn, usr, pw = ENVS[env]
    if not dsn or not pw:
        raise SystemExit(f"Missing env creds for {env} (set its DSN/USER/PASS env vars).")
    return oracledb.connect(user=usr, password=pw, dsn=dsn, tcp_connect_timeout=20)


def load_phd(env):
    cur = conn(env).cursor()
    cur.execute("SELECT CHECK_NAME, CHECK_ID, WHERE_FORMULA, SEVERITY_LEVEL "
                "FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME LIKE 'PHD%'")
    return {nm: (cid, (rd(wf) or "").strip(), sev) for nm, cid, wf, sev in cur.fetchall()}


def main():
    data = {e: load_phd(e) for e in ENVS}
    P, E = data["PLUTODEV"], data["ECAASTEST"]
    names = sorted(set(P) | set(E))
    diff = [n for n in names if n in P and n in E and P[n][1] != E[n][1]]
    print(f"PHD rules: PLUTODEV={len(P)} ECAASTEST={len(E)} union={len(names)}")
    print(f"only PLUTODEV : {[n for n in names if n in P and n not in E]}")
    print(f"only ECAASTEST: {[n for n in names if n in E and n not in P]}")
    print(f"WHERE_FORMULA diffs: {len(diff)} {diff}")
    print("\n=== target rules (by code): current WHERE_FORMULA + variables (plutodev) + Mel's criterion ===")
    cur = conn("PLUTODEV").cursor()
    for code, crit in TARGET_RULES:
        cur.execute("SELECT CHECK_ID, WHERE_FORMULA FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME=:n", [code])
        row = cur.fetchone()
        if not row:
            print(f"\n{code}: (not found in plutodev)"); continue
        cid, wf = row[0], (rd(row[1]) or "").strip()
        cur.execute("SELECT VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE "
                    "FROM TV_CTRL_CHECK_RULE_VARIABLE WHERE CHECK_ID=:c", [cid])
        vars_ = [(v[0], v[1], v[2]) for v in cur.fetchall()]
        print(f"\n{code} (plutodev id {cid})")
        print(f"   WHERE_FORMULA: {wf}")
        print(f"   variables    : {vars_}")
        print(f"   + add criterion: {crit}")


if __name__ == "__main__":
    main()
