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