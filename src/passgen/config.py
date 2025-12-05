# src/passgen/config.py

'''
IMPORT Path from pathlib

SET BASE_DIR to the directory where this file (config.py) is located

SET DATA_DIR to BASE_DIR joined with "data"

IF DATA_DIR does not exist:
    CREATE the DATA_DIR directory

SET PASSWORD_FILE to DATA_DIR joined with "passwords.json"

SET DEFAULT_LENGTH to some integer (e.g. 12)
SET MIN_LENGTH to some integer (e.g. 4)
SET MAX_LENGTH to some integer (e.g. 64)
'''

from pathlib import Path        # path helps us work with file system paths in an OS-independent way


# BASE_DIR represent the directory where this config.py file is located.
# From there, we can build other paths (like the data directory).
BASE_DIR: Path = Path(__file__).resolve().parent

# DATA_DIR is a subdirectory called "data" inside the package directory.
# This is where we will store our JSON file with saved passwords.
DATA_DIR: Path = BASE_DIR / "data"

# Make sure that the data directory exists.
# exist_ok=True means "do nothing if the directory already exists".
DATA_DIR.mkdir(exist_ok=True)

# Path to the JSON file where passwords will be stored.
# We will use this later in the storage module.
PASSWORD_FILE: Path = DATA_DIR / "passwords.json"

# Default configuration values for password length.
# These values will be used later when we ask the user for a password length.
DEFAULT_LENGTH: int = 12    # A reasonable default password length
MIN_LENGTH: int = 4         # Minimum allowed lenth for a password
MAX_LENGTH: int = 64        # MAximum allowed lenth for a password