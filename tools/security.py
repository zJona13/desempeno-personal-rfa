# tools/security.py
from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()

def hash_password(password_plain):
    return ph.hash(password_plain)

def verify_password(hashed_password, password_plain):
    try:
        return ph.verify(hashed_password, password_plain)
    except exceptions.VerifyMismatchError:
        return False
    except Exception as e:
        # Consider logging other exceptions
        print(f"Error al verificar la contraseña: {e}")
        return False