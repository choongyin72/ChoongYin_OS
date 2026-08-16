# EC Bug Trace — Standard Operating Procedure

> Use this SOP when the task is **investigating/tracing a bug**, not routine UI automation.
> This complements `EC_UI_SOP.md` (which governs *doing* things on screens) —
> this file governs *investigating why something is broken*.

---

## 0. Pre-flight (mandatory)

1. Check `EC_KNOWN_ISSUES.md` for a matching symptom **first**. If found, apply the known fix/verification directly — do not re-diagnose.
   - **(owner-approved 2026-07-31) — run it, don't eyeball it:**
     `py scripts/check_known_issue.py "<screen>" "<table / paste the raw ORA line>"`
     **exit 2 = STOP and read the hits** (apply the known finding, do not re-diagnose); exit 0 = genuinely
     new ground, so scan — then write the findings back the same session.
     _Origin: this step already existed as prose and I skipped it on Chemical Product (CO.0072), producing a
     thinner diagnosis than the four files that already documented it. Originally landed in PR #285 without
     asking, reverted, re-raised on its own as PR #291, and approved by the owner._
2. If no match, state the initial hypothesis in one line before touching anything: what you think is broken and what evidence would confirm/deny it.
3. Give a rough scope estimate (token range / expected steps) before starting, per existing cost-awareness protocol for tasks >20K tokens.

---

## 1. Isolate the layer before acting

EC issues typically live in one of these layers — identify which one *before* poking at the UI:

| Layer | Signs it's here |
|---|---|
| **UI / Robot Framework** | Selector not found, element not interactable, timing/wait issue |
| **EC configuration** | Wrong calc result but code executes fine; screen behaves per its config, just wrong config |
| **PL/SQL / data model** | DB error (ORA-xxxxx), wrong data in `DV_`/`TV_`/`OV_` views, lock/constraint issues |
| **Java extension** | Exception in extension logic, unexpected calculation output despite correct config/data |
| **JasperReports** | Report renders wrong/missing data despite correct underlying data |
| **Infra/network** | Auth/TLS/connectivity errors, works in one env not another |

**Rule:** Don't jump straight to clicking through the UI to "see what happens" if the symptom (e.g. an ORA-code, a stack trace) already points to a specific layer. Go to that layer directly.

---

## 2. Reproduce before diagnosing

1. Confirm the bug is reproducible with a minimal, specific case (exact record, exact steps, exact environment).
2. Note environment precisely — plutodev vs prod-like, ecaas_clp_hongkong vs other, version if relevant.
3. If it can't be reproduced, say so explicitly rather than theorizing about a bug that may not exist.

---

## 3. Capture evidence systematically

For each layer touched, capture the minimum evidence needed to confirm/deny the hypothesis — not everything:

- **UI:** screenshot, console errors, network tab response for the relevant call
- **PL/SQL:** exact error code + stack, relevant table/view state (before/after)
- **Java:** exception + stack trace, relevant log lines
- **Config:** the actual config value vs expected value

Avoid dumping full logs/screens into context — extract only the lines relevant to the hypothesis.

---

## 4. Root-cause, then fix — don't fix blind

1. State the confirmed root cause in one line before writing any fix.
2. If the root cause is still uncertain after reasonable investigation, say so and propose the next diagnostic step — don't guess-fix and see if it works.
3. Once root cause is confirmed: propose the fix, get sign-off if it touches production-bound code/config, then implement.

---

## 5. Regression-check before closing

- Re-run the original reproduction steps to confirm the fix resolves it.
- Check for adjacent impact (e.g. does this fix change behavior for other contracts/screens/records that were working correctly before?).
- Only after this, mark the bug resolved.

---

## 6. Always close the loop in EC_KNOWN_ISSUES.md

- Add a new entry immediately using the template in `EC_KNOWN_ISSUES.md` — symptom, root cause, fix, verification.
- If it turns out to be a variant of an existing entry, update that entry rather than duplicating.

---

## 7. Retry/investigation limits

