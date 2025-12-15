# tests/test_password_generator.py

import string
import pytest

from passgen.password_generator import generate_password, Difficulty


def test_generate_password_has_correct_length():
    """
    Generated password should have exactly the requested length.
    """
    length = 16
    pwd = generate_password(length, Difficulty.EASY)
    assert len(pwd) == length


def test_generate_password_easy_uses_only_letters_and_digits():
    """
    EASY difficulty should only use letters (upper/lower) and digits.
    No special characters allowed.
    """
    pwd = generate_password(40, Difficulty.EASY)

    allowed_chars = set(string.ascii_letters + string.digits)
    assert set(pwd) <= allowed_chars


def test_generate_password_medium_includes_specials():
    """
    MEDIUM difficulty should allow special characters.
    We check that at least one special character appears over a longer password.
    """
    pwd = generate_password(60, Difficulty.MEDIUM)

    letters_digits = set(string.ascii_letters + string.digits)
    
    # if all characters are letters/digits, then no specials were used.
    assert not set(pwd) <= letters_digits


def test_generate_password_hard_includes_specials():
    """
    HARD difficulty should also allow special characters.
    """
    pwd = generate_password(60, Difficulty.HARD)

    letters_digits = set(string.ascii_letters + string.digits)
    assert not set(pwd) <= letters_digits


def test_generate_password_invalid_length_raises():
    """
    Length <= 0 should raise ValueError.
    """
    with pytest.raises(ValueError):
        generate_password(0, Difficulty.EASY)