# src/passgen/io/module_io.py

'''
IMPORT json
IMPORT Path from pathlib
IMPORT Any from typing

FUNCTION read_json_file(path):
    IF path does not exist:
        RETURN None
    TRY:
        OPEN file for reading (utf-8)
        PARSE JSON and return data
    IF json is invalid:
        RETURN None

FUNCTION write_json_file(path, data):
    MAKE SURE parent directory exists
    OPEN file for writing (utf-8)
    DUMP JSON with indentation

FUNCTION append_text_line(path, line):
    MAKE SURE parent directory exists
    OPEN file in append mode (utf-8)
    WRITE line + newline
'''


import json
from pathlib import Path
from typing import Any, Optional


def read_json_file(path: Path) -> Optional[Any]:
    '''
    Read JSON from a file.
    
    - Returns the parsed JSON data (any Python type) if successful.
    - Returns None if the file does not exist or is not valid JSON.
    
    Args:
        path: Path to the JSON file.
        
    Returns:
        Parsed JSON data, or None if file is missing or invalid.
    '''
    if not path.exists():
        return None
    
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the content is not valid JSON, we return None instead of crashing.
        return None
    
    
