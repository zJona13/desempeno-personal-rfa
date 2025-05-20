# app/models/collaborator.py
from conexionBD import Conexion
import datetime # Para manejar fechas

# --- Clases CollaboratorType y ContractType (ya existentes) ---
class CollaboratorType:
    @staticmethod
    def get_all():
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idTipoColab, nombre FROM TIPO_COLABORADOR ORDER BY nombre")
            types = db_cursor.fetchall()
            return types
        except Exception as e:
            print(f"Error al obtener todos los tipos de colaborador: {e}")
            return []
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()
    # ... (get_by_id, create, update, delete para CollaboratorType ya los tienes) ...
    @staticmethod
    def get_by_id(type_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idTipoColab, nombre FROM TIPO_COLABORADOR WHERE idTipoColab = %s", (type_id,))
            ctype = db_cursor.fetchone()
            return ctype
        except Exception as e:
            print(f"Error al obtener tipo de colaborador por ID: {e}")
            return None
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def create(nombre):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("INSERT INTO TIPO_COLABORADOR (nombre) VALUES (%s)", (nombre,))
            db_conn.commit()
            return True, "Tipo de colaborador creado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al crear tipo de colaborador: {e}")
            return False, f"Error al crear tipo de colaborador: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def update(type_id, nombre):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("UPDATE TIPO_COLABORADOR SET nombre = %s WHERE idTipoColab = %s", (nombre, type_id))
            db_conn.commit()
            return True, "Tipo de colaborador actualizado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al actualizar tipo de colaborador: {e}")
            return False, f"Error al actualizar tipo de colaborador: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def delete(type_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("DELETE FROM TIPO_COLABORADOR WHERE idTipoColab = %s", (type_id,))
            db_conn.commit()
            return True, "Tipo de colaborador eliminado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al eliminar tipo de colaborador: {e}")
            if "foreign key constraint fails" in str(e).lower():
                 return False, "No se puede eliminar el tipo porque está siendo utilizado por colaboradores."
            return False, f"Error al eliminar tipo de colaborador: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

class ContractType:
    @staticmethod
    def get_all():
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idTipoContrato, nombre FROM TIPO_CONTRATO ORDER BY nombre")
            types = db_cursor.fetchall()
            return types
        except Exception as e:
            print(f"Error al obtener todos los tipos de contrato: {e}")
            return []
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()
    # ... (get_by_id, create, update, delete para ContractType ya los tienes) ...
    @staticmethod
    def get_by_id(type_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("SELECT idTipoContrato, nombre FROM TIPO_CONTRATO WHERE idTipoContrato = %s", (type_id,))
            ctype = db_cursor.fetchone()
            return ctype
        except Exception as e:
            print(f"Error al obtener tipo de contrato por ID: {e}")
            return None
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def create(nombre):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("INSERT INTO TIPO_CONTRATO (nombre) VALUES (%s)", (nombre,))
            db_conn.commit()
            return True, "Tipo de contrato creado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al crear tipo de contrato: {e}")
            return False, f"Error al crear tipo de contrato: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def update(type_id, nombre):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("UPDATE TIPO_CONTRATO SET nombre = %s WHERE idTipoContrato = %s", (nombre, type_id))
            db_conn.commit()
            return True, "Tipo de contrato actualizado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al actualizar tipo de contrato: {e}")
            return False, f"Error al actualizar tipo de contrato: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def delete(type_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            db_cursor.execute("DELETE FROM TIPO_CONTRATO WHERE idTipoContrato = %s", (type_id,))
            db_conn.commit()
            return True, "Tipo de contrato eliminado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al eliminar tipo de contrato: {e}")
            if "foreign key constraint fails" in str(e).lower():
                 return False, "No se puede eliminar el tipo porque está siendo utilizado en contratos."
            return False, f"Error al eliminar tipo de contrato: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

