"""Generate Commercial Objects RF artifacts (12 screens), data-driven from
commercial_objects_recon.json. Same method as Financial Objects plus optional
groupmodel NAV support (Field). Section default Start Date = 2003-01-01
(reference dropdowns are effective-date-filtered)."""
import json
import re
from pathlib import Path

BASE = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation")
PO_DIR = BASE / "pageobjects/Configuration/Assets/Commercial_Objects"
TEST_DIR = BASE / "tests/Configuration/Assets/Commercial_Objects"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/commercial_objects_recon.json")
PO_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

ABBR = {"Company": "COMP", "Customer": "CUST", "Vendor": "VEND", "Licence": "LIC",
        "MMS Lease": "MMSL", "State Lease": "STL", "Operator Lease": "OPL",
        "Field Group": "FG", "Commercial Entity": "CE", "Company Contact": "CCON",
        "Field": "FLD", "Sub Field": "SFLD"}
DEFAULT_DATE = "2003-01-01"   # section-wide: reference dds are date-filtered
EXTRA_VALUES = {"ERP Customer Code": "ERP999", "ERP Vendor Code": "ERP999",
                "Official Name": "AUTOTEST Official"}
# groupmodel navigator selections (value chosen per announced fallback:
# 'Offshore area' = the user-approved Sub Area context)
NAV = {"Field": [("nav:form:G:0:R:1:C:1:dd", "Offshore area")]}
# insert dds selected BY VALUE (exact label match via normalize-space)
INS_DD_VALUE = {"Field": [("Geo Area", "Offshore area")]}
# insert dds selected FIRST-OPTION (banner-discovered; grows during fix rounds)
REQUIRED_DDS = {"Customer": ["Customer Group"], "Vendor": ["Vendor Group"],
                "Company Contact": ["Company"]}
EXTRA_GO = {"Field"}   # versioned groupmodel grids redraw lazily after delete

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


PAGE_TMPL = """*** Settings ***
Documentation       T3 (screen) — {label} page object.
...                 Screen: Configuration > Assets > Commercial Objects > {label}.
...                 Manage-Object (OV{gm}) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{UP}_SCREEN}}    {label}
${{{UP}_TABLE}}    {table}
{nav_vars}# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${{{UP}_INS_CODE}}    {ins_code}
${{{UP}_INS_NAME}}    {ins_name}
${{{UP}_INS_DATE}}    {ins_date}
{extra_vars}# updateAttributes field IDs (Update — existing object)
${{{UP}_UPD_CODE}}    {upd_code}
${{{UP}_UPD_NAME}}    {upd_name}
# objectdates field ID (Delete — End Date = Start Date)
${{{UP}_DEL_ENDDATE}}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open {label} Screen
    [Documentation]    Suite Setup: launch, login, navigate to the {label} screen{nav_doc}.
    [Arguments]    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Open EC Browser
    Login To EC    ${{user}}    ${{pass}}
    Navigate To Screen    ${{{UP}_SCREEN}}
{nav_steps}
{label} Row Should Exist
    [Documentation]    Assert a {lower} with ${{code}} is present in the list.
    [Arguments]    ${{code}}
    Row Should Exist    ${{{UP}_TABLE}}    ${{code}}

{label} Row Should Not Exist
    [Documentation]    Assert a {lower} with ${{code}} is absent from the list.
    [Arguments]    ${{code}}
    Row Should Not Exist    ${{{UP}_TABLE}}    ${{code}}

{label} Should Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} really persisted in {view}.
    [Arguments]    ${{code}}
    Code Should Be Present In View    {view}    ${{code}}

{label} Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} was truly deleted from {view}.
    [Arguments]    ${{code}}
    Code Should Be Absent In View    {view}    ${{code}}

{label} Row Should Show Name
    [Documentation]    Assert the {label} row for ${{code}} displays ${{name}}.
    [Arguments]    ${{code}}    ${{name}}
    Object Row Should Show Name    ${{{UP}_TABLE}}    ${{code}}    ${{name}}

Insert {label} Record
    [Documentation]    Insert a new {lower}: Code/Name/Start Date{extra_doc} -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}
    Fill New Object Form    ${{{UP}_INS_CODE}}    ${{{UP}_INS_NAME}}    ${{{UP}_INS_DATE}}
    ...    ${{code}}    ${{name}}    ${{start_date}}
{extra_fill}    Save And Refresh List

Update {label} Name
    [Documentation]    Select the {lower}, edit Name, save + reload.
    [Arguments]    ${{code}}    ${{new_name}}
    Update Object Name    ${{{UP}_TABLE}}    ${{{UP}_UPD_CODE}}    ${{{UP}_UPD_NAME}}    ${{code}}    ${{new_name}}

Delete {label}
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${{code}}    ${{date}}
    Delete Object Via End Date    ${{{UP}_TABLE}}    ${{{UP}_DEL_ENDDATE}}    ${{code}}    ${{date}}
{extra_del}"""

