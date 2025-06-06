/*
  MIT License
  Copyright (c) 2025 Emirtopav
  
  This code is licensed under the MIT License.
  See LICENSE file for details.
*/
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define NUM_BANDS     32  // 32 bantlı görselleştirme
#define SMOOTHING_FACTOR 0.3  // Yumuşatma faktörü

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

float band_values[NUM_BANDS] = {0};  // Gerçek bant değerleri
float smoothed_values[NUM_BANDS] = {0};  // Yumuşatılmış bant değerleri

void setup() {
  Serial.begin(115200);

  // OLED Ekranı Başlat
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();
  display.display();
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    parseData(data);
    smoothData();
    drawBars();
  }
}

void parseData(String data) {
  int index = 0;
  int start = 0;
  int end = data.indexOf(',');

  while (end != -1 && index < NUM_BANDS) {
    band_values[index] = data.substring(start, end).toInt();
    start = end + 1;
    end = data.indexOf(',', start);
    index++;
  }
}

void smoothData() {
  for (int i = 0; i < NUM_BANDS; i++) {
    smoothed_values[i] = smoothed_values[i] * (1 - SMOOTHING_FACTOR) + band_values[i] * SMOOTHING_FACTOR;
  }
}

void drawBars() {
  display.clearDisplay();

  int barWidth = SCREEN_WIDTH / NUM_BANDS;  // Her bir çubuğun genişliği
  for (int i = 0; i < NUM_BANDS; i++) {
    int barHeight = map((int)smoothed_values[i], 0, 100, 0, SCREEN_HEIGHT);
    display.fillRect(i * barWidth, SCREEN_HEIGHT - barHeight, barWidth - 1, barHeight, SSD1306_WHITE);
  }

  display.display();
}
