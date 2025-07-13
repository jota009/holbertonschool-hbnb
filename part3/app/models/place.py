from app.extensions import db
from .base_model import BaseModel


# association table for Place -> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,        nullable=True)
    price       = db.Column(db.Float,       nullable=False)
    latitude    = db.Column(db.Float,       nullable=False)
    longitude   = db.Column(db.Float,       nullable=False)

    # one-to-many: User -> Place
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship(
        'User',
        backref=db.backref('places', lazy='select'),
        lazy='joined'
    )

    # one-to-many: Place -> Review
    reviews = db.relationship(
        'Review',
        backref='place',
        lazy='select',
        cascade='all, delete-orphan'
    )

    # many-to-many: Place ↔ Amenity
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        backref=db.backref('places', lazy='select'),
        lazy='subquery'
    )
