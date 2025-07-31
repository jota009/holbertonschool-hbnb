from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from flask_jwt_extended import get_jwt_identity


from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ── Users ────────────────────────────────────────────────
    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email = user_data['email'].strip().lower(),
            is_admin=user_data.get('is_admin', False)
        )
        user.hash_password(user_data['password'])
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, updates: dict):
        return self.user_repo.update(user_id, updates)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ── Amenities ───────────────────────────────────────────
    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, updates: dict):
        return self.amenity_repo.update(amenity_id, updates)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # ── Places ──────────────────────────────────────────────
    def create_place(self, place_data):
        """
        Create a new place. Expects:
          - title, description, price, latitude, longitude in place_data
          - owner_id in place_data when seeding (optional)
        """
         # pull off any amenity IDs so they don’t get passed blindly into the model
        amenity_ids = place_data.pop('amenities', [])
        # 1) Determine owner: use explicit owner_id for scripts/seed, otherwise JWT identity
        owner_id = place_data.get('owner_id') or get_jwt_identity()
        if not owner_id:
            raise ValueError("Must be authenticated to create a place")

        # 2) Construct Place model
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner_id
        )
        # now attach any pre‐existing amenities by id
        for aid in amenity_ids:
            amen = self.get_amenity(aid)
            if not amen:
                raise ValueError(f"Amenity {aid} not found")
            place.add_amenity(amen)
        # 3) Persist and return
        return self.place_repo.add(place)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, updates: dict):
        return self.place_repo.update(place_id, updates)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ── Reviews ─────────────────────────────────────────────
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        return self.review_repo.add(review)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return self.review_repo.get_by_place_id(place_id)

    def update_review(self, review_id, updates: dict):
        return self.review_repo.update(review_id, updates)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
