import cv2
from imutils.video import VideoStream
import sys

# We have one required argument, min. size
if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    print("Incorrect arguments! {}".format(str(sys.argv))
    sys.exit()
 
# Constant for minimal size of changed pixels to be considered as "motion"
MIN_SIZE = int(sys.argv[1])

# Read from webcam

vs = VideoStream(src=0).start()

