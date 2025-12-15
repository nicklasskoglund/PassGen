# tests/test_storage.py

"""
Tests for the storage module in PassGen.

Focus:
- Using a temporary PASSWORD_FILE path per test (via monkeypatch + tmp_path)
- Verifying that add_password() writes correct data to JSON
- Verifying that list_passwords() returns expected records
"""

import json
from pathlib import Path

from passgen import storage
from passgen.security import verify_password


def _setup_temp_password_file(tmp_path, monkeypatch) -> Path:
    """
    Helper to redirect storage.PASSWORD_FILE to a temporary file for each test.

    This ensures that tests do not touch the real passwords.json file.
    """
    temp_file = tmp_path / 'passwords.json'
    monkeypatch.setattr(storage, 'PASSWORD_FILE', temp_file)
    return temp_file


def test_list_passwords_empty_when_file_missing(tmp_path, monkeypatch):
    """
    If the password file does not exist, list_passwords() should return an empty list
    and should NOT create the file.
    """
    temp_file = _setup_temp_password_file(tmp_path, monkeypatch)

    passwords = storage.list_passwords()

    assert passwords == []
    assert not temp_file.exists()


def test_add_password_creates_file_and_record(tmp_path, monkeypatch):
    """
    add_password() should create the JSON file and store a single record
    with the expected fields.
    """
    temp_file = _setup_temp_password_file(tmp_path, monkeypatch)

    service = 'Gmail'
    username = 'user@example.com'
    password = 'SuperSecret123!'

    storage.add_password(service, username, password)

    # the file should now exist
    assert temp_file.exists()

    # read raw JSON to inspect the stored structure
    with temp_file.open('r', encoding='utf-8') as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 1

    record = data[0]
    
    # check that expected keys exist
    assert record['service'] == service
    assert record['username'] == username
    assert record['password'] == password
    assert 'password_hash' in record
    assert 'created_at' in record


def test_add_password_stores_hash_that_verifies(tmp_path, monkeypatch):
    """
    The stored password_hash field should be a salted PBKDF2 hash,
    and verify_password() should accept the original password.
    """
    temp_file = _setup_temp_password_file(tmp_path, monkeypatch)

    service = 'Spotify'
    username = 'test@example.com'
    password = 'AnotherSecret#456'

    storage.add_password(service, username, password)

    with temp_file.open('r', encoding='utf-8') as f:
        data = json.load(f)

    record = data[0]
    stored_hash = record['password_hash']

    # hash should not be the same as the plain password
    assert stored_hash != password

    # the security.verify_password() should validate the original password
    assert verify_password(password, stored_hash) is True


def test_list_passwords_returns_all_records(tmp_path, monkeypatch):
    """
    After adding multiple passwords, list_passwords() should return a list
    with the same number of records and matching service/username values.
    """
    _ = _setup_temp_password_file(tmp_path, monkeypatch)

    storage.add_password('Gmail', 'user1@example.com', 'PwdOne123!')
    storage.add_password('Spotify', 'user2@example.com', 'PwdTwo456!')
    storage.add_password('GitHub', 'kalle', 'PwdThree789!')

    records = storage.list_passwords()

    assert len(records) == 3

    # extract (service, username) pairs from the returned records
    pairs = {(r['service'], r['username']) for r in records}

    assert ('Gmail', 'user1@example.com') in pairs
    assert ('Spotify', 'user2@example.com') in pairs
    assert ('GitHub', 'kalle') in pairs
