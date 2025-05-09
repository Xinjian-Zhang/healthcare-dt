/*  Sensors.h  --------------------------------------------------------------- */
#pragma once
#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include "heartRate.h"
#include "Protocentral_MAX30205.h"
#include <AM2320_asukiaaa.h>
#include "Constants.h"

namespace Sensors {
  extern MAX30105          particle;
  extern MAX30205          bodyTemp;
  extern AM2320_asukiaaa   room;
}

void initAllSensors();
void readSamples(uint32_t *red, uint32_t *ir, uint8_t count);
void computeHrSpo2(uint32_t *ir, uint32_t *red,
                   int32_t &hr, int8_t &hrValid,
                   int32_t &spo2, int8_t &spo2Valid);
float readBodyTemp();
void  readRoomSensor(float &temp, float &hum);
