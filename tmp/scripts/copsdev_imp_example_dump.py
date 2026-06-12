"""READ-ONLY: dump the COMPLETE ZWP_INTERIM_DATA_UPLOAD example from COPSDEV
(source mappings + paths + target mappings) + scheduler links + save full JSON
for the deep-dive doc."""
import json
import oracledb
from pathlib import Path

OUT = Path(r"c:/Projects/ChoongYin_OS/DeepDiveLearnings/ecis-deep-dive/copsdev_examples.json")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev",
                        tcp_connect_timeout=20)
cur = conn.cursor()


def q(sql, **kw):
    cur.execute(sql, kw)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


result = {}
ifaces = q("SELECT OBJECT_ID, OBJECT_CODE, NAME, TYPE, TRANSACTION_TYPE, EC_DATA_LEVEL, "
           "EC_VALID_LEVEL, STAGING_VALIDATION_IND, PRE_STAGING_UE_TYPE, PRE_STAGING_UE_PATH, "
           "POST_STAGING_UE_TYPE, POST_STAGING_UE_PATH, PRE_TARGET_UE_TYPE, PRE_TARGET_UE_PATH, "
           "POST_TARGET_UE_TYPE, POST_TARGET_UE_PATH FROM IMP_SOURCE_INTERFACE")
for it in ifaces:
    iid = it["OBJECT_ID"]
    sm = q("SELECT OBJECT_ID, CODE, NAME, SORT_ORDER, PATH_ORIGIN, TYPE, VALUE_TYPE, "
           "STAGING_GROUP, EC_KEY, KEY_1, KEY_2, KEY_3, NAVIGATION_METHOD "
           "FROM IMP_SOURCE_MAPPING WHERE IMP_SOURCE_INTERFACE_ID = :i ORDER BY SORT_ORDER", i=iid)
    for m in sm:
        m["paths"] = q("SELECT SORT_ORDER, TYPE, PATH, PATH_PARAM_1, PATH_PARAM_2, PATH_PARAM_3 "
                       "FROM IMP_SOURCE_PATH WHERE IMP_SOURCE_MAPPING_ID = :m ORDER BY SORT_ORDER",
                       m=m["OBJECT_ID"])
    tm = q("SELECT EC_KEY, CLASS, ATTRIBUTE, CLASS_KEY_1, CLASS_KEY_2, CLASS_KEY_3, "
           "CONSTANT_STRING_VALUE, CONSTANT_NUMBER_VALUE, FROM_UNIT, TO_UNIT "
           "FROM IMP_TARGET_MAPPING WHERE IMP_SOURCE_INTERFACE_ID = :i", i=iid)
    result[it["OBJECT_CODE"]] = {"interface": it, "source_mappings": sm, "target_mappings": tm}
    print(f"{it['OBJECT_CODE']:28s} src_mappings={len(sm)} target_mappings={len(tm)}")

# print the ZWP_INTERIM_DATA_UPLOAD in detail (compact)
ex = result.get("ZWP_INTERIM_DATA_UPLOAD")
if ex:
    print("\n===== ZWP_INTERIM_DATA_UPLOAD detail =====")
    for m in ex["source_mappings"][:12]:
        print(f"  SRC {m['SORT_ORDER']} {m['CODE']:24s} type={m['TYPE']:9s} vtype={str(m['VALUE_TYPE']):7s} "
              f"origin={str(m['PATH_ORIGIN']):16s} eckey={m['EC_KEY']}")
        for p in m["paths"]:
            print(f"      path {p['SORT_ORDER']} {p['TYPE']:11s} {str(p['PATH']):15s} "
                  f"({p['PATH_PARAM_1']}, {p['PATH_PARAM_2']})")
    for t in ex["target_mappings"][:12]:
        print(f"  TGT {t['EC_KEY']:24s} -> {t['CLASS']}.{t['ATTRIBUTE']} keys=({t['CLASS_KEY_1']},{t['CLASS_KEY_2']}) "
              f"const={t['CONSTANT_STRING_VALUE'] or t['CONSTANT_NUMBER_VALUE'] or ''}")

# schedules / business actions referencing ECIS or import
print("\n===== schedules with ECIS/import flavour =====")
try:
    tabs = q("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND "
             "(table_name LIKE 'CTRL_SCHEDUL%' OR table_name LIKE '%BUSINESS_ACTION%' OR table_name LIKE 'CTRL_BA%')")
    print("  candidate tables:", [t["TABLE_NAME"] for t in tabs])
except Exception as e:
    print("  ERR", str(e)[:100])

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=1, default=str), encoding="utf-8")
print("->", OUT)
cur.close()
conn.close()
