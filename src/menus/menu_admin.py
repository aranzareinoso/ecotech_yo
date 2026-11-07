from src.persistencia.usuario_dao import UsuarioDAO
from src.persistencia.departamento_dao import DepartamentoDAO
from src.persistencia.proyecto_dao import ProyectoDAO
from src.persistencia.conexion import abrir_conexion

def menu_admin(sesion):
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Gestionar Empleados (Ver cuentas)")
        print("2. CRUD Departamentos")
        print("3. CRUD Proyectos")
        print("4. Volver al menú principal")
        opc = input("Opción: ").strip()

        if opc == "1":
            print("\nCuentas registradas:")
            for u in UsuarioDAO.listar():
                print(f" - {u.nombre_usuario} (rol={u.rol}, empleado_id={u.empleado_id})")
        
        elif opc == "2":
            print("\n--- DEPARTAMENTOS ---")
            print("1. Crear Departamento")
            print("2. Listar Departamentos")
            sub_opc = input("Opción: ").strip()
            if sub_opc == "1":
                nombre = input("Nombre del departamento: ").strip()
                try:
                    DepartamentoDAO.insertar(nombre)
                    print("Departamento creado exitosamente.")
                except ValueError as e:
                    print(f"\n[Error de Validación]: {e}")
            elif sub_opc == "2":
                print("\nLista de Departamentos:")
                for d in DepartamentoDAO.listar():
                    print(f" - ID {d[0]}: {d[1]}")
                    
        elif opc == "3":
            print("\n--- PROYECTOS ---")
            print("1. Crear Proyecto")
            print("2. Listar Proyectos (Todos)")
            sub_opc = input("Opción: ").strip()
            if sub_opc == "1":
                nombre = input("Nombre del proyecto: ").strip()
                try:
                    id_emp = int(input("ID del empleado a asignar: "))
                    ProyectoDAO.insertar(nombre, id_emp)
                    print("Proyecto creado y asignado exitosamente.")
                except ValueError as e:
                    print(f"\n[Error de Validación]: {e}")
            elif sub_opc == "2":
                print("\nLista de Proyectos:")
                conn = abrir_conexion()
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, empleado_id FROM proyecto")
                for p in cursor.fetchall():
                    print(f" - ID {p[0]}: {p[1]} (Asignado al empleado ID: {p[2]})")
                conn.close()
                
        elif opc == "4":
            break
        else:
            print("Opción no válida.")