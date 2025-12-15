# src/passgen/password_generator.py

"""
Password generation logic for PassGen.

Responsibility:
- Define difficulty levels (easy/medium/hard)
- Build character sets based on difficulty
- Generate random passwords using letters, digits and special characters

Demonstrates:
- Separation of business logic from CLI and storage concerns
- Use of Python's `random` and `string` modules
- Defensive programming with basic input validation and ValueError
"""


import random       # used to randomly choose characters for the password
import string       # provides ready-made sets of characters (letters, digits, etc.)


class Difficulty:
    '''
    Simple container for our difficulty levels.
    We will use string values "1", "2", "3" to match the menu choices later.
    '''
    
    EASY = '1'
    MEDIUM = '2'
    HARD = '3'
    

def get_charset_by_difficulty(level: str) -> str:
    '''
    Return a string containing all allowed characters
    for the given difficulty.
    
    :param level: One of "1", "2", "3" (EASY, MEDIUM, HARD)
    :return: A string with all characters that may be used.
    :raises ValueError: If the difficulty level is invalid.
    '''
    
    # basic character groups from the string module
    lower = string.ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"
    upper = string.ascii_uppercase  # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = string.digits          # "0123456789"
    
    # we define our set of special characters.
    # you can adjust this list if you want more or fewer symbols.
    specials = '!@#$%^&*()-_=+[]{};:,.?/'
    
    if level == Difficulty.EASY:
        # Easy: letters (lower + upper) and digits only
        return lower + upper + digits
    
    elif level == Difficulty.MEDIUM:
        # Medium: letters + digits + some special characters (first part of the list)
        return lower + upper + digits + specials[:10]
    
    elif level == Difficulty.HARD:
        # Hard: letters + digits + all defined special characters
        return lower + upper + digits + specials
    
    else:
        # if the caller passes something unexpected, we raise an error.
        # this will help us catch bugs early.
        raise ValueError(f'Invailid difficulty level: {level!r}')
    
    
def generate_password(length: int, level: str) -> str:
    '''
    Generate a random password with the given length and difficulty level.
    
    :param lenth: Desired lenth of the password (must be > 0).
    :param level: Difficulty level ("1", "2" or "3").
    :return: The generated password as a string.
    :raised ValueError: If lenth is invalid or the character set is empty.
    '''
    
    if length <= 0:
        # a password with zero or negativ lenth doesn´t make sense.
        raise ValueError('Password lenth must be greater that zero.')
    
    # get the allowed characters based on the difficulty level.
    charset = get_charset_by_difficulty(level)
    
    if not charset:
        # just a safety check - this should normally never happen.
        raise ValueError('Character set is empty. Cannot generate password.')
    
    # build the password by randomly picking one character at a time.
    password_chars = []     # we collect characters in a list first (efficient)
    
    
    for _ in range(length):
        # random.choice picks a single random character from the charset string.
        random_char = random.choice(charset)
        password_chars.append(random_char)
        
        
    # join the list of characters into a single string.
    password = ''.join(password_chars)
    return password