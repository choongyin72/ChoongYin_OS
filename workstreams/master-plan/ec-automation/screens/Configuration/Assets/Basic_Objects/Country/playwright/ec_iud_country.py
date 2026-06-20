"""EC IUD - Country (Playwright reference).
Thin config over the shared engine: ../_shared/iud_engine.py.
See country_sow.md for the screen analysis and README.md for run instructions."""
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUNDLE.parents[0] / "_shared"))
from iud_engine import run_iud

CFG = {
    "slug": "country",
    "label": "Country",
    "code_prefix": "CTRY",
    "table_id": "manage_object_nav_nav:form:T_data",
    "nav": [],
    "ins_code": "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in",
    "ins_name": "tab:tabPanel:objectForm:form:G:0:R:1:C:1:in",
    "ins_date": "tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input",
    "ins_dd": [],
    "upd_code": "tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in",
    "upd_name": "tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in",
    "del_end": "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input",
    "start_date": "2000-01-01",
    "end_date": "2000-01-01",
    "db_view": "OV_COUNTRY",
    "extra_go_after_delete": False,
}

if __name__ == "__main__":
    raise SystemExit(run_iud(CFG, str(BUNDLE)))
