"""EC Object Configuration - reusable IUD engine (OV screens).

Applies to ~95% of EC object config screens (Bank, Currency, Language-object, etc.).
Only the Navigator columns + Data Window field labels differ per object; the gestures
below are CONSTANT. Locators/field labels are ARGUMENTS - nothing is screen-hardcoded.

Verified live on EC 14.2.4 sandbox 2026-07-25 (Bank). See ec-ui-knowledge/EC_OBJECT_CONFIG_IUD.md.

Public API (all take a Playwright `page`):
    login(page, url, user, pw)
    open_object_screen(page, screen_name) -> screen label text
    row_exists(page, grid_data_id, code) -> bool
    insertObjectRecord(page, grid_data_id, fields)          # fields: [{label,value,kind}]
    updateObjectRecord(page, grid_data_id, code, fields)
    closeObjectRecord(page, grid_data_id, code, end_date)   # EC delete = End Date = Start Date

`kind` is 'text' or 'date'. Insert resolves ids in the New-Object 'objectForm';
update resolves ids in 'updateAttributes'; both by LABEL (never a blind row index).
"""
import os

WAIT = int(os.environ.get("EC_WAIT_MS", "30000"))
_SETTLE = 1200


def _css(fid):
    return "#" + fid.replace(":", "\\:")


def wait_ajax(page, t=None):
    page.wait_for_load_state("networkidle", timeout=t or WAIT)
    page.wait_for_timeout(_SETTLE)


# ---------------------------------------------------------------- login + nav
def login(page, url, user, pw):
    page.goto(url, wait_until="domcontentloaded", timeout=WAIT)
    page.fill("#username", user)
    page.fill("#password", pw)
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=WAIT * 2)
    wait_ajax(page)


def open_object_screen(page, screen_name):
    si = page.locator("#menu\\:searchForm\\:searchTxt")
    si.wait_for(state="visible", timeout=WAIT)
    si.clear()
    si.type(screen_name, delay=60)
    page.wait_for_load_state("networkidle", timeout=WAIT)
    page.wait_for_timeout(500)
    # EC 14.2.4: the search hit is a <label class="tv-link"> (was <span> pre-14.2). Match either.
    page.locator(
        "xpath=//*[self::label or self::span]"
        "[contains(@class,'tv-link') and normalize-space(text())='%s']" % screen_name
    ).first.click()
    wait_ajax(page)
    return page.locator("#screenToolbar\\:form\\:screenLabel").text_content(timeout=WAIT)


# ---------------------------------------------------------------- grid helpers
# Generic across all Bank-family OV screens: grids may be single-page or PrimeFaces-
# paginated (e.g. Port: 2 pages), and redraw asynchronously after open/GO/Save. The
# helpers below cater for both -- no per-screen tuning needed:
#   * _rows           = rows on the CURRENTLY rendered page
#   * row_exists      = membership across ALL pages (walks the paginator, resets to p1)
#   * wait_for_row    = polls for async appearance, then a full paginated sweep
#   * select_row      = navigates to the page holding the code before clicking
def _css_id(component_id):
    return component_id.replace(":", "\\:")


def _table_id(grid_data_id):
    """PrimeFaces datatable container id = the tbody data id minus the '_data' suffix."""
    return grid_data_id[:-5] if grid_data_id.endswith("_data") else grid_data_id


def _rows(page, grid_data_id):
    return page.evaluate(
        """(gid) => {
            const tb = document.getElementById(gid);
            if (!tb) return [];
            const out = [];
            tb.querySelectorAll('tr').forEach(tr => {
                const c = [];
                tr.querySelectorAll('td').forEach(td => c.push(td.textContent.trim()));
                if (c.some(x => x)) out.push(c);
            });
            return out;
        }""",
        grid_data_id,
    )


def _pager_next(page, grid_data_id):
    """The paginator 'next page' control for this grid (scoped to the datatable;
    falls back to page scope if the container id can't be matched). None if absent."""
    tid = _css_id(_table_id(grid_data_id))
    scoped = page.locator("css=#%s .ui-paginator-next" % tid).first
    if scoped.count():
        return scoped
    loose = page.locator("css=.ui-paginator-next").first
    return loose if loose.count() else None


def _pager_first(page, grid_data_id):
    tid = _css_id(_table_id(grid_data_id))
    scoped = page.locator("css=#%s .ui-paginator-first" % tid).first
    if scoped.count():
        return scoped
    loose = page.locator("css=.ui-paginator-first").first
    return loose if loose.count() else None


def _is_disabled(loc):
    return "ui-state-disabled" in ((loc.get_attribute("class") or "") if loc else "")


