# src/passgen/storage.py

'''
IMPORT json
IMPORT datetime (for timestamp)
IMPORT PASSWORD_FILE path from config

FUNCTION _load_raw():
    IF password file does not exist:
        RETURN empty list
    TRY:
        OPEN file for reading
        PARSE json into a Python list
        RETURN the list
    IF json is invalid:
        RETURN empty list

FUNCTION _save_raw(data_list):
    OPEN file for writing
    DUMP data_list as json with nice indentation

FUNCTION add_password(service, username, password):
    data_list = _load_raw()
    CREATE a record dict with:
        "service": service
        "username": username
        "password": password
        "created_at": current timestamp as ISO string
    APPEND record to data_list
    CALL _save_raw(data_list)

FUNCTION list_passwords():
    RETURN _load_raw()
'''


import json                         # used to read/write JSON files
from datetime import datetime       # used to store a timestamp for each password
from typing import List, Dict, Any  # type hints for better readability

from .config import PASSWORD_FILE   # import the path to our JSON file


def _load_raw() -> List[Dict[str, Any]]:
    '''
    Load the raw list of password records from the JSON file.
    
    :return: A list of dictioneries, each representing one saved password.
    '''
    # if the file does not exist yet, we simply return an empty list
    if not PASSWORD_FILE.exists():
        return[]
    
    try:
        with PASSWORD_FILE.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # if the file is corrupted or not valid JSON,
        # we return an empty list instead of crashing
        return[]
    
    # we expect the data to be a list. If not, we fall back to empty list
    if not isinstance(data, list):
        return[]
    
    return data


def _save_raw(data: List[Dict[str, Any]]) -> None:
    '''
    Save the given list of password records back to the JSON file.
    
    :param data: List of password dictionaries to write to the file.
    '''
    with PASSWORD_FILE.open('w', encoding='utf-8') as f:
        # indent=2 makes the JSON human-readable
        # ensure_ascii=False allowes Swedish characters etc.
        json.dump(data, f, indent=2, ensure_ascii=False)


