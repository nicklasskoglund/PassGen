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


