import serial
import threading
import time
from datetime import datetime

from config import SERIAL_PORT, BAUD_RATE, READ_INTERVAL
from adt_utils import upsert_property, update_status, get_twin_property
from sensors import (
    evaluate_body_temp_status, evaluate_heart_rate_status, evaluate_spo2_status,
    evaluate_room_temp_status, evaluate_room_humidity_status,
    determine_patient_status, determine_room_status
)
from parser import parse_sensor_data
from aggregator import aggregated_data, aggregation_lock, process_aggregation

# ADT Twin IDs
PATIENT_TWIN_ID = "Patinet1"
ROOM_TWIN_ID = "Room1"
BODY_TEMP_SENSOR_ID = "BodyTempSensor1"
HEART_RATE_SENSOR_ID = "HeartRateSensor1"
SPO2_SENSOR_ID = "SpO2Sensor1"
ROOM_TEMP_SENSOR_ID = "RoomTempSensor1"
ROOM_HUMIDITY_SENSOR_ID = "RoomHumiditySensor1"

def main():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Serial port {SERIAL_PORT} opened at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return

    last_agg_time = time.time()

    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                print(f"Received: {line}")
                sensor_data = parse_sensor_data(line)
                if sensor_data:
                    patient_status = determine_patient_status(sensor_data, sensor_data.get("Flag", 1))
                    room_status = determine_room_status(sensor_data)

                    # Upload sensor data to ADT
                    upsert_property(BODY_TEMP_SENSOR_ID, "Temperature", sensor_data["BodyTemperature"])
                    upsert_property(HEART_RATE_SENSOR_ID, "HeartRate", sensor_data["HeartRate"])
                    upsert_property(SPO2_SENSOR_ID, "SpO2", sensor_data["SpO2"])
                    upsert_property(ROOM_TEMP_SENSOR_ID, "Temperature", sensor_data["RoomTemperature"])
                    upsert_property(ROOM_HUMIDITY_SENSOR_ID, "Humidity", sensor_data["RoomHumidity"])

                    # Upload evaluation results to ADT
                    upsert_property(BODY_TEMP_SENSOR_ID, "Status", evaluate_body_temp_status(sensor_data["BodyTemperature"]))
                    upsert_property(HEART_RATE_SENSOR_ID, "Status", evaluate_heart_rate_status(sensor_data["HeartRate"]))
                    upsert_property(SPO2_SENSOR_ID, "Status", evaluate_spo2_status(sensor_data["SpO2"]))
                    upsert_property(ROOM_TEMP_SENSOR_ID, "Status", evaluate_room_temp_status(sensor_data["RoomTemperature"]))
                    upsert_property(ROOM_HUMIDITY_SENSOR_ID, "Status", evaluate_room_humidity_status(sensor_data["RoomHumidity"]))

                    update_status(PATIENT_TWIN_ID, patient_status)
                    update_status(ROOM_TWIN_ID, room_status)

                    record = {
                        "timestamp": datetime.now().isoformat(),
                        "data": sensor_data,
                        "sensorIds": {
                            "BodyTemperatureSensorId": get_twin_property(BODY_TEMP_SENSOR_ID, "BodyTemperatureSensorId"),
                            "HeartRateSensorId": get_twin_property(HEART_RATE_SENSOR_ID, "HeartRateSensorId"),
                            "SpO2SensorId": get_twin_property(SPO2_SENSOR_ID, "SpO2SensorId"),
                            "RoomTemperatureSensorId": get_twin_property(ROOM_TEMP_SENSOR_ID, "RoomTemperatureSensorId"),
                            "RoomHumiditySensorId": get_twin_property(ROOM_HUMIDITY_SENSOR_ID, "RoomHumiditySensorId")
                        }
                    }

                    with aggregation_lock:
                        aggregated_data.append(record)
                else:
                    print("Data parsing failed.")

            if time.time() - last_agg_time >= 30:
                threading.Thread(target=process_aggregation).start()
                last_agg_time = time.time()

            time.sleep(READ_INTERVAL)

        except KeyboardInterrupt:
            print("Program stopped manually.")
            break
        except Exception as e:
            print(f"Runtime error: {e}")

if __name__ == "__main__":
    main()
