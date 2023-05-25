#!/usr/bin/env python3
"""Module encrypts passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string."""
    password_byte = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_byte, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """return True if password match else False"""
    password_byte = password.encode("utf-8")
    return bcrypt.checkpw(password_byte, hashed_password)
