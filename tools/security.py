from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password_plain):
    return ph.hash(password_plain)
