# test_user_model.py

import pytest
from app.models.user import User
from app.extensions import bcrypt
import re

def test_hash_and_verify_password():
    u = User("Jane", "Doe", "jane.doe@example.com")
    u.hash_password("MySecret123")
    # After hashing, password is a non‐empty string
    assert isinstance(u.password, str) and u.password != ""
    # verify_password should return True on correct, False on wrong
    assert u.verify_password("MySecret123")
    assert not u.verify_password("WrongPass")

@pytest.mark.parametrize("first,last,email", [
    ("",      "Last",  "a@b.com"),
    ("F"*51,  "Last",  "a@b.com"),
    ("First", "",      "a@b.com"),
    ("First", "L"*51,  "a@b.com"),
    ("First", "Last",  "not-an-email"),
])
def test_user_invalid_init(first, last, email):
    with pytest.raises(ValueError):
        User(first, last, email)
