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
        
        
