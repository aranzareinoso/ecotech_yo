from src.persistencia.proyecto_dao import ProyectoDAO, RegistroHorasDAO
from src.servicios.permisos import exigir_sesion

def menu_empleado(sesion):
    exigir_sesion(sesion)
    empleado_id = sesion["empleado_id"]

    while True:
        print("\n--- MENÚ FUNCIONARIO ---")
        print("1. Ver mi perfil")
        print("2. Ver mis proyectos asignados")
        print("3. Registrar horas en un proyecto")
        print("4. Ver mis registros de tiempo")
        print("5. Volver al menú principal")
        opc = input("Opción: ").strip()

        if opc == "1":
            print(f"\nPerfil: {sesion['nombre_usuario']} (ID: {empleado_id}, Rol: {sesion['rol']})")
        elif opc == "2":
            print("\nMis proyectos:")
            for p in ProyectoDAO.listar_por_empleado(empleado_id):
                print(f" - ID {p[0]}: {p[1]}")
        elif opc == "3":
            proyectos = ProyectoDAO.listar_por_empleado(empleado_id)
            if not proyectos:
                print("No tienes proyectos asignados.")
                continue
            for p in proyectos:
                print(f" - ID {p[0]}: {p[1]}")
            try:
                proy_id = int(input("ID del proyecto: "))
                horas = float(input("Cantidad de horas: "))
                RegistroHorasDAO.insertar(empleado_id, proy_id, horas)
                print("Horas registradas con éxito.")
            except ValueError:
                print("Error: Ingresa números válidos.")
        elif opc == "4":
            print("\nMis registros de tiempo:")
            for r in RegistroHorasDAO.listar_por_empleado(empleado_id):
                print(f" - Proyecto ID {r[1]}: {r[2]} horas el {r[3]}")
        elif opc == "5":
            break