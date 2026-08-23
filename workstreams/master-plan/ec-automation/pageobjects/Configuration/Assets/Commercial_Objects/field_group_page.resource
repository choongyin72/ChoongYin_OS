*** Settings ***
Documentation       T3 (screen) — Field Group page object.
...                 Screen: Configuration > Assets > Commercial Objects > Field Group.
...                 Manage-Object (OV) screen, plain navigator (no mandatory nav scope -
...                 confirmed live 2026-08-23, matches docs/ec_screen_registry.md). Bank
...                 pattern: label-driven/properties-file-driven, delegating to T2
...                 (manage_object) and T1 (common) shared keywords, no hardcoded field ids
...                 except the objectdates End Date (documented precedent, see below).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${FIELD_GROUP_SCREEN}          Field Group
${FIELD_GROUP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/field_group_insert.properties
${FIELD_GROUP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/field_group_update.properties
${FIELD_GROUP_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/field_group_form_verify.properties
${FIELD_GROUP_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/field_group_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string
# (manage_object.resource defines this ONCE specifically so no T3 duplicates it). Confirmed live
# 2026-08-23 this screen's grid uses the same id as every other plain manage-object screen.
${FIELD_GROUP_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - matches Bank's own documented precedent (bank_page.resource) - LIVE-CONFIRMED
# 2026-08-23 for Field Group specifically via a throwaway recon script (row shape:
# Start Date C:1, End Date label C:2, End Date input C:3 - single row, unlike Bank's own
# combined-row shape but the SAME id pattern/column offsets).
${FIELD_GROUP_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Field Group's own form-field label set (Start Date deliberately excluded - it lives only in
# objectdates, not objectForm/updateAttributes comparison, matching Bank's own precedent).
# LIVE-CONFIRMED 2026-08-23 (objectForm recon): Code/Name/Start Date are the only MANDATORY
# fields; Description/Comments/Field Group Type (dropdown)/Reporting Field Group Indicator
# (checkbox) are all optional. Description is included here for business-realistic test data
# (matching Bank's own inclusion of optional descriptive fields) - the dropdown/checkbox are
# deliberately left untested (optional, not part of this screen's core IUD flow).
@{FIELD_GROUP_FORM_LABELS}    Code    Name    Description


*** Keywords ***
Find Field Group Row By Filter
    [Documentation]    Explicitly filter the Field Group grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    Bank/Account/Country's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${FIELD_GROUP_TABLE}    ${code}

Clear Field Group Row Filter
    [Documentation]    Clear the Code column filter (see Find Field Group Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${FIELD_GROUP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Field Group's OWN credentials (${FIELD_GROUP_EC_USER}/
    ...    ${FIELD_GROUP_EC_PASS} from credentials.py) on the current page. Screen-specific
    ...    wrapper supplying Field Group's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${FIELD_GROUP_EC_USER}    ${FIELD_GROUP_EC_PASS}

Open Field Group Screen
    [Documentation]    Navigate to the Field Group screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application). Delegates to the shared T1 Open EC
    ...    Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${FIELD_GROUP_SCREEN}

Insert Field Group Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so field_group_iud.robot's test case body
    ...    reads as a plain business step. Also owns the integrity check that the inserted Code
    ...    matches the suite's ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE
    ...    Save is clicked.
    [Arguments]    ${properties_path}=${FIELD_GROUP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Field Group Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/field_group_insert.properties - Code, Name, Description
    ...    (${FIELD_GROUP_FORM_LABELS}). Start Date is NOT verified here - it only exists as a
    ...    grid column / objectdates field, not an objectForm-comparable form field (matching
    ...    Bank's own precedent). Delegates the full sequence to the shared T2 Verify Object
    ...    Insert Exists. Filters via Find Field Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Group Row By Filter    ${code}
    Verify Object Insert Exists    ${FIELD_GROUP_TABLE}    ${code}    Field Group
    ...    ${FIELD_GROUP_INSERT_PROPERTIES}    @{FIELD_GROUP_FORM_LABELS}
    Clear Field Group Row Filter

Update Field Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via Find
    ...    Field Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${FIELD_GROUP_UPDATE_PROPERTIES}
    Find Field Group Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${FIELD_GROUP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Field Group Row Filter
    RETURN    ${data}

Verify Field Group Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Name/Description's LIVE
    ...    SCREEN value to testdata/field_group_update.properties. Delegates the full sequence to
    ...    the shared T2 Verify Object Form Record. Filters via Find Field Group Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Group Row By Filter    ${code}
    Verify Object Form Record    ${FIELD_GROUP_TABLE}    ${code}    Field Group
    ...    ${FIELD_GROUP_UPDATE_PROPERTIES}    Name    Description
    Clear Field Group Row Filter

Find Field Group Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Field
    ...    Group Row By Filter first, deliberately does NOT clear the filter afterward - Verify
    ...    Field Group Record Found (called right after) needs the grid still filtered.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Group Row By Filter    ${code}
    Find Object Record    ${FIELD_GROUP_TABLE}    ${code}    Field Group

Verify Field Group Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Delegates to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Field Group
    ...    Record before this) AND left the Code filter active - clears it here once both checks
    ...    are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${FIELD_GROUP_TABLE}    ${code}    ${FIELD_GROUP_GRID_VERIFY_PROPERTIES}
    ...    ${FIELD_GROUP_FORM_VERIFY_PROPERTIES}    @{FIELD_GROUP_FORM_LABELS}
    Clear Field Group Row Filter

Delete Field Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the field group, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked. Filters via Find Field Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Field Group Row By Filter    ${code}
    Delete Object Via End Date    ${FIELD_GROUP_TABLE}    ${FIELD_GROUP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Field Group Row Filter

Verify Field Group Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_FIELD_GROUP).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${FIELD_GROUP_TABLE}    ov_field_group    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Field Group Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${FIELD_GROUP_TABLE}    ${code}
