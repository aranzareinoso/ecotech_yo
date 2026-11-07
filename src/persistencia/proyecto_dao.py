from datetime import datetime
from src.persistencia.conexion import abrir_conexion, marcador_sql

class ProyectoDAO:
    @staticmethod
    def insertar(nombre, empleado_id):
        # Validación de seguridad
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre del proyecto es demasiado corto (mínimo 3 letras).")
        if not all(c.isalnum() or c.isspace() for c in nombre):
            raise ValueError("El nombre solo debe contener letras, números y espacios (sin símbolos).")

        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()
        cursor.execute(f"INSERT INTO proyecto (nombre, empleado_id) VALUES ({m}, {m})", (nombre.strip(), empleado_id))
        conexion.commit()
        conexion.close()

    @staticmethod
    def listar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()
        cursor.execute(f"SELECT id, nombre FROM proyecto WHERE empleado_id = {m}", (empleado_id,))
        filas = cursor.fetchall()
        conexion.close()
        return filas

class RegistroHorasDAO:
    @staticmethod
    def insertar(empleado_id, proyecto_id, horas):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()
        fecha = datetime.now().isoformat(timespec="seconds")
        cursor.execute(f"INSERT INTO registro_horas (empleado_id, proyecto_id, horas, fecha) VALUES ({m}, {m}, {m}, {m})", (empleado_id, proyecto_id, horas, fecha))
        conexion.commit()
        conexion.close()

    @staticmethod
    def listar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()
        cursor.execute(f"SELECT id, proyecto_id, horas, fecha FROM registro_horas WHERE empleado_id = {m}", (empleado_id,))
        filas = cursor.fetchall()
        conexion.close()
        return filas