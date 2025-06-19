🏗️ Business Logic Layer

The app/models/ directory defines HBnB’s core domain entities. Each class inherits from BaseModel, which provides:

🔑 UUID id: Globally unique identifier

⏱️ created_at & updated_at: Track when objects are created and modified

💾 save() & update(data): Update timestamps and bulk-apply attribute changes

👤 User

Attributes:

Field

Type

Constraints

first_name

String

Required, ≤50 characters

last_name

String

Required, ≤50 characters

email

String

Required, unique, valid

is_admin

Boolean

Defaults to False

from app.models.user import User

user = User(
  first_name="Jane",
  last_name="Doe",
  email="jane.doe@example.com"
)
print(user.id, user.email)

🏠 Place

Attributes & Relations:

Field

Type

Constraints

title

String

Required, ≤100 characters

description

String

Optional

price

Float

Required, > 0

latitude

Float

−90.0 to 90.0

longitude

Float

−180.0 to 180.0

owner

User

Must be a valid User instance

Relationships:

One-to-many with Review via add_review()

Many-to-many with Amenity via add_amenity()

from app.models.place import Place

place = Place(
  title="Cozy Loft",
  description="Central studio",
  price=75.0,
  latitude=40.72,
  longitude=-74.00,
  owner=user
)
print(place.title, place.owner.email)

⭐ Review

Attributes & Behavior:

Field

Type

Constraints

text

String

Required

rating

Integer

1–5

place

Place

Must be a valid Place instance

user

User

Must be a valid User instance

Automatically links itself to place.reviews on creation

Prevents owners from reviewing their own places

from app.models.review import Review

review = Review(
  text="Amazing stay!",
  rating=5,
  place=place,
  user=user
)
print(len(place.reviews))  # 1

🛎️ Amenity

Attributes:

Field

Type

Constraints

name

String

Required, ≤50 characters

Linked to places via place.add_amenity()

from app.models.amenity import Amenity

wifi = Amenity("Wi-Fi")
place.add_amenity(wifi)
print([a.name for a in place.amenities])

🚀 Running the Tests

Activate your virtualenv and install dependencies:

pip install -r requirements.txt pytest

From the project root, run:

pytest

All model tests should pass before moving to the API layer.

This section covers the Business Logic layer. For full technical documentation, including UML diagrams and API specs, see the main README.md in the project root.

