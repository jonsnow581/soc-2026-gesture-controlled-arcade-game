import cv2 as cv
import numpy as np

img = cv.imread('download.jpg')

blank = np.zeros((img.shape[:2]), dtype = 'uint8')

mask = cv.circle(blank, (img.shape[1]//2 + 100, img.shape[0]//2), 100, 255, thickness=-1)

masked = cv.bitwise_and(img, img, mask=mask)
cv.imshow('mask', masked)


cv.waitKey(0)