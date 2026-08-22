*** Settings ***
Documentation       T3 (screen) — Production Unit page object.
...                 Screen: Configuration > Assets > Basic Objects > Production Unit.
...                 Manage-Object (OV) screen. Holds Production Unit's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/Object List/State/Region/Functional
...                 Area/Business Unit exactly (owner: "reflect the current EC screen
...                 exactly the same way as the OV_BANK IUD related task") - replaces the
...                 older hardcoded-field-id pattern with the label-driven,
...                 properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PRODUCTION_UNIT_SCREEN}    Production Unit
${PRODUCTION_UNIT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/production_unit_insert.properties
${PRODUCTION_UNIT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/production_unit_update.properties
${PRODUCTION_UNIT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/production_unit_form_verify.properties
${PRODUCTION_UNIT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/production_unit_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${PRODUCTION_UNIT_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching the other rebuilt screens' convention.
${PRODUCTION_UNIT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Production Unit's own form-field label set. Labels are "Production Unit Code"/"Production
# Unit Name" (full screen-name prefix, standard "Start Date" capitalization) - confirmed
# live 2026-08-22 via RF recon (tmp/recon_pu_labels.robot) BEFORE building, same discipline
# as every other screen in this batch. The optional "System of Measurement" dropdown was
# confirmed NOT mandatory (tmp/recon_pu_mandatory.robot - no MandatoryCellStyle class) and is
# deliberately omitted, matching the IUD-fill-only-needed-fields convention. Start Date
# deliberately excluded from this label set - Insert-only, not present in updateAttributes.
# Defined ONCE here so both Verify Production Unit Record Exists (TC02) and Verify
# Production Unit Record Found (TC04) share the same list.
@{PRODUCTION_UNIT_FORM_LABELS}    Production Unit Code    Production Unit Name


*** Keywords ***
Find Production Unit Row By Filter
    [Documentation]    Explicitly filter the Production Unit grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Object List's explicit filter usage (owner, 2026-08-22: "same to
    ...    other ec screens"), rather than relying only on Select Object Row's implicit
    ...    3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRODUCTION_UNIT_TABLE}    ${code}

Clear Production Unit Row Filter
    [Documentation]    Clear the Code column filter (see Find Production Unit Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${PRODUCTION_UNIT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Production Unit's OWN credentials
    ...    (${PRODUCTION_UNIT_EC_USER}/${PRODUCTION_UNIT_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so production_unit_iud.robot's
    ...    test cases read as a plain business step; supplies Production Unit's own
    ...    credential defaults to the shared T1 Login To EC Screen (common.resource), which
    ...    owns the actual login mechanics.
    Login To EC Screen    ${PRODUCTION_UNIT_EC_USER}    ${PRODUCTION_UNIT_EC_PASS}

Open Production Unit Screen
    [Documentation]    Navigate to the Production Unit screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${PRODUCTION_UNIT_SCREEN}

Insert Production Unit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so production_unit_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching the other rebuilt screens. ${code_label}="Production Unit Code"
    ...    passed through so T2 reads the resolved code back from the right
    ...    properties-file key.
    [Arguments]    ${properties_path}=${PRODUCTION_UNIT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Production Unit Code
    RETURN    ${code}

Verify Production Unit Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching the other rebuilt screens' TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Production Unit Code/Production Unit Name only - Start Date is grid/insert-only,
    ...    not present in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Production Unit Row By Filter first, clears after (2026-08-23
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Production Unit Row By Filter    ${code}
    Verify Object Insert Exists    ${PRODUCTION_UNIT_TABLE}    ${code}    Production Unit
    ...    ${PRODUCTION_UNIT_INSERT_PROPERTIES}    @{PRODUCTION_UNIT_FORM_LABELS}
    ...    code_label=Production Unit Code
    Clear Production Unit Row Filter

Update Production Unit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching the other
    ...    rebuilt screens. Filters via Find Production Unit Row By Filter first, clears
    ...    after (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRODUCTION_UNIT_UPDATE_PROPERTIES}
    Find Production Unit Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRODUCTION_UNIT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Production Unit Code
    Clear Production Unit Row Filter
    RETURN    ${data}

Verify Production Unit Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching the other rebuilt screens' TC03 convention: the form shows
    ...    the updated Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Production Unit Row
    ...    By Filter first, clears after (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Production Unit Row By Filter    ${code}
    Verify Object Form Record    ${PRODUCTION_UNIT_TABLE}    ${code}    Production Unit
    ...    ${PRODUCTION_UNIT_UPDATE_PROPERTIES}    Production Unit Name
    ...    code_label=Production Unit Code
    Clear Production Unit Row Filter

Find Production Unit Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Production Unit Row By
    ...    Filter first (2026-08-23 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Production Unit Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Production Unit Row By Filter    ${code}
    Find Object Record    ${PRODUCTION_UNIT_TABLE}    ${code}    Production Unit
    ...    code_label=Production Unit Code

Verify Production Unit Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Production Unit Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done (2026-08-23
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRODUCTION_UNIT_TABLE}    ${code}    ${PRODUCTION_UNIT_GRID_VERIFY_PROPERTIES}
    ...    ${PRODUCTION_UNIT_FORM_VERIFY_PROPERTIES}    @{PRODUCTION_UNIT_FORM_LABELS}
    Clear Production Unit Row Filter

Delete Production Unit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the production unit, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching the other rebuilt screens'
    ...    convention. Filters via Find Production Unit Row By Filter first, clears after
    ...    (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Production Unit Row By Filter    ${code}
    Delete Object Via End Date    ${PRODUCTION_UNIT_TABLE}    ${PRODUCTION_UNIT_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Production Unit Row Filter

Verify Production Unit Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRODUCTION_UNIT_TABLE}    OV_PRODUCTIONUNIT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Production Unit Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRODUCTION_UNIT_TABLE}    ${code}
