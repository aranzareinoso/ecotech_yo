import math
from datetime import datetime

class Indicador:
    def __init__(self, fecha, valor, fuente="api_dolar_curso", codigo="dolar", unidad="CLP/USD", verificado_en=None):
        if not isinstance(fecha, str) or not fecha:
            raise ValueError("La fecha debe ser texto no vacío.")
        try:
            datetime.fromisoformat(fecha.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"Fecha inválida: {fecha}") from error

        if (type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0):
            raise ValueError("Valor del indicador inválido.")

        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente
        self.codigo = codigo
        self.unidad = unidad
        self.verificado_en = verificado_en

    def __str__(self):
        return f"{self.codigo}: {self.valor:.2f} {self.unidad} (fecha {self.fecha}, fuente {self.fuente})"