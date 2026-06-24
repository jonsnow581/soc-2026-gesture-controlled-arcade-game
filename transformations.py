import cv2 as cv
import numpy as np

img = cv.imread('download.jpg')

cv.imshow('veruit coli', img)

#TRANSLATE
def translate(img, x, y):
    transMat = np.float32([[1,0,x], [0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

resized = cv.resize(img, (500, 500), interpolation=cv.INTER_CUBIC)
translated = translate(resized, -100, -100)
cv.imshow('translated', translated)

#rotate
def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2, height//2)

    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(resized, 30)
cv.imshow('rotated', rotated)

#resize
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)

#flip
flipped = cv.flip(resized, -1)
cv.imshow('flipped', flipped)

#crop
cropped = resized[200:300, 200:300]
cv.imshow('cropped', cropped)
cv.waitKey(0)