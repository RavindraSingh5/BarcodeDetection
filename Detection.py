# USAGE
# python detect_barcode.py
# python detect_barcode.py --video video/barcode_example.mov

# import the necessary packages
from pyimagesearch import simple_barcode_detection
import argparse
import cv2

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="path to the (optional) video file")
#args = vars(ap.parse_args())

img = cv2.imread("IMGB.JPG")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

grad_X = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
grad_Y = cv2.Sobel(gray, ddepth= cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

gradient = cv2.subtract(grad_X, grad_Y)
gradient = cv2.convertScaleAbs(gradient)

# if the video path was not supplied, grab the reference to the
# camera
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping over the frames
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # check to see if we have reached the end of the
    # video
    if not grabbed:
        break

    # detect the barcode in the image
    box = simple_barcode_detection.detect(frame)

    # if a barcode was found, draw a bounding box on the frame
    cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

    # show the frame and record if the user presses a key
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()