"""GENERIC mandatory-field scanner for an OV New-Object form (the helper the owner asked for).

Given a screen, opens the New-Object form and returns the COMPLETE mandatory set (every yellow input,
any kind), with a valid value for each:
  - text with 'Code' in label   -> <prefix>001         (the object code)
  - text with 'Name' in label    -> AUTOTEST <screen> 001
  - date (Start Date)            -> 2000-01-01
  - dropdown                     -> first real option from its panel
  - any OTHER mandatory text/num -> '1' (non-empty, numeric-safe default)
Emits a build-ready config JSON to tmp/<slug>/config.json (feeds gen_ov_screen.py / build_screen.py).
NEVER saves. Usage: py tmp/scan_mandatory.py '<json: screen,bfcode,view,folder,slug,code_prefix>'
"""
import json, sys, re
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec

a = json.loads(sys.argv[1])
screen, bf, view, folder, slug, prefix = a["screen"], a["bfcode"], a["view"], a["folder"], a["slug"], a["code_prefix"]
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"

SCAN_JS = r"""()=>{
  const root=document.querySelector('[id*=":objectForm:form:"]')||document;
  const out=[];
  root.querySelectorAll('input,select,textarea').forEach(e=>{
    if(e.type==='hidden'||e.offsetParent===null) return;
    const id=e.id||''; if(!id.includes(':objectForm:form:')) return;
    let kind='text'; if(id.endsWith('da_input'))kind='date'; else if(id.endsWith('dd_input'))kind='dropdown';
    else if(id.endsWith('dd_hinput'))return;               // dropdown hidden twin - skip
    const yellow=getComputedStyle(e).backgroundColor.includes('252, 249, 192');
    let lbl=''; const row=e.closest('.tableRow')||e.closest('tr');
    if(row){const s=row.querySelector('span[class*=ECCell]'); if(s)lbl=(s.innerText||'').trim();}
    out.push({id,kind,mandatory:yellow,label:lbl});
  });
  return out;}"""

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, screen); ec.click_go(pg); ec._open_new_object(pg); pg.wait_for_timeout(600)
    shot = Path(r"C:\Projects\ChoongYin_OS\tmp") / slug / "newobject_form.png"
    shot.parent.mkdir(parents=True, exist_ok=True)
    try:
        pg.screenshot(path=str(shot)); print("screenshot ->", shot)
    except Exception:
        pass
    fields = pg.evaluate(SCAN_JS)
    mand = [f for f in fields if f["mandatory"]]
    print("=== %s: FULL field inventory (%d fields; %d mandatory) ===" % (screen, len(fields), len(mand)))
    for f in fields:
        print("  %s %-9s %-30s %s" % ("[M]" if f["mandatory"] else "[ ]", f["kind"], f["label"], f["id"]))

    # NAME is often NON-mandatory (not yellow) yet is the UPDATE target - so search ALL text fields,
    # not just the mandatory ones (lesson: EC Code Object has a non-mandatory Name we first mis-missed).
    all_text = [f for f in fields if f["kind"] == "text"]
    code_l = next((f["label"] for f in mand if f["kind"] == "text" and "code" in f["label"].lower()), None)
    name_l = next((f["label"] for f in all_text if "name" in f["label"].lower()), None)
    date_l = next((f["label"] for f in mand if f["kind"] == "date"), "Start Date")
    texts = [f for f in mand if f["kind"] == "text"]
    if not code_l and texts: code_l = texts[0]["label"]
    if not name_l:
        name_l = next((t["label"] for t in all_text if t["label"] != code_l), None)
    # extra mandatory text/num = mandatory text fields that are neither code nor name
    extras = [f["label"] for f in mand if f["kind"] == "text" and f["label"] not in (code_l, name_l)]
    # dropdown options (first real value)
    dds = []
    for f in mand:
        if f["kind"] == "dropdown":
            pfx = f["id"][:-6]
            try:
                pg.locator("css=[id=\"%s_button\"]" % pfx).first.click(); pg.wait_for_timeout(900)
                opts = pg.evaluate("""(p)=>{const pan=document.getElementById(p+'_panel');if(!pan)return[];
                  return Array.from(pan.querySelectorAll('tr[data-item-label]')).map(t=>t.getAttribute('data-item-label').trim()).filter(x=>x);}""", pfx)
                pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
                dds.append({"label": f["label"], "value": opts[0] if opts else None, "n_opts": len(opts)})
            except Exception as e:
                dds.append({"label": f["label"], "value": None, "err": repr(e)[:60]})
    br.close()

cfg = {
    "screen": screen, "bfcode": bf, "view": view, "folder": folder, "slug": slug,
    "code_prefix": prefix, "code_label": code_l, "name_label": name_l,
    "date_label": date_l, "end_label": "End Date",
    "name_val": "AUTOTEST %s 001" % screen,
    "dropdowns": [{"label": d["label"], "value": "__FIRST__"} for d in dds],  # first-available = cascade-safe
    "extra_fields": [{"label": e, "value": "1"} for e in extras],
}
blockers = [d["label"] for d in dds if not d["value"]]
cfg["_scan"] = {"mandatory_count": len(mand), "dropdowns_raw": dds, "extras": extras, "dropdown_blockers": blockers,
                "all_fields": [{"id": f["id"], "label": f["label"], "kind": f["kind"], "mandatory": f["mandatory"]} for f in fields]}
outp = Path(r"C:\Projects\ChoongYin_OS\tmp") / slug / "config.json"
outp.parent.mkdir(parents=True, exist_ok=True)
outp.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
print("\ncode=%r name=%r date=%r" % (code_l, name_l, date_l))
print("dropdowns:", cfg["dropdowns"])
print("extra mandatory:", cfg["extra_fields"])
print("BLOCKERS (dropdown with 0 options -> PARK):", blockers if blockers else "none")
print("VERDICT:", "PARK" if blockers else "BUILD")
print("wrote", outp)
