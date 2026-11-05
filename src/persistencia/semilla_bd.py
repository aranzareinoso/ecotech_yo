from persistencia.conexion import (
    abrir_conexion,
    obtener_motor,
    marcador_sql,
)


# ==========================================================
# DATOS DE SEMILLA
# ==========================================================

EMPLEADOS = [
    # (nombre, direccion, numero, correo, fecha_contrato, salario, cargo)
    ("Ana Torres",        "Av. Siempre Viva 123", "555-1001", "ana.torres@ecotech.com",    "2021-03-15", 4500.00, "Gerente de Proyectos"),
    ("Luis Ramírez",      "Calle Falsa 456",      "555-1002", "luis.ramirez@ecotech.com",  "2020-07-01", 5200.00, "Gerente de TI"),
    ("María González",    "Av. Central 789",      "555-1003", "maria.gonzalez@ecotech.com","2022-01-10", 3200.00, "Desarrolladora Senior"),
    ("Carlos Pérez",      "Calle Norte 321",      "555-1004", "carlos.perez@ecotech.com",  "2022-05-20", 2800.00, "Desarrollador Junior"),
    ("Sofía Herrera",     "Av. Sur 654",          "555-1005", "sofia.herrera@ecotech.com", "2023-02-14", 3100.00, "Analista de Datos"),
    ("Jorge Mendoza",     "Calle Este 987",       "555-1006", "jorge.mendoza@ecotech.com", "2021-11-05", 4000.00, "Arquitecto de Software"),
    ("Lucía Vargas",      "Av. Oeste 159",        "555-1007", "lucia.vargas@ecotech.com",  "2023-08-01", 2600.00, "QA Engineer"),
    ("Pedro Castro",      "Calle Bosque 753",     "555-1008", "pedro.castro@ecotech.com",  "2020-02-28", 5600.00, "Gerente de Operaciones"),
    ("Valentina Rojas",   "Av. Jardines 852",     "555-1009", "valentina.rojas@ecotech.com","2022-09-12", 3000.00, "Diseñadora UX"),
    ("Andrés Silva",      "Calle Río 963",        "555-1010", "andres.silva@ecotech.com",  "2024-01-08", 2400.00, "Soporte Técnico"),
]

# (nombre, id_gerente)  -> el id_gerente hace referencia a empleados 1, 2, 8...
DEPARTAMENTOS = [
    ("Proyectos",     1),
    ("Tecnología",    2),
    ("Operaciones",   8),
    ("Recursos Humanos", None),
    ("Diseño",        None),
]

# (nombre, fecha_inicio, descripcion)
PROYECTOS = [
    ("Plataforma EcoTech v2",   "2024-01-15", "Rediseño completo de la plataforma web corporativa."),
    ("Migración a la Nube",     "2024-03-01", "Migración de servicios internos a infraestructura cloud."),
    ("App Móvil EcoTech",       "2024-04-10", "Desarrollo de la aplicación móvil para clientes."),
    ("Dashboard de Métricas",   "2024-05-20", "Panel analítico para visualización de KPIs."),
    ("Auditoría de Seguridad",  "2024-06-01", "Revisión y endurecimiento de la seguridad de sistemas."),
    ("Portal de Clientes",      "2024-08-15", "Portal self-service para clientes de EcoTech."),
]

# (horas_trabajadas, fecha_trabajada, descripcion_tarea, empleado_id, proyecto_id)
REGISTROS_TIEMPO = [
    (6, "2024-06-03", "Definición de arquitectura del portal",        1, 1),
    (8, "2024-06-03", "Configuración de pipelines CI/CD",             2, 2),
    (5, "2024-06-04", "Maquetación de pantallas principales",         9, 3),
    (7, "2024-06-04", "Endpoint de autenticación de usuarios",        3, 1),
    (4, "2024-06-05", "Pruebas unitarias del módulo de login",        7, 1),
    (8, "2024-06-05", "Migración de base de datos a MySQL",           6, 2),
    (6, "2024-06-06", "Diseño del dashboard de KPIs",                 5, 4),
    (5, "2024-06-06", "Documentación de la API pública",              3, 6),
    (8, "2024-06-07", "Análisis de vulnerabilidades con OWASP ZAP",   2, 5),
    (3, "2024-06-07", "Soporte a usuarios internos durante el deploy",10, 2),
    (7, "2024-06-10", "Integración de pasarela de pago",              4, 3),
    (6, "2024-06-10", "Optimización de consultas SQL del reporte",    5, 4),
]


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def _insertar(cursor, motor, sql_base, valores):
    """Inserta una fila adaptando el marcador al motor."""
    if motor == "sqlite":
        cursor.execute(sql_base, valores)
        return cursor.lastrowid
    else:  # mysql / mariadb
        cursor.execute(sql_base, valores)
        return cursor.lastrowid


