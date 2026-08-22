*** Settings ***
Documentation       T3 (screen) — Company page object.
...                 Screen: Configuration > Assets > Commercial Objects > Company.
...                 Manage-Object (OV) screen. Holds Company's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/Object List/State/Region/Functional
...                 Area/Business Unit/Production Unit exactly (owner: "reflect the current
...                 EC screen exactly the same way as the OV_BANK IUD related task") -
...                 replaces the older hardcoded-field-id pattern with the label-driven,
...                 properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${COMPANY_SCREEN}       Company
${COMPANY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/company_insert.properties
${COMPANY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/company_update.properties
${COMPANY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/company_form_verify.properties
${COMPANY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/company_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${COMPANY_TABLE}        ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching the other rebuilt screens' convention.
${COMPANY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Company's own form-field label set. Labels are "Company Code"/"Company Name" (full
# screen-name prefix, standard "Start Date" capitalization) - confirmed live 2026-08-22 via
# RF recon (tmp/recon_company_labels.robot) BEFORE building, same discipline as every other
# screen in this batch. Company has 30+ optional fields (Address Line 1-8/Phone/Fax/Country
# dd/Local Currency dd/etc.) - all deliberately omitted, only Code/Name/Start Date confirmed
# mandatory (MandatoryCellStyle class, tmp/recon_company_mandatory.robot). Start Date
# deliberately excluded from this label set - Insert-only, not present in updateAttributes.
# Defined ONCE here so both Verify Company Record Exists (TC02) and Verify Company Record
# Found (TC04) share the same list.
@{COMPANY_FORM_LABELS}    Company Code    Company Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Company's OWN credentials (${COMPANY_EC_USER}/
    ...    ${COMPANY_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so company_iud.robot's test cases read as a plain business
    ...    step; supplies Company's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${COMPANY_EC_USER}    ${COMPANY_EC_PASS}

Open Company Screen
    [Documentation]    Navigate to the Company screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${COMPANY_SCREEN}

Insert Company Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so company_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching the other rebuilt screens. ${code_label}="Company Code" passed through
    ...    so T2 reads the resolved code back from the right properties-file key.
    [Arguments]    ${properties_path}=${COMPANY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Company Code
    RETURN    ${code}

Verify Company Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching the other rebuilt screens' TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Company Code/Company Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${COMPANY_TABLE}    ${code}    Company
    ...    ${COMPANY_INSERT_PROPERTIES}    @{COMPANY_FORM_LABELS}    code_label=Company Code

Update Company Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching the other
    ...    rebuilt screens.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${COMPANY_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${COMPANY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Company Code
    RETURN    ${data}

Verify Company Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching the other rebuilt screens' TC03 convention: the form shows
    ...    the updated Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${COMPANY_TABLE}    ${code}    Company
    ...    ${COMPANY_UPDATE_PROPERTIES}    Company Name    code_label=Company Code

Find Company Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object Record    ${COMPANY_TABLE}    ${code}    Company    code_label=Company Code

Verify Company Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Company Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${COMPANY_TABLE}    ${code}    ${COMPANY_GRID_VERIFY_PROPERTIES}
    ...    ${COMPANY_FORM_VERIFY_PROPERTIES}    @{COMPANY_FORM_LABELS}

Delete Company Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the company, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching the other rebuilt screens' convention.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object Via End Date    ${COMPANY_TABLE}    ${COMPANY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Verify Company Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${COMPANY_TABLE}    OV_COMPANY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Company Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${COMPANY_TABLE}    ${code}
