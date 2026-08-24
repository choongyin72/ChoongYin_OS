*** Settings ***
Documentation       T3 (screen) — Document Date Term page object.
...                 Screen: Configuration > Assets > Date Objects > Document Date Term (CD.0107).
...                 Manage-Object (OV) screen. Plain OV, same layout as Bank - the grid AUTO-LOADS
...                 on screen open (live recon 2026-08-24: 20 rows visible BEFORE any navigator GO
...                 click), unlike Disposition Type which needs GO to populate. The navigator's
...                 single date field is NOT a mandatory blocking gate - reclassified from this
...                 doc's own prior "Excluded" listing (see docs/bank-pattern-conversion-checklist.md,
...                 2026-08-24 entry). The New-Object form has two extra mandatory inputs beyond the
...                 universal Code/Name/Start-Date trio - a 'Date Calculation Method' autocomplete
...                 dropdown and a numeric 'Offset' cell (labels confirmed live 2026-08-24; the SOW's
...                 placeholder label "Method" was NOT the real live label).
...                 DELETE = End Date = Start Date (true delete; row leaves ov_doc_date_term).
...                 Converted to the full Bank-pattern shape (2026-08-24): was previously an OLD
...                 hardcoded-field-id build (Fill New Object Form with raw R:n:C:n ids, a generated
...                 unique AUTOTEST_DDT_<timestamp> code, one shared Suite Setup login, inline
...                 DB-verify calls in the test file, 4 TCs / no Find). Now matches
...                 bank_page.resource/berth_page.resource/disposition_type_page.resource exactly:
...                 properties-file-driven insert/update/verify, explicit grid-filter wiring, fixed
...                 test code, per-TC Login/Logout, 5 TCs, PURE SCREEN verification (no inline
...                 DB-verify in the T3/test file).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DDT_SCREEN}           Document Date Term
${DDT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/document_date_term_insert.properties
${DDT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/document_date_term_update.properties
${DDT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_date_term_form_verify.properties
${DDT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_date_term_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string
# (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${DDT_TABLE}            ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven —
# same documented precedent as Bank's own BANK_DEL_ENDDATE (the objectdates row packs TWO fields,
# Start Date C:1 / End Date C:3, a shape the one-field-per-row label scan cannot safely resolve).
${DDT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Document Date Term's own form-field label set (Start Date deliberately excluded from the
# updateAttributes verify - it lives only in objectForm/objectdates, not updateAttributes, same
# convention as Bank/Disposition Type). Labels are the GENERIC "Code"/"Name" (confirmed live
# 2026-08-24: NOT screen-prefixed, unlike Disposition Type's "Disposition Code"/"Disposition
# Name"). Defined ONCE here so both Verify Document Date Term Record Exists (TC02) and Verify
# Document Date Term Record Found (TC04) share the same list.
@{DDT_FORM_LABELS}      Code    Name


*** Keywords ***
Find Document Date Term Row By Filter
    [Documentation]    Explicitly filter the Document Date Term grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Disposition Type's own explicit filter usage, rather than relying only on Select
    ...    Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DDT_TABLE}    ${code}

Clear Document Date Term Row Filter
    [Documentation]    Clear the Code column filter (see Find Document Date Term Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${DDT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Document Date Term's OWN credentials
    ...    (${DOCUMENT_DATE_TERM_EC_USER}/${DOCUMENT_DATE_TERM_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab). Screen-specific wrapper (matches
    ...    Bank's convention: document_date_term_iud.robot's test cases call this with ZERO
    ...    arguments) that supplies Document Date Term's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${DOCUMENT_DATE_TERM_EC_USER}    ${DOCUMENT_DATE_TERM_EC_PASS}

Open Document Date Term Screen
    [Documentation]    Navigate to the Document Date Term screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates,
    ...    matching Bank's per-TC Login/Open/action/Logout convention. No navigator GO click here -
    ...    live recon (2026-08-24) confirmed the grid auto-loads (20 rows visible immediately on
    ...    screen open, unchanged after GO), the same shape as Bank, not Disposition Type's
    ...    GO-to-populate shape.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${DDT_SCREEN}

Insert Document Date Term Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, purely so
    ...    document_date_term_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Every field named in ${DDT_INSERT_PROPERTIES} (Code, Name, Start Date, Date Calculation
    ...    Method, Offset) is filled by label, auto-detecting kind (text/date/dropdown) - the
    ...    dropdown/numeric extras need no special-case code here, T2's Fill OV Field By Label Any
    ...    Kind already resolves them. Also owns the integrity check that the inserted Code matches
    ...    the suite's ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is
    ...    clicked (passed through to Insert Object From Properties, which fills every field
    ...    first).
    [Arguments]    ${properties_path}=${DDT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Document Date Term Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/document_date_term_insert.properties (the file used to
    ...    insert, not the post-update document_date_term_form_verify.properties) - Code, Name
    ...    (${DDT_FORM_LABELS}). NOTE: Start Date/Date Calculation Method/Offset are NOT verified
    ...    here - they only exist as objectForm/objectdates/grid-column fields, not updateAttributes
    ...    fields (matches Bank's/Disposition Type's own convention). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Filters via Find Document Date Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Date Term Row By Filter    ${code}
    Verify Object Insert Exists    ${DDT_TABLE}    ${code}    Document Date Term
    ...    ${DDT_INSERT_PROPERTIES}    @{DDT_FORM_LABELS}
    Clear Document Date Term Row Filter

Update Document Date Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked (passed through to
    ...    Update Object From Properties, which fills every field first). Filters via Find
    ...    Document Date Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DDT_UPDATE_PROPERTIES}
    Find Document Date Term Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DDT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Document Date Term Row Filter
    RETURN    ${data}

Verify Document Date Term Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Name's LIVE SCREEN value (via
    ...    Get OV Field Value By Label) to testdata/document_date_term_update.properties - only
    ...    that label, since that's the only field that file has. Delegates the full sequence
    ...    (select, form-compare, screenshot) to the shared T2 Verify Object Form Record. Filters
    ...    via Find Document Date Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Date Term Row By Filter    ${code}
    Verify Object Form Record    ${DDT_TABLE}    ${code}    Document Date Term
    ...    ${DDT_UPDATE_PROPERTIES}    Name
    Clear Document Date Term Row Filter

Find Document Date Term Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Document Date Term Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Document Date Term Record Found (called
    ...    right after, same TC) needs the grid still filtered to ${code} for its own grid-check,
    ...    since it doesn't re-select the row itself; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Date Term Row By Filter    ${code}
    Find Object Record    ${DDT_TABLE}    ${code}    Document Date Term

Verify Document Date Term Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND the
    ...    full form record match the expected data - the SAME two existing live-DOM round-trip
    ...    keywords, just called under one name. Also captures the TC04 evidence screenshot.
    ...    Delegates the full sequence (grid-compare, form-compare, screenshot) to the shared T2
    ...    Verify Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Document Date Term Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DDT_TABLE}    ${code}    ${DDT_GRID_VERIFY_PROPERTIES}
    ...    ${DDT_FORM_VERIFY_PROPERTIES}    @{DDT_FORM_LABELS}
    Clear Document Date Term Row Filter

Delete Document Date Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the Document Date Term, set End Date = Start Date (true delete), Save. Captures
    ...    the TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked - showing the data as entered, not the after-save/reloaded-grid state. Filters
    ...    via Find Document Date Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Document Date Term Row By Filter    ${code}
    Delete Object Via End Date    ${DDT_TABLE}    ${DDT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Document Date Term Row Filter

Verify Document Date Term Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database - the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DDT_TABLE}    OV_DOC_DATE_TERM    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Document Date Term Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DDT_TABLE}    ${code}
