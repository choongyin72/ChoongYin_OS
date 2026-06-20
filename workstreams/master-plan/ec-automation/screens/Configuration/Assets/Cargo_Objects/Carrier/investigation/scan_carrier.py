"""scan_ec_screen.py - Step-2 live DOM scan, keyed by SCREEN NAME only. READ-ONLY (opens forms, never
Saves). Pairs with resolve_ec_screen.py (Step 1 / DB metadata). Captures the bits config tables don't
carry: the treeview menu path (from the tv-link title), toolbar New/Delete enabled-state, navigator
shape + which nav fields are mandatory (yellow), the grid id, and the form/field ids. For GATED screens
(a mandatory nav dropdown - OV-GM / BU-gated / cascade) it fills the mandatory dropdown(s) first-option
in group order + clicks GO so the grid and forms actually load before capture (fills ONLY yellow dds -
over-filling white nav fields empties the grid). For OV it then drives New-Object + row-select to read
objectForm/updateAttributes/objectdates ids; for TV it reads the grid cells. READ-ONLY (never Saves). Usage:
   SCREEN="Bank" py tmp/scripts/scan_ec_screen.py        (EC_HEADED=1 to watch)
   SCREEN="Contract Area" py tmp/scripts/scan_ec_screen.py   (gated: auto-fills the Business Unit dd + GO)
"""
import os
import oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = os.environ.get("SCREEN", "Bank")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
YELLOW = "rgb(252, 249, 192)"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


# --- Step 1 (DB) inline: class_name + type, so the scan knows OV vs TV ---
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
cand = [r[0] for r in cur.execute("""SELECT class_name FROM class_property_cnfg
        WHERE property_code='LABEL' AND lower(property_value)=:s""", [SCREEN.lower()]).fetchall()]
real = [c for c in cand if not any(x in c for x in ("_ROWSORT", "_TEST", "AUTOSAVE"))]
ctype = None
if real:
    row = cur.execute("SELECT class_type, time_scope_code FROM class_cnfg WHERE class_name=:c", [real[0]]).fetchall()
    ctype = row[0][0] if row else None
cur.close()
is_ov = ctype == "OBJECT"
print(f"SCREEN='{SCREEN}'  class={real}  CLASS_TYPE={ctype}  -> {'OV' if is_ov else 'TV' if ctype else '?'}")


