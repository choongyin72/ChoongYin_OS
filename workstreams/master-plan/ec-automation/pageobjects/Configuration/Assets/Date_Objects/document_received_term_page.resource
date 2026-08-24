*** Settings ***
Documentation       T3 (screen) — Document Received Term page object.
...                 Screen: Configuration > Assets > Date Objects > Document Received Term (CD.0108).
...                 Manage-Object (OV, date-effective) screen. Rebuilt 2026-08-24 to mirror
...                 Bank/Port/Berth exactly - replaces the older hardcoded-field-id
...                 (`Fill New Object Form`) pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.
...                 Live navigator scan (2026-08-24) confirmed the navigator's single date
...                 field is OPTIONAL (mandatory=False) + GO — same shape as Bank/Report Area/
...                 Port, NOT a genuine mandatory-date gate (corrects this screen's grouping
...                 alongside Document Date Term/Payment Term/Choke/Choke Model in
...                 docs/bank-pattern-conversion-checklist.md's "Excluded" table).
...                 Richer than plain Bank: the New-Object form has two extra mandatory
...                 inputs beyond the universal Code/Name/Start-Date trio — a "Date
...                 Calculation Method" autocomplete dropdown and a numeric "Offset" field
...                 (both confirmed via a live objectForm field-inventory scan, 2026-08-24;
...                 labels are GENERIC "Code"/"Name", NOT screen-prefixed).
...                 DELETE = End Date = Start Date (true delete; row leaves OV_DOC_RECEIVED_TERM).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DRT_SCREEN}           Document Received Term
${DRT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/document_received_term_insert.properties
${DRT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/document_received_term_update.properties
${DRT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_received_term_form_verify.properties
${DRT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_received_term_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${DRT_TABLE}            ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth/Port's convention.
${DRT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Document Received Term's own form-field label set. Labels are GENERIC "Code"/"Name" (NOT
# screen-prefixed) - confirmed via a live objectForm field-inventory scan (2026-08-24). Date
# Calculation Method/Offset deliberately excluded (mandatory dropdown + numeric field, not
# round-trip-checked here - same convention as Carrier's Unit dropdown). Defined ONCE here so
# both Verify Document Received Term Record Exists (TC02) and Verify Document Received Term
# Record Found (TC04) share the same list.
@{DRT_FORM_LABELS}      Code    Name


*** Keywords ***
Find Document Received Term Row By Filter
    [Documentation]    Explicitly filter the Document Received Term grid's Code column to
    ...    ${code} via the shared T2 Find Object Row By Filter (resources/manage_object.resource)
    ...    - matches Bank/Berth/Port's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DRT_TABLE}    ${code}

Clear Document Received Term Row Filter
    [Documentation]    Clear the Code column filter (see Find Document Received Term Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${DRT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Document Received Term's OWN credentials
    ...    (${DOCUMENT_RECEIVED_TERM_EC_USER}/${DOCUMENT_RECEIVED_TERM_EC_PASS} from
    ...    credentials.py) on the current page. Standing decision (owner, 2026-08-22): every
    ...    EC screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    document_received_term_iud.robot's test cases read as a plain business step,
    ...    supplies Document Received Term's own credential defaults to the shared T1 Login
    ...    To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${DOCUMENT_RECEIVED_TERM_EC_USER}    ${DOCUMENT_RECEIVED_TERM_EC_PASS}

Open Document Received Term Screen
    [Documentation]    Navigate to the Document Received Term screen. Assumes the caller
    ...    already logged in this test case (via Login To EC Application) - this keyword
    ...    ONLY navigates. Delegates to the shared T1 Open EC Screen (common.resource) for
    ...    the actual mechanics.
    Open EC Screen    ${DRT_SCREEN}

Insert Document Received Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so document_received_term_iud.robot's test case body reads as a
    ...    plain business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth/Port.
    [Arguments]    ${properties_path}=${DRT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Code
    RETURN    ${code}

Verify Document Received Term Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth/Port's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Code/Name only -
    ...    Start Date is grid/insert-only, not present in updateAttributes). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists. Filters via Find Document Received Term Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Received Term Row By Filter    ${code}
    Verify Object Insert Exists    ${DRT_TABLE}    ${code}    Document Received Term
    ...    ${DRT_INSERT_PROPERTIES}    @{DRT_FORM_LABELS}    code_label=Code
    Clear Document Received Term Row Filter

Update Document Received Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth/Port. Filters via Find Document Received Term Row By Filter first,
    ...    clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DRT_UPDATE_PROPERTIES}
    Find Document Received Term Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DRT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Code
    Clear Document Received Term Row Filter
    RETURN    ${data}

Verify Document Received Term Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth/Port's TC03 convention: the form shows the
    ...    updated Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Document Received Term
    ...    Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Received Term Row By Filter    ${code}
    Verify Object Form Record    ${DRT_TABLE}    ${code}    Document Received Term
    ...    ${DRT_UPDATE_PROPERTIES}    Name    code_label=Code
    Clear Document Received Term Row Filter

Find Document Received Term Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Document Received Term Row
    ...    By Filter first (2026-08-22 standardisation). Deliberately does NOT clear the
    ...    filter afterward - Verify Document Received Term Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check, since it
    ...    doesn't re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Received Term Row By Filter    ${code}
    Find Object Record    ${DRT_TABLE}    ${code}    Document Received Term    code_label=Code

Verify Document Received Term Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Document
    ...    Received Term Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DRT_TABLE}    ${code}    ${DRT_GRID_VERIFY_PROPERTIES}
    ...    ${DRT_FORM_VERIFY_PROPERTIES}    @{DRT_FORM_LABELS}
    Clear Document Received Term Row Filter

Delete Document Received Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the object, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth/Port's convention. Filters
    ...    via Find Document Received Term Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Document Received Term Row By Filter    ${code}
    Delete Object Via End Date    ${DRT_TABLE}    ${DRT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Document Received Term Row Filter

Verify Document Received Term Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DRT_TABLE}    OV_DOC_RECEIVED_TERM    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Document Received Term Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DRT_TABLE}    ${code}
