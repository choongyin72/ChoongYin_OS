*** Settings ***
Documentation       T3 (screen) — Calculation Group Context page object.
...                 Screen: Configuration > Assets > Calculation_Objects > Calculation Group Context (CO.0245).
...                 Manage-Object (OV) screen. Holds Calculation Group Context's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common) — brought up to the
...                 full Bank-pattern shape (batch 7, 2026-08-23): properties-file-driven insert/
...                 update/verify + explicit grid-filter wiring, on top of the pre-existing
...                 label-driven Fill OV Field By Label mechanics (kept, not thrown away).
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped,
...                 per screen SOW screens/.../calculation_group_context_sow.md).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CALCULATION_GROUP_CONTEXT_SCREEN}    Calculation Group Context
${CALCULATION_GROUP_CONTEXT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_group_context_insert.properties
${CALCULATION_GROUP_CONTEXT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_group_context_update.properties
${CALCULATION_GROUP_CONTEXT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_group_context_form_verify.properties
${CALCULATION_GROUP_CONTEXT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_group_context_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${CALCULATION_GROUP_CONTEXT_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# The Code field's label on this screen is NOT the generic "Code" (unlike Bank) - it is
# "Calculation Group Context Code", confirmed via the pre-existing label-driven keywords below
# and the proven Python driver (py/calculation_group_context_iud.py INSERT_FIELDS). Threaded
# through as ${code_label} to every T2 keyword that needs it.
${CALCULATION_GROUP_CONTEXT_CODE_LABEL}    Calculation Group Context Code
# Calculation Group Context's own form-field label set for round-trip verification (Start Date
# deliberately excluded - it lives only in objectdates/the grid, not updateAttributes, matching
# Bank's own Start Date exclusion from its label set).
@{CALCULATION_GROUP_CONTEXT_FORM_LABELS}    Calculation Group Context Code    Calculation Group Context Name


*** Keywords ***
Find Calculation Group Context Row By Filter
    [Documentation]    Explicitly filter the Calculation Group Context grid's Code column to
    ...    ${code} via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank/Account's own explicit filter usage (batch 7, 2026-08-23: bringing this
    ...    screen up to the same full shape as bank_page.resource/customer_page.resource).
    [Arguments]    ${code}
    Find Object Row By Filter    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}

Clear Calculation Group Context Row Filter
    [Documentation]    Clear the Code column filter (see Find Calculation Group Context Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${CALCULATION_GROUP_CONTEXT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Calculation Group Context's OWN credentials
    ...    (${CALCULATION_GROUP_CONTEXT_EC_USER}/${CALCULATION_GROUP_CONTEXT_EC_PASS} from
    ...    credentials.py) on the current page - works whether this is the very first login (page
    ...    freshly loaded on the login form via the shared T1 Open EC Application) or a re-login
    ...    after Logout From EC Application. Matches Bank's per-TC login/logout convention
    ...    (batch 7, 2026-08-23).
    Login To EC Screen    ${CALCULATION_GROUP_CONTEXT_EC_USER}    ${CALCULATION_GROUP_CONTEXT_EC_PASS}

Open Calculation Group Context Screen
    [Documentation]    Navigate to the Calculation Group Context screen. Assumes the caller
    ...    already logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates and applies the navigator GO (grid needs GO to populate, no default rows on
    ...    open). Delegates to the shared T1 Open EC Screen (common.resource) for the actual
    ...    mechanics.
    Open EC Screen    ${CALCULATION_GROUP_CONTEXT_SCREEN}
    Apply Navigator

Insert Calculation Group Context Record And Save
    [Documentation]    Properties-file-driven insert (batch 7, 2026-08-23 addition, matching
    ...    Bank/Customer's full shape): opens New Object form, fills every field named in
    ...    ${properties_path} (Code/Name/Start Date + the 2 optional __FIRST__ dropdowns, all
    ...    auto-detected by kind), Saves, and asserts the resolved Code matches the suite's
    ...    ${TEST_CODE} - catching a properties-file/suite-variable drift immediately. Called
    ...    with ZERO arguments from the test case. The TC02 evidence screenshot is captured
    ...    BEFORE Save is clicked.
    [Arguments]    ${properties_path}=${CALCULATION_GROUP_CONTEXT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}
    RETURN    ${code}

Verify Calculation Group Context Record Exists
    [Documentation]    TC02 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}). PURE SCREEN verification: row exists in the grid, then every
    ...    field's LIVE SCREEN value is compared to testdata/calculation_group_context_insert.
    ...    properties (Code, Name - Start Date excluded, form-only field boundary). Delegates the
    ...    full sequence to the shared T2 Verify Object Insert Exists. Filters via Find
    ...    Calculation Group Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calculation Group Context Row By Filter    ${code}
    Verify Object Insert Exists    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}
    ...    Calculation Group Context    ${CALCULATION_GROUP_CONTEXT_INSERT_PROPERTIES}
    ...    @{CALCULATION_GROUP_CONTEXT_FORM_LABELS}    code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}
    Clear Calculation Group Context Row Filter

Update Calculation Group Context Record And Save
    [Documentation]    Properties-file-driven update (batch 7, 2026-08-23 addition), called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the applied
    ...    {label: value} dict so the caller can DB-verify against exactly what was set. Filters
    ...    via Find Calculation Group Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CALCULATION_GROUP_CONTEXT_UPDATE_PROPERTIES}
    Find Calculation Group Context Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}
    Clear Calculation Group Context Row Filter
    RETURN    ${data}

