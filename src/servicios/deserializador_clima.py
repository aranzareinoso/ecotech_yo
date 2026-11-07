from src.dominio.clima import Clima
from src.servicios.api_clima import extraer_clima

class DeserializadorClima:
    @staticmethod
    def desde_api(datos, ciudad):
        info = extraer_clima(datos, ciudad)
        return Clima(**info)