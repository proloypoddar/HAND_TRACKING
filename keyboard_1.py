import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# List of keys (simple layout for now)
keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']

# Function to check if index finger is near a key position
def is_finger_on_key(finger_x, finger_y, key_x, key_y, key_w, key_h):
    return key_x < finger_x < key_x + key_w and key_y < finger_y < key_y + key_h

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image to mirror the webcam feed
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Draw the virtual keyboard (simple horizontal row)
    key_w, key_h = 80, 80  # Key width and height
    for i, key in enumerate(keys):
        key_x, key_y = 100 + i * (key_w + 10), 100
        cv2.rectangle(img, (key_x, key_y), (key_x + key_w, key_y + key_h), (255, 0, 0), -1)
        cv2.putText(img, key, (key_x + 20, key_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get the index finger tip coordinates
            index_finger = handLms.landmark[8]  # Index finger tip
            h, w, _ = img.shape
            index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)

            # Draw a circle at the index finger tip
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            # Check if the finger is over any key
            for i, key in enumerate(keys):
                key_x, key_y = 100 + i * (key_w + 10), 100
                if is_finger_on_key(index_x, index_y, key_x, key_y, key_w, key_h):
                    cv2.rectangle(img, (key_x, key_y), (key_x + key_w, key_y + key_h), (0, 255, 0), -1)
                    cv2.putText(img, key, (key_x + 20, key_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                    # Trigger the key press using PyAutoGUI
                    pyautogui.press(key.lower())
                    break

    cv2.imshow("Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
