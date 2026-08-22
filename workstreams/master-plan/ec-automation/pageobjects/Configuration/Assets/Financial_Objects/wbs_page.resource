*** Settings ***
Documentation       T3 (screen) — WBS page object.
...                 Screen: Configuration > Assets > Financial Objects > WBS.
...                 Custom-URL OV (no navigator/GO — reload via toolbar Refresh, confirmed
...                 live 2026-08-22: grid id is nav:form:T_data, NOT the manage-object
...                 manage_object_nav_nav:form:T_data variant, and no GO button is present).
...                 Rebuilt 2026-08-22 to mirror Bank/State exactly (owner: "reflect the
...                 current EC screen exactly the same way as the OV_BANK IUD related task")
...                 - replaces the older hardcoded-field-id/generated-code pattern with the
...                 label-driven, properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${WBS_SCREEN}           WBS
${WBS_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/wbs_insert.properties
${WBS_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/wbs_update.properties
${WBS_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/wbs_form_verify.properties
${WBS_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/wbs_grid_verify.properties
# Grid id: WBS is a custom-URL OV - grid is nav:form:T_data (NOT the manage-object
# manage_object_nav_nav:form:T_data variant) and there is NO navigator GO button; T2's
# Save And Refresh List auto-detects this (falls back to toolbar Refresh) - confirmed live
# 2026-08-22 (GO button visible count: 0; grid nav:form:T_data count: 1) - cf.
# Calendar/Account/Cost Centre/Revenue Order.
${WBS_TABLE}            nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention -
# confirmed live 2026-08-22 (objectdates row: Start Date C:0 label/C:1 date input, End Date
# C:2 label/C:3 date input).
${WBS_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# WBS's own form-field label set. Labels are plain "Code"/"Name" (NOT screen-prefixed,
# unlike State's "State Code"/"State Name") - confirmed live 2026-08-22 via the New Object
# form mandatory-yellow scan (only Code/Name/Start Date are mandatory-and-empty; End Date,
# Description, WBS, External Ref, Split Share, Comments are all optional and left unset,
# matching the IUD-fill-only-needed-fields convention). Start Date deliberately excluded -
# Insert-only, not present in updateAttributes. Defined ONCE here so both Verify WBS Record
# Exists (TC02) and Verify WBS Record Found (TC04) share the same list.
@{WBS_FORM_LABELS}      Code    Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as WBS's OWN credentials (${WBS_EC_USER}/
    ...    ${WBS_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so wbs_iud.robot's test cases read as a plain business
    ...    step; supplies WBS's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${WBS_EC_USER}    ${WBS_EC_PASS}

Open WBS Screen
    [Documentation]    Navigate to the WBS screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${WBS_SCREEN}

Insert WBS Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so wbs_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State.
    [Arguments]    ${properties_path}=${WBS_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify WBS Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Code/Name only -
    ...    Start Date is grid/insert-only, not present in updateAttributes). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${WBS_TABLE}    ${code}    WBS    ${WBS_INSERT_PROPERTIES}
    ...    @{WBS_FORM_LABELS}

Update WBS Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${WBS_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${WBS_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify WBS Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Form Record.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${WBS_TABLE}    ${code}    WBS    ${WBS_UPDATE_PROPERTIES}
    ...    Name

Find WBS Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object Record    ${WBS_TABLE}    ${code}    WBS

Verify WBS Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    WBS Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${WBS_TABLE}    ${code}    ${WBS_GRID_VERIFY_PROPERTIES}
    ...    ${WBS_FORM_VERIFY_PROPERTIES}    @{WBS_FORM_LABELS}

Delete WBS Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the wbs, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/State's convention.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object Via End Date    ${WBS_TABLE}    ${WBS_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Verify WBS Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${WBS_TABLE}    OV_FIN_WBS    ${code}
    Capture Step    ${TEST NAME}_verify

Verify WBS Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${WBS_TABLE}    ${code}
