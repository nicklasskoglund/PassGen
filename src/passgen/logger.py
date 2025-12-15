# src/passgen/logger.py

"""
Logging utilities for PassGen.

Responsibility:
- Append timestamped log entries to a text file (passgen_log.txt)
- Provide helper functions for common events (generated/saved/listed passwords, backups, resets)

Demonstrates:
- Simple, custom logging using text files instead of print() statements
- Centralizing logging logic in one module
- Using timestamps and log levels (INFO, WARNING, ERROR) for basic observability
- Keeping sensitive data (actual passwords) out of logs
"""


from datetime import datetime

from .config import LOG_FILE
from .io.module_io import append_text_line


def _current_timestamp() -> str:
    '''
    Return the current timestamp as a formatted string.
    
    Ex format: "2025-12-10 21:37:12""
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log_event(message: str, level: str = 'INFO') -> None:
    """
    Append a single log entry to the passgen_log.txt file.

    Log format:
        YYYY-MM-DD HH:MM:SS [LEVEL] message

    Args:
        message: Text describing what happened.
        level:   Log level (e.g. "INFO", "WARNING", "ERROR").
    """
    timestamp = _current_timestamp()
    line = f'{timestamp} [{level}] {message}'

    # append_text_line adds a newline if needed and ensures the directory exists.
    append_text_line(LOG_FILE, line)
        
        
def log_password_generated(length: int, difficulty: str) -> None:
    """
    Log that a password was generated.

    Note:
        We do NOT log the actual password, only metadata.
    """
    message = f'Generated password length={length} difficulty={difficulty!r}'
    log_event(message, level='INFO')
    
    
def log_password_saved(service: str, username: str) -> None:
    """
    Log that a password was saved to storage.

    Note:
        We do NOT log the actual password, only metadata.
    """
    message = f'Saved password service={service!r} username={username!r}'
    log_event(message, level='INFO')
    
    
def log_passwords_listed(count: int) -> None:
    """
    Log that saved passwords were listed.

    Args:
        count: Number of password records that were displayed.
    """
    message = f'Listed saved passwords count={count}'
    log_event(message, level='INFO')
    

def log_backup_created(backup_path: str) -> None:
    """
    Log that a backup of the password file was created.

    Args:
        backup_path: The filesystem path to the created backup file.
    """
    message = f'Password backup created at {backup_path}'
    log_event(message, level='BACKUP')
    
    
def log_passwords_reset() -> None:
    """
    Log that the password storage file was reset/cleared.

    This is a destructive operation, so we log it as WARNING.
    """
    message = 'Password storage reset to empty list'
    log_event(message, level='WARNING')