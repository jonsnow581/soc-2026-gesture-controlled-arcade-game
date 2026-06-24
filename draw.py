import cv2 as cv
import numpy as np

blank = np.zeros((500, 500, 3), dtype='uint8')

cv.imshow('Blank', blank)
# img = cv.imread('download.jpg')

# cv.imshow('veruit coli', img)

# blank[200:300, 200:300] = 0,255, 0
# cv.imshow('gin', blank)

# blank[:] = 0,0,255
# cv.imshow('ed', blank)

# blank[:] = 255,0,0
# cv.imshow('idk', blank)


cv.rectangle(blank, (0,0), (50,50), (255,0,0), thickness=cv.FILLED)
cv.imshow('rt', blank)

cv.circle(blank, (250,250), 50, (255,0,0), thickness=-1)
cv.imshow('cr', blank)

cv.line(blank, (0,0), (250,250), (255,255,255), thickness=3)
cv.imshow('li', blank)

cv.putText(blank, 'valar morguilis!', (250,250), cv.FONT_HERSHEY_TRIPLEX, 2.0, (0,0,255), 2)
cv.imshow('txt', blank)
cv.waitKey(0)

