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


def _classify_static(f, dd_cache):
    """Resolve the free (no-click-required) primitives from id/type alone - checkbox, date,
    popup (':pin' suffix), and plain text are all structurally determined by EC's own markup
    conventions, no interaction needed. A 'dd_input'-suffixed field is genuinely ambiguous
    (dropdown vs popup-picker) without a live click (classify_dd) - checks `dd_cache` first
    (a field already resolved earlier this session is free to look up again) and only returns
    the placeholder 'dropdown_or_popup' for a genuinely never-seen id.

    Fixed 2026-08-16 (owner-directed): _refresh_field_map() used to call classify_field_by_id()
    eagerly for every visible field, which click-probed EVERY 'dd_input' field on the form the
    moment it appeared - including fields the current task never touches (Project Data Mapping
    Setup's New Object form has ~11 dropdown fields; a task using only 2-3 of them still triggered
    a live click on all 11). Only the dd_input case ever required a click at all - every other
    primitive was already free. Deferring resolution of just that one case to first actual use
    (see Engine._resolve_primitive) means untouched fields are never clicked. Checking dd_cache
    here (not just inside _resolve_primitive) matters because fill()/select()/check() all call
    _refresh_field_map() again at the end (Save/New Object/row-select can change which form is
    showing) - without this cache check, that rebuild would reset an already-resolved field straight
    back to the unresolved placeholder every time, even though nothing about it actually changed."""
    if f["type"] == "checkbox":
        return "checkbox"
    if f["id"].endswith("da_input"):
        return "date"
    if f["id"].endswith("pin"):
        return "popup"
    if f["id"].endswith("dd_input"):
        return dd_cache.get(f["id"], "dropdown_or_popup")
    return "text"


