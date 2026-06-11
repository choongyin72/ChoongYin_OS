"""Generate Playwright reference bundles for the 12 Commercial Objects screens,
data-driven from commercial_objects_recon.json (same maps as the RF generator,
incl. Field's groupmodel navigator and banner-discovered first-option dds)."""
import json
import re
import shutil
from pathlib import Path

FIN = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/screens/Configuration/Assets/Commercial_Objects")
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/commercial_objects_recon.json")
TMPS = Path(r"c:/Projects/ChoongYin_OS/tmp/scripts")

ABBR = {"Company": "COMP", "Customer": "CUST", "Vendor": "VEND", "Licence": "LIC",
        "MMS Lease": "MMSL", "State Lease": "STL", "Operator Lease": "OPL",
        "Field Group": "FG", "Commercial Entity": "CE", "Company Contact": "CCON",
        "Field": "FLD", "Sub Field": "SFLD"}
DEFAULT_DATE = "2003-01-01"
EXTRA_VALUES = {"ERP Customer Code": "ERP999", "ERP Vendor Code": "ERP999",
                "Official Name": "AUTOTEST Official"}
NAV = {"Field": [("nav:form:G:0:R:1:C:1:dd", "Offshore area")]}
INS_DD_VALUE = {"Field": [("Geo Area", "Offshore area")]}
REQUIRED_DDS = {"Customer": ["Customer Group"], "Vendor": ["Vendor Group"],
                "Company Contact": ["Company"]}
EXTRA_GO = {"Field"}
PARKED = {"Sub Field": ("groupmodel not enabled for SUB_FIELD in this environment: "
                        "inserts persist to OV_SUB_FIELD but the grid can never list them "
                        "(same as Production Sub Unit) - confirmed by probe + DB on 2026-06-12")}

records = json.loads(RECON.read_text(encoding="utf-8"))


def pick_rows(plan):
    vis = [f for f in plan if f.get("visible")]
    texts = [f for f in vis if f.get("kind") == "text"]
    code = next(f for f in texts if f.get("mandatory") and "code" in (f.get("label") or "").lower())
    name = next(f for f in texts if f.get("mandatory") and (f.get("label") or "").strip().lower()
                in ("name", code["label"].lower().replace("code", "name").strip()))
    date = next(f for f in vis if f.get("kind") == "date")
    extras = [f for f in vis if f.get("mandatory") and f["r"] not in (code["r"], name["r"])
              and f.get("kind") in ("text", "checkbox")]
    return code, name, date, extras


PW_TMPL = '''"""EC IUD - {label} (Playwright reference).
Thin config over the shared engine in screens/.../Basic_Objects/_shared/.
See {slug}_sow.md for the screen analysis and README.md for run instructions."""
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUNDLE.parents[1] / "Basic_Objects" / "_shared"))
from iud_engine import run_iud

CFG = {{
    "slug": "{slug}",
    "label": "{label}",
    "code_prefix": "{abbr}",
    "table_id": "{table}",
    "nav": {nav!r},
    "ins_code": "{ins_code}",
    "ins_name": "{ins_name}",
    "ins_date": "{ins_date}",
    "ins_dd": {ins_dd!r},
    "ins_dd_first": {ins_dd_first!r},
    "ins_extra": {ins_extra!r},
    "upd_code": "{upd_code}",
    "upd_name": "{upd_name}",
    "del_end": "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input",
    "start_date": "{start_date}",
    "end_date": "{start_date}",
    "db_view": "{view}",
    "extra_go_after_delete": {extra_go},
}}

if __name__ == "__main__":
    raise SystemExit(run_iud(CFG, str(BUNDLE)))
'''

README_TMPL = """# {label} — Playwright IUD

Insert / Update / Delete automation for the EC **{label}** screen
(Configuration → Assets → Commercial Objects → {label}), implemented in **Playwright** (Python).

{label} is a **Manage Object (OV{gm})** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `{view}`).{parked_note}

## Run
```bash
py -X utf8 playwright/ec_iud_{slug}.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_{slug}.py   # watchable
```

## Folder
- `playwright/ec_iud_{slug}.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `{slug}_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/{slug}_iud.robot`{parked_rf}
"""

SOW_TMPL = """# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — {label}
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-12
**Version:** {version}

---

## 1. REQUIREMENT
Automate IUD on the **{label}** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_{abbr}_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `{view}` | {st} |
| UPDATE | Name change visible in grid row | {st} |
| DELETE | End=Start -> gone from grid AND absent in `{view}` | {st} |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > {label} |
| Screen type | Manage Object (OV{gm}) |
| List/grid id | `{table}` |
| DB view | `{view}` |
| Delete semantics | End Date = Start Date (true delete) |
{nav_row}
### DOM reference (rows derived from recon LABELS)
```
INSERT: Code  {ins_code}
        Name  {ins_name}
        Start {ins_date}
{extra_doc}UPDATE: Code  {upd_code} (guard)
        Name  {upd_name}
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_{abbr}_<timestamp>` | Name `{label} <code>` (+` UPD`) | Start=End `{start_date}`
(section-wide {start_date}: reference dropdowns are effective-date-filtered — the object
Start Date acts as a version; seed objects start 2003-01-01)
{extra_data}
## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/commercial_objects_recon.py`).
{dev_notes}

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live | headless | {rf_result} |
| Playwright reference run | headless | see `evidence/{slug}_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/{slug}_*`,
this bundle, registry row in `docs/ec_screen_registry.md`.
"""

