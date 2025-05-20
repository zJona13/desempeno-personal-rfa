# tools/security.py
from argon2 import PasswordHasher, exceptions # Asegúrate que 'exceptions' esté importado

ph = PasswordHasher()

def hash_password(password_plain):
    return ph.hash(password_plain)

# Esta es la función que deberías tener
def verify_password(hashed_password, password_plain):
    try:
        # La función ph.verify devuelve True si la verificación es exitosa
        # o lanza una excepción si no lo es.
        # Si devuelve True, la contraseña es válida.
        ph.verify(hashed_password, password_plain)
        return True 
    except exceptions.VerifyMismatchError:
        # Contraseña incorrecta
        return False
    except Exception as e: 
        # Otras excepciones durante la verificación (ej. hash inválido)
        # Es buena idea registrar este error para depuración
        print(f"Error inesperado durante la verificación de contraseña: {e}")
        return False