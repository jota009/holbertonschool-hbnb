from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner: User):
        super().__init__()
        # Validate basics
        if not title or len(title) > 100:
            raise ValueError("title is required (<100 chars)")
        if price is None or price <= 0:
            raise ValueError("price must be positive")
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        if not (-90.0 <= latitude <= 90.0) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("latitude/longitude out of bounds")


        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        # Relationships
        self.reviews = []
        self.amenities = []


    def add_review(self, review):
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected a Review")
        self.reviews.append(review)


    def add_amenity(self, amenity):
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected an Amenity")
        self.amenities.append(amenity)


