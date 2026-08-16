"""Regenerate the Dispatching Objects page objects + suites as OV-GM (round 2).
Discovery: ALL these screens gate their grid behind a navigator Business Unit pick + GO
(grid id manageObject:form:T_data), and each insert must reference a parent consistent
with that BU to be visible. Meter is PARKED to slice 2 (popup picker gesture).
"""
from pathlib import Path

ROOT = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation")
PO_DIR = ROOT / "pageobjects/Configuration/Assets/Dispatching_Objects"
TEST_DIR = ROOT / "tests/Configuration/Assets/Dispatching_Objects"

# screen, slug, VARPREFIX, code-prefix, view, date_row,
# nav_bu_label, parent_label_text, parent_dd_row, parent_value
SCREENS = [
    ("Delivery Point", "delivery_point", "DELPNT", "AUTOTEST_DP_", "ov_delivery_point", 3,
     "ECP Norway", "Business Unit Name", 11, "ECP Norway"),
    ("Delivery Stream", "delivery_stream", "DELSTRM", "AUTOTEST_DS_", "ov_delivery_stream", 2,
     "ECP Norway", "Business Unit", 8, "ECP Norway"),
    ("Nomination Point", "nomination_point", "NOMPNT", "AUTOTEST_NP_", "ov_nomination_point", 3,
     "ECP Norway", "Contract Name", 5, "ECP Norway 3P Gas Purchase"),
    ("Pipeline Segment", "pipeline_segment", "PIPESEG", "AUTOTEST_PSEG_", "ov_pipeline_segment", 2,
     "TS5 BU", "Pipeline Name", 6, "TS5 Gas Pipeline"),
    ("Transport System", "transport_system", "TRNSYS", "AUTOTEST_TS_", "ov_transport_system", 2,
     "ECP Norway", "Business Unit Name", 6, "ECP Norway"),
    ("Transport Zone", "transport_zone", "TRNZON", "AUTOTEST_TZ_", "ov_transport_zone", 3,
     "TS5 BU", "Transport System Name", 5, "TS5 Transport System"),
]

PO_TMPL = '''*** Settings ***
Documentation       T3 (screen) — {screen} page object.
...                 Screen: Configuration > Assets > Dispatching Objects > {screen}.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "{parent_label}" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-12).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{P}_SCREEN}}          {screen}
${{{P}_TABLE}}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${{{P}_NAV_BU}}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${{{P}_INS_CODE}}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${{{P}_INS_NAME}}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${{{P}_INS_DATE}}        tab:tabPanel:objectForm:form:G:0:R:{drow}:C:1:da_input
# Insert form's "{parent_label}" dropdown (mandatory / grid-visibility parent)
${{{P}_INS_PARENT}}      tab:tabPanel:objectForm:form:G:0:R:{prow}:C:1:dd
# updateAttributes field IDs (Update — existing object)
${{{P}_UPD_CODE}}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${{{P}_UPD_NAME}}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${{{P}_DEL_ENDDATE}}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open {screen} Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${{business_unit}}    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Launch EC And Open Screen    ${{{P}_SCREEN}}    ${{user}}    ${{pass}}
    Select EC Dropdown Option    ${{{P}_NAV_BU}}    ${{business_unit}}
    Apply Navigator

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
    [Documentation]    Insert a new {lower}: New Object form -> Code/Name/Start Date +
    ...    "{parent_label}" = ${{parent}} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}    ${{parent}}
    Fill New Object Form    ${{{P}_INS_CODE}}    ${{{P}_INS_NAME}}    ${{{P}_INS_DATE}}
    ...    ${{code}}    ${{name}}    ${{start_date}}
    Select EC Dropdown Option    ${{{P}_INS_PARENT}}    ${{parent}}
    Save And Refresh List

Update {screen} Name
    [Documentation]    Select the {lower}, confirm it loaded, edit Name, Save.
    [Arguments]    ${{code}}    ${{new_name}}
    Update Object Name    ${{{P}_TABLE}}    ${{{P}_UPD_CODE}}    ${{{P}_UPD_NAME}}    ${{code}}    ${{new_name}}

Delete {screen}
    [Documentation]    Select the {lower}, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${{code}}    ${{date}}
    Delete Object Via End Date    ${{{P}_TABLE}}    ${{{P}_DEL_ENDDATE}}    ${{code}}    ${{date}}
    Apply Navigator
'''

TEST_TMPL = '''*** Settings ***
Documentation       EC IUD Test - {screen} (Configuration > Assets > Dispatching Objects > {screen}).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "{parent_label}" = {parent_value} so the row is visible
...                 under the {nav_bu} filter. DELETE = End Date = Start Date ({view}).
...                 NEVER touch existing data: unique {prefix}<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

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
${{NAV_BU}}           {nav_bu}
${{PARENT_VALUE}}     {parent_value}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test {lower} does not exist before inserting.
    [Tags]    clean-state
    {screen} Row Should Not Exist    ${{TEST_CODE}}
    Capture Step    {slug}_tc01_clean

TC02 Insert New {screen}
    [Documentation]    Insert a new {lower} and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert {screen} Record    ${{TEST_CODE}}    ${{OBJ_NAME}}    ${{START_DATE}}    ${{PARENT_VALUE}}
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
    [Documentation]    Generate a unique test code/name, then open the {screen} screen
    ...    with the ${{NAV_BU}} navigator context.
    Prepare IUD Object Data    {prefix}    {screen}
    Open {screen} Screen    ${{NAV_BU}}
'''

for screen, slug, P, prefix, view, drow, nav_bu, parent_label, prow, parent_value in SCREENS:
    ctx = dict(screen=screen, slug=slug, P=P, prefix=prefix, view=view, drow=drow,
               nav_bu=nav_bu, parent_label=parent_label, prow=prow,
               parent_value=parent_value, lower=screen.lower())
    (PO_DIR / f"{slug}_page.resource").write_text(PO_TMPL.format(**ctx), encoding="utf-8")
    (TEST_DIR / f"{slug}_iud.robot").write_text(TEST_TMPL.format(**ctx), encoding="utf-8")
    print(f"regenerated {slug}")

# Meter parked to slice 2 (popup picker gesture) - remove round-1 files
for f in [PO_DIR / "meter_page.resource", TEST_DIR / "meter_iud.robot"]:
    if f.exists():
        f.unlink()
        print(f"removed (parked to slice 2): {f.name}")
print("done")
