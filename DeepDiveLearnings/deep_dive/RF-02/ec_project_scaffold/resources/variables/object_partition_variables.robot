*** Settings ***
Documentation    Object Partition screen selectors — CO.???? Object Partition
...              NOTE: Exact IDs to be verified against live EC DOM via Playwright MCP

*** Variables ***
# ── Navigation ────────────────────────────────────────────────────────────────
${OP_SCREEN_NAME}               Object Partition

# ── Screen selectors (adjust after live DOM inspection) ──────────────────────
${OP_OPERATOR_DROPDOWN}         xpath=//select[contains(@id,'operatorDropdown')]
${OP_ROLE_DROPDOWN}             xpath=//select[contains(@id,'roleDropdown')]
${OP_INSERT_BTN}                xpath=//button[contains(@id,'insertBtn') or contains(@id,'addBtn')]
${OP_DATA_GRID}                 css=.ui-datatable
${OP_GRID_ROWS}                 tr[data-rk]
${OP_DELETE_BTN_TEMPLATE}       xpath=//tr[contains(.,'ROLE_PLACEHOLDER')]//button[contains(@id,'deleteBtn')]

# ── Test data prefix ──────────────────────────────────────────────────────────
${OP_AUTOTEST_PREFIX}           AUTOTEST_
