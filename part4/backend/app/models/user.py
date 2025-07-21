import re
from sqlalchemy.orm import validates
from app import db, bcrypt
from app.models.base_model import BaseModel


EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    @validates('first_name', 'last_name')
    def _validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError(f"{key} is required and must be ≤50 characters")
        return value.strip()

    @validates('email')
    def _validate_email(self, key, value):
        value = value.lower().strip()
        if not EMAIL_REGEX.match(value):
            raise ValueError("Invalid email format")
        return value

    def hash_password(self, plain):
        """
        Hash the plaintext password and store it in the model.
        """
        self.password = bcrypt.generate_password_hash(plain).decode('utf-8')

    def verify_password(self, plain):
        """
        Compare a plaintext password against the stored hash.
        """
        return bcrypt.check_password_hash(self.password, plain)
