"""Random-suite spot check: pick ONE random live suite (excluding the 5 canary suites
and parked suites) and run it headless. Part of the post-change verification ladder:
robocop -> dryrun-all -> canary pack -> THIS.
"""
import random
import subprocess
import sys
import time
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/tests")
CANARY = {"bank_iud", "area_iud", "mime_iud", "object_list_setup_iud", "account_mapping_iud"}
# Validation suites are RUN-verify evidence suites (data-anchored dates) — not IUD spot-check targets
EXCLUDE_DIRS = {"_parked", "Validation"}

candidates = [s for s in TESTS.rglob("*.robot")
              if s.stem not in CANARY and not (set(s.parts) & EXCLUDE_DIRS)]
suite = random.choice(candidates)
out = rf"c:/tmp/random_check/{time.strftime('%Y%m%d_%H%M%S')}_{suite.stem}"
print(f"RANDOM PICK ({len(candidates)} candidates): {suite.relative_to(TESTS)}")

r = subprocess.run(["robot", "--outputdir", out, str(suite)],
                   capture_output=True, text=True, timeout=900, shell=True)
lines = (r.stdout or "").splitlines()
stat = next((l.strip() for l in reversed(lines) if "tests," in l), "?")
print(f"  {stat}")
print(f"  output: {out}")
print(f"\n{'PASS - random spot check OK' if r.returncode == 0 else 'FAIL - investigate before declaring change good'}")
sys.exit(r.returncode)
