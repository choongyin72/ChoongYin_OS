#!/usr/bin/env python3
"""Owner-directed sweep: fix the wrong-family text in the 6 already-merged non-OV-GM bundles.

Fixed IN PLACE rather than by re-running the packager, deliberately:
  - those JOURNALs contain real hand-written history (Truck's records the #278 story); regenerating
    would DESTROY it.
  - none of the 6 has a saved config.json, so a regeneration would need me to reconstruct configs -
    i.e. guess.
So only statements that are demonstrably FALSE are rewritten, from ground truth read out of the shipped
artifacts:
  - real grid ids come from each driver's GRID_DATA_ID (truck_object:form:T_data etc.) - every KB claimed
    `manageObject:form:T_data`, which NONE of them uses.
  - "Op Production Unit (first-available)" appears in 0 of the 6 drivers -> the claim is false everywhere.
  - families come from docs/screen_families.json.
NOT touched (historical fact, not a false claim): branch names, and Trailer JOURNAL:14, which QUOTES the
old OV-GM wording while describing the #278 defect - that quote is the point of the sentence.
"""
import json
import re
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
EC = R / "workstreams" / "master-plan" / "ec-automation"

GRID = {"Truck": "truck_object:form:T_data", "Trailer": "trailer_object:form:T_data",
        "Driver": "driver_object:form:T_data", "Contract Area Setup": "nav:form:T_data",
        "Create Calculation": "calculation:form:T_data",
        "Cargo Planning Forecast": "fcst:form:T_data"}
SLUG = {k: k.lower().replace(" ", "_") for k in GRID}

KB_TYPE = {
    "plain": "Plain OV (EC Object Configuration, date-effective) - Bank family; date-only navigator + GO.",
    "custom": "Custom-URL OV (EC Object Configuration, date-effective) - grid loads directly; toolbar Refresh.",
    "tv": "TV-style table class - inline grid edits; per-screen delete gesture.",
    "gatedpf": "Gated OV with PER-FIELD navigator groups (date-effective) + GO.",
}
KB_NAV = {
    "plain": "date field `nav:form:G:0:R:1:C:0:da_input` -> GO `#button:form:B` (no cascade)",
    "custom": "none - grid loads from the screen URL; re-query via toolbar Refresh `[Ctrl+r]`",
    "tv": "per-screen context/date navigator (see SOW)",
    "gatedpf": "PER-FIELD nav groups `nav:form:G:<n>:R:1:C:0` (Production Unit / Area / Facility Class 1 / Storage) -> GO `#button:form:B`",
}
GRID_NOTE = {"plain": " (lists after GO)", "custom": " (lists on open)", "tv": "",
             "gatedpf": " (empty until all nav fields + GO)"}
ENGINE = {"plain": " + `click_go`", "custom": " + toolbar Refresh", "tv": "",
          "gatedpf": " + per-field nav helpers"}
QUIRKS = {
    "plain": "- Plain OV (Bank family): the navigator is a single DATE field + GO - no cascade, and no Op\n"
             "  Production Unit to satisfy.\n"
             "- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES\n"
             "  (that commits the intended delete).",
    "custom": "- Custom-URL OV: no navigator GO; the toolbar Refresh `[Ctrl+r]` is the re-query gesture.",
    "tv": "- TV-style: rows are edited in place; the delete gesture is per screen (see SOW).",
    "gatedpf": "- Every navigator group is a SEPARATE mandatory field (not one cascade widget); fill them all\n"
               "  before GO or the grid stays empty.",
}
SPEC = {
    "plain": "Plain-OV specifics: date-only navigator + GO (no cascade); no Op PU gating.",
    "custom": "Custom-URL specifics: grid loads directly from the screen URL; toolbar Refresh re-queries "
              "(no navigator GO).",
    "tv": "TV-style specifics: inline grid cell edits; per-screen delete gesture (see SOW).",
    "gatedpf": "Gated per-field specifics: nav groups are PER FIELD (nav:form:G:<n>:R:1:C:0) + GO.",
}
LABEL = {"plain": "plain OV", "custom": "custom-URL OV", "tv": "TV-style", "gatedpf": "gated OV (per-field nav)"}
LESSON = {
    "plain": "- Plain OV: date-only navigator + GO; no cascade and no Op PU, so the grid lists straight after\n"
             "  Save + GO.",
    "custom": "- Custom-URL OV: no navigator GO; the toolbar Refresh is the re-query gesture.",
    "tv": "- TV-style: the row is edited in place; confirm the delete gesture per screen.",
    "gatedpf": "- Gated per-field nav: every nav group is its own mandatory field; fill them all before GO.",
}
NOTE = ("\n_Family text corrected %s: this bundle shipped with OV-GM wording (grid `manageObject:form:T_data`,\n"
        "cascade + GO, Op Production Unit) that does not describe this screen - the packager templates were\n"
        "OV-GM-only until then. Code and gate results are unchanged; only the prose was wrong._\n")
