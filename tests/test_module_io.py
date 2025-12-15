# tests/test_module_io.py

from pathlib import Path

from passgen.io.module_io import read_json_file, write_json_file


def test_write_and_read_json_roundtrip(tmp_path):
    '''
    Writing data to a JSON file and reading it back
    should return the same data structure.
    '''
    path: Path = tmp_path / 'test.json'
    data = {'service': 'Gmail', 'count': 3, 'items': [1, 2, 3]}

    write_json_file(path, data)
    loaded = read_json_file(path)

    assert loaded == data


def test_read_json_missing_returns_none(tmp_path):
    '''
    If the JSON file does not exist, read_json_file should return None.
    '''
    path: Path = tmp_path / 'missing.json'
    assert read_json_file(path) is None


def test_read_json_invalid_returns_none(tmp_path):
    '''
    If the JSON file contains invalid JSON, read_json_file should return None.
    '''
    path: Path = tmp_path / 'invalid.json'
    path.write_text('this is not valid json', encoding='utf-8')

    assert read_json_file(path) is None
