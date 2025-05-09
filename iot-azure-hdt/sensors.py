def evaluate_body_temp_status(temp):
    return "Too Low" if temp < 36.0 else "Too High" if temp > 37.5 else "Normal"

def evaluate_heart_rate_status(hr):
    return "Too Low" if hr < 60 else "Too High" if hr > 100 else "Normal"

def evaluate_spo2_status(spo2):
    return "Too Low" if spo2 < 95 else "Normal"

def evaluate_room_temp_status(temp):
    return "Too Low" if temp < 18 else "Too High" if temp > 25 else "Normal"

def evaluate_room_humidity_status(humidity):
    return "Too Low" if humidity < 30 else "Too High" if humidity > 60 else "Normal"

def determine_patient_status(sensor_data, flag):
    if flag == 0:
        return "Alert"
    hr = sensor_data.get("HeartRate", 0)
    spo2 = sensor_data.get("SpO2", 100)
    body_temp = sensor_data.get("BodyTemperature", 37)
    return "Critical" if hr < 40 or hr > 180 or spo2 < 90 or body_temp < 35 or body_temp > 39 else "Normal"

def determine_room_status(sensor_data):
    room_temp = sensor_data.get("RoomTemperature", 22)
    room_humidity = sensor_data.get("RoomHumidity", 45)
    return "Abnormal" if room_temp < 18 or room_temp > 25 or room_humidity < 30 or room_humidity > 60 else "Normal"
