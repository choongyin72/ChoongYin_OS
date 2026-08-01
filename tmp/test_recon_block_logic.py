"""Unit-test the recon_nav_block branch logic in isolation, without a live gate cycle."""
import re
src = open(r"tmp/package_ovgm.py", encoding="utf-8").read()
# extract just the recon_nav_block assignment block
m = re.search(r"_nav_value_cfg = a\.get.*?else:\n    recon_nav_block = \"    pu = ec\.apply_ovgm_navigator\(pg\)\"", src, re.S)
assert m, "recon_nav_block logic not found"
ns = {"a": {}, "nav_mode": ""}
exec(m.group(0), ns)
print("old-style (no nav_value/nav_values/go_only):")
print(" ", ns["recon_nav_block"])
assert ns["recon_nav_block"] == "    pu = ec.apply_ovgm_navigator(pg)"

ns2 = {"a": {"nav_value": "TS3 BU1"}, "nav_mode": ""}
exec(m.group(0), ns2)
print("\nnav_value:")
print(" ", ns2["recon_nav_block"])
assert "select_dropdown" in ns2["recon_nav_block"] and "TS3 BU1" in ns2["recon_nav_block"]

ns3 = {"a": {"nav_values": ["A", "B", "C"]}, "nav_mode": ""}
exec(m.group(0), ns3)
print("\nnav_values:")
print(" ", ns3["recon_nav_block"])
assert ns3["recon_nav_block"].count("select_dropdown") == 3

ns4 = {"a": {}, "nav_mode": "go_only"}
exec(m.group(0), ns4)
print("\ngo_only:")
print(" ", ns4["recon_nav_block"])
assert "click_go" in ns4["recon_nav_block"] and "pu = None" in ns4["recon_nav_block"]
print("\nALL 4 BRANCHES CORRECT")
