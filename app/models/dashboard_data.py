# app/models/dashboard_data.py
from conexionBD import Conexion

class DashboardData:
    @staticmethod
    def get_evaluaciones_pendientes_count(user_id, user_role_id):
        """
        Obtiene el número de evaluaciones pendientes para el usuario.
        La lógica exacta dependerá de cómo se asignan y rastrean las evaluaciones.
        Aquí un ejemplo MUY simplificado asumiendo un campo 'estado' en EVALUACION.
        """
        db_conn = None
        db_cursor = None
        count = 0
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            
            # idTipoUsu: 1=Admin, 2=Docente, 3=Evaluador, 4=Estudiante, 5=Developer
            if user_role_id == 2: # Docente (Autoevaluaciones)
                # Asumimos que un docente es un colaborador. Necesitamos mapear idUsuario a idColaborador.
                # Esta consulta es un placeholder y necesitará un mapeo adecuado.
                # SELECT COUNT(*) FROM EVALUACION e JOIN COLABORADOR c ON e.idColaborador = c.idColaborador
                # JOIN USUARIO u ON c.idUsuario = u.idUsuario # (Suponiendo que COLABORADOR tiene un idUsuario)
                # WHERE e.tipo = 'autoevaluacion' AND e.estado = 'pendiente' AND u.idUsuario = %s
                # Por ahora, un valor dummy:
                # Si el idUsuario del docente es el mismo que el idColaborador para el que se registra la autoevaluación
                db_cursor.execute("""
                    SELECT COUNT(*) FROM EVALUACION 
                    WHERE tipo = 'autoevaluacion' 
                    AND estado = 'pendiente' 
                    AND idColaborador = (SELECT idColaborador FROM COLABORADOR WHERE idUsuario = %s LIMIT 1)
                """, (user_id,)) # Necesitarás una forma de vincular USUARIO.idUsuario con COLABORADOR.idColaborador
                result = db_cursor.fetchone()
                count = result[0] if result else 0

            elif user_role_id == 4: # Estudiante (Evaluaciones a Docentes)
                # Asume que el idUsuario en EVALUACION es el del estudiante que evalúa
                db_cursor.execute("""
                    SELECT COUNT(*) FROM EVALUACION 
                    WHERE tipo = 'evaluacion_estudiante' 
                    AND estado = 'pendiente' 
                    AND idUsuario = %s
                """, (user_id,))
                result = db_cursor.fetchone()
                count = result[0] if result else 0
            
            # Añadir lógica para otros roles (Evaluador/Validador)
            # elif user_role_id == 1 or user_role_id == 3 or user_role_id == 5: # Admin, Evaluador, Developer (Validaciones pendientes)
            #    db_cursor.execute("SELECT COUNT(*) FROM EVALUACION WHERE estado = 'requiere_validacion'")
            #    result = db_cursor.fetchone()
            #    count = result[0] if result else 0

            return count # Ejemplo, reemplazar con consulta real
        except Exception as e:
            print(f"Error al obtener evaluaciones pendientes: {e}")
            return 0 # Retorna 0 en caso de error
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def get_incidencias_activas_count():
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            # Asumimos que estado=1 es 'activo' o 'pendiente' en INCIDENCIA
            # En tu tabla_bd.sql, INCIDENCIA.estado es TINYINT(3). Definamos 1 = Pendiente/Activa, 0 = Resuelta/Cerrada
            db_cursor.execute("SELECT COUNT(*) FROM INCIDENCIA WHERE estado = 1") 
            result = db_cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener incidencias activas: {e}")
            return 0
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    @staticmethod
    def get_validaciones_pendientes_count(user_role_id):
        # Solo relevante para roles como Admin, Validador, Developer
        if user_role_id not in [1, 3, 5]: # 1=Admin, 3=Evaluador (si valida), 5=Developer
            return 0
            
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            # Asumiendo que las evaluaciones que necesitan validación tienen un estado específico
            db_cursor.execute("SELECT COUNT(*) FROM EVALUACION WHERE estado = 'requiere_validacion'")
            result = db_cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener validaciones pendientes: {e}")
            return 0
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()
    
    @staticmethod
    def get_total_resultados_count():
        db_conn = None
        db_cursor = None
        try:
            db_conn = Conexion().open
            db_cursor = db_conn.cursor()
            # Contar evaluaciones que están 'completada' o 'validada'
            db_cursor.execute("SELECT COUNT(*) FROM EVALUACION WHERE estado IN ('completada', 'validada')")
            result = db_cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener total de resultados: {e}")
            return 0
        finally:
            if db_cursor:
                db_cursor.close()
            if db_conn and db_conn.is_connected():
                db_conn.close()

    # Nota: Las funciones de 'tendencia' se omiten por ahora debido a su complejidad.