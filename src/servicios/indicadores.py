import requests
from src.servicios.api_dolar import obtener_datos
from src.servicios.api_clima import obtener_clima
from src.servicios.deserializador_indicador import DeserializadorIndicador
from src.servicios.deserializador_clima import DeserializadorClima
from src.persistencia.indicador_dao import IndicadorDAO
from src.persistencia.clima_dao import ClimaDAO
from src.servicios.permisos import exigir_sesion

def consultar_dolar(sesion):
    exigir_sesion(sesion)
    try:
        datos = obtener_datos()
        indicador = DeserializadorIndicador.desde_api(datos)
        origen = "API"
        mensaje = ""
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        indicador = IndicadorDAO.ultimo_por_codigo("dolar")
        origen = "BD local (respaldo)"
        mensaje = "Servicio no disponible. Se muestra el último dato guardado."
        if indicador is None:
            return None, "BD local", "Servicio no disponible y sin respaldo en la BD.", False

    guardado_ok = False
    if origen == "API":
        try:
            IndicadorDAO.guardar(indicador)
            guardado_ok = True
        except Exception as error:
            mensaje = f"Dato obtenido, pero no se pudo guardar: {error}"

    return indicador, origen, mensaje, guardado_ok

def consultar_clima(sesion, ciudad):
    exigir_sesion(sesion)
    try:
        datos = obtener_clima(ciudad)
        clima = DeserializadorClima.desde_api(datos, ciudad)
        origen = "API"
        mensaje = ""
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError) as error:
        return None, "Error", f"No se pudo consultar el clima: {error}", False

    try:
        ClimaDAO.guardar(clima)
        guardado_ok = True
    except Exception as error:
        mensaje = f"Dato obtenido, pero no se pudo guardar: {error}"
        guardado_ok = False

    return clima, origen, mensaje, guardado_ok

def obtener_historial_indicadores(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()

def obtener_historial_clima(sesion):
    exigir_sesion(sesion)
    return ClimaDAO.listar()