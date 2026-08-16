#!/usr/bin/env python3
"""READ-ONLY: which Business Unit / Contract Area owns the contract that existing SERVICE rows use?

The navigator gates on Business Unit -> Contract Area -> Contract, and OV_SERVICE links to a CONTRACT (it
has no BU column). The first-available BU ('EC LNG Norway') has an EMPTY Contract Area child, so it owns no
contracts - a Service row could never list there. All 43 existing rows use contract TS3_GTA_SHP_A, so the
nav scope that actually shows data is whichever BU owns that contract. Finder-first: pick a scope that has
data instead of the alphabetically-first one."""
import oracledb


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()


def q(title, sql, limit=10):
    print(a("\n--- %s ---" % title))
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print(a("   %s" % cols))
        for r in rows[:limit]:
            print(a("   %s" % (r,)))
        return rows
    except Exception as e:
        print(a("   ERR %s" % repr(e)[:150]))
        return []


q("contract TS3_GTA_SHP_A - its area / BU columns",
  """select column_name from all_tab_columns where table_name = 'OV_CONTRACT'
     and (column_name like '%AREA%' or column_name like '%BUSINESS%' or column_name like '%BU%')
     order by column_id""", 20)

q("the contract row itself (area/BU fields)",
  """select code, name, contract_area_id, contract_area_code from ov_contract
     where code = 'TS3_GTA_SHP_A'""")

q("that contract area -> which BU?",
  """select ca.code, ca.name, ca.business_unit_id, ca.business_unit_code
     from ov_contract_area ca
     where ca.object_id = (select contract_area_id from ov_contract where code = 'TS3_GTA_SHP_A')""")

q("distinct contracts used by existing SERVICE rows",
  """select contract_code, count(*) from ov_service group by contract_code order by 2 desc""")

cur.close()
con.close()
