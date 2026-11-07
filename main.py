import sys
from src.menus.menu_usuario import solicitar_login, solicitar_registro
from src.menus.menu_indicadores import menu_indicadores
from src.servicios.permisos import exigir_admin
from src.persistencia.usuario_dao import UsuarioDAO
from src.menus.menu_admin import menu_admin
from src.menus.menu_empleado import menu_empleado


def menu_privado(usuario_actual):
    rol_mostrar = "Administrador" if usuario_actual["rol"] == "admin" else "Funcionario"
    
    while True:
        print(f"\n=== ECOTECH === ({usuario_actual['nombre_usuario']} - {rol_mostrar})")
        print("1. Mi perfil")
        print("2. Consultar indicadores (dólar/clima)")
        
        
        if usuario_actual["rol"] == "admin":
            print("3. Administrar Empleados, Departamentos y Proyectos")
        else:
            print("3. Ver Proyectos y Registrar Horas")
            
        print("0. Cerrar sesión")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            return "0"
        elif opcion == "1":
            print(f"\nUsuario: {usuario_actual['nombre_usuario']}")
            print(f"Empleado ID: {usuario_actual['empleado_id']}")
            print(f"Rol: {rol_mostrar}")
        elif opcion == "2":
            menu_indicadores(usuario_actual)
        elif opcion == "3":
            if usuario_actual["rol"] == "admin":
                menu_admin(usuario_actual)
            else:
                menu_empleado(usuario_actual)
        else:
            print("Opción no válida.")

def main():
    while True:
        print("\n===== ECOTECH =====")
        print("1. Iniciar sesión")
        print("2. Registrar nueva cuenta")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("Hasta luego.")
            return
        elif opcion == "2":
            solicitar_registro()
        elif opcion == "1":
            usuario_actual = solicitar_login()
            if usuario_actual is None:
                if input("Enter para reintentar o 0 para salir: ") == "0":
                    return
                continue

            resultado = menu_privado(usuario_actual)
            usuario_actual = None
            if resultado == "0":
                return
            print("Sesión cerrada.")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        sys.exit(0)