import cv2 as cv
import numpy as np

img = cv.imread('download.jpg')

blank = np.zeros(img.shape, dtype = 'uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('grayscale', gray)


Canny = cv.Canny(img, 125, 175)
cv.imshow('Canny', Canny)

ret, thresh = cv.threshold(gray, 125, 255 , cv.THRESH_BINARY)
cv.imshow('thresh', thresh)

contours, hierarchies = cv.findContours(Canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contours found!')

cv.drawContours(blank, contours, -1, (0, 0, 255), thickness=1)
cv.imshow( 'drew', blank)

cv.waitKey(0)