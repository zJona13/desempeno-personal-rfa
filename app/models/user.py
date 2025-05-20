# app/models/user.py
from conexionBD import Conexion
from tools.security import hash_password, verify_password

class User:
    @staticmethod
    def find_by_email(email):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idUsuario, nombre, correo, contrasena, idTipoUsu, vigencia FROM USUARIO WHERE correo = %s", (email,))
            user_data = db_cursor.fetchone()
            return user_data
        except Exception as e:
            print(f"Error al buscar usuario por email: {e}")
            return None
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def create(nombre, correo, contrasena, id_tipo_usuario=4, vigencia=1):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            
            # Verificar si el correo ya existe
            db_cursor.execute("SELECT idUsuario FROM USUARIO WHERE correo = %s", (correo,))
            if db_cursor.fetchone():
                return False, "El correo electrónico ya está registrado."

            hashed_pass = hash_password(contrasena)
            db_cursor.execute(
                "INSERT INTO USUARIO (nombre, correo, contrasena, vigencia, idTipoUsu) VALUES (%s, %s, %s, %s, %s)",
                (nombre, correo, hashed_pass, vigencia, id_tipo_usuario)
            )
            db_conn.commit()
            return True, "Usuario creado exitosamente."
        except Exception as e:
            if db_conn:
                db_conn.rollback()
            print(f"Error al crear usuario: {e}")
            return False, f"Error durante el registro: {str(e)}"
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def verify_user_password(hashed_db_password, plain_password):
        return verify_password(hashed_db_password, plain_password)

    @staticmethod
    def get_role_name_by_id(role_id):
        if not role_id:
            return "Invitado"
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("SELECT nombre FROM TIPO_USUARIO WHERE idTipoUsu = %s", (role_id,))
            role_name_tuple = db_cursor.fetchone()
            return role_name_tuple[0] if role_name_tuple else "Desconocido"
        except Exception as e:
            print(f"Error al obtener nombre del rol: {e}")
            return "Error Rol"
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()