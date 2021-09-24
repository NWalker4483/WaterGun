import numpy as np
import cv2 as cv
import time
from imutils.video import VideoStream
import imutils
import time

# initialize the video stream, sensors, etc
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera = True)
        
vs.stream.camera.shutter_speed = 2000
vs = vs.start()
time.sleep(2)

window_name = "HSV Calibrator"
cv.namedWindow(window_name)


# Convert BGR to HSV
img = vs.read()
img = imutils.resize(img, width=500)
img = cv.medianBlur(img,5)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

uh = 130
us = 255
uv = 255
lh = 110
ls = 50
lv = 50
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])
def nothing(x):
    print("Trackbar value: " + str(x))
    pass

# create trackbars for Upper HSV
cv.createTrackbar('UpperH',window_name,0,255,nothing)
cv.setTrackbarPos('UpperH',window_name, uh)

cv.createTrackbar('UpperS',window_name,0,255,nothing)
cv.setTrackbarPos('UpperS',window_name, us)

cv.createTrackbar('UpperV',window_name,0,255,nothing)
cv.setTrackbarPos('UpperV',window_name, uv)

# create trackbars for Lower HSV
cv.createTrackbar('LowerH',window_name,0,255,nothing)
cv.setTrackbarPos('LowerH',window_name, lh)

cv.createTrackbar('LowerS',window_name,0,255,nothing)
cv.setTrackbarPos('LowerS',window_name, ls)

cv.createTrackbar('LowerV',window_name,0,255,nothing)
cv.setTrackbarPos('LowerV',window_name, lv)

font = cv.FONT_HERSHEY_SIMPLEX
lower_hsv_old, upper_hsv_old = () , () 

mask = cv.inRange(hsv, lower_hsv, upper_hsv)
while(1):
    img = vs.read()
    img = imutils.resize(img, width=500)
    img = cv.medianBlur(img,5)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    if (tuple(lower_hsv_old) != tuple(lower_hsv) or tuple(upper_hsv_old) != tuple(upper_hsv)):
        lower_hsv_old, upper_hsv_old = lower_hsv, upper_hsv
        h,s,v = cv2.split(hsv)
        mask = cv.inRange(hsv, lower_hsv_old, upper_hsv_old)
    cv.putText(mask,'Lower HSV: [' + str(lh) +',' + str(ls) + ',' + str(lv) + ']', (10,30), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    cv.putText(mask,'Upper HSV: [' + str(uh) +',' + str(us) + ',' + str(uv) + ']', (10,60), font, 0.5, (200,255,155), 1, cv.LINE_AA)

    cv.imshow(window_name,mask)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of Upper HSV trackbars
    uh = cv.getTrackbarPos('UpperH',window_name)
    us = cv.getTrackbarPos('UpperS',window_name)
    uv = cv.getTrackbarPos('UpperV',window_name)
    upper_blue = np.array([uh,us,uv])
    # get current positions of Lower HSCV trackbars
    lh = cv.getTrackbarPos('LowerH',window_name)
    ls = cv.getTrackbarPos('LowerS',window_name)
    lv = cv.getTrackbarPos('LowerV',window_name)
    upper_hsv = np.array([uh,us,uv])
    lower_hsv = np.array([lh,ls,lv])

cv.destroyAllWindows()