TEST_TMPL = """*** Settings ***
Documentation       EC IUD Test - {label} (Configuration > Assets > Commercial Objects > {label}).
...                 Manage-Object (OV{gm}) screen. DELETE = End Date = Start Date (true delete in {view}).
...                 NEVER touch existing data. A unique AUTOTEST_{abbr}_<timestamp> code is generated
...                 per run. Section Start Date {start_date}: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/{slug}_page.resource

Suite Setup         Set Up {label} Suite
Suite Teardown      Close EC

Test Tags           iud    {tag}


*** Variables ***
${{TEST_CODE}}        ${{EMPTY}}
${{OBJ_NAME}}         ${{EMPTY}}
${{OBJ_NAME_UPD}}     ${{EMPTY}}
${{START_DATE}}       {start_date}
${{END_DATE}}         {start_date}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test {lower} does not exist before inserting.
    [Tags]    clean-state
    {label} Row Should Not Exist    ${{TEST_CODE}}
    Capture Step    {slug}_tc01_clean

TC02 Insert New {label}
    [Documentation]    Insert a new {lower} and confirm it appears in the list.
    [Tags]    insert
    Insert {label} Record    ${{TEST_CODE}}    ${{OBJ_NAME}}    ${{START_DATE}}
    {label} Row Should Exist    ${{TEST_CODE}}
    {label} Should Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc02_inserted

TC03 Update {label} Name
    [Documentation]    Edit the {lower} name and confirm the list reflects the change.
    [Tags]    update
    Update {label} Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    {label} Row Should Show Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    Capture Step    {slug}_tc03_updated

TC04 Delete {label}
    [Documentation]    Delete via End Date = Start Date and confirm the {lower} is gone.
    [Tags]    delete    cleanup
    Delete {label}    ${{TEST_CODE}}    ${{END_DATE}}
    {label} Row Should Not Exist    ${{TEST_CODE}}
    {label} Should Not Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc04_deleted


*** Keywords ***
Set Up {label} Suite
    [Documentation]    Generate a unique test code/name, then open the {label} screen.
    ${{code}}    Generate Unique Code    AUTOTEST_{abbr}_
    VAR    ${{TEST_CODE}}    ${{code}}    scope=SUITE
    VAR    ${{OBJ_NAME}}    {label} ${{code}}    scope=SUITE
    VAR    ${{OBJ_NAME_UPD}}    {label} ${{code}} UPD    scope=SUITE
    Open {label} Screen
"""

for rec in records:
    label = rec["screen"]
    slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    up = slug.upper()
    ins_code, ins_name, ins_date, extras = pick_rows(rec["insertPlan"])
    uvis = [f for f in (rec.get("updatePlan") or []) if f.get("visible") and f.get("kind") == "text"]
    if uvis:
        def _upd(target_label, word):
            # prefer the exact insert-form label; never match Master System rows
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

    extra_vars = extra_fill = extra_doc = ""
    for i, f in enumerate(extras):
        lab = f.get("label") or f"extra{i}"
        var = f"{up}_INS_X{i}"
        extra_vars += f"# mandatory extra: {lab} ({f['kind']})\n${{{var}}}    {f['id']}\n"
        if f["kind"] == "checkbox":
            extra_fill += f"    Check Checkbox    css=[id=\"${{{var}}}\"]\n"
        else:
            extra_fill += f"    Fill EC Field    ${{{var}}}    {EXTRA_VALUES.get(lab, 'AUTOTEST')}\n"
        extra_doc = " + mandatory extras"
    dds_by_label = {(f.get("label") or "").strip(): f for f in rec["insertPlan"]
                    if f.get("kind") == "dropdown" and f.get("visible")}
    for j, (dlab, dval) in enumerate(INS_DD_VALUE.get(label, [])):
        f = dds_by_label.get(dlab)
        if not f:
            print(f"  !! {label}: value-dd '{dlab}' not in plan")
            continue
        dd = f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"]
        var = f"{up}_INS_VDD{j}"
        extra_vars += f"# {dlab} links the object into the groupmodel/navigator context\n${{{var}}}    {dd}\n"
        extra_fill += f"    Select EC Dropdown Option    ${{{var}}}    {dval}\n"
        extra_doc = " + mandatory extras"
    for j, dlab in enumerate(REQUIRED_DDS.get(label, [])):
        f = dds_by_label.get(dlab)
        if not f:
            print(f"  !! {label}: required dd '{dlab}' not in plan")
            continue
        dd = f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"]
        var = f"{up}_INS_DD{j}"
        extra_vars += f"# mandatory reference dd: {dlab} (banner-discovered; first option used)\n${{{var}}}    {dd}\n"
        extra_fill += f"    Select First EC Dropdown Option    ${{{var}}}\n"
        extra_doc = " + mandatory extras"

    nav_vars = nav_steps = nav_doc = ""
    for k, (dd, val) in enumerate(NAV.get(label, [])):
        var = f"{up}_NAV{k}"
        nav_vars += f"# groupmodel navigator dropdown — MANDATORY before the grid loads\n${{{var}}}    {dd}\n"
        nav_steps += f"    Select EC Dropdown Option    ${{{var}}}    {val}\n"
        nav_doc = " and set the groupmodel navigator context"
    if nav_steps:
        nav_steps += "    Apply Navigator\n"
    extra_del = ""
    if label in EXTRA_GO:
        extra_del = "    # versioned groupmodel grids redraw lazily after a delete\n    Apply Navigator\n"

    ctx = dict(label=label, slug=slug, UP=up, lower=label.lower(),
               tag=slug.replace("_", "-"), abbr=ABBR[label], view=rec["dbView"],
               table=rec["gridId"] or "manageObject:form:T_data",
               gm="-GM groupmodel" if label in NAV else "",
               ins_code=ins_code["id"], ins_name=ins_name["id"], ins_date=ins_date["id"],
               upd_code=u_code, upd_name=u_name, start_date=DEFAULT_DATE,
               extra_vars=extra_vars, extra_fill=extra_fill, extra_doc=extra_doc,
               nav_vars=nav_vars, nav_steps=nav_steps, nav_doc=nav_doc, extra_del=extra_del)
    (PO_DIR / f"{slug}_page.resource").write_text(PAGE_TMPL.format(**ctx), encoding="utf-8")
    (TEST_DIR / f"{slug}_iud.robot").write_text(TEST_TMPL.format(**ctx), encoding="utf-8")
    print(f"generated {slug}")
print("\n12 screens -> Commercial_Objects/")
