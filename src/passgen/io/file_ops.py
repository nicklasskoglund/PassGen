# src/passgen/io/file_ops.py

'''
IMPORT datetime
IMPORT Path
IMPORT PASSWORD_FILE, REPORTS_DIR, LOG_FILE from config
IMPORT read_json_file, write_json_file from module_io

FUNCTION generate_timestamp(format_str="%Y%m%d_%H%M%S"):
    RETURN current datetime formatted using format_str

FUNCTION backup_password_file():
    READ data from PASSWORD_FILE using read_json_file
    IF data is None:
        SET data to empty list
    SET backup_dir to data directory / "backups"
    CREATE backup_dir if needed
    CREATE filename "passwords_<timestamp>.json"
    WRITE data to backup file using write_json_file
    RETURN path to backup file

FUNCTION reset_password_file():
    WRITE [] to PASSWORD_FILE using write_json_file

FUNCTION backup_log_file():
    SET backup_dir to REPORTS_DIR / "backups"
    CREATE backup_dir if needed
    IF LOG_FILE does not exist:
        RETURN None
    READ all text from LOG_FILE
    CREATE filename "passgen_log_<timestamp>.txt"
    WRITE text to backup file (normal open/write)
    RETURN path to backup file
'''


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


