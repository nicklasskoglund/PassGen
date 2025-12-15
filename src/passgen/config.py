# src/passgen/config.py

"""
Configuration module for PassGen.

This module centralizes configuration, paths, and constants.

Demonstrates:
- Proper path handling using __file__ and pathlib
- A clear place for application-wide settings (length limits, data/report directories)
- Automatic creation of required directories (data/, reports/)
"""


from pathlib import Path        # path helps us work with file system paths in an OS-independent way


# BASE_DIR represent the directory where this config.py file is located.
# From there, we can build other paths (like the data directory).
BASE_DIR: Path = Path(__file__).resolve().parent

# =====================
# Data directory / JSON
# =====================

# DATA_DIR is a subdirectory called "data" inside the package directory.
# This is where we will store our JSON file with saved passwords.
DATA_DIR: Path = BASE_DIR / 'data'

# Make sure that the data directory exists.
# exist_ok=True means "do nothing if the directory already exists".
DATA_DIR.mkdir(exist_ok=True)

# Path to the JSON file where passwords will be stored.
# We will use this later in the storage module.
PASSWORD_FILE: Path = DATA_DIR / 'passwords.json'

# =====================
# Reports / logging
# =====================

# REPORTS_DIR is a subdirectory called "reports" inside the package directory
# This is where we will store log files and other reports.
REPORTS_DIR: Path = BASE_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)

# Single log file for the PassGen application.
# All log entries will be appended to this file.
LOG_FILE: Path = REPORTS_DIR / 'passgen_log.txt'

# =====================
# Password length configuration
# =====================

# Default configuration values for password length.
# These values will be used later when we ask the user for a password length.
DEFAULT_LENGTH: int = 12    # A reasonable default password length
MIN_LENGTH: int = 4         # Minimum allowed lenth for a password
MAX_LENGTH: int = 64        # MAximum allowed lenth for a password