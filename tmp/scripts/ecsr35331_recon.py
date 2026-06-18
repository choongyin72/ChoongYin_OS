import os
"""ECSR-35331 read-only recon against ECAASDEV (Pluto PLP dev). Verifies the deployed check-rule /
screen-validation config: which check groups are screen-bound (EC_USER_OBJECT), which rules carry
negative (< 0) / NULL checks, their ZWP_SCREEN_VAL flag, and whether the downstream streams in the
defect are covered. SELECT only. Usage: py tmp/scripts/ecsr35331_recon.py"""
import oracledb

DSN = "dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB"
USER = "ECKERNEL_EC"
PWD = os.environ.get("EC_DB_PWD","")


def main():
    try:
        con = oracledb.connect(user=USER, password=PWD, dsn=DSN, tcp_connect_timeout=20)
    except Exception as e:
        print("CONNECT FAILED:", str(e)[:200])
        return
    cur = con.cursor()
    print("CONNECTED to ECAASDEV /QDB\n")

    def q(sql, args=None):
        try:
            cur.execute(sql, args or [])
            return cur.fetchall()
        except Exception as e:
            print("  query err:", str(e)[:140]); return []

    # 1) check-related tables present
    print("=== [1] CHECK-related tables (ECKERNEL_EC) ===")
    for r in q("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
                  AND table_name LIKE '%CHECK%' ORDER BY table_name"""):
        print("   ", r[0])

    # helper: does a table/column exist?
    def cols(tbl):
        return [c[0] for c in q("""SELECT column_name FROM all_tab_columns
                WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id""", [tbl])]

    # 2) the rule table - discover real name + key columns
    for rt in ("CTRL_CHECK_RULE", "TV_CTRL_CHECK_RULES", "CTRL_CHECK_RULES"):
        c = cols(rt)
        if c:
            print(f"\n=== [2] RULE table = {rt} ===")
            print("    cols:", ", ".join(c))
            n = q(f"SELECT count(*) FROM {rt}")
            print("    rows:", n[0][0] if n else "?")
            RULE_TBL = rt
            RULE_COLS = c
            break
    else:
        RULE_TBL = None

    # 3) the group table
    for gt in ("CTRL_CHECK_GROUP", "TV_CTRL_CHECK_GROUP", "CTRL_CHECK_GROUPS"):
        c = cols(gt)
        if c:
            print(f"\n=== [3] GROUP table = {gt} ===")
            print("    cols:", ", ".join(c))
            GRP_TBL = gt
            GRP_COLS = c
            break
    else:
        GRP_TBL = None

    # 4) screen-bound groups (those with a non-null EC_USER_OBJECT) - the screen wiring
    if GRP_TBL:
        obj_col = next((x for x in GRP_COLS if "USER_OBJECT" in x or x == "EC_USER_OBJECT"), None)
        scrn_col = next((x for x in GRP_COLS if "SCREEN_VAL" in x), None)
        grp_col = next((x for x in GRP_COLS if x in ("CHECK_GROUP", "GROUP_NAME", "CHECK_GROUP_CODE")), GRP_COLS[0])
        print(f"\n=== [4] {GRP_TBL}: groups + screen binding (col={obj_col}, screenval={scrn_col}) ===")
        sel = [grp_col] + [c for c in (obj_col, scrn_col) if c]
        for r in q(f"SELECT {','.join(sel)} FROM {GRP_TBL} ORDER BY {grp_col}"):
            print("   ", " | ".join(str(x)[:90] for x in r))

    # 5) rules with negative / null formula + ZWP_SCREEN_VAL
    if RULE_TBL:
        wf = next((x for x in RULE_COLS if "FORMULA" in x or x == "WHERE_FORMULA"), None)
        sv = next((x for x in RULE_COLS if "SCREEN_VAL" in x), None)
        nm = next((x for x in RULE_COLS if x in ("CHECK_RULE", "RULE_NAME", "CHECK_RULE_CODE", "NAME")), RULE_COLS[0])
        tb = next((x for x in RULE_COLS if x in ("TABLE_ID", "TABLE_NAME", "SOURCE_TABLE", "VIEW_NAME")), None)
        sev = next((x for x in RULE_COLS if "SEVER" in x or x == "MESSAGE_TYPE"), None)
        print(f"\n=== [5] {RULE_TBL}: rules with '< 0' or 'IS NULL' (name={nm}, formula={wf}, screenval={sv}) ===")
        if wf:
            sel = [c for c in (nm, tb, sv, sev) if c]
            rows = q(f"""SELECT {','.join(sel)}, {wf} FROM {RULE_TBL}
                        WHERE UPPER({wf}) LIKE '%< 0%' OR UPPER({wf}) LIKE '%<0%'
                              OR UPPER({wf}) LIKE '%IS NULL%' ORDER BY {nm}""")
            print(f"    matched {len(rows)} rules:")
            for r in rows:
                head = " | ".join(str(x)[:40] for x in r[:-1])
                print(f"   {head}\n        formula: {str(r[-1])[:160]}")

    con.close()
    print("\nDONE (read-only).")


main()
