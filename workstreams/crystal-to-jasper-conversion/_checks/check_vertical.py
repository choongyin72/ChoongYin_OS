import fitz
B = r"C:\Projects\INPEX\sources\CrystalReports\R07.003"
gen = fitz.open(B + r"\output\R07_003_Onshore_Daily_Operations_Report.pdf")
ref = fitz.open(B + r"\crytsal report in pdf\R07.003 - Onshore Daily Operations Report.pdf")

# unique anchor strings per page whose y we can compare
ANCHORS = {
  2: ["Comment Type", "HSE", "Process Safety/Facility Risk", "Daily Flaring", "Executive",
      "LNG1 \u2013 Online."],
  3: ["Production", "PRODUCTION OPTIMISATION:", "CONSTRAINTS", "Alarm Management",
      "AGI Status", "PWC Export", "Facility Priorities", "UTES/CCPP: Major Production Activities (Next 24 hours)"],
  4: ["Maintenance & Implementation", "06OT-LNG/S&L PLAN Y25LOT42", "IC/MA -",
      "06OT - UTES/CCPP/INLET PLAN Y25LOT42", "Coatings & Insulation", "CUI Program",
      "I228 Program", "Engineering", "LNG/S&L", "Notes", "Disclaimer"],
}

for pno, anchors in ANCHORS.items():
    print(f"===== PAGE {pno+1} vertical offsets =====")
    for a in anchors:
        ys = {}
        for tag, d in (("ref", ref), ("gen", gen)):
            hits = [s["bbox"][1] for b in d[pno].get_text("dict")["blocks"]
                    for l in b.get("lines", []) for s in l["spans"]
                    if s["text"].strip() == a]
            ys[tag] = round(min(hits), 2) if hits else None
        if ys["ref"] is None or ys["gen"] is None:
            print(f"    {a[:44]:46} (not found in {'ref' if ys['ref'] is None else 'gen'})")
            continue
        dy = ys["gen"] - ys["ref"]
        flag = "   <-- " if abs(dy) > 3 else ""
        print(f"    {a[:44]:46} ref={ys['ref']:8.2f} gen={ys['gen']:8.2f} dy={dy:+7.2f}{flag}")
    print()
