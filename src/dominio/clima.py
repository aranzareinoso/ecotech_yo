import math
from datetime import datetime

class Clima:
    def __init__(self, ciudad, temperatura, humedad=None, estado=None, fecha=None, verificado_en=None):
        if not isinstance(ciudad, str) or not ciudad.strip():
            raise ValueError("La ciudad es obligatoria.")
        if (type(temperatura) not in (int, float) or not math.isfinite(temperatura)):
            raise ValueError("Temperatura inválida.")
        if humedad is not None and not (0 <= humedad <= 100):
            raise ValueError("Humedad fuera de rango (0-100).")
        if fecha is None:
            fecha = datetime.now().isoformat(timespec="seconds")

        self.ciudad = ciudad.strip().lower()
        self.temperatura = float(temperatura)
        self.humedad = humedad
        self.estado = estado or "desconocido"
        self.fecha = fecha
        self.verificado_en = verificado_en

    def __str__(self):
        return f"Clima en {self.ciudad}: {self.temperatura:.1f}°C, {self.estado}, humedad {self.humedad}%"