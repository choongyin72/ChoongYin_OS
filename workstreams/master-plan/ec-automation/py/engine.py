"""Universal EC Screen Engine - Phase 2: INTERACTION layer.

Generic, label-driven interaction API built on top of the Phase 1 classifier's output
(`universal_classifier.classify_screen`) - no per-family branching, no hardcoded field ids.
Each call: (1) resolves the field by LABEL via the classifier's region/primitive map,
(2) dispatches to the gesture already proven for that primitive in the `ec-screen-automation`
skill cookbook, (3) waits for the standard PrimeFaces AJAX settle, (4) re-reads the DOM
afterward to confirm the field's displayed value actually changed - a verification-echo
that catches the class of bug that bit CD.0024 (insert persisted, UI read failed on a wrong
assumed grid id).

Design: docs/universal_screen_engine_design.md section 4. Does not replace the classifier
(universal_classifier.py) or the proven OV-specific driver (ec_object_iud.py) - built on top
of the first, borrows low-level gestures from the second where they're already generic enough
(select_dropdown, pick_popup).

Usage:
    from universal_classifier import classify_screen
    result = classify_screen("Bank")            # Phase 1 (opens + closes its own browser)
    # Phase 2 opens its OWN page (classify_screen doesn't hand back an open one) and re-derives
    # the map live against that page - see open_and_classify() below.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from universal_classifier import (  # noqa: E402
    css,
    ajax,
    classify_dd,
    classify_field_by_id,
    scan_region_fields,
    scan_grid_columns,
    EC_URL,
    HEADED,
    USER,
    PW,
)
from ec_object_iud import ec_error  # noqa: E402 - proven structural (not text-substring) error-banner detector
from playwright.sync_api import sync_playwright  # noqa: E402


class FieldNotFound(LookupError):
    pass


class VerificationEchoFailed(AssertionError):
    """Raised when a fill/select call's post-write DOM re-read doesn't match what was set -
    the class of silent failure this layer exists to catch (CD.0024)."""


class SaveFailed(RuntimeError):
    """Raised when EC's own error banner reports a Save-time validation failure (e.g. a missing
    mandatory field) - confirmed live, Node: `ec_error()` checked immediately after the click
    correctly reports 'Required fields are empty...', but checking it after `click()`'s automatic
    `_refresh_field_map()` call instead reads '' - that refresh probes every dd_input field via a
    live click+Escape (classify_dd), which dismisses EC's own notification banner as a side
    effect. So error-detection must happen BEFORE any refresh, not left to the caller to remember
    to check first - `click('Save')` now raises this itself rather than silently reporting
    success by omission, the same failure class the verification-echo elsewhere exists to catch."""


def _norm(s):
    return (s or "").strip().lower()


class Engine:
    """One instance = one open, already-navigated EC screen. Build via open_screen()."""

    def __init__(self, page, screen_name):
        self.page = page
        self.screen_name = screen_name
        self._refresh_field_map()

    # ---------------------------------------------------------------- field resolution
    def _refresh_field_map(self):
        """Re-scan the live DOM for every labeled field currently visible - form region
        (objectForm insert / updateAttributes update / objectdates) + navigator. Called at
        construction and after any action that can change which form is showing (row-select,
        Save, New Object)."""
        page = self.page
        fields = []
        for prefix, source in [
            ("objectForm:form", "objectForm"),
            ("updateAttributes:form", "updateAttributes"),
            ("objectdates:form", "objectdates"),
            ("nav:form", "navigator"),
        ]:
            for f in scan_region_fields(page, prefix):
                if not f["label"]:
                    continue
                primitive = classify_field_by_id(page, f) if source != "navigator" else _nav_primitive(f)
                fields.append({**f, "primitive": primitive, "source": source})
        # Fixed 2026-08-14 (Project Data Mapping Setup, Phase 4 pilot 3 / Issue #361): plain
        # last-wins on duplicate labels breaks when a navigator FILTER field and an objectForm
        # field share a label (e.g. "Property") and are both visible at once (New Object form
        # open, navigator still on-screen) - navigator is scanned last, so it silently shadowed
        # the real, mandatory objectForm field, and Save failed with "Required fields are
        # empty... Property[CONTRACT_AREA_POPUP]" even though a value had been set on the
        # (wrong) navigator field. Save only ever acts on the form, never the nav filter, so a
        # non-navigator source must always win a label collision, regardless of scan order.
        self._by_label = {}
        for f in fields:
            key = _norm(f["label"])
            existing = self._by_label.get(key)
            if existing is None or existing["source"] == "navigator":
                self._by_label[key] = f

    def _field(self, label):
        f = self._by_label.get(_norm(label))
        if not f:
            raise FieldNotFound(f"No visible field labeled '{label}' on {self.screen_name!r} "
                                 f"(known labels: {sorted(x['label'] for x in self._by_label.values())})")
        return f

    # ---------------------------------------------------------------- primitives
    def fill(self, label, value):
        """text or date field. Verification-echo: re-reads the input's .value afterward - and,
        critically for date fields, confirms the SAVE actually succeeds server-side (see below),
        not just that the DOM shows what was typed.

        Date-field gotcha (confirmed live, Bank's Start Date): EC's calendar widget carries its
        real expected format in `data-p-pattern` (e.g. 'yyyy-MM-dd') on the input element. A value
        typed in a DIFFERENT format (e.g. '01/01/2020') still shows correctly in the DOM .value and
        raises no client-side error - but the widget's underlying date MODEL never parses it, and
        Save then fails server-side with 'Required fields are empty' for that field, even though
        every client-side signal looked fine. Root-caused by reading ec_error() after a Save
        attempt. Fix: read the field's own data-p-pattern and reformat the caller's value to match
        it (generic - not hardcoded to one screen's date convention), rather than assuming a fixed
        format."""
        f = self._field(label)
        if f["primitive"] not in ("text", "date"):
            raise ValueError(f"fill() called on a '{f['primitive']}' field ({label!r}) - use select()/resolve_popup()")
        loc = self.page.locator(css(f["id"])).first
        typed_value = str(value)
        if f["primitive"] == "date":
            typed_value = _reformat_date_to_pattern(loc, typed_value)
        loc.click()
        loc.fill(typed_value)
        self.page.keyboard.press("Tab")
        self.page.wait_for_timeout(400)
        loc.evaluate("(e) => { e.dispatchEvent(new Event('change',{bubbles:true})); e.dispatchEvent(new Event('blur',{bubbles:true})); }")
        ajax(self.page)
        actual = loc.input_value()
        if f["primitive"] == "date":
            ok = re.sub(r"\W", "", actual) == re.sub(r"\W", "", typed_value)
        else:
            ok = _norm(actual) == _norm(typed_value)
        if not ok:
            raise VerificationEchoFailed(f"fill({label!r}, {value!r}): DOM re-read shows {actual!r} after fill")
        return actual

    def select(self, label, value):
        """dropdown field. Click the button, match the panel row by data-item-label, close.
        Verification-echo: re-reads the dd's displayed label afterward."""
        f = self._field(label)
        if f["primitive"] != "dropdown":
            raise ValueError(f"select() called on a '{f['primitive']}' field ({label!r})")
        base = f["id"][: -len("_input")]
        self.page.locator(css(base + "_button")).first.click()
        want_first = value in (None, "", "__FIRST__")
        any_opt = f"xpath=//*[@id='{base}_panel']//tr[@data-item-label and normalize-space(@data-item-label)!='']"
        opt = any_opt if want_first else f"xpath=//*[@id='{base}_panel']//tr[normalize-space(@data-item-label)='{value}']"
        loc = self.page.locator(opt).first
        loc.wait_for(state="visible", timeout=6000)
        picked_label = loc.get_attribute("data-item-label")
        loc.click()
        ajax(self.page)
        actual = self.page.locator(css(f["id"])).first.input_value()
        target = picked_label if want_first else value
        if _norm(actual) != _norm(target):
            raise VerificationEchoFailed(f"select({label!r}, {value!r}): DOM re-read shows {actual!r} after select")
        self._refresh_field_map()
        return actual

    def check(self, label, value=True):
        """checkbox field. Verification-echo: re-reads .checked afterward."""
        f = self._field(label)
        if f["primitive"] != "checkbox":
            raise ValueError(f"check() called on a '{f['primitive']}' field ({label!r})")
        loc = self.page.locator(css(f["id"])).first
        current = loc.is_checked()
        if current != bool(value):
            loc.click()
        ajax(self.page)
        actual = self.page.locator(css(f["id"])).first.is_checked()
        if actual != bool(value):
            raise VerificationEchoFailed(f"check({label!r}, {value!r}): DOM re-read shows checked={actual}")
        return actual

    def resolve_popup(self, label):
        f = self._field(label)
        if f["primitive"] != "popup":
            raise ValueError(f"resolve_popup() called on a '{f['primitive']}' field ({label!r})")
        return _PopupHandle(self, f["id"])

    # ---------------------------------------------------------------- actions
    def click(self, action):
        """Named top-level actions: 'Save', 'GO'. For toolbar menu actions use toolbar()."""
        if action == "Save":
            self._save()
            err = ec_error(self.page)  # MUST run before _refresh_field_map() - see SaveFailed
            if err:
                raise SaveFailed(err)
        elif action == "GO":
            self._click_go()
        else:
            raise ValueError(f"Unknown action {action!r} - use toolbar() for menu items")
        self._refresh_field_map()

    def _click_go(self):
        """Structural GO-id list - same set proven in the Phase 1 classifier's readiness gate
        (includes 'buttongo:form:B', the id that caused the Stream Item open-failure before it
        was added there). Not every screen has a GO button (custom-URL OVs use toolbar Refresh
        instead) - a no-op here is legitimate, not an error."""
        for gid in ("go_button:form:B", "button:form:B", "navButton:form:B", "buttongo:form:B"):
            loc = self.page.locator(css(gid))
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                ajax(self.page, 20000)
                return True
        return False

    def apply_navigator(self, values=None, levels=4, row=1):
        """OV-GM navigator cascade - generic, structural, no per-screen hardcoding. The grid on an
        OV-GM screen is empty until a cascade of navigator dropdowns (Business Unit -> Production
        Unit -> Area -> ...) is set + GO; child options only render once the parent is chosen.

        - `values=None` (default): fill each column C:1..`levels` FIRST-AVAILABLE, parent before
          child (ports `ec_object_iud.py`'s proven `apply_ovgm_navigator()`).
        - `values=[...]`: fill C:1..len(values) with these EXACT values instead of first-available
          (for a screen where the default first option has no valid downstream combination -
          the same class of gotcha the classifier's `NAV_HINT_OPTION` exists to work around).
        - No `nav:form:G:*:R:<row>:C:*:dd_input` columns exist at all (a screen with only optional
          filters, or none): the loop naturally does nothing and this degrades automatically to a
          bare GO - no separate "go_only" mode flag needed, unlike the string-templated generators'
          current design, since the absence of columns already says everything.

        Fixed 2026-08-14 (Issue #335 - Property screen): this used to hardcode every column to
        group `G:0` (`nav:form:G:0:R:<row>:C:<col>:dd_input`), assuming Date and every mandatory
        dropdown always share one navigator group. Confirmed live this doesn't hold: Property puts
        Date in `G:0` but its Business Unit dropdown in a SEPARATE group `G:1` (also at column
        `C:0`, not `C:1`) - the old hardcoded pattern found nothing, broke out of the loop
        immediately, and silently applied no navigator filter at all. Fixed by discovering every
        `dd_input` under `nav:form` for this `row` live, across ANY group/column, sorted by
        (group, column) ascending - matching EC's own parent-before-child visual ordering - instead
        of assuming a fixed group index. Re-discovered FRESH on every iteration (not computed once
        upfront): a child dropdown's element does not exist in the DOM at all until its parent has
        been selected, so a one-time scan taken before any selection would never see it.

        Returns the C:1 (top-parent) value actually selected, or None (legitimately, on a
        go_only-shaped screen - callers must not assert this is non-None unconditionally)."""
        top = None

        def _discover():
            return self.page.evaluate(
                """(row) => {
                const re = new RegExp('^nav:form:G:(\\\\d+):R:' + row + ':C:(\\\\d+):dd_input$');
                return Array.from(document.querySelectorAll('input[id^="nav:form:G:"]'))
                    .map(e => { const m = e.id.match(re); return m ? {g: parseInt(m[1],10), c: parseInt(m[2],10), id: e.id} : null; })
                    .filter(Boolean)
                    .sort((a, b) => a.g - b.g || a.c - b.c);
            }""",
                row,
            )

        for col in range(1, levels + 1):
            found = _discover()
            if len(found) < col:
                break
            dd = found[col - 1]["id"]
            loc = self.page.locator(css(dd))
            if loc.count() == 0:
                break
            want = values[col - 1] if values and col <= len(values) else "__FIRST__"
            base = dd[: -len("_input")]
            self.page.locator(css(base + "_button")).first.click()
            want_first = want == "__FIRST__"
            any_opt = f"xpath=//*[@id='{base}_panel']//tr[@data-item-label and normalize-space(@data-item-label)!='']"
            opt = any_opt if want_first else f"xpath=//*[@id='{base}_panel']//tr[normalize-space(@data-item-label)='{want}']"
            self.page.locator(opt).first.wait_for(state="visible", timeout=6000)
            self.page.locator(opt).first.click()
            ajax(self.page, 12000)
            if col == 1:
                top = self.page.locator(css(dd)).first.input_value()
        self._click_go()
        self._refresh_field_map()
        return top

    def _save(self, attempts=2):
        """Same 2-strike logic already proven in ec_object_iud.py's save(): an enabled Save link
        first; if the link is `ui-state-disabled` (confirmed live, Bank update: EC's own
        dirty-tracking doesn't always register a field edit made via Playwright, leaving Save
        disabled even though the field's DOM value genuinely changed), force-enable it via EC's
        own `EC.toolbar.toggleSaveButton(true)` JS API and retry, then fall back to Ctrl+S.

        Locator gotcha (confirmed live, both Bank/OV and Language/TV): matching by
        `@title='Save [Ctrl+s]'` is fragile - EC's PrimeFaces tooltip widget BLANKS the anchor's
        native `title` attribute to '' after the first hover/interaction on that toolbar (moving
        the tooltip text into its own floating widget instead), even while the link stays fully
        enabled and clickable. So after the very first Save on a screen, a title-based locator
        finds 0 matches regardless of disabled state - not a false "still disabled" signal, a
        genuinely wrong search key. Locate by the `.ui-icon-save` icon class instead (the same
        structural-signature approach already proven for toolbar disabled-detection in the
        classifier: `closest('li')` + check the LI's own className), which EC does not mutate."""
        icon = "[id^='screenToolbar'] .ui-icon-save"
        for _ in range(attempts):
            is_disabled = self.page.evaluate(
                """(sel) => { const i = document.querySelector(sel); if (!i) return null;
                const li = i.closest('li'); return li ? /ui-state-disabled|ui-submenu-state-disabled/.test(li.className) : false; }""",
                icon,
            )
            if is_disabled is False:
                self.page.locator(icon).first.click()
                ajax(self.page)
                return "button"
            self.page.evaluate("() => { if (typeof EC !== 'undefined' && EC.toolbar) EC.toolbar.toggleSaveButton(true); }")
            self.page.wait_for_timeout(300)
            is_disabled2 = self.page.evaluate(
                """(sel) => { const i = document.querySelector(sel); if (!i) return null;
                const li = i.closest('li'); return li ? /ui-state-disabled|ui-submenu-state-disabled/.test(li.className) : false; }""",
                icon,
            )
            if is_disabled2 is False:
                self.page.locator(icon).first.click()
                ajax(self.page)
                return "toggle+button"
            self.page.keyboard.press("Control+s")
            ajax(self.page)
        raise RuntimeError("Save not actionable after %d attempts (2-strike stop)" % attempts)

    def toolbar(self, action, icon=None):
        """Hover each toolbar flyout icon in turn (generic - not keyed by known text strings)
        looking for a link matching `action`, click it. Handles both OV ('New Object', 'New
        Version' under the Insert icon; 'Delete' under the Delete icon) AND TV (confirmed live,
        Language: BOTH the Insert and Delete flyouts' link text is the CLASS's own label, e.g.
        'Language' - identical text under two different icons, so text alone can't disambiguate).
        Pass `icon='insert'` or `icon='delete'` to pin which icon to search when the action text
        is ambiguous across icons (as it always is for TV) - default (None) searches both and
        takes the first match, which is only safe when the text is unique (true for OV)."""
        wanted_classes = {
            "insert": "ui-icon-insert",
            "delete": "ui-icon-delete",
            None: "ui-icon-insert') or contains(@class,'ui-icon-delete",
        }[icon]
        icons = self.page.locator(
            f"xpath=//li[contains(@class,'ui-menu-parent')]"
            f"[.//span[contains(@class,'{wanted_classes}')]]"
        )
        clicked = False
        for i in range(icons.count()):
            icons.nth(i).hover()
            self.page.wait_for_timeout(700)
            links = self.page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
            for j in range(links.count()):
                if links.nth(j).is_visible() and links.nth(j).text_content(timeout=800).strip() == action:
                    links.nth(j).click()
                    clicked = True
                    break
            if clicked:
                break
            self.page.keyboard.press("Escape")
        if not clicked:
            self.page.locator(f"xpath=//a[normalize-space(text())='{action}']").first.click()
        ajax(self.page)
        self._refresh_field_map()

    def _pager_next(self, grid_id):
        """PrimeFaces datatable 'next page' control, scoped to this grid's own container
        (the tbody id minus '_data'); falls back to a page-wide selector if that container
        can't be matched. Returns None if no paginator is present (single-page grid)."""
        table_id = grid_id[: -len("_data")] if grid_id.endswith("_data") else grid_id
        scoped = self.page.locator(f"css=#{table_id.replace(':', chr(92) + ':')} .ui-paginator-next").first
        if scoped.count():
            return scoped
        loose = self.page.locator("css=.ui-paginator-next").first
        return loose if loose.count() else None

    def _pager_first(self, grid_id):
        table_id = grid_id[: -len("_data")] if grid_id.endswith("_data") else grid_id
        scoped = self.page.locator(f"css=#{table_id.replace(':', chr(92) + ':')} .ui-paginator-first").first
        if scoped.count():
            return scoped
        loose = self.page.locator("css=.ui-paginator-first").first
        return loose if loose.count() else None

    @staticmethod
    def _pager_disabled(loc):
        return "ui-state-disabled" in ((loc.get_attribute("class") or "") if loc else "")

    def _reset_to_first_page(self, grid_id):
        first = self._pager_first(grid_id)
        if first and not self._pager_disabled(first):
            first.click()
            ajax(self.page)
            self.page.wait_for_timeout(300)

    def row_on_current_page(self, grid_id, code):
        """Membership on the currently-rendered page only, no pager navigation. Checks BOTH
        rendered text (span-based OV rows, e.g. Bank/Node) AND input .value (confirmed live,
        Financial Item Definition: its list grid renders every cell as a readonly <input
        value="..."> - the SAME convention TV grids use for editable cells, just marked readonly
        here - so a span-only or textContent-only check finds nothing even though the row is
        genuinely present and visible)."""
        return self.page.evaluate(
            """([gid, code]) => { const tb = document.getElementById(gid); if (!tb) return false;
            return Array.from(tb.querySelectorAll('tr[data-ri]')).some(tr => {
                if (tr.textContent.includes(code)) return true;
                return Array.from(tr.querySelectorAll('input')).some(inp => inp.value === code);
            }); }""",
            [grid_id, code],
        )

    def row_exists(self, grid_id, code):
        """Membership across ALL paginator pages, not just the current one - confirmed live,
        Financial Item Definition: 24 rows (> PrimeFaces' 20-per-page default) meant a freshly
        inserted row could sort onto page 2, and a current-page-only check reported a false
        'row not visible' even though the DB insert had genuinely succeeded (Bank/Node/Chemical
        Tank never exposed this - their few-row AUTOTEST scopes never paginated). Walks next-page
        until found or the pager is exhausted, then restores page 1. A single-page grid (no
        paginator) collapses to the plain current-page check - fully backward compatible."""
        if self.row_on_current_page(grid_id, code):
            return True
        nxt = self._pager_next(grid_id)
        if nxt is None:
            return False
        found, guard = False, 0
        while not self._pager_disabled(nxt) and guard < 100:
            nxt.click()
            ajax(self.page)
            self.page.wait_for_timeout(350)
            if self.row_on_current_page(grid_id, code):
                found = True
                break
            nxt = self._pager_next(grid_id)
            guard += 1
        self._reset_to_first_page(grid_id)
        return found

    def select_row(self, grid_id, code):
        """OV-style row-select: click the grid row whose text (or, for readonly-input-rendered
        grids, cell VALUE) contains `code`, opening the row-select form (updateAttributes/
        objectdates). Returns True/False. Re-derives the field map afterward. NOT the right
        gesture for TV grids (see select_grid_row) - editable TV rows are a live edit surface,
        not a click-to-open-a-separate-form flow.

        Click target (confirmed live, Financial Item Definition - the first screen whose list
        grid renders EVERY cell as a readonly `<input value="...">`, same as Bank/Node's rendered
        text-span rows visually, but with zero `<span>` elements to click): click the identified
        `tr[data-ri]` itself, resolved by the same text-or-value match `row_on_current_page()`
        uses, instead of assuming a `<span>` exists inside it - a `tr` click works whether the row
        renders spans or readonly inputs, since PrimeFaces' row-select handler is bound to the
        row, not to any specific child element.

        Pagination-aware (ported from `ec_object_iud.py`'s proven `select_row()`, confirmed live
        the hard way on the same screen - the original version only ever looked at the
        currently-rendered page, so a row sorted onto page 2 was silently unselectable)."""
        if not self.row_on_current_page(grid_id, code):
            nxt = self._pager_next(grid_id)
            guard = 0
            while nxt is not None and not self._pager_disabled(nxt) and guard < 100:
                nxt.click()
                ajax(self.page)
                self.page.wait_for_timeout(350)
                if self.row_on_current_page(grid_id, code):
                    break
                nxt = self._pager_next(grid_id)
                guard += 1
        row_index = self.page.evaluate(
            """([gid, code]) => { const tb = document.getElementById(gid); if (!tb) return -1;
            const rows = Array.from(tb.querySelectorAll('tr[data-ri]'));
            const idx = rows.findIndex(tr => tr.textContent.includes(code) ||
                Array.from(tr.querySelectorAll('input')).some(inp => inp.value === code));
            return idx >= 0 ? parseInt(rows[idx].getAttribute('data-ri'), 10) : -1; }""",
            [grid_id, code],
        )
        if row_index < 0:
            return False
        tr = self.page.locator(f"css=#{grid_id.replace(':', chr(92) + ':')} tr[data-ri='{row_index}']").first
        tr.click()
        ajax(self.page)
        self.page.wait_for_timeout(600)
        self._refresh_field_map()
        return True

    def select_grid_row(self, grid_id, value):
        """TV-style row-select: find the row containing `value` (via find_grid_row - resolves by
        content, never a remembered/assumed index) and click the row itself to mark it selected
        in the datatable's own selection model, which the toolbar Delete action reads. Distinct
        from select_row() (OV's click-to-open-a-form gesture) - TV has no such form, Delete acts
        directly on whichever row is currently selected."""
        row_idx = self.find_grid_row(grid_id, value)
        tr = self.page.locator(f"css=#{grid_id.replace(':', chr(92) + ':')} tr[data-ri='{row_idx}']").first
        tr.click()
        ajax(self.page)
        return row_idx

    def grid_cell(self, grid_id, row, col_label):
        """Resolve a specific grid cell by 0-based row index + column LABEL (via the classifier's
        column scan), not a hardcoded id. Returns a _GridCellHandle with .set(value)/.get().

        Row-index warning (confirmed live, Language/TV): a Save can re-sort/reload the grid,
        moving a just-inserted row to a DIFFERENT index (e.g. to the end) rather than leaving it
        where it was filled - the SAME "never trust position, resolve by identity" gotcha already
        true for EC row-select elsewhere. Callers that need to act on a row again AFTER a Save
        must re-resolve its index via find_grid_row(), not reuse the index used for the insert."""
        columns = scan_grid_columns(self.page, grid_id)
        match = next((c for c in columns if _norm(c["label"]) == _norm(col_label)), None)
        if not match or not match.get("sample_cell_id"):
            raise FieldNotFound(f"No grid column labeled '{col_label}' on grid {grid_id!r} "
                                 f"(known columns: {[c['label'] for c in columns]})")
        cell_id = re.sub(r":T:\d+:", f":T:{row}:", match["sample_cell_id"])
        return _GridCellHandle(self, cell_id)

    def find_grid_row(self, grid_id, value):
        """Scan every row of `grid_id` live and return the 0-based row index of the first row
        containing `value` in ANY cell (input value, since grid cells are <input> elements whose
        text content doesn't reflect their value). Raises if not found. Use this instead of a
        remembered row index any time a Save may have happened in between."""
        rows = self.page.evaluate(
            """(gid) => { const tb = document.getElementById(gid);
            return Array.from(tb.querySelectorAll('tr[data-ri]')).map(tr => ({
                ri: parseInt(tr.getAttribute('data-ri'), 10),
                cells: Array.from(tr.querySelectorAll('td')).map(td => {
                    const inp = td.querySelector('input'); return inp ? inp.value : td.textContent.trim();
                }),
            })); }""",
            grid_id,
        )
        for r in rows:
            if str(value) in r["cells"]:
                return r["ri"]
        raise FieldNotFound(f"No row containing {value!r} found in grid {grid_id!r}")


_JAVA_TOKEN_RE = re.compile(r"yyyy|MM|dd")
_JAVA_TO_PY = {"yyyy": "%Y", "MM": "%m", "dd": "%d"}


def _reformat_date_to_pattern(loc, value):
    """Read the field's `data-p-pattern` (EC's calendar widgets carry this - e.g. 'yyyy-MM-dd')
    and reformat `value` to match it, so the caller can pass a date in any of the few formats
    EC actually configures across screens without needing to know each field's specific pattern.
    Accepts ISO ('2020-01-01'), slash-DMY ('01/01/2020'), or slash-MDY - tries each parse in turn
    and keeps whichever succeeds; if `value` already matches the target pattern's shape, or no
    pattern attribute is present, returns it unchanged."""
    pattern = loc.get_attribute("data-p-pattern")
    if not pattern:
        return value
    py_pattern = _JAVA_TOKEN_RE.sub(lambda m: _JAVA_TO_PY[m.group(0)], pattern)
    import datetime as _dt

    for fmt in (py_pattern, "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            parsed = _dt.datetime.strptime(value, fmt)
            return parsed.strftime(py_pattern)
        except ValueError:
            continue
    return value  # couldn't parse against any known format - pass through, let EC's own validation flag it


def _nav_primitive(f):
    """Classify a navigator field's primitive from its id suffix - same rule as
    classify_field_by_id but without needing a live dd probe (nav dd primitives are already
    known from classify_screen's own scan; here we default to 'dropdown' for any dd_input,
    since Engine.select() only needs to know it's a dropdown to dispatch the gesture)."""
    if f["id"].endswith("da_input"):
        return "date"
    if f["id"].endswith("dd_input"):
        return "dropdown"
    return "text"


class _PopupHandle:
    def __init__(self, engine, pin_id):
        self.engine = engine
        self.pin_id = pin_id

    def pick_by_code(self, value):
        page = self.engine.page
        page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", self.pin_id)
        popup_grid = page.locator("xpath=//table[contains(@id,'PopupList') and contains(@id,':T_data')]").first
        popup_grid.wait_for(state="visible", timeout=10000)
        want_first = value in (None, "", "__FIRST__")
        row = (
            popup_grid.locator("xpath=.//tr[@data-ri]").first
            if want_first
            else popup_grid.locator("xpath=.//tr[@data-ri]").filter(has_text=str(value)).first
        )
        row.click()
        ajax(page)
        actual = page.locator(css(self.pin_id)).first.input_value()
        if not want_first and _norm(value) not in _norm(actual):
            raise VerificationEchoFailed(f"resolve_popup(...).pick_by_code({value!r}): pin shows {actual!r}")
        self.engine._refresh_field_map()
        return actual


class _GridCellHandle:
    def __init__(self, engine, cell_id):
        self.engine = engine
        self.cell_id = cell_id

    def get(self):
        loc = self.engine.page.locator(css(self.cell_id)).first
        return loc.input_value() if loc.count() else None

    def set(self, value):
        """Confirmed live (Daily Gas Stream Status, clearing a cell back to its original empty
        value): Control+A then type(str(value)) is a no-op for value='' - typing zero characters
        leaves the selection alone and the cell unchanged. Delete after Control+A actually clears
        the selection, so it works for both the empty and non-empty case (typing after Delete on
        an empty target is equivalent to typing after a successful select-all-replace)."""
        page = self.engine.page
        loc = page.locator(css(self.cell_id)).first
        loc.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Delete")
        text = str(value)
        if text:
            page.keyboard.type(text, delay=25)
        page.keyboard.press("Tab")
        ajax(page)
        actual = loc.input_value()
        if _norm(actual) != _norm(text):
            raise VerificationEchoFailed(f"grid_cell.set({value!r}): DOM re-read shows {actual!r}")
        return actual


def open_screen(page, screen_name, user=USER, pw=PW):
    """Login (if not already) + navigate to `screen_name` via the menu search, same mechanism
    as classify_screen(). Returns nothing - call Engine(page, screen_name) once the screen has
    settled (caller fills any mandatory navigator scope + clicks GO first, same as a real user)."""
    if page.locator("#username").count():
        page.fill("#username", user)
        page.fill("#password", pw)
        page.click("#kc-login")
        page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000)
        ajax(page)
    box = page.locator(css("menu:searchForm:searchTxt"))
    box.click()
    box.fill("")
    box.type(screen_name, delay=45)
    ajax(page, 7000)
    tv_link = page.locator(
        f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_name}']"
    ).first
    tv_link.click()
    ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click()
        ajax(page)
    page.wait_for_timeout(1200)


if __name__ == "__main__":
    SCREEN = os.environ.get("SCREEN", "Bank")
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not HEADED, args=["--ignore-certificate-errors"])
        page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
        page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
        open_screen(page, SCREEN)
        eng = Engine(page, SCREEN)
        print("Known field labels:", sorted(eng._by_label.keys()))
        b.close()
