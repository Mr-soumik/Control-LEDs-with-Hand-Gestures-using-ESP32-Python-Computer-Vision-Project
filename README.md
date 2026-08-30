# AI Hand Gesture LED Controller using ESP32 & MediaPipe

A real-time computer vision and embedded systems project that detects hand gestures via a webcam using MediaPipe and OpenCV, then controls 5 discrete LEDs via serial communication to an ESP32 microcontroller.

## Subscribe Our Social Media channels

- YouTube: [@techtadka360official](https://youtube.com/@techtadka360official?si=GdlIntZKv30kPgBk)
- Instagram: [@techtadka360official](https://www.instagram.com/techtadka360official?igsh=cWR4bnhjdWw1MHdh)
- Facebook: [TechTadka360](https://www.facebook.com/share/1EkKAJNLdB/
---

## 📌 Features

* **Real-time Finger Counting:** Detects 0 to 5 fingers with high precision using MediaPipe landmark tracking.
* **Serial Interfacing:** Sends real-time finger count packets over USB serial (`115200` baud) to an ESP32.
* **Dynamic LED Mapping:** Progressively illuminates corresponding LEDs (`0` to `5`) based on the recognized hand state.
* **Low Latency:** Event-driven serial transmission ensures fast response without port locking.

---

## 🛠️ Hardware Requirements

* **ESP32 Development Board** (NodeMCU-32S / ESP32 DevKit V1)
* **5x LEDs** (Any standard color: Red/Green/Blue)
* **5x 220Ω Current Limiting Resistors**
* **Breadboard & Jumper Wires**
* **Micro-USB Data Cable**

---

## 🔌 Pin Configuration

| Component | ESP32 GPIO Pin | Description |
| :--- | :--- | :--- |
| LED 1 (Thumb) | `GPIO 18` | Anode (+) via 220Ω Resistor |
| LED 2 (Index) | `GPIO 19` | Anode (+) via 220Ω Resistor |
| LED 3 (Middle) | `GPIO 21` | Anode (+) via 220Ω Resistor |
| LED 4 (Ring) | `GPIO 22` | Anode (+) via 220Ω Resistor |
| LED 5 (Pinky) | `GPIO 23` | Anode (+) via 220Ω Resistor |
| Ground Rail | `GND` | Common Cathode (-) rail for all LEDs |

---

## 💻 Software & Libraries

### Python Requirements
* Python 3.8+
* `opencv-python`
* `mediapipe`
* `pyserial`

Install dependencies via pip:
```bash
pip install opencv-python mediapipe pyserial
