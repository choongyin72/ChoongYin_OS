"""Inventory every tag and attribute in a JasperReports 7 compact JRXML.

Written because grep is line-based and silently truncates multi-line <element ...> tags, which
gave an incomplete attribute list twice. An XML parse is authoritative, and it also proves the
file parses cleanly with the same parser the converter will use.

    py inventory.py <jrxml>
"""
import collections
import sys
import xml.etree.ElementTree as ET

path = sys.argv[1]
root = ET.parse(path).getroot()

print(f"root: <{root.tag}>")
print(f"  attrs: {sorted(root.attrib)}")

tags = collections.Counter()
attrs_by_tag = collections.defaultdict(collections.Counter)
kinds = collections.Counter()
attrs_by_kind = collections.defaultdict(collections.Counter)
children_by_kind = collections.defaultdict(collections.Counter)

for el in root.iter():
    tags[el.tag] += 1
    for a in el.attrib:
        attrs_by_tag[el.tag][a] += 1
    if el.tag == "element":
        k = el.get("kind", "?")
        kinds[k] += 1
        for a in el.attrib:
            if a != "kind":
                attrs_by_kind[k][a] += 1
        for c in el:
            children_by_kind[k][c.tag] += 1

print("\n=== tags ===")
for t, n in tags.most_common():
    print(f"  {t:24} x{n:<5} attrs: {dict(attrs_by_tag[t])}")

print("\n=== element kinds ===")
for k, n in kinds.most_common():
    print(f"\n  kind={k}  x{n}")
    print(f"     attrs   : {dict(attrs_by_kind[k])}")
    print(f"     children: {dict(children_by_kind[k])}")
