import os
import json
import time
from datetime import datetime
from threading import Lock

from adt_utils import get_twin_property
from blockchain_utils import encrypt_file, store_key_on_blockchain

aggregation_lock = Lock()
aggregated_data = []

def save_data_to_file(data, folder="data"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = os.path.join(folder, f"sensor_data_{timestamp}.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")
    return filename

def process_aggregation():
    global aggregated_data
    with aggregation_lock:
        data_to_process = aggregated_data.copy()
        aggregated_data = []
    if not data_to_process:
        print("No data to aggregate.")
        return
    file_path = save_data_to_file(data_to_process)
    encryption_key = encrypt_file(file_path)
    sensor_ids = [
        get_twin_property("BodyTempSensor1", "BodyTemperatureSensorId"),
        get_twin_property("HeartRateSensor1", "HeartRateSensorId"),
        get_twin_property("SpO2Sensor1", "SpO2SensorId"),
        get_twin_property("RoomTempSensor1", "RoomTemperatureSensorId"),
        get_twin_property("RoomHumiditySensor1", "RoomHumiditySensorId")
    ]
    sensor_ids_str = ",".join(filter(None, sensor_ids))
    if sensor_ids_str:
        store_key_on_blockchain(sensor_ids_str, encryption_key, file_path)
