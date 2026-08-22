*** Settings ***
Documentation       T3 (screen) — Business Unit page object.
...                 Screen: Configuration > Assets > Basic Objects > Business Unit.
...                 Manage-Object (OV) screen. Holds Business Unit's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/Object List/State/Region/Functional
...                 Area exactly (owner: "reflect the current EC screen exactly the same
...                 way as the OV_BANK IUD related task") - replaces the older
...                 hardcoded-field-id pattern with the label-driven, properties-file-driven,
...                 T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${BUSINESS_UNIT_SCREEN}    Business Unit
${BUSINESS_UNIT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/business_unit_insert.properties
${BUSINESS_UNIT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/business_unit_update.properties
${BUSINESS_UNIT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/business_unit_form_verify.properties
${BUSINESS_UNIT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/business_unit_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${BUSINESS_UNIT_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching the other rebuilt screens' convention.
${BUSINESS_UNIT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Business Unit's own form-field label set. Labels are "Business Unit Code"/"Business Unit
# Name" (full screen-name prefix, standard "Start Date" capitalization) - confirmed live
# 2026-08-22 via RF recon (tmp/recon_bu_labels.robot) BEFORE building, same discipline as
# every other screen in this batch. Start Date deliberately excluded - Insert-only, not
# present in updateAttributes. Defined ONCE here so both Verify Business Unit Record Exists
# (TC02) and Verify Business Unit Record Found (TC04) share the same list.
@{BUSINESS_UNIT_FORM_LABELS}    Business Unit Code    Business Unit Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Business Unit's OWN credentials
    ...    (${BUSINESS_UNIT_EC_USER}/${BUSINESS_UNIT_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so business_unit_iud.robot's
    ...    test cases read as a plain business step; supplies Business Unit's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${BUSINESS_UNIT_EC_USER}    ${BUSINESS_UNIT_EC_PASS}

Open Business Unit Screen
    [Documentation]    Navigate to the Business Unit screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${BUSINESS_UNIT_SCREEN}

Insert Business Unit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so business_unit_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching the other rebuilt screens. ${code_label}="Business Unit Code"
    ...    passed through so T2 reads the resolved code back from the right properties-file
    ...    key.
    [Arguments]    ${properties_path}=${BUSINESS_UNIT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Business Unit Code
    RETURN    ${code}

Verify Business Unit Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching the other rebuilt screens' TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Business Unit Code/Business Unit Name only - Start Date is grid/insert-only,
    ...    not present in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${BUSINESS_UNIT_TABLE}    ${code}    Business Unit
    ...    ${BUSINESS_UNIT_INSERT_PROPERTIES}    @{BUSINESS_UNIT_FORM_LABELS}
    ...    code_label=Business Unit Code

Update Business Unit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching the other
    ...    rebuilt screens.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${BUSINESS_UNIT_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${BUSINESS_UNIT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Business Unit Code
    RETURN    ${data}

Verify Business Unit Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching the other rebuilt screens' TC03 convention: the form shows
    ...    the updated Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${BUSINESS_UNIT_TABLE}    ${code}    Business Unit
    ...    ${BUSINESS_UNIT_UPDATE_PROPERTIES}    Business Unit Name    code_label=Business Unit Code

Find Business Unit Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object Record    ${BUSINESS_UNIT_TABLE}    ${code}    Business Unit
    ...    code_label=Business Unit Code

Verify Business Unit Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Business Unit Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${BUSINESS_UNIT_TABLE}    ${code}    ${BUSINESS_UNIT_GRID_VERIFY_PROPERTIES}
    ...    ${BUSINESS_UNIT_FORM_VERIFY_PROPERTIES}    @{BUSINESS_UNIT_FORM_LABELS}

Delete Business Unit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the business unit, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching the other rebuilt screens'
    ...    convention.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object Via End Date    ${BUSINESS_UNIT_TABLE}    ${BUSINESS_UNIT_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action

Verify Business Unit Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${BUSINESS_UNIT_TABLE}    OV_BUSINESS_UNIT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Business Unit Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${BUSINESS_UNIT_TABLE}    ${code}
