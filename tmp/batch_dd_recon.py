"""READ-ONLY: for each parked mandatory-dropdown OV screen, open the New-Object form and capture
a VALID option (first data-item-label) for each mandatory dropdown + confirm the plain fields.
One login; reload between screens. Emits JSON config-ready rows to tmp/batch_dd_results.json."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec

# (screen, bf, view, folder, short_prefix)  -- prefixes <=12 chars (CODE VARCHAR2 ~30-32 + 14-ts)
SCREENS = [
    ("HCB System", "CD.0097", "OV_BALANCE", "Configuration/Assets/Inventory_Objects", "AUTOTEST_HCB_"),
    ("Chemical Product", "CO.0072", "OV_CHEM_PRODUCT", "Configuration/Assets/Chemical_Objects", "AUTOTEST_CP_"),
    ("Orifice Plate", "CO.0089", "OV_ORIFICE_PLATE", "Configuration/Assets/Metering_Objects", "AUTOTEST_OP_"),
    ("Process Train", "CO.0120", "OV_PROCESS_TRAIN", "Configuration/Assets/Facility_Objects", "AUTOTEST_PT_"),
    ("Config Variable", "IN.0031", "OV_CONFIG_VARIABLE", "Configuration/Assets/Calculation_Objects", "AUTOTEST_CV_"),
    ("Data Extract Setup", "SP.0043", "OV_SUMMARY_SETUP", "Configuration/Assets/Reporting_Objects", "AUTOTEST_DXS_"),
    ("Data Extract Set", "SP.0049", "OV_SUMMARY_SET", "Configuration/Assets/Reporting_Objects", "AUTOTEST_DXT_"),
    ("Storage Flow", "CO.2091", "OV_STORAGE_FLOW", "Configuration/Assets/Tank_and_Storage_Objects", "AUTOTEST_SF_"),
    ("UOP Key", "CD.0099", "OV_FIN_UOP_DEPR_KEY", "Configuration/Assets/Financial_Objects", "AUTOTEST_UOP_"),
    ("EC Code Object", "CD.0135", "OV_EC_CODE_OBJECT", "Configuration/Assets/Basic_Objects", "AUTOTEST_ECO_"),
    ("Meter Run", "CO.0091", "OV_METER_RUN", "Configuration/Assets/Metering_Objects", "AUTOTEST_MR_"),
    ("Reservoir Block Formation", "CO.0137", "OV_RESV_BLOCK_FORMATION", "Configuration/Assets/Well_and_Reservoir_Objects", "AUTOTEST_RBF_"),
    ("Calculation Group Context", "CO.0245", "OV_CALC_GRP_CONTEXT", "Configuration/Assets/Calculation_Objects", "AUTOTEST_CGC_"),
]
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
RESULT = Path(r"C:\Projects\ChoongYin_OS\tmp\batch_dd_results.json")
out = []
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    pg.on("dialog", lambda d: d.accept())
    ec.login(pg, URL, "sysadmin", "sysadmin")
    for name, bf, view, folder, prefix in SCREENS:
        r = {"screen": name, "bfcode": bf, "view": view, "folder": folder, "code_prefix": prefix}
        try:
            pg.goto(URL, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(700)
            ec.open_object_screen(pg, name); ec.click_go(pg)
            ec._open_new_object(pg); pg.wait_for_timeout(500)
            fields = pg.evaluate("""()=>{const base='tab:tabPanel:objectForm:form:G:0:R:';const out=[];
              for(let i=0;i<26;i++){const inn=document.getElementById(base+i+':C:1:in');
                const dai=document.getElementById(base+i+':C:1:da_input');const ddi=document.getElementById(base+i+':C:1:dd_input');
                let el=null,kind='';if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(ddi){el=ddi;kind='dropdown';}
                if(!el)continue;const lc=document.getElementById(base+i+':C:0')||document.querySelector('[id^="'+base+i+':C:0"]');
                const label=lc?(lc.innerText||'').trim():'';
                const yellow=getComputedStyle(el).backgroundColor.includes('252, 249, 192');
                out.push({r:i,label:label,kind,mandatory:yellow,id:el.id});}return out;}""")
            texts = [f for f in fields if f["kind"] in ("text", "date")]
            # code = first mandatory text; name = second; date = first date
            code_l = next((f["label"] for f in fields if f["kind"] == "text" and f["mandatory"]), "Code")
            name_l = next((f["label"] for f in fields if f["kind"] == "text" and f["mandatory"] and f["label"] != code_l), "Name")
            date_l = next((f["label"] for f in fields if f["kind"] == "date" and f["mandatory"]), "Start Date")
            r["code_label"], r["name_label"], r["date_label"], r["end_label"] = code_l, name_l, date_l, "End Date"
            dds = []
            for f in fields:
                if f["kind"] == "dropdown" and f["mandatory"]:
                    prefix_id = f["id"][:-6]
                    try:
                        pg.locator("css=[id=\"%s_button\"]" % prefix_id).first.click(); pg.wait_for_timeout(900)
                        opts = pg.evaluate("""(pfx)=>{const pan=document.getElementById(pfx+'_panel');if(!pan)return[];
                          return Array.from(pan.querySelectorAll('tr[data-item-label]')).map(t=>t.getAttribute('data-item-label').trim()).filter(x=>x);}""", prefix_id)
                        pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
                        dds.append({"label": f["label"], "value": opts[0] if opts else None, "n_opts": len(opts), "sample": opts[:4]})
                    except Exception as e:
                        dds.append({"label": f["label"], "value": None, "err": repr(e)[:80]})
            r["dropdowns"] = dds
            r["all_mandatory_text"] = [f["label"] for f in fields if f["kind"] in ("text", "date") and f["mandatory"]]
        except Exception as e:
            r["error"] = repr(e)[:140]
        out.append(r); RESULT.write_text(json.dumps(out, indent=1), encoding="utf-8")
        dd_s = "; ".join("%s=%r(%d)" % (d["label"], d.get("value"), d.get("n_opts", 0)) for d in r.get("dropdowns", []))
        print("%-28s %-8s dds: %s | err=%s" % (name[:28], bf, dd_s, r.get("error", "")), flush=True)
    br.close()
print("\nwrote", RESULT)
