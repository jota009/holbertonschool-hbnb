# 🏗️ Business Logic Layer

The `app/models/` directory defines the core domain entities for HBnB. Each class inherits from **BaseModel**, which provides:

* 🔑 \*\*UUID \*\*\`\`: globally unique identifier
* 🕒 **Timestamps**: `created_at` & `updated_at`
* 🛠️ **Methods**:

  * 💾 `save()` — update `updated_at`
  * ⚙️ `update(data: dict)` — bulk-update attributes and call `save()`

---

## 🌟 BaseModel

**File:** `app/models/base_model.py`

```python
import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """Bulk-update valid attributes then update timestamp."""
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, key, val)
        self.save()
```

---

## 🚀 API Endpoints

All endpoints are rooted at `/api/v1` and return JSON. Status codes follow REST conventions:

* **200 OK**
* **201 Created**
* **400 Bad Request**
* **404 Not Found**
* **204 No Content**

### 👤 Users

* `GET /api/v1/users`
  List all users.

* `GET /api/v1/users/<user_id>`
  Retrieve a single user.

* `POST /api/v1/users`
  Create a new user.
  Body parameters: `email`, `password`.

* `PUT /api/v1/users/<user_id>`
  Update user attributes.

* `DELETE /api/v1/users/<user_id>`
  Delete a user.

### 🏠 Places

* `GET /api/v1/places`
  List all places.

* `GET /api/v1/places/<place_id>`
  Retrieve a single place.

* `POST /api/v1/cities/<city_id>/places`
  Create a place in a city.

* `PUT /api/v1/places/<place_id>`
  Update place attributes.

* `DELETE /api/v1/places/<place_id>`
  Delete a place.

### 📝 Reviews

* `GET /api/v1/places/<place_id>/reviews`
  List reviews for a place.

* `GET /api/v1/reviews/<review_id>`
  Retrieve a single review.

* `POST /api/v1/places/<place_id>/reviews`
  Create a review.
  Body parameters: `user_id`, `text`.

* `PUT /api/v1/reviews/<review_id>`
  Update review content.

* `DELETE /api/v1/reviews/<review_id>`
  Delete a review.

### 🛠️ Amenities

* `GET /api/v1/amenities`
  List all amenities.

* `GET /api/v1/amenities/<amenity_id>`
  Retrieve a single amenity.

* `POST /api/v1/amenities`
  Create a new amenity.
  Body parameter: `name`.

* `PUT /api/v1/amenities/<amenity_id>`
  Update amenity name.

* `DELETE /api/v1/amenities/<amenity_id>`
  Delete an amenity.

---

> *Short, precise, and ready for VSCode!*

---

## 🖋️ Author

* **Name**: Josniel Ramos
* **Affiliation**: Holberton School
* **GitHub**: [https://github.com/jota009](https://github.com/jota009)
