/*  DisplayUI.cpp  ----------------------------------------------------------- */
#include "DisplayUI.h"
#include "Constants.h"

static U8GLIB_SSD1306_128X64 oled(U8G_I2C_OPT_NONE | U8G_I2C_OPT_DEV_0);

void initDisplay() {
  oled.setFont(u8g_font_unifont);
}

void showSplash() {
  oled.firstPage();
  do {
    oled.setColorIndex(1);
    oled.drawStr((oled.getWidth() - oled.getStrWidth("Loading...")) / 2, 30,
                 "Loading...");
    oled.drawStr((oled.getWidth() - oled.getStrWidth("xinjian@ut.ee")) / 2, 50,
                 "xinjian@ut.ee");
  } while (oled.nextPage());
}

/* -- Page 0: body vitals --------------------------------------------------- */
void drawVitalsPage(int bpm, int spo2, float temp, bool fingerOnSensor) {
  oled.firstPage();
  do {
    oled.drawStr(0, 16, "HR:");
    oled.drawStr(0, 32, "BO:");
    oled.drawStr(0, 48, "TP:");
    oled.drawStr(0, 64, "ST:");

    if (!fingerOnSensor) {
      oled.drawStr(oled.getStrWidth("ST:"), 64, "Place Finger!");
    } else {
      oled.drawStr(oled.getStrWidth("ST:   "), 64, "OK");
    }

    oled.setPrintPos(48, 15); oled.print(bpm);  oled.print(" bpm");
    oled.setPrintPos(48, 31); oled.print(spo2); oled.print("%");
    oled.setPrintPos(48, 47); oled.print(temp, 1); oled.print(" C");
  } while (oled.nextPage());
}

/* -- Page 1: room conditions ---------------------------------------------- */
void drawRoomPage(float roomTemp, float roomHum) {
  oled.firstPage();
  do {
    oled.drawStr(0, 16, "Room Temp:");
    oled.setPrintPos(96, 16); oled.print(roomTemp, 1); oled.print("C");
    oled.drawStr(0, 32, "Room Hum:");
    oled.setPrintPos(96, 32); oled.print(roomHum, 0); oled.print("%");
  } while (oled.nextPage());
}
