import cv2 as cv
import mediapipe as mp
import time
import gestures
import handTrackingModule as htm

cap = cv.VideoCapture(0)
detector = htm.handDetector()

cTime = 0
pTime = 0

while True:
    success, img = cap.read()

    if not success:
        break

    img = cv.flip(img, 1)

    img = detector.findHands(img)
    lm_list = detector.findPosition(img)
    results = detector.results

    gesture = "NONE"
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        
        label = "Right"
        if results.multi_handedness:
            label = results.multi_handedness[0].classification[0].label
            
        gesture = gestures.classify(lm_list, label)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, f"FPS: {int(fps)}", (20, 120), cv.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 2)
    cv.putText(img, gesture, (20, 60), cv.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 2)
    cv.imshow("cam", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
    


