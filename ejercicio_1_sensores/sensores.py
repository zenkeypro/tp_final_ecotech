def limpiar_registro_sensor(registro_raw):
    registro_limpio = {}

    sensor_id_raw = registro_raw.get("sensor_id", "")
    registro_limpio["sensor_id"] = sensor_id_raw.strip()

    temperatura_raw = registro_raw.get("temperatura", "0")
    temperatura_clean = temperatura_raw.replace("C", "").replace("°", "").strip()
    registro_limpio["temperatura"] = float(temperatura_clean)

    ubicacion_raw = registro_raw.get("ubicacion", "")
    if ubicacion_raw is None or str(ubicacion_raw).strip() == "":
        registro_limpio["ubicacion"] = "Área No Asignada"
    else:
        registro_limpio["ubicacion"] = str(ubicacion_raw).strip()

    return registro_limpio

def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    if not lista_sensores_limpios:
        return [], 0.0

    lista_sensores_alerta = []
    temperatura_total = 0.0

    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])
        temperatura_total += temperatura

    promedio_temperatura = round(temperatura_total / len(lista_sensores_limpios), 2)

    return lista_sensores_alerta, promedio_temperatura

if __name__ == "__main__":
    datos_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": " SENSOR-002 ", "temperatura": "30.1C", "ubicacion": ""},
        {"sensor_id": " SENSOR-003 ", "temperatura": "27.8C"},
    ]

    umbral = 30.0

    print("--- Sanitización de registros ---")
    sensores_limpios = [limpiar_registro_sensor(r) for r in datos_crudos]
    for sensor in sensores_limpios:
        print(sensor)

    print("\n--- Generando Reporte Consolidado ---")
    alertas, promedio = generar_resumen_sensores(sensores_limpios, umbral_temperatura=umbral)
    print(f"Sensores en alerta (> {umbral}°C): {alertas}")
    print(f"Promedio de temperatura global: {promedio}°C")