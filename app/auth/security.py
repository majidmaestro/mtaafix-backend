"""
Password security utilities for MtaaFix authentication.
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """
    Generate a secure hash from a user's password.

    Passwords should never be stored in plain text.
    """
    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password cannot be empty.")

    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Check whether a password matches its stored hash.
    """
    if not isinstance(password, str) or not isinstance(password_hash, str):
        return False

    if not password or not password_hash:
        return False

    try:
        return check_password_hash(password_hash, password)
    except (ValueError, TypeError):
        return False
