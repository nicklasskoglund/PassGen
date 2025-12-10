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


