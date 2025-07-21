import pytest
from app.models.user import User

def test_user_creation_defaults_and_attrs():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    # default is_admin
    assert user.is_admin is False
    # UUID and timestamps
    assert isinstance(user.id, str) and len(user.id) > 0
    assert user.created_at <= user.updated_at

@pytest.mark.parametrize("first,last,email", [
    ("", "Doe", "a@b.com"),             # missing first name
    ("A"*51, "Doe", "a@b.com"),         # first name too long
    ("Jane", "", "a@b.com"),            # missing last name
    ("Jane", "B"*51, "a@b.com"),        # last name too long
    ("Jane", "Doe", "invalid-email"),   # bad email format
])
def test_user_invalid_inputs_raise(first, last, email):
    with pytest.raises(ValueError):
        User(first_name=first, last_name=last, email=email)