class Engine:
    """One instance = one open, already-navigated EC screen. Build via open_screen()."""

    def __init__(self, page, screen_name):
        self.page = page
        self.screen_name = screen_name
        # Fixed 2026-08-15 (Bank): classify_dd()'s dropdown-vs-popup probe is a real live click on
        # the field - structurally correct only once per screen session, since it never changes for
        # an already-open screen. Without this cache, _refresh_field_map() (called after every
        # action) re-probed EVERY dd_input field, including ones the current task never touches
        # (e.g. Bank's optional Country field got re-clicked on every Insert/Save/row-select).
        self._dd_cache = {}
        self._refresh_field_map()

    def _resolve_primitive(self, f):
        """Lazily resolve a field's real primitive on first actual use (fill/select/check/
        resolve_popup/_field). Only 'dropdown_or_popup' (the placeholder _classify_static() leaves
        for any 'dd_input' field) ever needs this - everything else was already resolved for free
        at scan time. Mutates the field dict in place (self._by_label holds the same dict objects
        _refresh_field_map() built), so once resolved it stays resolved until the next refresh."""
        if f["primitive"] == "dropdown_or_popup":
            f["primitive"] = classify_dd(self.page, f["id"], cache=self._dd_cache)
        return f["primitive"]

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
                primitive = _classify_static(f, self._dd_cache) if source != "navigator" else _nav_primitive(f)
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

    def field_inventory(self, grid_id=None):
        """Read-only, structured snapshot of every fillable field currently visible on this screen,
        grouped by region: 'navigator', 'objectForm' (Insert), 'updateAttributes'/'objectdates'
        (row-select/Update/Delete), and - if a grid_id is supplied - 'grid_columns'. Each form/nav
        entry carries label + mandatory (yellow) + primitive (text/date/dropdown/checkbox/popup).

        Built entirely from the field map _refresh_field_map() already maintains (self._by_label) -
        no extra live probing beyond what's already been scanned/cached. Intended as the single
        place to answer "what actually needs filling on this screen" before writing task-specific
        fill()/select() calls, instead of guessing or re-scanning ad hoc per task.

        Fixed 2026-08-16 (lazy dd classification): a 'dd_input' field this Engine instance has never
        actually fill()/select()-ed yet will show `primitive: "dropdown_or_popup"` here rather than
        a resolved "dropdown"/"popup" - deliberately, since resolving it requires the live click this
        change was built to avoid on untouched fields. Call fill()/select() on a specific field (or
        add a one-off `self._resolve_primitive(self._field(label))` if inventory-time certainty is
        genuinely needed) to force resolution for that one field."""
        by_source = {}
        for f in self._by_label.values():
            by_source.setdefault(f["source"], []).append(
                {"label": f["label"], "mandatory": f["mandatory"], "primitive": f["primitive"]}
            )
        inventory = {src: sorted(fields, key=lambda x: x["label"]) for src, fields in by_source.items()}
        if grid_id:
            inventory["grid_columns"] = [
                {"label": c["label"]} for c in scan_grid_columns(self.page, grid_id) if c.get("label")
            ]
        return inventory

    def _field(self, label):
        f = self._by_label.get(_norm(label))
        if not f:
            raise FieldNotFound(f"No visible field labeled '{label}' on {self.screen_name!r} "
                                 f"(known labels: {sorted(x['label'] for x in self._by_label.values())})")
        self._resolve_primitive(f)
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
                # Fixed 2026-08-17 (Meter Run, batch-3 stability test): a numeric text field can
                # come back auto-formatted by EC itself (e.g. typed '1' redisplays as '1.00') -
                # confirmed a real, successful fill, not a failure; the real hand-written driver
                # (ec_object_iud.py's fill_field()) has no verification-echo at all, so it never
                # hit this false negative. Only fall back to a numeric-equality check when BOTH
                # sides actually parse as numbers - a genuine text mismatch (wrong value entirely)
                # must still fail as before.
                try:
                    ok = float(actual) == float(typed_value)
                except ValueError:
                    ok = False
        if not ok:
            raise VerificationEchoFailed(f"fill({label!r}, {value!r}): DOM re-read shows {actual!r} after fill")
        return actual

    def select(self, label, value):
        """dropdown field. Click the button, match the panel row by data-item-label, close.
        Verification-echo: re-reads the dd's displayed label afterward.

        Type-to-search fallback (open-items tracker #4, root-caused on Project Data Mapping
        Setup / Phase 4 pilot 3): some `dd_input` fields are server-side type-to-search
        autocompletes - the panel renders visible but stays EMPTY ("No records found") until
        real text is typed, confirmed live on Target Property/Reference (clicking the button
        alone never showed options regardless of how much real backing data existed; typing a
        substring of the real code/name triggered the actual server search). `classify_dd()`
        currently classifies these identically to a plain full-list dropdown (`'dropdown'`
        primitive) - both share the same `ui-autocomplete-panel` structure, so the caller has
        no way to know in advance which behavior a given field has. Fix: try the plain
        click-only path first (fast, correct for the common full-list case); if no option ever
        renders and a real search value was given (not `__FIRST__`), type that value into the
        input to trigger the search, then retry - unifying both widget behaviors under one
        gesture instead of requiring a separate primitive or per-screen workaround."""
        f = self._field(label)
        if f["primitive"] != "dropdown":
            raise ValueError(f"select() called on a '{f['primitive']}' field ({label!r})")
        base = f["id"][: -len("_input")]
        loc_input = self.page.locator(css(f["id"])).first
        self.page.locator(css(base + "_button")).first.click()
        want_first = value in (None, "", "__FIRST__")
        any_opt = f"xpath=//*[@id='{base}_panel']//tr[@data-item-label and normalize-space(@data-item-label)!='']"
        exact_opt = f"xpath=//*[@id='{base}_panel']//tr[normalize-space(@data-item-label)='{value}']"
        contains_opt = f"xpath=//*[@id='{base}_panel']//tr[@data-item-label and contains(@data-item-label,'{value}')]"
        loc = self.page.locator(any_opt if want_first else exact_opt).first
        try:
            loc.wait_for(state="visible", timeout=6000)
        except Exception:
            if want_first:
                raise FieldNotFound(
                    f"select({label!r}, '__FIRST__'): panel never showed any option - this is "
                    f"likely a type-to-search field with no default list; '__FIRST__' cannot "
                    f"resolve it, a real search value is required"
                )
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(300)
            loc_input.click(force=True)
            loc_input.type(str(value), delay=80)
            self.page.wait_for_timeout(1500)
            loc = self.page.locator(contains_opt).first
            loc.wait_for(state="visible", timeout=6000)
        picked_label = loc.get_attribute("data-item-label")
        loc.click()
        ajax(self.page)
        actual = loc_input.input_value()
        if _norm(actual) != _norm(picked_label):
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
        """Named top-level actions: 'Save', 'GO'. For toolbar menu actions use toolbar().

        Fixed 2026-08-17 (External Location, round-2 stability test): every existing hand-written
        driver's insertObjectRecord/updateObjectRecord/closeObjectRecord (ec_object_iud.py) calls
        click_go() immediately after save() - this Engine's click("Save") never did. Confirmed live
        this is a real gap, not cosmetic: right after a fresh Insert+Save, select_row() can return
        False because the grid was never re-queried, so a caller falls through to reading a field
        from whatever form is still in the DOM - on External Location this resolved 'Start Date' to
        the stale (still-present, unrefreshed) objectForm field instead of the real objectdates one,
        showing a wrong value that then made the following End=Start delete fail with EC's own
        'Illegal end date... references from other objects' error. Reproduced on a completely fresh,
        never-before-touched code (ruling out session/data contamination) - a real engine defect, not
        a screen limitation or test-harness gap. Re-querying via GO here (a no-op on screens with no
        GO button, e.g. Bank's custom-URL OV - confirmed safe, canary still passes) matches every
        proven driver's own behavior instead of leaving the grid state stale after Save."""
        if action == "Save":
            self._save()
            err = ec_error(self.page)  # MUST run before _refresh_field_map() - see SaveFailed
            if err:
                raise SaveFailed(err)
            self._click_go()
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

    def apply_navigator(self, values=None, levels=None, row=1):
        """OV-GM navigator cascade - generic, structural, no per-screen hardcoding. The grid on an
        OV-GM screen is empty until a cascade of navigator dropdowns (Business Unit -> Production
        Unit -> Area -> ...) is set + GO; child options only render once the parent is chosen.

        - `values=None` (default): fill each column C:1..`levels` (default 4) FIRST-AVAILABLE,
          parent before child (ports `ec_object_iud.py`'s proven `apply_ovgm_navigator()`).
        - `values=[...]`: fill C:1..len(values) with these EXACT values instead of first-available
          (for a screen where the default first option has no valid downstream combination -
          the same class of gotcha the classifier's `NAV_HINT_OPTION` exists to work around).
          `levels` defaults to `len(values)` here - see the 2026-08-17 fix note below for why.
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

        Fixed 2026-08-17 (Service, round-5 stability test): `levels` used to default to a flat 4
        regardless of `values`, so a caller passing `values=["TS3 BU1"]` on a screen whose extra
        nav columns are NOT parent-gated (all present in the DOM upfront, unlike Property's true
        cascade) got those extra columns silently filled with `__FIRST__` too - two filters the
        caller never asked for. Confirmed live: this narrowed Service's grid from its real 20 rows
        down to 1 unrelated row, hiding a freshly-inserted object entirely (no error - it just
        vanished from the grid). The real hand-written driver only ever sets C:1 and clicks GO,
        never touching C:2/C:3. Root-caused via direct comparison: `apply_navigator(values=["TS3
        BU1"], levels=1)` correctly showed all 20 rows including the hidden one; the default
        `levels=4` call showed only 1. Fix: when `values` is given and `levels` is not explicitly
        overridden, default `levels` to `len(values)` - matching every real driver's own
        touch-only-what-I-set behavior. `values=None` (first-available mode) keeps defaulting to 4,
        unchanged, since that path has no caller-supplied list to size against.

        Returns the C:1 (top-parent) value actually selected, or None (legitimately, on a
        go_only-shaped screen - callers must not assert this is non-None unconditionally)."""
        if levels is None:
            levels = len(values) if values else 4
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


