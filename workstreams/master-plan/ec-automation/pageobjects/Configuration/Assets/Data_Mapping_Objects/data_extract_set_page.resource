*** Settings ***
Documentation       T3 (screen) - Data Extract Set page object.
...                 Screen: Configuration > Assets > Data_Mapping_Objects > Data Extract Set (SP.0049).
...                 Manage-Object (OV) screen. Holds Data Extract Set's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 10) to mirror Bank/Berth exactly - replaces the
...                 older label-driven-but-no-properties-file/no-filter pattern with the
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.
...                 NOTE: there is a SIBLING screen data_extract_setup_page.resource in this
...                 same folder - a DIFFERENT screen (Data Extract Setup, SP.0043), out of
...                 scope here, deliberately untouched.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DATA_EXTRACT_SET_SCREEN}    Data Extract Set
${DATA_EXTRACT_SET_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/data_extract_set_insert.properties
${DATA_EXTRACT_SET_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/data_extract_set_update.properties
${DATA_EXTRACT_SET_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/data_extract_set_form_verify.properties
${DATA_EXTRACT_SET_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/data_extract_set_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${DATA_EXTRACT_SET_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention
# (same objectdates row shape: Start Date C:1, End Date C:3 - not label-scannable per-row).
${DATA_EXTRACT_SET_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Data Extract Set's own form-field label set. Labels are GENERIC "Code"/"Name" (NOT
# screen-prefixed) - confirmed via ec-ui-knowledge/screens/data_extract_set.md (fresh scan
# 2026-07-26) and the already-proven Playwright driver py/data_extract_set_iud.py. Owner Class
# is mandatory at Insert (objectForm) but is NOT present in updateAttributes (confirmed via
# the SOW/KB: "Update (updateAttributes): Code (ro) - Name"), so it is deliberately excluded
# here - same pattern as Bank/Berth excluding their own Insert-only Start Date. Defined ONCE
# here so both Verify Data Extract Set Record Exists (TC02) and Verify Data Extract Set Record
# Found (TC04) share the same list.
@{DATA_EXTRACT_SET_FORM_LABELS}    Code    Name


*** Keywords ***
Find Data Extract Set Row By Filter
    [Documentation]    Explicitly filter the Data Extract Set grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/Berth's own explicit filter usage (owner, 2026-08-22: "others (Bank,
    ...    State, List_Object) should follow Account... utilise same filter feature"), rather
    ...    than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DATA_EXTRACT_SET_TABLE}    ${code}

Clear Data Extract Set Row Filter
    [Documentation]    Clear the Code column filter (see Find Data Extract Set Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${DATA_EXTRACT_SET_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Data Extract Set's OWN credentials
    ...    (${DATA_EXTRACT_SET_EC_USER}/${DATA_EXTRACT_SET_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so data_extract_set_iud.robot's test
    ...    cases read as a plain business step; supplies Data Extract Set's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${DATA_EXTRACT_SET_EC_USER}    ${DATA_EXTRACT_SET_EC_PASS}

Open Data Extract Set Screen
    [Documentation]    Navigate to the Data Extract Set screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${DATA_EXTRACT_SET_SCREEN}

Insert Data Extract Set Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so data_extract_set_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth.
    [Arguments]    ${properties_path}=${DATA_EXTRACT_SET_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Data Extract Set Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name only - Owner
    ...    Class is objectForm/Insert-only, not present in updateAttributes). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find Data Extract Set Row By Filter first, clears
    ...    after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Data Extract Set Row By Filter    ${code}
    Verify Object Insert Exists    ${DATA_EXTRACT_SET_TABLE}    ${code}    Data Extract Set
    ...    ${DATA_EXTRACT_SET_INSERT_PROPERTIES}    @{DATA_EXTRACT_SET_FORM_LABELS}
    Clear Data Extract Set Row Filter

Update Data Extract Set Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Berth. Filters via
    ...    Find Data Extract Set Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DATA_EXTRACT_SET_UPDATE_PROPERTIES}
    Find Data Extract Set Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DATA_EXTRACT_SET_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Data Extract Set Row Filter
    RETURN    ${data}

Verify Data Extract Set Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the shared
    ...    T2 Verify Object Form Record. Filters via Find Data Extract Set Row By Filter first,
    ...    clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Data Extract Set Row By Filter    ${code}
    Verify Object Form Record    ${DATA_EXTRACT_SET_TABLE}    ${code}    Data Extract Set
    ...    ${DATA_EXTRACT_SET_UPDATE_PROPERTIES}    Name
    Clear Data Extract Set Row Filter

Find Data Extract Set Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Data Extract Set Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Data Extract Set Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Data Extract Set Row By Filter    ${code}
    Find Object Record    ${DATA_EXTRACT_SET_TABLE}    ${code}    Data Extract Set

Verify Data Extract Set Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Data Extract
    ...    Set Record before this) AND left the Code filter active from that same call - clears
    ...    the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DATA_EXTRACT_SET_TABLE}    ${code}    ${DATA_EXTRACT_SET_GRID_VERIFY_PROPERTIES}
    ...    ${DATA_EXTRACT_SET_FORM_VERIFY_PROPERTIES}    @{DATA_EXTRACT_SET_FORM_LABELS}
    Clear Data Extract Set Row Filter

Delete Data Extract Set Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the data_extract_set, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End Date
    ...    is filled but BEFORE Save is clicked, matching Bank/Berth. Filters via Find Data
    ...    Extract Set Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Data Extract Set Row By Filter    ${code}
    Delete Object Via End Date    ${DATA_EXTRACT_SET_TABLE}    ${DATA_EXTRACT_SET_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Data Extract Set Row Filter

Verify Data Extract Set Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_SUMMARY_SET).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DATA_EXTRACT_SET_TABLE}    OV_SUMMARY_SET    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Data Extract Set Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DATA_EXTRACT_SET_TABLE}    ${code}
