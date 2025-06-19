from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: Place, user: User):
        # Initialize id, created_at, updated_at
        super().__init__()

        # Validate the review text
        if not text:
            raise ValueError("Review text is required")

        # Validate the rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # Ensure place & user are correct types
        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")

        # Assing attributes
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        # Link this review back to the place
        place.add_review(self)
