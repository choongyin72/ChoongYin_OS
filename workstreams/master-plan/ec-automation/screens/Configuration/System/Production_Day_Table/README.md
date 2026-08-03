# Production Day Table - EC Object IUD bundle

**Screen:** Configuration > System > Production Day Table (BF CO.1033). TV-style inline-editable
grid, no navigator. **INSERT ONLY** - Update and Delete are permanently out of scope by design
(owner-confirmed live 2026-08-03: no deletion allowed on this screen; End Date is a plain data
field here, not a delete trigger). **Self-clean is impossible** - every run permanently accumulates
one test row (owner-accepted, see `production_day_table_sow.md` §3). See `JOURNAL.md` for the full
root-cause chain (cell-fill method + DB commit latency + an RF argument-passing gotcha).
Driver `py/production_day_table_iud.py`; T3/suite under `Configuration/System`.
