*** Settings ***
Documentation       T3 (screen) - Data Extract Setup page object.
...                 Screen: Configuration > Assets > Data_Mapping_Objects > Data Extract Setup (SP.0043).
...                 Manage-Object (OV) screen. Holds Data Extract Setup's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-25 to mirror Bank/State/Data Extract Set exactly - replaces the
...                 older label-driven-but-no-properties-file/no-filter/timestamp-code pattern
...                 (generator-scaffolded 2026-07-26, which also had an inline
...                 `Field Should Equal In View` DB-verify call directly in the .robot file) with
...                 the properties-file-driven, grid-filter-wired, T2-consolidated,
...                 pure-screen-verification pattern.
...                 NOTE: there is a SIBLING screen data_extract_set_page.resource in this same
...                 folder - a DIFFERENT screen (Data Extract Set, SP.0049), out of scope here.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DATA_EXTRACT_SETUP_SCREEN}    Data Extract Setup
${DATA_EXTRACT_SETUP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/data_extract_setup_insert.properties
${DATA_EXTRACT_SETUP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/data_extract_setup_update.properties
${DATA_EXTRACT_SETUP_FORM_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/data_extract_setup_form_verify.properties
${DATA_EXTRACT_SETUP_GRID_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/data_extract_setup_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${DATA_EXTRACT_SETUP_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Data Extract Set's
# convention (same objectdates row shape: Start Date C:1, End Date C:3 - not label-scannable
# per-row).
${DATA_EXTRACT_SETUP_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Data Extract Setup's own form-field label set. Labels are SCREEN-PREFIXED "Data Extract Setup
# Code"/"Data Extract Setup Name" (NOT generic "Code"/"Name") - confirmed via
# ec-ui-knowledge/screens/data_extract_setup.md (fresh scan 2026-07-26) and the New Object form
# screenshot (DeepDiveLearnings/ec-screens/notes/SP.0043_shot_1.png). Data Extract Type is
# mandatory at Insert (objectForm) but is NOT present in updateAttributes (confirmed via the KB:
# "Update (updateAttributes): Data Extract Setup Code (ro) - Data Extract Setup Name"), so it is
# deliberately excluded here - same pattern as Bank/Berth/Data Extract Set excluding their own
# Insert-only mandatory dropdown. Defined ONCE here so both Verify Data Extract Setup Record
# Exists (TC02) and Verify Data Extract Setup Record Found (TC04) share the same list.
@{DATA_EXTRACT_SETUP_FORM_LABELS}    Data Extract Setup Code    Data Extract Setup Name


*** Keywords ***
Find Data Extract Setup Row By Filter
    [Documentation]    Explicitly filter the Data Extract Setup grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Data Extract Set's own explicit filter usage (owner, 2026-08-22:
    ...    "others (Bank, State, List_Object) should follow Account... utilise same filter
    ...    feature"), rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DATA_EXTRACT_SETUP_TABLE}    ${code}

Clear Data Extract Setup Row Filter
    [Documentation]    Clear the Code column filter (see Find Data Extract Setup Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${DATA_EXTRACT_SETUP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Data Extract Setup's OWN credentials
    ...    (${DATA_EXTRACT_SETUP_EC_USER}/${DATA_EXTRACT_SETUP_EC_PASS} from credentials.py) on
    ...    the current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so data_extract_setup_iud.robot's
    ...    test cases read as a plain business step; supplies Data Extract Setup's own
    ...    credential defaults to the shared T1 Login To EC Screen (common.resource), which owns
    ...    the actual login mechanics.
    Login To EC Screen    ${DATA_EXTRACT_SETUP_EC_USER}    ${DATA_EXTRACT_SETUP_EC_PASS}

Open Data Extract Setup Screen
    [Documentation]    Navigate to the Data Extract Setup screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${DATA_EXTRACT_SETUP_SCREEN}

Insert Data Extract Setup Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so data_extract_setup_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/State/Data Extract Set.
    [Arguments]    ${properties_path}=${DATA_EXTRACT_SETUP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Data Extract Setup Code
    RETURN    ${code}

Verify Data Extract Setup Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State/Data Extract Set's TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Data Extract Setup Code/Name only - Data Extract Type is objectForm/Insert-only, not
    ...    present in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists. Filters via
    ...    Find Data Extract Setup Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Data Extract Setup Row By Filter    ${code}
    Verify Object Insert Exists    ${DATA_EXTRACT_SETUP_TABLE}    ${code}    Data Extract Setup
    ...    ${DATA_EXTRACT_SETUP_INSERT_PROPERTIES}    @{DATA_EXTRACT_SETUP_FORM_LABELS}
    ...    code_label=Data Extract Setup Code
    Clear Data Extract Setup Row Filter

Update Data Extract Setup Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/State/Data
    ...    Extract Set. Filters via Find Data Extract Setup Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DATA_EXTRACT_SETUP_UPDATE_PROPERTIES}
    Find Data Extract Setup Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DATA_EXTRACT_SETUP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Data Extract Setup Code
    Clear Data Extract Setup Row Filter
    RETURN    ${data}

Verify Data Extract Setup Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State/Data Extract Set's TC03 convention: the form shows
    ...    the updated Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Data Extract Setup Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Data Extract Setup Row By Filter    ${code}
    Verify Object Form Record    ${DATA_EXTRACT_SETUP_TABLE}    ${code}    Data Extract Setup
    ...    ${DATA_EXTRACT_SETUP_UPDATE_PROPERTIES}    Data Extract Setup Name
    ...    code_label=Data Extract Setup Code
    Clear Data Extract Setup Row Filter

Find Data Extract Setup Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Data Extract Setup Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Data Extract Setup Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Data Extract Setup Row By Filter    ${code}
    Find Object Record    ${DATA_EXTRACT_SETUP_TABLE}    ${code}    Data Extract Setup
    ...    code_label=Data Extract Setup Code

Verify Data Extract Setup Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Data Extract
    ...    Setup Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DATA_EXTRACT_SETUP_TABLE}    ${code}    ${DATA_EXTRACT_SETUP_GRID_VERIFY_PROPS}
    ...    ${DATA_EXTRACT_SETUP_FORM_VERIFY_PROPS}    @{DATA_EXTRACT_SETUP_FORM_LABELS}
    Clear Data Extract Setup Row Filter

Delete Data Extract Setup Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the data_extract_setup, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End Date
    ...    is filled but BEFORE Save is clicked, matching Bank/State/Data Extract Set. Filters
    ...    via Find Data Extract Setup Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Data Extract Setup Row By Filter    ${code}
    Delete Object Via End Date    ${DATA_EXTRACT_SETUP_TABLE}    ${DATA_EXTRACT_SETUP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Data Extract Setup Row Filter

Verify Data Extract Setup Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_SUMMARY_SETUP).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DATA_EXTRACT_SETUP_TABLE}    OV_SUMMARY_SETUP    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Data Extract Setup Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DATA_EXTRACT_SETUP_TABLE}    ${code}
