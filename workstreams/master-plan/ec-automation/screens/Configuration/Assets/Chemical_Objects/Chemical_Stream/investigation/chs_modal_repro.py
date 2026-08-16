"""Item 6b: reproduce the confirmation-modal-blocks-next-click bug. Original observation: after
changing a field value on the updateAttributes form (dirty state) then re-navigating to the SAME
screen again in one page session (without Save or explicit discard), a row-click retry gets
intercepted by #confirmationForm:confirmation_modal. Read-only test - no Save.
Run headed: EC_HEADED=1 py -X utf8 tmp/chs_modal_repro.py
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[5] / "py"))
from engine import Engine, open_screen, css  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

HEADED = os.environ.get("EC_HEADED", "0") == "1"
NAV_PU, NAV_AREA, NAV_FC1 = "P1 Production Unit", "P1 Area", "P1 Facility 1"
CODE_A = "P1 CS001 CT001 SI"
CODE_B = "P1 CS001A CT001 W001 SI"

with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=250 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    print("=== PASS 1: open Chemical Stream, navigate, select a row, dirty a field (no Save) ===")
    open_screen(page, "Chemical Stream")
    eng = Engine(page, "Chemical Stream")
    eng.apply_navigator(values=[NAV_PU, NAV_AREA, NAV_FC1])
    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    eng.select_row(grid_id, CODE_A)
    eng.select("Stream Phase", "__FIRST__")   # dirty the form, deliberately do NOT Save
    print("  form dirtied (Stream Phase changed, not saved)")

    print("=== re-navigating to Chemical Stream AGAIN in the same page session (no reset) ===")
    modal_seen_1 = page.locator(css("confirmationForm:confirmation_modal")).count() > 0
    print("  confirmation modal present before re-nav:", modal_seen_1)
    try:
        open_screen(page, "Chemical Stream")
        print("  re-navigation SUCCEEDED (no modal block)")
    except Exception as e:
        print("  re-navigation FAILED/BLOCKED:", repr(e)[:150])
        modal = page.locator("css=[id*='confirmation']")
        n = modal.count()
        print(f"  {n} element(s) matching '*confirmation*' id")
        for i in range(min(n, 5)):
            el = modal.nth(i)
            try:
                print(f"    [{i}] id={el.get_attribute('id')!r} visible={el.is_visible()}")
            except Exception:
                pass
        for fid in ["confirmationForm:confirmationTitle", "confirmationForm:confirmation_content",
                    "confirmationForm:confirmation_title"]:
            loc = page.locator(css(fid))
            if loc.count():
                try:
                    print(f"  {fid} text: {loc.first.inner_text()!r}")
                except Exception as ex:
                    print(f"  {fid} text read failed: {ex}")
        buttons = page.locator("#confirmationForm\\:confirmation button, #confirmationForm\\:confirmation a")
        n2 = buttons.count()
        print(f"  {n2} button/anchor element(s) inside the dialog")
        for i in range(n2):
            try:
                print(f"    button[{i}]: id={buttons.nth(i).get_attribute('id')!r} "
                      f"text={buttons.nth(i).inner_text()!r} visible={buttons.nth(i).is_visible()}")
            except Exception as ex:
                print(f"    button[{i}]: read failed: {ex}")
        # also dump the raw outer HTML of the dialog for full ground truth
        try:
            html = page.locator(css("confirmationForm:confirmation")).first.inner_html()
            print("  dialog inner_html (first 1500 chars):", html[:1500])
        except Exception as ex:
            print("  inner_html read failed:", ex)

    print("=== retry: apply navigator + select a DIFFERENT row ===")
    try:
        eng2 = Engine(page, "Chemical Stream")
        eng2.apply_navigator(values=[NAV_PU, NAV_AREA, NAV_FC1])
        grids2 = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id2 = grids2[0]
        ok = eng2.select_row(grid_id2, CODE_B)
        print("  select_row on retry ->", ok)
    except Exception as e:
        print("  RETRY FAILED:", repr(e)[:300])
        # check if a modal is what's blocking it
        modal = page.locator(css("confirmationForm:confirmation_modal"))
        print("  modal count at failure:", modal.count(), "visible:", modal.first.is_visible() if modal.count() else None)
        title = page.locator(css("confirmationForm:confirmationTitle"))
        content = page.locator(css("confirmationForm:confirmationContent"))
        print("  title:", title.first.inner_text() if title.count() else None)
        print("  content:", content.first.inner_text() if content.count() else None)

    if HEADED:
        page.wait_for_timeout(4000)
    b.close()
