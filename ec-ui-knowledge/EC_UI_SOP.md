# EC UI Interaction — Standard Operating Procedure

> **Read this file in full before touching any EC UI screen.**
> This SOP is constant — it does not change between screens or sessions.
> Screen-specific selectors live separately in `screens/<screen-name>.md`.

---

## 0. Mandatory pre-flight (every task, no exceptions)

1. Read this SOP file.
2. Check `screens/<screen-name>.md` for the target screen.
   - **Exists** → use its selectors directly. Do NOT re-scan the DOM "just to check."
   - **Does not exist** → proceed to Step 1 (Discovery Mode) below.
3. Confirm which environment/credentials apply (`${EC_URL}`, `${EC_USERNAME}`, `${EC_PASSWORD}`, `${WAIT_TIMEOUT}=30s`).
4. State the plan back in one short line before executing (screen name, action, source of selectors: "file" or "fresh scan").

---

## 1. Discovery Mode (only when no screen file exists, or a selector fails)

1. Navigate to the target screen.
2. Perform **ONE** live DOM scan via Playwright (`page.content()` / accessibility tree / targeted `locator` queries) — not repeated trial-and-error clicking.
3. Capture:
   - Screen URL / navigation path
   - Element IDs/selectors for every field, button, dropdown involved in the task
   - Save/confirm sequence (some screens have a secondary confirm dialog, some don't)
   - Any validation or loading quirks observed
4. **Immediately write this to `screens/<screen-name>.md`** using the template, before performing the actual save/update/delete action.
5. Only after the file is written, proceed to execute.

**Rule:** One discovery scan per screen per session, maximum. If a freshly-scanned selector still fails, stop and report — do not re-scan repeatedly or guess variations.

---

## 2. Standard action sequence (applies to every screen)

1. Navigate to screen → wait for full load (`${WAIT_TIMEOUT}`).
2. Locate target record via **exact-text match** search/filter (never partial/fuzzy match).
3. Open record / trigger action (edit, new, delete).
4. Fill fields per screen file selectors.
5. Trigger save.
6. Wait for explicit confirmation (toast, dialog, or URL/state change) — do not assume success from absence of error.
7. Verify the change (re-query the record, or check returned confirmation text) before reporting success.
8. If a screenshot-on-failure convention exists, capture it on any unexpected state.

---

## 3. Retry & failure policy (hard limit)

- **Maximum 2 attempts** on any save/update/delete action.
- If both fail:
  - STOP.
  - Report exactly what was tried, what error/state was observed, and where it diverged from the screen file.
  - Do NOT keep trying alternate selectors, alternate click sequences, or "just one more variation."
- If a screen file's selector turns out to be wrong/stale, correct the screen file immediately (see below) rather than layering workarounds in the task itself.

---

## 4. Keeping screen files current

- If a documented selector fails and a corrected one is found: update `screens/<screen-name>.md` in the same session, and note the change (date + what changed) in that file's changelog section.
- If a new field/action is used on an already-documented screen: add it to the existing file rather than creating a duplicate.
- Screen files are the single source of truth — never trust memory of a screen's DOM from a previous session over what's written in the file.

---

## 5. Idempotency & test data conventions

- Use `AUTOTEST_` prefixed data for anything created during automation/testing, per existing RF conventions.
- Prefer patterns that can be safely re-run without creating duplicate/orphaned records.
- Clean up test data created during discovery/verification unless explicitly told to leave it.

---

## 6. Relationship to `ROBOT_CLAUDE.md`

- `ROBOT_CLAUDE.md` governs **RF code conventions** (Page Object Model structure, naming, file layout).
- This SOP + `screens/*.md` govern **live UI interaction knowledge** (what the screen actually looks like and how to drive it).
- Both are read before any EC UI automation task; neither substitutes for the other.
