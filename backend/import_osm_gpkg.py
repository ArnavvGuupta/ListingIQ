
from pathlib import Path
import re
import sqlite3

from database import SessionLocal
from models import Listing


GPKG = Path(
    r"D:\technical_asessment\backend\venv\osm-data\extracted"
    r"\Delhi_Business_Listings.geojson\Delhi_Business_Listings.geojson"
    r"\planet_76.238,27.904_78.223,29.214.gpkg"
)

SOURCE = "OpenStreetMap"
BATCH_SIZE = 250

CATEGORY_TAGS = [
    "amenity", "shop", "office", "craft", "healthcare",
    "tourism", "leisure", "sport", "industrial",
]

NAME_KEYS = ["name", "name:en", "official_name"]
CITY_KEYS = [
    "addr:city", "addr:town", "addr:municipality",
    "addr:village",
]
PHONE_KEYS = ["phone", "contact:phone", "mobile", "contact:mobile"]
ADDRESS_KEYS = [
    "addr:housenumber", "addr:street", "addr:suburb",
    "addr:neighbourhood", "addr:postcode",
]

# Parse the common OSM hstore representation in other_tags.
TAG_PATTERN = re.compile(
    r'"((?:[^"\\]|\\.)+)"\s*=>\s*"((?:[^"\\]|\\.)*)"'
)


def clean(value):
    return re.sub(r"\s+", " ", str(value)).strip() if value is not None else ""


def parse_tags(row):
    tags = {
        str(key).lower(): clean(row[key])
        for key in row.keys()
        if row[key] is not None
    }

    packed = tags.get("other_tags", "")
    for key, value in TAG_PATTERN.findall(packed):
        key = key.replace('\\"', '"').replace('\\\\', '\\')
        value = value.replace('\\"', '"').replace('\\\\', '\\')
        tags.setdefault(key.lower(), value)

    return tags


def first_value(tags, keys):
    for key in keys:
        value = clean(tags.get(key.lower(), ""))
        if value:
            return value
    return ""


def category_from(tags):
    for key in CATEGORY_TAGS:
        value = clean(tags.get(key, ""))
        if value:
            return value.replace("_", " ").title()
    return ""


def normalized(value):
    return clean(value).casefold()


def main():
    if not GPKG.is_file():
        raise FileNotFoundError(f"GeoPackage not found: {GPKG}")

    db = SessionLocal()
    imported = 0
    skipped = 0
    batch = []
    seen_osm_ids = set()

    try:
        # Make repeated runs idempotent for OSM objects that already exist.
        existing_keys = {
            (
                normalized(row.business_name),
                normalized(row.address or ""),
                normalized(row.city),
            )
            for row in db.query(Listing)
            .filter(Listing.source == SOURCE)
            .all()
        }

        with sqlite3.connect(GPKG) as conn:
            conn.row_factory = sqlite3.Row

            for table in ("points", "multipolygons"):
                print(f"\nScanning layer: {table}")

                cursor = conn.execute(f'SELECT * FROM "{table}"')
                layer_candidates = 0

                for row in cursor:
                    tags = parse_tags(row)
                    name = first_value(tags, NAME_KEYS)
                    category = category_from(tags)

                    # Require a real OSM name and a business-related tag.
                    if not name or not category:
                        continue

                    osm_id = clean(tags.get("osm_id", ""))
                    if osm_id:
                        # The same OSM feature may appear in multiple layers.
                        object_key = (table, osm_id)
                        if object_key in seen_osm_ids:
                            continue
                        seen_osm_ids.add(object_key)

                    city = first_value(tags, CITY_KEYS) or "Delhi NCR"

                    address_parts = []
                    for key in ADDRESS_KEYS:
                        value = clean(tags.get(key, ""))
                        if value and value not in address_parts:
                            address_parts.append(value)

                    address = ", ".join(address_parts) or None
                    phone = first_value(tags, PHONE_KEYS) or None

                    key = (
                        normalized(name),
                        normalized(address or ""),
                        normalized(city),
                    )

                    if key in existing_keys:
                        skipped += 1
                        continue

                    batch.append(
                        Listing(
                            business_name=name[:255],
                            category=category[:100],
                            city=city[:100],
                            address=address,
                            phone=phone[:30] if phone else None,
                            source=SOURCE,
                        )
                    )
                    existing_keys.add(key)
                    layer_candidates += 1

                    if len(batch) >= BATCH_SIZE:
                        db.add_all(batch)
                        db.commit()
                        imported += len(batch)
                        batch.clear()
                        print(f"New records committed: {imported}")

                print(f"New candidates from {table}: {layer_candidates}")

        if batch:
            db.add_all(batch)
            db.commit()
            imported += len(batch)

        total = (
            db.query(Listing)
            .filter(Listing.source == SOURCE)
            .count()
        )

        print("\n========== IMPORT SUMMARY ==========")
        print(f"New records imported: {imported}")
        print(f"Existing matches skipped: {skipped}")
        print(f"Total OpenStreetMap records in MySQL: {total}")

        if total >= 500:
            print("SUCCESS: The database has at least 500 OSM records.")
        else:
            print("TARGET NOT YET MET: fewer than 500 OSM records.")
            print("Inspect the layer candidates and tag fields.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
