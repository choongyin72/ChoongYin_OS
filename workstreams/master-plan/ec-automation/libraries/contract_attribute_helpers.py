"""General-purpose edit helper for EC's Contract Attribute screen family.

Verified 2026-08-09 that Sale Contract Attributes, Revenue Contract Attributes, and Transport
Contract Attributes are the SAME underlying JSF component:
    com.ec.tran.co.screens/contract_attribute/ACCESS_COLUMN/<SALE_CODE|REVN_CODE|TRAN_CODE>
Confirmed on two independent environments (CLP ECaaS TEST + this repo's local sandbox) that the
grid id, toolbar structure, edit-field ids, and the "unsaved changes" trap are byte-for-byte
identical across all three screens and both environments -- this module is therefore NOT
CLP-specific or Sale-specific; it targets the shared component and works on any screen built on it.

Mechanics (all verified live, not assumed):
  1. The value edit field always lives at the SAME fixed id `version:form:T:0:C1_...` regardless of
     which grid row you clicked -- only its TYPE changes: plain input (`_in`), dropdown
     (`_dd_button`/`_dd_input`/`_dd_panel`), or checkbox (`_cb`).
  2. A row whose attribute has NEVER had a value shows none of those fields when clicked (only
     "No records found" in the mini version panel) -- it needs Insert(+) -> "Attribute Version"
     (toolbar menuBar link index 2, hover to open the submenu, then index 3) BEFORE the edit field
     appears.
  3. Some attributes are flagged PROTECTED and CANNOT be inserted this way at all -- attempting it
     throws a dialog: "Not allowed to insert protected attributes." (dismissed via an OK button).
     This is a genuine business-rule wall, not a bug; the caller must detect and report it, never
     retry blindly. Protection is per-attribute-definition, decided by the EC config, not guessable
     from the grid alone -- the only way to know is to try the Insert and check for this dialog.
  4. A brand-new (non-protected) version row also needs its Daytime field
     (`version:form:T:0:C0_da_input`) filled, or Save silently no-ops (looks like it worked, but a
     subsequent Refresh throws an "UNSAVED CHANGES" modal proving nothing was actually persisted).
  5. Save = toolbar menuBar link index 0 (title-based xpath is unreliable on this toolbar; use
     position). Clicking into a DIFFERENT row while a previous edit is unsaved throws a
     confirmationForm modal ("UNSAVED CHANGES ... Do you want to save these changes?") with a
     `confirmationForm:cancelbtn` Cancel button (stays put) and YES/NO buttons (commit/discard).

Usage:
    from contract_attribute_helpers import set_attribute_value, AttributeProtectedError
    try:
        result_row = set_attribute_value(page, frame, row_idx=13, value="some code or label",
                                          daytime="2026-01-01")
    except AttributeProtectedError as e:
        print(f"row {e.row_idx} ('{e.label}') is protected -- cannot set via this UI mechanism")
"""

GRID_ID = "attribute:form:T_data"
MENUBAR_ID = "screenToolbar:form:menuBar"
INSERT_LINK_IDX = 2          # Insert (+) icon, has a submenu
INSERT_ATTR_VERSION_IDX = 3  # "ATTRIBUTE VERSION" submenu item under Insert
DELETE_LINK_IDX = 6          # Delete (-) icon, has a submenu -- mirrors Insert's structure
DELETE_ATTR_VERSION_IDX = 7  # "ATTRIBUTE VERSION" submenu item under Delete; DISABLED until the
                              # selected row has an existing version to remove
SAVE_LINK_IDX = 0
PROTECTED_ERROR_TEXT = "Not allowed to insert protected attributes"


class AttributeProtectedError(Exception):
    """Raised when EC refuses to insert a version for a protected attribute."""

    def __init__(self, row_idx, label):
        self.row_idx = row_idx
        self.label = label
        super().__init__(f"row {row_idx} ('{label}') is a protected attribute -- cannot insert a value")


def find_contract_attribute_frame(page):
    """Return the frame hosting any Contract Attribute screen (Sale/Revenue/Transport)."""
    for f in page.frames:
        if "contract_attribute" in (f.url or ""):
            return f
    return page.main_frame


def _menubar_links(page):
    return page.locator(f'[id="{MENUBAR_ID}"]').locator("a")


def _edit_field_state(fr):
    """Return which edit-field kind is currently present at the fixed version:form:T:0:C1_ id:
    'in' (plain input), 'dd' (dropdown), 'cb' (checkbox), or None (never-set -- needs Insert)."""
    if fr.locator('[id="version:form:T:0:C1_in"]').count() > 0:
        return "in"
    if fr.locator('[id="version:form:T:0:C1_cb"]').count() > 0:
        return "cb"
    if fr.locator('[id="version:form:T:0:C1_dd_button"]').count() > 0:
        return "dd"
    return None