def _tabla_vacia(cursor, tabla):
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    return cursor.fetchone()[0] == 0


# ==========================================================
# FUNCIÓN PRINCIPAL DE SEMILLA
# ==========================================================

def sembrar_datos() -> None:
    """
    Inserta datos de ejemplo en las tablas:
    empleado, departamento, proyecto y registro_tiempo.

    - No duplica datos: si una tabla ya tiene filas, la omite.
    - Compatible con SQLite y MySQL/MariaDB.
    """

    motor = obtener_motor()
    if motor not in ("sqlite", "mysql", "mariadb"):
        raise ValueError(f"Motor no soportado: '{motor}'")

    conexion = None
    cursor = None

    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        # ---------------- EMPLEADOS ----------------
        if _tabla_vacia(cursor, "empleado"):
            sql_empleado = """
                INSERT INTO empleado
                    (nombre, direccion, numero, correo,
                        fecha_contrato, salario, cargo)
                VALUES ({}, {}, {}, {}, {}, {}, {})
            """.format(*([marcador_sql()] * 7))

            for emp in EMPLEADOS:
                _insertar(cursor, motor, sql_empleado, emp)

            print(f"  · {len(EMPLEADOS)} empleados insertados.")
        else:
            print("  · Tabla 'empleado' ya contiene datos, se omite.")

        # ---------------- DEPARTAMENTOS ----------------
        if _tabla_vacia(cursor, "departamento"):
            sql_dep = f"""
                INSERT INTO departamento (nombre, id_gerente)
                VALUES ({marcador_sql()}, {marcador_sql()})
            """
            for dep in DEPARTAMENTOS:
                _insertar(cursor, motor, sql_dep, dep)
            print(f"  · {len(DEPARTAMENTOS)} departamentos insertados.")
        else:
            print("  · Tabla 'departamento' ya contiene datos, se omite.")

        # ---------------- PROYECTOS ----------------
        if _tabla_vacia(cursor, "proyecto"):
            sql_proy = f"""
                INSERT INTO proyecto (nombre, fecha_inicio, descripcion)
                VALUES ({marcador_sql()}, {marcador_sql()}, {marcador_sql()})
            """
            for proy in PROYECTOS:
                _insertar(cursor, motor, sql_proy, proy)
            print(f"  · {len(PROYECTOS)} proyectos insertados.")
        else:
            print("  · Tabla 'proyecto' ya contiene datos, se omite.")

        # ---------------- REGISTROS DE TIEMPO ----------------
        if _tabla_vacia(cursor, "registro_tiempo"):
            sql_rt = f"""
                INSERT INTO registro_tiempo
                    (horas_trabajadas, fecha_trabajada,
                    descripcion_tarea, empleado_id, proyecto_id)
                VALUES ({marcador_sql()}, {marcador_sql()},
                        {marcador_sql()}, {marcador_sql()},
                        {marcador_sql()})
            """
            for rt in REGISTROS_TIEMPO:
                _insertar(cursor, motor, sql_rt, rt)
            print(f"  · {len(REGISTROS_TIEMPO)} registros de tiempo insertados.")
        else:
            print("  · Tabla 'registro_tiempo' ya contiene datos, se omite.")

        conexion.commit()
        print(f"\nSemilla aplicada correctamente usando {motor.upper()}.")

    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"Error al aplicar la semilla: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


# ==========================================================
# EJECUCIÓN DIRECTA
# ==========================================================

if __name__ == "__main__":
    try:
        sembrar_datos()
    except Exception as e:
        print(f"Error al sembrar datos: {e}")