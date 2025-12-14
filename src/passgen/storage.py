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


from datetime import datetime       # used to store a timestamp for each password
from typing import List, Dict, Any  # type hints for better readability

from .config import PASSWORD_FILE   # import the path to our JSON file
from .io.module_io import read_json_file, write_json_file   # import read/writ JSON


def _load_raw() -> List[Dict[str, Any]]:
    '''
    Load the raw list of password records from the JSON file.
    
    Uses the generic read_json_file() helper from the io.module_io module.
    '''
    data = read_json_file(PASSWORD_FILE)
    
    # if the file was missing or invalid, we treat it as an empty list.
    if data is None:
        return []
    
    # we expect the data to be a list of dictionaries.
    if not isinstance(data, list):
        return []
    
    return data


def _save_raw(data: List[Dict[str, Any]]) -> None:
    '''
    Save the given list of password records back to the JSON file.
    
    Delegates JSON writing to the io.module_io helper.
    '''
    write_json_file(PASSWORD_FILE, data)


def add_password(service: str, username: str, password: str) -> None:
    '''
    Add a new password to the JSON file.
    
    :param service: The name of the service (e.g. "Gmail", "Spotify").
    :param username: The username or email used for that service.
    :param password: The generated password.
    '''
    data = _load_raw()
    
    record: Dict[str, Any] = {
        'service': service,
        'username': username,
        'password': password,
        # store a timestamp when the password was created
        'created_at': datetime.now().isoformat(timespec='seconds'),
    }
    
    data.append(record)
    _save_raw(data)
    
    
def list_passwords() -> List[Dict[str, Any]]:
    '''
    Return the list of all saved password records.
    
    :return: List of dictionaries with key: service, username, password, created_at.
    '''
    return _load_raw()