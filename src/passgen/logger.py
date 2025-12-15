# src/passgen/logger.py

"""
Logging utilities for PassGen.

Responsibility:
- Append timestamped log entries to a text file (passgen_log.txt)
- Provide small helper functions for common events (generated/saved/listed passwords)

Demonstrates:
- Simple, custom logging using text files instead of print() statements
- Centralizing logging logic in one module
- Using timestamps and log levels (INFO, ERROR) for basic observability
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
    '''
    Append a single log entry to the passgen_log.txt file.
    
    The log format is:
        YYYY-MM-DD HH:MM:SS [LEVEL] message
    '''
    timestamp = _current_timestamp()
    line = f'{timestamp} [{level}] {message}\n'
    # delegate the actual file writing to the I/O helper.
    append_text_line(LOG_FILE, line)
        
        
def log_password_generated(length: int, difficulty: str) -> None:
    '''
    Helper function to log that a password was generated.
    
    We intentionally DO NOT log the actual password, only metadata.
    '''
    message = f'Generated password length={length} difficulty={difficulty!r}'
    log_event(message, level='INFO')
    
    
def log_password_saved(service: str, username: str) -> None:
    '''
    Helper function to log that a password was saved to storage.
    
    Again, we do NOT log the actual password for security reasons.
    '''
    message = f'Saved password service={service!r} username={username!r}'
    log_event(message, level='INFO')
    
    
def log_passwords_listed(count: int) -> None:
    '''
    Helper function to log that a saved password where listed.
    
    Args:
        count: Number of password records that were displayed.
    '''
    message = f'Listed saved passwords count={count}'
    log_event(message, level='INFO')