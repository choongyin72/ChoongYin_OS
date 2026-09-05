"""Tile traced border rectangles so every boundary carries exactly ONE line.

Crystal does not tile its cells - it leaves a small gap between neighbours, so each
boundary is drawn twice (see R07.006 fact-finding 4). Tracing inherits that, and after
integer-rounding some pairs collapse to one 1pt line while others stay two, which renders
as the "borderline thickness is not the same" defect the owner has reported on every report
so far. The owner accepted one-line-per-boundary on R07.006; this applies the same rule.

Two stages, both inside a TABLE (a run of vertically adjacent rows) so a boundary in one
table never drags a different table's column with it - that mistake cost a round on R07.003:

  1. snap    cluster the tables's cell edges (single-linkage, tol pt) and move every edge in
             a cluster to the cluster's rounded centre, so the header's column 2 and the data
             rows' column 2 land on the SAME x. Un-snapped, they sit 1pt apart and the
             vertical renders ~2pt.
  2. tile     within a row, set each cell to span snapped_left..next_snapped_left, closing
             gaps and removing overlaps. An overlap is the worse of the two: it puts the
             neighbour's border INSIDE a column (R07.006 3.2).
"""
import collections


def _cluster(vals, tol):
    """Single-linkage cluster of sorted values; returns {value: cluster_centre}."""
    out, cur = {}, []
    for v in sorted(vals):
        if cur and v - cur[-1] > tol:
            c = round(sum(cur) / len(cur))
            out.update({x: c for x in cur})
            cur = []
        cur.append(v)
    if cur:
        c = round(sum(cur) / len(cur))
        out.update({x: c for x in cur})
    return out


def _tables(rows, gap=6):
    """Group row y-values into tables: a new table starts where the vertical gap to the
    previous row's BOTTOM exceeds `gap`."""
    ys = sorted(rows)
    groups, cur, prev_bottom = [], [], None
    for y in ys:
        h = max(h for _, _, h in rows[y])
        if prev_bottom is not None and y - prev_bottom > gap:
            groups.append(cur)
            cur = []
        cur.append(y)
        prev_bottom = max(prev_bottom or 0, y + h)
    if cur:
        groups.append(cur)
    return groups


def tile(borders, tol=4, vtol=3, min_w=5, gap_close=6, vgap_close=3):
    """borders: list of (x, y, w, h, colour, linewidth). Returns a new list, tiled.

    Rows of a single cell are left alone horizontally (a full-width sub-heading must keep
    spanning the table, not be split), but still take part in the vertical snap.
    """
    rows = collections.defaultdict(list)
    for i, (x, y, w, h, col, lw) in enumerate(borders):
        rows[y].append((x, i, h))

    out = list(borders)
    stats = collections.Counter()

    for tbl in _tables(rows):
        # ---- horizontal snap + tile ------------------------------------------------
        edges = []
        for y in tbl:
            for x, i, h in rows[y]:
                edges += [x, x + borders[i][2]]
        snap = _cluster(edges, tol)
        # a cluster narrower than min_w would collapse a real column - leave those alone
        widths = sorted(set(snap.values()))
        bad = {c for a, c in zip(widths, widths[1:]) if c - a < min_w}
        if bad:
            stats["narrow-cluster-skipped"] += len(bad)

        for y in tbl:
            cells = sorted(rows[y])
            if len(cells) < 2:
                # A single rect on a row is a table outer frame or a full-width sub-heading:
                # it must keep SPANNING the table rather than being split. It still has to be
                # snapped though - left un-snapped its edges sat ~1pt off the tiled column
                # boundaries, so the frame and the first/last cell each drew their own stroke
                # and the table's outer verticals rendered 1.98pt against the reference's
                # 1.02pt. That was the whole of page 7's "thickness" finding.
                for x, i, h in cells:
                    o = out[i]
                    nx, nr = snap[x], snap[x + borders[i][2]]
                    if nr - nx >= min_w and (nx, nr - nx) != (o[0], o[2]):
                        out[i] = (nx, o[1], nr - nx, o[3], o[4], o[5])
                        stats["h-moved-span"] += 1
                continue
            bounds = [snap[x] for x, i, h in cells]
            last = cells[-1]
            bounds.append(snap[last[0] + borders[last[1]][2]])
            if len(set(bounds)) != len(bounds):
                stats["row-skipped-collapsed-bound"] += 1
                continue
            for k, (x, i, h) in enumerate(cells):
                # Close the gap to the next cell ONLY if it is small. A LARGE gap is a cell
                # Crystal deliberately does not draw, and stretching into it is destructive:
                # on page 2 this turned a 54pt cell (23..77) into a 229pt one (23..252) and
                # wiped out the row's intended blank span. Only sub-6pt gaps are the
                # doubling artefact that tiling is meant to remove.
                raw_right = x + borders[i][2]
                raw_gap = cells[k + 1][0] - raw_right if k + 1 < len(cells) else 0
                right = bounds[k + 1] if abs(raw_gap) <= gap_close else snap[raw_right]
                nx, nw = bounds[k], right - bounds[k]
                if nw < min_w:
                    stats["cell-skipped-too-narrow"] += 1
                    continue
                if abs(raw_gap) > gap_close:
                    stats["gap-preserved"] += 1
                if (nx, nw) != (x, borders[i][2]):
                    stats["h-moved"] += 1
                o = out[i]
                out[i] = (nx, o[1], nw, o[3], o[4], o[5])

        # ---- vertical snap + tile --------------------------------------------------
        vedges = []
        for y in tbl:
            vedges += [y] + [y + h for _, _, h in rows[y]]
        vsnap = _cluster(vedges, vtol)
        tops = sorted({vsnap[y] for y in tbl})
        for k, y in enumerate(sorted(tbl)):
            ny = vsnap[y]
            nxt = [t for t in tops if t > ny]
            for x, i, h in rows[y]:
                # same gap rule as the horizontal pass: only close a small gap to the row
                # below, never stretch across a deliberate blank band
                own = vsnap.get(y + h, y + h)
                # vgap_close is tighter than the horizontal gap_close: Crystal's horizontal
                # cell gaps run to ~4.6pt, but a vertical gap that big is a real blank band.
                # At 6pt this swallowed the 5.85pt band between page 2's row ending at
                # abs 626.2 and the next table starting at 632.05, deleting that rule.
                nb = nxt[0] if nxt and abs(nxt[0] - own) <= vgap_close else own
                nh = nb - ny
                if nh < 3:
                    stats["row-skipped-too-short"] += 1
                    continue
                o = out[i]
                if (ny, nh) != (o[1], o[3]):
                    stats["v-moved"] += 1
                out[i] = (o[0], ny, o[2], nh, o[4], o[5])

    return out, stats