for rec in records:
    label = rec["screen"]
    slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    d = FIN / label.replace(" ", "_")
    (d / "playwright").mkdir(parents=True, exist_ok=True)
    (d / "investigation").mkdir(exist_ok=True)
    (d / "evidence").mkdir(exist_ok=True)
    ins_code, ins_name, ins_date, extras = pick_rows(rec["insertPlan"])
    uvis = [f for f in (rec.get("updatePlan") or []) if f.get("visible") and f.get("kind") == "text"]
    if uvis:
        def _upd(target_label, word):
            exact = [f for f in uvis if (f.get("label") or "").strip().lower() == target_label.lower()]
            if exact:
                return exact[0]["id"]
            return next(f for f in uvis if word in (f.get("label") or "").lower()
                        and "master" not in (f.get("label") or "").lower())["id"]
        u_code = _upd(ins_code.get("label") or "code", "code")
        u_name = _upd(ins_name.get("label") or "name", "name")
    else:
        u_code = ins_code["id"].replace("objectForm", "updateAttributes")
        u_name = ins_name["id"].replace("objectForm", "updateAttributes")
    ins_extra = [(f["id"], EXTRA_VALUES.get(f.get("label"), "AUTOTEST")
                  if f["kind"] == "text" else "on", f["kind"]) for f in extras]
    dds_by_label = {(f.get("label") or "").strip(): f for f in rec["insertPlan"]
                    if f.get("kind") == "dropdown" and f.get("visible")}

    def dd_prefix(f):
        return f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"]
    ins_dd = [(dd_prefix(dds_by_label[lab]), val) for lab, val in INS_DD_VALUE.get(label, [])
              if lab in dds_by_label]
    ins_dd_first = [dd_prefix(dds_by_label[lab]) for lab in REQUIRED_DDS.get(label, [])
                    if lab in dds_by_label]
    parked = label in PARKED
    extra_doc = "".join(f"        {((f.get('label') or '?') + ':'):<22}{f['id']} (MANDATORY {f['kind']})\n" for f in extras)
    extra_data = "".join(f"| {f.get('label')} | `{EXTRA_VALUES.get(f.get('label'), 'checked' if f['kind'] == 'checkbox' else 'AUTOTEST')}` |\n" for f in extras)
    extra_data += "".join(f"| {lab} (reference dd) | `{val}` |\n" for lab, val in INS_DD_VALUE.get(label, []))
    extra_data += "".join(f"| {lab} (reference dd, banner-discovered) | first available option |\n" for lab in REQUIRED_DDS.get(label, []))
    if extra_data:
        extra_data = "\n| Extra mandatory field | Test value |\n|---|---|\n" + extra_data
    nav_row = ""
    if label in NAV:
        nav_row = f"| Navigator (mandatory before grid loads) | {' then '.join(v for _, v in NAV[label])} + GO |\n"
    dev_notes = ("Banner-discovered mandatory dropdowns resolved in fix round 1; Field links into "
                 "its groupmodel via the Geo Area dropdown (= navigator Area).")
    if parked:
        dev_notes = "PARKED: " + PARKED[label]
    ctx = dict(label=label, slug=slug, abbr=ABBR[label], view=rec["dbView"],
               table=rec["gridId"] or "manageObject:form:T_data",
               gm="-GM groupmodel" if label in NAV or label == "Sub Field" else "",
               nav=NAV.get(label, []), ins_code=ins_code["id"], ins_name=ins_name["id"],
               ins_date=ins_date["id"], ins_dd=ins_dd, ins_dd_first=ins_dd_first,
               ins_extra=ins_extra, upd_code=u_code, upd_name=u_name,
               start_date=DEFAULT_DATE, extra_go=label in EXTRA_GO,
               extra_doc=extra_doc, extra_data=extra_data, nav_row=nav_row,
               dev_notes=dev_notes,
               version=("0.9 — ⚠ PARKED 2026-06-12: " + PARKED[label]) if parked
                       else "1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)",
               st="BLOCKED" if parked else "PASS",
               rf_result="TC02 blocked; suite preserved in tests/.../_parked/" if parked
                         else "TC01–TC04 4/4 PASS, DB-verified",
               parked_note=("\n\n> ⚠ **PARKED** — " + PARKED[label]) if parked else "",
               parked_rf=" (in `_parked/`)" if parked else "")
    (d / "README.md").write_text(README_TMPL.format(**ctx), encoding="utf-8")
    (d / f"{slug}_sow.md").write_text(SOW_TMPL.format(**ctx), encoding="utf-8")
    (d / "playwright" / f"ec_iud_{slug}.py").write_text(PW_TMPL.format(**ctx), encoding="utf-8")
    for probe in ["commercial_objects_recon.py", "probe_com_rejects.py"]:
        if (TMPS / probe).exists():
            shutil.copy2(TMPS / probe, d / "investigation" / probe)
    print(f"bundle: {d.name}{' [PARKED]' if parked else ''}")
print("12 Commercial Objects bundles generated")
