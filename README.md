# ✨ Kawaii OLED Star Hair Clip (Pico & ESP32 Editions) 🌟

A compact, wearable, and adorable animated star hair clip featuring a smooth, chubby 5-pointed cartoon star silhouette with dynamic facial expressions, sparkling background dust, and a minimalist direct-battery power setup. This repository contains implementations for both the **Raspberry Pi Pico (MicroPython)** and the **ESP32 (Arduino C++)**.

---

## 🛠️ Hardware Components

* **Microcontroller Options**: 
  * Raspberry Pi Pico 
  * ESP32 Development Board
* **Display**: 0.96-inch 128x64 I2C OLED Display (SSD1306 driver, address `0x3C`)
* **Power Supply**: 3.7V LiPo Battery (150–300mAh recommended for lightweight hair-clip wearability)
* **Connecting Wires**

---

## ⚡ Wiring & Pinouts

### 1. Raspberry Pi Pico (MicroPython)
| OLED Pin | Pico Pin | Description |
| :--- | :--- | :--- |
| **VCC** | **3V3** (Pin 36) | Power Supply[cite: 1] |
| **GND** | **GND** (Pin 38) | Ground[cite: 1] |
| **SCL** | **GP1** (Pin 2) | I2C Clock[cite: 1] |
| **SDA** | **GP0** (Pin 1) | I2C Data[cite: 1] |

### 2. ESP32 (Arduino C++)
| OLED Pin | ESP32 Pin | Description |
| :--- | :--- | :--- |
| **VCC** | **3V3** | Power Supply |
| **GND** | **GND** | Ground |
| **SCL** | **GPIO 22** (SCL) | I2C Clock |
| **SDA** | **GPIO 21** (SDA) | I2C Data |

---


For battery power, connect the 3.7V LiPo battery's Red wire to VSYS and Black wire to GND on the Raspberry Pi Pico.
