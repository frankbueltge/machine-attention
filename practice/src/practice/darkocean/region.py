"""The V0 region: the Baltic Sea as a fixed grid of half-degree bins.

The grid is deliberately dumb: cells are geometric bins over a bounding box,
not sea masks — a bin on the Swedish mainland simply never collects
positions or radar passes worth speaking of. Keeping the grid free of any
coastline dataset keeps every derivation reproducible from nothing but this
file, and honest about what a cell is: a bin, not a body of water.

Coordinates are WGS84 lon/lat. Cell ids name the bin's south-west corner.
"""

from __future__ import annotations

LON0, LON1 = 9.0, 30.0
LAT0, LAT1 = 53.5, 66.0
CELL = 0.5

REGION_WKT = "POLYGON((9 53.5,30 53.5,30 66,9 66,9 53.5))"


def cell_id(lon: float, lat: float) -> str | None:
    """The bin a position falls into, or None outside the region."""
    if not (LON0 <= lon < LON1 and LAT0 <= lat < LAT1):
        return None
    corner_lon = LON0 + int((lon - LON0) / CELL) * CELL
    corner_lat = LAT0 + int((lat - LAT0) / CELL) * CELL
    return f"E{corner_lon:.1f}_N{corner_lat:.1f}"


def cells() -> list[tuple[str, float, float]]:
    """(id, center_lon, center_lat) for every bin, west→east then south→north."""
    out = []
    lat = LAT0
    while lat < LAT1 - 1e-9:
        lon = LON0
        while lon < LON1 - 1e-9:
            out.append((f"E{lon:.1f}_N{lat:.1f}", lon + CELL / 2, lat + CELL / 2))
            lon += CELL
        lat += CELL
    return out


def point_in_ring(lon: float, lat: float, ring: list) -> bool:
    """Ray casting against one closed ring of [lon, lat] pairs."""
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat) and \
                lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def outer_rings(geojson: dict | None) -> list[list]:
    """Outer rings of a GeoJSON Polygon/MultiPolygon; holes are ignored —
    a radar footprint with a hole is not something Sentinel-1 produces."""
    if not geojson:
        return []
    kind = geojson.get("type")
    coords = geojson.get("coordinates") or []
    if kind == "Polygon":
        return [coords[0]] if coords else []
    if kind == "MultiPolygon":
        return [poly[0] for poly in coords if poly]
    return []


def covered_cells(geojson: dict | None) -> list[str]:
    """Every bin whose center lies inside the footprint. Center-in-polygon is
    the whole criterion — crude at edges, but symmetric, stateless and easy
    to re-derive; the verifier recomputes it independently."""
    rings = outer_rings(geojson)
    if not rings:
        return []
    boxed = []
    for ring in rings:
        lons = [p[0] for p in ring]
        lats = [p[1] for p in ring]
        boxed.append((min(lons), max(lons), min(lats), max(lats), ring))
    covered = []
    for cid, clon, clat in cells():
        for lon0, lon1, lat0, lat1, ring in boxed:
            if lon0 <= clon <= lon1 and lat0 <= clat <= lat1 \
                    and point_in_ring(clon, clat, ring):
                covered.append(cid)
                break
    return covered
