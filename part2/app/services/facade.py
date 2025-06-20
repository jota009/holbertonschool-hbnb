from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

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
        Create a new User instance from the provided dict,
        add it to the repository, and return the User.
        """
        user = User(**user_data)
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


    # Other resorce placeholders
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
