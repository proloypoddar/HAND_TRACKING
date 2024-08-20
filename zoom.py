import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Capture Video
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get the positions of the thumb and index finger
            thumb = handLms.landmark[4]  # Thumb tip
            index = handLms.landmark[8]  # Index finger tip

            # Convert landmark positions to pixel values
            h, w, c = img.shape
            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
            index_x, index_y = int(index.x * w), int(index.y * h)

            # Draw circles on thumb and index
            cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)

            # Calculate the distance between thumb and index finger
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # Trigger Zoom In/Out based on distance
            if distance < 40:
                pyautogui.hotkey('ctrl', '+')  # Zoom in
            elif distance > 100:
                pyautogui.hotkey('ctrl', '-')  # Zoom out

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
