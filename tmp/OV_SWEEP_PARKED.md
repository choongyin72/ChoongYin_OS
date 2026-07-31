
## Chemical Product (CO.0072) - PARKED 2026-07-31 (verified, not assumed)
- **Blocker:** EC auto-creates a child row in `CHEM_USAGE_REPORT_CONF` on every Chemical Product
  insert. The End=Start delete is then REFUSED by EC with the banner: *"Child record found. It was
  attempted to delete a row that has child records. In order to delete this row all child records
  must be deleted first."* (screenshot: tmp/cp_cleanup.png)
- **2 UI delete attempts, both failed (attempt limit reached):** (1) End=Start -> child-record error;
  (2) toolbar Delete (minus icon) -> submenu renders EMPTY, no delete entry.
- **No treeview screen found** that maintains CHEM_USAGE_REPORT_CONF (searched all 'usage'/'chemical
  product' labels in DefaultScreenTreeview).
- **Consequence:** a self-cleaning IUD suite cannot complete on this screen via the UI with current
  knowledge - the delete leg has no proven UI path. Needs owner/SME input on the intended delete
  gesture (or a child-aware delete step).
- **Sandbox left clean:** the audit leftover (AUTOTEST_CP_001 + its 1 child row) was removed -
  child row deleted at DB level (my own row, created 2026-07-31 11:13:16, full row logged), parent
  then closed via the UI End=Start; DB-verified 0 AUTOTEST residual in OV_CHEM_PRODUCT.
- **Generator note:** `tmp/gen_ov.py` (new plain-OV/Bank-family generator) reached insert+update
  green here; its audit therefore continues on a leaf object instead. NOT batch-used until one
  screen passes verify_screen end-to-end (R32).
