#!/usr/bin/env python3
''' contains the authentication engine '''
from hashlib import pbkdf2_hmac
import os


def hash_pwd(password: str) -> bytes:
    ''' encrypt a password in bytes '''
    if not password or type(password) != str:
        return None
    salt = os.urandom(14)
    hashed_pwd = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    return salt + hashed_pwd


def verify_password(stored_password: bytes, password: str) -> bool:
    ''' Check the validity of the password '''
    if not stored_password or not password:
        return False
    if type(stored_password) is not bytes or type(password) is not str:
        return False
    salt = stored_password[:14]
    hashed_password = stored_password[14:]

    hashed_pwd = hash_pwd('sha256', password.encode('utf-8'), salt, 100000)

    if hashed_pwd == hashed_password:
        return True
    return False


if __name__ == "__main__":
    pass
