# src/passgen/__main__.py

"""
Module entry point for PassGen.

Demonstrates:
- How to expose a package as a CLI using `python -m passgen`
- Delegating execution to a dedicated `run_app()` function in main.py
- Clean separation between packaging/entry logic and application logic
"""


from .main import run_app       # import the main application function


if __name__ == '__main__':
    # this block runs when you execute: python -m passgen
    run_app()