import cv2
import mediapipe as mp
import numpy as np
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

KEYS = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M'],
    ['SPACE','BACKSPACE','ENTER']
]

KEY_WIDTH, KEY_HEIGHT = 50, 50
OFFSET_X, OFFSET_Y = 20, 150   # shift keyboard lower so textbox fits above
GAP = 5

last_pressed_time = 0
DEBOUNCE = 0.5
PRESS_COLOR = (0, 200, 0)
NORMAL_COLOR = (200, 200, 200)

PINCH_THRESHOLD = 40
calibrated = False

typed_text = ""

def draw_keyboard(img, pressed_key=None):
    for row_index, row in enumerate(KEYS):
        for col_index, key in enumerate(row):
            x = OFFSET_X + col_index * (KEY_WIDTH + GAP)
            y = OFFSET_Y + row_index * (KEY_HEIGHT + GAP)
            
            
            if pressed_key == key:
                color = PRESS_COLOR
            else:
                color = NORMAL_COLOR

            cv2.rectangle(img, (x, y), (x + KEY_WIDTH, y + KEY_HEIGHT), color, -1)
            cv2.rectangle(img, (x, y), (x + KEY_WIDTH, y + KEY_HEIGHT), (100, 100, 100), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            label = key if key not in ['SPACE','BACKSPACE','ENTER'] else key[0]  
            text_size = cv2.getTextSize(label, font, 1, 2)[0]
            text_x = x + (KEY_WIDTH - text_size[0]) // 2
            text_y = y + (KEY_HEIGHT + text_size[1]) // 2
            cv2.putText(img, label, (text_x, text_y), font, 1, (50,50,50), 2)
            
def get_key_at_pos(xp, yp):
    for row_index, row in enumerate(KEYS):
        for col_index, key in enumerate(row):
            x = OFFSET_X + col_index * (KEY_WIDTH + GAP)
            y = OFFSET_Y + row_index * (KEY_HEIGHT + GAP)
            if x <= xp <= x + KEY_WIDTH and y <= yp <= y + KEY_HEIGHT:
                return key
    return None

def update_text(key):
    global typed_text
    if key == "SPACE":
        typed_text += " "
    elif key == "BACKSPACE":
        typed_text = typed_text[:-1]
    elif key == "ENTER":
        typed_text += "\n"
    else:
        typed_text += key

def calibrate_pinch(hands, cap):
    global PINCH_THRESHOLD, calibrated
    print("Calibration: Pinch and hold for 2 seconds...")
    start_time = None
    distances = []

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            ix, iy = int(lm.landmark[8].x * w), int(lm.landmark[8].y * h)
            tx, ty = int(lm.landmark[4].x * w), int(lm.landmark[4].y * h)
            dist = np.hypot(tx-ix, ty-iy)

            cv2.circle(frame, (ix, iy), 8, (255,0,255), -1)
            cv2.circle(frame, (tx, ty), 8, (255,0,255), -1)
            cv2.putText(frame, f"Dist:{int(dist)}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            if dist < 50:  # pinch detected
                if start_time is None:
                    start_time = time.time()
                else:
                    elapsed = time.time() - start_time
                    distances.append(dist)
                    if elapsed > 2:  # hold for 2s
                        PINCH_THRESHOLD = int(np.mean(distances)) + 5
                        calibrated = True
                        print(f"Calibrated PINCH_THRESHOLD = {PINCH_THRESHOLD}")
                        return
            else:
                start_time = None
                distances.clear()

        cv2.putText(frame, "Pinch to calibrate...", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow("Calibration", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
cap = cv2.VideoCapture(0)

cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Virtual Keyboard", 1000, 700)    

