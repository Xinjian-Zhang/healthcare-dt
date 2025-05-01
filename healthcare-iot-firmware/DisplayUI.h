/*  DisplayUI.h  ------------------------------------------------------------- */
#pragma once
#include <U8glib.h>

void initDisplay();
void showSplash();
void drawVitalsPage(int bpm, int spo2, float temp, bool fingerOnSensor);
void drawRoomPage(float roomTemp, float roomHum);
