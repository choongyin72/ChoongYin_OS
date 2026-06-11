"""EC IUD - Field (Playwright reference).
Thin config over the shared engine in screens/.../Basic_Objects/_shared/.
See field_sow.md for the screen analysis and README.md for run instructions."""
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUNDLE.parents[1] / "Basic_Objects" / "_shared"))
from iud_engine import run_iud

CFG = {
    "slug": "field",
    "label": "Field",
    "code_prefix": "FLD",
    "table_id": "manageObject:form:T_data",
    "nav": [('nav:form:G:0:R:1:C:1:dd', 'Offshore area')],
    "ins_code": "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in",
    "ins_name": "tab:tabPanel:objectForm:form:G:0:R:1:C:1:in",
    "ins_date": "tab:tabPanel:objectForm:form:G:0:R:6:C:1:da_input",
    "ins_dd": [('tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd', 'Offshore area')],
    "ins_dd_first": [],
    "ins_extra": [],
    "upd_code": "tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in",
    "upd_name": "tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in",
    "del_end": "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input",
    "start_date": "2003-01-01",
    "end_date": "2003-01-01",
    "db_view": "OV_FIELD",
    "extra_go_after_delete": True,
}

if __name__ == "__main__":
    raise SystemExit(run_iud(CFG, str(BUNDLE)))
