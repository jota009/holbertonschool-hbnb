from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    # repositories for each source
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods, Create and Read
    def create_user(self, user_data):
        """
        Create a new User, hash its password, persist it, and return it"""
        # Pull out raw password
        raw_pwd = user_data.get('password')

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        # Hash & store pawd
        user.hash_password(raw_pwd)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a User by their UUID.
        Returns None if not found.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a User by their email address.
        Returns None if not found.
        """
        return self.user_repo.get_by_attribute('email', email)

    # ----List ALL USERS----
    def get_all_users(self):
        """
        Returns a list of all User instances.
        """
        return self.user_repo.get_all()

    # ----Update User----
    def update_user(self, user_id, user_data):
        """
        Find a User by ID, apply updates, and return the updated User.
        Returns None if the user does not exist.
        """
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # ----Amenity methods----
    def create_amenity(self, amenity_data):
        """
        Create a new Amenity instance from the provided dict,
        add it to the repository, and return the Amenity.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an Amenity by its UUID.
        Returns None if not found.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Return a list of all Amenity instances.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Find an Amenity by ID, apply updates, and return the updated Amenity.
        Returns None if the amenity does not exist.
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # ----Place methods----
    def create_place(self, data):
        """
        - Validate owner_id & amenities list
        - Instantiate Place(owner=User, **attrs)
        - Attach amenities via place.add_amenity(...)
        - Store and run
        """
        owner_id = data.pop('owner_id')
        amenity_ids = data.pop('amenities', [])

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # Validate numeric fields (Place constructor also covers this)
        place = Place(owner=owner, **data)

        for aid in amenity_ids:
            amen = self.get_amenity(aid)
            if not amen:
                raise ValueError(f"Amenity {aid} not found")
            place.add_amenity(amen)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None
        place.update(data)
        return place

# ----Review methods----
    def create_review(self, data):
        """
        - Validate user_id & place_id
        - Instantiate Review(text, rating, place, user)
        - Attach it to place via place.add_review(...)
        - Store and return
        """
        user = self.get_user(data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(data['place_id'])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=data['text'],
            rating=data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Return a Review or None."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return list of all Review instances."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Returns all reviews linked to a given place.
        Raise ValueError if place not found.
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, data):
        """Find a Review by ID, apply update(), return it or None."""
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(data)
        return review

    def delete_review(self, review_id):
        """
        Delete a Review by ID.
        Also remove it from its place.reviews list.
        Returns True if deleted, False otherwise.
        """
        review = self.get_review(review_id)
        if not review:
            return False
        # Remove from place
        review.place.reviews.remove(review)
        # Remove from repo
        self.review_repo.delete(review_id)
        return True
