"""Move the orphaned PFLW registry row (appended at EOF) into the Screens-covered table, right after
the 'Daily Data Status Processes' (N3) row. Idempotent-ish: removes the PFLW row wherever it is, then
re-inserts it after the N3 row."""
PATH = r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\docs\ec_screen_registry.md"
with open(PATH, encoding="utf-8") as f:
    lines = f.readlines()

pflw = [ln for ln in lines if ln.startswith("| Daily Production Flowline, by Flowline |")]
assert len(pflw) == 1, f"expected 1 PFLW row, found {len(pflw)}"
pflw_row = pflw[0]
# remove it from current (EOF) position
lines = [ln for ln in lines if not ln.startswith("| Daily Production Flowline, by Flowline |")]
# find the N3 row index (Daily Data Status Processes) and insert PFLW right after it
idx = next(i for i, ln in enumerate(lines) if ln.startswith("| Daily Data Status Processes |"))
lines.insert(idx + 1, pflw_row)
with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("moved PFLW row to table position", idx + 1, "(after N3 row)")
# verify: row is now immediately after N3 and before the table-ending '---'
print("line after PFLW:", lines[idx + 2][:40].strip())
