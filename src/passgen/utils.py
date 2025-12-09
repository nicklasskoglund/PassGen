# src/passgen/utils.py

'''
FUNCTION ask_menu_choice(prompt):
    READ user input with the given prompt
    STRIP whitespace
    RETURN the string

FUNCTION ask_int(prompt, min_value, max_value, default=None):
    LOOP forever:
        READ user input with the given prompt
        STRIP whitespace

        IF input is empty AND default is not None:
            RETURN default

        TRY to convert input to int:
            IF conversion fails:
                PRINT error "invalid number"
                CONTINUE loop

        IF value is less than min_value OR greater than max_value:
            PRINT error "must be between min and max"
            CONTINUE loop

        RETURN value

FUNCTION ask_non_empty(prompt):
    LOOP forever:
        READ user input with the given prompt
        STRIP whitespace
        IF not empty:
            RETURN value
        ELSE:
            PRINT error "field cannot be empty"
'''


from typing import Optional


def ask_menu_choice(prompt: str = 'Chooce an option: ') -> str:
    '''
    Ask the user to chooce a menu option.
    The function simply returns the user's input as a stripped string.
    Validation of what is a "valid" choice is done by caller.
    '''
    choice = input(prompt).strip()
    return choice