class Contract:
    @staticmethod
    def create(fecha_inicio, fecha_fin, estado, modalidad, id_tipo_contrato, db_cursor):
        # Este método asume que db_cursor es un cursor existente y la transacción
        # se manejará externamente (por la función que crea al colaborador)
        try:
            db_cursor.execute(
                "INSERT INTO CONTRATO (fechaInicio, fechaFin, estado, modalidad, idTipoContrato) VALUES (%s, %s, %s, %s, %s)",
                (fecha_inicio, fecha_fin, estado, modalidad, id_tipo_contrato)
            )
            return db_cursor.lastrowid # Devuelve el ID del contrato creado
        except Exception as e:
            print(f"Error al crear contrato: {e}")
            raise # Relanza la excepción para que la transacción externa haga rollback

    @staticmethod
    def get_by_id(contract_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute(
                """SELECT c.idContrato, c.fechaInicio, c.fechaFin, c.estado, c.modalidad, 
                          tc.nombre as tipo_contrato_nombre, c.idTipoContrato
                   FROM CONTRATO c
                   JOIN TIPO_CONTRATO tc ON c.idTipoContrato = tc.idTipoContrato
                   WHERE c.idContrato = %s""", (contract_id,)
            )
            return db_cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener contrato por ID: {e}")
            return None
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()
    
    @staticmethod
    def update(contract_id, fecha_inicio, fecha_fin, estado, modalidad, id_tipo_contrato, db_cursor):
        # Asume que db_cursor es un cursor existente y la transacción se maneja externamente
        try:
            db_cursor.execute(
                """UPDATE CONTRATO 
                   SET fechaInicio = %s, fechaFin = %s, estado = %s, modalidad = %s, idTipoContrato = %s
                   WHERE idContrato = %s""",
                (fecha_inicio, fecha_fin, estado, modalidad, id_tipo_contrato, contract_id)
            )
        except Exception as e:
            print(f"Error al actualizar contrato: {e}")
            raise

class Collaborator:
    @staticmethod
    def create(nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab,
               # Datos del contrato
               fecha_inicio_contrato, fecha_fin_contrato, estado_contrato, modalidad_contrato, id_tipo_contrato,
               id_usuario_vinculado=None): # Opcional: para vincular a un USUARIO
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_conn.start_transaction()
            db_cursor = db_conn.cursor()

            # 1. Crear el Contrato
            id_contrato_nuevo = Contract.create(
                fecha_inicio_contrato, fecha_fin_contrato, estado_contrato, 
                modalidad_contrato, id_tipo_contrato, db_cursor
            )
            if not id_contrato_nuevo:
                raise Exception("No se pudo crear el contrato.")

            # 2. Crear el Colaborador
            # Si necesitas vincular a idUsuario, la tabla COLABORADOR debe tener esa columna.
            # Por ahora, el SQL de tablas_bd.sql no la tiene, así que id_usuario_vinculado no se usa aquí.
            # Si la añades: ALTER TABLE COLABORADOR ADD COLUMN idUsuario INT(10) NULL REFERENCES USUARIO(idUsuario);
            sql_insert_colab = """
                INSERT INTO COLABORADOR 
                (nombres, apePat, apeMat, fechaNacimiento, direccion, telefono, dni, estado, idTipoColab, idContrato) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Si tuvieras idUsuario:
            # sql_insert_colab = """
            #     INSERT INTO COLABORADOR 
            #     (nombres, apePat, apeMat, fechaNacimiento, direccion, telefono, dni, estado, idTipoColab, idContrato, idUsuario) 
            #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            # """
            # params_colab = (nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab, id_contrato_nuevo, id_usuario_vinculado)

            params_colab = (nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab, id_contrato_nuevo)
            db_cursor.execute(sql_insert_colab, params_colab)
            
            db_conn.commit()
            return True, "Colaborador y su contrato creados exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al crear colaborador: {e}")
            return False, f"Error al crear colaborador: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def get_all_with_details():
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            # Asegúrate que las tablas y columnas en el JOIN sean correctas
            db_cursor.execute("""
                SELECT 
                    col.idColaborador, col.nombres, col.apePat, col.apeMat, col.dni, col.estado AS estado_colaborador,
                    tc.nombre AS tipo_colaborador_nombre,
                    contr.idContrato, contr.fechaInicio, contr.fechaFin, contr.modalidad, contr.estado AS estado_contrato,
                    tcontr.nombre AS tipo_contrato_nombre
                FROM COLABORADOR col
                LEFT JOIN TIPO_COLABORADOR tc ON col.idTipoColab = tc.idTipoColab
                LEFT JOIN CONTRATO contr ON col.idContrato = contr.idContrato
                LEFT JOIN TIPO_CONTRATO tcontr ON contr.idTipoContrato = tcontr.idTipoContrato
                ORDER BY col.apePat, col.apeMat, col.nombres
            """)
            collaborators = db_cursor.fetchall()
            return collaborators
        except Exception as e:
            print(f"Error al obtener todos los colaboradores con detalles: {e}")
            return []
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def get_by_id_with_details(collaborator_id):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor(dictionary=True)
            db_cursor.execute("""
                SELECT 
                    col.idColaborador, col.nombres, col.apePat, col.apeMat, col.fechaNacimiento, 
                    col.direccion, col.telefono, col.dni, col.estado AS estado_colaborador,
                    col.idTipoColab, tc.nombre AS tipo_colaborador_nombre,
                    contr.idContrato, contr.fechaInicio, contr.fechaFin, contr.modalidad, 
                    contr.estado AS estado_contrato, contr.idTipoContrato,
                    tcontr.nombre AS tipo_contrato_nombre
                    -- , col.idUsuario -- Si añades idUsuario a COLABORADOR
                FROM COLABORADOR col
                LEFT JOIN TIPO_COLABORADOR tc ON col.idTipoColab = tc.idTipoColab
                LEFT JOIN CONTRATO contr ON col.idContrato = contr.idContrato
                LEFT JOIN TIPO_CONTRATO tcontr ON contr.idTipoContrato = tcontr.idTipoContrato
                WHERE col.idColaborador = %s
            """, (collaborator_id,))
            collaborator = db_cursor.fetchone()
            return collaborator
        except Exception as e:
            print(f"Error al obtener colaborador por ID con detalles: {e}")
            return None
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def update(collaborator_id, nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab,
               # Datos del contrato
               contract_id, fecha_inicio_contrato, fecha_fin_contrato, estado_contrato, modalidad_contrato, id_tipo_contrato,
               id_usuario_vinculado=None):
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_conn.start_transaction()
            db_cursor = db_conn.cursor()

            # 1. Actualizar el Contrato
            Contract.update(
                contract_id, fecha_inicio_contrato, fecha_fin_contrato, estado_contrato, 
                modalidad_contrato, id_tipo_contrato, db_cursor
            )

            # 2. Actualizar el Colaborador
            # Si tuvieras idUsuario:
            # sql_update_colab = """
            #     UPDATE COLABORADOR SET 
            #     nombres = %s, apePat = %s, apeMat = %s, fechaNacimiento = %s, direccion = %s, 
            #     telefono = %s, dni = %s, estado = %s, idTipoColab = %s, idUsuario = %s
            #     WHERE idColaborador = %s
            # """
            # params_colab = (nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab, id_usuario_vinculado, collaborator_id)
            sql_update_colab = """
                UPDATE COLABORADOR SET 
                nombres = %s, apePat = %s, apeMat = %s, fechaNacimiento = %s, direccion = %s, 
                telefono = %s, dni = %s, estado = %s, idTipoColab = %s
                WHERE idColaborador = %s
            """
            params_colab = (nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab, collaborator_id)
            db_cursor.execute(sql_update_colab, params_colab)
            
            db_conn.commit()
            return True, "Colaborador y su contrato actualizados exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al actualizar colaborador: {e}")
            return False, f"Error al actualizar colaborador: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()

    @staticmethod
    def delete(collaborator_id):
        # Eliminar un colaborador puede ser complejo debido a las dependencias (contrato, evaluaciones).
        # Usualmente, en lugar de eliminar, se cambia el estado del colaborador a 'inactivo'.
        # Si se elimina, el contrato asociado también debería eliminarse o manejarse.
        # Aquí se implementa un cambio de estado como ejemplo más seguro.
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            # Podrías también inactivar el contrato asociado
            # contract_to_inactivate = Collaborator.get_by_id_with_details(collaborator_id)
            # if contract_to_inactivate and contract_to_inactivate['idContrato']:
            #    Contract.update(contract_to_inactivate['idContrato'], ..., estado=0, ..., db_cursor) # Asumiendo 0=inactivo

            db_cursor.execute("UPDATE COLABORADOR SET estado = 0 WHERE idColaborador = %s", (collaborator_id,)) # 0 = Inactivo
            db_conn.commit()
            return True, "Colaborador inactivado exitosamente."
        except Exception as e:
            if db_conn: db_conn.rollback()
            print(f"Error al inactivar colaborador: {e}")
            return False, f"Error al inactivar colaborador: {str(e)}"
        finally:
            if db_cursor: db_cursor.close()
            if db_conn and db_conn.is_connected(): db_conn.close()