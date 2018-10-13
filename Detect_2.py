import numpy as np
import cv2

img = cv2.imread("IMG_Z.JPG")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imshow("Gray", gray)
#cv2.waitKey(0)

edged = cv2.Canny(gray, 10, 250)
cv2.imshow("Edged", edged)
#cv2.waitKey(0)
"""""
ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
contours = contours[0]
M = cv2.moments(contours)
print M

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
"""

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7 ,7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Closed", closed)
#cv2.waitKey(0)

image,contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
total = 0

#area = cv2.contourArea(contours)

rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.int0(box)

for i in contours:
    peri = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.04 * peri, True)

    if len(approx) == 4:
        cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)
        total = 1


#perimeter = cv2.arcLength(c,True)
#approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

cv2.drawContours(img,[box], 0, (0, 255, 0), 3)

print"I found a Barcode Image".format(total)
cv2.imshow("Output", img)
cv2.waitKey(0)

cv2.destroyAllWindows()

