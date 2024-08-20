import cv2
import mediapipe as mp
import pyautogui
from pynput.keyboard import Controller

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize Pynput keyboard controller
keyboard = Controller()

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Define keys for virtual keyboard (rows)
keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Backspace'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', 'Enter']
]

# Function to check if index finger is near a key position
def is_finger_on_key(finger_x, finger_y, key_x, key_y, key_w, key_h):
    return key_x < finger_x < key_x + key_w and key_y < finger_y < key_y + key_h

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the webcam feed
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Draw the virtual keyboard
    key_w, key_h = 80, 80  # Key width and height
    for row_idx, row in enumerate(keys):
        for col_idx, key in enumerate(row):
            key_x, key_y = 100 + col_idx * (key_w + 10), 100 + row_idx * (key_h + 10)
            cv2.rectangle(img, (key_x, key_y), (key_x + key_w, key_y + key_h), (255, 0, 0), -1)
            cv2.putText(img, key, (key_x + 20, key_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Hand landmark detection
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip coordinates
            index_finger = handLms.landmark[8]
            h, w, _ = img.shape
            index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)

            # Draw a circle at the index finger tip
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            # Check if the finger is over any key and simulate key press
            for row_idx, row in enumerate(keys):
                for col_idx, key in enumerate(row):
                    key_x, key_y = 100 + col_idx * (key_w + 10), 100 + row_idx * (key_h + 10)
                    if is_finger_on_key(index_x, index_y, key_x, key_y, key_w, key_h):
                        # Highlight the key being pressed
                        cv2.rectangle(img, (key_x, key_y), (key_x + key_w, key_y + key_h), (0, 255, 0), -1)
                        cv2.putText(img, key, (key_x + 20, key_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                        # Simulate the key press
                        if key == 'Space':
                            pyautogui.press('space')
                        elif key == 'Backspace':
                            pyautogui.press('backspace')
                        elif key == 'Enter':
                            pyautogui.press('enter')
                        else:
                            pyautogui.press(key.lower())

                        break  # Avoid multiple presses

    cv2.imshow("Hand Gesture Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
