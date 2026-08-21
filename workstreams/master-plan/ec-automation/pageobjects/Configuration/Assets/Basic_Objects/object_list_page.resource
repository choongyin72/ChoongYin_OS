*** Settings ***
Documentation       T3 (screen) — Object List page object.
...                 Screen: Configuration > Assets > Basic Objects > Object List.
...                 Manage-Object (OV) screen. Holds Object List's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${OBJECT_LIST_SCREEN}    Object List
${OBJECT_LIST_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_insert.properties
${OBJECT_LIST_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_update.properties
${OBJECT_LIST_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_form_verify.properties
${OBJECT_LIST_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${OBJECT_LIST_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded, matching Bank's convention
# and cross-confirmed against the already-proven Playwright driver config (del_end, identical id).
${OBJECT_LIST_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate on the current page using the SHARED environment.py
    ...    EC_USER/EC_PASS defaults - no screen-specific credentials.py for this screen
    ...    (per docs/rf-suite-styles.md point 6: cap per-screen credential files; Object
    ...    List has no real reason to override the shared default, unlike Bank).
    ...    Works whether this is the very first login (page freshly loaded on the login
    ...    form via the shared T1 Open EC Application) or a re-login after Logout From
    ...    EC Application (same login form, not a new page/tab). Zero-argument wrapper
    ...    so object_list_iud.robot's test cases read as a plain business step.
    Fill EC Login Form
    Capture Step    ${TEST NAME}_login

Open Object List Screen
    [Documentation]    Navigate to the Object List screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates, matching Bank's per-TC Login/Open Screen/Action/Verify/Logout shape.
    Navigate To Screen    ${OBJECT_LIST_SCREEN}
    Capture Step    ${TEST NAME}_open_screen

Object List Row Should Exist
    [Documentation]    Assert an object list with ${code} is present in the grid.
    [Arguments]    ${code}
    Row Should Exist    ${OBJECT_LIST_TABLE}    ${code}

Object List Row Should Not Exist
    [Documentation]    Assert an object list with ${code} is absent from the grid.
    [Arguments]    ${code}
    Row Should Not Exist    ${OBJECT_LIST_TABLE}    ${code}

Object List Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_OBJECT_LIST.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_OBJECT_LIST    ${code}

Object List Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_OBJECT_LIST.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_OBJECT_LIST    ${code}

Object List Class Should Equal In DB
    [Documentation]    DB ground-truth: assert ${code}'s GENERIC_CLASS_NAME column equals
    ...    ${expected_code} in OV_OBJECT_LIST - the mandatory "Class Name" dropdown field,
    ...    confirmed live (2026-08-21) to store a plain CODE (e.g. 'BANK'/'FIN_WBS'), not a
    ...    display label - so this checks the DB directly against the same code value used
    ...    to fill the field, no screen-vs-DB mismatch risk (unlike Bank's Country field).
    [Arguments]    ${code}    ${expected_code}
    Field Should Equal In View    OV_OBJECT_LIST    ${code}    GENERIC_CLASS_NAME    ${expected_code}

Object List Row Should Show Name
    [Documentation]    Assert the Object List row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OBJECT_LIST_TABLE}    ${code}    ${name}

Insert Object List From Properties
    [Documentation]    Insert a new object list by reading EVERY column=value entry from
    ...    ${properties_path} (testdata/object_list_insert.properties) and filling each
    ...    field by label, auto-detecting its kind (text/date/dropdown) live - mirrors
    ...    Bank's Insert Bank From Properties. Returns the Code that was inserted.
    [Arguments]    ${properties_path}=${OBJECT_LIST_INSERT_PROPERTIES}    ${pre_save_screenshot}=${EMPTY}
    ${code}=    Insert Object From Properties    ${properties_path}    ${pre_save_screenshot}
    RETURN    ${code}

Insert Object List Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object List From Properties,
    ...    so object_list_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments. Also checks the inserted Code matches the suite's ${TEST_CODE}.
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank.
    [Arguments]    ${properties_path}=${OBJECT_LIST_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Find Object List
    [Documentation]    Locate the object list row by ${code} and select it (loads
    ...    updateAttributes), verifying row-identity (Code read back) before returning.
    [Arguments]    ${code}
    Find Object By Code    ${OBJECT_LIST_TABLE}    ${code}    Object List

Find Object List Record
    [Documentation]    Friendly-narrative wrapper around Find Object List, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}).
    [Arguments]    ${code}=${TEST_CODE}
    Find Object List    ${code}
    Capture Step    ${TEST NAME}_action

Object List Form Should Match Properties
    [Documentation]    Assert fields show the expected value live in the updateAttributes
    ...    form. Caller must already have the row selected/form loaded (e.g. via Find
    ...    Object List). Defaults to Code/Name - Class Name/Start Date are Insert-only
    ...    fields, confirmed absent from updateAttributes (same pattern as Bank's Start
    ...    Date exclusion). If @{labels} is given, only THOSE labels are checked.
    [Arguments]    ${properties_path}=${OBJECT_LIST_FORM_VERIFY_PROPERTIES}    @{labels}
    ${default_labels}=    Create List    Code    Name
    ${use_labels}=    Set Variable If    ${labels}    ${labels}    ${default_labels}
    Verify Object Form Fields From Properties    updateAttributes    ${properties_path}
    ...    @{use_labels}

Verify Object List Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank's TC02 convention): row exists in
    ...    the grid, then the form shows what was just inserted (Code/Name only - Class
    ...    Name/Start Date are grid/insert-only, not present in updateAttributes).
    [Arguments]    ${code}=${TEST_CODE}
    Object List Row Should Exist    ${code}
    Find Object List    ${code}
    Object List Form Should Match Properties    ${OBJECT_LIST_INSERT_PROPERTIES}
    Capture Step    ${TEST NAME}_verify

Update Object List From Properties
    [Documentation]    Update the object list identified by ${code} by reading EVERY
    ...    column=value entry from ${properties_path} (testdata/object_list_update.properties)
    ...    and filling each field by label into updateAttributes. Mirrors Bank's Update
    ...    Bank From Properties. Returns the applied {label: value} dict.
    [Arguments]    ${code}    ${properties_path}=${OBJECT_LIST_UPDATE_PROPERTIES}    ${pre_save_screenshot}=${EMPTY}
    ${data}=    Update Object From Properties    ${OBJECT_LIST_TABLE}    ${code}    ${properties_path}
    ...    ${pre_save_screenshot}
    RETURN    ${data}

Update Object List Record And Save
    [Documentation]    Friendly-narrative wrapper around Update Object List From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${OBJECT_LIST_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${OBJECT_LIST_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify Object List Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank's TC03 convention: the form shows the updated Name.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object List    ${code}
    Object List Form Should Match Properties    ${OBJECT_LIST_UPDATE_PROPERTIES}    Name
    Capture Step    ${TEST NAME}_verify

Verify Object List Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Row Fields From Properties    ${OBJECT_LIST_TABLE}    ${code}
    ...    ${OBJECT_LIST_GRID_VERIFY_PROPERTIES}
    Object List Form Should Match Properties
    Capture Step    ${TEST NAME}_verify

Delete Object List
    [Documentation]    Select the object list, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after End Date is filled but BEFORE
    ...    Save is clicked, matching Bank's convention.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${OBJECT_LIST_TABLE}    ${OBJECT_LIST_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Delete Object List Record And Save
    [Documentation]    Friendly-narrative wrapper around Delete Object List, called with ZERO
    ...    arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object List    ${code}    ${date}

Verify Object List Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${OBJECT_LIST_TABLE}    OV_OBJECT_LIST    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Object List Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    [Arguments]    ${code}=${TEST_CODE}
    Object List Row Should Not Exist    ${code}
    Capture Step    ${TEST NAME}_verify
