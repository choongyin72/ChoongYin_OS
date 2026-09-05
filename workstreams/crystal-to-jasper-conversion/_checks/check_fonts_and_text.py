"""Font sizes and text presence, generated vs reference.

    py check_fonts_and_text.py R07.005

Two things in one pass because they interact: changing a font size can silently drop text when
a box is shorter than roughly fontSize * 1.2 (lessons file Part F1). Any font change must be
followed by the text check in the same breath.

Reported "missing"/"extra" pairs of the SAME string are span-splitting differences, not real
defects - the reference sometimes emits one run of text as two spans.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import open_pair  # noqa: E402


def spans(doc):
    out = []
    for p in range(len(doc)):
        for b in doc[p].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip():
                        out.append((p, s["text"].strip(), round(s["size"], 1), s["font"]))
    return out


def main():
    gen, ref = open_pair()
    G, R = spans(gen), spans(ref)

    print("=== font sizes ===")
    for tag, lst in (("ref", R), ("gen", G)):
        c = collections.Counter(s[2] for s in lst)
        print(f"  {tag}: " + "  ".join(f"{k}pt x{v}" for k, v in sorted(c.items())))

    print("\n=== size/style mismatches, by text ===")
    def keyed(lst):
        m = collections.defaultdict(collections.Counter)
        for _p, t, sz, fn in lst:
            m[t][(sz, "B" if "Bold" in fn else "-", "I" if "Italic" in fn else "-")] += 1
        return m
    KG, KR = keyed(G), keyed(R)
    bad = 0
    for t, rc in KR.items():
        gc = KG.get(t)
        if not gc:
            continue
        rk, gk = rc.most_common(1)[0][0], gc.most_common(1)[0][0]
        if rk != gk:
            print(f"  ref {rk[0]:5}pt {rk[1]}{rk[2]}   gen {gk[0]:5}pt {gk[1]}{gk[2]}   "
                  f"{t[:44]!r}")
            bad += 1
    print(f"  mismatches: {bad}")

    print("\n=== text presence, per page ===")
    total = 0
    for p in range(min(len(gen), len(ref))):
        g = collections.Counter(s[1] for s in G if s[0] == p)
        r = collections.Counter(s[1] for s in R if s[0] == p)
        miss, extra = r - g, g - r
        both = set(miss) & set(extra)          # same string on both sides = span split
        real_miss = sum(v for k, v in miss.items() if k not in both)
        real_extra = sum(v for k, v in extra.items() if k not in both)
        print(f"  page {p+1}: {real_miss} missing, {real_extra} extra "
              f"({len(both)} span-split, ignored)")
        for k, v in miss.items():
            if k not in both:
                print(f"     MISSING x{v} {k[:64]!r}")
        for k, v in extra.items():
            if k not in both:
                print(f"     EXTRA   x{v} {k[:64]!r}")
        total += real_miss + real_extra
    print(f"\nreal text differences: {total}")


if __name__ == "__main__":
    main()
