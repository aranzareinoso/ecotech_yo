from src.persistencia.crear_bd import crear_tablas
from src.persistencia.usuario_dao import UsuarioDAO
from src.servicios.autenticacion import registrar_usuario


def sembrar():
    crear_tablas()

    if UsuarioDAO.buscar_por_nombre("admin") is None:
        try:
            registrar_usuario(
                empleado_id=1,
                nombre="admin",
                clave="Admin2025!",
                rol="admin",
            )
            print("Cuenta admin creada: admin / Admin2025!")
        except ValueError as error:
            print(f"No se pudo crear admin: {error}")
    else:
        print("Cuenta admin ya existe, no se duplica.")

    if UsuarioDAO.buscar_por_nombre("ana_torres") is None:
        try:
            registrar_usuario(
                empleado_id=2,
                nombre="ana_torres",
                clave="Ana2025!",
                rol="empleado",
            )
            print("Cuenta empleado creada: ana_torres / Ana2025!")
        except ValueError as error:
            print(f"No se pudo crear ana_torres: {error}")
    else:
        print("Cuenta ana_torres ya existe, no se duplica.")


if __name__ == "__main__":
    sembrar()