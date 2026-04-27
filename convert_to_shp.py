import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPoint, Point, MultiPolygon
from shapely.ops import unary_union
import sys

csv_path = sys.argv[1]
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} points across {df['scan_num'].nunique()} scans")

# --- Option A: One polygon per scan ---
polygons = []
for scan_num, group in df.groupby('scan_num'):
    points = list(zip(group['x_m'], group['y_m']))
    if len(points) < 3:
        continue
    hull = MultiPoint(points).convex_hull
    # convex_hull can return Point or LineString if points are collinear
    if hull.geom_type == 'Polygon' and not hull.is_empty:
        polygons.append({'scan_num': int(scan_num), 'geometry': hull})
    else:
        print(f"  Scan {scan_num}: hull is {hull.geom_type}, skipping")

print(f"Valid polygons: {len(polygons)}")

if polygons:
    gdf = gpd.GeoDataFrame(
        polygons,
        geometry=[p['geometry'] for p in polygons],
        crs="EPSG:4326"
    )
    gdf.to_file("scan_hulls.shp")
    print("Saved scan_hulls.shp")

# --- Option B: Single merged polygon ---
# Extract only polygons from the union result
merged = unary_union([p['geometry'] for p in polygons]) if polygons else None

if merged is not None:
    # Force to MultiPolygon — shapefiles don't support GeometryCollection
    if merged.geom_type == 'Polygon':
        merged = MultiPolygon([merged])
    elif merged.geom_type == 'GeometryCollection':
        # Extract only polygon parts
        parts = [g for g in merged.geoms if g.geom_type in ('Polygon', 'MultiPolygon')]
        merged = MultiPolygon(parts) if parts else None

if merged is not None:
    gdf_merged = gpd.GeoDataFrame(
        [{'label': 'room'}],
        geometry=[merged],
        crs="EPSG:4326"
    )
    gdf_merged.to_file("room_outline.shp")
    print("Saved room_outline.shp")
else:
    print("No valid merged polygon — not enough data")

# --- Option C: Raw point cloud ---
gdf_points = gpd.GeoDataFrame(
    df,
    geometry=[Point(x, y) for x, y in zip(df['x_m'], df['y_m'])],
    crs="EPSG:4326"
)
gdf_points.to_file("scan_points.shp")
print("Saved scan_points.shp")
