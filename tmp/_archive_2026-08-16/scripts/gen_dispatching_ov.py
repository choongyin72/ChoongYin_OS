"""Generate the 7 plain-OV Dispatching Objects page objects + IUD suites from the
standard post-refactor template (modeled on country_page.resource / country_iud.robot).
Form row indices come from tmp/dispatching_recon/dispatching_recon.json.
Start Date uses TEST_START_DATE_REFDD (forms are full of reference dropdowns).
"""
from pathlib import Path

ROOT = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation")
PO_DIR = ROOT / "pageobjects/Configuration/Assets/Dispatching_Objects"
TEST_DIR = ROOT / "tests/Configuration/Assets/Dispatching_Objects"
PO_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

# screen, slug, VARPREFIX, code-prefix, view, ins_date_row, label
SCREENS = [
    ("Delivery Point",   "delivery_point",   "DELPNT",  "AUTOTEST_DP_",   "ov_delivery_point",   3, "Delivery Point"),
    ("Delivery Stream",  "delivery_stream",  "DELSTRM", "AUTOTEST_DS_",   "ov_delivery_stream",  2, "Delivery Stream"),
    ("Meter",            "meter",            "METER",   "AUTOTEST_MTR_",  "ov_meter",            2, "Meter"),
    ("Nomination Point", "nomination_point", "NOMPNT",  "AUTOTEST_NP_",   "ov_nomination_point", 3, "Nomination Point"),
    ("Pipeline Segment", "pipeline_segment", "PIPESEG", "AUTOTEST_PSEG_", "ov_pipeline_segment", 2, "Pipeline Segment"),
    ("Transport System", "transport_system", "TRNSYS",  "AUTOTEST_TS_",   "ov_transport_system", 2, "Transport System"),
    ("Transport Zone",   "transport_zone",   "TRNZON",  "AUTOTEST_TZ_",   "ov_transport_zone",   3, "Transport Zone"),
]

PO_TMPL = '''*** Settings ***
Documentation       T3 (screen) — {screen} page object.
...                 Screen: Configuration > Assets > Dispatching Objects > {screen}.
...                 Manage-Object (OV) screen. Holds {screen}'s locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{P}_SCREEN}}          {screen}
${{{P}_TABLE}}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${{{P}_INS_CODE}}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${{{P}_INS_NAME}}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${{{P}_INS_DATE}}        tab:tabPanel:objectForm:form:G:0:R:{drow}:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${{{P}_UPD_CODE}}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${{{P}_UPD_NAME}}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${{{P}_DEL_ENDDATE}}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open {screen} Screen
    [Documentation]    Suite Setup: launch, login as ${{user}} (defaults to the env
    ...    user), navigate to the {screen} screen.
    [Arguments]    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Launch EC And Open Screen    ${{{P}_SCREEN}}    ${{user}}    ${{pass}}

{screen} Row Should Exist
    [Documentation]    Assert a {lower} with ${{code}} is present in the list.
    [Arguments]    ${{code}}
    Row Should Exist    ${{{P}_TABLE}}    ${{code}}

{screen} Row Should Not Exist
    [Documentation]    Assert a {lower} with ${{code}} is absent from the list.
    [Arguments]    ${{code}}
    Row Should Not Exist    ${{{P}_TABLE}}    ${{code}}

{screen} Should Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} really persisted in {view}.
    [Arguments]    ${{code}}
    Code Should Be Present In View    {view}    ${{code}}

{screen} Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} was truly deleted from {view}.
    [Arguments]    ${{code}}
    Code Should Be Absent In View    {view}    ${{code}}

{screen} Row Should Show Name
    [Documentation]    Assert the {screen} row for ${{code}} displays ${{name}}.
    [Arguments]    ${{code}}    ${{name}}
    Object Row Should Show Name    ${{{P}_TABLE}}    ${{code}}    ${{name}}

Insert {screen} Record
    [Documentation]    Insert a new {lower}: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}
    Fill New Object Form    ${{{P}_INS_CODE}}    ${{{P}_INS_NAME}}    ${{{P}_INS_DATE}}
    ...    ${{code}}    ${{name}}    ${{start_date}}
    Save And Refresh List

Update {screen} Name
    [Documentation]    Select the {lower}, confirm it loaded, edit Name, Save.
    [Arguments]    ${{code}}    ${{new_name}}
    Update Object Name    ${{{P}_TABLE}}    ${{{P}_UPD_CODE}}    ${{{P}_UPD_NAME}}    ${{code}}    ${{new_name}}

Delete {screen}
    [Documentation]    Select the {lower}, set End Date = Start Date (true delete), Save.
    [Arguments]    ${{code}}    ${{date}}
    Delete Object Via End Date    ${{{P}_TABLE}}    ${{{P}_DEL_ENDDATE}}    ${{code}}    ${{date}}
'''

TEST_TMPL = '''*** Settings ***
Documentation       EC IUD Test - {screen} (Configuration > Assets > Dispatching Objects > {screen}).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in {view}).
...                 Layered: this test -> {slug}_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique {prefix}<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).
...                 Start Date = REFDD epoch: the form carries reference dropdowns.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/{slug}_page.resource

Suite Setup         Set Up {screen} Suite
Suite Teardown      Close EC

Test Tags           iud    {slug}


*** Variables ***
${{TEST_CODE}}        ${{EMPTY}}
${{OBJ_NAME}}         ${{EMPTY}}
${{OBJ_NAME_UPD}}     ${{EMPTY}}
${{START_DATE}}       ${{TEST_START_DATE_REFDD}}
${{END_DATE}}         ${{TEST_START_DATE_REFDD}}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test {lower} does not exist before inserting.
    [Tags]    clean-state
    {screen} Row Should Not Exist    ${{TEST_CODE}}
    Capture Step    {slug}_tc01_clean

TC02 Insert New {screen}
    [Documentation]    Insert a new {lower} and confirm it appears in the list.
    [Tags]    insert
    Insert {screen} Record    ${{TEST_CODE}}    ${{OBJ_NAME}}    ${{START_DATE}}
    {screen} Row Should Exist    ${{TEST_CODE}}
    {screen} Should Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc02_inserted

TC03 Update {screen} Name
    [Documentation]    Edit the {lower} name and confirm the list reflects the change.
    [Tags]    update
    Update {screen} Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    {screen} Row Should Show Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    Capture Step    {slug}_tc03_updated

TC04 Delete {screen}
    [Documentation]    Delete via End Date = Start Date and confirm the {lower} is gone.
    [Tags]    delete    cleanup
    Delete {screen}    ${{TEST_CODE}}    ${{END_DATE}}
    {screen} Row Should Not Exist    ${{TEST_CODE}}
    {screen} Should Not Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc04_deleted


*** Keywords ***
Set Up {screen} Suite
    [Documentation]    Generate a unique test code/name, then open the {screen} screen.
    Prepare IUD Object Data    {prefix}    {label}
    Open {screen} Screen
'''

for screen, slug, P, prefix, view, drow, label in SCREENS:
    ctx = dict(screen=screen, slug=slug, P=P, prefix=prefix, view=view,
               drow=drow, label=label, lower=screen.lower())
    (PO_DIR / f"{slug}_page.resource").write_text(PO_TMPL.format(**ctx), encoding="utf-8")
    (TEST_DIR / f"{slug}_iud.robot").write_text(TEST_TMPL.format(**ctx), encoding="utf-8")
    print(f"generated {slug}_page.resource + {slug}_iud.robot")
print("done")