def set_attribute_value(page, fr, row_idx, value, daytime=None, pause_ms=700):
    """Set the value of the attribute at `row_idx` in a Contract Attribute grid (Sale/Revenue/
    Transport -- any screen built on com.ec.tran.co.screens/contract_attribute).

    value: for a plain/numeric attribute, the string to type; for a checkbox attribute, pass
           True/False (or "Y"/"N"); for a dropdown/object-reference attribute, pass the label
           substring to match in the dropdown panel (matched case-sensitively, substring OK).
    daytime: 'YYYY-MM-DD' string. REQUIRED the first time an attribute is ever set (never-set
             row) -- pass it every time to be safe; it's a no-op if the field already has a date.

    Raises AttributeProtectedError if the attribute cannot be inserted (system-protected).
    Returns the row's [label, value] cell text after save, for verification.
    """
    grid = fr.locator(f'[id="{GRID_ID}"]')
    row = grid.locator("tr").nth(row_idx)
    label = row.locator("td").nth(0).inner_text()
    row.locator("td").nth(1).click()
    page.wait_for_timeout(pause_ms)

    kind = _edit_field_state(fr)
    if kind is None:
        links = _menubar_links(page)
        links.nth(INSERT_LINK_IDX).hover()
        page.wait_for_timeout(400)
        links.nth(INSERT_ATTR_VERSION_IDX).click()
        page.wait_for_timeout(pause_ms)
        page.wait_for_load_state("networkidle")

        protected_dialog = page.locator(f'text={PROTECTED_ERROR_TEXT}')
        if protected_dialog.count() > 0:
            ok_btn = page.locator('button:has-text("OK")')
            if ok_btn.count() > 0:
                ok_btn.first.click()
                page.wait_for_timeout(500)
            raise AttributeProtectedError(row_idx, label)

        kind = _edit_field_state(fr)
        if kind is None:
            raise RuntimeError(
                f"row {row_idx} ('{label}'): no edit field appeared after Insert->Attribute "
                f"Version, and no protected-attribute dialog was shown either -- unexpected state"
            )

    if daytime:
        daytime_in = fr.locator('[id="version:form:T:0:C0_da_input"]')
        if daytime_in.count() > 0:
            cur = daytime_in.input_value()
            if not cur:
                daytime_in.click()
                daytime_in.press("Control+a")
                daytime_in.type(daytime, delay=40)
                page.keyboard.press("Tab")
                page.wait_for_timeout(500)

    if kind == "in":
        fld = fr.locator('[id="version:form:T:0:C1_in"]')
        fld.click()
        fld.press("Control+a")
        fld.type(str(value), delay=40)
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
    elif kind == "cb":
        cb = fr.locator('[id="version:form:T:0:C1_cb"]')
        want_checked = value in (True, "Y", "y", "Yes", "yes")
        if cb.is_checked() != want_checked:
            cb.click()
            page.wait_for_timeout(300)
    elif kind == "dd":
        btn = fr.locator('[id="version:form:T:0:C1_dd_button"]')
        btn.click()
        page.wait_for_timeout(pause_ms)
        panel = fr.locator('[id="version:form:T:0:C1_dd_panel"]')
        items = panel.locator("tr")
        n = items.count()
        found = False
        for i in range(n):
            item_label = items.nth(i).get_attribute("data-item-label") or ""
            if str(value) in item_label:
                items.nth(i).click()
                found = True
                break
        if not found:
            raise RuntimeError(f"row {row_idx} ('{label}'): dropdown option matching '{value}' not found ({n} options)")
        page.wait_for_timeout(500)

    _menubar_links(page).nth(SAVE_LINK_IDX).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1200)

    grid2 = fr.locator(f'[id="{GRID_ID}"]')
    row_after = grid2.locator("tr").nth(row_idx).locator("td")
    return [row_after.nth(i).inner_text() for i in range(row_after.count())]


def delete_attribute_value(page, fr, row_idx, pause_ms=700):
    """Delete the version at `row_idx`, restoring it to the never-set/blank state -- the exact
    inverse of set_attribute_value(), verified round-trip (set -> delete -> blank again) on
    2026-08-09. Requires the row to currently have a value (Delete->Attribute Version is disabled
    on a row with no version to remove). Returns the row's [label, value] cells after save --
    value should be empty on success.
    """
    grid = fr.locator(f'[id="{GRID_ID}"]')
    row = grid.locator("tr").nth(row_idx)
    row.locator("td").nth(1).click()
    page.wait_for_timeout(pause_ms)

    links = _menubar_links(page)
    links.nth(DELETE_LINK_IDX).hover()
    page.wait_for_timeout(400)
    delete_item = links.nth(DELETE_ATTR_VERSION_IDX)
    if "ui-state-disabled" in (delete_item.get_attribute("class") or ""):
        raise RuntimeError(f"row {row_idx}: Delete->Attribute Version is disabled -- row has no existing version to remove")
    delete_item.click()
    page.wait_for_timeout(pause_ms)
    page.wait_for_load_state("networkidle")

    confirm = page.locator('button:has-text("YES")')
    if confirm.count() > 0:
        confirm.first.click()
        page.wait_for_timeout(pause_ms)
        page.wait_for_load_state("networkidle")

    links.nth(SAVE_LINK_IDX).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1200)

    grid2 = fr.locator(f'[id="{GRID_ID}"]')
    row_after = grid2.locator("tr").nth(row_idx).locator("td")
    return [row_after.nth(i).inner_text() for i in range(row_after.count())]


def discard_unsaved_changes(page):
    """Click Cancel on the 'UNSAVED CHANGES' modal (confirmationForm:cancelbtn) to stay on the
    current row without saving OR discarding -- use before navigating away if you want to keep
    editing the same row. To actually discard the pending edit, click the modal's NO button
    instead (not wrapped here since discarding is a deliberate, situational choice)."""
    cancel_btn = page.locator('[id="confirmationForm:cancelbtn"]')
    if cancel_btn.count() > 0:
        cancel_btn.click()
        page.wait_for_timeout(700)
        return True
    return False


if __name__ == "__main__":
    print(__doc__)
