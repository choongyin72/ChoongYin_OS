# Meter popup-picker gesture — ✅ RESOLVED (2026-06-13, Meter live 4/4)

The Delivery Point field on Meter's insert form (`...R:5:C:1:pin` + `pinB` button) is an
**EC framework popup**, not a dd:

1. `pinB` onclick = PrimeFaces.ab updating `popupForm:popupUrl` then `EC.popup.showPopup(...)`.
2. The popup = `popupForm:popup` dialog wrapping **`popupIFrame`** with URL
   `/com.ec.tran.co.screens/object_popup?CLASS_NAME=<class>` (DELIVERY_POINT here).
3. Inside the IFRAME: grid **`PopupList:form:T_data`** + controls
   (`PopupList:form:fcNum_input`, `hideMenu`, `T_selection`). Grid showed n=1 rows with
   form date 2003-01-01 — verify whether that's "No records found" or a real row; if empty,
   the popup may need a search/filter action inside the frame, or the form's date governs
   the effective-date filter (version-filter rule!).
4. Automation design (new T2 gesture `Pick From EC Object Popup`):
   - Click `<cell>pinB` → wait for `popupIFrame` visible
   - Browser-library: `Select Frame    id=popupIFrame` (or css iframe selector) →
     find row by code/label in `PopupList:form:T_data` (TV-style input values) → click row
   - Selection likely closes the popup + writes the `pin` input on the main form
     (verify; else look for an OK button) → `Unselect Frame`
   - Verify main-form `pin` input value before Save.
5. Meter's OTHER mandatory: Meter Type dd R4 (Entry/Exit/Fuel/Transit) — plain dd gesture.
6. Meter nav: BU-gated like its siblings (nav dd `nav:form:G:0:R:1:C:1:dd`).

7. **GOTCHA (2026-06-13): pinB click "times out" in Playwright even though it WORKS** —
   the click fires the AJAX and `popupForm:popup_modal` (dialog mask) appears mid-click,
   so actionability-checked clicks never report success and retries are intercepted.
   Use a JS click instead: `page.evaluate("document.getElementById('<pinB id>').click()")`
   (RF Browser: `Evaluate JavaScript` or `Click ... force=True`), THEN wait for
   `#popupIFrame` visible with src containing `object_popup`.

Remaining build steps: JS-click pinB → wait iframe → dump rows (verify the n=1 row is a
real DP vs "No records found"; if empty, drive the popup's own search) → row-click →
verify main-form `pin` value + popup closed → THEN: new T1 `popup.resource` with
`Pick From EC Object Popup    <pin-cell-prefix>    <code>` →
meter_page.resource + meter_iud.robot → live + DB verify (ov_meter).


## ✅ FINAL RECIPE (proven, Meter 4/4 live + DB-verified)
T1 keyword `Pick From EC Object Popup` (resources/popup.resource):
1. JS-click the pinB (actionability-checked clicks time out — dialog mask races the click).
2. Wait `#popupIFrame` visible + settle.
3. Find + click the row INSIDE the frame via JS matching the input VALUE PROPERTY **or**
   row innerText — NEVER XPath `@value` (EC populates grid inputs dynamically; the HTML
   attribute stays empty → attribute XPath never matches; also the popup renders cells as
   text in some modes). On miss, the keyword logs the popup innerText for diagnosis.
4. Row click selects + closes the popup + fills the main-form `pin` input (verified).
PRE-REQ: the screen NAVIGATOR context (BU) must be set before opening the form — the popup
list is navigator-filtered (else "No records found").
Meter insert order: Open form → date → POPUP pick → code/name → Meter Type dd → Save.
Cleanup note: probe meters deleted via UI End=Start; ov_meter has zero AUTOTEST rows.
