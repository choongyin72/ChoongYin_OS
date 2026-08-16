#!/usr/bin/env python3
"""ITEM 5 resolved by read-only probe (tmp/probe_dropdown_fidelity.py, nothing saved):
select_dropdown sets the field FAITHFULLY - asked for 'Administration' (both via __FIRST__ and by explicit
label), the input reads back 'Administration' before save. So the Administration -> ALLOCATION divergence
is introduced AT/AFTER SUBMIT, not by the pick. The shared engine is cleared, and with it the fear that 22
OV-GM screens might have been writing neighbouring parent-dd values.

Both docs are updated to state the PROVEN narrower finding instead of the wider suspicion."""
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")

cap = R / "workstreams/master-plan/ec-automation/docs/ov-gm-navigator-capability.md"
c = cap.read_text(encoding="utf-8")
i = c.index("> OPEN RISK (2026-07-31, Message Group")
new = ('''> RESOLVED 2026-07-31 (was logged here as an OPEN RISK - the wider fear is RETRACTED, with evidence).
> On Message Group (CO.0236) a parent-dd set to 'Administration' PERSISTED as 'Allocation'. A read-only
> probe (tmp/probe_dropdown_fidelity.py - nothing saved) set the field via `select_dropdown` both with
> `__FIRST__` and with the explicit label and READ THE INPUT BACK: it holds 'Administration' in both
> cases. **So the pick is faithful and the shared engine is NOT defective** - the divergence is introduced
> at/after SUBMIT (EC-side derivation/override of FUNCTIONAL_AREA, mechanism not yet established).
> Consequence: the other OV-GM screens' parent-dd handling is NOT implicated by this evidence. Still worth
> doing when convenient: assert the parent-dd value in the DB, not just CODE/NAME, so an EC-side override
> can never pass silently. Message Group stays parked - see tmp/OV_SWEEP_PARKED.md.
''')
c = c[:i] + new
cap.write_text(c, encoding="utf-8")
print("ov-gm-navigator-capability.md: open risk resolved + retracted")

park = R / "tmp" / "OV_SWEEP_PARKED.md"
t = park.read_text(encoding="utf-8")
old = "- **Two candidate causes, NOT yet distinguished (no evidence either way - do not treat as decided):**"
assert old in t, "message group candidate-cause bullet not found"
i = t.index(old)
j = t.index("- **Why it stopped here:**", i)
t = t[:i] + ('''- **CAUSE NOW DISTINGUISHED 2026-07-31 (read-only probe, nothing saved):** `select_dropdown` is
  FAITHFUL - the form field reads back `Administration` both via `__FIRST__` and by explicit label before
  any save. So the divergence is introduced **at/after SUBMIT**, not by the pick. The earlier worry that
  the shared engine might be mis-picking on all 22 OV-GM screens is **RETRACTED** - evidence
  tmp/probe_dropdown_fidelity.py.
- **Still unknown (do not treat as decided):** the mechanism by which EC ends up writing
  FUNCTIONAL_AREA_CODE='ALLOCATION' - candidates are an EC-side derivation/default overriding the
  submitted value, or the persisted column not being the one this form field feeds. Needs a save-time
  trace (EC log / IUD trigger read), which is why the screen stays parked.
''') + t[j:]
park.write_text(t, encoding="utf-8")
print("park entry: cause distinguished, wider claim retracted")
