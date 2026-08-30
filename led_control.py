import cv2
import mediapipe as mp
import serial
import time

# --- ESP32 SERIAL SETUP ---
SERIAL_PORT = 'COM7'  # Verify your ESP32 COM port in Device Manager
BAUD_RATE = 115200

try:
    esp32 = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)  # Wait for ESP32 auto-reset after serial connection
    print(f"Connected to ESP32 on {SERIAL_PORT}")
except Exception as e:
    print(f"Serial Error: {e}")
    esp32 = None

# --- MEDIAPIPE SETUP ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

# Custom drawing style: Red points and white connections
landmark_draw_spec = mp.solutions.drawing_utils.DrawingSpec(
    color=(0, 0, 255), thickness=cv2.FILLED, circle_radius=5
)
connection_draw_spec = mp.solutions.drawing_utils.DrawingSpec(
    color=(240, 240, 240), thickness=2
)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

tip_ids = [4, 8, 12, 16, 20]   # Thumb, Index, Middle, Ring, Pinky tips
pip_ids = [2, 6, 10, 14, 18]   # Knuckle joints

prev_count = -1

while True:
    success, frame = cap.read()
    if not success:
        continue

    # Flip horizontally for natural mirror behavior
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # Draw standard skeleton without extra pink lines/dots
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_lms, mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_draw_spec,
                connection_drawing_spec=connection_draw_spec
            )

            lm_list = []
            for lm in hand_lms.landmark:
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            fingers = []

            # 1. Thumb detection (checks horizontal position against palm orientation)
            if lm_list[17][0] < lm_list[5][0]:  # Right hand facing camera
                fingers.append(1 if lm_list[4][0] > lm_list[3][0] else 0)
            else:  # Left hand facing camera
                fingers.append(1 if lm_list[4][0] < lm_list[3][0] else 0)

            # 2. Other 4 fingers (checks if tip is higher than the knuckle)
            for i in range(1, 5):
                fingers.append(1 if lm_list[tip_ids[i]][1] < lm_list[pip_ids[i]][1] else 0)

            finger_count = sum(fingers)

    # --- SEND TO ESP32 ONLY ON STATE CHANGE ---
    if esp32 and finger_count != prev_count:
        try:
            esp32.write(f"{finger_count}\n".encode('utf-8'))
            prev_count = finger_count
        except Exception:
            pass

    # --- UI OVERLAY ---
    cv2.rectangle(frame, (20, 20), (220, 85), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, f"LEDs: {finger_count}/5", (35, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 2)

    cv2.imshow("Hand Landmark LED Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if esp32:
    esp32.close()