def ensure_dialog_in_view(page, timeout=3000):
    """Fixed 2026-08-17 (Chemical Stream, item 1 of the flagged round-3 issues): EC's popup
    dialogs (PrimeFaces .ui-dialog, draggable via their own .ui-dialog-titlebar header) can
    render appearing far down a long insert form and end up mostly or fully below the visible
    viewport - confirmed live via direct measurement (title bar at y=889 on a 1080px-tall
    viewport). Neither page-level scrolling NOR element.scrollIntoView() moves it at all
    (measured: window.scrollY stayed 0, the dialog's own position barely changed) - the dialog's
    position is independent of document scroll. Owner-diagnosed fix: it's a DRAGGABLE dialog: a
    real mouse down/move/up sequence on its own title bar repositions the whole thing, exactly
    like a human would drag it. Confirmed live, reproduced twice: dragging the title bar to near
    the top of the screen brings its full content into a normal Playwright-clickable position -
    no coordinate-click hack or bigger viewport needed. No-op if the dialog is already
    comfortably in view (title bar in the top 30% of the viewport) - safe to call unconditionally
    after any popup/dialog opens, not just when a caller suspects a problem."""
    try:
        titlebar = page.locator(".ui-dialog-titlebar.ui-draggable-handle").last
        titlebar.wait_for(state="visible", timeout=timeout)
    except Exception:
        return False
    box = titlebar.bounding_box()
    if not box:
        return False
    viewport_h = page.evaluate("() => window.innerHeight")
    if box["y"] < viewport_h * 0.3:
        return False
    start_x = box["x"] + box["width"] / 2
    start_y = box["y"] + box["height"] / 2
    target_y = 120
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    steps = 15
    for i in range(1, steps + 1):
        cur_y = start_y + (target_y - start_y) * i / steps
        page.mouse.move(start_x, cur_y)
        page.wait_for_timeout(20)
    page.mouse.up()
    page.wait_for_timeout(300)
    return True


