from datetime import datetime

from src.dominio.clima import Clima
from src.persistencia.conexion import (
    abrir_conexion, marcador_sql, obtener_motor,
)


class ClimaDAO:

    @staticmethod
    def _fila_a_clima(fila):
        return Clima(
            ciudad=fila[0],
            temperatura=fila[1],
            humedad=fila[2],
            estado=fila[3],
            fecha=fila[4],
            verificado_en=fila[5],
        )

    @staticmethod
    def guardar(clima):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            verificado = datetime.now().isoformat(timespec="seconds")

            if obtener_motor() == "sqlite":
                sql = (
                    "INSERT INTO clima_api "
                    "(ciudad, temperatura, humedad, estado, fecha, verificado_en) "
                    f"VALUES ({m}, {m}, {m}, {m}, {m}, {m}) "
                    "ON CONFLICT (ciudad, fecha) DO UPDATE SET "
                    "temperatura = excluded.temperatura, "
                    "humedad = excluded.humedad, "
                    "estado = excluded.estado, "
                    "verificado_en = excluded.verificado_en"
                )
            else:
                sql = (
                    "INSERT INTO clima_api "
                    "(ciudad, temperatura, humedad, estado, fecha, verificado_en) "
                    f"VALUES ({m}, {m}, {m}, {m}, {m}, {m}) "
                    "ON DUPLICATE KEY UPDATE "
                    "temperatura = VALUES(temperatura), "
                    "humedad = VALUES(humedad), "
                    "estado = VALUES(estado), "
                    "verificado_en = VALUES(verificado_en)"
                )

            cursor.execute(sql, (
                clima.ciudad, clima.temperatura, clima.humedad,
                clima.estado, clima.fecha, verificado,
            ))
            conexion.commit()
            clima.verificado_en = verificado
            return True
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT ciudad, temperatura, humedad, estado, fecha, "
                "verificado_en FROM clima_api ORDER BY fecha DESC"
            )
            return [
                ClimaDAO._fila_a_clima(f)
                for f in cursor.fetchall()
            ]
        finally:
            if conexion:
                conexion.close()