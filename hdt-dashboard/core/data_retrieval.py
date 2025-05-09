from core.adt_client import adt_client
from utils.config import *

from datetime import datetime

def get_patient_info():
    try:
        twin = adt_client.get_digital_twin(PATIENT_TWIN_ID)
        return {
            "Name": twin.get("Name", "Unknown"),
            "Age": twin.get("Age", "Unknown"),
            "Gender": twin.get("Gender", "Unknown"),
            "Diagnosis": twin.get("Diagnosis", "Unknown"),
            "Status": twin.get("Status", "Unknown"),
            "PatientId": twin.get("PatientId", "Unknown")
        }
    except Exception as e:
        print("Error retrieving patient info:", e)
        return {}

def get_room_info():
    try:
        twin = adt_client.get_digital_twin(ROOM_TWIN_ID)
        return {
            "RoomNumber": twin.get("RoomNumber", "Unknown"),
            "RoomType": twin.get("RoomType", "Unknown"),
            "Status": twin.get("Status", "Unknown"),
            "RoomId": twin.get("RoomId", "Unknown")
        }
    except Exception as e:
        print("Error retrieving room info:", e)
        return {}

def get_sensor_info(twin_id, sensor_type):
    try:
        twin = adt_client.get_digital_twin(twin_id)
        if sensor_type == "BodyTemperature":
            return {
                "value": twin.get("Temperature", 0),
                "sensorId": twin.get("BodyTemperatureSensorId", "N/A"),
                "status": twin.get("Status", "Unknown")
            }
        elif sensor_type == "HeartRate":
            return {
                "value": twin.get("HeartRate", 0),
                "sensorId": twin.get("HeartRateSensorId", "N/A"),
                "status": twin.get("Status", "Unknown")
            }
        elif sensor_type == "SpO2":
            return {
                "value": twin.get("SpO2", 0),
                "sensorId": twin.get("SpO2SensorId", "N/A"),
                "status": twin.get("Status", "Unknown")
            }
        elif sensor_type == "RoomTemperature":
            return {
                "value": twin.get("Temperature", 0),
                "sensorId": twin.get("RoomTemperatureSensorId", "N/A"),
                "status": twin.get("Status", "Unknown")
            }
        elif sensor_type == "RoomHumidity":
            return {
                "value": twin.get("Humidity", 0),
                "sensorId": twin.get("RoomHumiditySensorId", "N/A"),
                "status": twin.get("Status", "Unknown")
            }
        else:
            return {}
    except Exception as e:
        print(f"Error retrieving sensor data for {twin_id}:", e)
        return {}

def determine_global_alert(patient_status, room_status):
    return not (patient_status.lower() == "normal" and room_status.lower() == "normal")

def fetch_dashboard_data():
    patient_info = get_patient_info()
    room_info = get_room_info()
    sensor_body_temp = get_sensor_info(BODY_TEMP_SENSOR_ID, "BodyTemperature")
    sensor_heart_rate = get_sensor_info(HEART_RATE_SENSOR_ID, "HeartRate")
    sensor_spo2 = get_sensor_info(SPO2_SENSOR_ID, "SpO2")
    sensor_room_temp = get_sensor_info(ROOM_TEMP_SENSOR_ID, "RoomTemperature")
    sensor_room_humidity = get_sensor_info(ROOM_HUMIDITY_SENSOR_ID, "RoomHumidity")
    show_alert = determine_global_alert(patient_info.get("Status", ""), room_info.get("Status", ""))

    return {
        "timestamp": datetime.now().isoformat(),
        "patient": patient_info,
        "room": room_info,
        "sensors": {
            "bodyTemp": sensor_body_temp,
            "heartRate": sensor_heart_rate,
            "spo2": sensor_spo2,
            "roomTemp": sensor_room_temp,
            "roomHumidity": sensor_room_humidity
        },
        "globalAlert": show_alert
    }
