import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
hands=mp_hands.Hands()
mp_draw=mp.solutions.drawing_utils
cap=cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Display dots on each joint
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    cv2.imshow("Hand Tracking", img)

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
