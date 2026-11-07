from src.dominio.indicador import Indicador
from src.servicios.api_dolar import extraer_primero

class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        fecha, valor = extraer_primero(datos)
        return Indicador(fecha=fecha, valor=valor)