Verify Calculation Group Context Record Updated
    [Documentation]    TC03 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}). PURE SCREEN verification: selects the row (loading
    ...    updateAttributes), then compares Name's LIVE SCREEN value to testdata/
    ...    calculation_group_context_update.properties. Delegates to the shared T2 Verify Object
    ...    Form Record. Filters via Find Calculation Group Context Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calculation Group Context Row By Filter    ${code}
    Verify Object Form Record    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}
    ...    Calculation Group Context    ${CALCULATION_GROUP_CONTEXT_UPDATE_PROPERTIES}
    ...    Calculation Group Context Name    code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}
    Clear Calculation Group Context Row Filter

Find Calculation Group Context Record
    [Documentation]    TC04 select-step, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}). Delegates the full select+capture sequence to the shared T2
    ...    Find Object Record. Calls Find Calculation Group Context Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Calculation Group Context
    ...    Record Found (called right after) needs the grid still filtered.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calculation Group Context Row By Filter    ${code}
    Find Object Record    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}    Calculation Group Context
    ...    ${CALCULATION_GROUP_CONTEXT_CODE_LABEL}

Verify Calculation Group Context Record Found
    [Documentation]    TC04 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}): confirms BOTH the grid AND the full form record match the
    ...    expected data. Delegates to the shared T2 Verify Object Found. Caller must already
    ...    have selected the row (TC04 does, via Find Calculation Group Context Record before
    ...    this) AND left the Code filter active - clears the filter itself once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}
    ...    ${CALCULATION_GROUP_CONTEXT_GRID_VERIFY_PROPERTIES}
    ...    ${CALCULATION_GROUP_CONTEXT_FORM_VERIFY_PROPERTIES}
    ...    @{CALCULATION_GROUP_CONTEXT_FORM_LABELS}
    Clear Calculation Group Context Row Filter

Delete Calculation Group Context Record And Save
    [Documentation]    TC05, called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the calculation_group_context, set End Date = Start
    ...    Date (true delete), Save. Uses the pre-existing label-driven objectdates fill (kept
    ...    from before batch 7 - this screen's objectdates End Date resolves cleanly by label,
    ...    unlike Bank's documented two-fields-per-row exception). Filters via Find Calculation
    ...    Group Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Calculation Group Context Row By Filter    ${code}
    Select Object Row    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Capture Step    ${TEST NAME}_action
    Save
    Apply Navigator
    Clear Calculation Group Context Row Filter

Verify Calculation Group Context Record Removed
    [Documentation]    TC05 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}): confirms ${code} is absent from BOTH the grid and the database
    ...    (OV_CALC_GRP_CONTEXT). Delegates to the shared T2 Verify Object Removed.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CALCULATION_GROUP_CONTEXT_TABLE}    OV_CALC_GRP_CONTEXT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Calculation Group Context Record Does Not Exist
    [Documentation]    TC01 clean-state check, called with ZERO arguments (defaults ${code} to
    ...    the suite's ${TEST_CODE}). Delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CALCULATION_GROUP_CONTEXT_TABLE}    ${code}
