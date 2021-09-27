from watergun import WaterGun
import time
from simple_pid import PID
from sort import Sort
from imutils.video import VideoStream
import imutils
import cv2
import numpy as np

sort = Sort(max_age=24)
camera = VideoStream()
camera.start()
water_gun = WaterGun(max_on_time=2.5)
water_gun.start()
water_gun.tilt = 50
water_gun.pan = 50

frame = camera.read()
frame = imutils.resize(frame, width = 600)
frame_center = (frame.shape[1]//2, 100 + (frame.shape[0]//2))
pan_pid = PID(.5,0.5,.0025, setpoint=0, output_limits = (0, 100), sample_time = 0.01)

tilt_pid = PID(.5,0.5,.0025, setpoint=0, output_limits = (0, 100), sample_time = 0.01)

def get_box_center(box):
    return (int(box[0] + ((box[2] - box[0])//2)), int(box[1] + ((box[3] - box[1]) //2)))
def distance(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return ((x2 - x1)**2 + (y2 - y1)**2)**.5
lock_start = time.time()
while(1):
    frame = camera.read()

    frame = imutils.resize(frame, width = 600)
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
    
        cv2.rectangle(frame, tuple(box[:2].astype(int)),  tuple(box[2:].astype(int)), (10, 255, 0), 2)

        box_center = get_box_center(box)
        cv2.circle(frame, box_center, 5, (0,0,255), -1)

        cv2.circle(frame, frame_center, 5, (255,0,255), -1)
        

        lock_dist = distance(box_center, frame_center)
        if lock_dist <= 70:
            if time.time() - lock_start >= 0:
                print("Fire")
                lock_start = time.time()
                water_gun.shoot(duration=2, bump = 10)
        else:
            lock_start = time.time()
            pe = box_center[0] - frame_center[0]
            pt = box_center[1] - frame_center[1]
            
            water_gun.pan += 1 if pe > 0 else -1 #pan_pid()
            water_gun.tilt += 1 if pt > 0 else -1 # tilt_pid(box_center[0] - frame_center[0])

    try:
        pass
        #cv2.imshow('Original',frame)
        # cv2.imshow('Mask',mask)
        # cv2.imshow('Erosion',erosion)
        # cv2.imshow('Dilation',dilation)

        #k = cv2.waitKey(1) & 0xFF
        #if k == 27:
        #    break
    except:
        pass

#cv2.destroyAllWindows()
