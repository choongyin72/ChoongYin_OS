*** Settings ***
Documentation       T3 (screen) — Field Split Key page object.
...                 Screen: Configuration > Assets > Revenue Split Keys > Field Split Key
...                 (BF_CODE CD.0095, class SPLIT_KEY, view OV_SPLIT_KEY, controller
...                 manage_object_split_key/CLASS_NAME/SPLIT_KEY/SPLIT_TYPE/FIELD - URL
...                 confirmed live 2026-08-25). One of 6 sibling "* Split Key" screens
...                 (Product/Company/Field/Stream Item Category/Other/Stream Item) that ALL
...                 write to the SAME base view OV_SPLIT_KEY, differentiated only by SPLIT_TYPE
...                 - this build uses AUTOTEST_SPLITKEY_FIELD (NOT a generic AUTOTEST_SPLIT_KEY)
...                 specifically to avoid cross-screen collision with the 5 sibling builds.
...                 Holds Field Split Key's locators + thin IUD wrappers that delegate to T2
...                 (manage_object) and T1 (common).
...
...                 Grid id is SCREEN-SPECIFIC (${FIELD_SPLIT_KEY_TABLE} = nav:form:T_data),
...                 NOT the shared ${OV_MANAGE_OBJECT_TABLE} constant (manage_object_nav_nav:
...                 form:T_data) that Bank/Berth use - live DOM scan 2026-08-25 confirmed this
...                 screen's real datatable id differs even though it has a Date+GO navigator
...                 like Bank (GO button id is also screen-specific: navButton:form:B, not the
...                 button:form:B id Bank's Apply Navigator keyword hardcodes - Save And Refresh
...                 List (T2) will therefore fall through to its Refresh-toolbar branch after
...                 Save/Update here, same as any custom-URL OV without a GO button; this still
...                 reloads the grid from the DB correctly, live-confirmed in this build's 5/5
...                 run - not a functional gap, just a naming mismatch worth flagging for anyone
...                 auditing the shared keyword's id list later).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${FIELD_SPLIT_KEY_SCREEN}          Field Split Key
${FIELD_SPLIT_KEY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/field_split_key_insert.properties
${FIELD_SPLIT_KEY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/field_split_key_update.properties
${FIELD_SPLIT_KEY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/field_split_key_form_verify.properties
${FIELD_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/field_split_key_grid_verify.properties
# Grid id: THIS screen's own datatable id (live-confirmed 2026-08-25, NOT the shared
# ${OV_MANAGE_OBJECT_TABLE} - see Documentation above for why).
${FIELD_SPLIT_KEY_TABLE}           nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Live-confirmed 2026-08-25 by selecting
# an existing row: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input is the End Date input -
# same shape as Bank's own hardcoded ${BANK_DEL_ENDDATE} (Start Date C:1, End Date C:3).
${FIELD_SPLIT_KEY_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Field Split Key's own form-field label set. Start Date/End Date deliberately excluded (they
# live only in objectdates, not updateAttributes - same convention as Bank). Value Method/Shares
# add to 100%/Rounding Rule/Number of Rounding Decimals/Number Display Format are all confirmed
# NOT mandatory (live pristine-form scan 2026-08-25) and are deliberately left out of this list -
# not touched by Insert/Update, so nothing to verify.
@{FIELD_SPLIT_KEY_FORM_LABELS}    Split Key Code    Split Key Name    Description    Comments


*** Keywords ***
Find Field Split Key Row By Filter
    [Documentation]    Explicitly filter the Field Split Key grid's Split Key Code column to
    ...    ${code} via the shared T2 Find Object Row By Filter (resources/manage_object.resource)
    ...    - matches Bank/Account's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${FIELD_SPLIT_KEY_TABLE}    ${code}

Clear Field Split Key Row Filter
    [Documentation]    Clear the Split Key Code column filter (see Find Field Split Key Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${FIELD_SPLIT_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Field Split Key's OWN credentials
    ...    (${FIELD_SPLIT_KEY_EC_USER}/${FIELD_SPLIT_KEY_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application. Zero-argument wrapper (matches Bank's convention) that supplies Field
    ...    Split Key's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${FIELD_SPLIT_KEY_EC_USER}    ${FIELD_SPLIT_KEY_EC_PASS}

Open Field Split Key Screen
    [Documentation]    Navigate to the Field Split Key screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${FIELD_SPLIT_KEY_SCREEN}

Insert Field Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, so field_split_key_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    unchanged. Also asserts the inserted Split Key Code matches the suite's ${TEST_CODE}.
    ...    The evidence screenshot is captured BEFORE Save is clicked (passed through to Insert
    ...    Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${FIELD_SPLIT_KEY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    Split Key Code
    RETURN    ${code}

Verify Field Split Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check at all here): row exists in the grid, then every field's LIVE SCREEN value
    ...    (via Get OV Field Value By Label) is compared to testdata/field_split_key_insert.
    ...    properties (the file used to insert, not the post-update
    ...    field_split_key_form_verify.properties) - Split Key Code/Split Key Name/Description/
    ...    Comments (${FIELD_SPLIT_KEY_FORM_LABELS}). Start Date is NOT verified here - it only
    ...    exists as a grid column, not a form field (same convention as Bank). Delegates the
    ...    full sequence to the shared T2 Verify Object Insert Exists. Filters via Find Field
    ...    Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Split Key Row By Filter    ${code}
    Verify Object Insert Exists    ${FIELD_SPLIT_KEY_TABLE}    ${code}    Field Split Key
    ...    ${FIELD_SPLIT_KEY_INSERT_PROPERTIES}    @{FIELD_SPLIT_KEY_FORM_LABELS}
    ...    code_label=Split Key Code
    Clear Field Split Key Row Filter

Update Field Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict. The evidence screenshot is captured BEFORE Save is
    ...    clicked. Filters via Find Field Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${FIELD_SPLIT_KEY_UPDATE_PROPERTIES}
    Find Field Split Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${FIELD_SPLIT_KEY_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=Split Key Code
    Clear Field Split Key Row Filter
    RETURN    ${data}

Verify Field Split Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check): selects the row (loading updateAttributes), then compares Split Key Name/
    ...    Description's LIVE SCREEN value to testdata/field_split_key_update.properties.
    ...    Delegates to the shared T2 Verify Object Form Record. Filters via Find Field Split Key
    ...    Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Split Key Row By Filter    ${code}
    Verify Object Form Record    ${FIELD_SPLIT_KEY_TABLE}    ${code}    Field Split Key
    ...    ${FIELD_SPLIT_KEY_UPDATE_PROPERTIES}    Split Key Name    Description
    ...    code_label=Split Key Code
    Clear Field Split Key Row Filter

Find Field Split Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Field
    ...    Split Key Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Field Split Key Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Field Split Key Row By Filter    ${code}
    Find Object Record    ${FIELD_SPLIT_KEY_TABLE}    ${code}    Field Split Key
    ...    code_label=Split Key Code

Verify Field Split Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Delegates to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Field Split Key
    ...    Record before this) AND left the Split Key Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${FIELD_SPLIT_KEY_TABLE}    ${code}
    ...    ${FIELD_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${FIELD_SPLIT_KEY_FORM_VERIFY_PROPERTIES}
    ...    @{FIELD_SPLIT_KEY_FORM_LABELS}
    Clear Field Split Key Row Filter

Delete Field Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the record, set End Date = Start Date (true delete), Save. Captures the
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find Field Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Field Split Key Row By Filter    ${code}
    Delete Object Via End Date    ${FIELD_SPLIT_KEY_TABLE}    ${FIELD_SPLIT_KEY_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Field Split Key Row Filter

Verify Field Split Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (ov_split_key) - same shape as Bank's own
    ...    equivalent keyword, which is the established, already-shipped convention for this
    ...    step (the "PURE SCREEN, no DB check" convention this build follows everywhere else
    ...    applies to the Insert/Update/Find round-trip checks, not to this final DB-ground-truth
    ...    delete confirmation, which every other Bank-pattern screen also performs here).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${FIELD_SPLIT_KEY_TABLE}    ov_split_key    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Field Split Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${FIELD_SPLIT_KEY_TABLE}    ${code}
