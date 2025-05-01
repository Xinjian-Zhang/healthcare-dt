/*  Constants.h  ------------------------------------------------------------- */

#pragma once
#include <Arduino.h>

// -- Display
#define READ_LED_PIN         13       // onboard “heartbeat” LED
#define PAGE_INTERVAL_MS  2000        // switch OLED page every 2s

// -- MAX3010x & HR calculation
const uint8_t  HR_SCALE            = 3000;     // crude scaling for IR → BPM
const long     FINGER_IR_THRESHOLD = 50000;
const int32_t  INVALID_SPO2        = -999;

// -- Sample buffer
const uint8_t  BUFFER_LEN          = 100;      // 4s at 25 SPS
const uint8_t  NEW_SAMPLE_BLOCK    = 25;       // 1s of fresh data
