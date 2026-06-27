*** Settings ***
Documentation       T3 (screen) - Product Group Setup page object.
...                 Screen: Configuration > Assets > Royalty Objects > Product Group Setup.
...                 3-TIER master->detail->sub-detail, NO navigator: top grid lists Product
...                 Groups (click a row to select); middle grid = Product Group Setup (products
...                 in the group); bottom TABS COSTS (Product Group Cost) + Stream Calculation
...                 Category - both scoped to the selected product. Insert/Delete toolbar is
...                 TAB-GATED (an entity is selectable only when its section/tab is active).
...                 3 entities, each verified by a unique COMMENTS sentinel (present-in-view).
...                 Each entity's layout is a dict (&{SETUP_E}/&{COST_E}/&{SCC_E}):
...                   Setup -> DV_PRODUCT_GROUP_SETUP   (member C3_dd Product,   comment C10_in)
...                   Cost  -> DV_PRODUCT_GROUP_COST    (member C3_dd Cost Type, comment C7_in)
...                   SCC   -> PRODUCT_STRM_BAL_CAT     (member C2_dd Category,  comment C3_in)
...                 NOTE: SCC tab labelled "Stream Calculation Category" but its table is the
...                 Stream BALANCE Category (PRODUCT_STRM_BAL_CAT) - label != table.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table_class.resource


*** Variables ***
${PGS_SCREEN}       Product Group Setup
${TOP_GRID}         nav:form:T_data
${START_DATE}       2011-01-01
${TAB_COST}         product_group_sub:tabPanel:tab1_header
${TAB_SCC}          product_group_sub:tabPanel:tab2_header
# per-entity layout (label = Insert/Delete submenu item; pfx = grid row prefix;
# member_col = the member dropdown cell; cmt_col = the Comments cell; view = DB backing;
# m1/m2 = extra MANDATORY (yellow / DB NOT-NULL) cells to fill on insert, e.g. Sort Order /
# Cost Column - empty cols are skipped). Setup: C2 Sort Order. Cost: C2 Sort + C4 Cost Column.
&{SETUP_E}          label=Product Group Setup    pfx=prod_group_setup:form:T    member_col=C3_dd    cmt_col=C10_in    view=DV_PRODUCT_GROUP_SETUP    m1_col=C2_in    m1_val=999    m2_col=${EMPTY}    m2_val=${EMPTY}
&{COST_E}           label=Product Group Cost    pfx=product_group_sub:tabPanel:prod_group_cost:form:T    member_col=C3_dd    cmt_col=C7_in    view=DV_PRODUCT_GROUP_COST    m1_col=C2_in    m1_val=999    m2_col=C4_in    m2_val=99
&{SCC_E}            label=Stream Calculation Category    pfx=product_group_sub:tabPanel:strm_calc_cat:form:T    member_col=C2_dd    cmt_col=C3_in    view=PRODUCT_STRM_BAL_CAT    m1_col=${EMPTY}    m1_val=${EMPTY}    m2_col=${EMPTY}    m2_val=${EMPTY}


*** Keywords ***
Open Product Group Setup Screen
    [Documentation]    Suite Setup: launch + open the screen (no navigator on this screen).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PGS_SCREEN}    ${user}    ${pass}

Select Product Group
    [Documentation]    Click the top-grid row for ${code} to load its detail grids (no GO).
    [Arguments]    ${code}
    Click    xpath=//*[@id="${TOP_GRID}"]//tr[.//*[normalize-space(text())='${code}']]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.5s

Select Setup Row By Comment
    [Documentation]    Click the middle (Setup) row whose Comments = ${comment} so the bottom
    ...    tabs (Cost / SCC) scope to that product, and the middle grid is the active section.
    [Arguments]    ${comment}
    ${row}=    Find Grid Row By Cell Input Value    ${SETUP_E}[pfx]_data    ${SETUP_E}[cmt_col]    ${comment}
    Should Be True    ${row} >= 0    msg=Setup row with comment ${comment} not found
    Click    css=[id="${SETUP_E}[pfx]:${row}:${SETUP_E}[cmt_col]"]
    Sleep    1s

Activate Tab
    [Documentation]    Click a bottom tab header (so its entity's Insert/Delete enables).
    [Arguments]    ${tab_id}
    Click    css=[id="${tab_id}"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

Insert Member Row
    [Documentation]    Insert toolbar -> entity label -> blank row -> pick member dd + start date
    ...    + Comments sentinel -> Save (no Refresh, to preserve the group/product selection).
    [Arguments]    ${e}    ${member_value}    ${comment}
    VAR    ${grid}    ${e}[pfx]_data
    Insert New Grid Row By Label    ${e}[label]
    ${row}=    Find Grid Row By Cell Input Value    ${grid}    ${e}[member_col]_input    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank ${e}[label] row appeared
    Select EC Dropdown Option    ${e}[pfx]:${row}:${e}[member_col]    ${member_value}
    ${row}=    Find Grid Row By Cell Input Value    ${grid}    ${e}[member_col]_input    ${member_value}
    Should Be True    ${row} >= 0    msg=${e}[label] row vanished after member selection
    Fill New Row Fields    ${e}    ${row}
    Type Cell By Id    ${e}[pfx]:${row}:${e}[cmt_col]    ${comment}
    Save

Fill New Row Fields
    [Documentation]    Fill the new row's start date + the entity's extra mandatory (yellow /
    ...    DB NOT-NULL) cells, e.g. Sort Order / Cost Column - empty cols are skipped. Prevents
    ...    the EC silent reject (a row missing a mandatory cell saves in the UI but not the DB).
    [Arguments]    ${e}    ${row}
    Fill EC Date    ${e}[pfx]:${row}:C0_da_input    ${START_DATE}
    IF    '${e}[m1_col]' != ''
        Type Cell By Id    ${e}[pfx]:${row}:${e}[m1_col]    ${e}[m1_val]
    END
    IF    '${e}[m2_col]' != ''
        Type Cell By Id    ${e}[pfx]:${row}:${e}[m2_col]    ${e}[m2_val]
    END

Update Member Comment
    [Documentation]    Find the row by its current Comments value, set a new Comments -> Save.
    [Arguments]    ${e}    ${old_comment}    ${new_comment}
    ${row}=    Find Grid Row By Cell Input Value    ${e}[pfx]_data    ${e}[cmt_col]    ${old_comment}
    Should Be True    ${row} >= 0    msg=Row with comment ${old_comment} not found to update
    Type Cell By Id    ${e}[pfx]:${row}:${e}[cmt_col]    ${new_comment}
    Save

Delete Member Row
    [Documentation]    Find the row by its Comments value, select it (click the comment cell),
    ...    Delete toolbar -> entity label -> Save. (The matching tab must be active.)
    [Arguments]    ${e}    ${comment}
    ${row}=    Find Grid Row By Cell Input Value    ${e}[pfx]_data    ${e}[cmt_col]    ${comment}
    Should Be True    ${row} >= 0    msg=Row with comment ${comment} not found to delete
    Click    css=[id="${e}[pfx]:${row}:${e}[cmt_col]"]
    Sleep    0.8s
    Delete Selected Grid Row    ${e}[label]
    Save

Comment Should Be Present In DB
    [Documentation]    Assert the Comments sentinel persisted in the entity's backing.
    [Arguments]    ${e}    ${comment}
    Code Should Be Present In View    ${e}[view]    ${comment}

Comment Should Be Absent In DB
    [Documentation]    Assert the Comments sentinel is NOT present in the entity's backing.
    [Arguments]    ${e}    ${comment}
    Code Should Be Absent In View    ${e}[view]    ${comment}
