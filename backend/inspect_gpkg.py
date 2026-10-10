
from pathlib import Path
import sqlite3

DATA_DIR = Path(r"D:\technical_asessment\backend\venv\osm-data\extracted\Delhi_Business_Listings.geojson")
files = list(DATA_DIR.rglob("*.gpkg"))

if not files:
    raise FileNotFoundError(
        f"No .gpkg file found under {DATA_DIR}. "
        "Check that you extracted the ZIP."
    )

for gpkg in files:
    print(f"\nFILE: {gpkg}")
    print(f"SIZE: {gpkg.stat().st_size / (1024 * 1024):.1f} MB")

    with sqlite3.connect(gpkg) as conn:
        contents = conn.execute(
            """
            SELECT table_name, data_type
            FROM gpkg_contents
            ORDER BY table_name
            """
        ).fetchall()

        print("\nGeoPackage tables:")
        for table_name, data_type in contents:
            print(f"\n--- {table_name} ({data_type}) ---")

            # Table names come from the local GeoPackage metadata.
            safe_name = table_name.replace('"', '""')
            columns = conn.execute(
                f'PRAGMA table_info("{safe_name}")'
            ).fetchall()

            print("Columns:", [col[1] for col in columns])

            column_names = {col[1].lower() for col in columns}
            if "name" in column_names:
                sample = conn.execute(
                    f'SELECT * FROM "{safe_name}" '
                    'WHERE "name" IS NOT NULL LIMIT 3'
                ).fetchall()
                print("Sample named records:", len(sample))
