"""EC IUD - DOA Credit Limit (Playwright reference).
Thin config over the shared engine in screens/.../Basic_Objects/_shared/.
See doa_credit_limit_sow.md for the screen analysis and README.md for run instructions."""
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUNDLE.parents[1] / "Basic_Objects" / "_shared"))
from iud_engine import run_iud

CFG = {
    "slug": "doa_credit_limit",
    "label": "DOA Credit Limit",
    "code_prefix": "DOA",
    "table_id": "manage_object_nav_nav:form:T_data",
    "nav": [],
    "ins_code": "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in",
    "ins_name": "tab:tabPanel:objectForm:form:G:0:R:1:C:1:in",
    "ins_date": "tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input",
    "ins_dd": [],
    "ins_dd_first": ['tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd', 'tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd', 'tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd'],
    "ins_extra": [('tab:tabPanel:objectForm:form:G:0:R:5:C:1:in', '1000', 'text')],
    "upd_code": "tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in",
    "upd_name": "tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in",
    "del_end": "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input",
    "start_date": "2000-01-01",
    "end_date": "2000-01-01",
    "db_view": "OV_DOA_CREDIT_LIMIT",
    "extra_go_after_delete": False,
}

if __name__ == "__main__":
    raise SystemExit(run_iud(CFG, str(BUNDLE)))
