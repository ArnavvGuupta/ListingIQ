
import time
import requests
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Listing

OVERPASS_URL = "https://overpass.private.coffee/api/interpreter"

QUERY = """
[out:json][timeout:90];
area["name"="Delhi"]["boundary"="administrative"]["admin_level"="4"]->.searchArea;
(
  nwr(area.searchArea)["name"]["shop"];
  nwr(area.searchArea)["name"]["amenity"];
  nwr(area.searchArea)["name"]["office"];
  nwr(area.searchArea)["name"]["craft"];
  nwr(area.searchArea)["name"]["tourism"];
);
out center tags 1200;
"""

HEADERS = {
    "User-Agent": "BusinessListingsDashboard/1.0 (educational project; contact: arnavgupta140905@gmail.cpm)"
}


def get_category(tags):
    for key in ("shop", "amenity", "office", "craft", "tourism"):
        if tags.get(key):
            return tags[key].replace("_", " ").title()
    return "Other"


def get_address(tags):
    parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:postcode"),
    ]
    return ", ".join(part for part in parts if part) or None


def collect_listings():
    print("Requesting Delhi business data from OpenStreetMap...")

    response = requests.post(
        OVERPASS_URL,
        data={"data": QUERY},
        headers=HEADERS,
        timeout=120,
    )

    if response.status_code in (429, 406):
        print("Service rate limit reached. Wait at least 30 seconds before retrying.")
        return []
    if not response.ok:
        print("HTTP status:", response.status_code)
        print("Server response:", response.text[:1000])
        return []

    data = response.json()
    elements = data.get("elements", [])

    records = []
    seen = set()

    for element in elements:
        tags = element.get("tags", {})
        name = tags.get("name", "").strip()

        if not name:
            continue

        address = get_address(tags)
        key = (name.casefold(), (address or "").casefold())

        if key in seen:
            continue
        seen.add(key)

        records.append({
            "business_name": name[:255],
            "category": get_category(tags)[:100],
            "city": "Delhi",
            "address": address,
            "phone": (
                tags.get("phone")
                or tags.get("contact:phone")
                or None
            ),
            "source": "OpenStreetMap",
        })

    return records


def main():
    db: Session = SessionLocal()

    try:
        records = collect_listings()
        if not records:
            print("No records collected. Check the service response and try later.")
            return

        inserted = 0

        for record in records:
            # Avoid inserting an existing listing with the same name and address.
            existing = db.query(Listing.id).filter(
                Listing.business_name == record["business_name"],
                Listing.address == record["address"],
                Listing.source == record["source"],
            ).first()

            if existing:
                continue

            db.add(Listing(**record))
            inserted += 1

        db.commit()
        print(f"Collected {len(records)} unique source records.")
        print(f"Inserted {inserted} new listings into MySQL.")

    except Exception as exc:
        db.rollback()
        print(f"Collection failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
