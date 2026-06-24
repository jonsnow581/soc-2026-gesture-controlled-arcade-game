import cv2 as cv

img = cv.imread('download.jpg')
im = cv.resize(img, (500, 500))
cv.imshow('original', im)

#averaging
avg = cv.blur(im, (7,7))
cv.imshow('average', avg)

#gaussian
gauss = cv.GaussianBlur(im, (7,7), 0)
cv.imshow('gaussian', gauss)

#medianblur
median = cv.medianBlur(im, 3)
cv.imshow('median', median)

#bilateral
bilateral = cv.bilateralFilter(im, 5, 15, 15 )
cv.imshow('bilateral', bilateral)


cv.waitKey(0)
