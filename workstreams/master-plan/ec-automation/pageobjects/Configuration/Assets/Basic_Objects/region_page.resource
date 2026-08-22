*** Settings ***
Documentation       T3 (screen) — Region page object.
...                 Screen: Configuration > Assets > Basic Objects > Region.
...                 Manage-Object (OV) screen. Holds Region's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/Object List/State exactly (owner:
...                 "reflect the current EC screen exactly the same way as the OV_BANK
...                 IUD related task") - replaces the older hardcoded-field-id pattern
...                 with the label-driven, properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${REGION_SCREEN}        Region
${REGION_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/region_insert.properties
${REGION_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/region_update.properties
${REGION_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/region_form_verify.properties
${REGION_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/region_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${REGION_TABLE}         ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Object List/State's convention.
${REGION_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Region's own form-field label set. Labels are "Region Code"/"Region Name" (screen-prefixed) -
# confirmed live 2026-08-22 via RF recon (tmp/recon_region_labels.robot) BEFORE building, per the
# lesson from State's live build (do not assume "Code"/"Name" is universal). Start Date
# deliberately excluded - Insert-only, not present in updateAttributes. Defined ONCE here so
# both Verify Region Record Exists (TC02) and Verify Region Record Found (TC04) share the same list.
@{REGION_FORM_LABELS}    Region Code    Region Name


*** Keywords ***
Find Region Row By Filter
    [Documentation]    Explicitly filter the Region grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Object List's explicit filter usage (owner, 2026-08-22: "same to
    ...    other ec screens"), rather than relying only on Select Object Row's implicit
    ...    3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${REGION_TABLE}    ${code}

Clear Region Row Filter
    [Documentation]    Clear the Code column filter (see Find Region Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${REGION_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Region's OWN credentials (${REGION_EC_USER}/
    ...    ${REGION_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so region_iud.robot's test cases read as a plain business
    ...    step; supplies Region's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${REGION_EC_USER}    ${REGION_EC_PASS}

Open Region Screen
    [Documentation]    Navigate to the Region screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${REGION_SCREEN}

Insert Region Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so region_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Object List/State. ${code_label}="Region Code" passed through so
    ...    T2 reads the resolved code back from the right properties-file key.
    [Arguments]    ${properties_path}=${REGION_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Region Code
    RETURN    ${code}

Verify Region Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Object List/State's TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Region Code/Region Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Region Row By Filter first, clears after (2026-08-23
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Region Row By Filter    ${code}
    Verify Object Insert Exists    ${REGION_TABLE}    ${code}    Region    ${REGION_INSERT_PROPERTIES}
    ...    @{REGION_FORM_LABELS}    code_label=Region Code
    Clear Region Row Filter

Update Region Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/
    ...    Object List/State. Filters via Find Region Row By Filter first, clears after
    ...    (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${REGION_UPDATE_PROPERTIES}
    Find Region Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${REGION_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Region Code
    Clear Region Row Filter
    RETURN    ${data}

Verify Region Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Object List/State's TC03 convention: the form shows
    ...    the updated Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Region Row By Filter
    ...    first, clears after (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Region Row By Filter    ${code}
    Verify Object Form Record    ${REGION_TABLE}    ${code}    Region    ${REGION_UPDATE_PROPERTIES}
    ...    Region Name    code_label=Region Code
    Clear Region Row Filter

Find Region Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Region Row By Filter first
    ...    (2026-08-23 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Region Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Region Row By Filter    ${code}
    Find Object Record    ${REGION_TABLE}    ${code}    Region    code_label=Region Code

Verify Region Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Region Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${REGION_TABLE}    ${code}    ${REGION_GRID_VERIFY_PROPERTIES}
    ...    ${REGION_FORM_VERIFY_PROPERTIES}    @{REGION_FORM_LABELS}
    Clear Region Row Filter

Delete Region Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the region, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Object List/State's convention.
    ...    Filters via Find Region Row By Filter first, clears after (2026-08-23
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Region Row By Filter    ${code}
    Delete Object Via End Date    ${REGION_TABLE}    ${REGION_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Region Row Filter

Verify Region Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${REGION_TABLE}    OV_REGION    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Region Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${REGION_TABLE}    ${code}
