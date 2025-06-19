import re
from app.models.base_model import BaseModel


EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin=False):
        super().__init__
        # Basic validation
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required (≤50 chars)")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required (≤50 chars)")
        if not EMAIL_REGEX.match(email):
            raise ValueError("Invalid email format")


        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.is_admin = bool(is_admin)
