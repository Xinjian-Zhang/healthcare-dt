/*  healthcare-iot-firmware  --------------------------------------------------------
    An IoT formware that support collect data of heart-rate, SpO2, body temperature
    and ambient temperature / humidity, then shows them on a 128×64 SSD1306 OLED
    and streams a compact line over Serial every 100 ms.

    Hardware:
      • MAX30105             – pulse & SpO2
      • MAX30205             – body temperature
      • AM2320               – room temperature & humidity
      • SSD1306-based OLED   – 128 × 64, I²C
    Author:  Xinjian Zhang
    ------------------------------------------------------------------------- */

    #include "Constants.h"
    #include "Sensors.h"
    #include "DisplayUI.h"
    
    // --- Global state -----------------------------------------------------------
    uint32_t irBuf[BUFFER_LEN];
    uint32_t redBuf[BUFFER_LEN];
    
    int32_t   heartRate     = 0;
    int8_t    heartRateOk   = 0;
    int32_t   spo2          = 0;
    int8_t    spo2Ok        = 0;
    
    unsigned long lastPageFlip   = 0;
    uint8_t       currentPage    = 0;      // 0 = body values, 1 = room values
    
    // --- Setup ------------------------------------------------------------------
    void setup() {
      Serial.begin(115200);
      Wire.begin();
      
      pinMode(READ_LED_PIN, OUTPUT);
    
      initDisplay();
      showSplash();
    
      initAllSensors();     // sensors.cpp – blocks until hardware is present
    }
    
    // --- Loop -------------------------------------------------------------------
    void loop() {
    
      /* 1 – Fill first buffer (apprx. 4s at 25 SPS) */
      readSamples(redBuf, irBuf, BUFFER_LEN);
    
      /* 2 – Compute initial HR & SpO2 */
      computeHrSpo2(irBuf, redBuf,
                    heartRate, heartRateOk,
                    spo2,      spo2Ok);
    
      /* 3 – Continuous monitoring */
      while (true) {
        /* 3.1 – Shift last 75 samples to the front and read 25 new ones */
        memmove(redBuf, redBuf + NEW_SAMPLE_BLOCK, sizeof(uint32_t) * (BUFFER_LEN - NEW_SAMPLE_BLOCK));
        memmove(irBuf,  irBuf  + NEW_SAMPLE_BLOCK, sizeof(uint32_t) * (BUFFER_LEN - NEW_SAMPLE_BLOCK));
        readSamples(redBuf + (BUFFER_LEN - NEW_SAMPLE_BLOCK),
                    irBuf  + (BUFFER_LEN - NEW_SAMPLE_BLOCK),
                    NEW_SAMPLE_BLOCK);
    
        /* 3.2 – Re-compute HR & SpO2 */
        computeHrSpo2(irBuf, redBuf,
                      heartRate, heartRateOk,
                      spo2,      spo2Ok);
    
        /* 3.3 – Read auxiliary sensors (non-blocking) */
        float bodyTemp  = readBodyTemp();          // °C
        float roomTemp  = NAN, roomHum = NAN;
        readRoomSensor(roomTemp, roomHum);         // updates only if data ready
    
        long  irValue   = Sensors::particle.getIR();   // current IR raw
    
        /* 3.4 – Prepare display */
        bool  fingerPresent = irValue >= FINGER_IR_THRESHOLD;
        if (spo2 == INVALID_SPO2) spo2 = 95;       // graceful fallback
    
        if (millis() - lastPageFlip > PAGE_INTERVAL_MS) {
          lastPageFlip = millis();
          if (currentPage == 0) {
            drawVitalsPage(heartRate / HR_SCALE,
                           spo2,
                           bodyTemp,
                           fingerPresent);
          } else {
            drawRoomPage(roomTemp, roomHum);
          }
          currentPage ^= 1;                        // toggle page
        }
        digitalWrite(READ_LED_PIN, !digitalRead(READ_LED_PIN));  // visual heartbeat
    
        /* 3.5 – Serial packet */
        Serial.print(F("data#"));
        Serial.print(heartRate / HR_SCALE); Serial.print('&');
        Serial.print(spo2);               Serial.print('&');
        Serial.print(bodyTemp);           Serial.print('&');
        Serial.print(fingerPresent);      Serial.print('&');
        Serial.print(roomTemp);           Serial.print('&');
        Serial.print(roomHum);            Serial.println("&end#");
    
        delay(100);  // keep overall loop rate ~10 Hz
      }
    }
    