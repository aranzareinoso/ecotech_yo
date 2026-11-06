import bcrypt
from dominio.usuario import Usuario
from persistencia.UsuarioDAO import UsuarioDAO

MAX_BYTES_BCRYPT = 72

def crear_hash(contrasenia):
    contrasenia = Usuario.validad_contrasenia(contrasenia)
    clave_bytes = contrasenia.encode("utf-8")

    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
    ).decode("utf-8")

def registrar_usuario(empleado_id, nombre_usuario, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre_usuario) is not None:
        raise ValueError("No se pudo crear esa cuenta.")   

    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)
    
    return UsuarioDAO.insertar(usuario)

def autenticar(nombre_usuario, contrasenia):
    nombre = Usuario.normalizar_usuario(nombre_usuario)
    if not isinstance(contrasenia, str):
        return None
    datos = contrasenia.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
            return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre_usuario)

    if cuenta is None:
        print(f"No se encontró la cuenta para el usuario: {nombre_usuario}")
        return None
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None
    return {"id": cuenta.id, "empleado_id": cuenta.id_usuario,
            "nombre_usuario": cuenta.nombre_usuario}
