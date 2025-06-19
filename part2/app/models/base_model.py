import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        # Generate a string UUID
        self.id = str(uuid.uuid4())
        # Record creation time
        self.created_at = datetime.now()
        # Initialize updated_at
        self.updated_at = datetime.now()

    def save(self):
        """Call whenever you change this object."""
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """
        Given a dict of {attr_name: new_value}, set each valid attribute,
        the update the timestamp.
        """
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, key, val)
        self.save()
