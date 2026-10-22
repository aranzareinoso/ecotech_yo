from persistencia.conexion import abrir_conexion, obtener_motor

# Definición de sentencias SQL centralizadas por motor
TABLAS_SQLITE = [
    """CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT NOT NULL,
        numero TEXT NOT NULL,
        correo TEXT NOT NULL,
        fecha_contrato TEXT NOT NULL,
        salario REAL NOT NULL,
        cargo TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        id_gerente INTEGER,
        FOREIGN KEY (id_gerente) REFERENCES empleado(id) ON DELETE SET NULL
    )""",
    """CREATE TABLE IF NOT EXISTS proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        descripcion TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        horas_trabajadas INTEGER NOT NULL CHECK (horas_trabajadas > 0),
        fecha_trabajada TEXT NOT NULL,
        descripcion_tarea TEXT NOT NULL,
        empleado_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS departamento_empleado (
        departamento_id INTEGER NOT NULL,
        empleado_id INTEGER NOT NULL,
        PRIMARY KEY (departamento_id, empleado_id),
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE CASCADE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS departamento_proyecto (
        departamento_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,
        PRIMARY KEY (departamento_id, proyecto_id),
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS proyecto_empleado (
        proyecto_id INTEGER NOT NULL,
        empleado_id INTEGER NOT NULL,
        PRIMARY KEY (proyecto_id, empleado_id),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL UNIQUE,
        nombre_usuario TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
    )"""
]

TABLAS_MYSQL = [
    """CREATE TABLE IF NOT EXISTS empleado (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(200) NOT NULL,
        numero VARCHAR(30) NOT NULL,
        correo VARCHAR(150) NOT NULL,
        fecha_contrato DATE NOT NULL,
        salario DECIMAL(12, 2) NOT NULL,
        cargo VARCHAR(100) NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS departamento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        id_gerente INT,
        FOREIGN KEY (id_gerente) REFERENCES empleado(id) ON DELETE SET NULL ON UPDATE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS proyecto (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        fecha_inicio DATE NOT NULL,
        descripcion TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        horas_trabajadas INT NOT NULL CHECK (horas_trabajadas > 0),
        fecha_trabajada DATE NOT NULL,
        descripcion_tarea TEXT NOT NULL,
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS departamento_empleado (
        departamento_id INT NOT NULL,
        empleado_id INT NOT NULL,
        PRIMARY KEY (departamento_id, empleado_id),
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE ON UPDATE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS departamento_proyecto (
        departamento_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        PRIMARY KEY (departamento_id, proyecto_id),
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS proyecto_empleado (
        proyecto_id INT NOT NULL,
        empleado_id INT NOT NULL,
        PRIMARY KEY (proyecto_id, empleado_id),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE ON UPDATE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS usuario (
        id INT PRIMARY KEY AUTO_INCREMENT,
        empleado_id INT NOT NULL UNIQUE,
        nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE ON UPDATE CASCADE
    )"""
]


def crear_tablas() -> None:
    """Crea la estructura de tablas para la base de datos de EcoTech."""
    motor = obtener_motor().lower()
    
    if motor == "sqlite":
        tablas = TABLAS_SQLITE
    elif motor in ("mysql", "mariadb"):
        tablas = TABLAS_MYSQL
    else:
        raise ValueError(f"Motor de base de datos no soportado: '{motor}'")

    # Gestor de contexto para asegurar el cierre automático de la conexión
    with abrir_conexion() as conexion:
        if motor == "sqlite":
            # Habilitar soporte de claves foráneas en SQLite
            conexion.execute("PRAGMA foreign_keys = ON;")
            
        with conexion.cursor() as cursor:
            for sql in tablas:
                cursor.execute(sql)
                
        conexion.commit()


if __name__ == "__main__":
    try:
        crear_tablas()
        print("Tablas de EcoTech preparadas correctamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")