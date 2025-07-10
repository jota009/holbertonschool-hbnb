from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
# from app.models.place import Place
# from app.models.amenity import Amenity
# from app.models.review import Review


class HBnBFacade:
    # repositories for each source
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        # self.place_repo = InMemoryRepository()
        # self.review_repo = InMemoryRepository()
        # self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """user_data: dict with first_name, last_name, email, password (hashed already), is_admin"""
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, updates: dict):
        """
        updates: dict of fields to change (first_name, last_name, email, password_hash, is_admin)
        """
        return self.user_repo.update(user_id, updates)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

#     # ----Amenity methods----
#     def create_amenity(self, amenity_data):
#         """
#         Create a new Amenity instance from the provided dict,
#         add it to the repository, and return the Amenity.
#         """
#         amenity = Amenity(**amenity_data)
#         self.amenity_repo.add(amenity)
#         return amenity

#     def get_amenity(self, amenity_id):
#         """
#         Retrieve an Amenity by its UUID.
#         Returns None if not found.
#         """
#         return self.amenity_repo.get(amenity_id)

#     def get_all_amenities(self):
#         """
#         Return a list of all Amenity instances.
#         """
#         return self.amenity_repo.get_all()

#     def update_amenity(self, amenity_id, amenity_data):
#         """
#         Find an Amenity by ID, apply updates, and return the updated Amenity.
#         Returns None if the amenity does not exist.
#         """
#         amenity = self.get_amenity(amenity_id)
#         if not amenity:
#             return None
#         amenity.update(amenity_data)
#         return amenity

#     # ----Place methods----
#     def create_place(self, data):
#         """
#         - Validate owner_id & amenities list
#         - Instantiate Place(owner=User, **attrs)
#         - Attach amenities via place.add_amenity(...)
#         - Store and run
#         """
#         owner_id = data.pop('owner_id')
#         amenity_ids = data.pop('amenities', [])

#         owner = self.get_user(owner_id)
#         if not owner:
#             raise ValueError("Owner not found")

#         # Validate numeric fields (Place constructor also covers this)
#         place = Place(owner=owner, **data)

#         for aid in amenity_ids:
#             amen = self.get_amenity(aid)
#             if not amen:
#                 raise ValueError(f"Amenity {aid} not found")
#             place.add_amenity(amen)

#         self.place_repo.add(place)
#         return place

#     def get_place(self, place_id):
#         return self.place_repo.get(place_id)

#     def get_all_places(self):
#         return self.place_repo.get_all()

#     def update_place(self, place_id, data):
#         place = self.get_place(place_id)
#         if not place:
#             return None
#         place.update(data)
#         return place

# # ----Review methods----
#     def create_review(self, data):
#         """
#         - Validate user_id & place_id
#         - Instantiate Review(text, rating, place, user)
#         - Attach it to place via place.add_review(...)
#         - Store and return
#         """
#         user = self.get_user(data['user_id'])
#         if not user:
#             raise ValueError("User not found")

#         place = self.get_place(data['place_id'])
#         if not place:
#             raise ValueError("Place not found")

#         review = Review(
#             text=data['text'],
#             rating=data['rating'],
#             place=place,
#             user=user
#         )
#         self.review_repo.add(review)
#         return review

#     def get_review(self, review_id):
#         """Return a Review or None."""
#         return self.review_repo.get(review_id)

#     def get_all_reviews(self):
#         """Return list of all Review instances."""
#         return self.review_repo.get_all()

#     def get_reviews_by_place(self, place_id):
#         """
#         Returns all reviews linked to a given place.
#         Raise ValueError if place not found.
#         """
#         place = self.get_place(place_id)
#         if not place:
#             raise ValueError("Place not found")
#         return place.reviews

#     def update_review(self, review_id, data):
#         """Find a Review by ID, apply update(), return it or None."""
#         review = self.get_review(review_id)
#         if not review:
#             return None
#         review.update(data)
#         return review

#     def delete_review(self, review_id):
#         """
#         Delete a Review by ID.
#         Also remove it from its place.reviews list.
#         Returns True if deleted, False otherwise.
#         """
#         review = self.get_review(review_id)
#         if not review:
#             return False
#         # Remove from place
#         review.place.reviews.remove(review)
#         # Remove from repo
#         self.review_repo.delete(review_id)
#         return True
