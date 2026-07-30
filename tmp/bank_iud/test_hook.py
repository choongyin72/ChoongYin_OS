"""Test the check_existing_impl hook with fake PreToolUse events. tmp scratch."""
import json
import subprocess
import sys

HOOK = r"C:\Projects\ChoongYin_OS\.claude\hooks\check_existing_impl.py"
EC = "C:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/"

cases = {
    "WARN (new carrier file, existing carrier_page.resource)": EC + "py/carrier_iud.py",
    "SILENT (brand-new unique screen)": EC + "py/zzznewscreen_iud.py",
    "SILENT (non-EC path)": "C:/Projects/ChoongYin_OS/tmp/foo.py",
    "SILENT (editing existing engine)": EC + "py/ec_object_iud.py",
}

for label, path in cases.items():
    payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": path, "file_text": "x"}})
    r = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True, text=True)
    print("=" * 70)
    print(label)
    print("  exit:", r.returncode, "| stderr:", (r.stderr or "").strip()[:80])
    try:
        out = json.loads(r.stdout)
        ctx = out.get("hookSpecificOutput", {}).get("additionalContext")
        print("  decision:", out.get("hookSpecificOutput", {}).get("permissionDecision"))
        print("  warned:", "YES" if ctx else "no")
        if ctx:
            print("  msg:", ctx[:220])
    except Exception as e:
        print("  BAD OUTPUT:", r.stdout[:200], repr(e)[:80])
