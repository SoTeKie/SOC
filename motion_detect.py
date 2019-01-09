import cv2
from imutils.video import VideoStream
import sys
import time
import imutils

# We have one required argument, min. size
if len(sys.argv) != 4:
    print("Incorrect number of arguments! 3 arguments needed! {}".format(str(sys.argv)))
    sys.exit()

for i in range(1,4):
    if not sys.argv[i].isdigit():
        print("Incorrect use of arguments! Correct use is [MIN_SIZE] [MIN_FRAMES] [COOLDOWN]")

# Constant for minimal size of changed pixels to be considered as "motion"
MIN_SIZE = int(sys.argv[1])
# Minimal amount of frames needed to send notification about movement
MIN_FRAMES = int(sys.argv[2])
# Cooldown between movement notifications
COOLDOWN = int(sys.argv[3])

# Read from webcam and let it start up, sleep time can be adjusted for camera startup time
# or to make sure there's no motion in front of the camera
vs = VideoStream(src=0).start()
time.sleep(5.0)

# Set varible for first frame which will be used as a reference to compare to
# When starting the stream, there should be no motion in front of the camera
bgFrame = None

isMotion = False
motionCount = 0
untilCooldown = 0

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
    threshold = cv2.threshold(deltaFrame, tresh, maxVal, cv2.THRESH_BINARY)[1]

    # Fill in the holes caused by tresholding and then find the shapes/movement in the image, ignoring ones too small
    threshold = cv2.dilate(threshold, None, iterations=2)
    movement = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    movement = imutils.grab_contours(movement)
    
    # Set to false in every loop, only get rewritten to True if there is movement detected in a frame    
    isMovement = False

    for m in movement:
        if cv2.contourArea(m) < MIN_SIZE:
            continue

        isMotion = True

    #check to see if notification should be sent.    
    if isMotion:    

        # untilCooldown is when the cooldown ends in epoch time
        if time.time() > untilCooldown:
            motionCount += 1
            
            if motionCount >= MIN_FRAMES:
                print("MOVEMENT!")
                
                #reset counters
                motionCount = 0
                untilCooldown = time.time() + COOLDOWN
    #no movement
    else:
        motionCount = 0           
                   

    # Disabled for performance of camera
    cv2.imshow("Feed of delta", deltaFrame)
    cv2.imshow("Feed", frame)

    key = cv2.waitKey(1) & 0XFF 

    if key == ord("q"):
        break

vs.stop()
cv2.destroyAllWindows()
