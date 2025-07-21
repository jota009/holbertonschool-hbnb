from app.models.amenity import Amenity

def test_amenity_creation_valid():
    amenity = Amenity("Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert isinstance(amenity.id, str) and len(amenity.id) > 0

import pytest
def test_amenity_invalid_name():
    with pytest.raises(ValueError):
        Amenity("")          # missing name
    with pytest.raises(ValueError):
        Amenity("A"*51)      # name too long
