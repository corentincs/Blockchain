"""
This module allows to encrypt and decrypt data using Fernet (symmetric algorithm, AES). The key is generated from
a password.

To generate a private key, use generate_private_key(password, salt=default_salt). The salt is optional. A default value
is initialized in this module. You can generate a new salt with generate_salt().

To encrypt data, use encrypt(data, key). The key must be a base64 encoded string. To decrypt data, use decrypt(data, key).

The data are binary. To convert a string to a binary string, use encode(). To convert a binary string to a string, use
decode().
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

default_salt = b'\xb1\xc7\xbb\x04K\xd4\n~uA\xbe\xa4\x1a\xaeV\xe3'


def generate_salt():
    """
    Generate a salt
    :return: a binary string
    """
    return os.urandom(16)


def generate_private_key(password, salt=default_salt):
    """
    Generate a key from a password
    :param password: str
    :param salt: binary string
    :return: key encoded in base64
    """
    password = password.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt(data, key):
    """
    Encrypt data with a key
    :param data: binary data
    :param key: a base64 encoded key
    :return: binary data
    """
    fernet = Fernet(key)
    data = fernet.encrypt(data)
    return data


def decrypt(data, key):
    """
    Decrypt data with a key
    :param data: binary data
    :param key: a base64 encoded key
    :return: a string
    """
    fernet = Fernet(key)
    data = fernet.decrypt(data)
    return data


def test():
    key = generate_private_key("password")
    data = "A plain message that look good"
    print(f"Data : {data}")
    data = encrypt(data.encode(), key)
    print(f"Encrypted : {data}")
    data = decrypt(data, key)
    print(f"Decrypted data : {data.decode()}")


if __name__ == "__main__":
    test()
