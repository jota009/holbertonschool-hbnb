# app/persistence/review_repository.py
from app.models.review import Review
from .sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.orm import joinedload


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_by_place_id(self, place_id):
        # Acquire the active session; adapt if your base class differs
        session = getattr(self, 'session', None)
        if session is None:
            # fallback if base class doesn't expose session attribute
            from app.extensions import db
            session = db.session

        return (
            session.query(Review)
                   .options(joinedload(Review.user))
                   .filter(Review.place_id == place_id)
                   .all()
        )
