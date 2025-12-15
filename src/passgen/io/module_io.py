# src/passgen/io/module_io.py

"""
Generic file and JSON I/O helpers for PassGen.

Responsibility:
- Read JSON data safely from disk
- Write JSON data to disk with proper encoding and indentation
- Append lines of text to a file (used by the logging module)

Demonstrates:
- A dedicated I/O layer separate from business logic and CLI
- Robust handling of missing or invalid JSON files
- Using pathlib for file operations across platforms
"""


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
    except OSError:
        # could not read the file (permissions, IO error, etc.)
        return None
    
    
def write_json_file(path: Path, data: Any) -> None:
    '''
    Write Python data as JSON to a file.
    
    - Creates the parant directory if needed.
    - Overwrites the file if it already exists.
    
    Args:
        path: Path to the JSON file.
        data: Any JSON-serializable Python object.
    '''
    # ensure the parent directory exists.
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
        
def append_text_line(path: Path, line: str) -> None:
    '''
    Append a single line of text to a file.
    
    - Creates the parent directory if needed.
    - Adds a new line at the end of the line automatically.
    
    Args:
        path: Path to the text file.
        line: Line of text to append (without newline).
    '''
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open('a', encoding='utf-8') as f:
        f.write(line)
        # ensure there is exactly one newline at the end.
        if not line.endswith('\n'):
            f.write('\n')