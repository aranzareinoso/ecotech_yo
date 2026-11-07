from src.persistencia.conexion import abrir_conexion, marcador_sql

class DepartamentoDAO:
    @staticmethod
    def insertar(nombre):
        # Validación de seguridad
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre del departamento es demasiado corto (mínimo 3 letras).")
        if not all(c.isalnum() or c.isspace() for c in nombre):
            raise ValueError("El nombre solo debe contener letras, números y espacios (sin símbolos).")

        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()
        cursor.execute(f"INSERT INTO departamento (nombre) VALUES ({m})", (nombre.strip(),))
        conexion.commit()
        conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM departamento")
        filas = cursor.fetchall()
        conexion.close()
        return filas