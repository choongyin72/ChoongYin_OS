
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

### Chemical Product - CLASSIFICATION CORRECTED 2026-07-31: EC PRODUCT DEFECT (already diagnosed)
**This was already fully diagnosed in `ec-ui-knowledge/EC_KNOWN_ISSUES.md` lines 202-219.** I wrongly
re-investigated it and framed it as "needs owner/SME input on the intended gesture". It is not an
unknown-gesture problem - it is a **product defect**, and the KB says so with deeper evidence than my
re-scan produced:
- `CHEM_PRODUCT` is VERSIONED, but the zero-length close is blocked by a child FK:
  `ORA-02292: integrity constraint (ECKERNEL_EC.FK_CHEM_USAGE_REPORT_CONF_1) violated - child record found`
  (child delete rule NO ACTION), and the `IUD_CHEM_PRODUCT` trigger raises
  `ORA-20102: Object delete is not allowed, set object end date`.
- **THE DEFECT: the web UI SWALLOWS BOTH ERRORS.** End Date fills, Save clicks, `ec_error` = '' (no
  banner at all), yet `OV_CHEM_PRODUCT.OBJECT_END_DATE` stays NULL and the object remains in the view.
  A silent no-op that reports success = product defect, same class as ECSR-35448 -> route ECPD if raised.
- `CHEM_PRODUCT` is referenced by 18 FKs, so any clean delete must remove auto-created children first.
- KB remedy: remove the child config row(s) then End=Start; the generic engine
  (`py/ec_object_iud.py` `closeObjectRecord`) is NOT child-aware and would need extending.

**One open discrepancy to resolve before anyone acts on the remedy** (flagging, not picking a side):
KNOWN_ISSUES line 216 says the child is removable "via the Chemical Usage Report config screen", but my
DefaultScreenTreeview search for CHEM*/USAGE*/REPORT* found no screen maintaining
`CHEM_USAGE_REPORT_CONF` (a TABLE-class object). One of those two statements is wrong - [UNCONFIRMED],
must be verified before the delete leg is automated.

**Status: stays PARKED as a product-defect blocker, not as a missing-knowledge blocker.** No owner
question outstanding.

**Process lesson:** the EC-UI read-first rule exists exactly for this - read EC_KNOWN_ISSUES.md BEFORE
diagnosing. Three fresh scans (End=Start, toolbar Delete, Manage Chemical Product CO.0261) rediscovered
a thinner version of what was already on disk. Screenshots kept anyway: tmp/cp_cleanup.png,
tmp/manage_chem_product.png.

## Message Group (CO.0236) - PARKED 2026-07-31 (owner decision; verified, not assumed)
- **Family: genuinely OV-GM** (proven live, not inherited): navigator = Date + ONE mandatory dropdown
  `Functional Area` at `nav:form:G:0:R:1:C:1:dd` + GO `button:form:B`; grid `manageObject:form:T_data`;
  treeview Configuration > Messaging > Message Group. Mandatory insert fields: Message Group Code,
  Start Date, Name, Functional Area (dd). End Date optional.
- **Blocker: the insert PERSISTS but lands in the WRONG SCOPE, so the grid cannot list it.**
  `db.code_present('OV_MESSAGE_GROUP', 'AUTOTEST_MG001')` = True after Save, yet
  `wait_for_row` never sees it.
- **NOT the documented groupmodel-off case** (my first read, corrected): the persisted row's
  `FUNCTIONAL_AREA_CODE` is **ALLOCATION** while the navigator's captured scope is **Administration**.
- **Read-only probe (tmp/probe_mg_fa_options.py, nothing saved):** the navigator panel and the objectForm
  panel offer IDENTICAL option lists - `['Administration', 'Allocation', 'Billing', ...]` - with
  `Administration` FIRST and `Allocation` SECOND. So the requested value is option 1 and the persisted
  value is option 2.
- **Two candidate causes, NOT yet distinguished (no evidence either way - do not treat as decided):**
  1. the dropdown pick lands one row off in this panel shape; or
  2. the dropdown write silently fails and EC saves a default of `Allocation`. (`insert_ui` PASSing only
     means EC raised no error - it is not proof the dropdown took.)
- **Why it stopped here:** 2 fix attempts used (bind the form dd to the captured nav value via the new
  `parent_dd` key; then re-run) - both landed in ALLOCATION. The suspect code
  (`select_dropdown` / `Fill OV Dropdown By Label`) is in the SHARED engine used by all 22 OV-GM screens,
  so changing it needs the shared-file protocol (backup + canary + random sibling), not a fix inside a
  screen build. **POSSIBLE WIDER IMPACT: if cause (1) is real, other OV-GM screens may have been writing
  a NEIGHBOURING dropdown value all along - their assertions only check CODE and NAME, never the parent
  dropdown.** Owner deferred this investigation; recorded so it is not lost.
- **Sandbox left clean:** 3 rows my runs persisted (AUTOTEST_MG001 x2, AUTOTEST_MG20260731221346) closed
  via End Date = Start Date through `OV_MESSAGE_GROUP` (full row logged first, 1 row per statement);
  re-read shows **0 open AUTOTEST rows**.
- **Bundle removed** (driver/T3/suite/screens dir): verify_screen FAILed, so the packager never ran and
  no registry/scorecard/screen_families row exists. Kept: tmp/cfg_message_group.json,
  tmp/recon_mg_nav.py, tmp/probe_mg_fa_options.py, tmp/selfclean_message_group.py so a resume is cheap.
