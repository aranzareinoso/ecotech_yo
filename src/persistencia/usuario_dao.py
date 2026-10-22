from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.usuario import Usuario


class UsuarioDAO:

    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(
            id=fila[0],
            empleado_id=fila[1],
            nombre_usuario=fila[2],
            password_hash=fila[3]
        )

    @staticmethod
    def insertar(usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "INSERT INTO usuario "
                "(empleado_id, nombre_usuario, password_hash) "
                f"VALUES ({marca}, {marca}, {marca})"
            )
            cursor.execute(sql, (
                usuario.empleado_id,
                usuario.nombre_usuario,
                usuario.password_hash
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
    def actualizar(usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "UPDATE usuario SET "
                f"empleado_id = {marca}, nombre_usuario = {marca}, "
                f"password_hash = {marca} "
                f"WHERE id = {marca}"
            )
            cursor.execute(sql, (
                usuario.empleado_id,
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.id
            ))
            actualizado = cursor.rowcount > 0
            conexion.commit()
            return actualizado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = f"DELETE FROM usuario WHERE id = {marca}"
            cursor.execute(sql, (id_usuario,))
            eliminado = cursor.rowcount > 0
            conexion.commit()
            return eliminado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "SELECT id, empleado_id, nombre_usuario, password_hash "
                f"FROM usuario WHERE id = {marca}"
            )
            cursor.execute(sql, (id_usuario,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return UsuarioDAO._fila_a_usuario(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_nombre_usuario(nombre_usuario):
        """Útil para validar el inicio de sesión / autenticación."""
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "SELECT id, empleado_id, nombre_usuario, password_hash "
                f"FROM usuario WHERE nombre_usuario = {marca}"
            )
            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return UsuarioDAO._fila_a_usuario(fila)
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
                "SELECT id, empleado_id, nombre_usuario, password_hash FROM usuario"
            )
            filas = cursor.fetchall()
            usuarios = []
            for fila in filas:
                usuarios.append(UsuarioDAO._fila_a_usuario(fila))
            return usuarios
        finally:
            if conexion:
                conexion.close()