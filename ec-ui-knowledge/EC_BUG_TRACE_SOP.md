# EC Bug Trace — Standard Operating Procedure

> Use this SOP when the task is **investigating/tracing a bug**, not routine UI automation.
> This complements `EC_UI_SOP.md` (which governs *doing* things on screens) —
> this file governs *investigating why something is broken*.

---

## 0. Pre-flight (mandatory)

1. Check `EC_KNOWN_ISSUES.md` for a matching symptom **first**. If found, apply the known fix/verification directly — do not re-diagnose.
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
- Don't carry forward the full exploratory trace — it's noise once the root cause is known.
