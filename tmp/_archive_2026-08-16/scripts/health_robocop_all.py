"""Health pass step 1: robocop across the whole ec-automation framework."""
import subprocess
import sys

ROOT = r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation"
r = subprocess.run(["robocop", "check", ROOT], capture_output=True, text=True,
                   timeout=300, shell=True)
out = (r.stdout or "") + (r.stderr or "")
print(out[-12000:] if len(out) > 12000 else out)
print(f"\nexit code: {r.returncode}")
sys.exit(0)
