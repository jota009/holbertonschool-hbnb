#!/usr/bin/env python3
import os, sys

# insert the project root (one level up from scripts/) onto the path
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)


from app import create_app
from app.services import facade


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
            "first_name": "First",
            "last_name":  "Admin",
            "email":      ADMIN_EMAIL,
            "password":   ADMIN_PASSWORD,
            "is_admin":   True
        })
        print("Created admin:", admin.id)

    # 2) Seed some places if none exist
    existing_places = facade.get_all_places()  # returns a list of Place objects
    if existing_places:
        print(f"{len(existing_places)} place(s) already exist, skipping place seeding.")
    else:
        sample_places = [
            {
                "title":       "Lake House Deluxe",
                "description": "A beautiful lakeside cabin with all amenities.",
                "price":       80,
                "latitude":    45.0,
                "longitude":  -75.0,
                "owner_id":    str(admin.id)
            },
            {
                "title":       "Cozy Cabin",
                "description": "A rustic little cabin in the woods.",
                "price":       100,
                "latitude":    34.1,
                "longitude":  -118.2,
                "owner_id":    str(admin.id)
            },
            {
                "title":       "Modern Apartment",
                "description": "City‑center flat with skyline views.",
                "price":       200,
                "latitude":    40.7,
                "longitude":  -74.0,
                "owner_id":    str(admin.id)
            }
        ]
        for p in sample_places:
            place = facade.create_place(p)
            print("Created place:", place.id, p["title"])

        print("Sample places seeded!")

print("Seeding complete.")
