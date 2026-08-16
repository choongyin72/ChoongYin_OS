"""Generate Financial Objects RF artifacts (14 screens) DATA-DRIVEN from
tmp/screen_scan/financial_objects_recon.json: field rows are derived by LABEL
(code/name/start-date/update rows), extra mandatory fields get safe test
values, page objects stay thin over the T2 generics.
Emits: pageobjects/.../Financial_Objects/<slug>_page.resource
       tests/.../Financial_Objects/<slug>_iud.robot"""
import json
import re
from pathlib import Path

BASE = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation")
PO_DIR = BASE / "pageobjects/Configuration/Assets/Financial_Objects"
TEST_DIR = BASE / "tests/Configuration/Assets/Financial_Objects"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json")
PO_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

ABBR = {"Account": "ACC", "Bank Account": "BACC", "Cost Centre": "CC",
        "Cost Object Mapping": "COM", "Currency": "CUR", "DOA Credit Limit": "DOA",
        "Exchange Rate Source": "ERS", "Payment Scheme": "PSCH",
        "Product Description": "PD", "Revenue Order": "RO", "Sales Order": "SO",
        "VAT Code": "VAT", "WBS": "WBS", "Account Mapping": "AM"}

# safe throwaway values for extra mandatory TEXT fields, by label
EXTRA_VALUES = {"GL Account": "999999", "Sort Code": "000000",
                "Credit Limit": "1000", "VAT Code": "AT9", "Rate (Decimal)": "0.1"}

# per-screen test dates: reference dropdowns are EFFECTIVE-DATE-FILTERED, so the
# form Start Date must postdate the referenced seed objects (customers/cost
# objects start 2003-01-01) - user-explained 2026-06-12
SCREEN_DATES = {"Bank Account": "2003-01-01", "Cost Object Mapping": "2003-01-01"}

# mandatory reference DROPDOWNS per screen, discovered from the EC save banner
# ("Required fields are empty: ...") - the static {mandatory:true} marker misses
# popup-type fields. Throwaway records -> first available option is selected.
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
    """Derive (code_row, name_row, date_row, extras) from a labelled field plan."""
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
...                 Screen: Configuration > Assets > Financial Objects > {label}.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{UP}_SCREEN}}    {label}
${{{UP}_TABLE}}    {table}
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
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
    [Documentation]    Suite Setup: launch, login, navigate to the {label} screen.
    [Arguments]    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Open EC Browser
    Login To EC    ${{user}}    ${{pass}}
    Navigate To Screen    ${{{UP}_SCREEN}}

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
"""

TEST_TMPL = """*** Settings ***
Documentation       EC IUD Test - {label} (Configuration > Assets > Financial Objects > {label}).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in {view}).
...                 NEVER touch existing data. A unique AUTOTEST_{abbr}_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/{slug}_page.resource

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

manifest = []
for rec in records:
    label = rec["screen"]
    slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    up = slug.upper()
    ins_code, ins_name, ins_date, extras = pick_rows(rec["insertPlan"])
    upd_plan = rec.get("updatePlan") or []
    uvis = [f for f in upd_plan if f.get("visible") and f.get("kind") == "text"]
    if uvis:
        u_code = next(f for f in uvis if "code" in (f.get("label") or "").lower())
        u_name = next(f for f in uvis if (f.get("label") or "").strip().lower()
                      in ((ins_name.get("label") or "name").lower(), "name"))
    else:  # empty table (Payment Scheme): derive from insert order
        u_code = {"id": ins_code["id"].replace("objectForm", "updateAttributes")}
        u_name = {"id": ins_name["id"].replace("objectForm", "updateAttributes")}

    extra_vars = extra_fill = extra_doc = ""
    for i, f in enumerate(extras):
        lab = f.get("label") or f"extra{i}"
        var = f"{up}_INS_X{i}"
        extra_vars += f"# mandatory extra: {lab} ({f['kind']})\n${{{var}}}    {f['id']}\n"
        if f["kind"] == "checkbox":
            extra_fill += f"    Check Checkbox    css=[id=\"${{{var}}}\"]\n"
        else:
            val = EXTRA_VALUES.get(lab, "AUTOTEST")
            extra_fill += f"    Fill EC Field    ${{{var}}}    {val}\n"
        extra_doc = " + mandatory extras"
    # mandatory reference dropdowns (from the save banner): first available option
    dds_by_label = {(f.get("label") or "").strip(): f for f in rec["insertPlan"]
                    if f.get("kind") == "dropdown" and f.get("visible")}
    for j, dlab in enumerate(REQUIRED_DDS.get(label, [])):
        f = dds_by_label.get(dlab)
        if not f:
            print(f"  !! {label}: required dd '{dlab}' not found in insert plan")
            continue
        dd_prefix = f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"]
        var = f"{up}_INS_DD{j}"
        extra_vars += f"# mandatory reference dd: {dlab} (banner-discovered; first option used)\n${{{var}}}    {dd_prefix}\n"
        extra_fill += f"    Select First EC Dropdown Option    ${{{var}}}\n"
        extra_doc = " + mandatory extras"

    ctx = dict(start_date=SCREEN_DATES.get(label, "2000-01-01"), label=label, slug=slug, UP=up, lower=label.lower(),
               tag=slug.replace("_", "-"), abbr=ABBR[label], view=rec["dbView"],
               table=rec["gridId"], ins_code=ins_code["id"], ins_name=ins_name["id"],
               ins_date=ins_date["id"], upd_code=u_code["id"], upd_name=u_name["id"],
               extra_vars=extra_vars, extra_fill=extra_fill, extra_doc=extra_doc)
    (PO_DIR / f"{slug}_page.resource").write_text(PAGE_TMPL.format(**ctx), encoding="utf-8")
    (TEST_DIR / f"{slug}_iud.robot").write_text(TEST_TMPL.format(**ctx), encoding="utf-8")
    manifest.append(slug)
    print(f"generated {slug} (extras: {[ (f.get('label'), f['kind']) for f in extras ]})")

print(f"\n{len(manifest)} screens -> Financial_Objects/")
