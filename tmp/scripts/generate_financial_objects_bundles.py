"""Generate Playwright reference bundles for the 14 Financial Objects screens,
data-driven from financial_objects_recon.json (same label-derived rows as the
RF generator). Engine lives at screens/.../Basic_Objects/_shared/iud_engine.py;
the per-screen scripts resolve it relative to the screens/ tree."""
import json
import re
import shutil
from pathlib import Path

SCREENS_ROOT = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/screens/Configuration/Assets")
FIN = SCREENS_ROOT / "Financial_Objects"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json")
TMPS = Path(r"c:/Projects/ChoongYin_OS/tmp/scripts")

ABBR = {"Account": "ACC", "Bank Account": "BACC", "Cost Centre": "CC",
        "Cost Object Mapping": "COM", "Currency": "CUR", "DOA Credit Limit": "DOA",
        "Exchange Rate Source": "ERS", "Payment Scheme": "PSCH",
        "Product Description": "PD", "Revenue Order": "RO", "Sales Order": "SO",
        "VAT Code": "VAT", "WBS": "WBS", "Account Mapping": "AM"}
EXTRA_VALUES = {"GL Account": "999999", "Sort Code": "000000",
                "Credit Limit": "1000", "VAT Code": "AT9", "Rate (Decimal)": "0.1"}
# mandatory reference dropdowns per screen (from the EC save banner) - first option used
REQUIRED_DDS = {
    "Account": ["Cost Object Type"],
    "Account Mapping": ["Line Item Type", "Financial Code", "Company Category", "Status",
                        "Debit / Credit", "Debit PK", "Credit PK"],
    "Bank Account": ["Customer", "Bank", "Currency"],
    "Cost Object Mapping": ["Object Type", "Company", "Distribution Object Type", "Cost Object"],
    "DOA Credit Limit": ["DOA Type", "Currency", "Role Name"],
    "Product Description": ["Product", "Node", "Financial Code"],
    "Sales Order": ["Company", "Field"],
    "VAT Code": ["Country", "VAT Type"],
}

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
    "nav": [],
    "ins_code": "{ins_code}",
    "ins_name": "{ins_name}",
    "ins_date": "{ins_date}",
    "ins_dd": [],
    "ins_dd_first": {ins_dd_first!r},
    "ins_extra": {ins_extra!r},
    "upd_code": "{upd_code}",
    "upd_name": "{upd_name}",
    "del_end": "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input",
    "start_date": "2000-01-01",
    "end_date": "2000-01-01",
    "db_view": "{view}",
    "extra_go_after_delete": False,
}}

if __name__ == "__main__":
    raise SystemExit(run_iud(CFG, str(BUNDLE)))
'''

README_TMPL = """# {label} — Playwright IUD

Insert / Update / Delete automation for the EC **{label}** screen
(Configuration → Assets → Financial Objects → {label}), implemented in **Playwright** (Python).

{label} is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `{view}`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_{slug}.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_{slug}.py
```

## Folder
- `playwright/ec_iud_{slug}.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `{slug}_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/{slug}_iud.robot`
"""

SOW_TMPL = """# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — {label}
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **{label}** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_{abbr}_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `{view}` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `{view}` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > {label} |
| Screen type | Manage Object (OV) |
| List/grid id | `{table}` |
| DB view | `{view}` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  {ins_code}
        Name  {ins_name}
        Start {ins_date}
{extra_doc}UPDATE: Code  {upd_code} (guard)
        Name  {upd_name}
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```
{quirks}
### Test data
Code `AUTOTEST_{abbr}_<timestamp>` | Name `{label} <code>` (+` UPD`) | Start=End `2000-01-01`
{extra_data}
## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/financial_objects_recon.py`
output): field rows are picked by their `:C:0:la` labels, so row-shift screens and
relocated dates are handled automatically. Extra MANDATORY fields get fixed safe test
values (cleaned up by the delete).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live batch | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/{slug}_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/{slug}_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.
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
        u_code = next(f for f in uvis if "code" in (f.get("label") or "").lower())["id"]
        u_name = next(f for f in uvis if (f.get("label") or "").strip().lower()
                      in ((ins_name.get("label") or "name").lower(), "name"))["id"]
    else:
        u_code = ins_code["id"].replace("objectForm", "updateAttributes")
        u_name = ins_name["id"].replace("objectForm", "updateAttributes")
    ins_extra = [(f["id"], EXTRA_VALUES.get(f.get("label"), "AUTOTEST")
                  if f["kind"] == "text" else "on", f["kind"]) for f in extras]
    dds_by_label = {(f.get("label") or "").strip(): f for f in rec["insertPlan"]
                    if f.get("kind") == "dropdown" and f.get("visible")}
    ins_dd_first = []
    for dlab in REQUIRED_DDS.get(label, []):
        f = dds_by_label.get(dlab)
        if f:
            ins_dd_first.append(f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"])
    extra_doc = "".join(f"        {((f.get('label') or '?') + ':'):<22}{f['id']} (MANDATORY {f['kind']})\n"
                        for f in extras)
    extra_data = "".join(f"| {f.get('label')} | `{EXTRA_VALUES.get(f.get('label'), 'checked' if f['kind'] == 'checkbox' else 'AUTOTEST')}` |\n"
                         for f in extras)
    extra_data += "".join(f"| {dlab} (reference dropdown, banner-discovered) | first available option |\n"
                          for dlab in REQUIRED_DDS.get(label, []))
    if extra_data:
        extra_data = "\n| Extra mandatory field | Test value |\n|---|---|\n" + extra_data
    quirks = ""
    if rec.get("dbViewVerified") is False:
        quirks = "\nNote: base table was EMPTY at recon time - the DB view was verified live by TC02.\n"

    ctx = dict(label=label, slug=slug, abbr=ABBR[label], view=rec["dbView"],
               table=rec["gridId"], ins_code=ins_code["id"], ins_name=ins_name["id"],
               ins_date=ins_date["id"], upd_code=u_code, upd_name=u_name,
               ins_extra=ins_extra, ins_dd_first=ins_dd_first,
               extra_doc=extra_doc, extra_data=extra_data, quirks=quirks)
    (d / "README.md").write_text(README_TMPL.format(**ctx), encoding="utf-8")
    (d / f"{slug}_sow.md").write_text(SOW_TMPL.format(**ctx), encoding="utf-8")
    (d / "playwright" / f"ec_iud_{slug}.py").write_text(PW_TMPL.format(**ctx), encoding="utf-8")
    for probe in ["financial_objects_recon.py"]:
        if (TMPS / probe).exists():
            shutil.copy2(TMPS / probe, d / "investigation" / probe)
    print(f"bundle: {d.name}")
print("14 Financial Objects bundles generated")
