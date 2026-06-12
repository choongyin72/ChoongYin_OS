"""Rewrite the xlsx zip with [Content_Types].xml as the FIRST entry so streaming MIME
detectors (Tika) recognize it as OOXML instead of plain zip."""
import shutil
import zipfile
from pathlib import Path

p = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon/claude_excel_import_test.xlsx")
tmp = p.with_suffix(".reordered.xlsx")

with zipfile.ZipFile(p) as zin:
    names = zin.namelist()
    order = [n for n in names if n == "[Content_Types].xml"] + \
            [n for n in names if n != "[Content_Types].xml"]
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in order:
            zout.writestr(n, zin.read(n))

shutil.move(tmp, p)
with zipfile.ZipFile(p) as z:
    print("new entry order:", z.namelist()[:4])
print("rewritten:", p)
