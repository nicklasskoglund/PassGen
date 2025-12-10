# src/passgen/logger.py

from datetime import datetime
from typing import Optional

from .config import LOG_FILE


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
        
    Args:
        message: Text describing what happened.
        level: Log level (e.g. "INFO", "WARNING", "ERROR").
    '''
    timestamp = _current_timestamp()
    line = f'{timestamp} [{level}] {message}\n'
    
    # open the log file in append mode ("a") so we don´t overwrite existing logs.
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(line)
        
        
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