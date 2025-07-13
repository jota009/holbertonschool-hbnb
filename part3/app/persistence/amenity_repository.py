# app/persistence/amenity_repository.py
from app.models.amenity import Amenity
from .sqlalchemy_repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
