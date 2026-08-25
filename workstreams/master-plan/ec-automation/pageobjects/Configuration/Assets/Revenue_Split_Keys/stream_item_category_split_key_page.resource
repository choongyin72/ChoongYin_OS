*** Settings ***
Documentation       T3 (screen) — Stream Item Category Split Key page object.
...                 Screen: Configuration > Assets > Revenue Split Keys > Stream Item
...                 Category Split Key (CD.0042). Custom-URL OV (no navigator/GO at all -
...                 reload via toolbar Refresh, confirmed live 2026-08-25: navigator
...                 fields=[], go=['navButton:form:B'] present but not needed - the grid
...                 renders directly on open with no nav fields to fill; grid id is
...                 nav:form:T_data - matches Report Context/WBS/Calendar, NOT the
...                 manage-object manage_object_nav_nav:form:T_data + GO variant).
...                 CLASS_NAME=SPLIT_KEY, CLASS_TYPE=OBJECT, TIME_SCOPE_CODE=VERSIONED, base
...                 table SPLIT_KEY, version table SPLIT_KEY_VERSION, view OV_SPLIT_KEY.
...                 URL: /com.ec.revn.cd/manage_object_split_key/CLASS_NAME/SPLIT_KEY/
...                 SPLIT_TYPE/STREAM_ITEM_CATEGORY (confirmed live 2026-08-25).
...                 IMPORTANT - shared-view collision risk: OV_SPLIT_KEY is the SAME base
...                 view written to by 6 sibling "Split Key" screens (Product/Company/Field/
...                 Stream Item Category/Other/Stream Item), differentiated only by
...                 SPLIT_TYPE (server-set from which menu entry is opened, not a form
...                 field). This screen's own test code (AUTOTEST_SPLITKEY_STREAMCAT) is
...                 deliberately scoped to avoid colliding with the other 5 screens' own
...                 fixed test codes built in parallel.
...                 Brand-new build 2026-08-25 (no prior automation existed for any of the 6
...                 sibling Split Key screens) - built directly to the label-driven,
...                 properties-file-driven, T2-consolidated pattern matching Bank/Report
...                 Context (ec-bank-pattern-new-screen skill). Do NOT confuse with "Split
...                 Item Other" (CD.0017, different URL controller manage_object_nav, view
...                 OV_SPLIT_ITEM_OTHER, already built at split_item_other_page.resource -
...                 untouched by this build) or plain "Stream Item Category" (a different,
...                 already-built, unrelated screen - untouched by this build).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STREAM_ITEM_CATEGORY_SPLIT_KEY_SCREEN}    Stream Item Category Split Key
${SICSK_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_category_split_key_insert.properties
${SICSK_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_category_split_key_update.properties
${SICSK_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_category_split_key_form_verify.properties
${SICSK_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_category_split_key_grid_verify.properties
# Grid id: this screen is a custom-URL OV - grid is nav:form:T_data (NOT the manage-object
# manage_object_nav_nav:form:T_data variant) and there is NO navigator field to fill (a GO
# button DOM node exists but no navigator field requires it - confirmed live 2026-08-25:
# navigator fields=[]). T2's Save And Refresh List auto-detects this (falls back to toolbar
# Refresh) - matches Report Context/WBS/Calendar/Account.
${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Report Context's
# convention - framework-invariant objectdates layout (R:0:C:1 = Start Date, R:0:C:3 = End
# Date).
${SICSK_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# This screen's own form-field label set. Labels are "Split Key Code"/"Split Key Name"
# (screen-prefixed, confirmed live 2026-08-25 via both the New Object form (objectForm) and
# the row-select form (updateAttributes) label dumps). Start Date deliberately excluded -
# Insert-only, not present in updateAttributes. The objectForm also has End Date/Description/
# Comments/Value Method/Shares add to 100%/Rounding Rule/Number of Rounding Decimals/Number
# Display Format - all confirmed optional (not mandatory-yellow) live and deliberately
# omitted (IUD-fill-only-needed-fields convention).
@{SICSK_FORM_LABELS}    Split Key Code    Split Key Name


*** Keywords ***
Find Stream Item Category Split Key Row By Filter
    [Documentation]    Explicitly filter the Stream Item Category Split Key grid's Code
    ...    column to ${code} via the shared T2 Find Object Row By Filter
    ...    (resources/manage_object.resource) - matches Bank/Report Context's own explicit
    ...    filter usage, rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}

Clear Stream Item Category Split Key Row Filter
    [Documentation]    Clear the Code column filter (see Find Stream Item Category Split Key
    ...    Row By Filter) via the shared T2 Clear Object Row Filter, restoring the grid's
    ...    normal unfiltered view.
    Clear Object Row Filter    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as this screen's OWN credentials
    ...    (${STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_USER}/${STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_PASS}
    ...    from credentials.py) on the current page. Standing decision: every EC screen gets
    ...    its own dedicated credential pair. Zero-argument wrapper so
    ...    stream_item_category_split_key_iud.robot's test cases read as a plain business
    ...    step; supplies this screen's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_USER}    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_PASS}

Open Stream Item Category Split Key Screen
    [Documentation]    Navigate to the Stream Item Category Split Key screen. Assumes the
    ...    caller already logged in this test case (via Login To EC Application) - this
    ...    keyword ONLY navigates. Delegates to the shared T1 Open EC Screen
    ...    (common.resource) for the actual mechanics. Deliberately does NOT click any GO
    ...    button or call Apply Navigator - live scan 2026-08-25 confirmed this screen has no
    ...    navigator field to fill (fields=[]); the grid (nav:form:T_data) renders directly
    ...    on open, same as Report Context/WBS/Calendar/Account.
    Open EC Screen    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_SCREEN}

Insert Stream Item Category Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so stream_item_category_split_key_iud.robot's test case body
    ...    reads as a plain business step with ZERO arguments. Also checks the inserted Code
    ...    matches the suite's ${TEST_CODE}. Pre-save evidence screenshot captured before
    ...    Save is clicked, matching Bank/Report Context. ${code_label} passed as "Split Key
    ...    Code" since this screen's Code label is screen-prefixed, not the generic "Code".
    [Arguments]    ${properties_path}=${SICSK_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Split Key Code
    RETURN    ${code}

Verify Stream Item Category Split Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Report Context's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (Split Key
    ...    Code/Split Key Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find Stream
    ...    Item Category Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Category Split Key Row By Filter    ${code}
    Verify Object Insert Exists    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}
    ...    Stream Item Category Split Key    ${SICSK_INSERT_PROPERTIES}
    ...    @{SICSK_FORM_LABELS}    code_label=Split Key Code
    Clear Stream Item Category Split Key Row Filter

Update Stream Item Category Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Report
    ...    Context. Filters via Find Stream Item Category Split Key Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    ...    ${properties_path}=${SICSK_UPDATE_PROPERTIES}
    Find Stream Item Category Split Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=Split Key Code
    Clear Stream Item Category Split Key Row Filter
    RETURN    ${data}

Verify Stream Item Category Split Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Report Context's TC03 convention: the form shows the
    ...    updated Split Key Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Stream
    ...    Item Category Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Category Split Key Row By Filter    ${code}
    Verify Object Form Record    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}
    ...    Stream Item Category Split Key    ${SICSK_UPDATE_PROPERTIES}
    ...    Split Key Name    code_label=Split Key Code
    Clear Stream Item Category Split Key Row Filter

Find Stream Item Category Split Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Stream Item Category Split
    ...    Key Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Stream Item Category Split Key Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Category Split Key Row By Filter    ${code}
    Find Object Record    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}
    ...    Stream Item Category Split Key    code_label=Split Key Code

Verify Stream Item Category Split Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Stream Item Category Split Key Record before this) AND left the Code filter
    ...    active from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}
    ...    ${SICSK_GRID_VERIFY_PROPERTIES}
    ...    ${SICSK_FORM_VERIFY_PROPERTIES}
    ...    @{SICSK_FORM_LABELS}
    Clear Stream Item Category Split Key Row Filter

Delete Stream Item Category Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the split key, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Report Context's convention.
    ...    Filters via Find Stream Item Category Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Stream Item Category Split Key Row By Filter    ${code}
    Delete Object Via End Date    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}
    ...    ${SICSK_DEL_ENDDATE}    ${code}    ${date}    ${TEST NAME}_action
    Clear Stream Item Category Split Key Row Filter

Verify Stream Item Category Split Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    OV_SPLIT_KEY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Stream Item Category Split Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STREAM_ITEM_CATEGORY_SPLIT_KEY_TABLE}    ${code}
