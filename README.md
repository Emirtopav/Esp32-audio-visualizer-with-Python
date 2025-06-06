# 📊 32 Bantlı OLED Spektrum Görselleştirici (ESP32 + SSD1306)

Bu proje, **ESP32** ve **128x64 SSD1306 OLED ekran** kullanarak **seri port üzerinden gönderilen 32 bantlık frekans verilerini** görselleştiren basit bir spektrum analizörüdür.  

ESP32, bilgisayardan gelen frekans bant değerlerini okur, verileri yumuşatır ve ekran üzerinde 32 adet çubuk grafik olarak gösterir.

---

## 🔹 Özellikler
- 🔢 **32 frekans bandı için gerçek zamanlı görselleştirme**  
- 🌊 **Veri yumuşatma (smoothing) ile daha akıcı animasyon**  
- 🖥️ **128x64 OLED ekranda çubuk grafik çizimi**  
- 📡 **Seri haberleşme ile kolay veri aktarımı**

---

## ⚙️ Kod Açıklaması

### Kütüphaneler ve Tanımlar
- `Adafruit_SSD1306` ve `Adafruit_GFX` OLED ekran kontrolü için  
- `Wire` I2C haberleşmesi için  
- `NUM_BANDS = 32` : Toplam 32 bant görselleştiriliyor  
- `SMOOTHING_FACTOR = 0.3` : Veri yumuşatma katsayısı  

### Global Değişkenler
- `band_values[]` : Seri porttan alınan ham bant değerleri  
- `smoothed_values[]` : Yumuşatılmış, ekran çizimi için kullanılan bant değerleri  

### setup()
- Seri haberleşme başlatılır (115200 baud)  
- OLED ekran başlatılır ve temizlenir  

### loop()
- Seri portta veri varsa okunur  
- `parseData()` fonksiyonu ile veri virgülle ayrılarak `band_values` dizisine aktarılır  
- `smoothData()` ile önceki değerlerle yumuşatma uygulanır  
- `drawBars()` fonksiyonu ile OLED ekranda 32 çubuk çizilir  

### parseData(String data)
- Gelen string içindeki virgüller baz alınarak her bant değeri ayrılır ve tamsayıya çevrilir  
- Bant değerleri `band_values[]` dizisine aktarılır  

### smoothData()
- Her bant değeri, önceki yumuşatılmış değerle ağırlıklı ortalama alınarak güncellenir  
- Bu sayede ani değişimler yumuşatılır, animasyon daha akıcı olur  

### drawBars()
- OLED ekran temizlenir  
- Her bant için, değerler 0-100 aralığından ekran yüksekliğine ölçeklenir  
- Her bant için dikey çubuklar çizilir  
- OLED ekran güncellenir  

---

## 📌 Notlar
- Seri porttan gelen veriler, 32 adet tam sayı değerini (0-100 arası) virgülle ayrılmış şekilde içermelidir. Örnek:  
  `10,20,15,5,30,45,...\n`  
- OLED ekran I2C adresi `0x3C` olarak ayarlanmıştır.  
- Yumuşatma faktörü 0.3, hız ve akıcılık için ayarlanmıştır. İstersen değiştirebilirsin.  

---

# 📢 🔊 Audio Input

Bu proje, dışarıdan gelen **audio frekans verilerini** seri port üzerinden alır. Bu veriler tipik olarak:

- Ses kaynağından (mikrofon, hat girişi vb.) FFT veya benzeri frekans analizleri yapılarak üretilir,  
- Bilgisayar, ESP32 gibi bir mikrodenetleyiciye seri port aracılığıyla 32 bantlık frekans genlik değerleri olarak gönderilir,  
- ESP32 bu verileri ekran üzerinde görsel olarak gösterir.

Projenin kendisi doğrudan ses sinyali işlemez; ses verisi harici bir cihazda işlenip sayısal veri olarak Arduino'ya aktarılır.

---

# 📊 32-Band OLED Spectrum Visualizer (ESP32 + SSD1306)

This project visualizes 32-band frequency data sent over serial using an **ESP32** and a **128x64 SSD1306 OLED display**.

ESP32 reads the frequency band values from the computer, smooths the data, and draws 32 bar graphs on the OLED screen in real-time.

---

## 🔹 Features
- 🔢 **Real-time visualization for 32 frequency bands**  
- 🌊 **Data smoothing for fluid animation**  
- 🖥️ **Bar graph rendering on 128x64 OLED screen**  
- 📡 **Easy serial data communication**  

---

## ⚙️ Code Overview

### Libraries and Definitions
- Uses `Adafruit_SSD1306` and `Adafruit_GFX` for OLED control  
- `Wire` for I2C communication  
- `NUM_BANDS = 32` for total bands visualized  
- `SMOOTHING_FACTOR = 0.3` controls data smoothing  

### setup()
- Initializes serial communication at 115200 baud  
- Initializes and clears the OLED display  

### loop()
- Checks for incoming serial data  
- Parses the CSV-formatted frequency data into `band_values[]`  
- Smooths the data with `smoothData()`  
- Draws bars on OLED using `drawBars()`  

### parseData(String data)
- Splits incoming string by commas and converts to integers  
- Stores values in `band_values[]` array  

### smoothData()
- Updates each band by weighted average with previous value for smoothing  

### drawBars()
- Clears the display  
- Maps band values (0-100) to screen height  
- Draws vertical bars representing each frequency band  
- Updates the OLED display  

---

## 📌 Notes
- Serial data should be a CSV string with 32 integers (0-100), e.g.:  
  `10,20,15,5,30,45,...\n`  
- OLED I2C address is set to `0x3C`  
- Smoothing factor 0.3 balances responsiveness and smoothness; adjustable as needed  

---

# 📢 🔊 Audio Input

This project receives **audio frequency data** from an external source via serial port. Typically:

- The audio source (microphone, line-in, etc.) is processed with FFT or similar frequency analysis externally,  
- The processed frequency magnitude values (32 bands) are sent via serial to the ESP32,  
- The ESP32 displays the data visually on the OLED screen.

The project itself does not process raw audio signals; it visualizes numerical data received from an external audio processing unit.
