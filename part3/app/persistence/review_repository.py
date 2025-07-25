# app/persistence/review_repository.py
from app.models.review import Review
from .sqlalchemy_repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
