# Real-Time Hand Gesture Recognition

Summer of Science 2026 (Project CS03) — a real-time hand gesture recognition system built with OpenCV and MediaPipe, eventually feeding into a gesture-controlled game.

## Overview

This project tracks a hand via webcam, extracts 21 landmark coordinates per frame using MediaPipe, and classifies the hand pose into one of several discrete gestures (FIST, OPEN_PALM, POINT, PEACE, THUMB, PINCH) using geometric rules — finger up/down checks and normalized landmark distances.

## Milestones Achieved

**Week 1–2: Setup**
- Python + OpenCV + MediaPipe environment configured.
- Worked through MediaPipe Hands documentation and core tracking tutorials.

**Week 3: Live Hand Detection & Landmark Extraction**
- Built `handTrackingModule.py` — a reusable `handDetector` class wrapping MediaPipe's `solutions.hands` API, with `findHands()` (detect + draw skeleton) and `findPosition()` (extract 21 `[id, x, y]` pixel-coordinate landmarks per frame).
- Live webcam feed with hand skeleton overlay and FPS counter.
- Printed gestures to terminal as a first proof of concept.

**Week 4: Gesture Logic Module**
- Built `gestures.py` as a standalone module exposing one entry point, `classify(lm_list, hand_label)`, that returns a gesture name string.
- Implemented three core techniques:
  - **Finger up/down** via tip-vs-joint y-coordinate comparison.
  - **Normalized Euclidean distance** (e.g. thumb tip ↔ index tip) divided by a hand-scale reference (wrist ↔ middle knuckle), so thresholds like the pinch detector hold up regardless of how close the hand is to the camera.
  - **Handedness-aware thumb logic**, since the thumb direction check flips between left and right hands.
- Final gesture set: **FIST, OPEN_PALM, POINT, PEACE, THUMB, PINCH** — 5+ gestures classified reliably and distinguishably.

## Challenges Faced & Fixed

- **`mediapipe.solutions` API breakage on newer mediapipe versions** — the old `solutions` API (used in most tutorials) is deprecated and throws `AttributeError` on recent releases. Fixed by downgrading to `mediapipe==0.10.14`, which still supports it.
- **Handedness/mirror bug** — after applying `cv2.flip()` for a natural mirror view, MediaPipe's `multi_handedness` label is reported relative to the *unflipped* frame, so it reads backwards if you flip the feed before passing it to MediaPipe but try to "correct" the label afterward. Resolved by being consistent about flip-before-detect and not double-correcting the label.
- **Camera-distance-dependent thresholds** — raw pixel distance (e.g. for pinch detection) varies wildly with how close the hand is to the camera. Fixed by normalizing all distance-based gestures against the hand's own scale (wrist-to-middle-knuckle distance) instead of using a fixed pixel threshold.

## Project Structure
├── handTrackingModule.py   # Hand detection + landmark extraction class

├── gestures.py             # Gesture classification logic

├── test_gestures.py                 # Webcam loop wiring detection + classification together

I've also added a file that controls volume through hand gestures named volumeHandControl.py following Mortaza's YouTube tutorial.

## Tech Stack
- Python
- OpenCV (`opencv-python`)
- MediaPipe (`0.10.14`)

## Status
Midterm checkpoint (Weeks 1–4) complete: live detection, landmark extraction, and a 5-gesture classification module are functional and tested.

## Next Steps
- Integrate gesture commands into a Pygame-based game.
- Add gesture-hold/smoothing buffer to reduce flicker between frames.
- HUD overlay showing live gesture state.