def _reset_to_first_page(page, grid_data_id):
    first = _pager_first(page, grid_data_id)
    if first and not _is_disabled(first):
        first.click()
        wait_ajax(page)
        page.wait_for_timeout(300)


def row_on_current_page(page, grid_data_id, code):
    """Membership on the rendered page only (no pager navigation)."""
    return any(r and r[0].strip() == code for r in _rows(page, grid_data_id))


def row_exists(page, grid_data_id, code):
    """Membership across ALL paginator pages. Walks next-page until found or the
    pager is exhausted, then restores the grid to page 1. Single-page grids (no
    paginator) collapse to the plain current-page check -- fully backward compatible."""
    if row_on_current_page(page, grid_data_id, code):
        return True
    nxt = _pager_next(page, grid_data_id)
    if nxt is None:
        return False
    found, guard = False, 0
    while not _is_disabled(nxt) and guard < 100:
        nxt.click()
        wait_ajax(page)
        page.wait_for_timeout(350)
        if row_on_current_page(page, grid_data_id, code):
            found = True
            break
        nxt = _pager_next(page, grid_data_id)
        guard += 1
    _reset_to_first_page(page, grid_data_id)
    return found


def wait_for_row(page, grid_data_id, code, timeout_ms=None):
    """Poll for the row to render (grid draws async after open/GO/Save). Cheap
    current-page check each tick handles the common timing case; a final full
    paginated sweep catches a code that sorts onto a later page."""
    attempts = max(1, (timeout_ms or WAIT) // 500)
    for _ in range(attempts):
        if row_on_current_page(page, grid_data_id, code):
            return True
        page.wait_for_timeout(500)
    return row_exists(page, grid_data_id, code)


def wait_for_row_absent(page, grid_data_id, code, timeout_ms=None):
    """Poll until the row is GONE from every page (grid redraws async after
    delete+GO; row_exists is immediate and can catch the pre-redraw render).
    Mirror of wait_for_row for delete-absence assertions."""
    attempts = max(1, (timeout_ms or WAIT) // 500)
    for _ in range(attempts):
        if not row_exists(page, grid_data_id, code):
            return True
        page.wait_for_timeout(500)
    return not row_exists(page, grid_data_id, code)


def select_row(page, grid_data_id, code):
    """Select a grid row by code. Waits for the row (async redraw), then navigates
    to the paginator page that holds it before clicking (the span for an off-page
    code is not in the DOM)."""
    if not wait_for_row(page, grid_data_id, code):
        return False
    if not row_on_current_page(page, grid_data_id, code):
        nxt = _pager_next(page, grid_data_id)
        guard = 0
        while nxt is not None and not _is_disabled(nxt) and guard < 100:
            nxt.click()
            wait_ajax(page)
            page.wait_for_timeout(350)
            if row_on_current_page(page, grid_data_id, code):
                break
            nxt = _pager_next(page, grid_data_id)
            guard += 1
    span = page.locator("css=#%s span" % _css_id(grid_data_id)).filter(has_text=code).first
    if span.count() == 0:
        return False
    span.click()
    wait_ajax(page)
    page.wait_for_timeout(800)
    return True


def read_form_record(page, grid_data_id, code, form_key="updateAttributes"):
    """Select `code` and return every form-window field as {label: value} (text/date value,
    or dropdown display label). Reusable read for test-case verification / inspection."""
    if not select_row(page, grid_data_id, code):
        raise RuntimeError("read_form_record: row not found: %s" % code)
    return page.evaluate(
        """(form) => {
            const base = 'tab:tabPanel:' + form + ':form:G:0:R:';
            const out = {};
            for (let r = 0; r < 80; r++) {
                const inn = document.getElementById(base + r + ':C:1:in');
                const dai = document.getElementById(base + r + ':C:1:da_input');
                const ddi = document.getElementById(base + r + ':C:1:dd_input');
                const el = inn || dai || ddi;
                if (!el) continue;
                const lc = document.getElementById(base + r + ':C:0')
                        || document.querySelector('[id^="' + base + r + ':C:0"]');
                const label = lc ? (lc.innerText || '').trim() : ('R' + r);
                let val = el.value || '';
                if (ddi) { const lbl = document.getElementById(base + r + ':C:1:dd_label');
                           if (lbl) val = (lbl.innerText || '').trim(); }
                out[label] = (val || '').trim();
            }
            return out;
        }""",
        form_key,
    )


# ---------------------------------------------------------------- field resolve + fill
def _resolve_field(page, form_key, label):
    """Return {'id','kind'} for the row whose C:0 label == `label`, inside the given
    form ('objectForm' | 'updateAttributes'). One field per row: input at C:1, label at C:0.
    Drives off the input id (exact, proven) and reads the label via a prefix fallback because
    the C:0 label-cell id carries a generated suffix (exact getElementById returns null)."""
    return page.evaluate(
        """([form, want]) => {
            const base = 'tab:tabPanel:' + form + ':form:G:0:R:';
            for (let r = 0; r < 80; r++) {
                const inn = document.getElementById(base + r + ':C:1:in');
                const dai = document.getElementById(base + r + ':C:1:da_input');
                const ddi = document.getElementById(base + r + ':C:1:dd_input');
                const pin = document.getElementById(base + r + ':C:1:pin');
                let el = null, kind = '';
                if (inn) { el = inn; kind = 'text'; }
                else if (dai) { el = dai; kind = 'date'; }
                else if (ddi) { el = ddi; kind = 'dropdown'; }
                else if (pin) { el = pin; kind = 'popup'; }
                if (!el) continue;
                const lc = document.getElementById(base + r + ':C:0')
                        || document.querySelector('[id^="' + base + r + ':C:0"]');
                const label = lc ? (lc.innerText || '').trim() : '';
                if (label.toLowerCase() === want.toLowerCase()) return { id: el.id, kind };
            }
            return null;
        }""",
        [form_key, label],
    )


def _fire(page, fid):
    page.evaluate(
        """(id) => { const e = document.getElementById(id);
            if (e) { e.dispatchEvent(new Event('change',{bubbles:true}));
                     e.dispatchEvent(new Event('blur',{bubbles:true})); } }""",
        fid,
    )


def select_dropdown(page, dd_input_id, value):
    """Pick an option from an EC autocomplete dropdown BY its item label. dd_input_id is the
    resolved '...:C:1:dd_input'; the PrimeFaces widget prefix is that minus '_input' (=> '...:dd'),
    with '<prefix>_button' (chevron) + '<prefix>_panel' (options). Match tr[data-item-label] via
    normalize-space (stored labels can carry leading/double spaces). One reopen retry (a pending
    re-render can close the panel). Typing into autocomplete dds is unreliable - never .fill()."""
    prefix = dd_input_id[:-6] if dd_input_id.endswith("_input") else dd_input_id
    any_opt = "xpath=//*[@id='%s_panel']//tr[@data-item-label and normalize-space(@data-item-label)!='']" % prefix
    # value None/''/'__FIRST__' => take the first available option; also used as fallback when a
    # requested value isn't in the panel (cascade child: its options only appear once the parent
    # dropdown - filled earlier in form order - is selected). So cascade + stale values both resolve.
    want_first = value in (None, "", "__FIRST__")
    opt = None if want_first else ("xpath=//*[@id='%s_panel']//tr[normalize-space(@data-item-label)='%s']" % (prefix, value))
    for attempt in range(2):
        page.locator(_css(prefix + "_button")).first.click()
        try:
            page.locator(opt or any_opt).first.wait_for(state="visible", timeout=6000)
            break
        except Exception:
            if attempt == 0:
                page.keyboard.press("Escape")
                page.wait_for_timeout(1200)
            elif opt is not None:
                opt = None  # requested value absent -> retry accepting ANY (first) option
                page.locator(_css(prefix + "_button")).first.click()
                try:
                    page.locator(any_opt).first.wait_for(state="visible", timeout=6000)
                except Exception:
                    raise RuntimeError("dropdown has no options: %s (value=%r)" % (dd_input_id, value))
            else:
                raise RuntimeError("dropdown has no options: %s" % dd_input_id)
    target = opt if (opt is not None and page.locator(opt).count() > 0) else any_opt
    page.locator(target).first.click()
    wait_ajax(page)
    page.wait_for_timeout(400)


def pick_popup(page, pin_id, value):
    """Select a 'Pick from EC Object' popup reference (the Playwright twin of RF Pick From/First EC Object
    Popup). pin_id = the readonly '...:pin' input; its launch button is pin_id + 'B'. JS-click the button
    (a normal click times out - the dialog mask appears mid-click), wait for the popup iframe + its grid
    'PopupList:form:T_data', click the first row (value in None/''/'__FIRST__') or the row whose input
    .value / text matches value, verify the pin input took a value. Location-agnostic: works for a form
    pin or a navigator pin. GOTCHA: the popup list is filtered by the navigator scope - empty if unset."""
    page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin_id)
    page.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    # Wait for the grid INSIDE the iframe (frame_locator pierces the iframe - the proven RF pattern).
    # A clean timeout here == empty/absent source list (navigator scope not set), not a code fault.
    try:
        page.frame_locator('css=[id="popupIFrame"]').locator('css=[id="PopupList:form:T_data"]').first.wait_for(
            state="visible", timeout=15000)
    except Exception:
        raise RuntimeError("popup opened but grid 'PopupList:form:T_data' never appeared for %s "
                           "(empty source list - check the navigator scope is set first)" % pin_id)
    page.wait_for_timeout(1500)
    fr = None
    for f in page.frames:
        try:
            if f.query_selector('[id="PopupList:form:T_data"]'):
                fr = f
                break
        except Exception:
            pass
    if fr is None:
        raise RuntimeError("popup grid not found (iframe) for %s" % pin_id)
    want = None if value in (None, "", "__FIRST__") else value
    picked = fr.evaluate(
        """(want) => {
            const tb = document.getElementById('PopupList:form:T_data'); if (!tb) return false;
            for (const tr of tb.querySelectorAll('tr')) {
                const inp = tr.querySelector('td input'); const v = inp ? inp.value.trim() : '';
                const t = (tr.innerText || '').trim();
                if (want === null || v === want || t === want || t.startsWith(want)) {
                    const td = tr.querySelector('td'); if (td) { td.click(); return true; } } }
            return false; }""",
        want,
    )
    if not picked:
        raise RuntimeError("popup row not found (value=%r, first-available if None) for %s" % (value, pin_id))
    page.wait_for_selector('css=[id="popupIFrame"]', state="hidden", timeout=15000)
    page.wait_for_timeout(800)
    val = page.eval_on_selector(_css(pin_id), "e => e.value")
    if not (val and val.strip()):
        raise RuntimeError("popup pick did not fill the pin field: %s" % pin_id)


def fill_field(page, fid, value, kind):
    if kind == "dropdown":
        select_dropdown(page, fid, value)
        return
    if kind == "popup":
        pick_popup(page, fid, value)
        return
    el = page.locator(_css(fid))
    if el.count() == 0 or not el.is_visible():
        raise RuntimeError("field not visible: %s" % fid)
    el.click()
    el.fill(value)
    if kind == "date":
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
    _fire(page, fid)
    page.wait_for_timeout(350)


def save(page, attempts=2):
    """Save the screen, 2-strike then raise. Returns the method that worked.
    Order: enabled Save button -> force-enable via EC.toolbar then click (grafted from the legacy
    Bank bundle; robust when the button stays greyed) -> Ctrl+S."""
    enabled = "xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]"
    disabled = "xpath=//a[@title='Save [Ctrl+s]' and contains(@class,'ui-state-disabled')]"
    for _ in range(attempts):
        btn = page.locator(enabled)
        if btn.count() > 0:
            btn.first.click()
            wait_ajax(page)
            return "button"
        # legacy fallback: force-enable the Save button, then click
        page.evaluate("() => { if (typeof EC !== 'undefined' && EC.toolbar) EC.toolbar.toggleSaveButton(true); }")
        page.wait_for_timeout(300)
        btn2 = page.locator(enabled)
        if btn2.count() > 0:
            btn2.first.click()
            wait_ajax(page)
            return "toggle+button"
        page.keyboard.press("Control+s")
        wait_ajax(page)
        # if Save went disabled again the write likely landed; loop re-checks
        if page.locator(disabled).count() > 0:
            return "ctrl+s"
    raise RuntimeError("Save not actionable after %d attempts (2-strike stop)" % attempts)


def click_go(page):
    """Reload the object list. Manage-object OV: click the navigator GO. Custom-URL OV:
    NO GO button -> reload via the toolbar Refresh icon instead (grid = nav:form:T_data). Generalises both.

    Fixed 2026-08-14 (Issue #345 - Stream Item false "no grid renders" negative): a single
    hardcoded GO id (`button:form:B`) silently fell through to Refresh (which does NOT apply
    the navigator filter) on any screen whose real GO button uses a different id - confirmed
    live, Stream Item's real GO is `buttongo:form:B`, producing a misleading "no data" result
    on a screen that actually had 14 pages of real rows. Same structural id list already
    proven in the newer engine.py's _click_go() (Universal Screen Engine project) - ported
    here so the older per-screen driver gets the same fix, not just new-engine screens."""
    for gid in ("go_button:form:B", "button:form:B", "navButton:form:B", "buttongo:form:B"):
        go = page.locator("#" + gid.replace(":", "\\:"))
        if go.count() > 0 and go.is_visible():
            go.first.click()
            wait_ajax(page)
            return
    rf = page.locator("xpath=//a[starts-with(@title,'Refresh') and not(contains(@class,'ui-state-disabled'))]")
    if rf.count() > 0 and rf.first.is_visible():
        rf.first.click()
        wait_ajax(page)


def apply_ovgm_navigator(page, levels=4, row=1):
    """OV-GM (grid manageObject:form:T_data) is navigator-GATED: the grid is empty until a cascade of
    navigator dropdowns (Business Unit / Production Unit -> Area -> Facility Class 1 ...) is set + GO.
    Fill nav:form:G:0:R:<row>:C:1..N dd FIRST-AVAILABLE parent->child (child options only render after the
    parent is chosen), click GO, and RETURN the C:1 (top-parent) value. The insert form's parent-dd (e.g.
    'Op Production Unit' / 'Business Unit Name') must be set to that returned value or the new row won't be
    grid-visible under this scope. `levels` = max cascade columns to try (stops at the first absent column)."""
    top = None
    for col in range(1, levels + 1):
        dd = "nav:form:G:0:R:%d:C:%d:dd_input" % (row, col)
        if page.locator(_css(dd)).count() == 0:
            break
        select_dropdown(page, dd, "__FIRST__")
        page.wait_for_timeout(700)
        if col == 1:
            top = page.eval_on_selector(_css(dd), "e => e.value")
    click_go(page)
    return top


def ec_error(page):
    """Detects EC's own error banner by its STRUCTURAL marker (the ErrorRowClass row / ui-icon-ec-ERROR
    icon PrimeFaces renders for any error message), not by substring-matching the message text. The
    prior substring check ("Error" in txt or "Required" in txt) missed real error banners whose text
    didn't happen to contain either word (e.g. Property's "Object not found. The referenced object could
    not be found." - issue #319) while every message this function is meant to catch, including that
    one, carries the same class marker (confirmed live on both a "Required fields" validation error and
    the "Object not found" case)."""
    info = page.evaluate(
        """() => { const n = document.getElementById('ECNotificationArea')
            || document.getElementById('ECClientNotificationArea');
            if (!n) return {has_error: false, txt: ''};
            const has_error = !!n.querySelector('.ErrorRowClass, [class*="ui-icon-ec-ERROR"]');
            return {has_error: has_error, txt: n.textContent.trim()}; }"""
    )
    if not info["has_error"]:
        return ""
    return info["txt"].replace("EC.jsMessage.clear();", "").strip()[:200]


# ---------------------------------------------------------------- I / U / D
def _open_new_object(page):
    li = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    li.first.hover()
    page.wait_for_timeout(900)
    page.locator(
        "xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']"
    ).first.click()
    wait_ajax(page)


def insertObjectRecord(page, grid_data_id, fields):
    """fields = [{'label','value','kind'}] against the New-Object form."""
    _open_new_object(page)
    for f in fields:
        r = _resolve_field(page, "objectForm", f["label"])
        if not r:
            raise RuntimeError("insert: field label not found: %s" % f["label"])
        fill_field(page, r["id"], f["value"], r["kind"])
    save(page)
    err = ec_error(page)
    click_go(page)
    if err:
        raise RuntimeError("insert save error: %s" % err)


def updateObjectRecord(page, grid_data_id, code, fields):
    if not select_row(page, grid_data_id, code):
        raise RuntimeError("update: row not found: %s" % code)
    for f in fields:
        r = _resolve_field(page, "updateAttributes", f["label"])
        if not r:
            raise RuntimeError("update: field label not found: %s" % f["label"])
        fill_field(page, r["id"], f["value"], r["kind"])
    save(page)
    err = ec_error(page)
    click_go(page)
    if err:
        raise RuntimeError("update save error: %s" % err)


# objectdates row R:0 = Start Date (C:1) + End Date (C:3); label 'End Date' sits at C:2, so
# End Date is resolved by its known cell id, not the one-field-per-row label scan.
END_DATE_ID = "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input"


def closeObjectRecord(page, grid_data_id, code, end_date, end_date_id=END_DATE_ID):
    """EC delete = End Date = Start Date (zero-length window). No toolbar Delete for EC Objects."""
    if not select_row(page, grid_data_id, code):
        raise RuntimeError("delete: row not found: %s" % code)
    if page.locator(_css(end_date_id)).count() == 0:
        raise RuntimeError("delete: End Date field not found: %s" % end_date_id)
    fill_field(page, end_date_id, end_date, "date")
    save(page)
    err = ec_error(page)
    click_go(page)
    if err:
        raise RuntimeError("delete save error: %s" % err)
