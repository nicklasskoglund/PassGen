# src/passgen/security.py

'''
Security module for PassGen.

Demonstrates common security practices and concepts:
- Input validation (used throughout the CLI with helper functions)
- Safe path handling via pathlib (reduces path traversal risks)
- Avoiding command injection (no user input is executed as shell commands)
- Password hashing with salt using PBKDF2-HMAC-SHA256
- Safe data handling (no plain passwords in logs, optional masking in UI)
'''


import base64
import hashlib
import hmac
import secrets
from typing import Tuple


def _pbkdf2_sha256(password: str, salt: bytes, iterations: int) -> bytes:
    '''
    Derive a cryptographic key from a password using PBKDF2-HMAC-SHA256.

    Args:
        password: The plain text password.
        salt: Random salt bytes.
        iterations: Number of PBKDF2 iterations.

    Returns:
        Derived key bytes.
    '''
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )


def hash_password(password: str, iterations: int = 100_000) -> str:
    '''
    Create a salted, hashed representation of a password.

    The format is:
        pbkdf2_sha256$iterations$salt_b64$hash_b64

    This is similar in spirit to how many web frameworks store password hashes.

    Args:
        password: The plain text password to hash.
        iterations: Number of PBKDF2 iterations (default: 100_000).

    Returns:
        A single string containing algorithm, iterations, salt and hash.
    '''
    # generate a random 16-byte salt.
    salt = secrets.token_bytes(16)
    
    # derive the key using PBKDF2-HMAC-SHA256.
    dk = _pbkdf2_sha256(password, salt, iterations)
    
    # encode salt and hash to base64 so they can be stored as text.
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(dk).decode('ascii')
    
    return f'pbkdf2_sha256${iterations}${salt_b64}${hash_b64}'


def _parse_stored_hash(stored: str) -> Tuple[int, bytes, bytes]:
    '''
    Parse a stored hash string into its components.

    Expected format:
        pbkdf2_sha256$iterations$salt_b64$hash_b64

    Args:
        stored: The stored hash string.

    Returns:
        Tuple of (iterations, salt_bytes, hash_bytes).

    Raises:
        ValueError: If the format is invalid.
    '''
    try:
        algorithm, iter_str, salt_b64, hash_b64 = stored.split('$', 3)
    except ValueError as exc:
        raise ValueError('Invalid stored hash format.') from exc
    
    if algorithm != 'pbkdf2_sha256':
        raise ValueError(f'Unsupported algorithm: {algorithm}')
    
    iterations = int(iter_str)
    salt = base64.b64decode(salt_b64)
    stored_hash = base64.b64decode(hash_b64)
    
    return iterations, salt, stored_hash


