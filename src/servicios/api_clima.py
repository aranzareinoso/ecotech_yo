import requests

URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = (3, 5)

CIUDADES = {
    "la serena": {"lat": -29.9027, "lon": -71.2519},
    "santiago": {"lat": -33.4489, "lon": -70.6693},
    "valparaiso": {"lat": -33.0472, "lon": -71.6127},
    "concepcion": {"lat": -36.8201, "lon": -73.0444},
}

ESTADOS_WMO = {
    0: "cielo despejado", 1: "mayormente despejado",
    2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 48: "niebla con escarcha",
    51: "llovizna ligera", 61: "lluvia ligera",
    63: "lluvia moderada", 65: "lluvia fuerte",
    71: "nieve ligera", 80: "chubascos",
    95: "tormenta", 96: "tormenta con granizo",
}


def obtener_clima(ciudad):
    ciudad_norm = ciudad.strip().lower()
    if ciudad_norm not in CIUDADES:
        raise ValueError(
            f"Ciudad no soportada. Opciones: {', '.join(CIUDADES)}"
        )

    coords = CIUDADES[ciudad_norm]
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "auto",
    }

    respuesta = requests.get(URL_CLIMA, params=params, timeout=TIMEOUT)
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_clima(datos, ciudad):
    if not isinstance(datos, dict):
        raise ValueError("Respuesta de clima inesperada.")

    actual = datos.get("current")
    if not isinstance(actual, dict):
        raise ValueError("La respuesta no contiene datos actuales.")

    temperatura = actual.get("temperature_2m")
    humedad = actual.get("relative_humidity_2m")
    codigo = actual.get("weather_code")
    fecha = actual.get("time")

    if temperatura is None or fecha is None:
        raise ValueError("Faltan datos obligatorios de clima.")

    return {
        "ciudad": ciudad,
        "temperatura": temperatura,
        "humedad": humedad,
        "estado": ESTADOS_WMO.get(codigo, "desconocido"),
        "fecha": fecha,
    }
