import cv2
import mediapipe as mp
import serial
import time


arduino = serial.Serial('COM3', 9600) 
time.sleep(2) 


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    landmarks = hand_landmarks.landmark
    count = 0

 
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        count += 1

    for tip in tips[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            count += 1
    return count

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        led_status = 0
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        
                finger_count = count_fingers(hand_landmarks)

           
                h, w, _ = frame.shape
                x_coords = [lm.x * w for lm in hand_landmarks.landmark]
                y_coords = [lm.y * h for lm in hand_landmarks.landmark]
                x_min, x_max = int(min(x_coords)), int(max(x_coords))
                y_min, y_max = int(min(y_coords)), int(max(y_coords))
                cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (0, 255, 0), 2)

               
                if finger_count == 2 or finger_count == 5:
                    led_status = 1
                else:
                    led_status = 0

            
                cv2.putText(frame, f"Jari: {finger_count}", (x_min, y_min - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"LED: {'ON' if led_status else 'OFF'}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

      
        arduino.write(f"{led_status}\n".encode())

        cv2.imshow("Finger LED Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
arduino.close()
