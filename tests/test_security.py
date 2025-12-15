# tests/test_security.py

from passgen.security import hash_password, verify_password, mask_password


def test_hash_and_verify_password_match():
    """
    The same password should verify correctly against its own hash.
    """
    password = 'SuperSecret123!'
    stored_hash = hash_password(password)

    assert stored_hash != password  # hash should not be plain text
    assert verify_password(password, stored_hash) is True


def test_hash_and_verify_password_mismatch():
    """
    A different password should NOT verify against the stored hash.
    """
    password = 'SuperSecret123!'
    wrong_password = 'WrongPassword999!'
    stored_hash = hash_password(password)

    assert verify_password(wrong_password, stored_hash) is False


def test_mask_password_short():
    """
    Short passwords should be fully masked.
    """
    masked = mask_password('abc', visible_chars=5)
    assert masked == '***'  # length 3, all masked


def test_mask_password_long():
    """
    Longer passwords should show only the first N characters, rest masked.
    """
    password = 'MyVerySecretPassword'
    masked = mask_password(password, visible_chars=3)

    assert masked.startswith('MyV')
    assert len(masked) == len(password)
    
    # the rest after the visible part should be '*'
    assert set(masked[3:]) == {'*'}