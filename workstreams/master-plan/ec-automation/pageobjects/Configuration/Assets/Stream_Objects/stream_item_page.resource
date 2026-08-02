*** Settings ***
Documentation       T3 (screen) — Stream Item page object.
...                 Screen: Configuration > Assets > Stream Objects > Stream Item (CD.0008).
...                 Custom-URL OV (grid nav:form:T_data); date-effective (VERSIONED).
...                 INSERT + DELETE only — UPDATE is out of scope for this screen (see below).
...                 Reuses T2 label-driven OV keywords (Fill OV Field/Date/Dropdown By Label);
...                 no hardcoded row/column ids beyond the grid id and the objectdates End Date cell.
...
...                 UPDATE SKIPPED (owner instruction 2026-08-02): any Save on the updateAttributes
...                 tab fails with EC's own error "Cannot run schedule job UpdateStreamItem because it
...                 has not been configured" - a genuine EC sandbox configuration gap (BF VO.0031 -
...                 Daily SI Pending Calculation scheduler job not enabled here), confirmed live 3x and
...                 against EC's own online help page for this screen. Not a code defect.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/toolbar.resource


*** Variables ***
${STREAM_ITEM_SCREEN}      Stream Item
${STREAM_ITEM_TABLE}       nav:form:T_data
${STREAM_ITEM_GO}          buttongo:form:B
# objectdates field ID (Delete — End Date = Start Date); the same fixed cell id every OV uses.
${STREAM_ITEM_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
@{STREAM_ITEM_REF_LABELS}
...    Stream Item Category
...    Product
...    Field
...    Company
...    Stream
...    Measurement Node
...    Calc. Method
...    Conversion Method
...    Master UOM Group
...    Daily Accrual Method
...    Monthly Accrual Method
...    Reporting Category


*** Keywords ***
Open Stream Item Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Stream Item screen,
    ...    then click this screen's own non-standard GO button (${STREAM_ITEM_GO}) to
    ...    load the grid — the generic navigator.resource "Apply Navigator" keyword
    ...    hardcodes button:form:B, which does not exist on this screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${STREAM_ITEM_SCREEN}    ${user}    ${pass}
    Stream Item Apply Navigator

Stream Item Apply Navigator
    [Documentation]    This screen's navigator GO has id buttongo:form:B (not the generic
    ...    button:form:B). Click it directly to (re)load the grid from the DB.
    Click    css=[id="${STREAM_ITEM_GO}"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

Stream Item Row Should Exist
    [Documentation]    Assert a stream item with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${STREAM_ITEM_TABLE}    ${code}

Stream Item Row Should Not Exist
    [Documentation]    Assert a stream item with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${STREAM_ITEM_TABLE}    ${code}

Stream Item Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_STREAM_ITEM.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_STREAM_ITEM    ${code}

Stream Item Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_STREAM_ITEM.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_STREAM_ITEM    ${code}

Insert Stream Item Record
    [Documentation]    Insert a new Stream Item: New Object form -> Code + Start Date +
    ...    12 mandatory reference dropdowns (each first-available option) -> Name last
    ...    (mandatory to Save, but EC server-derives its real value from the references
    ...    regardless of what is typed - see the module docstring) -> Save -> this
    ...    screen's own GO (not the generic Apply Navigator).
    [Arguments]    ${code}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Stream Item Code    ${code}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    FOR    ${label}    IN    @{STREAM_ITEM_REF_LABELS}
        Fill OV Dropdown By Label    objectForm    ${label}    __FIRST__
    END
    Fill OV Field By Label    objectForm    Name    AUTOTEST SI (server-derived, ignored)
    Save
    Stream Item Apply Navigator

Delete Stream Item
    [Documentation]    Select the stream item, set End Date = Start Date (true delete
    ...    for this VERSIONED class), Save, this screen's own GO.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${STREAM_ITEM_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${STREAM_ITEM_DEL_ENDDATE}    ${date}
    Save
    Stream Item Apply Navigator
