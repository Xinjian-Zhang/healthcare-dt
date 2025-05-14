# Healthcare IoT Firmware (Arduino)

This provide a firmware for Arduino board to collect data of **heart-rate**, **SpO₂**, **body temperature** 
and ambient  **temperature / humidity**, shows them on a 128 × 64 OLED and streams
a compact line over Serial (~10 Hz).

| Sensor | Purpose | Library |
|--------|---------|---------|
| MAX30105 / MAX30102 | PPG (HR & SpO₂) | `SparkFun MAX3010x` |
| MAX30205 | Body temperature | `Protocentral_MAX30205` |
| AM2320 | Room T & RH | `AM2320_asukiaaa` |
| SSD1306 OLED | 128×64 UI | `U8glib` |

## Wiring (I²C)

| Pin | Module |
| --- | --- |
| 3.3V | MAX30102, MAX30205, AM2320, OLED12864 |
| 5V | MAX30102, MAX30205, AM2320, OLED12864 |
| GND | Ground for All |
| 20 (SDA) | I²C Data Line for MAX30102, MAX30205, AM2320, OLED12864 |
| 21 (SCL) | I²C Clock Line for MAX30102, MAX30205, AM2320, OLED12864 |

> **Tip** – All three sensors share the same I²C bus.

## Building

1. Install the four libraries above with the Arduino Library Manager.  
2. Open **healthcare-iot-firmware.ino** in Arduino IDE.
3. Select your board/port → *Upload*.

## Serial Output Format
```
data#<HR>&<SpO2>&<BodyTemp>&<FingerFlag>&<RoomTemp>&<RoomHum>&end#
```

---

## About

> This code is as a part of a Master's thesis project.

- Author: Xinjian Zhang
- [Github Link](https://github.com/Xinjian-Zhang)

---
