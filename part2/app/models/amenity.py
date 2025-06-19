from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__() #serial#, timestamps
        if not name or len(name) > 50:
            raise ValueError("name is required (≤50 chars)")
        self.name = name
