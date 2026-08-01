*** Settings ***
Documentation       STANDALONE mandatory-field pre-flight gate (RF twin of py/mandatory_field_gate.py).
...                 Additive only - does NOT modify common.resource / manage_object.resource / any
...                 existing shared keyword. A T3 suite opts in by importing this resource file
...                 explicitly; every already-shipped screen is unaffected.
Library             Browser


*** Keywords ***
Find Empty Mandatory Fields
    [Documentation]    Scan every input/select/textarea whose id starts with ${scope_prefix} for the
    ...    mandatory-yellow background (EC's own rgb(252, 249, 192)) AND an empty current value.
    ...    Returns a list of {id, label} dicts - empty list means safe to proceed.
    [Arguments]    ${scope_prefix}
    ${hits}=    Evaluate JavaScript    ${None}
    ...    () => { const YELLOW='rgb(252, 249, 192)'; const out=[];
    ...    document.querySelectorAll('input,select,textarea').forEach(e=>{
    ...    if(!e.id||!e.id.startsWith('${scope_prefix}'))return; if(e.type==='hidden')return;
    ...    if(!e.offsetParent)return; const y=getComputedStyle(e).backgroundColor===YELLOW;
    ...    if(!y)return; const val=(e.value||'').trim(); if(val!=='')return;
    ...    const m=e.id.match(/^(.*:R:\\d+):C:\\d+:/); let lab='';
    ...    if(m){const lc=document.getElementById(m[1]+':C:0:la'); if(lc) lab=(lc.innerText||'').trim();}
    ...    out.push({id:e.id,label:lab}); }); return out; }
    RETURN    ${hits}

Assert No Empty Mandatory Field
    [Documentation]    Gate: FAIL naming every mandatory-and-empty field under ${scope_prefix} BEFORE
    ...    the caller clicks GO/Save - the proactive counterpart to reading EC's post-Save error banner.
    ...    Opt-in only; not called by any existing shared keyword.
    [Arguments]    ${scope_prefix}    ${action_label}=proceed
    ${hits}=    Find Empty Mandatory Fields    ${scope_prefix}
    ${n}=    Get Length    ${hits}
    IF    ${n} > 0
        Fail    BLOCKED before ${action_label}: ${n} mandatory field(s) still empty: ${hits}
    END
