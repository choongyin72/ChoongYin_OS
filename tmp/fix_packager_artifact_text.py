#!/usr/bin/env python3
"""Found while auditing Report Group's OWN generated bundle (2026-07-31). Three defects, all of a class
I had claimed was fixed:

 1. FABRICATED TICK: CHECKLIST item 19 shipped as "[x] 19 PR (R9 body)" - written at package time, when
    no PR can possibly exist yet. Exactly the #235 repeat-offence pattern (a tick no command earned).
 2. FABRICATED TICK: "0b grep ec-automation -> only this build" was pre-ticked; no grep had run.
 3. WRONG-FAMILY VOCABULARY, still alive in files my validator never looked at: the CHECKLIST footer, the
    whole JOURNAL template (title "OV-GM IUD", branch "feature/ov-gm-*", "stacked on ... PR #244",
    "manageObject:form:T_data", "navigator cascade", "Op Production Unit first-available") and the KB
    map's Type line all hardcode OV-GM - on a PLAIN-OV screen. check_row_vocab.py only ever validated the
    registry + scorecard ROWS, so #265/#278/#283's defect class survived in the bundle documents.

Fixes: family-aware text everywhere, item 19 written UNTICKED, and 0b ticked from a REAL grep.
"""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\package_ovgm.py")
src = p.read_text(encoding="utf-8")

# ---------------------------------------------------------------- 1. family text + a REAL 0b grep
anchor = '# ---- #7 CHECKLIST.md (ticks from the real VERIFY-REPORT) -------------------------'
assert src.count(anchor) == 1
prelude = '''# ---- family-aware artifact text + a REAL check-existing grep ---------------------
# (the CHECKLIST/JOURNAL/KB templates used to hardcode OV-GM wording on every screen)
FAM_LABEL = {"ovgm": "OV-GM", "plain": "plain OV", "custom": "custom-URL OV", "tv": "TV-style",
             "gatedpf": "gated OV (per-field nav)"}
FAM_SPEC = {
    "ovgm": "OV-GM specifics: navigator cascade %s first-available + GO; Op Production Unit "
            "first-available for grid visibility." % (" -> ".join(nav) if nav else ""),
    "plain": "Plain-OV specifics: date-only navigator + GO (no cascade); no Op PU gating.",
    "custom": "Custom-URL specifics: grid loads directly from the screen URL; toolbar Refresh re-queries "
              "(no navigator GO).",
    "tv": "TV-style specifics: inline grid cell edits; per-screen delete gesture (see SOW).",
    "gatedpf": "Gated per-field specifics: nav groups are PER FIELD (nav:form:G:<n>:R:1:C:0) + GO.",
}
FAM_GRID_TXT = {"ovgm": "OV-GM (grid `manageObject:form:T_data`)",
                "plain": "plain OV (Bank family, grid `%s`)" % grid_txt,
                "custom": "custom-URL OV (grid `%s`)" % grid_txt,
                "tv": "TV-style inline grid (`%s`)" % grid_txt,
                "gatedpf": "gated OV, per-field nav groups (grid `%s`)" % grid_txt}
FAM_KB_TYPE = {
    "ovgm": "OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.",
    "plain": "Plain OV (EC Object Configuration, date-effective) - Bank family; date-only navigator + GO.",
    "custom": "Custom-URL OV (EC Object Configuration, date-effective) - grid loads directly; toolbar Refresh.",
    "tv": "TV-style table class - inline grid edits; per-screen delete gesture.",
    "gatedpf": "Gated OV with PER-FIELD navigator groups (date-effective) + GO.",
}
FAM_LESSON = {
    "ovgm": "- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd "
            "need not equal the nav PU - probe per screen).",
    "plain": "- Plain OV: date-only navigator + GO; no cascade and no Op PU to satisfy, so the grid lists "
             "immediately after Save + GO.",
    "custom": "- Custom-URL OV: no navigator GO; the toolbar Refresh is the re-query gesture.",
    "tv": "- TV-style: the row is edited in place; confirm the delete gesture per screen.",
    "gatedpf": "- Gated per-field nav: each nav group is its own field; fill every mandatory one before GO.",
}
fam_label = FAM_LABEL[family]

# 0b is a CLAIM, so it must come from a real command: does anything OUTSIDE this build already
# implement this screen? (Pre-ticking this was defect #2 above.)
_own = {("%s_iud.py" % slug), ("%s_page.resource" % slug), ("%s_iud.robot" % slug), ("%s_sow.md" % slug),
        ("%s.md" % slug)}
_dupes = []
for _f in EC.rglob("*"):
    if not _f.is_file() or _f.suffix.lower() not in (".py", ".robot", ".resource"):
        continue
    if _f.name in _own or sfolder in _f.parts:
        continue
    try:
        if slug in _f.read_text(encoding="utf-8", errors="replace"):
            _dupes.append(_f.relative_to(EC).as_posix())
    except Exception:
        pass
_shared_ok = {"py/ec_object_iud.py"}          # the shared engine legitimately dispatches by slug
_dupes = [d for d in _dupes if d not in _shared_ok]
zerob = ("0b grep ec-automation -> only this build (checked: %d other file(s) reference %r)"
         % (len(_dupes), slug))
zerob_tick = "x" if not _dupes else " "
if _dupes:
    zerob += " -- REVIEW: %s" % ", ".join(_dupes[:4])

''' + anchor
src = src.replace(anchor, prelude)