DATE = "2026-07-31"

fams = json.loads((EC / "docs" / "screen_families.json").read_text(encoding="utf-8"))
total = 0

for scr, grid in GRID.items():
    fam = fams[scr]
    assert fam in KB_TYPE, "unexpected family %r for %s" % (fam, scr)
    slug = SLUG[scr]
    n_scr = 0

    # ---------------------------------------------------------------- KB map
    kb = R / "ec-ui-knowledge" / "screens" / ("%s.md" % slug)
    if kb.is_file():
        t = kb.read_text(encoding="utf-8")
        o = t
        t = t.replace("- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object "
                      "groupmodel; navigator-GATED.", "- **Type:** " + KB_TYPE[fam])
        t = t.replace("| Grid | `manageObject:form:T_data` (empty until cascade + GO) |",
                      "| Grid | `%s`%s |" % (grid, GRID_NOTE[fam]))
        t = re.sub(r"\| Navigator \(gated\) \| cascade[^\n]*\|",
                   "| Navigator | %s |" % KB_NAV[fam], t)
        t = t.replace(" - Op Production Unit (first-available, grid visibility)", "")
        t = t.replace(" + `apply_ovgm_navigator`", ENGINE[fam])
        t = re.sub(r"- OV-GM navigator-gated: grid empty until cascade \+ GO\. First-available nav PU is a "
                   r"sparse test scope - it is\n\s*NOT necessarily a valid Op Production Unit option, and it "
                   r"empties nav-scoped popups \(see issue OV_SWEEP_PARKED\);\n\s*parent-dd \+ Op PU use "
                   r"first-available, probe per screen\.", QUIRKS[fam], t)
        if t != o:
            t = t.rstrip("\n") + "\n" + NOTE % DATE
            kb.write_text(t, encoding="utf-8")
            n_scr += 1

    # ---------------------------------------------------------------- bundle CHECKLIST + JOURNAL
    for d in EC.rglob(scr.replace(" ", "_")):
        if not d.is_dir():
            continue
        cl = d / "CHECKLIST.md"
        if cl.is_file():
            t = cl.read_text(encoding="utf-8")
            o = t
            # keep any real "+ dropdowns X" / "+ popups Y" note, drop the OV-GM claims around it
            def _footer(m):
                extras = ""
                for kind in ("dropdowns", "popups"):
                    mm = re.search(r"\+ %s ([^;_]+)" % kind, m.group(0))
                    if mm:
                        extras += " + %s %s" % (kind, mm.group(1).strip())
                return SPEC[fam] + extras + "_"
            t = re.sub(r"OV-GM specifics:[^\n]*_", _footer, t)
            if t != o:
                cl.write_text(t, encoding="utf-8")
                n_scr += 1
        jr = d / "JOURNAL.md"
        if jr.is_file():
            t = jr.read_text(encoding="utf-8")
            o = t
            t = t.replace("(%s) OV-GM IUD" % "", "")          # no-op guard
            t = re.sub(r"^# JOURNAL - (.*?) OV-GM IUD", lambda m: "# JOURNAL - %s %s IUD"
                       % (m.group(1), LABEL[fam]), t, count=1, flags=re.M)
            t = t.replace(" (stacked on the gated-navigator capability, PR #244)",
                          " (branch name is historical; the gated-navigator/PR #244 claim was WRONG - this "
                          "is a %s build)" % LABEL[fam])
            t = re.sub(r"scan\): OV-GM \(grid\n\s*`manageObject:form:T_data`\), navigator cascade \.",
                       "scan): %s (grid `%s`). Nav: %s." % (LABEL[fam], grid, KB_NAV[fam]), t)
            t = t.replace(" Op Production Unit set first-available for grid visibility.", "")
            t = re.sub(r"- OV-GM: first-available nav scope \+ Op PU first-available lists the row after GO "
                       r"\(parent-dd need not equal\n\s*the nav PU - probe per screen\)\.", LESSON[fam], t)
            if t != o:
                t = t.rstrip("\n") + "\n" + NOTE % DATE
                jr.write_text(t, encoding="utf-8")
                n_scr += 1
    print("%-24s [%-7s] %d file(s) corrected" % (scr, fam, n_scr))
    total += n_scr

print("\nTOTAL files corrected: %d" % total)
assert total >= 6, "expected at least one file per screen, got %d" % total
