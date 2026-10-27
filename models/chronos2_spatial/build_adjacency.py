"""Write adjacency.json (location -> bordering locations) from a geojson whose feature ids are locations.

    uv run --with shapely python other_models/chronos2_spatial/build_adjacency.py \
        input/vietnam.geojson
"""

import json
import sys
from pathlib import Path

from shapely.geometry import shape

OUT = Path(__file__).parent / "adjacency.json"

features = json.load(open(sys.argv[1]))["features"]
polygons = {f["id"]: shape(f["geometry"]).buffer(0) for f in features}
# A small buffer so provinces whose borders do not line up exactly still count as touching
adjacency = {
    a: sorted(b for b in polygons if b != a and polygons[a].buffer(0.01).intersects(polygons[b]))
    for a in sorted(polygons)
}
existing = json.loads(OUT.read_text()) if OUT.exists() else {}
OUT.write_text(json.dumps({**existing, **adjacency}, indent=1) + "\n")
print(f"{len(adjacency)} locations, {sum(map(len, adjacency.values())) // 2} borders -> {OUT}")
