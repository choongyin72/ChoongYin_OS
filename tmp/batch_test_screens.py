import subprocess, sys

screens = [
    ("Well Hole", "CO.0051", "OV_WELL_HOLE", "well_hole", "Configuration/Assets/Well and Reservoir Objects"),
    ("Shift", "CO.0224", "OV_SHIFT", "shift", "Configuration/Assets/Facility Objects"),
    ("Well Hookup", "CO.0108", "OV_WELL_HOOKUP", "well_hookup", "Configuration/Assets/Facility Objects"),
    ("Lifting Account", "CO.2004", "OV_LIFTING_ACCOUNT", "lifting_account", "Configuration/Assets/Transport Objects"),
    ("Channel", "CO.2077", "OV_CHANNEL", "channel", "Configuration/Assets/Transport Objects"),
    ("Loading Arm", "CO.2078", "OV_LOADING_ARM", "loading_arm", "Configuration/Assets/Transport Objects"),
]

for screen, bf, view, slug, folder in screens:
    cmd = f'''py tmp/gen_ovgm.py '{{"screen":"{screen}","bf":"{bf}","view":"{view}","base":"{slug.upper()}","folder":"{folder}","slug":"{slug}","abbr":"{slug[:3]}","code_prefix":"AUTOTEST_{slug.upper()}_","code_label":"{screen} Code","name_label":"{screen} Name","screen_folder":"{screen.replace(' ','_')}","extra_dropdowns":[],"popups":[],"has_op_pu":true,"nav":["Production Unit","Area","Facility Class 1"],"date":"2026-07-30"}}'  '''
    print(f"[{screen}] generating...", end=" ", flush=True)
    r = subprocess.run(cmd, shell=True, capture_output=True, timeout=60)
    if r.returncode == 0:
        print("OK")
    else:
        print(f"FAIL: {r.stderr.decode()[:80]}")
