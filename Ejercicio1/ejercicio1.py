import re


def limpiar_registro_sensor(registro_raw):
    """
    Normaliza un registro crudo de sensor.
    """
    if not isinstance(registro_raw, dict):
        raise TypeError("El registro debe ser un diccionario.")

    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    temp_raw = registro_raw.get("temperatura")
    if temp_raw is None:
        raise ValueError("El registro no contiene temperatura.")

    if isinstance(temp_raw, (int, float)):
        temperatura = float(temp_raw)
    else:
        texto = str(temp_raw).strip().replace(",", ".")
        coincidencia = re.search(r"[-+]?\d+(?:\.\d+)?", texto)
        if not coincidencia:
            raise ValueError(f"Temperatura no válida: {temp_raw!r}")
        temperatura = float(coincidencia.group())

    ubicacion_raw = registro_raw.get("ubicacion")
    if ubicacion_raw is None or str(ubicacion_raw).strip() == "":
        ubicacion = "No especificada"
    else:
        ubicacion = str(ubicacion_raw).strip()

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Retorna una tupla: (lista_de_ids_en_alerta, promedio_temperatura_global)
    """
    if not lista_sensores_limpios:
        return [], 0.0

    ids_alerta = [
        sensor["sensor_id"]
        for sensor in lista_sensores_limpios
        if sensor["temperatura"] > umbral_temperatura
    ]

    promedio = (
        sum(sensor["temperatura"] for sensor in lista_sensores_limpios)
        / len(lista_sensores_limpios)
    )

    return ids_alerta, promedio


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "27,8 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003 ", "temperatura": "22.1C"},
        {"sensor_id": "SENSOR-004", "temperatura": 30.2, "ubicacion": "  Planta Centro  "},
    ]

    sensores_limpios = [
        limpiar_registro_sensor(registro)
        for registro in registros_crudos
    ]

    umbral = 25.0
    alertas, promedio = generar_resumen_sensores(sensores_limpios, umbral)

    print("=== REGISTROS NORMALIZADOS ===")
    for sensor in sensores_limpios:
        print(sensor)

    print("\n=== REPORTE CONSOLIDADO ===")
    print(f"Promedio global de temperatura: {promedio:.2f} °C")
    print(f"Umbral de alerta: {umbral:.2f} °C")
    print(f"Sensores en alerta: {alertas}")