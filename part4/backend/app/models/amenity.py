from app.extensions import db
from .base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100),
                     unique=True,
                     nullable=False)
