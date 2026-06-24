import cv2 as cv
import numpy as np

blank = np.zeros((400,400), dtype='uint8')

rectangle = cv.rectangle(blank.copy(), (30,30), (370,370), 255, thickness=-1)
circle = cv.circle(blank.copy(), (200,200), 200, 255, thickness=-1)

cv.imshow('rectangle', rectangle)
cv.imshow('circle', circle)

bwand = cv.bitwise_and(rectangle, circle)
cv.imshow('bwand', bwand)

bwor = cv.bitwise_or(rectangle, circle)
cv.imshow('bwor', bwor)

bwxor = cv.bitwise_xor(rectangle, circle)
cv.imshow('bwxor', bwxor)

bwnot = cv.bitwise_not(rectangle)
cv.imshow('bwnot', bwnot)   


cv.waitKey(0)