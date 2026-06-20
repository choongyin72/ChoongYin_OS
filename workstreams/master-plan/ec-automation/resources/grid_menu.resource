*** Settings ***
Documentation       T2 - EC table column "hamburger" menu: filtering + reset-personalisation keywords,
...                 derived from the deep-dive (all 8 menu items live-verified) in
...                 DeepDiveLearnings/ec-ui/ec-table-column-menu.md and proven live on Business Function.
...                 Reusable across ANY EC table-layout screen. Parameterised by ${form} = the screenlet
...                 form prefix (e.g. "bf:form" on Business Function): grid table = ${form}:T, grid body
...                 = ${form}:T_data, text filter input for column N (0-based, left-to-right) =
...                 ${form}:T:sfilterN_ft_filter, filter toggle = ${form}:T:tfo, and the column-menu items
...                 are rendered as ${form}:T:{leaf} (rpc=Reset personalisation, ups=Use scrollbar,
...                 fc=Freeze, ctc=Copy, pfc=Paste).
...                 FRAME NOTE: EC renders each screen inside a content iframe. The Browser library's css=
...                 selectors pierce that frame automatically, but raw "Evaluate JavaScript ${None}" runs
...                 in the TOP frame and cannot see the screen elements - so every JS call here is anchored
...                 to an in-frame element via a css= selector and reaches the frame document through
...                 el.ownerDocument. The hamburger icon + filter toggle are also hover-revealed, hence the
...                 hidden elements are clicked via JS rather than a flaky real hover.
...                 This file is NEW/additive (no existing keyword signatures changed).

Library             Browser


*** Keywords ***
Grid Filtering Is On
    [Documentation]    True if the per-column filter row is currently rendered (any sfilter input present).
    [Arguments]    ${form}
    ${n}=    Get Element Count    css=[id^="${form}:T:sfilter"]
    ${on}=    Evaluate    ${n} > 0
    RETURN    ${on}

Turn Grid Filtering On
    [Documentation]    Turn the column filter row ON (idempotent). Clicks the hover-revealed toggle
    ...    ${form}:T:tfo in the content frame via JS, then waits for the filter-row AJAX to settle.
    [Arguments]    ${form}
    ${on}=    Grid Filtering Is On    ${form}
    IF    not ${on}
        Evaluate JavaScript    css=[id="${form}:T"]
        ...    (el) => { const e=el.ownerDocument.getElementById('${form}:T:tfo'); if(e){ e.click(); } }
        Wait For Load State    networkidle    timeout=15s
        Sleep    0.8s
    END

Turn Grid Filtering Off
    [Documentation]    Turn the column filter row OFF (idempotent). EC also CLEARS all active filters when
    ...    the filter row is removed (so this doubles as "clear filters").
    [Arguments]    ${form}
    ${on}=    Grid Filtering Is On    ${form}
    IF    ${on}
        Evaluate JavaScript    css=[id="${form}:T"]
        ...    (el) => { const e=el.ownerDocument.getElementById('${form}:T:tfo'); if(e){ e.click(); } }
        Wait For Load State    networkidle    timeout=15s
        Sleep    0.8s
    END

Clear Grid Filters
    [Documentation]    Clear all active column filters by turning the filter row off (EC clears filters on
    ...    removal). Readable alias of Turn Grid Filtering Off for tests.
    [Arguments]    ${form}
    Turn Grid Filtering Off    ${form}

Filter Grid Text Column By Value
    [Documentation]    With filtering ON, type ${value} into the text filter of column ${col} (0-based,
    ...    left-to-right) and submit with Enter. EC does a partial "contains" match and narrows the grid.
    [Arguments]    ${form}    ${col}    ${value}
    Turn Grid Filtering On    ${form}
    VAR    ${f}=    ${form}:T:sfilter${col}_ft_filter
    Wait For Elements State    css=[id="${f}"]    visible    timeout=10s
    Click    css=[id="${f}"]
    Type Text    css=[id="${f}"]    ${value}    clear=Yes
    Keyboard Key    press    Enter
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

Clear Grid Text Column Filter
    [Documentation]    Clear the text filter on column ${col} (select-all + Delete + Enter) and let the grid
    ...    refresh back to the unfiltered (or other-column-filtered) set.
    [Arguments]    ${form}    ${col}
    VAR    ${f}=    ${form}:T:sfilter${col}_ft_filter
    Click    css=[id="${f}"]
    Keyboard Key    press    Control+A
    Keyboard Key    press    Delete
    Keyboard Key    press    Enter
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

Grid Data Row Count
    [Documentation]    Count the real data rows in the grid body (${form}:T_data) - the live result count
    ...    after filtering. Counts by the PrimeFaces row-index attribute (tr[data-ri]) so it works on grids
    ...    whose cells are input fields (where tr.textContent is empty); the "no records" message row has no
    ...    data-ri and is excluded. Anchored in the content frame.
    [Arguments]    ${form}
    ${n}=    Evaluate JavaScript    css=[id="${form}:T_data"]
    ...    (el) => el.querySelectorAll('tr[data-ri]').length
    RETURN    ${n}

Click Grid Menu Item
    [Documentation]    Fire a column-menu item by its leaf id (rpc=Reset personalisation, ups=Use scrollbar,
    ...    fc=Freeze, ctc=Copy, pfc=Paste). Items render as ${form}:T:{leaf}. Clicks the item link in the
    ...    content frame via JS (the menu is hover-revealed), then waits for the resulting AJAX.
    [Arguments]    ${form}    ${leaf}
    Evaluate JavaScript    css=[id="${form}:T"]
    ...    (el) => { const d=el.ownerDocument; const m=d.getElementById('${form}:T:${leaf}'); if(!m) return; const a=(m.tagName==='A')?m:(m.querySelector('a')||m); a.click(); }
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

Reset Grid Personalisation
    [Documentation]    Click "Reset personalisation for component" (leaf rpc) to clear THIS grid's per-user
    ...    personalisation (filter / freeze / hidden columns / rows-per-page / scrollbar) back to defaults.
    ...    Server-side per-user (DB CTRL_PERSONALISATION). Ideal as a test setup/teardown for a clean grid.
    [Arguments]    ${form}
    Click Grid Menu Item    ${form}    rpc
