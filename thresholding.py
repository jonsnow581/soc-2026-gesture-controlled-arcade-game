import cv2 as cv

img = cv.imread('download.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

threshold, thresh = cv. threshold(gray, 150, 255, cv.THRESH_BINARY)

cv.imshow('threshold', thresh)

threshold, thresh = cv. threshold(gray, 150, 255, cv.THRESH_BINARY_INV)

cv.imshow('threshold', thresh)


#adaptive the thresholding

adapt_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 3)
cv.imshow('adaptive threshold', adapt_thresh)

cv.waitKey(0)