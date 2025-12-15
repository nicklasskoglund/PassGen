# src/passgen/io/file_ops.py

"""
File operations module for PassGen.

Responsibility:
- Create timestamped backups of the password storage file (passwords.json)
- Reset the password storage file to an empty list
- Create timestamped backups of the main log file (passgen_log.txt)

Demonstrates:
- Timestamp-based filenames for backup and archival
- Using pathlib for directory management and file copying
- Keeping backup/maintenance functionality separate from core logic
"""


from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..config import PASSWORD_FILE, REPORTS_DIR, LOG_FILE
from .module_io import read_json_file, write_json_file


def generate_timestamp(format_str: str = '%Y%m%d_%H%M%S') -> str:
    '''
    Generate a timestamp string for filenames.
    
    Ex:
        20251210_214530
    '''
    return datetime.now().strftime(format_str)


def backup_password_file() -> Path:
    '''
    Create a backup of the current passwords.json file.
    
    - Reads the current password data (or uses an empty list if missing/invalid).
    - Writes a backup file with a timestamped name in a 'backups' directory next to the original passwords.json file.
    
    Returns:
        Path to the created backup file.
    '''
    # load current data (may be None if file is missing or invalid)
    data: Any = read_json_file(PASSWORD_FILE)
    
    if data is None:
        # if there is no valid data, we still create a backup,
        # but the file will contain an empty list.
        data = []
        
    # define a backups directory under the same parent as PASSWORD_FILE
    backup_dir: Path = PASSWORD_FILE.parent / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # build a filename: passwords_YYYYMMDD_HHMMSS.json
    timestamp = generate_timestamp()
    backup_filename = f'passwords_{timestamp}.json'
    backup_path = backup_dir / backup_filename
    
    # write JSON data to the backup file
    write_json_file(backup_path, data)
    
    return backup_path


def reset_password_file() -> None:
    '''
    Reset the password storage file to an empty list.
    
    This is useful for testing or if you want to clear all stored passwords.
    '''
    write_json_file(PASSWORD_FILE, [])
    
    
def backup_log_file() -> Optional[Path]:
    '''
    Create a backup of the main log file (passgen_log.txt), if it exists.
    
    - Reads the entire log file as text.
    - Writes it to a timestamped backup file in REPORTS_DIR / 'backups'.'
    
    Returns:
        Path to the created backup file, or None if the log file does not exists.
    '''
    if not LOG_FILE.exists():
        # no log file to back up.
        return None
    
    backup_dir: Path = REPORTS_DIR / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = generate_timestamp()
    backup_filename = f'passgen_log_{timestamp}.txt'
    backup_path = backup_dir / backup_filename
    
    # read all text from the original log file
    text = LOG_FILE.read_text(encoding='utf-8')
    
    # write text to the backup file
    backup_path.write_text(text, encoding='utf-8')
    
    return backup_path