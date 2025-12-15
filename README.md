<a id="readme-top"></a>
# 🔐 PassGen – Password Generator CLI


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python version">
  <img src="https://img.shields.io/badge/Project%20status-Active-success?style=flat-square" alt="Project status">
  <img src="https://img.shields.io/badge/Interface-CLI-black?style=flat-square" alt="CLI">
  <img src="https://img.shields.io/badge/Storage-JSON-lightgrey?style=flat-square" alt="JSON Storage">
  <img src="https://img.shields.io/badge/Tests-PyTest-orange?logo=pytest&logoColor=white" alt="Tests">
</p>


<!-- PROJECT LOGO -->
```
__________                        ________               
\______   \_____    ______ ______/  _____/  ____   ____  
 |     ___/\__  \  /  ___//  ___/   \  ____/ __ \ /    \ 
 |    |     / __ \_\___ \ \___ \\    \_\  \  ___/|   |  \
 |____|    (____  /____  >____  >\______  /\___  >___|  /
                \/     \/     \/        \/     \/     \/ 
```

## About The Project

PassGen is a small command-line password generator written in Python.  
It lets you create random passwords with different difficulty levels, customize the length, and optionally store them in a local JSON file together with service name, username, and timestamp.  
This repository was created as a school assignment / learning project and demonstrates a simple but structured CLI application.

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#how-to-run-the-program">How to Run the Program</a></li>
      <ul>
        <li><a href="#as-a-cli-tool">As a CLI tool</a></li>
        <li><a href="#using-the-module-directly">Using the module directly</a></li>
      </ul>
    <li><a href="#main-features">Main Features</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#tests">Tests</a></li>
    <li><a href="#author">Author (coming)</a></li>
    <li><a href="#future-improvements">Future Improvements (coming)</a></li>
  </ol>
</details>


---

## Installation

### Prerequisites
- Python **3.11+**
- (Recommended) Virtual environment (`.venv`)
- Git (if cloning the repository)

### Steps

### 1. Clone the repository
```bash
git clone https://github.com/nicklasskoglund/PassGen.git
cd PassGen
```

### 2. Create and activate a virtual environment
- ### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
- ### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the project (and dependencies)
- The project uses ```rich``` for colored CLI output and is configured via ```pyproject.toml```:
```bash
# Install in development mode (editable)
pip install -e .

# Or install normally
pip install .
```

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to Run the Program

### Usage
PassGen uses the ```pyproject.toml``` configuration and the ```rich``` library for colored CLI output.

### As a CLI tool
After installation, run from anywhere:
```bash
passgen
```

### Using the module directly
From the project root:
```bash
cd src
python -m passgen
```

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Main Features

- 🔐 **Password generation**
  - Random passwords using:
    - Lowercase letters
    - Uppercase letters
    - Digits
    - Special characters (depending on difficulty)
  - Three difficulty levels: Easy, Medium, Hard
  - Configurable password length with minimum, maximum and default values
- 💾 **Password storage (JSON)**
  - Optional saving of generated passwords to ```passwords.json```
  - Each entry includes:
    - Service name (e.g. “Gmail”, “Spotify”)
    - Username or email
    - Generated password
    - Creation timestamp
- 📂 **View saved passwords**
  - List all stored passwords directly in the CLI
  - Shows service, username, password and timestamp
- 🧾 **Security & logging**
  - ```security.py```
    - Password hashing with salt using PBKDF2-HMAC-SHA256
    - Masking helper to hide parts of the password when displaying it in the CLI
  - ```logging.py```
    - Logs important events to ```reports/passgen_log.txt```
    - Log entries include timestamp, log level and metadata (never the full password)
  - Path handling is done with ```pathlib``` for safer file paths.
  - Input validation is handled by helper functions in ```utils.py```.
- 🎨 **Colored CLI output**
  - Uses the rich library to provide a clearer and more user-friendly interface (colored headers, menu, and messages)
- **Backups & maintenance**
  - ```io/file_ops.py```:
    - ```backup_password_file()``` creates timestamped backups of ```passwords.json``` under ```data/backups/```
    - ```reset_password_file()``` clears the password store (writes an empty list)
    - ```backup_log_file()``` can back up the main log file under ```reports/backups/```
  - The CLI menu includes options to:
    - create a backup of the password file
    - reset (clear) all saved passwords (with confirmation)
  - All backup/reset operations are logged via ```logger.py```.
