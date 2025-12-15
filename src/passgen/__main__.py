# src/passgen/__main__.py

'''
Module entry point for PassGen.

Demonstrates:
- How to expose a package as a CLI using `python -m passgen`
- Delegating execution to a dedicated `run_app()` function in main.py
- Clean separation between packaging/entry logic and application logic
'''


from .main import run_app       # import the main application function
from . import logger            # import logger function


def main() -> None:
    '''
    Wrapper around run_app() with a global safety net.

    Catches unexpected exceptions, logs them and shows a friendly message.
    '''
    try:
        run_app()
    except Exception as exc:  # broad on purpose here
        # log critical error
        logger.log_event(f'Unexpected error in main: {exc!r}', level='ERROR')
        # last-resort message to user
        print('\nA critical error occurred. Please try again or check the log file.\n')


if __name__ == '__main__':
    main()