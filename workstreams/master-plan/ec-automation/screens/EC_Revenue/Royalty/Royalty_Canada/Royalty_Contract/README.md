# Royalty Contract - EC Object INSERT+UPDATE-ONLY bundle

**Screen:** EC_Revenue > Royalty > Royalty_Canada > Royalty Contract (BF RC.0059). OV-GM (grid `manageObject:form:T_data`), navigator-GATED,
date-effective. **DELETE IS PERMANENTLY OUT OF SCOPE** - genuine EC product limitation (Contract
Template "Royalty Fixed Percentage Canada" auto-provisions `CNTR_PG_SETUP` child rows this screen's
UI cannot remove), owner-confirmed 2026-08-15, closes Issue #336. See `royalty_contract_sow.md`,
`investigation/ROOT_CAUSE_delete_blocked.md`, and `VERIFY-REPORT.md`.

**Run:**
- Driver: `EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/royalty_contract_iud.py`
- Suite: `robot workstreams/master-plan/ec-automation/tests/EC_Revenue/Royalty/Royalty_Canada/royalty_contract_iud.robot`
- Full verify gate: `py scripts/verify_screen.py --name "Royalty Contract" --t3 workstreams/master-plan/ec-automation/pageobjects/EC_Revenue/Royalty/Royalty_Canada/royalty_contract_page.resource --suite workstreams/master-plan/ec-automation/tests/EC_Revenue/Royalty/Royalty_Canada/royalty_contract_iud.robot --driver workstreams/master-plan/ec-automation/py/royalty_contract_iud.py --out workstreams/master-plan/ec-automation/screens/EC_Revenue/Royalty/Royalty_Canada/Royalty_Contract/VERIFY-REPORT.md`
