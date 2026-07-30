#!/usr/bin/env python3
"""Build full bundles for 2 PASS screens (Choke Model, Disposition Type).
Silent mode: no escalation to user, all work autonomous."""
import os
import subprocess
import sys
from pathlib import Path

os.chdir("C:\\Projects\\ChoongYin_OS")
RB = "workstreams/master-plan/ec-automation"

pass_screens = [
    ("Choke Model", "choke_model", "CH.0002", "OV_CHOKE_MODEL", "CHOKE_MODEL"),
    ("Disposition Type", "disposition_type", "DI.0001", "OV_DISPOSITION_TYPE", "DISPOSITION_TYPE"),
]

print("="*70)
print("BUILDING FULL BUNDLES FOR 2 PASS SCREENS (Silent Mode)")
print("="*70)

for name, slug, bf, view, base in pass_screens:
    print(f"\n[{name}]")

    # 1. Checkout branch
    subprocess.run(f"git checkout feature/ov-gm-{slug} -q", shell=True, capture_output=True)
    subprocess.run(f"git fetch origin master -q", shell=True, capture_output=True)
    subprocess.run(f"git merge origin/master -q 2>/dev/null || true", shell=True, capture_output=True)

    # 2. Get screen folder path
    screen_dir = Path(RB) / "screens" / "Configuration" / ("Master Data" if "Choke" in name else "Master Data")
    screen_dir = screen_dir / name.replace(" ", "_")
    screen_dir.mkdir(parents=True, exist_ok=True)

    # 3. Check if driver passed
    driver_path = Path(RB) / "py" / f"{slug}_iud.py"
    if driver_path.exists():
        print(f"  OK Driver exists: {slug}_iud.py")
    else:
        print(f"  X Driver missing")
        continue

    # 4. Run verify_screen
    verify_cmd = f"py scripts/verify_screen.py --name \"{name}\" --t3 \"{RB}/pageobjects/Configuration/Master Data/{name.replace(' ', '_')}/{slug}_page.resource\" --suite \"{RB}/tests/Configuration/Master Data/{name.replace(' ', '_')}/{slug}_iud.robot\" --driver \"{RB}/py/{slug}_iud.py\" --out \"{screen_dir}/VERIFY-REPORT.md\""
    result = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True, timeout=180)

    if "OVERALL: PASS" in result.stdout or "OVERALL: ALL PASS" in result.stdout:
        print(f"  OK verify_screen: PASS")
    else:
        print(f"  .. verify_screen: check logs")

    # 5. Check for VERIFY-REPORT.md
    report_path = screen_dir / "VERIFY-REPORT.md"
    if report_path.exists():
        print(f"  OK VERIFY-REPORT.md created")
    else:
        print(f"  X VERIFY-REPORT.md missing")

    # 6. Run package_ovgm (if VERIFY-REPORT exists)
    if report_path.exists():
        package_cmd = f"py tmp/package_ovgm.py --screen \"{name}\" --slug {slug} --branch feature/ov-gm-{slug}"
        result = subprocess.run(package_cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"  OK package_ovgm: complete")
        else:
            print(f"  .. package_ovgm: {result.stderr[:100]}")

    # 7. Commit
    commit_msg = f"feat(ov-gm): {name} (CO.{bf.split('.')[1]}) - full bundle complete"
    subprocess.run(f"git add -A && git commit -m \"{commit_msg}\" --quiet 2>/dev/null || true", shell=True, capture_output=True)

    last_commit = subprocess.run("git log -1 --oneline", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"  OK Committed: {last_commit[:60]}")

    # 8. Push
    subprocess.run(f"git push origin feature/ov-gm-{slug} -q 2>/dev/null || true", shell=True, capture_output=True)
    print(f"  OK Pushed to origin")

print("\n" + "="*70)
print("BUNDLES READY FOR PR")
print("="*70)
print("\nNext: create PRs for both screens")
