import handTrackingModule as htm
import cv2 as cv

detector = htm.handDetector()

cap = cv.VideoCapture(0)

while True:
    success, img = cap.read()

    if not success:
        break

    img = cv.flip(img, 1) # Flip the image horizontally for a mirror effect
    
    # 1. Find the hands and draw the lines
    img = detector.findHands(img)
    
    cv.imshow("cam", img)
    cv.waitKey(1)   
    if cv.waitKey(10) & 0xFF == ord('q'):
        break
 