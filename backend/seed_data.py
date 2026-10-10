
import random

from sqlalchemy.orm import Session

from database import SessionLocal
from models import Listing

random.seed(42)

cities = {
    "Delhi": ["Connaught Place", "Rohini", "Dwarka", "Karol Bagh"],
    "Mumbai": ["Andheri", "Bandra", "Dadar", "Powai"],
    "Bengaluru": ["Indiranagar", "Whitefield", "Koramangala", "Jayanagar"],
    "Pune": ["Baner", "Hinjawadi", "Kothrud", "Viman Nagar"],
    "Jaipur": ["Malviya Nagar", "Vaishali Nagar", "Mansarovar", "C-Scheme"],
}

categories = [
    "Restaurant",
    "Hospital",
    "Gym",
    "Salon",
    "Car Repair",
]

# These are synthetic source labels, not actual scraped sources.
sources = ["Sample Dataset", "Sample Dataset", "Sample Dataset"]

prefixes = [
    "City", "Prime", "Green", "Urban", "Royal",
    "Smart", "Bright", "Metro", "Elite", "Modern",
]

suffixes = {
    "Restaurant": ["Kitchen", "Restaurant", "Cafe"],
    "Hospital": ["Clinic", "Healthcare Centre", "Medical Centre"],
    "Gym": ["Fitness Hub", "Gym", "Fitness Centre"],
    "Salon": ["Salon", "Beauty Studio", "Style Lounge"],
    "Car Repair": ["Auto Care", "Car Service", "Garage"],
}


def generate_listings(total=500):
    records = []

    for i in range(1, total + 1):
        city = random.choice(list(cities.keys()))
        area = random.choice(cities[city])
        category = random.choice(categories)

        name = (
            f"{random.choice(prefixes)} "
            f"{random.choice(suffixes[category])} {i:04d}"
        )

        records.append(
            {
                "business_name": name,
                "category": category,
                "city": city,
                "address": f"{area}, {city}",
                "phone": None,
                "source": "Synthetic Sample",
            }
        )

    return records


def main():
    db: Session = SessionLocal()

    try:
        records = generate_listings(500)

        db.add_all([Listing(**record) for record in records])
        db.commit()

        print(f"Successfully inserted {len(records)} synthetic listings.")

    except Exception as exc:
        db.rollback()
        print(f"Failed to insert listings: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
