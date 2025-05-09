/*  Sensors.cpp  ------------------------------------------------------------- */
#include "Sensors.h"

MAX30105          Sensors::particle;
MAX30205          Sensors::bodyTemp;
AM2320_asukiaaa   Sensors::room;

static const byte LED_BRIGHTNESS = 50;
static const byte SAMPLE_AVG     = 4;
static const byte LED_MODE       = 2;      // red + IR
static const byte SAMPLE_RATE    = 100;
static const int  PULSE_WIDTH    = 411;
static const int  ADC_RANGE      = 4096;

/* -- init ----------------------------------------------------------------- */
void initAllSensors() {

  // Block until MAX30205 detected (prevents endless error loops later)
  while (!Sensors::bodyTemp.scanAvailableSensors()) delay(1000);
  Sensors::bodyTemp.begin();          // continuous mode

  if (!Sensors::particle.begin(Wire, I2C_SPEED_FAST)) {
    while (true) {                    // fatal – stay here
      Serial.println(F("MAX30105 NOT FOUND"));
      delay(2000);
    }
  }
  Sensors::particle.setup(LED_BRIGHTNESS, SAMPLE_AVG, LED_MODE,
                          SAMPLE_RATE, PULSE_WIDTH, ADC_RANGE);
  Sensors::particle.enableDIETEMPRDY();

  Sensors::room.setWire(&Wire);
}

/* -- sample helpers ------------------------------------------------------- */
void readSamples(uint32_t *red, uint32_t *ir, uint8_t count) {
  for (uint8_t i = 0; i < count; ++i) {
    while (!Sensors::particle.available()) Sensors::particle.check();
    red[i] = Sensors::particle.getRed();
    ir[i]  = Sensors::particle.getIR();
    Sensors::particle.nextSample();
  }
}

void computeHrSpo2(uint32_t *ir, uint32_t *red,
                   int32_t &hr, int8_t &hrValid,
                   int32_t &spo2, int8_t &spo2Valid) {

  maxim_heart_rate_and_oxygen_saturation(ir,
                                         BUFFER_LEN,
                                         red,
                                         &spo2,
                                         &spo2Valid,
                                         &hr,
                                         &hrValid);
}

float readBodyTemp() {
  return Sensors::bodyTemp.getTemperature();   // °C
}

void readRoomSensor(float &temp, float &hum) {
  if (Sensors::room.update() == 0) {
    temp = Sensors::room.temperatureC;
    hum  = Sensors::room.humidity;
  }
}
