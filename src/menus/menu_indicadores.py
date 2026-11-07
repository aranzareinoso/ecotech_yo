from src.servicios.indicadores import (
    consultar_dolar, consultar_clima,
    obtener_historial_indicadores, obtener_historial_clima,
)
from src.servicios.api_clima import CIUDADES

def menu_indicadores(usuario_actual):
    while True:
        print("\n=== MENÚ DE INDICADORES ===")
        print("1. Consultar dólar actualizado")
        print("2. Ver historial del dólar")
        print("3. Consultar clima de una ciudad")
        print("4. Ver historial de clima")
        print("0. Volver al menú principal")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            return
        elif opcion == "1":
            _consultar_dolar(usuario_actual)
        elif opcion == "2":
            _historial_dolar(usuario_actual)
        elif opcion == "3":
            _consultar_clima(usuario_actual)
        elif opcion == "4":
            _historial_clima(usuario_actual)
        else:
            print("Opción no válida.")

def _consultar_dolar(sesion):
    resultado = consultar_dolar(sesion)
    indicador, origen, mensaje, guardado = resultado
    if indicador is None:
        print(mensaje)
        return
    print(f"\nDólar: {indicador.valor:.2f} {indicador.unidad}")
    print(f"Fecha del dato: {indicador.fecha}")
    print(f"Origen: {origen}")
    if mensaje:
        print(f"Aviso: {mensaje}")
    if guardado:
        print("Guardado en BD confirmado.")

def _historial_dolar(sesion):
    try:
        historial = obtener_historial_indicadores(sesion)
    except PermissionError as error:
        print(error)
        return
    if not historial:
        print("Aún no existe historial.")
        return
    print("\nFecha           Valor       Unidad")
    for d in historial:
        print(f"{d.fecha:<15} {d.valor:>8.2f}   {d.unidad}")

def _consultar_clima(sesion):
    print(f"Ciudades disponibles: {', '.join(CIUDADES)}")
    ciudad = input("Ciudad: ").strip()
    resultado = consultar_clima(sesion, ciudad)
    clima, origen, mensaje, guardado = resultado
    if clima is None:
        print(mensaje)
        return
    print(f"\n{clima}")
    print(f"Fecha: {clima.fecha}")
    print(f"Origen: {origen}")
    if mensaje:
        print(f"Aviso: {mensaje}")
    if guardado:
        print("Guardado en BD confirmado.")

def _historial_clima(sesion):
    try:
        historial = obtener_historial_clima(sesion)
    except PermissionError as error:
        print(error)
        return
    if not historial:
        print("Aún no existe historial de clima.")
        return
    print("\nCiudad        Fecha           Temp    Estado")
    for c in historial:
        print(f"{c.ciudad:<12}  {c.fecha:<15} {c.temperatura:>6.1f}  {c.estado}")