"""#237 item 3: replace plain-OV boilerplate in merged screens' docs with the REAL mandatory extras."""
from pathlib import Path
RB = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
KB = Path(r"C:\Projects\ChoongYin_OS\ec-ui-knowledge\screens")
# screen slug -> (bundle folder, accurate mandatory-extras phrase)
EXTRAS = {
 "orifice_plate": ("Stream_Objects/Orifice_Plate",
   "mandatory extras beyond Code/Name/Start Date: Material (dropdown), Diameter [mm], Measurement Temp [deg R]"),
 "meter_run": ("Stream_Objects/Meter_Run",
   "mandatory extras beyond Code/Name/Start Date: Type of Taps, Pipe Material, Location of Taps (dropdowns), "
   "Pipe Diameter [mm], Diameter Meas Temp [deg R], All Calibration Factor"),
 "data_extract_setup": ("Data_Mapping_Objects/Data_Extract_Setup",
   "mandatory extra beyond Code/Name/Start Date: Data Extract Type (dropdown)"),
 "data_extract_set": ("Data_Mapping_Objects/Data_Extract_Set",
   "mandatory extra beyond Code/Name/Start Date: Owner Class (dropdown)"),
}
PHRASES = [
 "plain Bank-layout OV, no mandatory dropdowns",
 "plain (no mandatory dropdowns)",
 "optional dropdowns only, none mandatory",
 "no mandatory dropdowns",
 "plain; no mandatory dropdowns",
]
total = 0
for slug, (folder, phrase) in EXTRAS.items():
    files = list((RB/"screens"/"Configuration"/"Assets"/folder).glob("*.md"))
    kb = KB/f"{slug}.md"
    if kb.exists(): files.append(kb)
    for f in files:
        t = f.read_text(encoding="utf-8"); orig = t
        for p in PHRASES:
            t = t.replace(p, phrase)
        if t != orig:
            f.write_text(t, encoding="utf-8", newline="\n")
            print(f"  fixed {f.relative_to(Path(r'C:/Projects/ChoongYin_OS'))}")
            total += 1
print(f"retrofitted {total} doc file(s)")
