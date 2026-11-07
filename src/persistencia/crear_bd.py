from src.persistencia.conexion import abrir_conexion, obtener_motor

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    if obtener_motor() == "sqlite":
        sql_usuario = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            empleado_id INTEGER NOT NULL UNIQUE,
            rol TEXT NOT NULL DEFAULT 'empleado'
                CHECK (rol IN ('admin', 'empleado'))
        )
        """
        sql_indicador = """
        CREATE TABLE IF NOT EXISTS indicador_api (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL,
            codigo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL,
            unidad TEXT NOT NULL,
            verificado_en TEXT,
            UNIQUE (fuente, codigo, fecha)
        )
        """
        sql_clima = """
        CREATE TABLE IF NOT EXISTS clima_api (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciudad TEXT NOT NULL,
            temperatura REAL NOT NULL,
            humedad INTEGER,
            estado TEXT,
            fecha TEXT NOT NULL,
            verificado_en TEXT,
            UNIQUE (ciudad, fecha)
        )
        """
        sql_departamento = """
        CREATE TABLE IF NOT EXISTS departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
        """
        sql_proyecto = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empleado_id INTEGER NOT NULL
        )
        """
        sql_registro_horas = """
        CREATE TABLE IF NOT EXISTS registro_horas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado_id INTEGER NOT NULL,
            proyecto_id INTEGER NOT NULL,
            horas REAL NOT NULL,
            fecha TEXT NOT NULL
        )
        """
    else:
        sql_usuario = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            empleado_id INT NOT NULL UNIQUE,
            rol VARCHAR(20) NOT NULL DEFAULT 'empleado'
        )
        """
        sql_indicador = """
        CREATE TABLE IF NOT EXISTS indicador_api (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fuente VARCHAR(50) NOT NULL,
            codigo VARCHAR(20) NOT NULL,
            fecha VARCHAR(30) NOT NULL,
            valor DOUBLE NOT NULL,
            unidad VARCHAR(20) NOT NULL,
            verificado_en VARCHAR(30),
            UNIQUE KEY uq_indicador (fuente, codigo, fecha)
        )
        """
        sql_clima = """
        CREATE TABLE IF NOT EXISTS clima_api (
            id INT PRIMARY KEY AUTO_INCREMENT,
            ciudad VARCHAR(80) NOT NULL,
            temperatura DOUBLE NOT NULL,
            humedad INT,
            estado VARCHAR(80),
            fecha VARCHAR(30) NOT NULL,
            verificado_en VARCHAR(30),
            UNIQUE KEY uq_clima (ciudad, fecha)
        )
        """
        sql_departamento = """
        CREATE TABLE IF NOT EXISTS departamento (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL UNIQUE
        )
        """
        sql_proyecto = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            empleado_id INT NOT NULL
        )
        """
        sql_registro_horas = """
        CREATE TABLE IF NOT EXISTS registro_horas (
            id INT PRIMARY KEY AUTO_INCREMENT,
            empleado_id INT NOT NULL,
            proyecto_id INT NOT NULL,
            horas DOUBLE NOT NULL,
            fecha VARCHAR(30) NOT NULL
        )
        """

    cursor.execute(sql_usuario)
    cursor.execute(sql_indicador)
    cursor.execute(sql_clima)
    cursor.execute(sql_departamento)
    cursor.execute(sql_proyecto)
    cursor.execute(sql_registro_horas)
    conexion.commit()
    conexion.close()
    print("Base de datos preparada correctamente.")


if __name__ == "__main__":
    crear_tablas()