import cv2 as cv 
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id==0:
                    cv.circle(img, (cx,cy), 25, (0,255,0), -1)
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTIme = cTime

    cv.putText(img, str(int(fps)), (70,10), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv.imshow("Image", img)
    cv.waitKey(1)