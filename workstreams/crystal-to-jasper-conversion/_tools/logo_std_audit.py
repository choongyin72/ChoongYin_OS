"""Current state of the logo contract across ALL R07.XXX and R10.XXX, against the owner's standard.

    py tmp/logo_std_audit.py

Owner's target (2026-09-06), to hold for every report:

    <parameter name="P_BASE_URL" class="java.lang.String" forPrompting="false">
        <defaultValueExpression><![CDATA["/extension/ZREP/reports/"]]></defaultValueExpression>
    </parameter>
    <expression><![CDATA[$P{P_BASE_URL} + "ichthys-logo.png"]]></expression>

Read-only. Three things are checked separately, because they are three different edits:
  1. the parameter's defaultValueExpression
  2. $P{} vs $F{} in the image expression
  3. the filename asked for

(3) is reported rather than assumed, because EC-DEPLOYMENT-FINDINGS.md records a NAME COLLISION
as the root cause of the original R07 logo failures: R07.001-006 use a wide INPEX wordmark
(aspect ~5.78) and R07.011-025 an "INPEX | Ichthys Project" tile (aspect 1.903). Forcing one
filename on both families is what broke them before, so the box aspect is printed alongside.
"""
import os
import re

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
WANT_DEF = "/extension/ZREP/reports/"
ELEM = re.compile(r'<element\b[^>]*?/>|<element\b[^>]*?>.*?</element>', re.S)

print("%-9s %-44s %-7s %-6s %-22s %-4s %s"
      % ("report", "jrxml", "box", "asp", "param default", "ref", "file"))
print("-" * 122)
rows = []
for rep in sorted(d for d in os.listdir(BASE) if re.match(r'R(07|10)\.\d+$', d)):
    S = os.path.join(BASE, rep, "output")
    if not os.path.isdir(S):
        continue
    for fn in sorted(f for f in os.listdir(S) if f.endswith(".jrxml") and "backup" not in f):
        t = open(os.path.join(S, fn), encoding="utf-8", errors="replace").read()
        pm = re.search(r'<parameter name="P_BASE_URL"[^>]*>(.*?)</parameter>', t, re.S)
        dflt = "(no parameter)"
        if pm:
            dm = re.search(r'<defaultValueExpression><!\[CDATA\[(.*?)\]\]>', pm.group(1), re.S)
            dflt = dm.group(1) if dm else "(no default)"
        elif '<parameter name="P_BASE_URL"' in t:
            dflt = "(self-closing)"
        img = next((s for s in ELEM.findall(t) if 'kind="image"' in s), None)
        ref, fname, box, asp = "-", "-", "-", "-"
        if img:
            e = re.search(r'<expression><!\[CDATA\[(.*?)\]\]>', img, re.S)
            expr = re.sub(r'\s+', ' ', e.group(1)).strip() if e else ""
            ref = "$F" if "$F{P_BASE_URL}" in expr else ("$P" if "$P{P_BASE_URL}" in expr
                                                         else "none")
            f = re.search(r'"([^"]*\.(?:png|jpg|jpeg|gif))"', expr)
            fname = f.group(1) if f else "(dynamic)"
            g = dict(re.findall(r'\b(width|height)="(\d+)"', img))
            w, h = int(g.get("width", 0)), int(g.get("height", 0))
            box, asp = "%dx%d" % (w, h), ("%.2f" % (w / h)) if h else "-"
        rows.append((rep, fn[:-6], dflt, ref, fname, box, asp))
        print("%-9s %-44s %-7s %-6s %-22s %-4s %s"
              % (rep, fn[:-6][:44], box, asp, dflt[:22], ref, fname))

print("\n=== what needs changing ===")
for what, bad in (
        # the default is stored as a Java string literal INSIDE the CDATA, so it arrives with
        # its quotes: "/extension/ZREP/reports/". Comparing against the bare path made all 22
        # already-correct R07 files look non-compliant.
        ("parameter default != %r" % WANT_DEF,
         [r for r in rows if r[2].strip().strip('"') != WANT_DEF]),
        ("expression uses $F{} not $P{}", [r for r in rows if r[3] == "$F"]),
        ("no P_BASE_URL parameter at all", [r for r in rows if "no parameter" in r[2]]),
        ("no image element", [r for r in rows if r[5] == "-"])):
    print("\n%s: %d" % (what, len(bad)))
    for r in bad:
        print("   %-9s %-44s %s" % (r[0], r[1][:44], r[2] if "default" in what else ""))

print("\n=== filenames in use (do NOT unify blindly - see docstring) ===")
byname = {}
for r in rows:
    byname.setdefault((r[4], r[6]), []).append(r[0])
for (fname, asp), reps in sorted(byname.items()):
    print("   %-22s box aspect %-6s %2d file(s): %s"
          % (fname, asp, len(reps), ", ".join(sorted(set(reps)))))
