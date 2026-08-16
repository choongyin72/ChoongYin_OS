"""Generate Basic Objects phase-A artifacts: 9 page objects + 9 IUD suites,
mirroring the Bank template exactly (same layering, same TC01-04 shape).
Field row indexes come from tmp/screen_scan/basic_objects_recon.json recon."""
from pathlib import Path

BASE = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation")
PO_DIR = BASE / "pageobjects/Configuration/Assets/Basic_Objects"
TEST_DIR = BASE / "tests/Configuration/Assets/Basic_Objects"
PO_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

# slug, Screen label, abbr, table id, insR(code,name,date), updR(code,name), view
SCREENS = [
    ("production_unit", "Production Unit", "PU", "manage_object_nav_nav:form:T_data", (0, 1, 4), (0, 1), "OV_PRODUCTIONUNIT"),
    ("business_unit", "Business Unit", "BU", "manage_object_nav_nav:form:T_data", (0, 1, 2), (0, 1), "OV_BUSINESS_UNIT"),
    ("country", "Country", "CTRY", "manage_object_nav_nav:form:T_data", (0, 1, 5), (0, 1), "OV_COUNTRY"),
    ("state", "State", "ST", "manage_object_nav_nav:form:T_data", (2, 3, 4), (2, 3), "OV_STATE"),
    ("county", "County", "CNTY", "manage_object_nav_nav:form:T_data", (2, 3, 5), (2, 3), "OV_COUNTY"),
    ("region", "Region", "REG", "manage_object_nav_nav:form:T_data", (0, 1, 4), (0, 1), "OV_REGION"),
    ("object_list", "Object List", "OL", "manage_object_nav_nav:form:T_data", (0, 1, 2), (0, 1), "OV_OBJECT_LIST"),
    ("functional_area", "Functional Area", "FA", "manage_object_nav_nav:form:T_data", (0, 1, 2), (0, 1), "OV_FUNCTIONAL_AREA"),
    ("regulatory_permits", "Regulatory Permits", "RP", "nav:form:T_data", (0, 1, 2), (0, 1), "OV_REGULATORY_PERMITS"),
]

PAGE_TMPL = '''*** Settings ***
Documentation       T3 (screen) — {label} page object.
...                 Screen: Configuration > Assets > Basic Objects > {label}.
...                 Manage-Object (OV) screen. Holds {label}'s locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{UP}_SCREEN}}{pad_screen}{label}
${{{UP}_TABLE}}{pad_table}{table}
# objectForm field IDs (Insert — new object)
${{{UP}_INS_CODE}}{pad_ins_code}tab:tabPanel:objectForm:form:G:0:R:{ic}:C:1:in
${{{UP}_INS_NAME}}{pad_ins_name}tab:tabPanel:objectForm:form:G:0:R:{iname}:C:1:in
${{{UP}_INS_DATE}}{pad_ins_date}tab:tabPanel:objectForm:form:G:0:R:{idate}:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${{{UP}_UPD_CODE}}{pad_upd_code}tab:tabPanel:updateAttributes:form:G:0:R:{uc}:C:1:in
${{{UP}_UPD_NAME}}{pad_upd_name}tab:tabPanel:updateAttributes:form:G:0:R:{uname}:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${{{UP}_DEL_ENDDATE}}{pad_del}tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open {label} Screen
    [Documentation]    Suite Setup: launch, login as ${{user}} (defaults to the env
    ...    user), navigate to the {label} screen. Pass a different user for role tests.
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
    ${{row}}=    Get Text    xpath=//tbody[@id='${{{UP}_TABLE}}']//tr[.//span[normalize-space(text())='${{code}}']]
    Should Contain    ${{row}}    ${{name}}    msg={label} row ${{code}} does not show name ${{name}}

Insert {label} Record
    [Documentation]    Insert a new {lower}: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}
    Open New Object Form
    Fill EC Field    ${{{UP}_INS_CODE}}    ${{code}}
    Fill EC Field    ${{{UP}_INS_NAME}}    ${{name}}
    Fill EC Date    ${{{UP}_INS_DATE}}    ${{start_date}}
    Save
    Apply Navigator

Update {label} Name
    [Documentation]    Select the {lower}, confirm it loaded, edit Name, Save.
    [Arguments]    ${{code}}    ${{new_name}}
    Select Object Row    ${{{UP}_TABLE}}    ${{code}}
    ${{loaded}}=    Get Property    css=[id="${{{UP}_UPD_CODE}}"]    value
    Should Be Equal    ${{loaded}}    ${{code}}    msg=Row select failed - code not loaded
    Fill EC Field    ${{{UP}_UPD_NAME}}    ${{new_name}}
    Save
    Apply Navigator

Delete {label}
    [Documentation]    Select the {lower}, set End Date = Start Date (true delete), Save.
    [Arguments]    ${{code}}    ${{date}}
    Select Object Row    ${{{UP}_TABLE}}    ${{code}}
    Delete Object By Zero-Length Window    ${{{UP}_DEL_ENDDATE}}    ${{date}}
    Save
    Apply Navigator
'''

TEST_TMPL = '''*** Settings ***
Documentation       EC IUD Test - {label} (Configuration > Assets > Basic Objects > {label}).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in {view}).
...                 Layered: this test -> {slug}_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_{abbr}_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/{slug}_page.resource

Suite Setup         Set Up {label} Suite
Suite Teardown      Close EC

Test Tags           iud    {tag}


*** Variables ***
${{TEST_CODE}}        ${{EMPTY}}
${{OBJ_NAME}}         ${{EMPTY}}
${{OBJ_NAME_UPD}}     ${{EMPTY}}
${{START_DATE}}       2000-01-01
${{END_DATE}}         2000-01-01


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
'''


def pad(varname, target=24):
    """Robot-style alignment: at least 4 spaces after the ${VAR} token."""
    return " " * max(4, target - len(varname))


for slug, label, abbr, table, (ic, iname, idate), (uc, uname), view in SCREENS:
    up = slug.upper()
    ctx = dict(
        slug=slug, label=label, abbr=abbr, table=table, view=view,
        UP=up, lower=label.lower(), tag=slug.replace("_", "-"),
        ic=ic, iname=iname, idate=idate, uc=uc, uname=uname,
        pad_screen=pad(f"${{{up}_SCREEN}}"),
        pad_table=pad(f"${{{up}_TABLE}}"),
        pad_ins_code=pad(f"${{{up}_INS_CODE}}"),
        pad_ins_name=pad(f"${{{up}_INS_NAME}}"),
        pad_ins_date=pad(f"${{{up}_INS_DATE}}"),
        pad_upd_code=pad(f"${{{up}_UPD_CODE}}"),
        pad_upd_name=pad(f"${{{up}_UPD_NAME}}"),
        pad_del=pad(f"${{{up}_DEL_ENDDATE}}"),
    )
    (PO_DIR / f"{slug}_page.resource").write_text(PAGE_TMPL.format(**ctx), encoding="utf-8")
    (TEST_DIR / f"{slug}_iud.robot").write_text(TEST_TMPL.format(**ctx), encoding="utf-8")
    print(f"generated {slug}_page.resource + {slug}_iud.robot")

print(f"\n{len(SCREENS)} screens -> {PO_DIR}\n              {TEST_DIR}")
