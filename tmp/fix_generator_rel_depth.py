#!/usr/bin/env python3
"""Latent bug in BOTH generators, surfaced by Message Group: the T3 and suite templates hardcode
`../../../../` (4 levels up). That is only correct for a THREE-segment folder like
Configuration/Assets/Facility_Objects (pageobjects/A/B/C/x.resource -> up 4 = ec-automation root).

Message Group lives at Configuration/Messaging - TWO segments - so 4 levels climbs one directory ABOVE
ec-automation and every import silently fails to resolve. Symptom was dryrun 0/4 with "No keyword with
name 'Prepare IUD Object Data' found" (the resource never loaded), not an obvious path error.

Fix: compute the depth from the folder itself.
  - T3 sits at   pageobjects/<folder>/x.resource  -> up = len(folder segments) + 1
  - suite sits at tests/<folder>/x.robot          -> up = len(folder segments) + 1
Every screen shipped so far had a 3-segment folder, which is why this never bit before.
"""
from pathlib import Path

ROOT = Path(r"C:\Projects\ChoongYin_OS")
UP = '''
# relative depth must be computed, not hardcoded: `../../../../` is only right for a 3-segment folder
# (Message Group at Configuration/Messaging has 2 and every import silently failed to resolve)
_up = "../" * (len(folder.split("/")) + 1)
'''

for name in ("gen_ovgm.py", "gen_ov.py"):
    p = ROOT / "tmp" / name
    s = p.read_text(encoding="utf-8")
    assert s.count("../../../../") == 4, "%s: expected 4 hardcoded depths, found %d" % (
        name, s.count("../../../../"))

    # define _up right after `folder` is parsed
    anchor = 'folder = a["folder"].strip("/")'
    assert s.count(anchor) == 1, "%s: folder parse line not found" % name
    line_end = s.index("\n", s.index(anchor))
    s = s[:line_end + 1] + UP.lstrip("\n") + s[line_end + 1:]

    # swap the literals for the token, and make sure each template interpolates it
    s = s.replace("../../../../", "%(up)s")

    # both templates are `'''...''' % dict(...)`; add up=_up to every dict that now needs it
    out, changed = [], 0
    for chunk in s.split("''' % dict("):
        out.append(chunk)
    s = "''' % dict(".join(out)
    # append up=_up to the dict calls belonging to templates containing %(up)s
    import re
    def add_up(m):
        global changed
        body = m.group(1)
        if "up=" in body:
            return m.group(0)
        changed += 1
        return "''' %% dict(%s, up=_up)" % body
    s = re.sub(r"''' % dict\((.*?)\)\n", lambda m: add_up(m) + "\n", s, flags=re.S)
    p.write_text(s, encoding="utf-8")
    print("%s: 4 hardcoded depths -> computed _up; %d template dict(s) updated" % (name, changed))
