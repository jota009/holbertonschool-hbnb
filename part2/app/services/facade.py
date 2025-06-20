from app.persistence.repository import InMemoryRepository
from app.models.user import User


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


    # Other resorce placeholders
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
