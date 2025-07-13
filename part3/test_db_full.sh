#!/usr/bin/env bash
set -euo pipefail

python3 <<'PYCODE'
import sys
from sqlalchemy import inspect
from app import create_app, db
from app.models.user    import User
from app.models.place   import Place
from app.models.amenity import Amenity
from app.models.review  import Review

# 1) Spin up app & reset schema
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    inspector = inspect(db.engine)
    print("Tables:", inspector.get_table_names())

    # 2) Create a User
    u = User(first_name="Test", last_name="User", email="test@example.com")
    u.hash_password("secret")
    db.session.add(u)
    db.session.commit()
    print("  ↳ User OK:", User.query.first().id)

    # 3) Create an Amenity
    a = Amenity(name="Pool")
    db.session.add(a)
    db.session.commit()
    print("  ↳ Amenity OK:", Amenity.query.first().id)

    # 4) Create a Place owned by our User
    p = Place(
      title="Lake House",
      description="Getting away",
      price=123.45,
      latitude=45.0,
      longitude=-75.0,
      owner_id=u.id
    )
    # link our amenity
    p.amenities.append(a)
    db.session.add(p)
    db.session.commit()
    print("  ↳ Place OK:", Place.query.first().id)
    print("      • owner relationship →", Place.query.first().owner.id)
    print("      • amenities →", [am.id for am in p.amenities])

    # 5) Create a Review of that Place by our User
    r = Review(
      text="Loved it!",
      rating=5,
      place_id=p.id,
      user_id=u.id
    )
    db.session.add(r)
    db.session.commit()
    print("  ↳ Review OK:", Review.query.first().id)
    print("      • place.reviews →", [rv.id for rv in p.reviews])
    print("      • user.reviews  →", [rv.id for rv in u.reviews])

# 6) Exit cleanly
sys.exit(0)
PYCODE
