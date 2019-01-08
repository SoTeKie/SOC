import cv2
from imutils.video import VideoStream
import sys
import time
import imutils

# We have one required argument, min. size
if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    print("Incorrect arguments! {}".format(str(sys.argv))
    sys.exit()
 
# Constant for minimal size of changed pixels to be considered as "motion"
MIN_SIZE = int(sys.argv[1])

# Read from webcam and let it start up, sleep time can be adjusted for camera startup time
# or to make sure there's no motion in front of the camera
vs = VideoStream(src=0).start()
time.sleep(5.0)

# Set varible for first frame which will be used as a reference to compare to
# When starting the stream, there should be no motion in front of the camera
bgFrame = None


# video loop 
while True:
    # Read current frame
    frame = vs.read()

    # End of video
    if frame is None:
        break

    # Variables required for Gaussian blur
    # There's no real need to mess with these values
    kernelSize = (21, 21)
    stigmaXY = 0

    # Processing for image to make it easier to calculate on
    # Resized and smoothed out with Gaussian Blur
    frame = imutils.resize(frame, width=500)
    smoothFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smoothFrame = cv2.GaussianBlur(smoothFrame, kernelSize, stigmaXY)

    # If there is no background frame, set it now so we can use it for comparison
    if bgFrame is None:
        bgFrame = smoothFrame
        continue

    # The absolue distance between the background/first frame and new frame will
    # create a new image highlighting only the differences between the two
    deltaFrame = cv2.absdiff(bgFrame, smoothFrame)

    # Variables for tresholding
    tresh = 25
    maxVal = 255

    # Treshold the image
    threshold = cv2.treshold(deltaFrame, tresh, maxVal, cv.THRESH_BINARY)

    # Fill in the holes caused by tresholding and then find the shapes/movement in the image, ignoring ones too small
    treshold = cv2.dilate(treshold, None, iterations=2)
    movement = cv2.findContours(treshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    movement = imutils.grab_contours(movement)
    
    for m in movement:
        if cv2.contourArea(m) < MIN_SIZE:
            continue

        print("MOVEMENT DETECTED!")
