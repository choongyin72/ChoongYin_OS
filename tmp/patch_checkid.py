from pathlib import Path
p=Path("workstreams/ecsr-35236-phd-validations/backport-ec14151-4rules/create_ECSR-35236_4rules.sql")
s=p.read_text(encoding="utf-8"); orig=s
# 1) add check_id to the INSERT column list (identical line x4)
s=s.replace("      (check_name, table_id, select_clause, severity_level, check_message, class_obj_validation_ind, where_formula, rev_text)",
            "      (check_id, check_name, table_id, select_clause, severity_level, check_message, class_obj_validation_ind, where_formula, rev_text)")
# 2) prepend the runtime CHECK_ID to each rule's VALUES (unique per rule)
seq="(SELECT NVL(MAX(check_id),0)+1 FROM ctrl_check_rules)"
for name,tbl in [("PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY","RV_STRM_DAY_STREAM_MEAS_GAS"),
                 ("PHD_STREAM_GAS_MEAS_VAL_GCV","RV_STRM_DAY_STREAM_MEAS_GAS"),
                 ("MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS","RV_TANK_DAY_DIP_STATUS"),
                 ("MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS","RV_TANK_DAY_DIP_STATUS")]:
    old=f"VALUES ('{name}', '{tbl}', 'Count(*)', 'ERROR',"
    new=f"VALUES ({seq}, '{name}', '{tbl}', 'Count(*)', 'ERROR',"
    assert old in s, "anchor not found: "+name
    s=s.replace(old,new)
assert s!=orig
p.write_text(s,encoding="utf-8",newline="\n")
print("patched: check_id added to 4 rule INSERTs;", s.count(seq), "seq refs")
