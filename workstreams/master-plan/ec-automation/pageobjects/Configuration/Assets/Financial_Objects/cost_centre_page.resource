*** Settings ***
Documentation       T3 (screen) — Cost Centre page object.
...                 Screen: Configuration > Assets > Financial Objects > Cost Centre.
...                 Custom-URL OV screen (grid id nav:form:T_data, NO navigator GO button
...                 - confirmed live 2026-08-22, GO button count=0 - reload is via T2's
...                 Save And Refresh List, which auto-detects the missing GO and falls back
...                 to toolbar Refresh). Holds Cost Centre's locators + thin IUD wrappers
...                 that delegate to T2 (manage_object) and T1 (common).
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
${COST_CENTRE_SCREEN}    Cost Centre
${COST_CENTRE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_centre_insert.properties
${COST_CENTRE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_centre_update.properties
${COST_CENTRE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_centre_form_verify.properties
${COST_CENTRE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_centre_grid_verify.properties
# Grid id: this is a CUSTOM-URL OV (not manage-object) - own constant, NOT T2's
# ${OV_MANAGE_OBJECT_TABLE} (that one is manage_object_nav_nav:form:T_data, a different
# screen family). Confirmed live 2026-08-22: nav:form:T_data count=1, GO button count=0.
${COST_CENTRE_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention.
# Resolved live via OV Field Id By Label on 2026-08-22 and confirmed identical to this
# constant, which is the framework-invariant objectdates layout also seen on Bank/State.
${COST_CENTRE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Cost Centre's own form-field label set: "Code"/"Name" (generic, NOT screen-prefixed) -
# confirmed live 2026-08-22 via both the New Object form (objectForm) and the row-select
# form (updateAttributes) label dumps - same convention as Bank/Object List, unlike State.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes.
# Defined ONCE here so both Verify Cost Centre Record Exists (TC02) and Verify Cost Centre
# Record Found (TC04) share the same list.
@{COST_CENTRE_FORM_LABELS}    Code    Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Cost Centre's OWN credentials (${COST_CENTRE_EC_USER}/
    ...    ${COST_CENTRE_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so cost_centre_iud.robot's test cases read as a plain
    ...    business step; supplies Cost Centre's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${COST_CENTRE_EC_USER}    ${COST_CENTRE_EC_PASS}

Open Cost Centre Screen
    [Documentation]    Navigate to the Cost Centre screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${COST_CENTRE_SCREEN}

Insert Cost Centre Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so cost_centre_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching Bank/State.
    [Arguments]    ${properties_path}=${COST_CENTRE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Cost Centre Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name only - Start
    ...    Date is grid/insert-only, not present in updateAttributes). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${COST_CENTRE_TABLE}    ${code}    Cost Centre    ${COST_CENTRE_INSERT_PROPERTIES}
    ...    @{COST_CENTRE_FORM_LABELS}

Update Cost Centre Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${COST_CENTRE_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${COST_CENTRE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify Cost Centre Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Form Record.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${COST_CENTRE_TABLE}    ${code}    Cost Centre    ${COST_CENTRE_UPDATE_PROPERTIES}
    ...    Name

Find Cost Centre Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object Record    ${COST_CENTRE_TABLE}    ${code}    Cost Centre

Verify Cost Centre Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Cost Centre Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${COST_CENTRE_TABLE}    ${code}    ${COST_CENTRE_GRID_VERIFY_PROPERTIES}
    ...    ${COST_CENTRE_FORM_VERIFY_PROPERTIES}    @{COST_CENTRE_FORM_LABELS}

Delete Cost Centre Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the cost centre, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State's convention.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object Via End Date    ${COST_CENTRE_TABLE}    ${COST_CENTRE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Verify Cost Centre Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${COST_CENTRE_TABLE}    OV_FIN_COST_CENTER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Cost Centre Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${COST_CENTRE_TABLE}    ${code}
