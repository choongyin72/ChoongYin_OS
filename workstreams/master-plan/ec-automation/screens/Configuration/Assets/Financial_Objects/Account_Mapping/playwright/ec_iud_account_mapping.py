"""EC IUD - Account Mapping (Playwright reference).
Thin config over the shared engine in screens/.../Basic_Objects/_shared/.
See account_mapping_sow.md for the screen analysis and README.md for run instructions."""
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUNDLE.parents[1] / "Basic_Objects" / "_shared"))
from iud_engine import run_iud

CFG = {
    "slug": "account_mapping",
    "label": "Account Mapping",
    "code_prefix": "AM",
    "table_id": "manageObject:form:T_data",
    "nav": [],
    "ins_code": "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in",
    "ins_name": "tab:tabPanel:objectForm:form:G:0:R:2:C:1:in",
    "ins_date": "tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input",
    "ins_dd": [('tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd', 'All Line Item Types'), ('tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd', 'Journal Entry'), ('tab:tabPanel:objectForm:form:G:0:R:9:C:1:dd', 'All'), ('tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd', 'Accrual'), ('tab:tabPanel:objectForm:form:G:0:R:12:C:1:dd', 'Credit'), ('tab:tabPanel:objectForm:form:G:0:R:13:C:1:dd', 'Debit General Ledger (40)'), ('tab:tabPanel:objectForm:form:G:0:R:14:C:1:dd', 'Credit General Ledger (50)'), ('tab:tabPanel:objectForm:form:G:0:R:15:C:1:dd', 'Revenue'), ('tab:tabPanel:objectForm:form:G:0:R:16:C:1:dd', 'ACCRUAL CR Acct')],
    "ins_dd_first": [],
    "ins_extra": [],
    "upd_code": "tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in",
    "upd_name": "tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in",
    "del_end": "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input",
    "start_date": "2003-01-01",
    "end_date": "2003-01-01",
    "db_view": "OV_FIN_ACCOUNT_MAPPING",
    "extra_go_after_delete": False,
}

if __name__ == "__main__":
    raise SystemExit(run_iud(CFG, str(BUNDLE)))
