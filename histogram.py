import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('download.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

blank = np.zeros(gray.shape[:2], dtype='uint8')
mask = cv.circle(blank, (img.shape[1]//2 + 100, img.shape[0]//2), 100, 255, thickness=-1)

masked = cv.bitwise_and(gray, gray, mask=mask)
cv.imshow('mask', masked)

gray_hist = cv.calcHist([masked], [0], mask, [256], [0,256])

plt.figure()
plt.title('grayscale histogram')
plt.xlabel('bins')
plt.ylabel('# of pixels')
plt.plot(gray_hist)
plt.xlim([0,256])
plt.show()



hist  = cv.calcHist([img], [0], mask, [256], [0,256])
plt.figure()
plt.title('color histogram')
plt.xlabel('bins')
plt.ylabel('# of pixels')
colors = ('b', 'g', 'r')
for i,col in enumerate(colors):
    hist = cv. calcHist
    plt.plot(hist, color=col)
    plt.xlim([0,256])

plt.show()


cv.waitKey(0)