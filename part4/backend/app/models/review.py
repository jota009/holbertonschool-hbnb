from app.extensions import db
from .base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text     = db.Column(db.Text,    nullable=False)
    rating   = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36),
                         db.ForeignKey('places.id'),
                         nullable=False)
    user_id  = db.Column(db.String(36),
                         db.ForeignKey('users.id'),
                         nullable=False)


    # one-to-many: User → Review (gives User.reviews)
    user = db.relationship(
        'User',
        backref=db.backref('reviews', lazy='select', cascade='all, delete-orphan'),
        lazy='joined'
    )
