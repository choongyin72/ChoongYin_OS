import re, json
from pathlib import Path
RB = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
for s in ["orifice_plate","meter_run","data_extract_setup","data_extract_set"]:
    drv = (RB/"py"/f"{s}_iud.py").read_text(encoding="utf-8")
    labels = re.findall(r'"label":\s*"([^"]+)",\s*"value":\s*"[^"]*",\s*"kind":\s*"([^"]+)"', drv)
    # exclude the Code/Name/Date core (heuristic: keep ones after core)
    print(s, "->", [f"{l} ({k})" for l,k in labels])
