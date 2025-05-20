from argon2 import PasswordHasher
import re

def hash_password(password_plain):
    ph = PasswordHasher()
    return ph.hash(password_plain)

#Función que permite validar una contraseña, la cual debe tener: mayúsculas, números, caracteres especiales y al menos 6 caracteres
def validate_password(password):
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 10 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener letras mayúsculas"
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener números"
    if not re.search(r'[!@#%^&*(),.=?":{}$¿?¡]', password):
        return False, "La contraseña debe contener caracteres especiales"
    return True, 'Contraseña válida'