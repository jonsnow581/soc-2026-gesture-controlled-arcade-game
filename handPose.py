import cv2 as cv
import mediapipe as mp
import time
import numpy as np

cap = cv.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing.utils


with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, img = cap.read()
        frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = hands.process(frame)
        frame.flags.writeable = True
        img = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        cv.imshow("cam", img)


        if cv.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()