- **CLI experience**
  - Uses the ```rich``` library to render:
    - a colorful header (panel)
    - styled menu and messages
    - tables for listing saved passwords
  - Simple, menu-based navigation:
    1. Generate new password
    2. Show saved passwords
    3. Backup passwords file
    4. Reset passwords file
    5. Exit

### Note: This is a teaching project.
Passwords are still stored in plain text in the JSON file, even though a secure hash is also stored.
Do not use this application to store real, sensitive passwords.

---
  <p align="right">(<a href="#readme-top">back to top</a>)</p>

## Project Structure

```bash
PassGen/                          # PROJECT ROOT
├── .venv/                        # Virtual environment (optional, created with: python -m venv .venv)
├── requirements.txt              # Dependencies (runtime + dev tools like pytest, rich)
├── pyproject.toml                # Package configuration (name, scripts, dependencies)
├── README.md                     # Project documentation (this file)
├── tests/                        # Test suite (PyTest)
│   ├── test_password_generator.py
│   ├── test_security.py
│   ├── test_module_io.py
│   ├── test_storage.py
│   └── test_file_ops.py
└── src/                          # Source directory (src layout)
    └── passgen/                  # Main package
        ├── __init__.py           # Package initializer
        ├── __main__.py           # Module entry point (python -m passgen)
        ├── config.py             # Configuration & paths (data/report directories, length limits)
        ├── main.py               # Application entry point, CLI menu and main loop
        ├── password_generator.py # Password generation logic and difficulty levels
        ├── storage.py            # Password storage using JSON (add/list)
        ├── security.py           # Security helpers (hashing, verify, masking)
        ├── logger.py             # Logging utilities (writes to passgen_log.txt)
        ├── utils.py              # Input helpers and validation for CLI
        ├── io/                   # I/O layer for file operations
        │   ├── __init__.py       # Marks io as a subpackage
        │   ├── module_io.py      # Generic JSON/text I/O helpers
        │   └── file_ops.py       # Higher-level file operations (backups, reset)
        ├── data/                 # Data files (not tracked in git)
        │   ├── passwords.json    # Main password store (JSON)
        │   └── backups/          # Timestamped backups of passwords.json
        └── reports/              # Log and log backups (not tracked in git)
            ├── passgen_log.txt   # Application log file
            └── backups/          # Timestamped backups of the log file
```

---
  <p align="right">(<a href="#readme-top">back to top</a>)</p>

## Tests
The project includes automated tests using **PyTest**.

### Installation for tests
If PyTest is not already installed in your environment:
```bash
pip install pytest
```

### Running the tests
From the project root (```PassGen/```), with your virtual environment active:
```bash
pytest
```
or with more detailed output:
```bash
pytest -v
```

## What is tested
The ```tests/``` directory contains several test modules:
- ```test_password_generator.py```
  - checks that generated passwords have the correct length
  - validates that Easy/Medium/Hard difficulties use the expected character sets
  - verifies that invalid lengths raise ```ValueError```
- ```test_security.py```
  - verifies that ```hash_password``` and ```verify_password``` work together correctly
  - ensures that wrong passwords do not validate
  - tests the ```mask_password``` helper for both short and long passwords
- ```test_module_io.py```
  - ensures that JSON read/write roundtrips correctly
  - covers behavior for missing and invalid JSON files
- ```test_storage.py```
  - uses a temporary ```PASSWORD_FILE``` path (via PyTest ```tmp_path``` + ```monkeypatch```)
  - checks that ```add_password()``` creates the file and stores correct fields
  - validates that the stored ```password_hash``` matches the original password
  - checks that ```list_passwords()``` returns all added records
- ```test_file_ops.py```
  - tests ```backup_password_file()``` with and without an existing passwords file
  - tests ```reset_password_file()``` to ensure it writes an empty list
  - tests ```backup_log_file()``` for both missing and existing log files

All tests are isolated using temporary directories and do not touch your real data/ or reports/ directories.

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>