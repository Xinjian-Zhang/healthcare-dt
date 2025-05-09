import re

def parse_sensor_data(line):
    pattern = r"^data#([\d\.]+)&([\d\.]+)&([\d\.]+)&(\d+)&([\d\.]+)&([\d\.]+)&end#$"
    match = re.match(pattern, line.strip())
    if match:
        try:
            return {
                "HeartRate": int(float(match.group(1))),
                "SpO2": float(match.group(2)),
                "BodyTemperature": float(match.group(3)),
                "Flag": int(match.group(4)),
                "RoomTemperature": float(match.group(5)),
                "RoomHumidity": float(match.group(6))
            }
        except Exception as e:
            print(f"Data conversion error: {e}")
            return None
    return None
