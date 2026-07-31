import json, re, subprocess
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS"); EC = R / "workstreams/master-plan/ec-automation"
def a(s): return str(s).encode("ascii", "replace").decode("ascii")
SCR = {"Truck":"truck","Trailer":"trailer","Driver":"driver","Contract Area Setup":"contract_area_setup",
       "Create Calculation":"create_calculation","Cargo Planning Forecast":"cargo_planning_forecast"}
fams = json.loads((EC/"docs/screen_families.json").read_text(encoding="utf-8"))
br = subprocess.run(["git","branch","-a"], cwd=str(R), capture_output=True, text=True).stdout
for scr, slug in SCR.items():
    grids, navs = set(), set()
    for pat in ("py/%s_iud.py" % slug, "pageobjects/**/%s_page.resource" % slug):
        for f in EC.glob(pat):
            t = f.read_text(encoding="utf-8", errors="replace")
            grids |= set(re.findall(r'([A-Za-z_0-9]+(?::form)?[A-Za-z_0-9:]*:T_data)', t))
            for kw in ("apply_ovgm_navigator", "click_go", "Refresh", "nav:form:G"):
                if kw in t: navs.add(kw)
    has_branch = ("ov-gm-%s" % slug.replace("_","-")) in br
    print(a("%-24s fam=%-8s grid=%s nav=%s ov-gm-branch-exists=%s"
            % (scr, fams.get(scr), sorted(grids) or "?", sorted(navs), has_branch)))
