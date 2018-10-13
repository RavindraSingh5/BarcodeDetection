import numpy as np
import cv2
import argparse

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--img", required = True, help = "path to the image file")
#args = vars(ap.parse_args())
#print argparse.parse_args()

img = cv2.imread("IMG_A.JPG")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

grad_X = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
grad_Y = cv2.Sobel(gray, ddepth= cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

gradient = cv2.subtract(grad_X, grad_Y)
gradient = cv2.convertScaleAbs(gradient)

cv2.imshow('Original',img)
OutputImge = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
OutputImge = cv2.resize(OutputImge,(0,0),fx=0.5,fy=0.5)
cv2.imshow('Scaled',OutputImge)
cv2.imshow('gradX',grad_X)

blurred = cv2.blur(gradient,(9,9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21,7))
closed = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE, kernel)

# perform a series of erosions and dilations
edged = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

#cnts, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
image,contours,_ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

# compute the rotated bounding box of the largest contour
#rect = cv2.minAreaRect(c)
#box = np.int(cv2.cv.BoxPoints(rect))
rect = cv2.minAreaRect(c)
box = np.int(cv2.boxPoints(rect))

cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
