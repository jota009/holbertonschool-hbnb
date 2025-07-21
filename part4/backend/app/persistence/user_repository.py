from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str) -> User | None:
        """Look up a user by their email address (lowercased)."""
        return self.model.query.filter_by(email=email.lower()).first()
