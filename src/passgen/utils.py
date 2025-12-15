# src/passgen/utils.py

"""
Utility functions for user input and validation in PassGen.

Responsibility:
- Read and validate menu choices
- Read and validate integer input within a given range
- Ensure non-empty string input for critical fields (e.g. service, username)

Demonstrates:
- Reusable helper functions for CLI input handling
- Input validation to prevent crashes from invalid user input
- Separation of low-level input logic from the main application flow
"""


from typing import Optional


def ask_menu_choice(prompt: str = 'Chooce an option: ') -> str:
    '''
    Ask the user to chooce a menu option.
    The function simply returns the user's input as a stripped string.
    Validation of what is a "valid" choice is done by caller.
    '''
    choice = input(prompt).strip()
    return choice


def ask_int(
    prompt: str,
    min_value: int,
    max_value: int,
    default: Optional[int] = None,
) -> int:
    '''
    Ask the user for an integer within a given range.
    Optionally, a default value can be provided.
    If the user presses Enter with no input and default is not None,
    the default value is returned.
    
    :param prompt: Text to show the user.
    :param min_value: Minimum allowed integer value.
    :param max_value: Maximum allowed integer value.
    :param default: Default value if the user inputs nothing (optional).
    :return: A valid integer within the range [min_value, max_value].
    '''
    while True:
        raw = input(prompt).strip()
        
        # if the user just presses Enter and a default is provided, use it.
        if raw == '' and default is not None:
            return default
        
        try:
            value = int(raw)
        except ValueError:
            print('❌ Invalid number, please enter an integer.')
            continue
        
        if value < min_value or value > max_value:
            print(f'❌ Value must be between {min_value} and {max_value}.')
            continue
        
        return value
    
    
def ask_non_empty(prompt: str) -> str:
    '''
    Ask the user for a non-empty string.
    The function will keep asking until the user writes something.
    
    :param prompt: Text to show the user.
    :return: A non-empty string.
    '''
    while True:
        value = input(prompt).strip()
        if value:
            return value
        
        print('❌ This field cannot be empty. Please enter a value.')