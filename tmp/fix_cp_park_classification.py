from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\OV_SWEEP_PARKED.md")
src = p.read_text(encoding="utf-8")
i = src.index("### Chemical Product - item-4 follow-up investigation")
src = src[:i] + '''### Chemical Product - CLASSIFICATION CORRECTED 2026-07-31: EC PRODUCT DEFECT (already diagnosed)
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
'''
p.write_text(src, encoding="utf-8")
print("park entry reclassified as product defect")
