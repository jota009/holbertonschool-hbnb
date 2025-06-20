# tests/model_tests/test_review.py

import pytest
from app.models.user   import User
from app.models.place  import Place
from app.models.review import Review

def test_review_creation_valid():
    """A Review should be created with correct attributes."""
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    place = Place(
        title="Test Place",
        description="A lovely spot",
        price=50.0,
        latitude=10.0,
        longitude=20.0,
        owner=user
    )

    review = Review(text="Great stay!", rating=4, place=place, user=user)
    assert review.text == "Great stay!"
    assert review.rating == 4
    assert review.place is place
    assert review.user is user
    assert isinstance(review.id, str) and len(review.id) > 0

def test_review_invalid_inputs():
    """Empty text or out‐of‐range ratings should raise ValueError."""
    user = User(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
    place = Place(
        title="Cozy Cottage",
        description="Quiet and comfortable",
        price=75.0,
        latitude=-45.0,
        longitude=60.0,
        owner=user
    )

    # missing text
    with pytest.raises(ValueError):
        Review(text="", rating=3, place=place, user=user)
    # rating below 1
    with pytest.raises(ValueError):
        Review(text="OK", rating=0, place=place, user=user)
    # rating above 5
    with pytest.raises(ValueError):
        Review(text="OK", rating=6, place=place, user=user)
