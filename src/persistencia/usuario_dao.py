from src.dominio.usuario import Usuario
from src.persistencia.conexion import abrir_conexion, marcador_sql


class UsuarioDAO:

    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(
            nombre_usuario=fila[1],
            password_hash=fila[2],
            empleado_id=fila[3],
            rol=fila[4],
            id=fila[0],
        )

    @staticmethod
    def insertar(usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            sql = (
                f"INSERT INTO usuario "
                f"(nombre_usuario, password_hash, empleado_id, rol) "
                f"VALUES ({m}, {m}, {m}, {m})"
            )
            cursor.execute(sql, (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.empleado_id,
                usuario.rol,
            ))
            conexion.commit()
            usuario.id = cursor.lastrowid
            return usuario
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            cursor.execute(
                f"SELECT id, nombre_usuario, password_hash, "
                f"empleado_id, rol FROM usuario WHERE nombre_usuario = {m}",
                (nombre,),
            )
            fila = cursor.fetchone()
            return UsuarioDAO._fila_a_usuario(fila) if fila else None
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_empleado(empleado_id):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            cursor.execute(
                f"SELECT id, nombre_usuario, password_hash, "
                f"empleado_id, rol FROM usuario WHERE empleado_id = {m}",
                (empleado_id,),
            )
            fila = cursor.fetchone()
            return UsuarioDAO._fila_a_usuario(fila) if fila else None
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre_usuario, password_hash, "
                "empleado_id, rol FROM usuario ORDER BY id"
            )
            return [
                UsuarioDAO._fila_a_usuario(f)
                for f in cursor.fetchall()
            ]
        finally:
            if conexion:
                conexion.close()