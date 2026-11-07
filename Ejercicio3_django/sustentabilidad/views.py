from django.shortcuts import render

def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo de kWh no puede ser negativo.")
    return consumo_kwh * factor_emision

def obtener_metricas_consumo(registros):
    if not registros:
        return {"total_emisiones": 0.0, "planta_mayor_consumo": None, "mayor_consumo_kwh": 0.0}

    total_emisiones = 0.0
    consumo_por_planta = {}

    for registro in registros:
        planta = str(registro.get("planta", "Sin planta")).strip() or "Sin planta"
        consumo = float(registro.get("consumo_kwh", 0))

        total_emisiones += calcular_emisiones_carbono(consumo)
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0.0) + consumo

    planta_mayor = max(consumo_por_planta, key=consumo_por_planta.get)

    return {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor,
        "mayor_consumo_kwh": consumo_por_planta[planta_mayor],
    }

def vista_panel_sustentabilidad(request):
    # Simulamos los datos que vendrían de una base de datos o API
    registros = [
        {"planta": "Planta Norte", "consumo_kwh": 1200},
        {"planta": "Planta Sur", "consumo_kwh": 800},
        {"planta": "Planta Norte", "consumo_kwh": 300},
        {"planta": "Planta Centro", "consumo_kwh": 1500},
    ]

    metricas = obtener_metricas_consumo(registros)

    contexto = {
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "mayor_consumo_kwh": metricas["mayor_consumo_kwh"],
        "registros": registros,
    }

    return render(request, "sustentabilidad/panel.html", contexto)