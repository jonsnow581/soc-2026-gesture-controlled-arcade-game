import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        # Note: model_complexity=1 is added here to prevent errors in newer versions of MediaPipe
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, 
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                # This converts the raw decimal ratio into actual pixel coordinates
                cx, cy = int(lm.x * w), int(lm.y * h) 
                lmList.append([id, cx, cy])
                if draw:
                    # Draws a larger circle on the joints
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED) 
        return lmList

# --- THIS IS THE TEST SCRIPT ---
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()

        if not success:
            break

        img = cv2.flip(img, 1) # Flip the image horizontally for a mirror effect
        
        # 1. Find the hands and draw the lines
        img = detector.findHands(img)
        
        # 2. Get the specific landmark coordinates
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4]) # This prints the coordinate of the thumb tip to your terminal

        # 3. Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        
        # Press 'q' to quit the window properly
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

# The Magic Switch
if __name__ == "__main__":
    main()