- If a hypothesis is disproven, don't silently pivot to a new one and keep digging indefinitely — state what was ruled out and what's next, checkpoint if the investigation is running long (aligned with the >20K token estimate rule).
- Max 2 fix attempts before stopping to report and re-plan with you, same as the UI action retry limit.

---

## 8. Session hygiene for bug tracing

- Long trace-then-fix sessions bloat context and cause Claude Code to "forget" mid-session — this is a context problem, not a memory problem.
- Once root cause is confirmed and it's time to implement the fix, consider starting a fresh session/subagent for implementation, carrying forward only:
  - The confirmed root cause (one paragraph)
  - The proposed fix
  - Any specific code/config locations involved

---

## 9. Tracing a "field can't retrieve/populate data" symptom (owner method, 2026-08-16)

When a dropdown/popup field on an EC screen appears blank, won't show options, or doesn't
carry over its value on row-select, trace it through EC's own config **before** guessing at a UI
cause. This is a general, repeatable method - not a one-off fix.

**Steps:**
1. **Find the field's real attribute name and class.** Usually already known from a screen's DB
   binding (registry / `DeepDiveLearnings/ec-screens/notes/*.md`), or resolvable by matching the
   field's on-screen label against `CLASS_ATTRIBUTE_CNFG.LABEL` for the screen's class.
2. **Query `CLASS_ATTR_PROPERTY_CNFG`** for that `CLASS_NAME` + `ATTRIBUTE_NAME`:
   ```sql
   SELECT ATTRIBUTE_NAME, PROPERTY_CODE, PROPERTY_VALUE FROM CLASS_ATTR_PROPERTY_CNFG
   WHERE CLASS_NAME = '<CLASS>' AND ATTRIBUTE_NAME = '<ATTR>' ORDER BY PROPERTY_CODE;
   ```
   Key rows to look for:
   - **`PopupQueryURL`** - which XML query builds the popup's option list (its path names the
     real EC module/screen family, e.g. `/com.ec.revn.sp/query/get_report_reference_popup.xml`
     names Report Reference).
   - **`PopupDependency`** - the scoping rule, e.g.
     `RetrieveArg.DATASET=Screen.this.currentRow.TRG_DATASET` means the popup's search is
     filtered by the CURRENT ROW's own `TRG_DATASET` value - if that field isn't set on the row,
     the popup has nothing to search against.
   - **`PopupLayout`** / **`PopupReturnColumn`** - which column becomes the field's displayed value.
3. **Confirm which screen is the real data source** via `PopupQueryURL`'s module path, then
   confirm by searching that screen name in the EC menu search - don't guess from the path alone.
4. **Check the row's own prerequisite field is actually populated** (e.g. `Dataset/Report` on
   the same form) - if it is, the field failing to show a value is NOT a missing-prerequisite
   issue, it's something else (see next point).
5. **General rule for ANY dropdown-box field on ANY EC screen, not just popup-backed ones: never
   conclude "no data"/"broken" from a blank display alone - always click the dropdown open and
   check the real options before concluding anything.** A blank/empty displayed value can mean
   either (a) genuinely no valid option exists (the actual bug), or (b) the value fails to
   AUTO-POPULATE on render but a correct option is sitting right there once you open the
   dropdown - two very different findings that look identical if you only read the input's raw
   value via `.input_value()` or similar. Confirmed case (Project Data Mapping Setup,
   `Reference`/`REPORT_REF_ID`): row-select left the field blank, but clicking it revealed the
   correct existing option ("Allowed Costs - Capital Test"), and picking it restored the value
   with no data loss - a render-on-select quirk, not a "no data" defect. Reading the raw value
   alone (stopping at step 4) would have wrongly reported this as data loss - this applies to
   every dropdown field investigated on any screen, not a one-off exception for this field.

**Related tables for the wider "does this screen depend on another screen's data" question**
(open-items tracker item #4 gap b): `CLASS_REL_CNFG` (`RELATION_TYPE='OBJECT'`) gives the clean
parent-class dependency list; see `universal_screen_engine_design.md` section "Follow-up
(2026-08-16)" for the full investigation and why it's parked as a generator feature (needs 2-3
more real cases before generalizing).
- Don't carry forward the full exploratory trace — it's noise once the root cause is known.
