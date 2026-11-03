
from persistencia.conexion import abrir_conexion, obtener_motor


# ==========================================================
# ESTRUCTURA DE TABLAS PARA SQLITE
# ==========================================================

TABLAS_SQLITE = [

    # Tabla empleado
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT NOT NULL,
        numero TEXT NOT NULL,
        correo TEXT NOT NULL,
        fecha_contrato TEXT NOT NULL,
        salario REAL NOT NULL,
        cargo TEXT NOT NULL
    )
    """,

    # Tabla departamento
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        id_gerente INTEGER,
        FOREIGN KEY (id_gerente)
            REFERENCES empleado(id)
            ON DELETE SET NULL
    )
    """,

    # Tabla proyecto
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        descripcion TEXT NOT NULL
    )
    """,

    # Tabla registro de tiempo
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        horas_trabajadas INTEGER NOT NULL
            CHECK (horas_trabajadas > 0),
        fecha_trabajada TEXT NOT NULL,
        descripcion_tarea TEXT NOT NULL,
        empleado_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE,

        FOREIGN KEY (proyecto_id)
            REFERENCES proyecto(id)
            ON DELETE CASCADE
    )
    """,

    # Relación departamento - empleado
    """
    CREATE TABLE IF NOT EXISTS departamento_empleado (
        departamento_id INTEGER NOT NULL,
        empleado_id INTEGER NOT NULL,

        PRIMARY KEY (departamento_id, empleado_id),

        FOREIGN KEY (departamento_id)
            REFERENCES departamento(id)
            ON DELETE CASCADE,

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
    )
    """,

    # Relación departamento - proyecto
    """
    CREATE TABLE IF NOT EXISTS departamento_proyecto (
        departamento_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,

        PRIMARY KEY (departamento_id, proyecto_id),

        FOREIGN KEY (departamento_id)
            REFERENCES departamento(id)
            ON DELETE CASCADE,

        FOREIGN KEY (proyecto_id)
            REFERENCES proyecto(id)
            ON DELETE CASCADE
    )
    """,

    # Relación proyecto - empleado
    """
    CREATE TABLE IF NOT EXISTS proyecto_empleado (
        proyecto_id INTEGER NOT NULL,
        empleado_id INTEGER NOT NULL,

        PRIMARY KEY (proyecto_id, empleado_id),

        FOREIGN KEY (proyecto_id)
            REFERENCES proyecto(id)
            ON DELETE CASCADE,

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
    )
    """,

    # Tabla usuario
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL UNIQUE,
        nombre_usuario TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'empleado'
            CHECK (rol IN ('admin', 'empleado')),

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
    )
    """
]


# ==========================================================
# ESTRUCTURA DE TABLAS PARA MYSQL / MARIADB
# ==========================================================

TABLAS_MYSQL = [

    # Tabla empleado
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(200) NOT NULL,
        numero VARCHAR(30) NOT NULL,
        correo VARCHAR(150) NOT NULL,
        fecha_contrato DATE NOT NULL,
        salario DECIMAL(12, 2) NOT NULL,
        cargo VARCHAR(100) NOT NULL
    ) ENGINE=InnoDB
    """,

    # Tabla departamento
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        id_gerente INT,

        FOREIGN KEY (id_gerente)
            REFERENCES empleado(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    ) ENGINE=InnoDB
    """,

    # Tabla proyecto
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        fecha_inicio DATE NOT NULL,
        descripcion TEXT NOT NULL
    ) ENGINE=InnoDB
    """,

    # Tabla registro de tiempo
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        horas_trabajadas INT NOT NULL
            CHECK (horas_trabajadas > 0),
        fecha_trabajada DATE NOT NULL,
        descripcion_tarea TEXT NOT NULL,
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

        FOREIGN KEY (proyecto_id)
            REFERENCES proyecto(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB
    """,

    # Relación departamento - empleado
    """
    CREATE TABLE IF NOT EXISTS departamento_empleado (
        departamento_id INT NOT NULL,
        empleado_id INT NOT NULL,

        PRIMARY KEY (departamento_id, empleado_id),

        FOREIGN KEY (departamento_id)
            REFERENCES departamento(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB
    """,

    # Relación departamento - proyecto
    """
    CREATE TABLE IF NOT EXISTS departamento_proyecto (
        departamento_id INT NOT NULL,
        proyecto_id INT NOT NULL,

        PRIMARY KEY (departamento_id, proyecto_id),

        FOREIGN KEY (departamento_id)
            REFERENCES departamento(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

        FOREIGN KEY (proyecto_id)
            REFERENCES proyecto(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB
    """,

    # Relación proyecto - empleado
    """
    CREATE TABLE IF NOT EXISTS proyecto_empleado (
        proyecto_id INT NOT NULL,
        empleado_id INT NOT NULL,

        PRIMARY KEY (proyecto_id, empleado_id),

        FOREIGN KEY (proyecto_id)
            REFERENCES proyecto(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB
    """,

    # Tabla usuario
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INT PRIMARY KEY AUTO_INCREMENT,
        empleado_id INT NOT NULL UNIQUE,
        nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        rol VARCHAR(10) NOT NULL DEFAULT 'empleado'
            CHECK (rol IN ('admin', 'empleado')),

        FOREIGN KEY (empleado_id)
            REFERENCES empleado(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    ) ENGINE=InnoDB
    """
]


# ==========================================================
# FUNCIÓN PARA CREAR LAS TABLAS
# ==========================================================

def crear_tablas() -> None:
    """
    Crea todas las tablas de la base de datos EcoTech.

    Compatible con:
    - SQLite
    - MySQL
    - MariaDB
    """

    motor = obtener_motor().lower()

    # Seleccionar estructura según motor
    if motor == "sqlite":
        tablas = TABLAS_SQLITE

    elif motor in ("mysql", "mariadb"):
        tablas = TABLAS_MYSQL

    else:
        raise ValueError(
            f"Motor de base de datos no soportado: '{motor}'"
        )

    conexion = None
    cursor = None

    try:
        # Abrir conexión
        conexion = abrir_conexion()

        # Crear cursor
        cursor = conexion.cursor()

        # Ejecutar sentencias SQL
        for sql in tablas:
            cursor.execute(sql)

        # Confirmar cambios
        conexion.commit()

        print(
            f"Base de datos EcoTech preparada correctamente "
            f"utilizando {motor.upper()}."
        )

    except Exception as e:

        if conexion:
            conexion.rollback()

        print(f"Error al crear las tablas: {e}")

        raise

    finally:

        # Cerrar cursor
        if cursor:
            cursor.close()

        # Cerrar conexión
        if conexion:
            conexion.close()


# ==========================================================
# EJECUCIÓN DIRECTA
# ==========================================================

if __name__ == "__main__":

    try:
        crear_tablas()

    except Exception as e:
        print(f"Error al preparar la base de datos: {e}")
