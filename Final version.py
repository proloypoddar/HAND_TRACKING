import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height to 720 pixels

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Backspace'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', 'Enter']
]
def is_finger_on_key(finger_x, finger_y, key_x, key_y, key_w, key_h):
    return key_x < finger_x < key_x + key_w and key_y < finger_y < key_y + key_h
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
key_pressed = None 
finger_off_key = True  
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    key_w, key_h = 100, 100  
    for row_idx, row in enumerate(keys):
        for col_idx, key in enumerate(row):
            key_x, key_y = 100 + col_idx * (key_w + 10), 100 + row_idx * (key_h + 10)
            cv2.rectangle(img, (key_x, key_y), (key_x + key_w, key_y + key_h), (255, 0, 0), -1)
            cv2.putText(img, key, (key_x + 20, key_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            index_finger = handLms.landmark[8]
            h, w, _ = img.shape
            index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)
            thumb_finger = handLms.landmark[4]
            thumb_x, thumb_y = int(thumb_finger.x * w), int(thumb_finger.y * h)
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (thumb_x, thumb_y), 10, (0, 0, 255), cv2.FILLED)
            distance = calculate_distance(index_x, index_y, thumb_x, thumb_y)
            touch_threshold = 30  
            if distance < touch_threshold:
                for row_idx, row in enumerate(keys):
                    for col_idx, key in enumerate(row):
                        key_x, key_y = 100 + col_idx * (key_w + 10), 100 + row_idx * (key_h + 10)
                        if is_finger_on_key(index_x, index_y, key_x, key_y, key_w, key_h):
 
                            cv2.rectangle(img, (key_x, key_y), (key_x + key_w, key_y + key_h), (0, 255, 0), -1)
                            cv2.putText(img, key, (key_x + 20, key_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                            if finger_off_key:
                                if key == 'Space':
                                    pyautogui.press('space')
                                elif key == 'Backspace':
                                    pyautogui.press('backspace')
                                elif key == 'Enter':
                                    pyautogui.press('enter')
                                else:
                                    pyautogui.press(key.lower())
                                key_pressed = key
                                finger_off_key = False
                            break
                    else:
                        continue
                    break
            else:
                finger_off_key = True

    cv2.imshow("Hand Gesture Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
