#!/usr/bin/env python3
"""Park Message Group (CO.0236) per owner decision, and remove the failing generated bundle so no
non-passing suite is left in the repo (verify_screen never reached PASS, so the packager never ran -
there are no registry/scorecard/manifest rows to unwind; asserted below)."""
import json
import shutil
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
EC = R / "workstreams" / "master-plan" / "ec-automation"

PARK = '''
## Message Group (CO.0236) - PARKED 2026-07-31 (owner decision; verified, not assumed)
- **Family: genuinely OV-GM** (proven live, not inherited): navigator = Date + ONE mandatory dropdown
  `Functional Area` at `nav:form:G:0:R:1:C:1:dd` + GO `button:form:B`; grid `manageObject:form:T_data`;
  treeview Configuration > Messaging > Message Group. Mandatory insert fields: Message Group Code,
  Start Date, Name, Functional Area (dd). End Date optional.
- **Blocker: the insert PERSISTS but lands in the WRONG SCOPE, so the grid cannot list it.**
  `db.code_present('OV_MESSAGE_GROUP', 'AUTOTEST_MG001')` = True after Save, yet
  `wait_for_row` never sees it.
- **NOT the documented groupmodel-off case** (my first read, corrected): the persisted row's
  `FUNCTIONAL_AREA_CODE` is **ALLOCATION** while the navigator's captured scope is **Administration**.
- **Read-only probe (tmp/probe_mg_fa_options.py, nothing saved):** the navigator panel and the objectForm
  panel offer IDENTICAL option lists - `['Administration', 'Allocation', 'Billing', ...]` - with
  `Administration` FIRST and `Allocation` SECOND. So the requested value is option 1 and the persisted
  value is option 2.
- **Two candidate causes, NOT yet distinguished (no evidence either way - do not treat as decided):**
  1. the dropdown pick lands one row off in this panel shape; or
  2. the dropdown write silently fails and EC saves a default of `Allocation`. (`insert_ui` PASSing only
     means EC raised no error - it is not proof the dropdown took.)
- **Why it stopped here:** 2 fix attempts used (bind the form dd to the captured nav value via the new
  `parent_dd` key; then re-run) - both landed in ALLOCATION. The suspect code
  (`select_dropdown` / `Fill OV Dropdown By Label`) is in the SHARED engine used by all 22 OV-GM screens,
  so changing it needs the shared-file protocol (backup + canary + random sibling), not a fix inside a
  screen build. **POSSIBLE WIDER IMPACT: if cause (1) is real, other OV-GM screens may have been writing
  a NEIGHBOURING dropdown value all along - their assertions only check CODE and NAME, never the parent
  dropdown.** Owner deferred this investigation; recorded so it is not lost.
- **Sandbox left clean:** 3 rows my runs persisted (AUTOTEST_MG001 x2, AUTOTEST_MG20260731221346) closed
  via End Date = Start Date through `OV_MESSAGE_GROUP` (full row logged first, 1 row per statement);
  re-read shows **0 open AUTOTEST rows**.
- **Bundle removed** (driver/T3/suite/screens dir): verify_screen FAILed, so the packager never ran and
  no registry/scorecard/screen_families row exists. Kept: tmp/cfg_message_group.json,
  tmp/recon_mg_nav.py, tmp/probe_mg_fa_options.py, tmp/selfclean_message_group.py so a resume is cheap.
'''

p = R / "tmp" / "OV_SWEEP_PARKED.md"
t = p.read_text(encoding="utf-8")
assert "Message Group (CO.0236)" not in t, "already parked"
p.write_text(t.rstrip("\n") + "\n" + PARK, encoding="utf-8")
print("parked in tmp/OV_SWEEP_PARKED.md")

# ---- prove nothing was published, then remove the failing bundle --------------------------------
man = json.loads((EC / "docs" / "screen_families.json").read_text(encoding="utf-8"))
assert "Message Group" not in man, "manifest row exists - packager DID run; unwind before deleting"
for doc in (EC / "docs" / "ec_screen_registry.md", R / "docs" / "automation-scorecard.md"):
    assert "message_group" not in doc.read_text(encoding="utf-8", errors="replace"), \
        "%s references message_group - unwind first" % doc.name
print("verified: no registry / scorecard / manifest row for Message Group")

removed = []
for tgt in (EC / "py" / "message_group_iud.py",
            EC / "pageobjects" / "Configuration" / "Messaging" / "message_group_page.resource",
            EC / "tests" / "Configuration" / "Messaging" / "message_group_iud.robot",
            EC / "screens" / "Configuration" / "Messaging" / "Message_Group"):
    if tgt.is_dir():
        shutil.rmtree(tgt); removed.append(str(tgt.relative_to(R)))
    elif tgt.is_file():
        tgt.unlink(); removed.append(str(tgt.relative_to(R)))
# drop the now-empty Messaging dirs
for d in (EC / "pageobjects" / "Configuration" / "Messaging", EC / "tests" / "Configuration" / "Messaging",
          EC / "screens" / "Configuration" / "Messaging"):
    if d.is_dir() and not any(d.iterdir()):
        d.rmdir(); removed.append(str(d.relative_to(R)) + " (empty dir)")
for r in removed:
    print("  removed:", r)

# ---- flag the wider risk where the next OV-GM build will see it ---------------------------------
cap = EC / "docs" / "ov-gm-navigator-capability.md"
c = cap.read_text(encoding="utf-8")
note = ('\n> OPEN RISK (2026-07-31, Message Group CO.0236): a parent-dd set to the captured navigator value\n'
        '> PERSISTED AS THE NEXT OPTION IN THE LIST (requested `Administration`, saved `Allocation`; both\n'
        '> panels offer identical lists). Cause not yet established - either the pick lands one row off, or\n'
        '> the write silently fails and EC defaults. Until this is settled, an OV-GM screen whose parent-dd\n'
        '> value MATTERS must have that value ASSERTED IN THE DB, not assumed from a green insert. Existing\n'
        '> suites assert only CODE and NAME. See tmp/OV_SWEEP_PARKED.md (Message Group).\n')
if "OPEN RISK (2026-07-31, Message Group" not in c:
    cap.write_text(c.rstrip("\n") + "\n" + note, encoding="utf-8")
    print("open risk noted in docs/ov-gm-navigator-capability.md")