# ---------------------------------------------------------------- 2. CHECKLIST fixes
old = ("- [x] 0a KB map created / 0b grep ec-automation -> only this build / 0c reused shared engine "
       "(ec_object_iud.py) + DbVerify + T2 (thin driver, no per-screen plumbing).")
assert src.count(old) == 1
src = src.replace(old, "- [x] 0a KB map created\n- [%(zerob_tick)s] %(zerob)s\n"
                       "- [x] 0c reused shared engine (ec_object_iud.py) + DbVerify + T2 (thin driver).")

old = "- [x] 17 Registry row - [x] 18 Scorecard row - [x] 19 PR (R9 body)"
assert src.count(old) == 1
src = src.replace(old, "- [x] 17 Registry row - [x] 18 Scorecard row\n"
                       "- [ ] 19 PR (R9 body) - CANNOT be ticked here: this file is written BEFORE the PR "
                       "exists. Tick it in the PR body/commit, never at scaffold time (#235).")

old = ("OV-GM specifics: navigator cascade %(nav)s first-available + GO%(dd_note)s%(pp_note)s; "
       "Op Production Unit first-available for grid visibility._")
assert src.count(old) == 1, "checklist footer not found"
src = src.replace(old, "%(fam_spec)s%(dd_note)s%(pp_note)s_")

old = ("""screen_abbr=a.get("abbr", slug[:3]), nav=" -> ".join(nav), dd_note=dd_note, pp_note=pp_note)""")
assert src.count(old) == 1
src = src.replace(old, """screen_abbr=a.get("abbr", slug[:3]), nav=" -> ".join(nav), dd_note=dd_note,
           pp_note=pp_note, fam_spec=FAM_SPEC[family], zerob=zerob, zerob_tick=zerob_tick)""")

# ---------------------------------------------------------------- 3. JOURNAL fixes
old = "journal = '''# JOURNAL - %(screen)s (%(bf)s) OV-GM IUD"
assert src.count(old) == 1
src = src.replace(old, "journal = '''# JOURNAL - %(screen)s (%(bf)s) %(fam_label)s IUD")

old = """- **Branch:** `feature/ov-gm-%(slug_dash)s` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify."""
assert src.count(old) == 1
src = src.replace(old, """- **Branch:** `%(branch)s`.
  Check-existing gate: %(zerob)s; reused shared engine (ec_object_iud.py) + T2 + DbVerify.""")

old = """- **Recon** (`investigation/recon.py`, read-only + tmp/%(slug)s/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade %(nav)s. Mandatory %(code_l)s / %(name_l)s / Start Date%(dd_note)s%(pp_note)s."""
assert src.count(old) == 1
src = src.replace(old, """- **Recon** (`investigation/recon.py`, read-only + tmp/%(slug)s/config.json scan): %(fam_grid)s.
  Nav: %(nav_txt)s. Mandatory %(code_l)s / %(name_l)s / Start Date%(dd_note)s%(pp_note)s.""")

old = """- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility."""
assert src.count(old) == 1
src = src.replace(old, """- **Built** (generator `%(gen)s`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.""")

old = """## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.
'''"""
assert src.count(old) == 1
src = src.replace(old, """## Lessons
%(fam_lesson)s Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
'''""")

old = """           nav=" -> ".join(nav), code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note,
           rf_txt=rf_txt, pw_txt=pw_txt)"""
assert src.count(old) == 1
src = src.replace(old, """           nav=" -> ".join(nav), code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note,
           rf_txt=rf_txt, pw_txt=pw_txt, fam_label=fam_label, fam_grid=FAM_GRID_TXT[family],
           nav_txt=nav_txt, fam_lesson=FAM_LESSON[family], branch=_branch(), zerob=zerob,
           gen="tmp/gen_ovgm.py" if family == "ovgm" else "tmp/gen_ov.py")""")

# ---------------------------------------------------------------- 4. KB Type line
old = "- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED."
assert src.count(old) == 1
src = src.replace(old, "- **Type:** %(fam_type)s")
# add fam_type to the kb_txt % dict (find its arg list)
import re as _re
m = _re.search(r"kb_txt = '''.*?''' % dict\((.*?)\)\n", src, _re.S)
assert m, "kb_txt dict not found"
src = src[:m.end(1)] + ", fam_type=FAM_KB_TYPE[family]" + src[m.end(1):]

# ---------------------------------------------------------------- 5. real branch name helper
helper = '''

def _branch():
    """The JOURNAL used to hardcode `feature/ov-gm-<slug>` + "PR #244". Report the REAL branch."""
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True)
        return r.stdout.strip() or "(unknown branch)"
    except Exception:
        return "(unknown branch)"

'''
anchor2 = "a = json.loads(sys.argv[1])"
assert src.count(anchor2) == 1
src = src.replace(anchor2, helper.strip("\n") + "\n\n" + anchor2)

p.write_text(src, encoding="utf-8")
print("package_ovgm.py patched: family-aware CHECKLIST/JOURNAL/KB, item 19 unticked, 0b from a real grep")