def dump_inputs(page, id_substr):
    """ids + value + mandatory(yellow) + nearest label text for inputs whose id contains id_substr."""
    return page.evaluate("""(sub) => [...document.querySelectorAll('input,select,textarea')]
        .filter(e=>e.id && e.id.includes(sub) && e.type!=='hidden')
        .map(e=>{ const y=getComputedStyle(e).backgroundColor==='""" + YELLOW + """';
            let lab='';
            // label cell = same row/col-0 (replace :C:N:suffix with :C:0); fall back to row text
            const m=e.id.match(/^(.*:R:\\d+):C:\\d+:/);
            if(m){ const lc=document.getElementById(m[1]+':C:0:la')||document.getElementById(m[1]+':C:0:out')||document.querySelector("[id^='"+m[1]+":C:0']"); if(lc) lab=(lc.innerText||lc.value||'').trim(); }
            if(!lab){ const r=e.closest('tr'); if(r){const c=[...r.querySelectorAll('td,th,label')].map(x=>(x.innerText||'').trim()).filter(Boolean); lab=c[0]||'';} }
            return {id:e.id, val:e.value, mandatory:y, label:lab}; }).slice(0,30)""", id_substr)


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=600 if HEADED else 0, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(css("menu:searchForm:searchTxt")); box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 7000)
    tv_link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first
    # EC stores the full menu breadcrumb in title= on a tv-link (or a near ancestor). Search may render
    # several tv-links with the same text; take the first whose title actually holds a '>'-path.
    tv_path = page.evaluate("""(name) => {
        const ls=[...document.querySelectorAll('.tv-link')].filter(e=>(e.textContent||'').trim()===name);
        for(const e of ls){ const t=((e.getAttribute('title')||e.getAttribute('data-tooltip')||'')).trim(); if(t.includes('>')) return t; }
        for(const e of ls){ let n=e; for(let i=0;i<4&&n;i++){ n=n.parentElement; if(n&&n.getAttribute){ const t=(n.getAttribute('title')||'').trim(); if(t.includes('>')) return t; } } }
        return ''; }""", SCREEN).strip()
    tv_link.click()
    ajax(page)
    print("treeview path:", tv_path or "(not in title attr - capture via hover/Maintain Treeview)")
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)

    # 1) toolbar New/Delete enabled-state (detect by ICON class - works for text menus AND icon-only buttons)
    tb = page.evaluate("""() => { const out={};
        const find = (...cs) => { for(const c of cs){ const e=document.querySelector('span.'+c)||document.querySelector('.'+c); if(e) return e; } return null; };
        const dis = e => { const li=e&&e.closest('li,a'); return li ? /ui-state-disabled|ui-submenu-state-disabled/.test(li.outerHTML) : false; };
        const ins=find('ui-icon-insert','ui-icon-add'); const del=find('ui-icon-delete','ui-icon-remove','ui-icon-trash');
        if(ins) out.insert = dis(ins)?'DISABLED':'enabled';
        if(del) out.delete = dis(del)?'DISABLED':'enabled';
        return out; }""")
    print("toolbar:", tb, " (default assumption: enabled; only flag the rare DISABLED)")

    # 2) navigator fields (FULL id) + which are mandatory (yellow) + GO button
    nav = page.evaluate("""() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:']").forEach(e=>{
        const m=e.id.match(/nav:form:(G:\\d+):R:\\d+:C:\\d+:(da_input|dd_input|in)/); if(!m) return;
        const y=getComputedStyle(e).backgroundColor==='""" + YELLOW + """';
        out.push({id:e.id, grp:m[1], kind:m[2], mandatory:y}); });
        const go=['go_button:form:B','button:form:B','navButton:form:B'].filter(id=>document.getElementById(id));
        return {fields:[...new Map(out.map(o=>[o.id,o])).values()], go}; }""")
    print("navigator:", {"fields": [{k: f[k] for k in ("grp", "kind", "mandatory")} for f in nav["fields"]], "go": nav["go"]})

    # 2b) GATED screen: fill the mandatory nav dropdown(s) first-option (in group order) + GO, so the grid
    #     and forms actually load. Fill ONLY yellow/mandatory dds - over-filling white nav fields empties the grid.
    go_id = nav["go"][0] if nav["go"] else "button:form:B"
    mand_dds = [f for f in nav["fields"] if f["kind"] == "dd_input" and f["mandatory"]]
    if mand_dds:
        print(f"gated nav: filling {len(mand_dds)} mandatory dropdown(s) first-option + GO")
        for f in sorted(mand_dds, key=lambda x: x["grp"]):
            ddp = f["id"][:-len("_input")]   # ...:dd_input -> ...:dd
            try:
                page.locator(css(ddp + "_button")).first.click(); page.wait_for_timeout(900)
                opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]").first
                opt.wait_for(state="visible", timeout=6000)
                picked = (opt.get_attribute("data-item-label") or "").strip()
                opt.click(); ajax(page, 12000)
                print(f"   {f['grp']} <- '{picked}'")
            except Exception as e:
                print(f"   {f['grp']} fill err: {str(e)[:60]}")
        try:
            page.locator(css(go_id)).first.click(); ajax(page, 20000)
            print("   GO clicked")
        except Exception as e:
            print("   GO err:", str(e)[:60])

    # 3) grid id (now populated, post-GO for gated screens)
    grid = page.evaluate("""() => { const t=[...document.querySelectorAll("[id$=':T_data']")].filter(e=>e.offsetParent||e.querySelector('tr'));
        return t.length? t[0].id : null; }""")
    print("grid id:", grid)

    if is_ov:
        # 4) UPDATE + DELETE FIRST (while the list is shown): select a data row -> updateAttributes + objectdates
        try:
            sp = page.locator(f"xpath=//*[@id='{grid}']//tr//span[normalize-space(text())!='']").first
            if sp.count():
                sp.click(); ajax(page); page.wait_for_timeout(1200)
                print("\nUPDATE updateAttributes fields (id | mandatory | label):")
                for f in dump_inputs(page, "updateAttributes:form")[:8]:
                    print(f"   {f['id']:55s} mand={f['mandatory']!s:5s} {f['label'][:22]}")
                print("DELETE objectdates fields (End Date = the C:3 da_input):")
                for f in dump_inputs(page, "objectdates:form"):
                    print(f"   {f['id']:55s} {f['label'][:22]}")
        except Exception as e:
            print("  row-select scan err:", str(e)[:70])
        # 5) INSERT LAST: hover Insert -> New Object -> dump objectForm (this leaves the screen in insert mode)
        try:
            page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
            page.wait_for_timeout(900)
            links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
            for i in range(links.count()):
                if links.nth(i).is_visible() and links.nth(i).text_content(timeout=800).strip() == "New Object":
                    links.nth(i).click(); break
            ajax(page)
            print("\nINSERT objectForm fields (id | mandatory | label):")
            for f in dump_inputs(page, "objectForm:form"):
                print(f"   {f['id']:55s} mand={f['mandatory']!s:5s} {f['label'][:22]}")
        except Exception as e:
            print("  insert-form scan err:", str(e)[:70])
    else:
        # TV: existing row 0 = column pattern + sample values (these are FILLED -> white, correctly not mandatory)
        print("\nTV existing row 0 (column pattern + sample values; filled = white, expected):")
        for f in dump_inputs(page, ":form:T:0:C"):
            print(f"   {f['id']:45s} val={f['val']}")
        # to read MANDATORY: click Insert '+' -> a fresh BLANK row (yellow = mandatory & empty)
        cell_prefix = (grid or "table:form:T_data").replace("_data", "")  # 'table:form:T'
        try:
            page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
            page.wait_for_timeout(900)
            links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
            for i in range(links.count()):
                if links.nth(i).is_visible() and (links.nth(i).text_content(timeout=800) or "").strip():
                    links.nth(i).click(); break
            ajax(page)
        except Exception as e:
            print("  TV insert err:", str(e)[:70])
        blank = page.evaluate("""(args) => { const [pfx,Y]=args; const rows={};
            document.querySelectorAll("[id^='"+pfx+":'][id$='_in']").forEach(e=>{
              const m=e.id.match(/T:(\\d+):C(\\d+)/); if(!m) return;
              (rows[+m[1]] ||= []).push({id:e.id, col:+m[2], val:e.value, mandatory:getComputedStyle(e).backgroundColor===Y}); });
            for(const r of Object.keys(rows)){ if(rows[r].every(c=>c.val==='')) return rows[r]; } return null; }""",
            [cell_prefix, YELLOW])
        print("\nTV blank Insert row (yellow = mandatory & empty):")
        if blank:
            for c in blank:
                print(f"   {c['id']:45s} mand={c['mandatory']!s:5s}")
        else:
            print("   (no blank insert row captured)")
    b.close()
print("\nDONE (read-only scan; nothing saved). Fills spec sec.2/sec.3.")
