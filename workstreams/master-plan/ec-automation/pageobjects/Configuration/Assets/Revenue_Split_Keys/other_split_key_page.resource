*** Settings ***
Documentation       T3 (screen) — Other Split Key page object.
...                 Screen: Configuration > Assets > Revenue Split Keys > Other Split Key
...                 (BF_CODE CD.0046, class SPLIT_KEY, view OV_SPLIT_KEY). Custom-URL OV screen
...                 (grid id nav:form:T_data, NO gating navigator/GO - confirmed live 2026-08-25
...                 via tmp/scripts/_recon_other_split_key5.py: 7 existing rows render
...                 immediately on open, before any GO/navButton click) - same shape as Product
...                 Split Key (CD.0036, product_split_key_page.resource), used as this build's
...                 clone template. Label-driven, properties-file-driven, T2-consolidated
...                 pattern (bank_page.resource/cost_centre_page.resource style).
...
...                 One of 6 sibling "* Split Key" screens (Product/Company/Field/Stream Item
...                 Category/Other/Stream Item) that ALL share the SAME underlying class
...                 (SPLIT_KEY) and base view (OV_SPLIT_KEY), differentiated only by a
...                 server-side SPLIT_TYPE value bound to which menu entry/URL is opened
...                 (this screen's own real URL, confirmed live via page.url capture:
...                 manage_object_split_key/CLASS_NAME/SPLIT_KEY/SPLIT_TYPE/SPLIT_ITEM_OTHER).
...                 Each sibling screen is built independently with its OWN distinctly-scoped
...                 fixed test code (this one: AUTOTEST_SPLITKEY_OTHER, confirmed free in
...                 OV_SPLIT_KEY via a fresh DB query before use, and confirmed to not collide
...                 with any AUTOTEST_SPLITKEY% code from the 5 parallel sibling builds) to
...                 avoid cross-screen collision on the shared view - do NOT reuse a generic
...                 "AUTOTEST_SPLIT_KEY" code for any of the 6.
...
...                 NOT the same screen as "Split Item Other" (CD.0017,
...                 pageobjects/.../split_item_other_page.resource, same folder) - that is a
...                 DIFFERENT, already-built, standalone screen on class SPLIT_ITEM_OTHER via
...                 the plain manage_object_nav controller, unrelated to this build. Also NOT
...                 "Other Split Key Shares" (CD.0047, a related but genuinely different
...                 percentage-share screen, not built this round) - only "Other Split Key"
...                 itself (CD.0046) is covered here.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${OTHER_SPLIT_KEY_SCREEN}    Other Split Key
${OTHER_SPLIT_KEY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/other_split_key_insert.properties
${OTHER_SPLIT_KEY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/other_split_key_update.properties
${OTHER_SPLIT_KEY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/other_split_key_form_verify.properties
${OTHER_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/other_split_key_grid_verify.properties
# Grid id: CUSTOM-URL OV (not manage-object) - own constant, NOT T2's ${OV_MANAGE_OBJECT_TABLE}.
# Confirmed live 2026-08-25 (tmp/scripts/_recon_other_split_key4.py/_recon_other_split_key5.py):
# nav:form:T_data, 7 existing rows render immediately (no gating GO needed); a navButton:form:B
# exists but is not a gating navigator, matching Product Split Key's own finding exactly.
${OTHER_SPLIT_KEY_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Product Split Key's
# framework-invariant objectdates layout (Start Date C:1, End Date C:3).
${OTHER_SPLIT_KEY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Confirmed live 2026-08-25 (tmp/scripts/_recon_other_split_key3.py): the Code/Name labels on
# THIS screen are "Split Key Code"/"Split Key Name" (screen-prefixed), NOT the generic
# "Code"/"Name" Bank/Cost Centre use.
${OTHER_SPLIT_KEY_CODE_LABEL}    Split Key Code
# Form-field label set for the full-record compare (Verify Object Insert Exists/Verify Object
# Form Record). Start Date deliberately excluded - Insert-only (objectdates), not present in
# updateAttributes. Description/Comments/Value Method/Shares add to 100%/Rounding Rule/Number
# of Rounding Decimals/Number Display Format all confirmed live (screenshot-verified white
# background, several pre-defaulted) as NOT mandatory on the pristine Insert form and are left
# out of the round-trip compare - not filled with a specific asserted value this build.
@{OTHER_SPLIT_KEY_FORM_LABELS}    Split Key Code    Split Key Name


*** Keywords ***
Find Other Split Key Row By Filter
    [Documentation]    Explicitly filter the Other Split Key grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    Bank/Product Split Key's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${OTHER_SPLIT_KEY_TABLE}    ${code}

Clear Other Split Key Row Filter
    [Documentation]    Clear the Code column filter (see Find Other Split Key Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${OTHER_SPLIT_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Other Split Key's OWN credentials
    ...    (${OTHER_SPLIT_KEY_EC_USER}/${OTHER_SPLIT_KEY_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login or a re-login after Logout
    ...    From EC Application. Screen-specific wrapper (matches Bank/Product Split Key's
    ...    convention) supplying this screen's own credential defaults to the shared T1 Login
    ...    To EC Screen (common.resource), which owns the actual mechanics.
    Login To EC Screen    ${OTHER_SPLIT_KEY_EC_USER}    ${OTHER_SPLIT_KEY_EC_PASS}

Open Other Split Key Screen
    [Documentation]    Navigate to the Other Split Key screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource). No gating
    ...    navigator/GO step needed - the grid loads immediately (confirmed live: 7 existing
    ...    rows render before any GO/navButton click).
    Open EC Screen    ${OTHER_SPLIT_KEY_SCREEN}

Insert Other Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so other_split_key_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments - the underlying mechanics (properties-file-driven insert,
    ...    auto-detecting each field's kind by label) are UNCHANGED. Also checks the inserted
    ...    Code matches the suite's ${TEST_CODE}. Pre-save evidence screenshot captured before
    ...    Save is clicked.
    [Arguments]    ${properties_path}=${OTHER_SPLIT_KEY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${OTHER_SPLIT_KEY_CODE_LABEL}
    RETURN    ${code}

Verify Other Split Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Product Split Key's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (Split Key
    ...    Code/Name - ${OTHER_SPLIT_KEY_FORM_LABELS}). Delegates the full sequence (row-check,
    ...    select, form-compare, screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Other Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Other Split Key Row By Filter    ${code}
    Verify Object Insert Exists    ${OTHER_SPLIT_KEY_TABLE}    ${code}    Other Split Key
    ...    ${OTHER_SPLIT_KEY_INSERT_PROPERTIES}    @{OTHER_SPLIT_KEY_FORM_LABELS}
    ...    code_label=${OTHER_SPLIT_KEY_CODE_LABEL}
    Clear Other Split Key Row Filter

Update Other Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can compare against exactly what was
    ...    set. Pre-save evidence screenshot captured before Save is clicked. Filters via Find
    ...    Other Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${OTHER_SPLIT_KEY_UPDATE_PROPERTIES}
    Find Other Split Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${OTHER_SPLIT_KEY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${OTHER_SPLIT_KEY_CODE_LABEL}
    Clear Other Split Key Row Filter
    RETURN    ${data}

Verify Other Split Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification: selects the row (loading updateAttributes), then compares Split Key
    ...    Name's LIVE SCREEN value to testdata/other_split_key_update.properties. Delegates
    ...    the full sequence (select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Form Record. Filters via Find Other Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Other Split Key Row By Filter    ${code}
    Verify Object Form Record    ${OTHER_SPLIT_KEY_TABLE}    ${code}    Other Split Key
    ...    ${OTHER_SPLIT_KEY_UPDATE_PROPERTIES}    Split Key Name
    ...    code_label=${OTHER_SPLIT_KEY_CODE_LABEL}
    Clear Other Split Key Row Filter

Find Other Split Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Other Split Key Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Other Split
    ...    Key Record Found (called right after, same TC) needs the grid still filtered for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Other Split Key Row By Filter    ${code}
    Find Object Record    ${OTHER_SPLIT_KEY_TABLE}    ${code}    Other Split Key
    ...    code_label=${OTHER_SPLIT_KEY_CODE_LABEL}

Verify Other Split Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the full form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find Other
    ...    Split Key Record before this) AND left the Code filter active - clears the filter
    ...    itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${OTHER_SPLIT_KEY_TABLE}    ${code}
    ...    ${OTHER_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${OTHER_SPLIT_KEY_FORM_VERIFY_PROPERTIES}
    ...    @{OTHER_SPLIT_KEY_FORM_LABELS}
    Clear Other Split Key Row Filter

Delete Other Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the record, set End Date = Start Date (true
    ...    delete for this VERSIONED class), Save. Captures the TC05 evidence screenshot right
    ...    after the End Date is filled but BEFORE Save is clicked. Filters via Find Other
    ...    Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Other Split Key Row By Filter    ${code}
    Delete Object Via End Date    ${OTHER_SPLIT_KEY_TABLE}    ${OTHER_SPLIT_KEY_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Other Split Key Row Filter

Verify Other Split Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_SPLIT_KEY).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${OTHER_SPLIT_KEY_TABLE}    OV_SPLIT_KEY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Other Split Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${OTHER_SPLIT_KEY_TABLE}    ${code}
