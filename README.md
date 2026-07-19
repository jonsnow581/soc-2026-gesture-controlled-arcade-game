# Real Time Hand Gesture Recognition
**Seasons of Code 2026, Project CS03.** A real time hand gesture recognition system built using OpenCV and MediaPipe, which I later used to control a Snake game with just my hand in front of a webcam.

## **Overview**
This project tracks a hand through the webcam, pulls out 21 landmark points per frame using MediaPipe, and figures out what pose the hand is making using simple geometric rules like checking if a finger is up or down and comparing distances between landmarks. Later in the project this got connected to an actual Pygame Snake game so the gestures could control something in real time instead of just printing to the terminal.

## **Milestones Achieved**

### **Week 1 and 2: Setup**
* Set up Python, OpenCV and MediaPipe.
* Went through the MediaPipe Hands documentation and some basic tracking tutorials to understand how landmark detection works.

### **Week 3: Live Hand Detection and Landmark Extraction**
* Built `handTrackingModule.py`, a `handDetector` class that wraps MediaPipe's `solutions.hands` API.
* `findHands()` detects the hand and draws the skeleton, `findPosition()` pulls out the 21 landmark points as pixel coordinates.
* Got a live webcam feed working with the hand skeleton drawn on top and an FPS counter.
* Printed detected gestures to the terminal as a first working version.

### **Week 4: Gesture Logic Module**
* Built `gestures.py`, a separate module with one function `classify(lm_list, hand_label)` that takes the landmark list and returns the gesture name.
* Used three main techniques to classify gestures:
  * Checking if a finger is up or down by comparing the tip and the joint below it.
  * Normalized distance between landmarks (like thumb tip to index tip for a pinch) divided by the hand's own scale (wrist to middle knuckle), so it still works whether the hand is close or far from the camera.
  * Handling left and right hands differently for the thumb check, since the thumb direction flips depending on which hand it is.
* Final gesture set: **FIST, OPEN_PALM, POINT, PEACE, THUMB, PINCH** — 6 gestures classified reliably.

### **Week 5: Pygame Snake Logic**
* Built the Snake game itself in Pygame, separate from the gesture code at this point, controlled with arrow keys just to get the game logic working on its own.
* Grid based movement, the snake as a list of segments, food that respawns in a free cell, score tracking, and speed that increases as the score goes up.
* Added a welcome screen, a pause screen, and a game over screen with restart handling.

### **Week 6: Final Output, Gesture Controlled Snake Game**
* Combined the Pygame snake game with the hand detection code into one file, `gesture_snake_game.py`, so gestures now control the game directly instead of arrow keys.
* Moved from the older `mediapipe.solutions.hands` API to the newer `HandLandmarker` Tasks API for this part, mainly because it has a VIDEO mode that tracks the hand across frames instead of treating every frame as a fresh image, which gave much steadier detection.
* Final gesture set for the game:
  * Index finger up → **UP**
  * Thumb out → **LEFT**
  * Pinky out → **RIGHT**
  * Closed fist → **DOWN**
  * Open palm → **PAUSE**
* Added a stability filter so a gesture only counts once it has shown up for a few frames in a row, instead of flipping around every single frame.
* Added a landmark skeleton overlay drawn directly on the webcam feed so I can actually see what the model is tracking while testing.
* This is the final working version of the project.

## **Challenges Faced and Fixed**
* **`mediapipe.solutions` API breaking on newer mediapipe versions.** The old `solutions` API that most tutorials use is deprecated and throws an `AttributeError` on newer releases. Fixed by downgrading to `mediapipe==0.10.14`, which still supports it.
* **Handedness and mirror bug.** After flipping the frame with `cv2.flip()` for a natural mirror view, MediaPipe's handedness label is still based on the unflipped frame, so it reads backwards if you flip before detecting but then also try to correct the label afterward. Fixed by being consistent: flip first, then detect, and don't correct the label a second time.
* **Camera distance messing up thresholds.** Raw pixel distance for things like pinch detection changes a lot depending on how close the hand is to the camera. Fixed by normalizing distances against the hand's own scale instead of using one fixed pixel number.
* **Corrupted model file.** Downloaded `hand_landmarker.task` through the browser once and it saved an error page instead of the actual model. Since `.task` files are zip archives internally, this threw an "unable to open zip archive" error. Fixed by downloading it directly and checking the file size and that it actually opens as a zip.
* **Angle calculated after it was used.** In an earlier version of the gesture logic, the pointing angle was computed after the if/else block that used it, so the value was always stale. This is part of why I moved away from angle based detection toward the finger up/down pose approach for the game.
* **Up and down flipped.** Turned out to be the image y axis increasing downward instead of upward like normal math, so the angle came out backwards. Fixed with a sign flip on the y difference in that earlier angle version.
* **Landmark drawing function defined but never actually called anywhere,** so nothing showed up on screen even though the function itself was correct.
* **Quit key only working through Ctrl+C in the terminal.** This was because the key press was only being checked in the OpenCV window and not in the Pygame window, so if the game window had focus, `q` did nothing. Fixed by checking for `q` in both places.

## **Project Structure**
```
├── handTrackingModule.py     # Hand detection and landmark extraction class
├── gestures.py                # Gesture classification logic (6 gesture set)
├── test_gestures.py           # Webcam loop wiring detection and classification together
├── gesture_snake_game.py      # Pygame Snake game controlled by hand gestures
├── hand_landmarker.task       # MediaPipe hand landmark model file
```

I also have a file that controls volume through hand gestures named `volumeHandControl.py`, following Mortaza's YouTube tutorial.

## **Tech Stack**
* Python
* OpenCV (`opencv-python`)
* MediaPipe (`0.10.14`)
* Pygame

## **Status**
All six weeks are complete. Live detection, landmark extraction, gesture classification, the Pygame snake game, and the final gesture controlled version of the game are all functional and tested.

