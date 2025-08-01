#!/usr/bin/env python3
import os, sys

# insert the project root (one level up from scripts/) onto the path
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from app import create_app
from app.services import facade


def run_seed():
    """Seed the database with an admin user, amenities, and sample places."""
    app = create_app()
    with app.app_context():
        # 1) Seed admin user if missing
        ADMIN_EMAIL    = "admin@example.com"
        ADMIN_PASSWORD = "SuperSecret123"
        admin = facade.get_user_by_email(ADMIN_EMAIL)
        if admin:
            print("Admin already exists:", admin.id)
        else:
            admin = facade.create_user({
                "first_name": "Jay",
                "last_name":  "Ramos",
                "email":      ADMIN_EMAIL,
                "password":   ADMIN_PASSWORD,
                "is_admin":   True
            })
            print("Created admin:", admin.id)

        # 1b) Seed a non‑admin reviewer
        REV_EMAIL    = "rev@example.com"
        REV_PASSWORD = "RevPass123"
        reviewer = facade.get_user_by_email(REV_EMAIL)
        if reviewer:
            print("Reviewer already exists:", reviewer.id)
        else:
            reviewer = facade.create_user({
                "first_name": "John",
                "last_name":  "Cena",
                "email":      REV_EMAIL,
                "password":   REV_PASSWORD,
                # is_admin defaults to False
            })
            print("Created reviewer:", reviewer.id)

        # 2) Seed amenities if none exist
        existing_aments = facade.get_all_amenities()
        if not existing_aments:
            for name in ['WiFi', 'Pool', 'Air Conditioning', 'Kitchen', 'Free Parking']:
                amen = facade.create_amenity({'name': name})
                print('Created amenity:', amen.id, amen.name)
        else:
            print(f"{len(existing_aments)} amenity(ies) already exist, skipping.")

        # collect all amenity IDs
        amen_ids = [a.id for a in facade.get_all_amenities()]

        # 3) Seed sample places if none exist
        existing_places = facade.get_all_places()
        if not existing_places:
            sample_places = [
                {
                    "title":       "Lake House Deluxe",
                    "description": "A beautiful lakeside cabin with all amenities.",
                    "price":       80,
                    "latitude":    45.0,
                    "longitude":   -75.0,
                    "owner_id":    admin.id,
                    "amenities":   amen_ids  # attach all amenities
                },
                {
                    "title":       "Cozy Cabin",
                    "description": "A rustic little cabin in the woods.",
                    "price":       100,
                    "latitude":    34.1,
                    "longitude":   -118.2,
                    "owner_id":    admin.id,
                    "amenities":   amen_ids[:3]  # example subset
                },
                {
                    "title":       "Modern Apartment",
                    "description": "City‑center flat with skyline views.",
                    "price":       200,
                    "latitude":    40.7,
                    "longitude":   -74.0,
                    "owner_id":    admin.id,
                    "amenities":   amen_ids[1:]
                },
                {
                    "title":       "Beachfront Bungalow",
                    "description": "Cozy bungalow steps from the sand.",
                    "price":       150,
                    "latitude":    26.1,
                    "longitude":   -80.1,
                    "owner_id":    admin.id,
                    "amenities":   amen_ids[::2]
                },
                {
                    "title":       "Mountain Retreat",
                    "description": "Secluded cabin with mountain views and a hot tub.",
                    "price":       220,
                    "latitude":    39.7,
                    "longitude":   -105.3,
                    "owner_id":    admin.id,
                    "amenities":   amen_ids[-2:]
                }
            ]
            for p in sample_places:
                place = facade.create_place(p)
                print("Created place:", place.id, p["title"])
        else:
            print(f"{len(existing_places)} place(s) already exist, skipping place seeding.")

        print("🎉 Seeding complete.")


if __name__ == '__main__':
    run_seed()
