import cv2 as cv
# img = cv.imread('download.jpg')
# cv.imshow('veruit coli', img)
# cv.waitKey(0)

capture = cv.VideoCapture('Recording 2026-05-16 135005.gif')

while True:
    isTrue, frame = capture.read()

    cv.imshow('CAD', frame)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()