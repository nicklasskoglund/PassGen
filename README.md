# 🔐 PassGen – Password Generator CLI


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python version">
  <img src="https://img.shields.io/badge/Project%20status-Active-success?style=flat-square" alt="Project status">
  <img src="https://img.shields.io/badge/Interface-CLI-black?style=flat-square" alt="CLI">
  <img src="https://img.shields.io/badge/Storage-JSON-lightgrey?style=flat-square" alt="JSON Storage">
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
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#as-a-cli-tool">As a CLI tool</a></li>
        <li><a href="#using-the-module-directly">Using the module directly</a></li>
      </ul>
    <li><a href="#main-features">Main Features</a></li>
    <li><a href="#project-structure">Project Structure (coming)</a></li>
    <li><a href="#tests">Tests (coming)</a></li>
    <li><a href="#author">Author (coming)</a></li>
    <li><a href="#future-improvements">Future Improvements (coming)</a></li>
  </ol>
</details>


---

## Installation

```bash
# Install in development mode (editable)
pip install -e .

# Or install normally
pip install .
```

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
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

- 🔐 Password generation
  - Random passwords using:
    - Lowercase letters
    - Uppercase letters
    - Digits
    - Special characters (depending on difficulty)
  - Three difficulty levels: Easy, Medium, Hard
  - Configurable password length with minimum, maximum and default values
- 💾 Password storage (JSON)
  - Optional saving of generated passwords to ```passwords.json```
  - Each entry includes:
    - Service name (e.g. “Gmail”, “Spotify”)
    - Username or email
    - Generated password
    - Creation timestamp
- 📂 View saved passwords
  - List all stored passwords directly in the CLI
  - Shows service, username, password and timestamp
- 🧾 Logging
  - Application events (e.g. password generated/saved, list viewed) are logged to ```reports/passgen_log.txt```
  - Logs include timestamp and basic metadata (but not the actual passwords)
- 🎨 Colored CLI output
  - Uses the rich library to provide a clearer and more user-friendly interface (colored headers, menu, and messages)

  ---
  <p align="right">(<a href="#readme-top">back to top</a>)</p>