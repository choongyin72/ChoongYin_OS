from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\fix_scanner_readiness.py")
s = p.read_text(encoding="utf-8")
old = '''assert "import sys" in s, "sys not imported in the scanner - the abort path needs it"'''
assert s.count(old) == 1
s = s.replace(old, '''if "\nimport sys" not in s:                      # the abort path needs sys.exit
    s = s.replace("import os\n", "import os\nimport sys\n", 1)
    print("added missing 'import sys'")''')
p.write_text(s, encoding="utf-8")
print("patched the patcher")
