import json
import time
import subprocess
import paho.mqtt.client as mqtt

# ==============================
# CONFIGURACIÓN
# ==============================

THINGSBOARD_HOST = "demo.thingsboard.io"
ACCESS_TOKEN = "TU_ACCESS_TOKEN_AQUI"

BARCO = "RIOSOLISIV"

# ==============================
# MQTT SETUP
# ==============================

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)

# ==============================
# FUNCIÓN PARA OBTENER LOCATION
# ==============================

def obtener_location():
    try:
        result = subprocess.run(
            ["python3", "dish_grpc_text.py", "location"],
            capture_output=True,
            text=True
        )

        salida = result.stdout.strip()

        partes = salida.split(",")

        lat = float(partes[0])
        lon = float(partes[1])

        return lat, lon

    except Exception as e:
        print("Error obteniendo location:", e)
        return None, None

# ==============================
# LOOP PRINCIPAL
# ==============================

while True:
    lat, lon = obtener_location()

    if lat is not None and lon is not None:
        payload = {
            "barco": BARCO,
            "latitude": lat,
            "longitude": lon
        }

        client.publish("v1/devices/me/telemetry", json.dumps(payload), 1)
        print("Enviado:", payload)

    else:
        print("No se pudo obtener location")

    time.sleep(10)
