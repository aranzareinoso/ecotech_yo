from datetime import datetime

from src.dominio.indicador import Indicador
from src.persistencia.conexion import (
    abrir_conexion, marcador_sql, obtener_motor,
)


class IndicadorDAO:

    @staticmethod
    def _fila_a_indicador(fila):
        return Indicador(
            fecha=fila[2],
            valor=fila[3],
            fuente=fila[0],
            codigo=fila[1],
            unidad=fila[4],
            verificado_en=fila[5],
        )

    @staticmethod
    def guardar(indicador):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            verificado = datetime.now().isoformat(timespec="seconds")

            if obtener_motor() == "sqlite":
                sql = (
                    "INSERT INTO indicador_api "
                    "(fuente, codigo, fecha, valor, unidad, verificado_en) "
                    f"VALUES ({m}, {m}, {m}, {m}, {m}, {m}) "
                    "ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET "
                    "valor = excluded.valor, "
                    "unidad = excluded.unidad, "
                    "verificado_en = excluded.verificado_en"
                )
            else:
                sql = (
                    "INSERT INTO indicador_api "
                    "(fuente, codigo, fecha, valor, unidad, verificado_en) "
                    f"VALUES ({m}, {m}, {m}, {m}, {m}, {m}) "
                    "ON DUPLICATE KEY UPDATE "
                    "valor = VALUES(valor), "
                    "unidad = VALUES(unidad), "
                    "verificado_en = VALUES(verificado_en)"
                )

            cursor.execute(sql, (
                indicador.fuente, indicador.codigo, indicador.fecha,
                indicador.valor, indicador.unidad, verificado,
            ))
            conexion.commit()
            indicador.verificado_en = verificado
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
                "SELECT fuente, codigo, fecha, valor, unidad, verificado_en "
                "FROM indicador_api ORDER BY fecha DESC"
            )
            return [
                IndicadorDAO._fila_a_indicador(f)
                for f in cursor.fetchall()
            ]
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def ultimo_por_codigo(codigo):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            cursor.execute(
                "SELECT fuente, codigo, fecha, valor, unidad, verificado_en "
                f"FROM indicador_api WHERE codigo = {m} "
                "ORDER BY fecha DESC LIMIT 1",
                (codigo,),
            )
            fila = cursor.fetchone()
            return IndicadorDAO._fila_a_indicador(fila) if fila else None
        finally:
            if conexion:
                conexion.close()