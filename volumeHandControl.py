import cv2 as cv
import mediapipe as mp
import time
import handTrackingModule as htm
import math
import numpy as np

wCam, hCam = 1280, 720

handDetector = htm.handDetector(detectionCon=0.7) # You can adjust the detection confidence as needed

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
# Just import AudioUtilities, you no longer need ctypes or comtypes
from pycaw.pycaw import AudioUtilities

# Get the audio device (your speakers)
devices = AudioUtilities.GetSpeakers()

# The new pycaw update simplified this to a single line!
volume = devices.EndpointVolume

# --- Examples of what you can do with the 'volume' object ---

# volume.GetMute()                 # Check if muted
# volume.GetMasterVolumeLevel()    # Get current volume

# Get the volume range (returns a tuple like (-65.25, 0.0, 0.03125))
# Index 0 is min volume, Index 1 is max volume
volRange = volume.GetVolumeRange()

# Set the master volume level (0.0 is usually max volume, negative numbers lower it)

volume.SetMasterVolumeLevel(0.0, None)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]



cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

length = 0

ptime = 0
while True:
    success, img = cap.read()

    img = handDetector.findHands(img)
    lmlist = handDetector.findPosition(img, draw=False)
    print (lmlist)

    if len(lmlist) != 0:
        print(lmlist[4], lmlist[8]) # This prints the coordinate of the thumb tip to your terminal
        x1, y1 = lmlist[4][1], lmlist[4][2] # Thumb tip
        x2, y2 = lmlist[8][1], lmlist[8][2] # Index finger tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # Midpoint between thumb and index finger

        cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        vol = np.interp(length, [20,200], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

        if length < 50:
            cv.circle(img, (cx, cy), 15, (0, 255, 0), cv.FILLED)

        
    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    volBar = np.interp(length, [20,200], [400, 150])
    cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv.FILLED)
    volPer = np.interp(length, [20,200], [0, 100])
    cv.putText(img, f'{int(volPer)} %', (40,450), cv.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)


    cTime = time.time()
    fps = 1/(cTime-ptime)
    ptime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (40,70), cv.FONT_HERSHEY_PLAIN, 3, (255,255,0), 3)

    cv.imshow("cam", img)
    cv.waitKey(1)