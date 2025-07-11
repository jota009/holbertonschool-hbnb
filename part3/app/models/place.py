from app.extensions import db
from .base_model import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,        nullable=True)
    price       = db.Column(db.Float,       nullable=False)
    latitude    = db.Column(db.Float,       nullable=False)
    longitude   = db.Column(db.Float,       nullable=False)

    # foreign key to users.id
    owner_id    = db.Column(db.String(36),
                            db.ForeignKey('users.id'),
                            nullable=False)
