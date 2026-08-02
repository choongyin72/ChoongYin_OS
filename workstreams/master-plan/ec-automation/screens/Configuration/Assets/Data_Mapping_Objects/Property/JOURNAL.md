# JOURNAL - Property (SP.0059) OV-GM IUD

## 2026-08-02
- **Branch:** `feature/retry-property-iud`. Previously parked (PR #313) as "silent Save failure + a
  real `ec_error()` detection gap" - the detection gap was fixed separately in #319/#326. Retried here.
- **Blocker chased down the wrong path first:** on retry, the Business Unit Name reference dropdown
  kept persisting the wrong value ("SS1 BU" instead of the requested "Royalty Canada"), reproduced
  live 4 times (raw DOM check, screenshots, video, and headed in front of the owner). Initially
  suspected/reported as a shared-engine defect in `select_dropdown()` (`py/ec_object_iud.py`) - the
  same symptom had also appeared on Price Index and Royalty Contract.
- **Real root cause (owner correction):** not a code defect at all. A Property record's Start Date
  was set to `2000-01-01`, but the target Business Unit "Royalty Canada" (`ROYALTY_CA`) only exists
  from `2003-01-01` onward (checked live: `OV_BUSINESS_UNIT.OBJECT_START_DATE`). EC's reference
  dropdowns only offer parent objects already effective by the child record's own Start Date - a
  child object cannot exist before its parent does. With `2000-01-01`, "Royalty Canada" wasn't even
  in the filtered option list (only SS1 BU/SS2 BU/TS5 BU were, matching what the panel actually
  showed); the code's fallback silently took the first option in that list instead of the requested
  one that wasn't there. Confirmed fix live + DB-verified with `AUTOTEST_PROP_FIXEDDATE` on
  Start Date `2003-01-01`: Business Unit persisted correctly as `ROYALTY_CA`. Cleaned (0 residual).
  Recorded as a standing lesson: [[feedback_child_object_date_must_follow_parent]].
- **Built** (generator `tmp/gen_ovgm.py`, config `nav_value="Royalty Canada"`,
  `extra_dropdowns=[["Business Unit Name","Royalty Canada"]]`, `start_date="2003-01-01"`): label-driven
  T3 (no hardcoded ids); thin driver `py/property_iud.py`; RF T3/suite.
- **Generator template gap found + fixed locally:** the generator's default single-level nav dropdown
  id template (`nav:form:G:0:R:1:C:1:dd`) does not match this screen's actual layout - Property's Date
  and Business Unit fields are TWO SEPARATE navigator groups (`G:0`=Date, `G:1`=Business Unit), not one
  group with Date at C:0/dropdown at C:1. Confirmed the real id live (`nav:form:G:1:R:1:C:0:dd_input`)
  and hand-corrected both `py/property_iud.py` and the T3's `${NAV_DD}` variable before running the
  live gate. Not pushed back into `tmp/gen_ovgm.py` itself this round - flagged here for whoever next
  hits a screen where Date and the mandatory dropdown are in different navigator groups.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright driver 8/8. DB residual 0.

## Lessons
- **Reference-dropdown screens need `Start Date >= the referenced object's own effective date`**, not
  just the plain default test date. This project already has `EC_TEST_START_DATE_REFDD` (2003-01-01)
  in `resources/environment.py` for exactly this; use it (or an equivalent >= 2003-01-01 date) whenever
  the New-Object form has ANY reference dropdown to another EC object.
- **Chase the data before the code.** Reproducing a symptom 4 times (screenshots/video/live) proved the
  symptom was real, but proved nothing about WHERE the fault was - the actual fault was in the test
  data (Start Date), not in `select_dropdown()`. The lesson: check the referenced object's own
  effective dates in the DB *before* concluding a shared function is defective, especially when the
  same symptom recurs across multiple unrelated screens (a shared wrong-assumption in test data setup
  is at least as likely as a shared code defect).
- **Don't assume the generator's navigator-id template transfers 1:1** to every OV-GM screen - the
  BU-gated single-dropdown pattern can have Date and the dropdown in either the same group or
  different groups; verify the live id before trusting the generated driver/T3.
