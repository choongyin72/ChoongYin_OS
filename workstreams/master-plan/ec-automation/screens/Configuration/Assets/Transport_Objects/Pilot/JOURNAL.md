# JOURNAL - Pilot (CO.2079) OV-GM IUD

## 2026-07-31
- **Branch:** `feature/pilot-iud`. Group A #8. Standard OV-GM - the plainest screen of this batch.
- **Registry-first check mattered here:** an early substring-based audit had wrongly listed Pilot as
  "already documented (PASS)" (it was matching the *Pilot Boat* row). `grep -c "^| Pilot |"` = 0 and
  the exact-match audit proved it genuinely unbuilt. Same defect class as issue #278/#265: a loose
  match reporting a wrong-but-plausible answer.
- **Recon (executed):** 3-level cascade + GO, grid `manageObject:form:T_data`, mandatory
  Code/Name/Start Date only, Op Production Unit present. DB: OV_PILOT = 8 rows.
- Generated with `tmp/gen_ovgm.py`; **8/8 driver and all 5 gates PASS on the FIRST run.**
- **Validator improvement made here:** `tmp/check_row_vocab.py` reported "4 rows for Pilot" because
  its prefix match also caught "Pilot Boat". Tightened to EXACT first-cell equality; re-validated -
  Pilot 2 rows, Pilot Boat 2 rows, both clean. (Also proved the validator correctly reports
  "no row found" for a screen whose PR is not yet merged - e.g. Driver on this branch.)

## Lessons
- Prefix matching keeps producing wrong-but-plausible results (Pilot/Pilot Boat here; the phantom
  screen names earlier). Match identifiers EXACTLY - in audits and in tooling.
