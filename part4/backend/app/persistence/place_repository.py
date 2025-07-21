# app/persistence/place_repository.py
from app.models.place import Place
from .sqlalchemy_repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
