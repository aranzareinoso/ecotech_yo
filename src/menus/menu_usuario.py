import getpass
from src.servicios.autenticacion import autenticar, registrar_usuario
from src.dominio.usuario import Usuario

def pedir_dato(mensaje, validador, leer=input):
    while True:
        try:
            return validador(leer(mensaje))
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")

def solicitar_registro():
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass.getpass)
        
        if clave != getpass.getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden.")
            return None

        usuario_id = registrar_usuario(empleado_id, nombre, clave)
        print(f"Cuenta creada correctamente. ID: {usuario_id}")
        return usuario_id
    except (TypeError, ValueError) as error:
        print(error)
        return None

def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass.getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None

    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print(f"Sesión iniciada. Rol: {usuario['rol']}")
    return usuario