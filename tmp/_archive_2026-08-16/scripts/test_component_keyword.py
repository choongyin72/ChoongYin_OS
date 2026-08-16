"""Read-only smoke test of the new DbVerify component keyword against live DB state."""
import os
import sys
sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\libraries")
os.environ.setdefault("EC_DB_DSN", "localhost:1521/ORCL")
import DbVerify as d

V = "DV_STRM_COMP_ANALYSIS"
OID = "96D7FD4F6CB90217E053020011AC1940"
DATE = "2011-11-01"
print("C1 MOL_PCT =", d.component_value(V, OID, DATE, "C1", "MOL_PCT"))
print("C2 MOL_PCT =", d.component_value(V, OID, DATE, "C2", "MOL_PCT"))
# positive asserts (current truth)
d.component_value_should_be(V, OID, DATE, "C1", "MOL_PCT", 70.68)
d.component_value_should_be(V, OID, DATE, "C2", "MOL_PCT", 14.14)
print("PASS: positive asserts (C1=70.68, C2=14.14)")
# negative assert must raise
try:
    d.component_value_should_be(V, OID, DATE, "C1", "MOL_PCT", 99.99)
    print("FAIL: expected AssertionError for wrong value")
except AssertionError as e:
    print("PASS: negative assert raised ->", str(e)[:70])
print("DONE")
