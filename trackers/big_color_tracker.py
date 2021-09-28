import cv2
import numpy as np
class BigColorTracker():
    def __init__(self):
        pass
    def update(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_red = np.array([0,90,50])
        upper_red = np.array([15,255,230])
        
        mask = cv2.inRange(hsv, lower_red, upper_red)
        # ksize
        ksize = (10, 10)
        
        # Using cv2.blur() method 
        mask = cv2.blur(mask, ksize) 
        
        res = cv2.bitwise_and(frame,frame, mask= mask)

        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(mask,kernel,iterations = 1)
        dilation = cv2.dilate(erosion,kernel,iterations = 1)

        im2,contours, hierarchy = cv2.findContours(dilation.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        bbox = None
        # Getting the biggest contour
        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(frame, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)
            bbox = (x,y, x+w,y+h)

        if bbox != None:
            pred = sort.update(np.array([bbox]))
        else:
            pred = sort.update()

        if len(pred) > 0:
            box = pred[0][:-1]

if __name__ == "__main__":
    pass

"""
import numpy as np
import cv2 as cv
import time
from imutils.video import VideoStream
import imutils
import time

# initialize the video stream, sensors, etc
print("[INFO] starting video stream...")
vs = VideoStream()
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
        h,s,v = cv.split(hsv)
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
"""