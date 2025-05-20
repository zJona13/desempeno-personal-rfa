# app/models/criterion.py
from conexionBD import Conexion

class Criterion:
    @staticmethod
    def get_all():
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idCriterio, nombre, descripcion, valor, vigencia FROM CRITERIOS ORDER BY nombre")
            criteria = db_cursor.fetchall()
            return criteria
        except Exception as e:
            print(f"Error al obtener todos los criterios: {e}")
            return []
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def get_by_id(criterion_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idCriterio, nombre, descripcion, valor, vigencia FROM CRITERIOS WHERE idCriterio = %s", (criterion_id,))
            criterion = db_cursor.fetchone()
            return criterion
        except Exception as e:
            print(f"Error al obtener criterio por ID: {e}")
            return None
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def create(nombre, descripcion, valor, vigencia):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "INSERT INTO CRITERIOS (nombre, descripcion, valor, vigencia) VALUES (%s, %s, %s, %s)",
                (nombre, descripcion, valor, vigencia)
            )
            db_conn.commit()
            return True, "Criterio creado exitosamente."
        except Exception as e:
            if db_conn:
                db_conn.rollback()
            print(f"Error al crear criterio: {e}")
            return False, f"Error al crear criterio: {str(e)}"
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def update(criterion_id, nombre, descripcion, valor, vigencia):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "UPDATE CRITERIOS SET nombre = %s, descripcion = %s, valor = %s, vigencia = %s WHERE idCriterio = %s",
                (nombre, descripcion, valor, vigencia, criterion_id)
            )
            db_conn.commit()
            return True, "Criterio actualizado exitosamente."
        except Exception as e:
            if db_conn:
                db_conn.rollback()
            print(f"Error al actualizar criterio: {e}")
            return False, f"Error al actualizar criterio: {str(e)}"
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def delete(criterion_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            # Considerar si hay dependencias antes de eliminar (ej. EVALUACION_CRITERIO)
            # Por ahora, eliminación directa:
            db_cursor.execute("DELETE FROM CRITERIOS WHERE idCriterio = %s", (criterion_id,))
            db_conn.commit()
            return True, "Criterio eliminado exitosamente."
        except Exception as e:
            if db_conn:
                db_conn.rollback()
            print(f"Error al eliminar criterio: {e}")
            # Podrías verificar errores de FK y dar un mensaje más amigable
            if "foreign key constraint fails" in str(e).lower():
                 return False, "No se puede eliminar el criterio porque está siendo utilizado en evaluaciones."
            return False, f"Error al eliminar criterio: {str(e)}"
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()