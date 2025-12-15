# tests/test_file_ops.py

'''
Tests for the file operations module in PassGen (io.file_ops).

Focus:
- backup_password_file(): creates a timestamped backup of passwords.json
- reset_password_file(): resets the password storage to an empty list
- backup_log_file(): creates a timestamped backup of the log file (if it exists)

All tests use tmp_path + monkeypatch so no real files in the project are touched.
'''

import json
from pathlib import Path

from passgen.io import file_ops
from passgen.io.module_io import write_json_file


def _setup_password_file_env(tmp_path, monkeypatch) -> Path:
    '''
    Redirect file_ops.PASSWORD_FILE to a temporary location for each test.
    '''
    temp_password_file = tmp_path / 'passwords.json'
    monkeypatch.setattr(file_ops, 'PASSWORD_FILE', temp_password_file)
    return temp_password_file


def _setup_log_file_env(tmp_path, monkeypatch) -> Path:
    '''
    Redirect file_ops.REPORTS_DIR and file_ops.LOG_FILE to a temporary location.
    '''
    reports_dir = tmp_path / 'reports'
    temp_log_file = reports_dir / 'passgen_log.txt'

    monkeypatch.setattr(file_ops, 'REPORTS_DIR', reports_dir)
    monkeypatch.setattr(file_ops, 'LOG_FILE', temp_log_file)

    return temp_log_file


def test_backup_password_file_creates_backup_with_same_content(tmp_path, monkeypatch):
    '''
    backup_password_file() should create a backup file under 'backups/'
    with the same JSON content as the original passwords.json.
    '''
    temp_password_file = _setup_password_file_env(tmp_path, monkeypatch)

    # Prepare some fake password data
    original_data = [
        {
            'service': 'Gmail',
            'username': 'user@example.com',
            'password': 'Secret123!',
            'created_at': '2025-12-10T22:30:00',
        }
    ]

    # Write original data to the temporary passwords.json
    write_json_file(temp_password_file, original_data)

    # Run backup
    backup_path = file_ops.backup_password_file()

    # Backup file should exist
    assert backup_path.exists()
    assert backup_path.parent == temp_password_file.parent / 'backups'

    # Backup content should match original content
    backup_data = json.loads(backup_path.read_text(encoding='utf-8'))
    assert backup_data == original_data


def test_backup_password_file_when_missing_creates_empty_backup(tmp_path, monkeypatch):
    '''
    If the password file does not exist, backup_password_file() should still
    create a backup file containing an empty list.
    '''
    temp_password_file = _setup_password_file_env(tmp_path, monkeypatch)

    # Ensure original file does NOT exist
    assert not temp_password_file.exists()

    backup_path = file_ops.backup_password_file()

    assert backup_path.exists()
    backup_data = json.loads(backup_path.read_text(encoding='utf-8'))

    # Since there was no valid data, backup should contain an empty list
    assert backup_data == []


def test_reset_password_file_writes_empty_list(tmp_path, monkeypatch):
    '''
    reset_password_file() should overwrite the password file with an empty list.
    '''
    temp_password_file = _setup_password_file_env(tmp_path, monkeypatch)

    # Write some initial data
    write_json_file(temp_password_file, [{'service': 'Test'}])
    assert temp_password_file.exists()

    # Reset file
    file_ops.reset_password_file()

    # File should still exist, but contain an empty JSON list
    data = json.loads(temp_password_file.read_text(encoding='utf-8'))
    assert data == []


def test_backup_log_file_returns_none_when_log_missing(tmp_path, monkeypatch):
    '''
    If the log file does not exist, backup_log_file() should return None
    and not create any backup.
    '''
    temp_log_file = _setup_log_file_env(tmp_path, monkeypatch)

    # Ensure log file does NOT exist
    assert not temp_log_file.exists()

    backup_path = file_ops.backup_log_file()

    assert backup_path is None
    # There should be no backups directory yet
    backups_dir = temp_log_file.parent / 'backups'
    assert not backups_dir.exists()


def test_backup_log_file_creates_backup_with_same_content(tmp_path, monkeypatch):
    '''
    If the log file exists, backup_log_file() should create a timestamped backup
    with the same textual content.
    '''
    temp_log_file = _setup_log_file_env(tmp_path, monkeypatch)

    # Create a fake log file
    log_content = '2025-12-10 22:40:00 [INFO] Test log entry\n'
    temp_log_file.parent.mkdir(parents=True, exist_ok=True)
    temp_log_file.write_text(log_content, encoding='utf-8')

    backup_path = file_ops.backup_log_file()

    assert backup_path is not None
    assert backup_path.exists()
    assert backup_path.parent == temp_log_file.parent / 'backups'

    backup_content = backup_path.read_text(encoding='utf-8')
    assert backup_content == log_content
