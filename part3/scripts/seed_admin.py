#!/usr/bin/env python3
import os, sys

# insert the project root (one level up from scripts/) onto the path
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)


from app import create_app
from app.services import facade


app = create_app()
with app.app_context():
    ADMIN_EMAIL    = "admin@example.com"
    ADMIN_PASSWORD = "SuperSecret123"
    existing = facade.get_user_by_email(ADMIN_EMAIL)
    if existing:
        print("Admin already exists:", existing.id)
    else:
        u = facade.create_user({
            "first_name": "First",
            "last_name":  "Admin",
            "email":      ADMIN_EMAIL,
            "password":   ADMIN_PASSWORD,
            "is_admin":   True
        })
        print("Created admin:", u.id)