class _PopupHandle:
    def __init__(self, engine, pin_id):
        self.engine = engine
        self.pin_id = pin_id

    def pick_by_code(self, value):
        page = self.engine.page
        page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", self.pin_id)
        popup_grid = page.locator("xpath=//table[contains(@id,'PopupList') and contains(@id,':T_data')]").first
        popup_grid.wait_for(state="visible", timeout=10000)
        ensure_dialog_in_view(page)
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
    # Fixed 2026-08-14 (Universal Screen Engine open-items tracker #1): root-caused via live DOM
    # instrumentation (logging computed style + ancestor chain, not blind is_visible() polling).
    # This function's OWN trailing action below (`minmaxMenu` click, "expand to full page") closes
    # #ec-menu-container_0 (the panel the search box lives in) at the END of every call - so a 2nd
    # open_screen() call in the same page session finds the search box genuinely display:none
    # (confirmed live: box.offsetParent is null, ancestor #ec-menu-container_0 carries class
    # 'hidden' + computed display:none), not merely covered by a stray panel as first assumed.
    # Self-inflicted: the function never re-opens the panel it closed last time before trying to
    # use the search box inside it. Fix: re-expand first if the box isn't visible.
    box = page.locator(css("menu:searchForm:searchTxt"))
    if not box.is_visible():
        mm_reopen = page.locator(css("screenToolbar:form:minmaxMenu"))
        if mm_reopen.count() and mm_reopen.first.is_visible():
            mm_reopen.first.click()
            ajax(page)
            box.wait_for(state="visible", timeout=10000)
    box.click()
    box.fill("")
    box.type(screen_name, delay=45)
    ajax(page, 7000)
    tv_link = page.locator(
        f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_name}']"
    ).first
    tv_link.click()
    # Universal Screen Engine open-items tracker #6b: if the previous screen was left dirty, this
    # click triggers EC's genuine "Unsaved Changes" dialog - handled centrally inside ajax() (see
    # universal_classifier._dismiss_unsaved_changes_dialog) since the same dialog can also appear
    # on other actions (e.g. select_row() opening a different record), not just navigation.
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
