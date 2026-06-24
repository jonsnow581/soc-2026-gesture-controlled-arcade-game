import cv2 as cv
import mediapipe as mp
import handTrackingModule as htm

def fingers_up(lm_list):
    tips = [4,8,12,16,20]
    fingers = []

    fingers.append(1 if lm_list[4][1]>lm_list[3][1] else 0)

    for tip in tips[1:]:
        fingers.append(1 if lm_list[tip][2]<lm_list[tip-2][2] else 0)

    
    return fingers

def classify_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "fist"
    
    elif fingers == [1, 1, 1, 1, 1]:
        return "open palm"
    
    elif fingers == [0, 1, 0, 0, 0]:
        return "pointing"
    
    elif fingers == [1, 0, 0, 0, 0]:
        return "thumbs up"
    
    elif fingers == [0, 1, 1, 0, 0]:
        return "peace"
    
    return "unknown"

cap = cv.VideoCapture(0)

detector = htm.handDetector()

while cap.isOpened():
    success, img = cap.read()

    if not success:
        break

    # img = cv.flip(img, 1) # Flip the image horizontally for a mirror effect
    
    # 1. Find the hands and draw the lines
    img = detector.findHands(img)
    
    # 2. Get the specific landmark coordinates
    lmList = detector.findPosition(img)
    
    str=''
    if len(lmList) != 0:
        fingers = fingers_up(lmList)
        gesture = classify_gesture(fingers)
        str = gesture
        print(f"Detected gesture: {gesture}")


    cv.putText(img, f'Gesture: {str}', (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv.imshow("cam", img)


    if cv.waitKey(10) & 0xFF == ord('q'):
        break