"""world-atlas(ISC) land-50m → SVG path (단순 등장방형, x = 경도·cos35°, y = -위도)."""
import json, math
from pathlib import Path

K = math.cos(math.radians(35))
GEO = Path(__file__).parent / "geo" / "land50.json"


def P(lon, lat):
    return lon * K, -lat


def land_path(lon0=-30, lon1=160, lat0=-5, lat1=75):
    tj = json.loads(GEO.read_text(encoding="utf-8"))
    sx, sy = tj["transform"]["scale"]; tx, ty = tj["transform"]["translate"]
    arcs = []
    for a in tj["arcs"]:
        x = y = 0; pts = []
        for dx, dy in a:
            x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            pts = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(pts if not out else pts[1:])
        return out

    d = []
    for g in tj["objects"]["land"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in polys:
            for r in poly:
                pts = ring(r)
                if min(la for _, la in pts) < -55:
                    continue
                if max(lo for lo, _ in pts) - min(lo for lo, _ in pts) > 180:
                    pts = [(lo + 360 if lo < -150 else lo, la) for lo, la in pts]
                if not any(lon0 <= lo <= lon1 and lat0 <= la <= lat1 for lo, la in pts):
                    continue
                if len(pts) < 4:
                    continue
                xy = [P(lo, la) for lo, la in pts]
                # 너무 촘촘한 점 줄이기
                keep = [xy[0]]
                for p in xy[1:]:
                    if abs(p[0] - keep[-1][0]) + abs(p[1] - keep[-1][1]) > 0.04:
                        keep.append(p)
                if len(keep) < 3:
                    continue
                d.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in keep) + "Z")
    return "".join(d)


if __name__ == "__main__":
    s = land_path(); print(len(s))
