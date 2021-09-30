from watergun import WaterGun
#from utils.mock import WaterGun

import time
from imutils.video import VideoStream
import cv2
import numpy as np
from trackers.NCS2_Wrapper import NCS2_Wrapper

#from trackers.TFLite_Wrapper import TFLite_Wrapper

get_box_area = lambda box: box[0]
get_box_center = lambda box: (int(box[0] + ((box[2] - box[0])//2)), int(box[1] + ((box[3] - box[1]) //2)))
distance = lambda p1, p2: ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**.5

try:
    camera = VideoStream(usePiCamera=True)
    camera.start()
    camera_matrix = np.load("camera_matrix.npy")
    dist_coefficients = np.load("dist_coefficients.npy")
except Exception as e:
    raise(e)

water_gun = WaterGun()
water_gun.start()
water_gun.center()

tracker = NCS2_Wrapper(filter_for = set(["person", "dog"]))
#tracker = TFLite_Wrapper("Sample_TFLite_model")

lock_start = time.time()
last_detection = time.time()

scan_mode_started = False
scan_pass_start = time.time()
scan_time = 2
scan_value = 100
while True:
    frame = camera.read()
    frame = cv2.flip(frame, 0)
    #frame = cv2.undistort(frame, camera_matrix, dist_coefficients, None, camera_matrix)
    
    cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 5, (255,0,255), -1)
    
    boxes = tracker.update(frame)
    if len(boxes) > 0:
        box = boxes[0]
        last_detection = time.time()
    else:
        box = None

    if type(box) != type(None):
        cv2.rectangle(frame, tuple(box[:2]),  tuple(box[2:]), (10, 255, 0), 2)

        box_center = get_box_center(box)
        cv2.circle(frame, box_center, 5, (0,0,255), -1)

        norm_box_center = (box_center[0]/frame.shape[1], box_center[1]/frame.shape[0])
      
        lock_dist = distance(norm_box_center, (.5,.5))
        if lock_dist <= .15:
            if time.time() - lock_start >= 1:
                print("Firing")
                lock_start = time.time()
                water_gun.shoot(duration=1, bump = 10)
        else:
            lock_start = time.time()
            water_gun.pan += 1 if norm_box_center[0] < .5 else -1
            water_gun.tilt += 1 if norm_box_center[1] > .5 else -1
        

    if False and (time.time() - last_detection) > 10:
        if not scan_mode_started:
            water_gun.center()
            scan_mode_started = True

        if (time.time() - scan_pass_start) > scan_time:
            scan_value = 0 if scan_value == 100 else 100
            water_gun.pan = scan_value

    cv2.imshow("dd", frame)
    cv2.waitKey(1)