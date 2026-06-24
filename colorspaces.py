import cv2 as cv
import numpy as np

im = cv.imread('download.jpg')

gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
lab = cv.cvtColor(im, cv.COLOR_BGR2LAB)
rgb = cv.cvtColor(im, cv.COLOR_BGR2RGB)