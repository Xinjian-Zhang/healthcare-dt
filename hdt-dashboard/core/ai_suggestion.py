import os
import openai
from core.data_retrieval import get_patient_info, get_room_info, get_sensor_info
from utils.config import *

# DeepSeek API client
client = openai.OpenAI(
    api_key=os.getenv("DEEPSEEAK_API_KEY"),
    base_url=os.getenv("DEEPSEEAK_BASE_URL", "https://api.deepseek.com")
)

def get_ai_suggestion():
    patient = get_patient_info()
    room = get_room_info()
    sensor_body_temp = get_sensor_info(BODY_TEMP_SENSOR_ID, "BodyTemperature")
    sensor_heart_rate = get_sensor_info(HEART_RATE_SENSOR_ID, "HeartRate")
    sensor_spo2 = get_sensor_info(SPO2_SENSOR_ID, "SpO2")
    sensor_room_temp = get_sensor_info(ROOM_TEMP_SENSOR_ID, "RoomTemperature")
    sensor_room_humidity = get_sensor_info(ROOM_HUMIDITY_SENSOR_ID, "RoomHumidity")

    prompt = (
        f"Patient: {patient.get('Name', 'Unknown')}, Age: {patient.get('Age', 'Unknown')}, "
        f"Gender: {patient.get('Gender', 'Unknown')}, Diagnosis: {patient.get('Diagnosis', 'Unknown')}, "
        f"Status: {patient.get('Status', 'Unknown')}. "
        f"Room: {room.get('RoomNumber', 'Unknown')} ({room.get('RoomType', 'Unknown')}), "
        f"Status: {room.get('Status', 'Unknown')}. "
        f"Sensors: BodyTemp {sensor_body_temp.get('value', 0)} (Status: {sensor_body_temp.get('status', 'Unknown')}), "
        f"HeartRate {sensor_heart_rate.get('value', 0)} (Status: {sensor_heart_rate.get('status', 'Unknown')}), "
        f"SpO2 {sensor_spo2.get('value', 0)} (Status: {sensor_spo2.get('status', 'Unknown')}), "
        f"RoomTemp {sensor_room_temp.get('value', 0)} (Status: {sensor_room_temp.get('status', 'Unknown')}), "
        f"RoomHumidity {sensor_room_humidity.get('value', 0)} (Status: {sensor_room_humidity.get('status', 'Unknown')}). "
        "Provide a concise clinical suggestion within 100 words in a fixed sentence structure."
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful clinical assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        suggestion = response.choices[0].message.content.strip()
        return suggestion
    except Exception as e:
        print("Error during AI suggestion call:", e)
        return "Error generating AI suggestion."
