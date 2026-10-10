
import json
import sys
from pathlib import Path

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Listing

BUSINESS_TAGS = (
    "shop",
    "amenity",
    "office",
    "craft",
    "tourism",
    "healthcare",
    "leisure",
    "club",
    "sport",
)

def get_category(tags):
    for key in BUSINESS_TAGS:
        if tags.get(key):
            return str(tags[key]).replace("_", " ").title()[:100]
    return "Other"


def get_address(tags):
    parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:city"),
        tags.get("addr:postcode"),
    ]
    return ", ".join(str(part) for part in parts if part) or None


def load_features(path):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if data.get("type") != "FeatureCollection":
        raise ValueError("Expected a GeoJSON FeatureCollection.")

    return data.get("features", [])


def main():
    if len(sys.argv) != 2:
        print(
            'Usage: python import_osm_geojson.py '
            '"D:\\data\\your_extract.geojson"'
        )
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.is_file():
        print(f"File not found: {path}")
        sys.exit(1)

    features = load_features(path)
    print(f"Features in downloaded file: {len(features)}")

    records = []
    seen = set()

    for feature in features:
        properties = feature.get("properties") or {}

        # Some exports nest OSM tags inside a "tags" object.
        tags = properties.get("tags", properties)

        if not isinstance(tags, dict):
            continue

        name = tags.get("name") or properties.get("name")
        if not isinstance(name, str) or not name.strip():
            continue

        if not any(tags.get(key) for key in BUSINESS_TAGS):
            continue

        address = get_address(tags)
        name = name.strip()[:255]

        # Keep source features unique without inventing information.
        identity = (
            name.casefold(),
            (address or "").casefold(),
            get_category(tags).casefold(),
        )
        if identity in seen:
            continue
        seen.add(identity)

        records.append({
            "business_name": name,
            "category": get_category(tags),
            "city": (
                tags.get("addr:city")
                or properties.get("addr:city")
                or "Delhi"
            )[:100],
            "address": address,
            "phone": (
                tags.get("phone")
                or tags.get("contact:phone")
                or None
            ),
            "source": "OpenStreetMap",
        })

    print(f"Named business/POI records after filtering: {len(records)}")

    if not records:
        print(
            "No suitable records found. The extract may use a different "
            "GeoJSON property layout. Inspect a feature before importing."
        )
        sys.exit(1)

    db: Session = SessionLocal()
    inserted = 0
    skipped = 0

    try:
        for record in records:
            existing = db.query(Listing.id).filter(
                Listing.business_name == record["business_name"],
                Listing.address == record["address"],
                Listing.source == record["source"],
            ).first()

            if existing:
                skipped += 1
                continue

            db.add(Listing(**record))
            inserted += 1

            # Commit in batches to avoid holding a huge transaction.
            if inserted % 100 == 0:
                db.commit()
                print(f"Inserted so far: {inserted}")

        db.commit()
        print("\nImport completed.")
        print(f"New records inserted: {inserted}")
        print(f"Existing records skipped: {skipped}")
        print(
            "Note: records are OpenStreetMap points of interest; "
            "not every one is necessarily a commercial business."
        )

    except Exception as exc:
        db.rollback()
        print(f"Import failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
