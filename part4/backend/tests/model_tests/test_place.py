import pytest
from app.models.user  import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

@pytest.fixture
def sample_user():
    return User("Alice", "Smith", "alice.smith@example.com")

def test_place_creation_and_attrs(sample_user):
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=sample_user
    )
    assert place.title == "Cozy Apartment"
    assert isinstance(place.price, float) and place.price == 100.0
    assert place.owner is sample_user
    assert place.reviews == []
    assert place.amenities == []

def test_place_invalid_price_and_coords(sample_user):
    with pytest.raises(ValueError):
        Place("T", "", -5, 0, 0, owner=sample_user)
    with pytest.raises(ValueError):
        Place("T", "", 10, 100.0, 0, owner=sample_user)
    with pytest.raises(ValueError):
        Place("T", "", 10, 0.0, -200.0, owner=sample_user)

def test_add_review_and_amenity(sample_user):
    place = Place("P", "", 50, 0, 0, owner=sample_user)
    review = Review("Great!", 5, place=place, user=sample_user)
    assert len(place.reviews) == 1
    assert place.reviews[0] is review

    amenity = Amenity("Wi-Fi")
    place.add_amenity(amenity)
    assert amenity in place.amenities
